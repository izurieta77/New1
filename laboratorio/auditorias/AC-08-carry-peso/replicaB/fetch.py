import os, sys, json, csv, io, urllib.request
sys.path.insert(0, "/home/user/New1")
assert os.environ.get("BANXICO_TOKEN"), "exporta BANXICO_TOKEN (no se guarda en git)"
from herramientas import banxico
D = os.path.dirname(os.path.abspath(__file__))
for sid in ["SF43936", "SF43718", "SF61745"]:
    rows = banxico.rango(sid, "2005-01-01", "2026-10-05")
    with open(f"{D}/{sid}.csv", "w") as f:
        f.write("fecha,valor\n")
        for d, v in rows:
            f.write(f"{d.isoformat()},{v}\n")
    print(sid, len(rows), rows[0], rows[-1])
for s in []:
    req = urllib.request.Request(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={s}", headers={"User-Agent": "Mozilla/5.0"})
    txt = urllib.request.urlopen(req, timeout=60).read().decode()
    open(f"{D}/{s}.csv", "w").write(txt)
    lines = txt.strip().splitlines()
    print(s, len(lines), lines[0], lines[1], lines[-1])
