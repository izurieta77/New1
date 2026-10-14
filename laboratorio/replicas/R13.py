#!/usr/bin/env python3
"""R13 - Anomalia de devengos (Sloan, 1996), antes y despues de publicarse. Ejecucion A.

Reproduce desde la raiz del repo:  python3 laboratorio/replicas/R13.py
Pre-registro: laboratorio/replicas/R13-devengos-sloan.md (secciones 1-9).
Datos: French Data Library, Portfolios_Formed_on_AC (VW y EW, deciles y quintiles) y
F-F_Research_Data_5_Factors_2x3. Solo biblioteca estandar. Escribe R13-salida.txt,
R13-resultados.json y R13-variantes.csv (N = 4 variantes pre-registradas).
"""
from __future__ import annotations

import csv
import io
import json
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from herramientas import datos_historicos as dh  # noqa: E402
from herramientas import estadistica as est  # noqa: E402

AQUI = Path(__file__).resolve().parent
PRE = (date(1963, 7, 1), date(1996, 6, 30))
POST_INI = date(1996, 7, 1)
GHS_INI = date(2001, 1, 1)
COSTO_MENSUAL = 0.01 / 12
VARIANTES = [  # (id, seccion, largo, corto)
    ("VW_deciles", "Value Weighted Returns -- Monthly", "Lo 10", "Hi 10"),
    ("EW_deciles", "Equal Weighted Returns -- Monthly", "Lo 10", "Hi 10"),
    ("VW_quintiles", "Value Weighted Returns -- Monthly", "Lo 20", "Hi 20"),
    ("EW_quintiles", "Equal Weighted Returns -- Monthly", "Lo 20", "Hi 20"),
]


def largo_corto(tabla, largo, corto):
    serie = []
    for f, a, b in zip(tabla["fechas"], tabla["columnas"][largo], tabla["columnas"][corto]):
        if a is not None and b is not None:
            serie.append((f, a - b))
    return serie


def tramo(serie, ini, fin=None):
    return [v for f, v in serie if f >= ini and (fin is None or f <= fin)]


def ols(y, xs):
    """Coeficientes de y = a + b'x por ecuaciones normales (Gauss-Jordan); devuelve [a, b...]."""
    filas = [[1.0] + list(x) for x in xs]
    k = len(filas[0])
    xtx = [[sum(r[i] * r[j] for r in filas) for j in range(k)] for i in range(k)]
    xty = [sum(r[i] * yv for r, yv in zip(filas, y)) for i in range(k)]
    m = [row[:] + [v] for row, v in zip(xtx, xty)]
    for c in range(k):
        p = max(range(c, k), key=lambda r: abs(m[r][c]))
        m[c], m[p] = m[p], m[c]
        piv = m[c][c]
        m[c] = [v / piv for v in m[c]]
        for r in range(k):
            if r != c:
                fac = m[r][c]
                m[r] = [a - fac * b for a, b in zip(m[r], m[c])]
    beta = [m[i][k] for i in range(k)]
    resid = [yv - sum(b * v for b, v in zip(beta, r)) for r, yv in zip(filas, y)]
    return beta, resid


def alfa(serie, fac, cols, ini, fin=None):
    pares = [(v, [fac[f][c] for c in cols]) for f, v in serie
             if f in fac and f >= ini and (fin is None or f <= fin)]
    y = [p[0] for p in pares]
    xs = [p[1] for p in pares]
    beta, resid = ols(y, xs)
    # t NW del alfa: alfa + residuo es la serie "cubierta"; su media es alfa
    cubierta = [beta[0] + e for e in resid]
    nw = est.newey_west(cubierta, 6)
    return {"alfa_mensual": beta[0], "t_nw": nw["t"], "n": len(y)}


def resumen(x):
    nw = est.newey_west(x, 6)
    return {"n": nw["n"], "media_mensual": nw["media"], "anual_x12": nw["media"] * 12,
            "t_iid": nw["t_iid"], "t_nw6": nw["t"]}


def main():
    out = []
    p = out.append
    res = {"variantes": {}}
    tablas = {}
    for _, sec, _, _ in VARIANTES:
        if sec not in tablas:
            tablas[sec] = dh.french("Portfolios_Formed_on_AC", "mensual", sec)
    t0 = next(iter(tablas.values()))
    res["fuente"] = {"url": t0["url"], "sha256": t0["sha256"], "version_crsp": t0["version_crsp"],
                     "primer_mes": str(t0["fechas"][0]), "ultimo_mes": str(t0["fechas"][-1])}
    ff = dh.french("F-F_Research_Data_5_Factors_2x3", "mensual")
    fac = {f: {c: ff["columnas"][c][i] for c in ff["columnas"]} for i, f in enumerate(ff["fechas"])}
    p(f"Fuente A: {t0['url']} | CRSP {t0['version_crsp']} | sha256 {t0['sha256']}")
    p(f"Meses: {t0['fechas'][0]} a {t0['fechas'][-1]}; faltantes en tabla VW: {t0['faltantes']}")
    p(f"Factores: {ff['url']} | sha256 {ff['sha256']} | hasta {ff['fechas'][-1]}")
    p("")
    filas_var = []
    for vid, sec, lg, ct in VARIANTES:
        s = largo_corto(tablas[sec], lg, ct)
        pre = resumen(tramo(s, *PRE))
        post = resumen(tramo(s, POST_INI))
        ghs = resumen(tramo(s, GHS_INI))
        caida = 1 - post["media_mensual"] / pre["media_mensual"] if pre["media_mensual"] else None
        neto_pre = resumen([v - COSTO_MENSUAL for v in tramo(s, *PRE)])
        neto_post = resumen([v - COSTO_MENSUAL for v in tramo(s, POST_INI)])
        d = {"pre": pre, "post": post, "desde_2001": ghs, "caida_media": caida,
             "neto_1pct_pre": neto_pre, "neto_1pct_post": neto_post}
        if vid == "VW_deciles":
            for nombre, cols in (("capm", ["Mkt-RF"]), ("ff5", ["Mkt-RF", "SMB", "HML", "RMW", "CMA"])):
                d[f"alfa_{nombre}_pre"] = alfa(s, fac, cols, *PRE)
                d[f"alfa_{nombre}_post"] = alfa(s, fac, cols, POST_INI)
            mk = [(f, fac[f]["Mkt-RF"]) for f in fac]
            d["mercado_pre"] = resumen(tramo(mk, *PRE))
            d["mercado_post"] = resumen(tramo(mk, POST_INI))
        res["variantes"][vid] = d
        filas_var.append({"id": vid, "largo": lg, "corto": ct, "seccion": sec,
                          "media_pre": f"{pre['media_mensual']:.6f}", "t_nw_pre": f"{pre['t_nw6']:.3f}",
                          "media_post": f"{post['media_mensual']:.6f}", "t_nw_post": f"{post['t_nw6']:.3f}",
                          "caida": f"{caida:.4f}" if caida is not None else ""})
        p(f"== {vid} ({lg} - {ct}) ==")
        for et, r in (("1963-07..1996-06", pre), ("1996-07..fin", post), ("2001-01..fin", ghs),
                      ("neto 1% pre", neto_pre), ("neto 1% post", neto_post)):
            p(f"  {et:18s} n={r['n']:4d} media={r['media_mensual']*100:+.3f}%/mes (x12 {r['anual_x12']*100:+.2f}%)"
              f" t_iid={r['t_iid']:+.2f} t_NW6={r['t_nw6']:+.2f}")
        p(f"  caida de la media pre->post: {caida*100:.1f}%")
        for k in ("alfa_capm_pre", "alfa_capm_post", "alfa_ff5_pre", "alfa_ff5_post"):
            if k in d:
                a = d[k]
                p(f"  {k:15s} {a['alfa_mensual']*100:+.3f}%/mes t_NW6={a['t_nw']:+.2f} n={a['n']}")
        for k in ("mercado_pre", "mercado_post"):
            if k in d:
                p(f"  {k:15s} Mkt-RF {d[k]['media_mensual']*100:+.3f}%/mes t_NW6={d[k]['t_nw6']:+.2f}")
        p("")
    v = res["variantes"]["VW_deciles"]
    h1 = v["pre"]["media_mensual"] > 0 and v["pre"]["t_nw6"] >= 2.0
    h2 = (v["post"]["media_mensual"] <= 0.5 * v["pre"]["media_mensual"]) and v["post"]["t_nw6"] < 2.0
    estado = "No replicado" if not h1 else ("Replicado" if h2 else "Replicado con diferencias")
    res["veredicto"] = {"H1_sostenida": h1, "H2_sostenida": h2, "estado_A": estado}
    p(f"Veredicto A (principal VW deciles): H1 {'sostenida' if h1 else 'refutada'}; "
      f"H2 {'sostenida' if h2 else 'refutada'} -> {estado}")
    texto = "\n".join(out) + "\n"
    (AQUI / "R13-salida.txt").write_text(texto, encoding="utf-8")
    (AQUI / "R13-resultados.json").write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(filas_var[0]))
    w.writeheader()
    w.writerows(filas_var)
    (AQUI / "R13-variantes.csv").write_text(buf.getvalue(), encoding="utf-8")
    sys.stdout.write(texto)


if __name__ == "__main__":
    main()
