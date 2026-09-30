"""Construye la serie diaria del diferencial de tasas de politica Banxico - Fed (limite superior)."""
import json, csv, os
from datetime import date, timedelta
D = os.path.dirname(os.path.abspath(__file__))
def P(s): return date.fromisoformat(s)
bmx = json.load(open(f"{D}/bmx.json"))
obj = [(P(f), v) for f, v in bmx["SF61745"]]           # tasa objetivo 2008-01-21..
fix = [(P(f), v) for f, v in bmx["SF43718"]]
fondeo = [(P(f), v) for f, v in json.load(open(f"{D}/fondeo43773.json"))]
def fred(s):
    out = []
    for r in csv.DictReader(open(f"{D}/{s}.csv")):
        v = r[s]
        if v not in ("", "."): out.append((P(r["observation_date"]), float(v)))
    return out
ftar = fred("DFEDTAR"); ftaru = fred("DFEDTARU")
fed = [x for x in ftar if x[0] < date(2008,12,16)] + ftaru
CORTE = date(2008,1,21)
def asof(serie):
    d = dict(serie); keys = sorted(d)
    import bisect
    def f(t):
        i = bisect.bisect_right(keys, t) - 1
        return None if i < 0 else d[keys[i]]
    return f
fed_f = asof(fed); obj_f = asof(obj)
# pre-2008: fondeo bancario redondeado a 0.25 (proxy de la tasa objetivo/"corto" de ese regimen)
fondeo_d = dict(fondeo)
def bmx_rate(t, redondeo=True):
    if t >= CORTE: return obj_f(t), "SF61745"
    # usar fondeo del dia (o el ultimo disponible)
    v = asof(fondeo)(t)
    return (round(v*4)/4 if redondeo else v), "SF43773"
# dias: todos los dias habiles del FIX (calendario MX) 2005-01-03..2026-09-30 + hoy
dias = [t for t, _ in fix]
if dias[-1] < date(2026,9,30): dias.append(date(2026,9,30))
serie = []
for t in dias:
    b, src = bmx_rate(t); b_raw, _ = bmx_rate(t, False); f = fed_f(t)
    serie.append((t, b, b_raw, f, round(b - f, 4), src))
json.dump([(str(t), b, br, f, d, s) for t, b, br, f, d, s in serie], open(f"{D}/diferencial.json", "w"))
fixd = dict(fix)
if __name__ == "__main__":
    print("n dias", len(serie), serie[0], serie[-1])
    # cambios de nivel (para listar regimenes)
    prev = None
    for t, b, br, f, d, s in serie:
        if t < date(2006,1,1): prev = d; continue
        if prev is None or abs(d - prev) > 1e-9:
            print(t, f"bmx={b:.2f}({s}) fed={f:.2f} dif={d:.2f}", "FIX=", fixd.get(t))
        prev = d
