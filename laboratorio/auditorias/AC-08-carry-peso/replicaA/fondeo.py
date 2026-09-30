import sys, json
sys.path.insert(0, "/home/user/New1")
from herramientas import banxico as b
d = b.rango("SF43773","2005-01-01","2026-09-30")
json.dump([(str(f),v) for f,v in d], open("fondeo43773.json","w"))
print(len(d), d[:2], d[-2:])
