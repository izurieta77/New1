"""R20 (ejecución A): brecha del UPRO real contra el 3x sintético de nuestros backtests, por tramos de tasa.
Pre-registro: R20-brecha-upro-sintetico-tasas.md (mismo commit). Fuentes: Yahoo UPRO (adjclose), ^SP500TR; FRED DTB3.
Reproduce: python3 laboratorio/replicas/R20.py"""
import hashlib, json, math, os, sys, time, urllib.parse, urllib.request
from datetime import date, datetime, timezone
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "..", "..", "herramientas"))
import datos  # noqa: E402

GASTO = 0.0091 / 252          # el mismo costo anual que R16/R18
INI, FIN = "2009-06-26", "2026-10-23"
CACHE = os.path.join(BASE, "R20-datos", "series.json")
TRAMOS = [("bajo <0.5%", -1, 0.5), ("medio 0.5-3%", 0.5, 3.0), ("alto >=3%", 3.0, 99)]


def yahoo(t):
    q = urllib.parse.urlencode({"period1": 1240000000, "period2": int(time.time()), "interval": "1d", "events": "div,split"})
    req = urllib.request.Request(f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(t)}?{q}", headers={"User-Agent": "Mozilla/5.0"})
    r = json.load(urllib.request.urlopen(req, timeout=60))["chart"]["result"][0]
    adj = r["indicators"].get("adjclose", [{}])[0].get("adjclose") or r["indicators"]["quote"][0]["close"]
    return [(datetime.fromtimestamp(ts, timezone.utc).date().isoformat(), a) for ts, a in zip(r["timestamp"], adj) if a is not None]


def cargar():
    if not os.path.exists(CACHE):
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        s = {t: yahoo(t) for t in ["UPRO", "^SP500TR"]}
        s["DTB3"] = [(str(d), v) for d, v in datos.fred_serie("DTB3")]
        json.dump(s, open(CACHE, "w"))
    raw = open(CACHE, "rb").read()
    return json.loads(raw), hashlib.sha256(raw).hexdigest()


def ols(y, x):
    n = len(y); mx, my = sum(x) / n, sum(y) / n
    sxx = sum((a - mx) ** 2 for a in x); b = sum((a - mx) * (c - my) for a, c in zip(x, y)) / sxx
    a0 = my - b * mx; e = [c - a0 - b * a for a, c in zip(x, y)]
    # Newey-West(6) para la pendiente
    u = [(a - mx) * ei for a, ei in zip(x, e)]
    s = sum(v * v for v in u)
    for L in range(1, 7):
        w = 1 - L / 7; s += 2 * w * sum(u[i] * u[i - L] for i in range(L, n))
    return a0, b, b / (math.sqrt(s) / sxx)


def main():
    s, sha = cargar()
    up = {d: v for d, v in s["UPRO"]}; tr = {d: v for d, v in s["^SP500TR"]}
    tb = sorted((d, v) for d, v in s["DTB3"])
    f = sorted(d for d in set(up) & set(tr) if INI <= d <= FIN)
    rf, j, ult = {}, 0, 0.0
    for d in f:
        while j < len(tb) and tb[j][0] <= d:
            ult = tb[j][1]; j += 1
        rf[d] = ult
    gap, rtr, tasa, ano = [], [], [], []
    for a, b in zip(f, f[1:]):
        r_up = up[b] / up[a] - 1; r_tr = tr[b] / tr[a] - 1
        sint = 3 * r_tr - 2 * rf[b] / 100 / 252 - GASTO   # misma fórmula que R16.py L73
        gap.append(r_up - sint); rtr.append(r_tr); tasa.append(rf[b]); ano.append(b[:4])
    n = len(gap)
    res = {"sha256_cache": sha, "periodo": [f[0], f[-1]], "n_dias": n}
    res["M1_brecha_aritmetica_pp_anual"] = round(252 * sum(gap) / n * 100, 3)
    cagr = lambda xs: (math.prod(1 + x for x in xs) ** (252 / len(xs)) - 1) * 100
    real = [g + 3 * t - 2 * r / 100 / 252 - GASTO for g, t, r in zip(gap, rtr, tasa)]
    sint = [3 * t - 2 * r / 100 / 252 - GASTO for t, r in zip(rtr, tasa)]
    res["M1b_CAGR_real_vs_sintetico_pp"] = [round(cagr(real), 3), round(cagr(sint), 3), round(cagr(real) - cagr(sint), 3)]
    res["M2_tramos"] = {}
    for nom, lo, hi in TRAMOS:
        g = [x for x, r in zip(gap, tasa) if lo <= r < hi]
        res["M2_tramos"][nom] = {"n": len(g), "brecha_pp_anual": round(252 * sum(g) / len(g) * 100, 3) if g else None,
                                 "tasa_media": round(sum(r for r in tasa if lo <= r < hi) / max(len(g), 1), 2)}
    res["M2_por_ano"] = {y: round(252 * sum(x for x, a in zip(gap, ano) if a == y) / sum(1 for a in ano if a == y) * 100, 2) for y in sorted(set(ano))}
    a0, b, t = ols(gap, [r / 100 / 252 for r in tasa])
    res["M3_gap_sobre_tasa"] = {"alfa_pp_anual": round(a0 * 252 * 100, 3), "pendiente": round(b, 3), "t_NW6": round(t, 2)}
    a1, b1, t1 = ols(gap, rtr)
    res["M4_gap_sobre_retorno_indice"] = {"pendiente": round(b1, 5), "t_NW6": round(t1, 2)}
    m = res["M1_brecha_aritmetica_pp_anual"]; tr2 = res["M2_tramos"]
    res["H1_brecha<=-0.5"] = m <= -0.5
    alto, bajo = tr2["alto >=3%"]["brecha_pp_anual"], tr2["bajo <0.5%"]["brecha_pp_anual"]
    res["H2_alto-bajo<=-0.5"] = (alto is not None and bajo is not None and alto - bajo <= -0.5)
    res["H3_tNW<=-2"] = t1 <= -2
    print(json.dumps(res, indent=1, ensure_ascii=False))
    json.dump(res, open(os.path.join(BASE, "R20-resultados.json"), "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
