"""AC-24-R18 · Adenda 22-oct-2026: niveles del perfil `arena_agresivo` (−12/−20/−28/−35%), lado B.

Reutiliza las curvas de `b.py` (misma fuente B y misma construcción; b.py no tiene funciones
importables sin ejecutarse, así que se ejecuta con runpy redirigiendo su salida y su JSON a un
archivo temporal para no tocar `b-resultados.json`). La métrica de toque y el conteo de episodios
se escriben aquí.

Uso: python3 -I ac24_niveles_arena.py <carpeta_datos> [salida_json]
"""
import contextlib, io, json, os, runpy, sys, tempfile, datetime as dt

AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, "datos")
SALIDA = sys.argv[2] if len(sys.argv) > 2 else None
H = 63
NIVELES = (0.12, 0.20, 0.28, 0.35)

tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False).name
argv0 = sys.argv
sys.argv = [os.path.join(AQUI, "b.py"), DATOS, tmp]
with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path(os.path.join(AQUI, "b.py"), run_name="b_ac24")
sys.argv = argv0
os.unlink(tmp)
curva, VARIANTES = g["curva"], g["VARIANTES"]


def peor_ventana(val, t):
    """Peor caída V_s/max(V_t..V_s)-1, s en t+1..t+H; y el índice del pico vigente al tocar ese peor punto."""
    pico, ipico, peor, ipeor_pico = val[t], t, 0.0, t
    for s in range(t + 1, t + H + 1):
        if val[s] > pico:
            pico, ipico = val[s], s
        dd = val[s] / pico - 1
        if dd < peor:
            peor, ipeor_pico = dd, ipico
    return peor, ipeor_pico


def probs(fechas, val, paso=1):
    m = len(val)
    inicios = list(range(0, m - H, paso))
    res = {u: 0 for u in NIVELES}
    for t in inicios:
        p, _ = peor_ventana(val, t)
        for u in NIVELES:
            if p <= -u:
                res[u] += 1
    return {f"{int(u*100)}%": res[u] / len(inicios) for u in NIVELES}, {f"{int(u*100)}%": res[u] for u in NIVELES}, len(inicios)


def episodios(fechas, val, u):
    """Episodios distintos de caída ≥u en la curva: un episodio empieza cuando la caída desde el máximo
    acumulado toca −u y termina cuando la curva recupera ese máximo. Además, se agrupan los inicios t
    con toque en bloques contiguos (huecos > H días de inicio separan bloques)."""
    eps, pico, ipico, dentro, peor = [], val[0], 0, False, 0.0
    for i, v in enumerate(val):
        if v >= pico:
            if dentro:
                eps[-1]["recupera"] = str(fechas[i])
                dentro = False
            pico, ipico = v, i
            continue
        dd = v / pico - 1
        if dd <= -u and not dentro:
            dentro = True
            eps.append({"pico": str(fechas[ipico]), "toca": str(fechas[i]), "fondo_dd": dd, "recupera": None})
        if dentro and dd < eps[-1]["fondo_dd"]:
            eps[-1]["fondo_dd"] = dd
    # Bloques de inicios t cuya ventana de 63 días toca −u (caída desde el máximo dentro de la ventana).
    bloques, ult = [], None
    for t in range(0, len(val) - H):
        p, ip = peor_ventana(val, t)
        if p <= -u:
            if ult is None or t - ult > H:
                bloques.append({"desde": str(fechas[t]), "hasta": str(fechas[t]), "n_inicios": 0, "peor": p})
            b = bloques[-1]
            b["hasta"] = str(fechas[t]); b["n_inicios"] += 1; b["peor"] = min(b["peor"], p)
            ult = t
    return eps, bloques


out = {"H": H, "variantes": {}}
lin = []
for nombre, wu in VARIANTES.items():
    f, v = curva(wu)
    p, k, n = probs(f, v)
    ps, ks, ns = probs(f, v, paso=H)
    d = {"traslape": {"p": p, "k": k, "n": n}, "sin_traslape": {"p": ps, "k": ks, "n": ns}}
    lin.append(f"UPRO {nombre:16s} traslape(n={n}): " + "  ".join(f"P>={x} {p[x]:.1%}" for x in p)
               + f" | sin traslape(n={ns}): " + "  ".join(f"{x} {ps[x]:.1%} ({ks[x]})" for x in ps))
    d["episodios"] = {}
    for u in (0.20, 0.28):
        eps, bl = episodios(f, v, u)
        d["episodios"][f"{int(u*100)}%"] = {"drawdowns": eps, "bloques_ventanas": bl}
        lin.append(f"   ≥{int(u*100)}%: {len(eps)} drawdowns distintos, {len(bl)} bloques de ventanas")
        for b in bl:
            lin.append(f"      bloque {b['desde']}..{b['hasta']}  inicios {b['n_inicios']:4d}  peor {b['peor']:.1%}")
    out["variantes"][nombre] = d
print("\n".join(lin))
if SALIDA:
    json.dump(out, open(SALIDA, "w"), indent=2, ensure_ascii=False)
