"""AC-24-R18 · Adenda 24-oct-2026: P(tocar −12% / −20%) con la métrica del cortacircuitos (lado B).

`herramientas/riesgo.estado_cortacircuitos` (L82-L89) mide DD(t) = índice(t)/max_{s≤t} índice(s) − 1,
con el máximo desde el inicio de la cuenta. Aquí se calcula, sobre la curva B de la mezcla:

  (a)  cuenta nueva en t0 (pico = índice(t0)); P(DD toca −u en t0+1..t0+H). Es la métrica de R18.
  (a') definición del lado A (abogado W43): pico = máximo desde el inicio de la serie (1990);
       inicios con DD(t0) > −u.  Y (a'c) lo mismo condicionado a DD(t0) ∈ [−5%, −2%].
  (b)  condicional al estado de hoy: pico de la cuenta = max(índice[t0−L .. t0]) con L = 20/25/30
       días hábiles (vida previa ≈ 20 sesiones: la cuenta abrió el 28-sep-2026); se condiciona a
       DD(t0) ∈ [−3.8%, −2.8%] (hoy −3.3%) y se mide P(DD contra ese pico, con el pico actualizándose
       si hay máximos nuevos, toque −u en t0+1..t0+H). Sensibilidad: L = 63 y 126.

Curvas: las de `b.py` (fuente B: CBOE SPX + dividendo multpl, CBOE VIX, FRED DTB3, FRED NASDAQ100;
V0 con histéresis, señal t−2, rebalanceo mensual). b.py se ejecuta con runpy y su JSON va a un
temporal (no se toca `b-resultados.json`). La métrica se escribe aquí. No se leyó `R18.py`.

Uso: python3 -I ac24_maximo_historico.py <carpeta_datos> [salida_json]
"""
import contextlib, io, json, os, runpy, sys, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, "datos")
SALIDA = sys.argv[2] if len(sys.argv) > 2 else None
HS = (63, 126, 252)  # 252: solo para cotejar la columna "cuenta nueva, −20% en 252 d" de A
US = (0.12, 0.20)
BANDA_B = (-0.038, -0.028)
BANDA_A = (-0.05, -0.02)
LS = (20, 25, 30, 63, 126)

tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False).name
argv0 = sys.argv
sys.argv = [os.path.join(AQUI, "b.py"), DATOS, tmp]
with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path(os.path.join(AQUI, "b.py"), run_name="b_ac24")
sys.argv = argv0
os.unlink(tmp)
curva, VARIANTES = g["curva"], g["VARIANTES"]


def toca(val, t0, pico, h, u):
    """¿DD contra max(pico, índice[t0+1..s]) llega a −u para algún s en t0+1..t0+h?"""
    for s in range(t0 + 1, t0 + h + 1):
        if val[s] > pico:
            pico = val[s]
        elif val[s] / pico - 1 <= -u + 1e-12:
            return True
    return False


def bloques(idx, h):
    """Número de grupos de inicios separados por huecos > h (aprox. de episodios independientes)."""
    n, ult = 0, None
    for t in idx:
        if ult is None or t - ult > h:
            n += 1
        ult = t
    return n


def prob(val, inicios_pico, h, u):
    """inicios_pico: lista de (t0, pico). Devuelve p, k, n, bloques de inicios con toque."""
    hit = [t for t, pk in inicios_pico if toca(val, t, pk, h, u)]
    n = len(inicios_pico)
    return {"p": len(hit) / n if n else None, "k": len(hit), "n": n,
            "bloques_toque": bloques(hit, h), "bloques_inicios": bloques([t for t, _ in inicios_pico], h)}


out = {"HS": HS, "US": US, "banda_b": BANDA_B, "banda_a": BANDA_A, "variantes": {}}
lin = []
for nombre, wu in VARIANTES.items():
    f, v = curva(wu)
    m = len(v)
    # máximo acumulado desde el inicio de la serie
    cm, mx = [], 0.0
    for x in v:
        mx = max(mx, x)
        cm.append(mx)
    d = {}
    for h in HS:
        ult = m - h  # t0 < ult => ventana completa
        for u in US:
            k = f"H{h}_{int(u*100)}"
            # (a) cuenta nueva
            d[f"a_{k}"] = prob(v, [(t, v[t]) for t in range(ult)], h, u)
            d[f"a_sintraslape_{k}"] = prob(v, [(t, v[t]) for t in range(0, ult, h)], h, u)
            # (a') definición A: máximo desde 1990, arranca arriba de −u
            d[f"aA_{k}"] = prob(v, [(t, cm[t]) for t in range(ult) if v[t] / cm[t] - 1 > -u], h, u)
            d[f"aAc_{k}"] = prob(v, [(t, cm[t]) for t in range(ult)
                                     if BANDA_A[0] <= v[t] / cm[t] - 1 <= BANDA_A[1]], h, u)
            # (b) pico = max de los L días previos (incluye t0), DD(t0) en la banda de hoy
            for L in LS:
                ip = []
                for t in range(L, ult):
                    pk = max(v[t - L:t + 1])
                    if BANDA_B[0] <= v[t] / pk - 1 <= BANDA_B[1]:
                        ip.append((t, pk))
                d[f"b_L{L}_{k}"] = prob(v, ip, h, u)
    out["variantes"][nombre] = d
    lin.append(f"\nUPRO {nombre}")
    for h in HS:
        for u in US:
            k = f"H{h}_{int(u*100)}"
            r = lambda key: f"{d[key]['p']:.1%} ({d[key]['k']}/{d[key]['n']}, {d[key]['bloques_toque']} bl)"
            lin.append(f"  H={h:3d} −{int(u*100)}%  a {r('a_'+k)} | a sin trasl {r('a_sintraslape_'+k)} | "
                       f"A-def {r('aA_'+k)} | A-def cond[-5,-2] {r('aAc_'+k)}")
            lin.append("              b: " + "  ".join(f"L{L} {r(f'b_L{L}_{k}')}" for L in LS))
print("\n".join(lin))
if SALIDA:
    json.dump(out, open(SALIDA, "w"), indent=2, ensure_ascii=False)
