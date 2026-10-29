"""Ficha 2026-10-29 · Pástor-Veronesi (JFE 2013), "Political uncertainty and risk premia".

Réplica propia, con datos públicos, de la parte empírica (§7, tablas 2-5) del NBER WP 17464
(sep-2011, rev. abr-2013), dentro de su muestra (1985-2010) y fuera de ella (2011-2026), y su
extensión a BTC (2014-2026).

Variables (mensuales), como en PV §7.1 salvo lo que se declara:
  PU   índice de incertidumbre de política de Baker-Bloom-Davis / 100. Principal: la hoja
       "Legacy Three Component EPU" de policyuncertainty.com (la familia de índice que usó PV en
       oct-2011; la añada de hoy está revisada). Robustez: la hoja "Main News Index".
  E    condiciones económicas (más alto = mejor): CFI (CFNAI), −REC (USREC), IPG (Δln INDPRO),
       −DEF (−(BAA − AAA), Moody's en FRED; PV usan AAA − BBB). Sin P/E de Shiller.
  RV   vol realizada del S&P 500 (^GSPC, rendimientos log diarios del mes), anualizada (√252), decimal.
  IV   promedio diario del VIX del mes / 100.
  R    rendimiento log del S&P (precio, sin dividendos ni T-bill: PV usan CRSP en exceso) de t+1 a t+h.
  BTC  vol realizada de BTC-USD (Yahoo, √365), DVOL mensual (Deribit, desde abr-2021) y correlación
       mensual BTC–S&P con rendimientos diarios en fechas comunes (asíncronos: Yahoo cierra BTC a las
       00:00 UTC; se declara).
Regresiones (PV ec. 56-62), MCO con errores Newey-West (3 rezagos; h rezagos en la tabla 5):
  T2: PU = a + b E (+ c PU_{t−1})          predicción b < 0
  T3: VC = a + b PU (+ c VC_{t−1})         predicción b > 0
  T4: VC = a + b PU·E + c PU + d E (+ e VC_{t−1})   predicción b < 0
  T5: R_{t+1,t+h} = a + b PU·E + c PU + d E          predicción b < 0

Uso (rutas relativas a este archivo):
  python3 -I conocimiento/cripto/fichas/2026-10-29-pastor-veronesi-incertidumbre-politica.py descargar
  python3 -I conocimiento/cripto/fichas/2026-10-29-pastor-veronesi-incertidumbre-politica.py
"""
import datetime as dt
import io
import json
import math
import os
import re
import sys
import time
import urllib.request
import zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
FOTO = os.path.join(AQUI, "2026-10-29-pastor-veronesi-incertidumbre-politica-datos.json")
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}  # Yahoo, Deribit y policyuncertainty.com
FRED = ["CFNAI", "USREC", "INDPRO", "BAA", "AAA"]  # FRED solo acepta el UA por defecto de urllib


def _get(url, ua=True, intentos=4):
    for i in range(intentos):
        try:
            req = urllib.request.Request(url, headers=UA) if ua else urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception:
            if i == intentos - 1:
                raise
            time.sleep(3 * (i + 1))


def _xlsx(raw):
    """Lee las dos hojas del xlsx de policyuncertainty.com sin dependencias."""
    z = zipfile.ZipFile(io.BytesIO(raw))
    ss = [re.sub(r"<[^>]+>", "", s) for s in
          re.findall(r"<si>(.*?)</si>", z.read("xl/sharedStrings.xml").decode(), re.S)]
    hojas = {}
    for nombre, f in (("noticias", "xl/worksheets/sheet1.xml"), ("tres", "xl/worksheets/sheet2.xml")):
        filas = []
        for fila in re.findall(r"<row [^>]*>(.*?)</row>", z.read(f).decode(), re.S):
            celdas = {}
            for ref, t, v in re.findall(r'<c r="([A-Z]+)\d+"(?: s="\d+")?( t="s")?(?: s="\d+")?>(?:<v>(.*?)</v>)?', fila):
                if v:
                    celdas[ref] = ss[int(v)] if t else float(v)
            filas.append(celdas)
        enc = filas[0]
        col = {v: k for k, v in enc.items()}
        clave = "News_Based_Policy_Uncert_Index" if nombre == "noticias" else "Three_Component_Index"
        serie = {}
        for c in filas[1:]:
            try:
                a, m, x = int(c["A"]), int(c["B"]), c[col[clave]]
            except (KeyError, ValueError):
                continue
            serie[f"{a:04d}-{m:02d}"] = round(x, 4)
        hojas[nombre] = sorted(serie.items())
    return hojas


def _yahoo(sim, desde):
    fin = int(time.time())
    r = json.loads(_get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sim}"
                        f"?period1={desde}&period2={fin}&interval=1d"))["chart"]["result"][0]
    return [[dt.datetime.fromtimestamp(t, dt.timezone.utc).date().isoformat(), round(c, 4)]
            for t, c in zip(r["timestamp"], r["indicators"]["quote"][0]["close"]) if c]


def descargar():
    foto = {"descargado_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
    foto.update({"epu_" + k: v for k, v in _xlsx(_get(
        "https://www.policyuncertainty.com/media/US_Policy_Uncertainty_Data.xlsx")).items()})
    for s in FRED:
        txt = _get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={s}", ua=False).decode()
        foto[s] = [[l.split(",")[0][:7], float(l.split(",")[1])] for l in txt.strip().splitlines()[1:]
                   if l.split(",")[1] not in (".", "") and l[:4] >= "1983"]
    foto["gspc_1d"] = _yahoo("%5EGSPC", 410227200)   # 1983-01-01
    foto["vix_1d"] = _yahoo("%5EVIX", 631152000)     # 1990-01-01
    foto["btc_1d"] = _yahoo("BTC-USD", 1410825600)   # 2014-09-16
    dvol, hasta = {}, int(time.time()) * 1000
    while True:
        r = json.loads(_get("https://www.deribit.com/api/v2/public/get_volatility_index_data?currency=BTC"
                            f"&resolution=1D&start_timestamp=1609459200000&end_timestamp={hasta}"))["result"]
        for t, o, h, l, c in r["data"]:
            dvol[dt.datetime.fromtimestamp(t / 1000, dt.timezone.utc).date().isoformat()] = c
        if not r["continuation"]:
            break
        hasta = r["continuation"]
    foto["dvol_1d"] = sorted(dvol.items())
    json.dump(foto, open(FOTO, "w"), separators=(",", ":"))
    print("foto guardada:", FOTO, foto["descargado_utc"],
          {k: len(v) for k, v in foto.items() if isinstance(v, list)})


# ------------------------------------------------------------------ álgebra mínima
def inv(A):
    n = len(A)
    M = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        pv = M[c][c]
        M[c] = [x / pv for x in M[c]]
        for r in range(n):
            if r != c and M[r][c]:
                f = M[r][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [row[n:] for row in M]


def ols_nw(y, X, lags):
    """MCO con constante; devuelve (beta, t Newey-West, n). X: lista de columnas."""
    n = len(y)
    Z = [[1.0] + [col[i] for col in X] for i in range(n)]
    k = len(Z[0])
    XtX = [[sum(Z[i][a] * Z[i][b] for i in range(n)) for b in range(k)] for a in range(k)]
    Xty = [sum(Z[i][a] * y[i] for i in range(n)) for a in range(k)]
    Q = inv(XtX)
    b = [sum(Q[a][c] * Xty[c] for c in range(k)) for a in range(k)]
    u = [y[i] - sum(b[a] * Z[i][a] for a in range(k)) for i in range(n)]
    S = [[sum(u[i] ** 2 * Z[i][a] * Z[i][c] for i in range(n)) for c in range(k)] for a in range(k)]
    for L in range(1, lags + 1):
        w = 1 - L / (lags + 1)
        for a in range(k):
            for c in range(k):
                g = sum(u[i] * u[i - L] * (Z[i][a] * Z[i - L][c] + Z[i - L][a] * Z[i][c]) for i in range(L, n))
                S[a][c] += w * g
    V = [[sum(Q[a][p] * S[p][q] * Q[q][c] for p in range(k) for q in range(k)) for c in range(k)] for a in range(k)]
    return b, [b[a] / math.sqrt(V[a][a]) for a in range(k)], n


# ------------------------------------------------------------------ series mensuales
def mes(d):
    return d[:7]


def sig(m, k):
    a, b = int(m[:4]), int(m[5:7]) - 1 + k
    return f"{a + b // 12:04d}-{b % 12 + 1:02d}"


def mensual_vol(diario, anual):
    por = {}
    for (d0, c0), (d1, c1) in zip(diario, diario[1:]):
        por.setdefault(mes(d1), []).append(math.log(c1 / c0))
    out = {}
    for m, r in por.items():
        if len(r) >= 10:
            mu = sum(r) / len(r)
            out[m] = math.sqrt(sum((x - mu) ** 2 for x in r) / (len(r) - 1) * anual)
    return out


def mensual_prom(diario, escala=1.0):
    por = {}
    for d, v in diario:
        por.setdefault(mes(d), []).append(v * escala)
    return {m: sum(v) / len(v) for m, v in por.items() if len(v) >= 10}


def mensual_ret(diario):
    ult = {}
    for d, c in diario:
        ult[mes(d)] = c
    ms = sorted(ult)
    return {m1: math.log(ult[m1] / ult[m0]) for m0, m1 in zip(ms, ms[1:])}


def mensual_corr(a, b):
    """Correlación mensual de rendimientos diarios en fechas comunes (a y b: [[fecha, cierre]])."""
    da, db = dict(a), dict(b)
    comunes = sorted(set(da) & set(db))
    por = {}
    for d0, d1 in zip(comunes, comunes[1:]):
        por.setdefault(mes(d1), []).append((math.log(da[d1] / da[d0]), math.log(db[d1] / db[d0])))
    out = {}
    for m, xs in por.items():
        if len(xs) >= 12:
            ma = sum(x for x, _ in xs) / len(xs)
            mb = sum(y for _, y in xs) / len(xs)
            sab = sum((x - ma) * (y - mb) for x, y in xs)
            saa = sum((x - ma) ** 2 for x, _ in xs)
            sbb = sum((y - mb) ** 2 for _, y in xs)
            out[m] = sab / math.sqrt(saa * sbb)
    return out


def armar(f):
    s = {}
    s["PU3"] = {m: v / 100 for m, v in f["epu_tres"]}
    s["PUN"] = {m: v / 100 for m, v in f["epu_noticias"]}
    s["CFI"] = dict(f["CFNAI"])
    s["-REC"] = {m: -v for m, v in f["USREC"]}
    ip = dict(f["INDPRO"])
    s["IPG"] = {m: math.log(ip[m] / ip[p]) for m, p in zip(sorted(ip)[1:], sorted(ip)) if ip.get(p)}
    baa, aaa = dict(f["BAA"]), dict(f["AAA"])
    s["-DEF"] = {m: -(baa[m] - aaa[m]) for m in baa if m in aaa}
    s["RV"] = mensual_vol(f["gspc_1d"], 252)
    s["IV"] = mensual_prom(f["vix_1d"], 0.01)
    s["RET"] = mensual_ret(f["gspc_1d"])
    s["BTCRV"] = mensual_vol(f["btc_1d"], 365)
    s["DVOL"] = mensual_prom(f["dvol_1d"], 0.01)
    s["CORR"] = mensual_corr(f["btc_1d"], f["gspc_1d"])
    return s


def muestra(s, m0, m1, need):
    out, m = [], m0
    while m <= m1:
        if all(m in s[k] for k in need):
            out.append(m)
        m = sig(m, 1)
    return out


def t2(s, pu, E, m0, m1, spec):
    ms = [m for m in muestra(s, m0, m1, [pu, E]) if spec == 1 or sig(m, -1) in s[pu]]
    y = [s[pu][m] for m in ms]
    X = [[s[E][m] for m in ms]] + ([[s[pu][sig(m, -1)] for m in ms]] if spec == 2 else [])
    b, t, n = ols_nw(y, X, 3)
    return b[1], t[1], n


def t3(s, pu, VC, m0, m1, spec):
    ms = [m for m in muestra(s, m0, m1, [pu, VC]) if spec == 1 or sig(m, -1) in s[VC]]
    y = [s[VC][m] for m in ms]
    X = [[s[pu][m] for m in ms]] + ([[s[VC][sig(m, -1)] for m in ms]] if spec == 2 else [])
    b, t, n = ols_nw(y, X, 3)
    return b[1], t[1], n


def t4(s, pu, VC, E, m0, m1, spec):
    ms = [m for m in muestra(s, m0, m1, [pu, VC, E]) if spec == 1 or sig(m, -1) in s[VC]]
    y = [s[VC][m] for m in ms]
    X = [[s[pu][m] * s[E][m] for m in ms], [s[pu][m] for m in ms], [s[E][m] for m in ms]]
    if spec == 2:
        X.append([s[VC][sig(m, -1)] for m in ms])
    b, t, n = ols_nw(y, X, 3)
    return b[1], t[1], n


def t5(s, pu, E, h, m0, m1):
    ms = [m for m in muestra(s, m0, m1, [pu, E]) if all(sig(m, k) in s["RET"] for k in range(1, h + 1))]
    y = [sum(s["RET"][sig(m, k)] for k in range(1, h + 1)) for m in ms]
    X = [[s[pu][m] * s[E][m] for m in ms], [s[pu][m] for m in ms], [s[E][m] for m in ms]]
    b, t, n = ols_nw(y, X, h)
    return b[1], t[1], n


def robustez(s, pu, VC, m0, m1):
    ms = muestra(s, m0, m1, [pu, VC])
    y = [s[VC][m] for m in ms]
    b, t, n = ols_nw(y, [[s[pu][m] for m in ms], [i / 12 for i in range(len(ms))]], 3)
    out = {"tendencia": (b[1], t[1], n)}
    medias = {}
    for m in ms:
        medias.setdefault(m[:4], []).append(m)
    yy, xx = [], []
    for grupo in medias.values():
        my = sum(s[VC][m] for m in grupo) / len(grupo)
        mp = sum(s[pu][m] for m in grupo) / len(grupo)
        yy += [s[VC][m] - my for m in grupo]
        xx += [s[pu][m] - mp for m in grupo]
    b, t, n = ols_nw(yy, [xx], 3)
    out["intra"] = (b[1], t[1], n)
    return out


def fmt(r):
    return f"{r[0]:+.3f} ({r[1]:+.2f}) n={r[2]}"


def analizar(f):
    s = armar(f)
    print("Foto:", f["descargado_utc"], "| último EPU:", f["epu_tres"][-1], f["epu_noticias"][-1],
          "| último CFNAI:", f["CFNAI"][-1])
    IS, OOS = ("1985-01", "2010-12"), ("2011-01", "2026-09")
    Es = ["CFI", "-REC", "IPG", "-DEF"]
    res = {}
    print("\n== Tabla 2 · PU sobre E (predicción b < 0); b (t NW3) ==")
    pv2 = {"CFI": (-0.31, -0.05), "-REC": (-0.69, -0.09), "IPG": (-20.95, -2.90), "-DEF": (-0.75, -0.09)}
    for pu in ("PU3", "PUN"):
        for E in Es:
            for spec in (1, 2):
                r_is, r_oos = t2(s, pu, E, *IS, spec), t2(s, pu, E, *OOS, spec)
                res[f"T2|{pu}|{E}|{spec}"] = (r_is, r_oos)
                print(f"{pu} {E:5s} esp{spec}: PV {pv2[E][spec - 1]:+.2f} | 1985-2010 {fmt(r_is)} | 2011-2026 {fmt(r_oos)}")
    print("\n== Tabla 3 · VC sobre PU (predicción b > 0) ==  [PV: RV 0.01 (4.81)/0.00 (3.45); IV 0.08 (5.27)/0.01 (2.53)]")
    for pu in ("PU3", "PUN"):
        for VC, m0 in (("RV", "1985-01"), ("IV", "1990-01")):
            for spec in (1, 2):
                r_is, r_oos = t3(s, pu, VC, m0, IS[1], spec), t3(s, pu, VC, *OOS, spec)
                res[f"T3|{pu}|{VC}|{spec}"] = (r_is, r_oos)
                print(f"{pu} {VC} esp{spec}: 1985/90-2010 {fmt(r_is)} | 2011-2026 {fmt(r_oos)}")
    print("\n== Tabla 4 · VC sobre PU·E (predicción b < 0) ==")
    cuenta = {"is": [0, 0, 0], "oos": [0, 0, 0]}
    for VC, m0 in (("RV", "1985-01"), ("IV", "1990-01")):
        for E in Es:
            for spec in (1, 2):
                r_is, r_oos = t4(s, "PU3", VC, E, m0, IS[1], spec), t4(s, "PU3", VC, E, *OOS, spec)
                res[f"T4|PU3|{VC}|{E}|{spec}"] = (r_is, r_oos)
                for k, r in (("is", r_is), ("oos", r_oos)):
                    if k == "oos" and E == "-REC":
                        continue  # degenerada fuera de muestra: solo 2 meses de recesión (mar-abr 2020)
                    cuenta[k][0] += 1
                    cuenta[k][1] += r[0] < 0
                    cuenta[k][2] += r[1] < -1.96
                print(f"PU3 {VC} {E:5s} esp{spec}: dentro {fmt(r_is)} | fuera {fmt(r_oos)}")
    rec = sum(1 for m in muestra(s, *OOS, ["-REC"]) if s["-REC"][m] == -1)
    print(f"Conteo (total, b<0, t<−1.96): dentro {cuenta['is']} | fuera, sin −REC {cuenta['oos']}"
          f" (−REC fuera de muestra tiene {rec} meses de recesión: sus t son degenerados)"
          " | PV vol: 16 de 16 negativos, 14 significativos (sin P/E)")
    res["meses_recesion_oos"] = rec
    res["T4_conteo"] = cuenta
    print("\n== Tabla 5 · R(t+1..t+h) sobre PU·E (predicción b < 0) ==")
    for h in (3, 6, 12):
        for E in Es:
            r_is, r_oos = t5(s, "PU3", E, h, *IS), t5(s, "PU3", E, h, "2011-01", "2025-09")
            res[f"T5|{h}|{E}"] = (r_is, r_oos)
            print(f"h={h:2d} {E:5s}: dentro {fmt(r_is)} | fuera {fmt(r_oos)}")
    print("\n== BTC (2014-10 a 2026-09; DVOL desde 2021-04) · ¿más vol y más correlación con el S&P cuando PU sube? ==")
    for pu in ("PU3", "PUN"):
        for VC, m0 in (("BTCRV", "2014-10"), ("DVOL", "2021-04"), ("CORR", "2014-10"), ("RV", "2014-10"), ("IV", "2014-10")):
            for spec in (1, 2):
                r = t3(s, pu, VC, m0, "2026-09", spec)
                res[f"BTC|{pu}|{VC}|{spec}"] = r
                print(f"{pu} {VC:5s} esp{spec}: {fmt(r)}")
        for VC in ("BTCRV", "CORR"):
            r = t4(s, pu, VC, "CFI", "2014-10", "2026-09", 1)
            res[f"BTC4|{pu}|{VC}|CFI"] = r
            print(f"{pu} {VC:5s} interacción PU·CFI: {fmt(r)}")
    # Robustez: control de tendencia lineal, media de cada año calendario quitada y submuestras
    print("\n== Robustez (PU3, esp. 1): tendencia lineal | sin la media de cada año | submuestras ==")
    for VC, m0, m1 in (("CORR", "2014-10", "2026-09"), ("BTCRV", "2014-10", "2026-09"),
                       ("RV", "2011-01", "2026-09"), ("IV", "2011-01", "2026-09")):
        rb = robustez(s, "PU3", VC, m0, m1)
        res[f"ROB|{VC}"] = rb
        print(f"{VC:5s} {m0}..{m1}: tendencia {rb['tendencia'][0]:+.3f} ({rb['tendencia'][1]:+.2f}) |"
              f" intra-año {rb['intra'][0]:+.3f} ({rb['intra'][1]:+.2f})")
    for a, b in (("2014-10", "2019-12"), ("2020-01", "2026-09"), ("2022-01", "2026-09")):
        r = t3(s, "PU3", "CORR", a, b, 1)
        res[f"SUB|CORR|{a}"] = r
        print(f"CORR {a}..{b}: {fmt(r)}")
    # Elasticidades comparables: efecto de +1 desviación estándar de PU, en puntos de vol
    def desv(xs):
        mu = sum(xs) / len(xs)
        return math.sqrt(sum((x - mu) ** 2 for x in xs) / (len(xs) - 1))
    ms = muestra(s, "2014-10", "2026-09", ["PU3", "BTCRV", "RV", "CORR"])
    sd = desv([s["PU3"][m] for m in ms])
    efecto = {k: res[f"BTC|PU3|{k}|1"][0] * sd for k in ("BTCRV", "RV", "CORR")}
    medias = {k: sum(s[k][m] for m in ms) / len(ms) for k in ("BTCRV", "RV", "CORR")}
    print(f"\n+1σ de PU3 (σ={sd:.3f}) 2014-2026: BTC RV {100 * efecto['BTCRV']:+.1f} pts (media {100 * medias['BTCRV']:.1f}),"
          f" S&P RV {100 * efecto['RV']:+.1f} pts (media {100 * medias['RV']:.1f}), corr {efecto['CORR']:+.3f} (media {medias['CORR']:.3f})")
    res["efecto_1sd"] = {"sd_pu3": sd, **efecto, "medias": medias}
    # Lectura de hoy
    pu3, pun = dict(f["epu_tres"]), dict(f["epu_noticias"])
    def pct(serie, m):
        v = sorted(serie.values())
        return 100 * sum(x <= serie[m] for x in v) / len(v)
    ult = sorted(pu3)[-6:]
    print("\nPU de los últimos 6 meses (tres comp. / noticias, percentil 1985-2026):")
    for m in ult:
        print(f"  {m}: {pu3[m]:7.1f} (p{pct({k: x for k, x in pu3.items() if k >= '1985'}, m):.0f}) / "
              f"{pun[m]:7.1f} (p{pct({k: x for k, x in pun.items() if k >= '1985'}, m):.0f})  CFI {s['CFI'].get(m, float('nan')):+.2f}")
    res["ultimos"] = {m: [pu3[m], pun[m]] for m in ult}
    # Segunda lectura: pendiente simple por cov/var y RV de oct-2008 a mano
    ms = muestra(s, "1990-01", "2010-12", ["PU3", "IV"])
    x = [s["PU3"][m] for m in ms]; y = [s["IV"][m] for m in ms]
    mx, my = sum(x) / len(x), sum(y) / len(y)
    b_cv = sum((a - mx) * (c - my) for a, c in zip(x, y)) / sum((a - mx) ** 2 for a in x)
    oct08 = [c for d, c in f["gspc_1d"] if "2008-09-30" <= d <= "2008-10-31"]
    r = [math.log(b / a) for a, b in zip(oct08, oct08[1:])]
    mu = sum(r) / len(r)
    rv08 = math.sqrt(sum((q - mu) ** 2 for q in r) / (len(r) - 1) * 252)
    print(f"\nSegunda lectura: T3 IV esp1 por cov/var = {b_cv:.4f} (matricial {res['T3|PU3|IV|1'][0][0]:.4f});"
          f" RV oct-2008 a mano {rv08:.4f} vs función {s['RV']['2008-10']:.4f}")
    return res


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "descargar":
        descargar()
    analizar(json.load(open(FOTO)))
