"""
P(R_claude > R_rival) a 6 meses para distintos niveles de exposicion.
Solo stdlib. Supuestos explicitos arriba de cada bloque. Uso:
    python3 p_ganar_torneo.py            # tablas analiticas + Monte Carlo (10,000 trayectorias)
    python3 p_ganar_torneo.py 20000      # mas trayectorias
Todos los rendimientos son EN EXCESO sobre un mismo rendimiento de efectivo (CETES/cash);
el tipo de cambio se trata como parte del factor comun (ambas cuentas en activos en USD).
"""
import math, random, statistics, sys

T = 0.5          # horizonte: 6 meses
DIAS = 126       # dias habiles en 6 meses
def Phi(x):      # CDF normal estandar
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

# ---------------------------------------------------------------------------
# 1) MODELO ANALITICO (log-normal, rebalanceo continuo)
#    Cuenta i: exposicion k_i al factor comun M (mu_e, sigma), ruido idiosincratico s_i,
#    costo anual c_i, alfa anual a_i. Log-rendimiento en T:
#    X_i = [a_i + k_i*mu_e - (k_i^2*sigma^2 + s_i^2)/2 - c_i]*T + k_i*sigma*W_T + s_i*Z_i*sqrt(T)
#    D = X_c - X_r es normal => P(gana Claude) = Phi(E[D]/sd[D]).
# ---------------------------------------------------------------------------
def p_analitica(k_c, k_r, mu_e, sigma, s_c=0.0, s_r=0.0, c_c=0.0, c_r=0.0, a_c=0.0, a_r=0.0, tau=T, ventaja_log=0.0):
    m_c = a_c + k_c * mu_e - (k_c**2 * sigma**2 + s_c**2) / 2 - c_c
    m_r = a_r + k_r * mu_e - (k_r**2 * sigma**2 + s_r**2) / 2 - c_r
    media = ventaja_log + (m_c - m_r) * tau
    sd = math.sqrt(((k_c - k_r)**2 * sigma**2 + s_c**2 + s_r**2) * tau)
    if sd == 0:
        return 1.0 if media > 0 else (0.5 if media == 0 else 0.0)
    return Phi(media / sd)

def costo_letf(k):   # comision anual implicita de ETF apalancado (supuesto: 1%/ano como Gayed-Bilello)
    return 0.01 if k > 1 else 0.001

def tabla_analitica():
    sigma = 0.20
    escenarios = [("bajista", -0.10, 0.25), ("base", 0.08, 0.50), ("alcista", 0.20, 0.25)]
    rivales = [
        ("R-conservador  k=0.8 s=5%",  0.8, 0.05),
        ("R-concentrado  k=1.3 s=30%", 1.3, 0.30),
        ("R-apalancado   k=2.5 s=15%", 2.5, 0.15),
    ]
    exposiciones = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    print("\n=== 1) P(Claude > rival) analitica, sigma_M=20%, T=6m, ponderada por escenario (25% bajista -10%, 50% base +8%, 25% alcista +20%) ===")
    print("Claude sin ruido idiosincratico (ETF de indice / ETF apalancado). Costos: 1%/ano si k>1.")
    print("rival \\ k_Claude       " + " ".join(f"{k:>6.1f}" for k in exposiciones))
    for nombre, k_r, s_r in rivales:
        fila = []
        for k in exposiciones:
            p = sum(w * p_analitica(k, k_r, mu, sigma, 0.0, s_r, costo_letf(k), 0.005) for _, mu, w in escenarios)
            fila.append(p)
        print(f"{nombre:24s}" + " ".join(f"{p:6.1%}" for p in fila))
    print("\nMismo calculo por escenario de mercado (rival concentrado k=1.3, s=30%):")
    for esc, mu, _ in escenarios:
        print(f"  {esc:8s} mu_e={mu:+.0%}: " + " ".join(f"k={k:.1f}:{p_analitica(k, 1.3, mu, sigma, 0, 0.30, costo_letf(k), 0.005):5.1%}" for k in exposiciones))

    print("\n=== 2) Formula de 'carrera de beta pura' (sin ruido idiosincratico, k_c > k_r) ===")
    print("P = Phi( sqrt(T) * (mu_e - (k_c + k_r) * sigma^2 / 2) / sigma )  -> no depende de CUANTO mas expuesto estes, solo de la suma")
    for mu in (-0.10, 0.0, 0.08, 0.15, 0.20):
        print(f"  mu_e={mu:+.0%}: " + " ".join(
            f"(k_c={kc},k_r={kr}):{p_analitica(kc, kr, mu, sigma):5.1%}" for kc, kr in ((1.5, 1.0), (2.0, 1.0), (3.0, 1.0), (3.0, 2.0))))

    print("\n=== 3) Ventaja por habilidad: P ~ Phi(IR * sqrt(T)), IR = razon de informacion de la DIFERENCIA ===")
    for ir in (0.0, 0.25, 0.5, 0.75, 1.0, 1.5):
        print(f"  IR={ir:.2f}: P(gana en 6m)={Phi(ir * math.sqrt(T)):5.1%}")

    print("\n=== 4) Kelly: crecimiento mediano g(k)=k*mu_e - k^2*sigma^2/2 (anual, en exceso), sigma=20% ===")
    for mu in (0.05, 0.08, 0.15):
        kstar = mu / sigma**2
        print(f"  mu_e={mu:.0%}: k*={kstar:.2f}  " + " ".join(f"g({k:.0f})={k*mu - k*k*sigma*sigma/2:+.1%}" for k in (1, 2, 3, 4)))

    print("\n=== 5) Estrategia segun marcador: P(gana) a mitad de temporada (quedan 3 meses), mu_e=8%, sigma=20% ===")
    print("Filas: ventaja actual (pp de log-rendimiento). Columnas: tracking error anual de la diferencia (via |k_c-k_r|*sigma).")
    tes = [0.02, 0.05, 0.10, 0.20, 0.40]
    print("ventaja \\ TE        " + " ".join(f"{te:>6.0%}" for te in tes))
    for lead in (-0.10, -0.05, 0.0, 0.05, 0.10):
        fila = []
        for te in tes:
            dk = te / sigma
            fila.append(p_analitica(1.0 + dk, 1.0, 0.08, sigma, tau=0.25, ventaja_log=lead))
        print(f"  {lead:+.0%}               " + " ".join(f"{p:6.1%}" for p in fila))

# ---------------------------------------------------------------------------
# 2) MONTE CARLO con regimenes (colas gordas y agrupamiento de volatilidad), ETFs con reinicio diario,
#    filtro de tendencia SMA200 + costos de GBM.
#    Factor M: 2 regimenes Markov. Calma: mu=+16%/ano, vol=13%; estres: mu=-15%/ano, vol=35%.
#    P(calma->estres)=1/120 por dia, P(estres->calma)=1/40 -> 25% del tiempo en estres;
#    mu incondicional ~ +8%/ano, vol incondicional ~ 21%. Arranque de temporada en calma
#    (hecho al 24-sep-2026: S&P 500 +7% sobre su SMA200 y VIX 15.7).
#    Costos: comision GBM 0.29% por lado (0.25% + IVA) + 0.10% de spread; ETF apalancado 1%/ano; ETF 1x 0.1%/ano.
# ---------------------------------------------------------------------------
COM = 0.0029 + 0.0010
# Mezcla "rival tipo Grok" (supuesto, ver documento 03): 40% concentrado, 25% 3x, 20% trader activo, 15% conservador
PESOS_RIVAL_GROK = (0.40, 0.25, 0.20, 0.15)
REGIMENES = {
    # A: estres corto y volatil (tendencia poco persistente). mu incondicional ~ +8%, vol ~ 21%
    "A_estres_corto": dict(mu_c=0.16, sd_c=0.13, mu_s=-0.15, sd_s=0.35, p_cs=1 / 120, p_sc=1 / 40),
    # B: mercados bajistas persistentes (lo que explota el filtro SMA200). mu incondicional ~ +8%, vol ~ 18%
    "B_bajista_persistente": dict(mu_c=0.20, sd_c=0.12, mu_s=-0.30, sd_s=0.30, p_cs=1 / 250, p_sc=1 / 80),
}
def simula(n, semilla=7, regimen="A_estres_corto"):
    rng = random.Random(semilla)
    g = REGIMENES[regimen]
    mu_c, sd_c = g["mu_c"] / 252, g["sd_c"] / math.sqrt(252)
    mu_s, sd_s = g["mu_s"] / 252, g["sd_s"] / math.sqrt(252)
    p_cs, p_sc = g["p_cs"], g["p_sc"]
    nombres_c = ["C0 efectivo", "C1 indice 1x", "C2 2x comprar-mantener", "C3 3x comprar-mantener",
                 "C4 2x con filtro SMA200", "C5 3x con filtro SMA200", "C6 barbell 60% cash + 40% 3x filtro",
                 "C7 momentum concentrado (1.3x, s=20%, alfa 4%)", "C7b igual que C7 pero alfa 0%",
                 "C8 2x con filtro SMA200 y banda 3%"]
    nombres_r = ["R1 concentrado (1.3x, s=30%)", "R2 3x comprar-mantener", "R3 trader sin ventaja (0-2x semanal)",
                 "R4 conservador (0.6x)"]
    finales_c = {c: [] for c in nombres_c}
    finales_r = {r: [] for r in nombres_r}
    finales_c9 = {}
    for _ in range(n):
        # 200 dias de historia para la SMA200, luego 126 dias de temporada
        # Historia condicionada al estado actual (hecho al 24-sep-2026): precio entre +4% y +10% sobre su SMA200
        while True:
            estado = 0
            precios = [100.0]
            for _d in range(200):
                if estado == 0 and rng.random() < p_cs: estado = 1
                elif estado == 1 and rng.random() < p_sc: estado = 0
                mu, sd = (mu_c, sd_c) if estado == 0 else (mu_s, sd_s)
                precios.append(precios[-1] * math.exp(mu - sd * sd / 2 + sd * rng.gauss(0, 1)))
            if 1.04 <= precios[-1] / (sum(precios[-200:]) / 200) <= 1.10:
                break
        estado = 0  # arranque en calma
        v = {c: 1.0 for c in nombres_c}
        w = {r: 1.0 for r in nombres_r}
        # costos de entrada (compra inicial)
        for c in nombres_c[1:]: v[c] *= (1 - COM)
        for r in nombres_r: w[r] *= (1 - COM)
        dentro = {"C4": None, "C5": None, "C6": None}
        dentro_c8 = True  # arranca dentro (precio +4% a +10% sobre SMA200)
        exp_r3 = 1.0
        # C9 (modo torneo): igual que C8 hasta la mitad; en el dia 63 compara contra CADA rival:
        #   atras >=5% -> 3x con el mismo filtro; adelante >=5% -> copia la beta estimada del rival (sin filtro);
        #   en otro caso sigue igual. Se calcula una trayectoria de C9 por rival.
        BETA_RIVAL = {"R1 concentrado (1.3x, s=30%)": 1.3, "R2 3x comprar-mantener": 3.0,
                      "R3 trader sin ventaja (0-2x semanal)": 1.0, "R4 conservador (0.6x)": 0.6}
        # Variantes de modo torneo: (nombre, k_base, k_atras, usa_filtro_banda)
        VARIANTES9 = [("C9 = C8 + modo torneo", 2.0, 3.0, True),
                      ("C10 = 2x sin filtro + modo torneo", 2.0, 3.0, False),
                      ("C11 = 1x sin filtro + modo torneo (atras->2x)", 1.0, 2.0, False)]
        v9 = {(vn, r_): 1.0 - COM for vn, _, _, _ in VARIANTES9 for r_ in nombres_r}
        modo9 = {(vn, r_): "normal" for vn, _, _, _ in VARIANTES9 for r_ in nombres_r}
        sleeve_letf, sleeve_cash = 0.4 * v["C6 barbell 60% cash + 40% 3x filtro"], 0.6 * v["C6 barbell 60% cash + 40% 3x filtro"]
        for d in range(DIAS):
            sma = sum(precios[-200:]) / 200
            senal = precios[-1] > sma
            for clave in dentro:
                if dentro[clave] is None:
                    dentro[clave] = senal
                elif dentro[clave] != senal:
                    dentro[clave] = senal
                    if clave == "C4": v["C4 2x con filtro SMA200"] *= (1 - COM)
                    if clave == "C5": v["C5 3x con filtro SMA200"] *= (1 - COM)
                    if clave == "C6": sleeve_letf *= (1 - COM)
            # C8: sale solo si cierra >3% debajo de la SMA200; reentra al cerrar arriba de la SMA200
            if dentro_c8 and precios[-1] < 0.97 * sma:
                dentro_c8 = False; v["C8 2x con filtro SMA200 y banda 3%"] *= (1 - COM)
            elif (not dentro_c8) and precios[-1] > sma:
                dentro_c8 = True; v["C8 2x con filtro SMA200 y banda 3%"] *= (1 - COM)
            if d == 63:
                for key in v9:
                    ventaja = v9[key] / w[key[1]] - 1
                    if ventaja <= -0.05: modo9[key] = "atras"; v9[key] *= (1 - 2 * COM)
                    elif ventaja >= 0.05: modo9[key] = "adelante"; v9[key] *= (1 - 2 * COM)
            if d % 5 == 0:  # R3 cambia exposicion cada semana al azar
                nueva = rng.choice((0.0, 1.0, 2.0))
                if nueva != exp_r3:  # a/desde efectivo = 1 lado; cambio de instrumento = 2 lados
                    lados = 1 if 0.0 in (nueva, exp_r3) else 2
                    w["R3 trader sin ventaja (0-2x semanal)"] *= (1 - COM * lados)
                    exp_r3 = nueva
            if estado == 0 and rng.random() < p_cs: estado = 1
            elif estado == 1 and rng.random() < p_sc: estado = 0
            mu, sd = (mu_c, sd_c) if estado == 0 else (mu_s, sd_s)
            r = math.exp(mu - sd * sd / 2 + sd * rng.gauss(0, 1)) - 1  # rendimiento simple diario del factor
            precios.append(precios[-1] * (1 + r))
            f1, f2 = 0.001 / 252, 0.01 / 252
            v["C1 indice 1x"] *= (1 + r - f1)
            v["C2 2x comprar-mantener"] *= max(0.0, 1 + 2 * r - f2)
            v["C3 3x comprar-mantener"] *= max(0.0, 1 + 3 * r - f2)
            if dentro["C4"]: v["C4 2x con filtro SMA200"] *= max(0.0, 1 + 2 * r - f2)
            if dentro["C5"]: v["C5 3x con filtro SMA200"] *= max(0.0, 1 + 3 * r - f2)
            if dentro["C6"]: sleeve_letf *= max(0.0, 1 + 3 * r - f2)
            e7 = 0.20 / math.sqrt(252) * rng.gauss(0, 1)
            v["C7 momentum concentrado (1.3x, s=20%, alfa 4%)"] *= max(0.0, (1 + 1.3 * r) * math.exp(e7 - 0.20**2 / 504) + 0.04 / 252 - f1)
            v["C7b igual que C7 pero alfa 0%"] *= max(0.0, (1 + 1.3 * r) * math.exp(e7 - 0.20**2 / 504) - f1)
            if dentro_c8: v["C8 2x con filtro SMA200 y banda 3%"] *= max(0.0, 1 + 2 * r - f2)
            for vn, kbase, katras, filtro in VARIANTES9:
                for r_ in nombres_r:
                    key = (vn, r_)
                    if modo9[key] == "adelante":
                        kb = BETA_RIVAL[r_]; v9[key] *= max(0.0, 1 + kb * r - (f2 if kb > 1 else f1))
                    elif dentro_c8 or not filtro:
                        kk = katras if modo9[key] == "atras" else kbase
                        v9[key] *= max(0.0, 1 + kk * r - (f2 if kk > 1 else f1))
            e1 = 0.30 / math.sqrt(252) * rng.gauss(0, 1)
            w["R1 concentrado (1.3x, s=30%)"] *= max(0.0, (1 + 1.3 * r) * math.exp(e1 - 0.30**2 / 504) - f1)
            w["R2 3x comprar-mantener"] *= max(0.0, 1 + 3 * r - f2)
            w["R3 trader sin ventaja (0-2x semanal)"] *= max(0.0, 1 + exp_r3 * r - (f2 if exp_r3 > 1 else f1))
            w["R4 conservador (0.6x)"] *= (1 + 0.6 * r - f1)
        v["C6 barbell 60% cash + 40% 3x filtro"] = sleeve_letf + sleeve_cash
        for c in nombres_c: finales_c[c].append(v[c] - 1)
        for r_ in nombres_r: finales_r[r_].append(w[r_] - 1)
        for key in v9: finales_c9.setdefault(key, []).append(v9[key] - 1)
    return nombres_c, nombres_r, finales_c, finales_r, finales_c9

def reporte_mc(n, regimen):
    nc, nr, fc, fr, f9 = simula(n, regimen=regimen)
    print(f"\n=== 6) Monte Carlo [{regimen}], {n} trayectorias, 6 meses (rendimiento en exceso de efectivo) ===")
    print(f"{'estrategia':46s} {'mediana':>8s} {'p5':>8s} {'p95':>8s} {'P(<-35%)':>9s}  " + "  ".join(f"vs {r[:2]}" for r in nr) + "  promedio  mezcla_grok")
    for c in nc:
        xs = sorted(fc[c])
        med, p5, p95 = xs[n // 2], xs[int(0.05 * n)], xs[int(0.95 * n)]
        ruina = sum(1 for x in xs if x < -0.35) / n
        ps = [sum(1.0 if a > b else (0.5 if a == b else 0.0) for a, b in zip(fc[c], fr[r])) / n for r in nr]  # empate = 1/2
        mezcla = sum(wi * pi for wi, pi in zip(PESOS_RIVAL_GROK, ps))
        print(f"{c:46s} {med:8.1%} {p5:8.1%} {p95:8.1%} {ruina:9.1%}  " + "  ".join(f"{p:5.1%}" for p in ps) + f"  {statistics.mean(ps):6.1%}  {mezcla:6.1%}")
    for vn in sorted({k[0] for k in f9}):
        ps9 = [sum(1.0 if a > b else (0.5 if a == b else 0.0) for a, b in zip(f9[(vn, r)], fr[r])) / n for r in nr]
        ruina9 = statistics.mean(sum(1 for x in f9[(vn, r)] if x < -0.35) / n for r in nr)
        print(f"{vn:46s} {'':>8s} {'':>8s} {'':>8s} {ruina9:9.1%}  " + "  ".join(f"{p:5.1%}" for p in ps9)
              + f"  {statistics.mean(ps9):6.1%}  {sum(wi * pi for wi, pi in zip(PESOS_RIVAL_GROK, ps9)):6.1%}")
    print("\nRivales (referencia):")
    for r in nr:
        xs = sorted(fr[r])
        print(f"  {r:40s} mediana {xs[n//2]:6.1%}  p5 {xs[int(0.05*n)]:6.1%}  p95 {xs[int(0.95*n)]:6.1%}")

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    tabla_analitica()
    for reg in REGIMENES:
        reporte_mc(n, reg)
