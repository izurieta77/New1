import os, sys
sys.path.insert(0, "/home/user/New1")
assert os.environ.get("BANXICO_TOKEN"), "exporta BANXICO_TOKEN (no se guarda en git)"
from herramientas import banxico
print(banxico.oportuno(("SF43936","SF43718","SF61745")))
print(banxico.rango("SF43936","2026-09-01","2026-10-05"))
