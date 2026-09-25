"""V01 - Verificacion independiente: momentum (MOM) y rentabilidad (RMW) de Kenneth French.
Reproduce: python3 laboratorio/replicas/V01-momentum-y-rentabilidad/reproducir.py  (desde la raiz del repo)
Datos congelados en ./datos (ver SHA256SUMS.txt). Sin red."""
import json, os, re, sys, zipfile
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from herramientas.estadistica import newey_west, veredicto
from herramientas.huellas import verificar

AQUI = os.path.dirname(os.path.abspath(__file__))

def cargar(nombre, col):
    z = zipfile.ZipFile(os.path.join(AQUI, "datos", nombre))
    lineas = z.read(z.namelist()[0]).decode("latin-1").splitlines()
    hdr, out = None, {}
    for ln in lineas:
        s = [c.strip() for c in ln.split(",")]
        if hdr is None and len(s) > 1 and s[0] == "" and col in s:
            hdr = s; continue
        if hdr is not None:
            if not re.match(r"^\d{6}$", s[0] or ""):
                if out: break
                continue
            out[int(s[0])] = float(s[hdr.index(col)])
    meses = sorted(out); idx = [m // 100 * 12 + m % 100 for m in meses]
    assert all(b - a == 1 for a, b in zip(idx, idx[1:])), "meses no consecutivos"
    return out, lineas[0].strip()

def ventana(d, a, b): return [v for k, v in sorted(d.items()) if a <= k <= b]

assert verificar(os.path.join(AQUI, "SHA256SUMS.txt")) == [], "los datos congelados cambiaron"
mom, v1 = cargar("F-F_Momentum_Factor_CSV.zip", "Mom")
rmw, v2 = cargar("F-F_Research_Data_5_Factors_2x3_CSV.zip", "RMW")
res = {"version_datos": {"Mom": v1, "RMW": v2}, "MOM": {}, "RMW": {}}
for a, b in [(198401, 200609), (200610, 202512), (200610, 201512), (201601, 202512)]:
    r = newey_west(ventana(mom, a, b), 6); r["veredicto"] = veredicto(r["ic95"]); res["MOM"][f"{a}-{b}"] = r
for a, b in [(196307, 199912), (200001, 202512), (201501, 202512), (201601, 202512)]:
    r = newey_west(ventana(rmw, a, b), 6); r["veredicto"] = veredicto(r["ic95"]); res["RMW"][f"{a}-{b}"] = r
with open(os.path.join(AQUI, "resultados.json"), "w") as f:
    json.dump(res, f, indent=1)
for fac in ("MOM", "RMW"):
    for k, r in res[fac].items():
        print(f"{fac} {k}: n={r['n']} media={r['media']:.4f}%/mes (x12={12*r['media']:.2f}%) t_NW6={r['t']:.2f} IC95=[{r['ic95'][0]:.3f},{r['ic95'][1]:.3f}] {r['veredicto']}")
