"""Revisión de Bianchi y Goldberg (arXiv:2604.27287): ¿el término de covarianza
Cov(lambda, R) que explica el déficit de UPRO/SSO en 2022-2023 es en realidad
costo de acarreo (financiamiento 2x/1x, comisión anual, dividendos)?
Uso: python3 -I este.py DIR_YAHOO DFF.csv   (DIR con UPRO.json, SSO.json, %5EGSPC.json, %5ESP500TR.json)
Datos: Yahoo chart v8 (close sin ajustar = rendimiento de precio, como retx de CRSP), FRED DFF.
"""
import sys, json, csv, os, statistics as st, datetime as dtm
d, dff = sys.argv[1], sys.argv[2]
def serie(f, adj=False):
    j = json.load(open(os.path.join(d, f)))["chart"]["result"][0]
    ts = j["timestamp"]; q = j["indicators"]["quote"][0]["close"]
    if adj: q = j["indicators"]["adjclose"][0]["adjclose"]
    import datetime as dt
    return {dt.datetime.utcfromtimestamp(t).date().isoformat(): c for t, c in zip(ts, q) if c}
fed = {}
for row in list(csv.reader(open(dff)))[1:]:
    if row[1] not in ("", "."): fed[row[0]] = float(row[1]) / 100
spx, tr = serie("%5EGSPC.json"), serie("%5ESP500TR.json")
dias = sorted(k for k in spx if "2022-01-03" <= k <= "2023-12-29")
def rets(s):
    return [s[b] / s[a] - 1 for a, b in zip(dias, dias[1:])]
R, RTR = rets(spx), rets(tr)
# días naturales que devenga el financiamiento entre cierres (lunes = 3)
GAP = [(dtm.date.fromisoformat(b) - dtm.date.fromisoformat(a)).days for a, b in zip(dias, dias[1:])]
FED = [fed.get(a, 0) for a in dias[:-1]]
ann = lambda x: 252 * st.mean(x) * 100
print(f"dias {len(R)} | S&P precio arit {ann(R):.3f}% | S&P TR arit {ann(RTR):.3f}% | div impl {ann(RTR)-ann(R):.3f}%")
for tk, L, er in (("SSO", 2, 0.0089), ("UPRO", 3, 0.0091)):
    p, a = serie(tk + ".json"), serie(tk + ".json", adj=True)
    rp, ra = rets(p), rets(a)
    lam = [x / y for x, y in zip(rp, R) if y != 0]
    cov = ann(rp) - st.mean(lam) * ann(R)
    # modelo de acarreo: L x total return - (L-1) x tasa diaria - comisión diaria
    mod = [L * t - (L - 1) * f * g / 360 - er * g / 365 for t, f, g in zip(RTR, FED, GAP)]
    print(f"{tk}: arit precio {ann(rp):.3f}% (paper {'1.655' if L==2 else '0.309'}) | ajustado {ann(ra):.3f}% | "
          f"ideal L*R {L*ann(R):.3f}% | brecha {ann(rp)-L*ann(R):.3f} | Cov(lam,R) {cov:.3f} | "
          f"modelo acarreo {ann(mod):.3f}% (brecha vs ajustado {ann(ra)-ann(mod):.3f})")
# Por año: residual (ajustado - modelo de acarreo), anualizado
for tk, L, er in (("SSO", 2, 0.0089), ("UPRO", 3, 0.0091)):
    a = serie(tk + ".json", adj=True); ra = rets(a)
    for y in ("2022", "2023"):
        idx = [i for i, k in enumerate(dias[1:]) if k.startswith(y)]
        mod = [L * RTR[i] - (L - 1) * FED[i] * GAP[i] / 360 - er * GAP[i] / 365 for i in idx]
        res = ann([ra[i] for i in idx]) - ann(mod)
        dif = [ra[i] - L * RTR[i] for i in idx]
        print(f"{tk} {y}: residual {res:.3f}%/año | sd diaria de (ETF - L*TR) {st.pstdev(dif)*100:.3f}% | "
              f"corr(ETF-L*TR, R) {st.correlation(dif, [R[i] for i in idx]):.3f}")
