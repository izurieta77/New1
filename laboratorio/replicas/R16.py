"""R16 (ejecución A): stop fijo del UPRO de papel encima del filtro de tendencia, sobre un 3x sintético del S&P 500 TR.
Pre-registro: R16-stop-fijo-upro.md (commit c067ef6). Fuentes A: Yahoo ^GSPC (cierre, apertura, mínimo), ^SP500TR, ^VIX; FRED DTB3.
Reproduce: python3 laboratorio/replicas/R16.py"""
import hashlib, json, math, os, sys, time, urllib.parse, urllib.request
from datetime import date
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "..", "..", "herramientas"))
import datos  # noqa: E402

COSTO, GASTO, FIN = 0.0010, 0.0091 / 252, "2026-10-16"
CACHE = os.path.join(BASE, "R16-datos", "series.json")
STOPS = {"S8": 0.08, "S10.92": 0.1092, "S15": 0.15, "S20": 0.20}


def yahoo(t):
    q = urllib.parse.urlencode({"period1": 599616000, "period2": int(time.time()), "interval": "1d"})
    req = urllib.request.Request(f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(t)}?{q}", headers={"User-Agent": "Mozilla/5.0"})
    r = json.load(urllib.request.urlopen(req, timeout=60))["chart"]["result"][0]
    qq = r["indicators"]["quote"][0]
    out = []
    for i, ts in enumerate(r["timestamp"]):
        d = str(date.fromtimestamp(ts))
        if d <= FIN and qq["close"][i] is not None:
            out.append((d, qq["close"][i], qq["open"][i], qq["low"][i]))
    return out


def cargar():
    if not os.path.exists(CACHE):
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        s = {t: yahoo(t) for t in ["^GSPC", "^SP500TR", "^VIX"]}
        s["DTB3"] = [(str(d), v) for d, v in datos.fred_serie("DTB3")]
        json.dump(s, open(CACHE, "w"))
    raw = open(CACHE, "rb").read()
    return json.loads(raw), hashlib.sha256(raw).hexdigest()


def preparar(s):
    g = {r[0]: r for r in s["^GSPC"]}; tr = {r[0]: r[1] for r in s["^SP500TR"]}; vx = {r[0]: r[1] for r in s["^VIX"]}
    fechas = sorted(set(g) & set(tr) & set(vx))
    tb = sorted((d, v) for d, v in s["DTB3"]); rf, ult, j = [], 0.0, 0
    for d in fechas:
        while j < len(tb) and tb[j][0] <= d:
            ult = tb[j][1]; j += 1
        rf.append(ult / 100 / 252)
    px = [g[d][1] for d in fechas]; op = [g[d][2] for d in fechas]; lo = [g[d][3] for d in fechas]
    return fechas, px, op, lo, [tr[d] for d in fechas], [vx[d] for d in fechas], rf


def filtro(px, vix):
    n, acc, sen, est = 200, 0.0, [None] * len(px), None
    for i, p in enumerate(px):
        acc += p
        if i >= n: acc -= px[i - n]
        if i < n - 1: continue
        sma = acc / n
        if est is None: est = 1 if (p > sma and vix[i] < 25) else 0
        elif est == 1 and (p < sma * 0.97 or vix[i] >= 25): est = 0
        elif est == 0 and p > sma and vix[i] < 25: est = 1
        sen[i] = est
    return sen


def simular(D, sen, stop=None, intradia=False, reentrada21=False, desde=None, hasta=None):
    fechas, px, op, lo, tr, vix, rf = D
    i0 = next(i for i, x in enumerate(sen) if x is not None) + 2
    if desde: i0 = max(i0, next(i for i, d in enumerate(fechas) if d >= desde))
    i1 = len(fechas) - 1 if not hasta else max(i for i, d in enumerate(fechas) if d <= hasta)
    eq, exc = [1.0], []
    pos = 0; bloqueado = False; espera = 0; nivel3 = 1.0; entrada3 = None
    salidas = salidas_stop = 0; dias_dentro = 0; dias_stop = []
    for i in range(i0, i1 + 1):
        r3 = 3 * (tr[i] / tr[i - 1] - 1) - 2 * rf[i] - GASTO
        # posición decidida al cierre de i-1 (señal del filtro de i-2 ejecutada en i-1)
        e = eq[-1]
        if pos == 1:
            dias_dentro += 1
            hit = False
            if stop is not None and intradia:
                low3 = nivel3 * (1 + 3 * (lo[i] / px[i - 1] - 1))
                stop_lvl = entrada3 * (1 - stop)
                if low3 <= stop_lvl:
                    open3 = nivel3 * (1 + 3 * (op[i] / px[i - 1] - 1))
                    salida = min(stop_lvl, open3)
                    r = salida / nivel3 - 1
                    e *= (1 + r) * (1 - COSTO); hit = True
            if not hit:
                e *= 1 + r3
            nivel3 *= 1 + r3
            if not hit and stop is not None and not intradia and nivel3 <= entrada3 * (1 - stop):
                e *= 1 - COSTO; hit = True
            if hit:
                pos = 0; bloqueado = True; espera = 0; salidas += 1; salidas_stop += 1; dias_stop.append(i)
                eq.append(e); exc.append(e / eq[-2] - 1 - rf[i]); continue
            exc.append(e / eq[-1] - 1 - rf[i])
        else:
            e *= 1 + rf[i]; nivel3 *= 1 + r3
            exc.append(e / eq[-1] - 1 - rf[i])
        # decisión para mañana con la señal de ayer (i-1), ejecutada al cierre de hoy (i)
        s = sen[i - 1]
        if bloqueado:
            espera += 1
            if s == 0: bloqueado = False
            elif reentrada21 and espera >= 21 and s == 1: bloqueado = False
        objetivo = 1 if (s == 1 and not bloqueado) else 0
        if objetivo != pos:
            e *= 1 - COSTO
            if objetivo == 0: salidas += 1
            else: entrada3 = nivel3
            pos = objetivo
        eq.append(e)
    a = (date.fromisoformat(fechas[i1]) - date.fromisoformat(fechas[i0])).days / 365.25
    m = sum(exc) / len(exc); sd = math.sqrt(sum((x - m) ** 2 for x in exc) / (len(exc) - 1))
    pico, mdd = eq[0], 0.0
    for v in eq: pico = max(pico, v); mdd = min(mdd, v / pico - 1)
    return dict(desde=fechas[i0], hasta=fechas[i1], cagr=eq[-1] ** (1 / a) - 1, sharpe=m / sd * math.sqrt(252), mdd=mdd,
                salidas=salidas, salidas_stop=salidas_stop, invertido=dias_dentro / (i1 - i0 + 1)), dias_stop


def bh(D, desde=None, hasta=None, i0min=201):
    fechas, px, op, lo, tr, vix, rf = D
    i0 = max(i0min, next(i for i, d in enumerate(fechas) if d >= desde) if desde else i0min)
    i1 = len(fechas) - 1 if not hasta else max(i for i, d in enumerate(fechas) if d <= hasta)
    eq, exc = [1 - COSTO], []
    for i in range(i0, i1 + 1):
        r3 = 3 * (tr[i] / tr[i - 1] - 1) - 2 * rf[i] - GASTO
        eq.append(eq[-1] * (1 + r3)); exc.append(r3 - rf[i])
    a = (date.fromisoformat(fechas[i1]) - date.fromisoformat(fechas[i0])).days / 365.25
    m = sum(exc) / len(exc); sd = math.sqrt(sum((x - m) ** 2 for x in exc) / (len(exc) - 1))
    pico, mdd = eq[0], 0.0
    for v in eq: pico = max(pico, v); mdd = min(mdd, v / pico - 1)
    return dict(cagr=eq[-1] ** (1 / a) - 1, sharpe=m / sd * math.sqrt(252), mdd=mdd)


if __name__ == "__main__":
    s, sha = cargar()
    D = preparar(s); fechas = D[0]
    sen = filtro(D[1], D[5])
    L = [f"Yahoo ^GSPC/^SP500TR/^VIX + FRED DTB3: {len(fechas)} días comunes {fechas[0]} a {fechas[-1]}; sha256 {sha[:16]}…"]
    # cotejo contra la caché de R11 (mismas fuentes, descarga del 12-oct)
    try:
        r11 = json.load(open(os.path.join(BASE, "R11-datos", "series.json")))
        a = {d: v for d, v in r11["^SP500TR"]}; b = {r[0]: r[1] for r in s["^SP500TR"]}
        comun = [d for d in a if d in b]
        dif = max(abs(a[d] / b[d] - 1) for d in comun)
        L.append(f"Cotejo con la caché de R11 (^SP500TR): {len(comun)} días comunes, diferencia relativa máxima {dif:.2e}")
    except Exception as ex:
        L.append(f"Cotejo con R11 no disponible: {ex}")
    periodos = {"completo": (None, None), "1990-2008": (None, "2008-12-31"), "2009-hoy": ("2009-01-01", None)}
    out = {}
    for pn, (de, ha) in periodos.items():
        L.append(f"\n== {pn}")
        filas = [("V0 filtro vigente", {})] + [(k, {"stop": v}) for k, v in STOPS.items()]
        if pn == "completo":
            filas += [("S10.92 intradía (sens. a)", {"stop": 0.1092, "intradia": True}), ("S10.92 reentrada 21d (sens. b)", {"stop": 0.1092, "reentrada21": True})]
        for nombre, kw in filas:
            r, ds = simular(D, sen, desde=de, hasta=ha, **kw)
            out[f"{pn}|{nombre}"] = r
            if pn == "completo" and nombre == "S10.92": dias_stop = ds
            L.append(f"{nombre:31s} CAGR {r['cagr']:+.1%} Sharpe {r['sharpe']:.3f} MDD {r['mdd']:.1%} salidas {r['salidas']:3d} (stop {r['salidas_stop']:2d}) invertido {r['invertido']:.0%} [{r['desde']}→{r['hasta']}]")
        b_ = bh(D, de, ha)
        L.append(f"{'3x comprar y mantener':31s} CAGR {b_['cagr']:+.1%} Sharpe {b_['sharpe']:.3f} MDD {b_['mdd']:.1%}")
        out[f"{pn}|BH"] = b_
    # H2: tras cada stop de S10.92, ¿el filtro V0 da señal de salida (0) en los 21 días hábiles siguientes?
    red = sum(1 for i in dias_stop if any(sen[k] == 0 for k in range(i, min(i + 22, len(sen)))))
    v0, s1 = out["completo|V0 filtro vigente"], out["completo|S10.92"]
    d_mdd, d_sh = s1["mdd"] - v0["mdd"], s1["sharpe"] - v0["sharpe"]
    h1 = d_mdd >= 0.03 and d_sh >= -0.03
    h2 = len(dias_stop) > 0 and red / len(dias_stop) >= 0.5
    estado = "Replicado" if h1 else "No replicado"
    L.append(f"\nStops de S10.92: {len(dias_stop)}; en {red} el filtro V0 sale dentro de 21 días hábiles ({(red / len(dias_stop) if dias_stop else float('nan')):.0%})")
    L.append(f"Fechas de stop: {', '.join(fechas[i] for i in dias_stop)}")
    L.append(f"ΔMDD (S10.92 − V0) {d_mdd * 100:+.1f} pp; ΔSharpe {d_sh:+.3f}")
    L.append(f"Veredicto A: H1 {'sostenida' if h1 else 'refutada'}; H2 {'sostenida' if h2 else 'refutada'} -> {estado}")
    txt = "\n".join(L) + "\n"
    open(os.path.join(BASE, "R16-salida.txt"), "w").write(txt)
    json.dump({"sha256": sha, "veredicto": {"H1": h1, "H2": h2, "estado_A": estado, "stops": len(dias_stop), "redundantes": red}, "resultados": out},
              open(os.path.join(BASE, "R16-resultados.json"), "w"), indent=1)
    sys.stdout.write(txt)
