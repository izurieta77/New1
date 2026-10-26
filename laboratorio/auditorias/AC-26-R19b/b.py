"""AC-26-R19b · Ejecución B independiente de R19b (parte de AC-25-R19/b.py, biblioteca estándar).

Pregunta (pre-registro R19b, commit 4755d91): arrastre fiscal TOTAL de la mezcla de papel en MXN,
1994-01-03 a 2026-10-16 = CAGR sin ningún impuesto − CAGR con ISR art. 129 (10%) + impuesto al
dividendo de la manga S&P (τ_div) + impuesto al interés nominal del efectivo en CETES (τ_int).

Fuente B (distinta de A en todo lo que se pudo):
  - S&P 500: CBOE SPX (precio) + rendimiento por dividendo mensual de multpl.  [A: ^SP500TR − ^GSPC]
    El dividendo diario = yield multpl del mes / 252 × días hábiles; se grava a τ_div y se reinvierte
    el neto sin comisión y sin tocar el costo fiscal (regla §4 de R19b).
  - VIX: CBOE VIX_History.  Nasdaq-100: FRED NASDAQ100 (precio).  Tasa USD (financiamiento UPRO): FRED DTB3.
  - USD/MXN: Banxico SIE, FIX (SF43718), diario.            [A: FRED DEXMXUS]
  - INPC: Banxico SIE, SP1, mensual hasta sep-2026.          [A: OCDE MEXCPIALLMINMEI + 4%]
  - CETES: Banxico SIE SF43936, tasa de rendimiento de la subasta semanal de CETES 28 días,
    se arrastra el último dato; devenga tasa/360 × días naturales.  [A: FRED INTGSTMXM193N mensual]
  - Efectivo (5.3% núcleo + manga UPRO apagada) en MXN: en USD dentro del modelo, cada día
    × (1 + i_CETES·(1−τ_int)) × FIX(t−1)/FIX(t).
Uso: python3 -I b.py <carpeta_datos> <salida_json> [banderas]
"""
import csv, json, math, re, sys, datetime as dt

DATOS = sys.argv[1] if len(sys.argv) > 1 else "datos"
SALIDA = sys.argv[2] if len(sys.argv) > 2 else "b-resultados.json"
# Sensibilidades (solo para explicar diferencias con A; la corrida base no lleva banderas):
#   comis_fuera  : comisiones fuera de la base fiscal (costo sin comisión de compra, venta bruta)
#   reentrada_w  : al reentrar, UPRO se compra al 26.9% del total (no con la manga), tope el efectivo
#   fx_dexmxus   : USD/MXN de FRED DEXMXUS (copia de A en R19-datos) en lugar del FIX
#   cpi_ocde     : OCDE MEXCPIALLMINMEI + 4% anual desde 2024-08 (como A) en lugar del INPC
#   caja_usd     : efectivo en USD a DTB3 sin impuesto (control: reproduce R19/AC-25 con τ_div = 0)
#   upro_div     : también se grava 1× el dividendo del S&P dentro de UPRO (sensibilidad)
# El §4 de R19b manda conservar las desviaciones de A en R19: correr con "comis_fuera,reentrada_w".
BANDERAS = set(sys.argv[3].split(",")) if len(sys.argv) > 3 and sys.argv[3] else set()
INI, FIN = dt.date(1994, 1, 3), dt.date(2026, 10, 16)
C = 0.0029            # comisión GBM 0.25% + IVA, por operación (compra y venta)
ISR = 0.10
W = {"spym": 0.410, "qqqm": 0.268, "upro": 0.269}   # efectivo 5.3%
W_CASH = 0.053
G_SPYM, G_QQQM, G_UPRO = 0.0002, 0.0015, 0.0091


# ---------------------------------------------------------------- lectura
def mdy(s):
    m, d, y = s.split("/"); return dt.date(int(y), int(m), int(d))


def dmy(s):
    d, m, y = s.split("/"); return dt.date(int(y), int(m), int(d))


def leer_cboe(nombre, col):
    out = {}
    with open(f"{DATOS}/{nombre}") as f:
        for r in csv.DictReader(f):
            try:
                v = float(r[col])
            except (ValueError, KeyError):
                continue
            if v > 0:
                out[mdy(r["DATE"])] = v
    return out


def leer_fred(nombre):
    out = {}
    with open(f"{DATOS}/{nombre}") as f:
        rd = csv.reader(f); next(rd)
        for d, v in rd:
            try:
                out[dt.date.fromisoformat(d)] = float(v)
            except ValueError:
                pass
    return out


def leer_banxico(nombre):
    out = {}
    with open(f"{DATOS}/{nombre}", encoding="latin-1") as f:
        for linea in f:
            m = re.match(r"^(\d\d/\d\d/\d{4}),([\d.]+)\s*$", linea)
            if m:
                out[dmy(m.group(1))] = float(m.group(2))
    return out


def leer_multpl():
    t = open(f"{DATOS}/multpl_sp500_dividend_yield_by_month.html", encoding="utf-8").read()
    filas = re.findall(r"<td>([A-Z][a-z]{2} \d{1,2}, \d{4})</td>\s*<td>(.*?)</td>", t, re.S)
    out = {}
    for d, v in filas:
        f = dt.datetime.strptime(d, "%b %d, %Y").date()
        y = float(re.search(r"([\d.]+)%", v).group(1)) / 100
        k = (f.year, f.month)
        if k not in out or f.day > out[k][0]:
            out[k] = (f.day, y)
    return {k: v[1] for k, v in out.items()}


spx = leer_cboe("SPX_History_cboe.csv", "SPX")
vix = leer_cboe("VIX_History.csv", "CLOSE")
ndx = leer_fred("NASDAQ100.csv")
tb = leer_fred("DTB3.csv")
dy = leer_multpl()
fix = leer_banxico("banxico_fix_SF43718.csv")
inpc_d = leer_banxico("banxico_inpc_SP1.csv")
cetes = leer_banxico("banxico_cetes28_SF43936.csv")
INPC = {(d.year, d.month): v for d, v in inpc_d.items()}
if "fx_dexmxus" in BANDERAS:
    fix = leer_fred("../../../replicas/R19-datos/DEXMXUS.csv")
if "cpi_ocde" in BANDERAS:
    INPC = {(d.year, d.month): v for d, v in leer_fred("../../../replicas/R19-datos/MEXCPIALLMINMEI.csv").items()}
    y, m = max(INPC); v = INPC[(y, m)]
    while (y, m) < (2026, 12):
        m += 1
        if m == 13:
            y, m = y + 1, 1
        v *= 1.04 ** (1 / 12); INPC[(y, m)] = v

# Días: SPX ∩ VIX ∩ NDX (tasa y FX con último dato disponible).
dias = sorted(d for d in spx if d in vix and d in ndx and d <= FIN)
n = len(dias)
assert dias[-1] == FIN, dias[-1]


def arrastrar(serie):
    ks = sorted(serie); out = []; j = 0; ult = None
    for d in dias:
        while j < len(ks) and ks[j] <= d:
            ult = serie[ks[j]]; j += 1
        out.append(ult)
    return out


RFa, FX, CET = arrastrar(tb), arrastrar(fix), arrastrar(cetes)
DH = [1] + [sum(1 for k in range(1, (dias[i] - dias[i - 1]).days + 1)
                if (dias[i - 1] + dt.timedelta(k)).weekday() < 5) for i in range(1, n)]
RF = [RFa[i] / 100 / 252 * DH[i] for i in range(n)]
# CETES: tasa vigente al cierre de i−1, devengo simple por días naturales / 360
RC = [0.0] + [CET[i - 1] / 100 / 360 * (dias[i] - dias[i - 1]).days for i in range(1, n)]
r_px = [0.0] * n; r_div = [0.0] * n
r_tr = [0.0] * n; r_ndx = [0.0] * n
for i in range(1, n):
    r_px[i] = spx[dias[i]] / spx[dias[i - 1]] - 1
    r_div[i] = dy[(dias[i].year, dias[i].month)] / 252 * DH[i]
    r_tr[i] = r_px[i] + r_div[i]
    r_ndx[i] = ndx[dias[i]] / ndx[dias[i - 1]] - 1

# Filtro V0: SMA200 sobre TODOS los cierres de SPX (no solo los comunes), con histéresis.
spx_d = sorted(spx); est_spx = {}; on = None; suma = 0.0
for k, d in enumerate(spx_d):
    suma += spx[d]
    if k >= 200:
        suma -= spx[spx_d[k - 200]]
    if k < 199 or d not in vix:
        continue
    sma = suma / 200; p = spx[d]; v = vix[d]
    if on is None:
        on = p > sma and v < 25
    elif on and (p < sma * 0.97 or v >= 25):
        on = False
    elif (not on) and p > sma and v < 25:
        on = True
    est_spx[d] = on
estado = [est_spx.get(d) for d in dias]

i_ini = dias.index(INI)


def r_upro(i):  # rendimiento del día i con UPRO invertido
    return 3 * r_tr[i] - 2 * RF[i] - G_UPRO / 252 * DH[i]


def ret(k, i, td):
    """Rendimiento del día i de la emisora k, neto del impuesto al dividendo τ_div = td.
    Regresa (rendimiento, impuesto al dividendo como fracción de la posición)."""
    if k == "spym":
        return r_tr[i] - td * r_div[i] - G_SPYM / 252 * DH[i], td * r_div[i]
    if k == "sp500tr":
        return r_tr[i] - td * r_div[i], td * r_div[i]
    if k == "qqqm":
        return r_ndx[i] - G_QQQM / 252 * DH[i], 0.0
    t = td * r_div[i] if "upro_div" in BANDERAS else 0.0
    return r_upro(i) - t, t


def inpc(y, m):
    while (y, m) not in INPC:      # no ocurre en 1994-2026 (SP1 llega a sep-2026)
        m -= 1
        if m == 0:
            y, m = y - 1, 12
    return INPC[(y, m)]


def mes_menos(d, k):
    y, m = d.year, d.month - k
    while m <= 0:
        y, m = y - 1, m + 12
    return y, m


# ---------------------------------------------------------------- simulación
def simular(variante, con_isr, td=0.0, ti=0.0):
    """variante: M (rebalanceo mensual), A (anual, enero), F (solo filtro), B (100% S&P TR)."""
    etfs = ["sp500tr"] if variante == "B" else ["spym", "qqqm", "upro"]
    pos = {k: 0.0 for k in etfs}                     # valor USD de cada emisora
    base = {k: {"usd": 0.0, "mxn": 0.0, "real": 0.0} for k in etfs}  # costo promedio agregado
    caja, caja_upro = 0.0, 0.0                       # efectivo núcleo y manga UPRO apagada (USD)
    reg = {"ops": 0, "comis_usd": 0.0, "g_mxn_nom": 0.0, "g_usd_fx": 0.0,
           "isr_mxn": 0.0, "div_mxn": 0.0, "int_mxn": 0.0, "pagos": 0, "ganancia_anual": {}, "base_gravable": {}}
    perdidas = []                                    # [(año, monto)] pendientes, sin actualizar
    g_año = {}                                       # ganancia fiscal neta por año calendario

    def comprar(k, monto, i):                        # monto = efectivo gastado (incluye comisión)
        if monto <= 0:
            return
        val = monto / (1 + C); pos[k] += val
        fxi = FX[i]; y, m = mes_menos(dias[i], 1)
        cb = val if "comis_fuera" in BANDERAS else monto
        base[k]["usd"] += cb; base[k]["mxn"] += cb * fxi
        base[k]["real"] += cb * fxi / inpc(y, m)
        reg["ops"] += 1; reg["comis_usd"] += monto - val

    def vender(k, val, i):                           # val = valor de mercado vendido; regresa neto
        if val <= 0:
            return 0.0
        q = min(1.0, val / pos[k]) if pos[k] > 0 else 1.0
        neto = val * (1 - C); fxi = FX[i]
        nb = val if "comis_fuera" in BANDERAS else neto   # monto que entra a la base fiscal
        b = base[k]
        c_usd, c_nom, c_real = q * b["usd"], q * b["mxn"], q * b["real"]
        y, m = mes_menos(dias[i], 2)
        c_act = max(c_nom, c_real * inpc(y, m))      # factor del agregado, nunca < 1
        gan = nb * fxi - c_act
        g_año[dias[i].year] = g_año.get(dias[i].year, 0.0) + gan
        reg["g_mxn_nom"] += nb * fxi - c_nom
        reg["g_usd_fx"] += (nb - c_usd) * fxi
        b["usd"] -= c_usd; b["mxn"] -= c_nom; b["real"] -= c_real
        pos[k] -= val
        if pos[k] < 1e-14:
            pos[k] = 0.0
        reg["ops"] += 1; reg["comis_usd"] += val * C
        return neto

    def impuesto_año(y):                             # neteo + pérdidas de hasta 10 años
        g = g_año.get(y, 0.0)
        nonlocal perdidas
        perdidas = [(a, p) for a, p in perdidas if y - a <= 10]
        if g <= 0:
            if g < 0:
                perdidas.append((y, -g))
            reg["base_gravable"][y] = 0.0
            return 0.0
        resto = []
        for a, p in perdidas:                        # se aplican las más antiguas primero
            uso = min(p, g); g -= uso
            if p - uso > 1e-12:
                resto.append((a, p - uso))
        perdidas = resto
        reg["base_gravable"][y] = g
        return ISR * g

    def total():
        return sum(pos.values()) + caja + caja_upro

    def rebalancear(i, upro_on):
        nonlocal caja, caja_upro
        wt = {"sp500tr": 1.0} if variante == "B" else dict(W)
        if variante != "B" and not upro_on:
            wt["upro"] = 0.0
        tot = total(); tot2 = tot
        for _ in range(30):                          # punto fijo: comisiones salen del total
            com = sum(abs(wt[k] * tot2 - pos[k]) for k in etfs) * C
            tot2 = tot - com
        # primero ventas (liberan efectivo), luego compras
        caja += caja_upro; caja_upro = 0.0
        for k in etfs:
            obj = wt[k] * tot2
            if pos[k] > obj + 1e-15:
                caja += vender(k, pos[k] - obj, i)
        for k in etfs:
            obj = wt[k] * tot2
            if obj > pos[k] + 1e-15:
                dif = obj - pos[k]; caja -= dif * (1 + C); comprar(k, dif * (1 + C), i)
        if variante != "B" and not upro_on:
            caja_upro = W["upro"] * tot2; caja -= caja_upro

    # Compra inicial al cierre de 1994-01-03 (estado del filtro para el rendimiento de 01-04: t-2).
    caja = 1.0 / FX[i_ini]                           # 1 MXN convertido a USD
    upro_on = bool(estado[i_ini - 1])
    rebalancear(i_ini, upro_on)
    m0 = 1.0
    for i in range(i_ini + 1, n):
        # rendimientos del día i
        for k in etfs:
            r, t = ret(k, i, td)
            reg["div_mxn"] += pos[k] * t * FX[i]
            pos[k] *= 1 + r
        if "caja_usd" in BANDERAS:
            caja *= 1 + RF[i]; caja_upro *= 1 + RF[i]
        else:                                          # efectivo en MXN a CETES, τ_int al interés nominal
            reg["int_mxn"] += (caja + caja_upro) * FX[i - 1] * RC[i] * ti
            f = (1 + RC[i] * (1 - ti)) * FX[i - 1] / FX[i]
            caja *= f; caja_upro *= f
        if i == n - 1:
            break
        # decisiones al cierre de i (aplican al rendimiento de i+1; señal del cierre de i-1)
        nuevo = bool(estado[i - 1])
        nuevo_mes = dias[i].month != dias[i - 1].month
        reb = (variante == "M" and nuevo_mes) or (variante == "A" and nuevo_mes and dias[i].month == 1)
        if variante != "B":
            if reb:
                rebalancear(i, nuevo)
            elif nuevo != upro_on:
                if not nuevo:                         # salida: vender todo UPRO
                    caja_upro += vender("upro", pos["upro"], i)
                elif "reentrada_w" in BANDERAS:       # sensibilidad: al 26.9% del total
                    caja += caja_upro; caja_upro = 0.0
                    monto = min(W["upro"] * total() * (1 + C), caja)
                    caja -= monto; comprar("upro", monto, i)
                else:                                 # entrada: recomprar con toda la manga
                    comprar("upro", caja_upro, i); caja_upro = 0.0
            upro_on = nuevo
        elif reb:
            rebalancear(i, True)
        # ISR del año anterior: primer día hábil de mayo, venta pro rata de todo
        if con_isr and nuevo_mes and dias[i].month == 5:
            y = dias[i].year - 1
            t_mxn = impuesto_año(y)
            reg["ganancia_anual"][y] = g_año.get(y, 0.0)
            if t_mxn > 0:
                t_usd = t_mxn / FX[i]
                disp = sum(pos.values()) * (1 - C) + caja + caja_upro
                f = t_usd / disp
                for k in etfs:
                    vender(k, pos[k] * f, i)
                caja *= 1 - f; caja_upro *= 1 - f
                reg["isr_mxn"] += t_mxn; reg["pagos"] += 1
    # Liquidación final al cierre del 2026-10-16
    i = n - 1
    usd = caja + caja_upro
    for k in etfs:
        usd += vender(k, pos[k], i)
    mxn = usd * FX[i]
    if con_isr:
        y = dias[i].year
        for yy in sorted(g_año):                      # años sin pago registrado (no debería haber)
            if yy < y and yy not in reg["base_gravable"]:
                t = impuesto_año(yy); mxn -= t; reg["isr_mxn"] += t
        t = impuesto_año(y); mxn -= t; reg["isr_mxn"] += t
        reg["ganancia_anual"][y] = g_año.get(y, 0.0)
    años = (dias[-1] - dias[i_ini]).days / 365.25
    reg["final_mxn"] = mxn
    reg["cagr_mxn"] = (mxn / m0) ** (1 / años) - 1
    reg["cagr_usd"] = (usd / (1.0 / FX[i_ini])) ** (1 / años) - 1
    reg["parte_cambiaria"] = 1 - reg["g_usd_fx"] / reg["g_mxn_nom"] if reg["g_mxn_nom"] else None
    reg["perdidas_vivas_al_final"] = sum(p for _, p in perdidas)
    return reg


out = {"fuente": "B: CBOE SPX + multpl div, CBOE VIX, FRED NASDAQ100, FRED DTB3, Banxico FIX SF43718, "
                 "Banxico INPC SP1, Banxico CETES 28 SF43936",
       "banderas": sorted(BANDERAS),
       "inicio": str(dias[i_ini]), "fin": str(dias[-1]), "dias": n - i_ini,
       "fx_ini": FX[i_ini], "fx_fin": FX[-1], "cetes_ini": CET[i_ini], "cetes_fin": CET[-1],
       "div_yield_medio": sum(r_div[i_ini + 1:]) / ((dias[-1] - dias[i_ini]).days / 365.25),
       "pct_v0_on_1994": sum(1 for i in range(i_ini + 1, n) if estado[i - 2]) / (n - i_ini - 1),
       "rejilla": {}, "sensibilidad_tdiv44": {}, "descomposicion_M_central": {}}
L = [f"Banderas: {','.join(sorted(BANDERAS)) or '(ninguna)'}",
     f"Periodo {out['inicio']} a {out['fin']} ({out['dias']} días). FIX {out['fx_ini']:.4f} -> {out['fx_fin']:.4f}. "
     f"CETES28 {out['cetes_ini']:.2f}% -> {out['cetes_fin']:.2f}%. Dividendo medio {out['div_yield_medio']:.2%}/año. "
     f"V0 encendido {out['pct_v0_on_1994']:.1%}",
     f"{'Var':3s} {'τdiv':>5s} {'τint':>5s} {'CAGR pre':>9s} {'CAGR post':>9s} {'arrastre':>9s} {'ops':>6s} "
     f"{'ISR/ini':>8s} {'Div/ini':>8s} {'Int/ini':>8s}"]
PRE = {}


def fila(v, td, ti):
    if v not in PRE:
        PRE[v] = simular(v, False)
    pre, post = PRE[v], simular(v, True, td, ti)
    d = {"tau_div": td, "tau_int": ti, "cagr_pre": pre["cagr_mxn"], "cagr_post": post["cagr_mxn"],
         "arrastre_pp": (pre["cagr_mxn"] - post["cagr_mxn"]) * 100, "cagr_usd_pre": pre["cagr_usd"],
         "final_mxn_pre": pre["final_mxn"], "final_mxn_post": post["final_mxn"], "ops_post": post["ops"],
         "isr_mxn": post["isr_mxn"], "imp_div_mxn": post["div_mxn"], "imp_int_mxn": post["int_mxn"],
         "parte_cambiaria_post": post["parte_cambiaria"]}
    L.append(f"{v:3s} {td:5.0%} {ti:5.0%} {d['cagr_pre']:9.3%} {d['cagr_post']:9.3%} {d['arrastre_pp']:8.3f}p "
             f"{d['ops_post']:6d} {post['isr_mxn']:8.2f} {post['div_mxn']:8.2f} {post['int_mxn']:8.2f}")
    return d


for td in (0.10, 0.20, 0.30):
    for ti in (0.0, 0.20):
        out["rejilla"][f"M_{td:.2f}_{ti:.2f}"] = fila("M", td, ti)
for v in ("A", "F", "B"):
    out["rejilla"][f"{v}_0.20_0.20"] = fila(v, 0.20, 0.20)
L.append("-- sensibilidad declarada: τ_div = 44% (t_m 35% + 9 pp, W-8BEN), τ_int = 20%")
for v in ("M", "F"):
    out["sensibilidad_tdiv44"][v] = fila(v, 0.44, 0.20)
L.append("-- descomposición M (solo ISR art.129 / ISR + τ_div 20% / ISR + τ_int 20% / todo)")
for nom, td, ti in (("solo_isr", 0, 0), ("isr_div", 0.2, 0), ("isr_int", 0, 0.2), ("todo", 0.2, 0.2)):
    out["descomposicion_M_central"][nom] = fila("M", td, ti)
M, F = out["rejilla"]["M_0.20_0.20"], out["rejilla"]["F_0.20_0.20"]
rng = [x["arrastre_pp"] for k, x in out["rejilla"].items() if k.startswith("M_")]
out["H1b"] = {"arrastre_M_pp": M["arrastre_pp"], "sostenida": M["arrastre_pp"] >= 1.0, "rango_M": [min(rng), max(rng)]}
out["H2b"] = {"M_menos_F_pp": M["arrastre_pp"] - F["arrastre_pp"], "sostenida": M["arrastre_pp"] - F["arrastre_pp"] >= 0.3}
L.append(f"\nH1b: arrastre M central = {M['arrastre_pp']:.3f} pp -> {'sostenida' if out['H1b']['sostenida'] else 'REFUTADA'} (>= 1.0); "
         f"rango M {min(rng):.2f}-{max(rng):.2f}")
L.append(f"H2b: M - F = {out['H2b']['M_menos_F_pp']:.3f} pp -> {'sostenida' if out['H2b']['sostenida'] else 'REFUTADA'} (>= 0.3)")
L.append("(ISR/ini, Div/ini, Int/ini = impuestos totales pagados en MXN por 1 MXN inicial)")
print("\n".join(L))
json.dump(out, open(SALIDA, "w"), indent=2, ensure_ascii=False, default=str)
