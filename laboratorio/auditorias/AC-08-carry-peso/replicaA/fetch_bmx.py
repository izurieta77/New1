import sys, os, json
sys.path.insert(0, "/home/user/New1")
from herramientas import banxico as b
out = {}
for sid, desde in [("SF61745","2005-01-01"),("SF43718","2005-01-01"),("SF43936","2005-01-01"),("SF43783","2005-01-01")]:
    try:
        d = b.rango(sid, desde, "2026-09-30")
        out[sid] = [(str(f), v) for f, v in d]
        print(sid, len(d), d[0] if d else None, d[-1] if d else None)
    except Exception as e:
        print(sid, "ERR", type(e).__name__, str(e)[:100])
json.dump(out, open("bmx.json","w"))
