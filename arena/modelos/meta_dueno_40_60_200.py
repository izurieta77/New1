"""Meta del dueño (25-sep-2026): +40%, +60% o +200% en la temporada de 4 meses, para las tres IAs.
Pregunta: ¿qué probabilidad histórica tiene cada modo de operación de alcanzarla, y de tocar los topes de pérdida
del propio dueño (GBM −10,000 MXN, Binance −5,000 MXN)?
Datos: Yahoo chart v8 (^GSPC, ^NDX, BTC-USD, MXN=X), 2014-09 a hoy. Ventanas traslapadas de 85 días hábiles, en MXN.
Proxy de ETF 3x: 3 × rendimiento diario del NDX, rebalanceo diario, gasto ~2.5%/año. Efectivo GBM al 4%/año.
Limitaciones (importantes): (1) el periodo 2014-2026 es el mejor de la historia del Nasdaq, lo que infla los modos
apalancados; en 2000-02 o 2022 el modo D se habría liquidado. (2) Solo ~30 ventanas independientes. (3) No incluye
comisiones, deslizamiento ni el filtro SMA200/VIX (que reduciría tanto la caída como la subida).
Reproducir: python3 arena/modelos/meta_dueno_40_60_200.py
"""
import json, urllib.request, datetime as dt, statistics as st, bisect

def closes(t, p1):
    u = f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?period1={p1}&period2={int(dt.datetime.now().timestamp())}&interval=1d"
    r = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
    d = json.load(urllib.request.urlopen(r, timeout=60))["chart"]["result"][0]
    ts = d["timestamp"]; c = d["indicators"]["quote"][0]["close"]
    return {dt.datetime.utcfromtimestamp(a).date(): v for a, v in zip(ts, c) if v is not None}

def main(H=85):
    p1 = int(dt.datetime(2014, 9, 1).timestamp())
    sp = closes("^GSPC", p1); ndx = closes("^NDX", p1); btc = closes("BTC-USD", p1); fx = closes("MXN=X", p1)
    days = sorted(d for d in sp if d in ndx and d in fx)
    bdays = sorted(btc)
    bval = lambda d: btc[bdays[bisect.bisect_right(bdays, d) - 1]]
    S = [sp[d] for d in days]; N = [ndx[d] for d in days]; F = [fx[d] for d in days]; B = [bval(d) for d in days]
    n = len(days)
    modes = {
        "A · actual (83% índice, 17% efectivo; 40% BTC)": dict(w_idx=0.83, w_lev=0, cash=0.17, wb=0.40),
        "B · máximo sin apalancar (100% índice; 65% BTC)": dict(w_idx=1.0, w_lev=0, cash=0, wb=0.65),
        "C · tope actual de apalancados (50% 3x NDX + 50% índice; 100% BTC)": dict(w_idx=0.5, w_lev=0.5, cash=0, wb=1.0),
        "D · todo apalancado (100% 3x NDX; 100% BTC)": dict(w_idx=0, w_lev=1.0, cash=0, wb=1.0),
    }
    print(f"Ventanas de {H} días hábiles, {days[0]} a {days[-1]}, en MXN (n={n-H}, ~{(n-H)//H} independientes).")
    print(f"{'modo':70s} {'mediana':>8s} {'p10':>7s} {'p90':>7s} {'≥40%':>6s} {'≥60%':>6s} {'≥200%':>6s} {'tope GBM':>9s} {'tope BTC':>9s}")
    for name, m in modes.items():
        res = []
        for i in range(0, n - H):
            g = 20000.0; b = 10000.0; hitG = hitB = False
            for k in range(i + 1, i + H + 1):
                rs = S[k]/S[k-1]-1; rn = N[k]/N[k-1]-1; rf = F[k]/F[k-1]-1; rb = B[k]/B[k-1]-1
                r_idx = (1+rs)*(1+rf)-1
                r_lev = (1+3*rn-0.0001)*(1+rf)-1
                g *= 1 + m["w_idx"]*r_idx + m["w_lev"]*r_lev + m["cash"]*0.04/252
                b *= 1 + m["wb"]*((1+rb)*(1+rf)-1)
                hitG |= g <= 10000; hitB |= b <= 5000
            res.append(((g+b)/30000-1, hitG, hitB))
        R = sorted(x[0] for x in res); M = len(R)
        q = lambda th: sum(1 for x in R if x >= th)/M
        print(f"{name:70s} {st.median(R):8.1%} {R[int(0.1*M)]:7.1%} {R[int(0.9*M)]:7.1%} {q(0.4):6.1%} {q(0.6):6.1%} {q(2.0):6.1%} "
              f"{sum(1 for x in res if x[1])/M:9.1%} {sum(1 for x in res if x[2])/M:9.1%}")

if __name__ == "__main__":
    main()
