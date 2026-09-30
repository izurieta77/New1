import os, sys, json, time, urllib.request
sys.path.insert(0, "/home/user/New1")
assert os.environ.get("BANXICO_TOKEN"), "exporta BANXICO_TOKEN (no se guarda en git)"
from herramientas import banxico
D = os.path.dirname(os.path.abspath(__file__))
out = {}
# FIX, objetivo, CETES 28/91/182/364, TIIE28, fondeo bancario
for sid in ["SF43718","SF61745","SF43936","SF43939","SF43942","SF43945","SF43783","SF43773"]:
    try:
        rows = banxico.rango(sid, "2005-01-01", "2026-10-05")
        out[sid] = [(d.isoformat(), v) for d, v in rows]
        print(sid, len(rows), rows[0], rows[-1])
    except Exception as e:
        print(sid, "ERR", type(e).__name__)
json.dump(out, open(f"{D}/bmx.json","w"))
for s in ["DFEDTARU","DFEDTARL","DFEDTAR","DFF","DTB3","DTB4WK","DGS1MO","DGS3MO"]:
    txt=None
    for i in range(3):
        try:
            txt = urllib.request.urlopen(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={s}", timeout=90).read().decode(); break
        except Exception as e:
            print(s,"retry",type(e).__name__); time.sleep(3)
    if txt:
        open(f"{D}/{s}.csv","w").write(txt); L=txt.strip().splitlines(); print(s, len(L), L[1], L[-1])
