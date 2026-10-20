"""Contraste del Brier real (bitacora/pronosticos.csv, resueltos) contra el esperado con calibración perfecta.
Spiegelhalter (1986): bajo calibración perfecta, Z = Σ(o−p)(1−2p) / sqrt(Σ(1−2p)² p(1−p)) ~ N(0,1).
Murphy (1973) por cubetas de 10 pp: BS = REL − RES + UNC (+ término de varianza dentro de la cubeta).
Reproduce: python3 conocimiento/fichas/codigo/2026-10-20-brier-contraste-real.py"""
import csv, math, os, random
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
filas = [r for r in csv.DictReader(open(os.path.join(RAIZ, "bitacora", "pronosticos.csv"), encoding="utf-8"))
         if r["resultado"] in ("0", "1")]
def analiza(F, etiqueta):
    p = [float(r["probabilidad"]) for r in F]; o = [int(r["resultado"]) for r in F]; n = len(p)
    bs = sum((a - b) ** 2 for a, b in zip(p, o)) / n
    esperado = sum(a * (1 - a) for a in p) / n                     # Brier esperado si p fuera la probabilidad verdadera
    num = sum((b - a) * (1 - 2 * a) for a, b in zip(p, o)); den = math.sqrt(sum((1 - 2 * a) ** 2 * a * (1 - a) for a in p))
    z = num / den
    # Murphy por cubetas de 10 pp
    cub = {}
    for a, b in zip(p, o): cub.setdefault(min(int(a * 10), 9), []).append((a, b))
    obar = sum(o) / n
    rel = sum(len(v) * (sum(a for a, _ in v) / len(v) - sum(b for _, b in v) / len(v)) ** 2 for v in cub.values()) / n
    res = sum(len(v) * (sum(b for _, b in v) / len(v) - obar) ** 2 for v in cub.values()) / n
    unc = obar * (1 - obar)
    wbv = sum(sum((a - sum(x for x, _ in v) / len(v)) ** 2 for a, _ in v) for v in cub.values()) / n  # varianza de p dentro de la cubeta
    wbc = sum(sum(2 * (a - sum(x for x, _ in v) / len(v)) * (sum(x for x, _ in v) / len(v) - b) for a, b in v) for v in cub.values()) / n
    assert abs(bs - (rel - res + unc + wbv + wbc)) < 1e-9, "identidad de Murphy extendida"
    # simulación: distribución del Brier de un pronosticador calibrado con estas mismas p
    random.seed(20261020)
    sims = [sum((a - (1 if random.random() < a else 0)) ** 2 for a in p) / n for _ in range(20000)]
    p_sobre = sum(s >= bs for s in sims) / len(sims)
    p_meta = sum(s <= 0.20 for s in sims) / len(sims)
    sesgo = sum(o) / n - sum(p) / n
    print(f"{etiqueta:8s} n={n:3d} Brier {bs:.4f} | esperado calibrado {esperado:.4f} | Spiegelhalter Z {z:+.2f} | "
          f"P(sim ≥ real) {p_sobre:.2f} | P(sim ≤ 0.20) {p_meta:.2f} | frecuencia − p media {sesgo:+.3f} | REL {rel:.4f} RES {res:.4f} UNC {unc:.4f}")
    return dict(n=n, bs=bs, esp=esperado, z=z, p_sobre=p_sobre, p_meta=p_meta, sesgo=sesgo, rel=rel, res=res, unc=unc)
g = analiza(filas, "GLOBAL")
for autor in ("claude", "vigia"):
    analiza([r for r in filas if r["autor"] == autor], autor)
# Comprobación a mano de la fórmula del esperado con dos pronósticos: 0.7 y 0.4 -> (0.21 + 0.24)/2 = 0.225
assert abs(((0.7 * 0.3) + (0.4 * 0.6)) / 2 - 0.225) < 1e-12
print("Todas las aserciones pasaron.")
