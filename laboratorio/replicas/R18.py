"""R18 (ejecución A): probabilidad de tocar el cortacircuitos (−8%) en 63 días hábiles con la mezcla del papel GBM
(SPYM ≈ S&P 500 TR 1x, QQQM ≈ Nasdaq-100 1x, UPRO ≈ 3x sintético del S&P con filtro V0, efectivo a T-bill).
Pre-registro: R18-tamano-upro-cortacircuitos.md (mismo commit). Datos: cachés de R16 (^GSPC, ^SP500TR, ^VIX, DTB3) y R12 (^NDX).
Reproduce: python3 laboratorio/replicas/R18.py"""
import json, os, sys
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import R16  # noqa: E402

GASTO_UPRO, GASTO_SPYM, GASTO_QQQM = 0.0091 / 252, 0.0002 / 252, 0.0015 / 252
VARIANTES = {"U0": 0.0, "U13": 0.135, "U27 (vigente)": 0.269, "U40": 0.40}   # peso de UPRO; QQQM 0.268 y efectivo 0.053 fijos; SPYM el resto
H, NIVELES = 63, (0.08, 0.12)


def cargar():
    s, sha = R16.cargar()
    D = R16.preparar(s)
    ndx = {d: v for d, v in json.load(open(os.path.join(BASE, "R12-datos", "series.json")))["^NDX"]}
    return D, ndx, sha


def rendimientos(D, ndx):
    fechas, px, op, lo, tr, vix, rf = D
    sen = R16.filtro(px, vix)
    out = []
    for i in range(2, len(fechas)):
        d, d0 = fechas[i], fechas[i - 1]
        if d not in ndx or d0 not in ndx or sen[i - 2] is None:
            continue
        r1 = tr[i] / tr[i - 1] - 1
        r3 = 3 * r1 - 2 * rf[i] - GASTO_UPRO
        rq = ndx[d] / ndx[d0] - 1 - GASTO_QQQM
        out.append((d, r1 - GASTO_SPYM, rq, r3 if sen[i - 2] == 1 else rf[i], rf[i]))
    return out


def curva(R, wu):
    """Rebalanceo mensual a los pesos objetivo (cuando cambia el mes)."""
    wq, wc = 0.268, 0.053
    ws = 1 - wu - wq - wc
    eq, v, mes = [1.0], [ws, wq, wu, wc], None
    for d, rs, rq, ru, rf in R:
        if d[:7] != mes:
            tot = sum(v); v = [tot * ws, tot * wq, tot * wu, tot * wc]; mes = d[:7]
        v = [v[0] * (1 + rs), v[1] * (1 + rq), v[2] * (1 + ru), v[3] * (1 + rf)]
        eq.append(sum(v))
    return eq


def prob_toque(eq, nivel, desde=0, hasta=None):
    """Fracción de días de inicio t en los que, dentro de t+1..t+H, el valor cae ≥ nivel bajo el máximo desde t."""
    hasta = len(eq) - H - 1 if hasta is None else min(hasta, len(eq) - H - 1)
    n = toques = 0
    for t in range(desde, hasta + 1):
        pico, toco = eq[t], False
        for k in range(t + 1, t + H + 1):
            pico = max(pico, eq[k])
            if eq[k] / pico - 1 <= -nivel:
                toco = True; break
        n += 1; toques += toco
    return toques / n, n


if __name__ == "__main__":
    D, ndx, sha = cargar()
    R = rendimientos(D, ndx)
    fechas = [r[0] for r in R]
    i08 = next(i for i, d in enumerate(fechas) if d >= "2009-01-01")
    L = [f"Datos: R16 + ^NDX de R12; {len(R)} días con todas las series, {fechas[0]} a {fechas[-1]}; sha256 R16 {sha[:16]}…"]
    out = {}
    for nombre, wu in VARIANTES.items():
        eq = curva(R, wu)
        fila = {}
        for nv in NIVELES:
            p, n = prob_toque(eq, nv); pa, _ = prob_toque(eq, nv, hasta=i08); pb, _ = prob_toque(eq, nv, desde=i08)
            fila[f"{int(nv*100)}"] = dict(completo=p, h1990_2008=pa, h2009_hoy=pb, ventanas=n)
        out[nombre] = fila
        f8, f12 = fila["8"], fila["12"]
        L.append(f"{nombre:14s} P(−8% en 63d) {f8['completo']:.1%} [1990-2008 {f8['h1990_2008']:.1%} | 2009-hoy {f8['h2009_hoy']:.1%}]   "
                 f"P(−12%) {f12['completo']:.1%}   ventanas {f8['ventanas']}")
    p27, p13 = out["U27 (vigente)"]["8"]["completo"], out["U13"]["8"]["completo"]
    h1 = p27 <= 0.15
    h2 = (p27 - p13) >= 0.05
    estado = "Replicado" if h1 else "No replicado"
    L.append(f"\nVeredicto A: H1 (P vigente ≤ 15%) {'sostenida' if h1 else 'refutada'} ({p27:.1%}); "
             f"H2 (bajar a 13.5% reduce ≥ 5 pp) {'sostenida' if h2 else 'refutada'} ({(p27 - p13) * 100:.1f} pp) -> {estado}")
    txt = "\n".join(L) + "\n"
    open(os.path.join(BASE, "R18-salida.txt"), "w").write(txt)
    json.dump({"sha256_r16": sha, "veredicto": {"H1": h1, "H2": h2, "estado_A": estado}, "resultados": out},
              open(os.path.join(BASE, "R18-resultados.json"), "w"), indent=1)
    sys.stdout.write(txt)
