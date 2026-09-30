import sys, json
sys.path.insert(0, "/home/user/New1")
from herramientas import banxico as b
for sid in ["SF331451","SF43773","SF43758","SF61745","SF17801"]:
    try:
        p = b._fetch(f"{b.BASE}/{sid}")
        for s in p.get("bmx",{}).get("series",[]):
            print(sid, "|", s.get("titulo"), "|", s.get("fechaInicio"), s.get("fechaFin"), s.get("periodicidad"))
    except Exception as e:
        print(sid, "ERR", type(e).__name__, str(e)[:80])
d = b.rango("SF331451","2005-01-01","2008-03-31")
json.dump([(str(f),v) for f,v in d], open("fondeo.json","w"))
print(len(d), d[:2], d[-2:])
