"""AC-28 · Ejecución B independiente de R21 (R18 + brecha UPRO real de R20).
Código escrito desde cero, sin importar R16/R18/R21. Solo biblioteca estándar.
Fuentes descargadas en esta corrida: Yahoo chart v8 (^GSPC, ^SP500TR, ^VIX, ^NDX), FRED DTB3 y,
como sensibilidad de fuente, FRED NASDAQ100 (en lugar de ^NDX) y CBOE VIX_History (en lugar de ^VIX).
Uso: python3 -I ac28_r21.py [--sin-descarga]"""
import csv, hashlib, io, json, os, ssl, sys, time, urllib.request
from datetime import date

AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(AQUI, "datos")
FIN = "2026-10-16"                      # mismo corte que R18
WQ, WC = 0.268, 0.053                   # QQQM y efectivo fijos (R18)
G_SPYM, G_QQQM, G_UPRO = 0.0002, 0.0015, 0.0091
PESOS = {"U13.5": 0.135, "U27": 0.269}
BRECHA_CONST = -1.59                    # pp/año (R20-A M1)
BRECHA_TRAMOS = ((0.5, -1.31), (3.0, -1.54), (None, -2.30))   # DTB3 <0.5 / 0.5-3 / >=3 (R20-A M2)
HS, NIVELES = (63, 126), (0.12, 0.20)

CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt") if os.path.exists("/root/.ccr/ca-bundle.crt") else ssl.create_default_context()


RESPALDO = {  # copias FRED de auditorías previas, solo si FRED no responde (se declara en el informe)
    "fred_DTB3.csv": "../AC-27-R20/datos/fred_DTB3.csv",
    "fred_NASDAQ100.csv": "../AC-26-R19b/datos/NASDAQ100.csv",
}
ORIGEN = {}


def bajar(url, archivo):
    ruta = os.path.join(DATOS, archivo)
    ORIGEN[archivo] = url
    if "--sin-descarga" in sys.argv and os.path.exists(ruta):
        ORIGEN[archivo] = "caché local"
        return open(ruta, "rb").read()
    for intento in range(2 if "fred" in url else 4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=60, context=CTX) as r:
                b = r.read()
            open(ruta, "wb").write(b)
            return b
        except Exception as e:  # noqa: BLE001
            print(f"  reintento {intento + 1} {archivo}: {e}", file=sys.stderr); time.sleep(3 * (intento + 1))
    if archivo in RESPALDO:
        src = os.path.normpath(os.path.join(AQUI, RESPALDO[archivo]))
        b = open(src, "rb").read(); open(ruta, "wb").write(b)
        ORIGEN[archivo] = "COPIA de " + os.path.relpath(src, os.path.dirname(AQUI)) + " (FRED sin respuesta)"
        print(f"  {archivo}: uso copia {src}", file=sys.stderr)
        return b
    raise RuntimeError(f"no se pudo bajar {url}")


def yahoo(sim):
    p2 = int(time.time()) + 86400
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(sim)}?period1=567993600&period2={p2}&interval=1d&events=div%7Csplit"
    b = bajar(url, "yahoo_" + sim.replace("^", "") + ".json")
    res = json.loads(b)["chart"]["result"][0]
    out = {}
    for ts, c in zip(res["timestamp"], res["indicators"]["quote"][0]["close"]):
        if c is None: continue
        # Yahoo marca con la hora de apertura de NY (UTC-4/-5): fecha de NY = UTC - 5 h
        d = time.strftime("%Y-%m-%d", time.gmtime(ts - 5 * 3600))
        out[d] = float(c)
    return out


def fred(serie):
    b = bajar(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={serie}", f"fred_{serie}.csv")
    out = {}
    for fila in list(csv.reader(io.StringIO(b.decode())))[1:]:
        try: out[fila[0]] = float(fila[1])
        except (ValueError, IndexError): pass
    return out


def cboe_vix():
    b = bajar("https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv", "cboe_VIX_History.csv")
    out = {}
    for fila in list(csv.reader(io.StringIO(b.decode())))[1:]:
        m, d, y = fila[0].split("/")
        out[f"{y}-{int(m):02d}-{int(d):02d}"] = float(fila[4])
    return out


def sha(archivo):
    return hashlib.sha256(open(os.path.join(DATOS, archivo), "rb").read()).hexdigest()


# ---------- señal V0 (definición de R16: SMA200 de ^GSPC; sale si < 0.97·SMA o VIX ≥ 25; entra si > SMA y VIX < 25)
def senal_v0(dias, spx, vix):
    est, ventana, s, out = None, [], 0.0, {}
    for d in dias:
        p = spx[d]; ventana.append(p); s += p
        if len(ventana) > 200: s -= ventana.pop(0)
        if len(ventana) < 200: continue
        sma = s / 200; v = vix[d]
        if est is None: est = 1 if (p > sma and v < 25) else 0
        elif est == 1 and (p < 0.97 * sma or v >= 25): est = 0
        elif est == 0 and p > sma and v < 25: est = 1
        out[d] = est
    return out


def brecha_dia(modo, tasa_pct):
    if modo == "sin": return 0.0
    if modo == "constante": return BRECHA_CONST / 100 / 252
    for lim, g in BRECHA_TRAMOS:
        if lim is None or tasa_pct < lim: return g / 100 / 252


def construir(spx, tr, vix, ndx, dtb3):
    # calendario de la señal: días con ^GSPC y VIX (la SMA usa todos los días de SPX con VIX)
    cal_sen = sorted(d for d in spx if d in vix and d <= FIN)
    sen = senal_v0(cal_sen, spx, vix)
    pos_sen = {d: i for i, d in enumerate(cal_sen)}
    # calendario de rendimientos: días con todas las series
    cal = sorted(d for d in cal_sen if d in tr and d in ndx)
    tb = sorted(dtb3.items()); j, ult = 0, None
    filas = []
    for k in range(1, len(cal)):
        d, d0 = cal[k], cal[k - 1]
        while j < len(tb) and tb[j][0] <= d:
            ult = tb[j][1]; j += 1
        i = pos_sen[d]
        if i < 2 or cal_sen[i - 2] not in sen or ult is None: continue
        s = sen[cal_sen[i - 2]]           # cierre de t−2 → rendimiento de t
        rf = ult / 100 / 252
        r1 = tr[d] / tr[d0] - 1
        filas.append(dict(d=d, rs=r1 - G_SPYM / 252, rq=ndx[d] / ndx[d0] - 1 - G_QQQM / 252,
                          r3=3 * r1 - 2 * rf - G_UPRO / 252, rf=rf, tasa=ult, on=s))
    return filas


def curva(filas, wu, modo):
    ws = 1 - wu - WQ - WC
    v, mes, eq, dias_on = None, None, [1.0], 0
    for f in filas:
        if f["d"][:7] != mes:
            tot = sum(v) if v else 1.0
            v = [tot * ws, tot * WQ, tot * wu, tot * WC]; mes = f["d"][:7]
        if f["on"] == 1:
            ru = f["r3"] + brecha_dia(modo, f["tasa"]); dias_on += 1
        else:
            ru = f["rf"]
        v = [v[0] * (1 + f["rs"]), v[1] * (1 + f["rq"]), v[2] * (1 + ru), v[3] * (1 + f["rf"])]
        eq.append(sum(v))
    return eq, dias_on


def peor_en_ventana(eq, H):
    """Para cada inicio t (0..N−H−1), la peor caída bajo el máximo desde t dentro de t+1..t+H."""
    out = []
    for t in range(0, len(eq) - H - 1 + 1):
        pico, peor = eq[t], 0.0
        for k in range(t + 1, t + H + 1):
            x = eq[k]
            if x > pico: pico = x
            dd = x / pico - 1
            if dd < peor: peor = dd
        out.append(peor)
    return out


def metricas(eq, fechas):
    años = (date.fromisoformat(fechas[-1]) - date.fromisoformat(fechas[0])).days / 365.25
    rs = [eq[i] / eq[i - 1] - 1 for i in range(1, len(eq))]
    m = sum(rs) / len(rs); vol = (sum((x - m) ** 2 for x in rs) / (len(rs) - 1)) ** 0.5 * 252 ** 0.5
    pico, mdd = eq[0], 0.0
    for x in eq:
        pico = max(pico, x); mdd = min(mdd, x / pico - 1)
    return dict(cagr=eq[-1] ** (1 / años) - 1, cagr252=eq[-1] ** (252 / len(rs)) - 1, vol=vol, mdd=mdd)


def correr(filas, etiqueta):
    fechas = [filas[0]["d"]] + [f["d"] for f in filas]   # eq[0] es la base antes del primer rendimiento
    res = {}
    for nom, wu in PESOS.items():
        res[nom] = {}
        for modo in ("sin", "constante", "tramos"):
            eq, on = curva(filas, wu, modo)
            fila = metricas(eq, fechas); fila["dias_upro_on"] = on
            for H in HS:
                w = peor_en_ventana(eq, H)
                fila[f"ventanas_{H}"] = len(w)
                for nv in NIVELES:
                    fila[f"P{int(nv * 100)}_{H}"] = sum(1 for x in w if x <= -nv) / len(w)
            res[nom][modo] = fila
    return dict(etiqueta=etiqueta, dias=len(filas), desde=filas[0]["d"], hasta=filas[-1]["d"], resultados=res)


def veredicto(r):
    a = r["resultados"]["U13.5"]
    dP = (a["tramos"]["P12_126"] - a["sin"]["P12_126"]) * 100
    dC = (a["tramos"]["cagr"] - a["sin"]["cagr"]) * 100
    dC252 = (a["tramos"]["cagr252"] - a["sin"]["cagr252"]) * 100
    return dict(dP12_126_pp=dP, H1=dP <= 1.0, dCAGR_pp=dC, dCAGR252_pp=dC252, H2=(-0.30 <= dC <= -0.10))


def imprimir(r, L):
    L.append(f"\n== {r['etiqueta']}: {r['dias']} días, {r['desde']} a {r['hasta']}")
    L.append(f"{'peso':6s} {'modo':10s} {'P12_63':>7s} {'P20_63':>7s} {'P12_126':>8s} {'P20_126':>8s} {'CAGR':>7s} {'vol':>6s} {'MDD':>7s} díasON")
    for nom in PESOS:
        for modo, f in r["resultados"][nom].items():
            L.append(f"{nom:6s} {modo:10s} {f['P12_63']:7.2%} {f['P20_63']:7.2%} {f['P12_126']:8.2%} {f['P20_126']:8.2%} "
                     f"{f['cagr']:7.2%} {f['vol']:6.2%} {f['mdd']:7.2%} {f['dias_upro_on']}")
    v = r["veredicto"]
    L.append(f"H1 ΔP(−12%,126d) U13.5 tramos−sin = {v['dP12_126_pp']:+.2f} pp → {'sostenida' if v['H1'] else 'refutada'} (≤ 1.0)")
    L.append(f"H2 ΔCAGR U13.5 tramos−sin = {v['dCAGR_pp']:+.3f} pp/año (base 252: {v['dCAGR252_pp']:+.3f}) → "
             f"{'sostenida' if v['H2'] else 'refutada'} ([−0.30, −0.10])")


if __name__ == "__main__":
    import urllib.parse  # noqa: F401
    os.makedirs(DATOS, exist_ok=True)
    spx, tr, vix, ndx = yahoo("^GSPC"), yahoo("^SP500TR"), yahoo("^VIX"), yahoo("^NDX")
    dtb3 = fred("DTB3")
    try: ndx_fred = fred("NASDAQ100")
    except Exception: ndx_fred = None
    try: vix_cboe = cboe_vix()
    except Exception: vix_cboe = None
    hashes = {f: sha(f) for f in sorted(os.listdir(DATOS))}
    L = ["AC-28 · B independiente de R21", "sha256 de los datos:"] + [f"  {h}  {f}  <- {ORIGEN.get(f, '?')}" for f, h in hashes.items()]
    corridas = []
    r = correr(construir(spx, tr, vix, ndx, dtb3), "Principal: Yahoo ^GSPC/^SP500TR/^VIX/^NDX + FRED DTB3")
    r["veredicto"] = veredicto(r); corridas.append(r); imprimir(r, L)
    if ndx_fred and vix_cboe:
        r2 = correr(construir(spx, tr, vix_cboe, ndx_fred, dtb3), "Sensibilidad de fuente: FRED NASDAQ100 + CBOE VIX")
        r2["veredicto"] = veredicto(r2); corridas.append(r2); imprimir(r2, L)
    txt = "\n".join(L) + "\n"
    open(os.path.join(AQUI, "salida.txt"), "w").write(txt)
    json.dump(dict(sha256=hashes, origen=ORIGEN, fin=FIN, corridas=corridas), open(os.path.join(AQUI, "resultados.json"), "w"), indent=1, ensure_ascii=False)
    sys.stdout.write(txt)
