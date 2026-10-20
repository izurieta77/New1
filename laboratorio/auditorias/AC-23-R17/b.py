"""AC-23-R17, ejecución B independiente.

Escrito desde cero a partir del pre-registro R17 (commit 1a3bdda). No usa R17.py, R16.py ni R11.py.
Fuente B: CBOE SPX (precio) + dividend yield mensual de multpl (TR sintético), CBOE VIX,
FRED DTB3 (extendido con Treasury 13 semanas, descuento bancario, donde DTB3 no llega).
Solo biblioteca estándar.

Uso: python3 -I b.py [--deriva]
"""
import csv, datetime as dt, json, math, os, re, sys, hashlib

AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(AQUI, "datos")
FIN = dt.date(2026, 10, 16)
INICIO = dt.date(1990, 10, 1)        # H1: "1990-10 a 2026-10-16"
COSTO = 0.0010                       # por lado sobre nocional movido
GASTO = 0.0091                       # gasto anual del 3x
BANDA = 0.10
OBJETIVOS = {"VT30": 0.30, "VT45": 0.45, "VT60": 0.60}
DERIVA = "--deriva" in sys.argv      # sensibilidad: el peso deriva entre ajustes


def verificar_hashes():
    for linea in open(os.path.join(DATOS, "SHA256SUMS")):
        h, f = linea.split()
        real = hashlib.sha256(open(os.path.join(DATOS, f), "rb").read()).hexdigest()
        assert real == h, f"hash distinto: {f}"


def fecha_mdy(s):
    m, d, y = s.split("/")
    return dt.date(int(y), int(m), int(d))


def cargar():
    spx = {}
    for r in csv.DictReader(open(os.path.join(DATOS, "SPX_History_cboe.csv"))):
        v = float(r["SPX"])
        if v > 0:
            spx[fecha_mdy(r["DATE"])] = v
    vix = {}
    for r in csv.DictReader(open(os.path.join(DATOS, "VIX_History.csv"))):
        v = float(r["CLOSE"])
        if v > 0:
            vix[fecha_mdy(r["DATE"])] = v
    tb = {}
    for r in csv.DictReader(open(os.path.join(DATOS, "DTB3_fred_copia_AC17.csv"))):
        if r["DTB3"] not in (".", ""):
            tb[dt.date.fromisoformat(r["observation_date"])] = float(r["DTB3"])
    ultimo_fred = max(tb)
    ext = 0
    for r in csv.DictReader(open(os.path.join(DATOS, "treasury_bill_rates_2026.csv"))):
        d = fecha_mdy(r["Date"])
        if d > ultimo_fred:
            tb[d] = float(r["13 WEEKS BANK DISCOUNT"])
            ext += 1
    html = open(os.path.join(DATOS, "multpl_sp500_dividend_yield_by_month.html"), encoding="utf-8").read()
    filas = re.findall(r"<td>([A-Z][a-z]{2} \d{1,2}, \d{4})</td>\s*<td>(.*?)</td>", html, re.S)
    dy = {}
    for f, v in filas:
        d = dt.datetime.strptime(f, "%b %d, %Y").date()
        num = re.search(r"([\d.]+)%", v)
        if num:
            dy[d] = float(num.group(1)) / 100
    return spx, vix, tb, dy, ultimo_fred, ext


def ultimo_valor(serie_ordenada, fechas_ord, d, estricto):
    """Último valor con fecha < d (estricto) o <= d. Búsqueda binaria."""
    import bisect
    i = bisect.bisect_left(fechas_ord, d) if estricto else bisect.bisect_right(fechas_ord, d)
    return serie_ordenada[fechas_ord[i - 1]] if i > 0 else None


def construir():
    spx, vix, tb, dy, ultimo_fred, ext = cargar()
    fechas = sorted(d for d in spx if d <= FIN)
    tb_f = sorted(tb); dy_f = sorted(dy); vix_f = sorted(vix)
    # rendimiento TR: precio + dividend yield del último fin de mes publicado antes del día /252
    rtr, rf, r3 = {}, {}, {}
    for a, b in zip(fechas, fechas[1:]):
        y = ultimo_valor(dy, dy_f, b, estricto=True)
        t = ultimo_valor(tb, tb_f, a, estricto=False)   # tasa conocida al cierre previo
        rtr[b] = spx[b] / spx[a] - 1 + y / 252
        rf[b] = t / 100 / 252
        r3[b] = 3 * rtr[b] - 2 * rf[b] - GASTO / 252
    # SMA200 del precio y estado del filtro (con histéresis) al cierre de cada día
    estado = {}
    on = False
    suma, ventana = 0.0, []
    for d in fechas:
        ventana.append(spx[d]); suma += spx[d]
        if len(ventana) > 200:
            suma -= ventana.pop(0)
        v = ultimo_valor(vix, vix_f, d, estricto=False)   # VIX del día (o último si faltara)
        if len(ventana) < 200 or v is None:
            estado[d] = None
            continue
        sma = suma / 200
        p = spx[d]
        if on:
            if p < sma * 0.97 or v >= 25:
                on = False
        else:
            if p > sma and v < 25:
                on = True
        estado[d] = on
    return fechas, rtr, rf, r3, estado, ultimo_fred, ext


def simular(fechas, rf, r3, estado, objetivo, deriva=False):
    """Decisión al cierre de t con filtro del cierre t-1 y vol de r3 hasta t-1.
    El peso decidido al cierre de t se aplica al rendimiento de t+1."""
    idx = {d: i for i, d in enumerate(fechas)}
    w = 0.0
    serie = []   # (fecha, r_cartera, rf, w_aplicado)
    cambios = 0
    w_dec = {}
    for i in range(2, len(fechas) - 1):
        t = fechas[i]
        senal = estado.get(fechas[i - 1])
        if senal is None:
            continue
        # volatilidad: 20 rendimientos del 3x previos a t (t-20..t-1)
        prev = [r3[fechas[j]] for j in range(i - 20, i) if fechas[j] in r3]
        if len(prev) < 20:
            continue
        if objetivo is None:
            wstar = 1.0
        else:
            m = sum(prev) / 20
            sd = math.sqrt(sum((x - m) ** 2 for x in prev) / 19) * math.sqrt(252)
            wstar = min(1.0, objetivo / sd)
        if not senal:
            nuevo = 0.0
        elif w == 0.0:
            nuevo = wstar                     # entrada: al día
        elif t.weekday() == 4 and abs(wstar - w) > BANDA:
            nuevo = wstar                     # ajuste: viernes y fuera de banda
        else:
            nuevo = w
        costo = COSTO * abs(nuevo - w)
        if nuevo != w:
            cambios += 1
        w = nuevo
        d1 = fechas[i + 1]
        rp = w * r3[d1] + (1 - w) * rf[d1]
        serie.append((t, d1, rp, rf[d1], w, costo))
        if deriva and w > 0:
            # el peso deriva con los rendimientos hasta el siguiente ajuste
            w = w * (1 + r3[d1]) / (1 + rp)
            w = min(w, 1.0) if w > 0 else 0.0
    # costo se carga el día de la decisión (cierre t), es decir, reduce la riqueza antes de t+1
    out = []
    for (t, d1, rp, rfd, wa, c) in serie:
        out.append((d1, (1 - c) * (1 + rp) - 1, rfd, wa, c > 0))
    return out


def metricas(serie, desde, hasta):
    s = [x for x in serie if desde <= x[0] <= hasta]
    if not s:
        return None
    n = len(s)
    riq, pico, mdd = 1.0, 1.0, 0.0
    for x in s:
        riq *= 1 + x[1]
        pico = max(pico, riq)
        mdd = min(mdd, riq / pico - 1)
    anios = n / 252
    cagr = riq ** (1 / anios) - 1
    r = [x[1] for x in s]
    m = sum(r) / n
    vol = math.sqrt(sum((v - m) ** 2 for v in r) / (n - 1)) * math.sqrt(252)
    ex = [x[1] - x[2] for x in s]
    me = sum(ex) / n
    sde = math.sqrt(sum((v - me) ** 2 for v in ex) / (n - 1))
    sharpe = me / sde * math.sqrt(252)
    return {"inicio": s[0][0].isoformat(), "fin": s[-1][0].isoformat(), "dias": n,
            "cagr": cagr, "vol": vol, "sharpe": sharpe, "mdd": mdd,
            "exposicion": sum(x[3] for x in s) / n, "cambios": sum(1 for x in s if x[4])}


def main():
    verificar_hashes()
    fechas, rtr, rf, r3, estado, ultimo_fred, ext = construir()
    variantes = {"V0": None, **OBJETIVOS}
    series = {k: simular(fechas, rf, r3, estado, v, DERIVA) for k, v in variantes.items()}
    # comprar y mantener el 3x
    series["BH3x"] = [(d, r3[d], rf[d], 1.0, False) for d in fechas[1:] if d in r3]
    periodos = {"completo": (INICIO, FIN),
                "1990-2008": (INICIO, dt.date(2008, 12, 31)),
                "2009-hoy": (dt.date(2009, 1, 1), FIN),
                "desde_1990-01_sens": (dt.date(1990, 1, 1), FIN)}
    res = {"datos": {"fuente": "CBOE SPX + multpl dividend yield (TR sintético), CBOE VIX, FRED DTB3 + Treasury 13w",
                     "dtb3_ultimo": ultimo_fred.isoformat(), "dias_rf_extendidos_treasury": ext,
                     "deriva": DERIVA},
           "resultados": {}}
    lineas = []
    for p, (a, b) in periodos.items():
        lineas.append(f"\n== {p} ==")
        lineas.append(f"{'var':6} {'inicio':10} {'CAGR':>7} {'Vol':>6} {'Sharpe':>7} {'MDD':>7} {'Exp':>5} {'Camb':>5}")
        res["resultados"][p] = {}
        for k, s in series.items():
            m = metricas(s, a, b)
            res["resultados"][p][k] = m
            lineas.append(f"{k:6} {m['inicio']} {m['cagr']*100:6.2f}% {m['vol']*100:5.1f}% {m['sharpe']:7.3f} "
                          f"{m['mdd']*100:6.1f}% {m['exposicion']:5.2f} {m['cambios']:5d}")
    c = res["resultados"]["completo"]
    dmdd = (c["VT45"]["mdd"] - c["V0"]["mdd"]) * 100
    dsh = c["VT45"]["sharpe"] - c["V0"]["sharpe"]
    h1 = dmdd >= 5 and dsh >= -0.03
    h2 = dsh > 0
    res["veredicto"] = {"dMDD_pp": dmdd, "dSharpe": dsh, "H1_sostenida": h1, "H2_sharpe_mayor": h2,
                        "estado": "Replicado" if h1 else "No replicado"}
    lineas.append(f"\nVT45 vs V0 (completo): ΔMDD = {dmdd:+.1f} pp, ΔSharpe = {dsh:+.3f}")
    lineas.append(f"H1 {'SOSTENIDA' if h1 else 'REFUTADA'} -> {res['veredicto']['estado']}; H2 {'sí' if h2 else 'no'}")
    texto = "\n".join(lineas)
    print(texto)
    suf = "-deriva" if DERIVA else ""
    open(os.path.join(AQUI, f"salida{suf}.txt"), "w").write(texto + "\n")
    json.dump(res, open(os.path.join(AQUI, f"b-resultados{suf}.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
