"""R21 (ejecución A): ¿cambian las probabilidades de cortacircuitos de R18 si al 3x sintético se le resta la brecha
medida en R20 (UPRO real contra sintético)? Pre-registro: R21-r18-con-brecha-r20.md (mismo commit).
Datos: los de R18 (cachés de R16 y R12). Reproduce: python3 laboratorio/replicas/R21.py"""
import json, math, os, sys
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import R16, R18  # noqa: E402

PESOS = {"U13.5 (vigente tras W43 B1)": 0.135, "U27 (antes de B1)": 0.269}
NIVELES, HORIZONTES = (0.12, 0.20), (63, 126)
# brecha anual en pp, de R20 lado A con DTB3 (tramos <0.5%, 0.5-3%, >=3%) y M1 total
TRAMOS_A = [(-1, 0.5, 1.31), (0.5, 3.0, 1.54), (3.0, 99, 2.30)]
CONSTANTE = 1.59


def rendimientos(D, ndx, modo):
    fechas, px, op, lo, tr, vix, rf = D
    sen = R16.filtro(px, vix)
    out = []
    for i in range(2, len(fechas)):
        d, d0 = fechas[i], fechas[i - 1]
        if d not in ndx or d0 not in ndx or sen[i - 2] is None:
            continue
        r1 = tr[i] / tr[i - 1] - 1
        r3 = 3 * r1 - 2 * rf[i] - R18.GASTO_UPRO
        tasa = rf[i] * 252 * 100
        if modo == "constante":
            r3 -= CONSTANTE / 100 / 252
        elif modo == "tramos":
            r3 -= next(b for lo_, hi, b in TRAMOS_A if lo_ <= tasa < hi) / 100 / 252
        rq = ndx[d] / ndx[d0] - 1 - R18.GASTO_QQQM
        out.append((d, r1 - R18.GASTO_SPYM, rq, r3 if sen[i - 2] == 1 else rf[i], rf[i]))
    return out


def prob(eq, nivel, H):
    n = toques = 0
    for t in range(0, len(eq) - H - 1):
        pico = eq[t]
        for k in range(t + 1, t + H + 1):
            pico = max(pico, eq[k])
            if eq[k] / pico - 1 <= -nivel:
                toques += 1; break
        n += 1
    return toques / n


def cagr(eq, n_dias):
    return (eq[-1] / eq[0]) ** (252 / n_dias) - 1


if __name__ == "__main__":
    D, ndx, sha = R18.cargar()
    res = {"sha256_r16": sha}
    for modo in ("sin brecha", "constante", "tramos"):
        R = rendimientos(D, ndx, modo)
        res[modo] = {}
        for nom, w in PESOS.items():
            eq = R18.curva(R, w)
            fila = {"CAGR_pct": round(cagr(eq, len(R)) * 100, 3)}
            for nv in NIVELES:
                for H in HORIZONTES:
                    fila[f"P{int(nv*100)}_{H}d"] = round(prob(eq, nv, H) * 100, 2)
            res[modo][nom] = fila
        res[modo]["n_dias"] = len(R); res[modo]["periodo"] = [R[0][0], R[-1][0]]
    v = "U13.5 (vigente tras W43 B1)"
    dP = res["tramos"][v]["P12_126d"] - res["sin brecha"][v]["P12_126d"]
    dC = res["tramos"][v]["CAGR_pct"] - res["sin brecha"][v]["CAGR_pct"]
    res["H1_dP12_126d_vigente_pp"] = round(dP, 2); res["H1_sostenida"] = dP <= 1.0
    res["H2_dCAGR_vigente_pp"] = round(dC, 3); res["H2_sostenida"] = -0.30 <= dC <= -0.10
    print(json.dumps(res, indent=1, ensure_ascii=False))
    json.dump(res, open(os.path.join(BASE, "R21-resultados.json"), "w"), indent=1, ensure_ascii=False)
