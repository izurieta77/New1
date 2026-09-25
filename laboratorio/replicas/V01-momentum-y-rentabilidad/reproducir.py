"""V01 - Verificacion independiente: momentum (MOM) y rentabilidad (RMW) de Kenneth French.
Reproduce: python3 laboratorio/replicas/V01-momentum-y-rentabilidad/reproducir.py  (desde la raiz del repo)
Datos congelados en ./datos (ver SHA256SUMS.txt). Sin red.

Version 2 (2026-09-25, segunda corrida). Cambios respecto de la version 1 (05:14 UTC):
- Cada ventana reporta ademas: desviacion estandar, t convencional (IID), media x12 (no es CAGR),
  rendimiento anual compuesto de la serie largo-corto (no es el rendimiento de una cuenta),
  peor y mejor mes. Las claves de la version 1 (n, media, se, t, t_iid, ic95, rezagos,
  veredicto) no cambian de nombre ni de valor.
- Sensibilidad (no pre-registrada; ya citada en el README de la version 1): RMW 2000-01 a 2026-07
  y el detalle de RMW de ene-2026 a jul-2026.
- Contraste con las auditorias ciegas AC-01 y AC-02 (fuente A de cada una), si sus
  resultados.json existen. Se guarda la huella SHA-256 de cada archivo contrastado.
- SHA256SUMS.txt incluye ahora reproducir.py: si el codigo cambia, el script se detiene.
"""
import hashlib, json, math, os, re, statistics, sys, zipfile
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, RAIZ)
from herramientas.estadistica import newey_west, veredicto
from herramientas.huellas import verificar

AQUI = os.path.dirname(os.path.abspath(__file__))
AUDITORIAS = os.path.join(RAIZ, "laboratorio", "auditorias")


def sha256(ruta):
    with open(ruta, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


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
    assert all(v > -99 for v in out.values()), "faltantes (-99.99/-999) en la serie"
    return out, lineas[0].strip()


def ventana(d, a, b): return [(k, v) for k, v in sorted(d.items()) if a <= k <= b]


def estadisticos(d, a, b):
    pares = ventana(d, a, b)
    x = [v for _, v in pares]
    r = newey_west(x, 6)
    r["veredicto"] = veredicto(r["ic95"])
    r["desde"], r["hasta"] = pares[0][0], pares[-1][0]
    r["de"] = statistics.stdev(x)
    r["x12_no_es_cagr"] = 12 * r["media"]
    # (prod(1 + r_t/100))^(12/n) - 1, en %: compuesto de la serie largo-corto; no es una cuenta.
    r["compuesto_anual_pct"] = 100 * (math.exp(12 / len(x) * math.fsum(math.log1p(v / 100) for v in x)) - 1)
    peor = min(pares, key=lambda p: p[1]); mejor = max(pares, key=lambda p: p[1])
    r["peor_mes"] = {"mes": peor[0], "pct": peor[1]}
    r["mejor_mes"] = {"mes": mejor[0], "pct": mejor[1]}
    return r


fallas = verificar(os.path.join(AQUI, "SHA256SUMS.txt"))
assert not [f for f in fallas if f.startswith("datos/")], f"los datos congelados cambiaron: {fallas}"
assert not fallas, f"el codigo cambio respecto de SHA256SUMS.txt (regenera el manifiesto si es intencional): {fallas}"

mom, v1 = cargar("F-F_Momentum_Factor_CSV.zip", "Mom")
rmw, v2 = cargar("F-F_Research_Data_5_Factors_2x3_CSV.zip", "RMW")
res = {"version_datos": {"Mom": v1, "RMW": v2}, "MOM": {}, "RMW": {}}
for a, b in [(198401, 200609), (200610, 202512), (200610, 201512), (201601, 202512)]:
    res["MOM"][f"{a}-{b}"] = estadisticos(mom, a, b)
for a, b in [(196307, 199912), (200001, 202512), (201501, 202512), (201601, 202512)]:
    res["RMW"][f"{a}-{b}"] = estadisticos(rmw, a, b)

# Sensibilidad (no pre-registrada): la serie completa hasta el ultimo mes publicado.
m26 = ventana(rmw, 202601, 202607)
res["sensibilidad"] = {
    "nota": "No pre-registrada. Ventana hasta el ultimo mes del archivo (CRSP 202607).",
    "RMW 200001-202607": estadisticos(rmw, 200001, 202607),
    "RMW 202601-202607 (meses)": {
        "n": len(m26), "suma_pct": math.fsum(v for _, v in m26),
        "media_pct": math.fsum(v for _, v in m26) / len(m26),
        "meses_negativos": sum(1 for _, v in m26 if v < 0),
        "serie": {str(k): v for k, v in m26},
    },
}

# Contraste con las auditorias ciegas (fuente A de cada una: mismos bytes, codigo independiente).
CLAVES_AC = {
    "AC-01-momentum-eua": ("MOM", "A_French_Mom", {"W1": "198401-200609", "W2": "200610-202512", "W3": "200610-201512", "W4": "201601-202512"}),
    "AC-02-rentabilidad-eua": ("RMW", "A_FF5_RMW", {"W1": "196307-199912", "W2": "200001-202512", "W3": "201501-202512", "W4": "201601-202512"}),
}
res["contraste_auditorias"] = {}
for ac, (fac, fuente, mapa) in CLAVES_AC.items():
    ruta = os.path.join(AUDITORIAS, ac, "resultados.json")
    if not os.path.exists(ruta):
        res["contraste_auditorias"][ac] = "no encontrado"; continue
    aud = json.load(open(ruta))
    est = aud["estadisticos"][fuente]
    filas = {}
    for w, k in mapa.items():
        e, p = est[w], res[fac][k]
        ic_a = e.get("ic95_nw_pct") or e.get("ic95_nw_mensual_pct")
        filas[k] = {
            "ventana_auditoria": w,
            "dif_n": e["n"] - p["n"],
            "dif_media": e["media_mensual_pct"] - p["media"],
            "dif_t_iid": e["t_iid"] - p["t_iid"],
            "dif_t_nw6": e["t_nw6"] - p["t"],
            "dif_compuesto_pct": e["compuesto_anual_pct"] - p["compuesto_anual_pct"],
            "dif_ic95": [ic_a[0] - p["ic95"][0], ic_a[1] - p["ic95"][1]],
            "mismo_veredicto": e["veredicto"] == p["veredicto"],
        }
    res["contraste_auditorias"][ac] = {
        "archivo": os.path.relpath(ruta, RAIZ), "sha256": sha256(ruta),
        "sha256_fuente_A_auditoria": {k: v for k, v in aud["sha256"].items() if k in (
            "F-F_Momentum_Factor_CSV.zip", "F-F_Research_Data_5_Factors_2x3_CSV.zip")},
        "nota_ic": "Las auditorias usan z = 1.96; V01 usa z = 1.959964 (herramientas/estadistica.py).",
        "ventanas": filas,
    }

res["huellas_codigo"] = {
    "laboratorio/replicas/V01-momentum-y-rentabilidad/reproducir.py": sha256(os.path.abspath(__file__)),
    "herramientas/estadistica.py": sha256(os.path.join(RAIZ, "herramientas", "estadistica.py")),
}

with open(os.path.join(AQUI, "resultados.json"), "w") as f:
    json.dump(res, f, indent=1)

print("x12 = media mensual x 12 (no es CAGR). Compuesto = (prod(1+r))^(12/n)-1 de la serie largo-corto (no es una cuenta).")
for fac in ("MOM", "RMW"):
    for k, r in res[fac].items():
        print(f"{fac} {k}: n={r['n']} media={r['media']:.4f}%/mes DE={r['de']:.3f} t_IID={r['t_iid']:.2f} "
              f"t_NW6={r['t']:.2f} IC95=[{r['ic95'][0]:.3f},{r['ic95'][1]:.3f}] x12={r['x12_no_es_cagr']:.2f}% "
              f"compuesto={r['compuesto_anual_pct']:.2f}% {r['veredicto']}")
r = res["sensibilidad"]["RMW 200001-202607"]
print(f"[sensibilidad] RMW 200001-202607: n={r['n']} x12={r['x12_no_es_cagr']:.2f}% compuesto={r['compuesto_anual_pct']:.2f}% "
      f"t_IID={r['t_iid']:.2f} t_NW6={r['t']:.2f} {r['veredicto']}")
m = res["sensibilidad"]["RMW 202601-202607 (meses)"]
print(f"[sensibilidad] RMW ene-jul 2026: suma={m['suma_pct']:.2f}% media={m['media_pct']:.3f}%/mes meses negativos={m['meses_negativos']} de {m['n']}")
for ac, c in res["contraste_auditorias"].items():
    if isinstance(c, str):
        print(f"[contraste] {ac}: {c}"); continue
    peor = max(max(abs(v["dif_media"]), abs(v["dif_t_iid"]), abs(v["dif_t_nw6"]), abs(v["dif_compuesto_pct"]),
                   abs(v["dif_ic95"][0]), abs(v["dif_ic95"][1])) for v in c["ventanas"].values())
    iguales = all(v["mismo_veredicto"] and v["dif_n"] == 0 for v in c["ventanas"].values())
    print(f"[contraste] {ac} (fuente A): max |dif| en media, t IID, t NW, compuesto e IC = {peor:.6f}; "
          f"mismo n y veredicto en las 4 ventanas: {iguales}")
