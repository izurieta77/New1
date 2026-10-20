"""R17 (ejecución A): exposición por volatilidad objetivo en el 3x sintético del S&P 500 TR, encima del filtro vigente.
Pre-registro: R17-volatilidad-objetivo-upro.md (mismo commit que este script). Fuentes A: Yahoo ^GSPC, ^SP500TR, ^VIX; FRED DTB3
(caché de R16: R16-datos/series.json, mismo FIN 2026-10-16).
Reproduce: python3 laboratorio/replicas/R17.py"""
import json, math, os, sys
from datetime import date
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import R16  # noqa: E402  (reutiliza carga, preparación y filtro V0 de R16; ya auditados en AC-22)

COSTO, GASTO = 0.0010, 0.0091 / 252
OBJETIVOS = {"VT30": 0.30, "VT45": 0.45, "VT60": 0.60}
VENTANA, BANDA = 20, 0.10   # vol realizada de 20 días del 3x; rebalanceo semanal solo si |w* − w| > 10 pp


def simular(D, sen, objetivo=None, desde=None, hasta=None):
    fechas, px, op, lo, tr, vix, rf = D
    r3 = [None] + [3 * (tr[i] / tr[i - 1] - 1) - 2 * rf[i] - GASTO for i in range(1, len(tr))]
    i0 = next(i for i, x in enumerate(sen) if x is not None) + 2
    i0 = max(i0, VENTANA + 2)
    if desde: i0 = max(i0, next(i for i, d in enumerate(fechas) if d >= desde))
    i1 = len(fechas) - 1 if not hasta else max(i for i, d in enumerate(fechas) if d <= hasta)
    eq, exc, w, wsum, cambios = [1.0], [], 0.0, 0.0, 0
    for i in range(i0, i1 + 1):
        r = w * r3[i] + (1 - w) * rf[i]
        e = eq[-1] * (1 + r)
        exc.append(r - rf[i]); wsum += w
        # decisión al cierre de i con información hasta i-1 (señal del filtro de i-1), ejecutada al cierre de i
        filtro = sen[i - 1] == 1
        if objetivo is None:
            obj = 1.0 if filtro else 0.0
        else:
            xs = r3[i - VENTANA:i]
            m = sum(xs) / len(xs); sd = math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1)) * math.sqrt(252)
            obj = min(1.0, objetivo / sd) if filtro else 0.0
        semanal = date.fromisoformat(fechas[i]).weekday() == 4   # viernes
        if (obj == 0.0 and w > 0) or (obj > 0 and w == 0) or (semanal and abs(obj - w) > BANDA):
            e *= 1 - COSTO * abs(obj - w); cambios += 1; w = obj
        eq.append(e)
    a = (date.fromisoformat(fechas[i1]) - date.fromisoformat(fechas[i0])).days / 365.25
    mu = sum(exc) / len(exc); sd = math.sqrt(sum((x - mu) ** 2 for x in exc) / (len(exc) - 1))
    pico, mdd = eq[0], 0.0
    for v in eq: pico = max(pico, v); mdd = min(mdd, v / pico - 1)
    return dict(desde=fechas[i0], hasta=fechas[i1], cagr=eq[-1] ** (1 / a) - 1, vol=sd * math.sqrt(252),
                sharpe=mu / sd * math.sqrt(252), mdd=mdd, cambios=cambios, exposicion_media=wsum / (i1 - i0 + 1))


if __name__ == "__main__":
    s, sha = R16.cargar()
    D = R16.preparar(s)
    sen = R16.filtro(D[1], D[5])
    L = [f"Datos de R16 (Yahoo + DTB3): {len(D[0])} días {D[0][0]} a {D[0][-1]}; sha256 {sha[:16]}…"]
    out = {}
    for pn, (de, ha) in {"completo": (None, None), "1990-2008": (None, "2008-12-31"), "2009-hoy": ("2009-01-01", None)}.items():
        L.append(f"\n== {pn}")
        for nombre, obj in [("V0 filtro vigente", None)] + list(OBJETIVOS.items()):
            r = simular(D, sen, obj, de, ha); out[f"{pn}|{nombre}"] = r
            L.append(f"{nombre:18s} CAGR {r['cagr']:+.1%} vol {r['vol']:.1%} Sharpe {r['sharpe']:.3f} MDD {r['mdd']:.1%} "
                     f"exposición media {r['exposicion_media']:.2f} cambios {r['cambios']} [{r['desde']}→{r['hasta']}]")
    v0, v45 = out["completo|V0 filtro vigente"], out["completo|VT45"]
    h1 = (v45["mdd"] - v0["mdd"]) >= 0.05 and (v45["sharpe"] - v0["sharpe"]) >= -0.03
    h2 = v45["sharpe"] > v0["sharpe"]
    estado = "Replicado" if h1 else "No replicado"
    L.append(f"\nΔMDD (VT45 − V0) {(v45['mdd'] - v0['mdd']) * 100:+.1f} pp; ΔSharpe {v45['sharpe'] - v0['sharpe']:+.3f}")
    L.append(f"Veredicto A: H1 {'sostenida' if h1 else 'refutada'}; H2 {'sostenida' if h2 else 'refutada'} -> {estado}")
    txt = "\n".join(L) + "\n"
    open(os.path.join(BASE, "R17-salida.txt"), "w").write(txt)
    json.dump({"sha256_datos": sha, "veredicto": {"H1": h1, "H2": h2, "estado_A": estado}, "resultados": out},
              open(os.path.join(BASE, "R17-resultados.json"), "w"), indent=1)
    sys.stdout.write(txt)
