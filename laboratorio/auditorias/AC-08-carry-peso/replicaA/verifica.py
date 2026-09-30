"""Verificacion independiente: FIX desde el CSV de otra descarga (replicaB) y calculo directo sin reutilizar analisis.py."""
import csv, json
from datetime import date, timedelta
import os
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "replicaB")
fx = {date.fromisoformat(r["fecha"]): float(r["valor"]) for r in csv.DictReader(open(f"{B}/SF43718.csv"))}
ob = {date.fromisoformat(r["fecha"]): float(r["valor"]) for r in csv.DictReader(open(f"{B}/SF61745.csv"))}
mine = {date.fromisoformat(f): v for f, v in json.load(open("bmx.json"))["SF43718"]}
dif = [k for k in set(fx) | set(mine) if fx.get(k) != mine.get(k)]
print("FIX: fechas distintas entre descargas:", len(dif), sorted(dif)[:5])
def last_on_or_before(t):
    while t not in fx: t -= timedelta(days=1)
    return t, fx[t]
def plus_months(t, m):
    import calendar
    y = t.year + (t.month - 1 + m) // 12; mo = (t.month - 1 + m) % 12 + 1
    return date(y, mo, min(t.day, calendar.monthrange(y, mo)[1]))
for e in [date(2006,2,24), date(2014,6,6), date(2026,3,27), date(2006,3,28), date(2015,12,16), date(2026,9,17), date(2006,1,27), date(2013,9,6), date(2025,6,27)]:
    t0, x0 = last_on_or_before(e)
    row = [f"{e} FIX0={x0}"]
    for m in (1,3,6,12):
        tt = plus_months(e, m)
        if tt > max(fx): row.append(f"{m}m=NA"); continue
        t1, x1 = last_on_or_before(tt); row.append(f"{m}m({t1})={100*(x1/x0-1):.2f}")
    end = plus_months(e, 12)
    w = [(k, v) for k, v in fx.items() if e < k <= end]
    k, v = max(w, key=lambda z: z[1]); row.append(f"max12={100*(v/x0-1):.2f}@{k}")
    print(" ".join(row))
# tasa objetivo alrededor de fechas clave
for d in [date(2014,6,5),date(2014,6,6),date(2015,12,16),date(2015,12,17),date(2026,3,26),date(2026,3,27),date(2026,5,7),date(2026,5,8),date(2026,9,30)]:
    print(d, "objetivo", ob.get(d))
