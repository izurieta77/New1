"""AC-12: doble ejecucion independiente (ciega) de R03.

Decaimiento post-publicacion McLean-Pontiff (2016) sobre SMB, HML, Mom, RMW y CMA (French),
crashes de momentum (H4) y "muerte del value" (H5).

Solo stdlib + herramientas.datos_historicos.french (lector de zip/CSV de French, leido desde
datos/<vintage>/ sin red). Toda la logica de tramos, regresion, bootstrap, H4 y H5 es propia.
Se corre sobre dos vintages: 202608 (descarga directa 2026-10-05; via B principal) y 202607
(mismos sha256 que declara el pre-registro de A). Las ventanas se recortan a 2026-07 (pre-registro).

Comando: python3 laboratorio/auditorias/AC-12-R03/AC12.py   (~1-2 min, sin red)
"""
from __future__ import annotations

import hashlib
import io
import json
import math
import random
import sys
import zipfile
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ))
from herramientas.datos_historicos import french  # noqa: E402

AQUI = Path(__file__).resolve().parent
SEMILLA = 20261005           # distinta de 20260925 (A)
PANEL_EXTRA = None           # solo conciliacion: panel de meses del bootstrap
REPS = 5000
BLOQUE = 12
FIN = (2026, 7)              # ultimo mes del pre-registro

ARCH = {"3F": "F-F_Research_Data_Factors", "MOM": "F-F_Momentum_Factor",
        "5F": "F-F_Research_Data_5_Factors_2x3"}

# Tramos (seccion 6 del pre-registro): (inicio IS, fin IS, fecha de publicacion = fin OOS)
TRAMOS = {
    "SMB": ((1936, 1), (1975, 12), (1981, 3)),
    "HML": ((1963, 7), (1990, 12), (1992, 6)),
    "Mom": ((1965, 1), (1989, 12), (1993, 3)),
    "RMW": ((1963, 7), (2013, 12), (2015, 4)),
    "CMA": ((1963, 7), (2013, 12), (2015, 4)),
}
CONTEOS = {"SMB": (480, 63, 544), "HML": (330, 18, 409), "Mom": (300, 39, 400),
           "RMW": (606, 16, 135), "CMA": (606, 16, 135)}
FF2015 = {"SMB": 0.29, "HML": 0.37, "RMW": 0.25, "CMA": 0.33}
DM15 = ["1932-08", "1932-07", "2001-01", "2009-04", "1939-09", "1933-04", "2009-03", "2002-11",
        "1938-06", "2009-08", "1931-06", "1933-05", "2001-11", "2001-10", "1974-01"]

LINEAS: list[str] = []


def p(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LINEAS.append(s)


def ym(d: date) -> tuple[int, int]:
    return (d.year, d.month)


def mes_str(k: tuple[int, int]) -> str:
    return f"{k[0]:04d}-{k[1]:02d}"


def mas_meses(k, n):
    t = k[0] * 12 + (k[1] - 1) + n
    return (t // 12, t % 12 + 1)


# ---------------------------------------------------------------- lector propio (control)
def lector_propio(zpath: Path, col: str) -> dict:
    """Parser minimo independiente: primera tabla mensual YYYYMM; devuelve {(y,m): decimal}."""
    with zipfile.ZipFile(zpath) as z:
        texto = z.read(z.namelist()[0]).decode("latin-1")
    cab = None
    out = {}
    empezado = False
    for ln in texto.splitlines():
        celdas = [c.strip() for c in ln.split(",")]
        if cab is None:
            if len(celdas) > 1 and celdas[0] == "" and col in celdas:
                cab = celdas
            continue
        if len(celdas[0]) == 6 and celdas[0].isdigit():
            empezado = True
            v = float(celdas[cab.index(col)])
            out[(int(celdas[0][:4]), int(celdas[0][4:]))] = None if v <= -99.99 else v / 100
        elif empezado:
            break
    return out


def cargar(vintage: str) -> dict:
    d = AQUI / "datos" / vintage
    info = {}
    series = {}
    for clave, nombre in ARCH.items():
        t = french(nombre, "mensual", dir_cache=d)
        zp = Path(t["ruta_cache"])
        sha = hashlib.sha256(zp.read_bytes()).hexdigest()
        info[clave] = {"archivo": zp.name, "sha256": sha, "version_crsp": t.get("version_crsp"),
                       "n": len(t["fechas"]), "primero": mes_str(ym(t["fechas"][0])),
                       "ultimo": mes_str(ym(t["fechas"][-1]))}
        fechas = [ym(f) for f in t["fechas"]]
        assert all(mas_meses(a, 1) == b for a, b in zip(fechas, fechas[1:])), "fechas no consecutivas"
        for c, vals in t["columnas"].items():
            s = {k: v for k, v in zip(fechas, vals) if v is not None and k <= FIN}
            series[(clave, c.strip())] = s
            # control con lector propio
            prop = lector_propio(zp, c.strip())
            assert all(abs(prop[k] - s[k]) < 1e-12 for k in s), f"lector difiere {clave} {c}"
    f = {
        "SMB": series[("3F", "SMB")], "HML": series[("3F", "HML")], "Mom": series[("MOM", "Mom")],
        "RMW": series[("5F", "RMW")], "CMA": series[("5F", "CMA")],
        "SMB5": series[("5F", "SMB")], "HML5": series[("5F", "HML")],
    }
    rf = series[("3F", "RF")]
    mkt = {k: v + rf[k] for k, v in series[("3F", "Mkt-RF")].items()}
    return {"f": f, "mkt": mkt, "mktrf": series[("3F", "Mkt-RF")], "info": info}


# ---------------------------------------------------------------- estadistica
def media(x):
    return sum(x) / len(x)


def desv(x):
    m = media(x)
    return math.sqrt(sum((v - m) ** 2 for v in x) / (len(x) - 1))


def t_iid(x):
    return media(x) / (desv(x) / math.sqrt(len(x)))


def ee_nw(x, L=6):
    n = len(x)
    m = media(x)
    e = [v - m for v in x]
    s = sum(v * v for v in e) / n
    for l in range(1, L + 1):
        g = sum(e[i] * e[i - l] for i in range(l, n)) / n
        s += 2 * (1 - l / (L + 1)) * g
    return math.sqrt(s / n)


def tramo(k, fac, pub=None):
    ini, fis, fpub = TRAMOS[fac]
    if pub is not None:
        fpub = pub
    if k < ini:
        return None
    if k <= fis:
        return 0
    if k <= fpub:
        return 1
    return 2


def inv3(a):
    (a11, a12, a13), (a21, a22, a23), (a31, a32, a33) = a
    det = a11 * (a22 * a33 - a23 * a32) - a12 * (a21 * a33 - a23 * a31) + a13 * (a21 * a32 - a22 * a31)
    c = [[a22 * a33 - a23 * a32, a13 * a32 - a12 * a33, a12 * a23 - a13 * a22],
         [a23 * a31 - a21 * a33, a11 * a33 - a13 * a31, a13 * a21 - a11 * a23],
         [a21 * a32 - a22 * a31, a12 * a31 - a11 * a32, a11 * a22 - a12 * a21]]
    return [[v / det for v in fila] for fila in c]


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def regresion_mp(panel):
    """panel: lista de (mes, factor, tramo, y). OLS y = a + b1*OOS + b2*POST; EE agrupado por mes."""
    X = [[1.0, 1.0 if t == 1 else 0.0, 1.0 if t == 2 else 0.0] for (_, _, t, _) in panel]
    Y = [y for (*_, y) in panel]
    N, K = len(Y), 3
    XtX = [[sum(r[i] * r[j] for r in X) for j in range(K)] for i in range(K)]
    XtY = [sum(r[i] * y for r, y in zip(X, Y)) for i in range(K)]
    Ai = inv3(XtX)
    b = [sum(Ai[i][j] * XtY[j] for j in range(K)) for i in range(K)]
    grupos = {}
    for r, y, (m, *_ ) in zip(X, Y, panel):
        e = y - sum(bi * xi for bi, xi in zip(b, r))
        g = grupos.setdefault(m, [0.0, 0.0, 0.0])
        for i in range(K):
            g[i] += r[i] * e
    G = len(grupos)
    S = [[sum(g[i] * g[j] for g in grupos.values()) for j in range(K)] for i in range(K)]
    V = mm(mm(Ai, S), Ai)
    c = G / (G - 1) * (N - 1) / (N - K)
    ee = [math.sqrt(V[i][i] * c) for i in range(K)]
    return b, ee, N, G


def pctl(v, q):
    v = sorted(v)
    h = (len(v) - 1) * q
    lo = math.floor(h)
    return v[lo] + (v[min(lo + 1, len(v) - 1)] - v[lo]) * (h - lo)


# ---------------------------------------------------------------- analisis
def decaimiento(D, facs, etiqueta, pubs=None, bootstrap=True):
    f = D["f"]
    pubs = pubs or {}
    p(f"\n--- Decaimiento McLean-Pontiff [{etiqueta}] factores={facs}")
    res = {"factores": {}}
    medias_is = {}
    panel = []
    for fac in facs:
        base = fac[:3] if fac in ("SMB5", "HML5") else fac
        s = f[fac]
        grupos = {0: [], 1: [], 2: []}
        for k in sorted(s):
            t = tramo(k, base, pubs.get(base))
            if t is not None:
                grupos[t].append(s[k])
        n = tuple(len(grupos[i]) for i in range(3))
        if not pubs and fac in CONTEOS:
            assert n == CONTEOS[fac], f"conteo {fac} {n} != {CONTEOS[fac]}"
        mis, moos, mpost = (media(grupos[i]) for i in range(3))
        medias_is[fac] = mis
        dif = mpost - mis
        tdif = dif / math.sqrt(ee_nw(grupos[2]) ** 2 + ee_nw(grupos[0]) ** 2)
        dec = 1 - mpost / mis
        res["factores"][fac] = {"n": n, "media_IS_pct": 100 * mis, "t_iid_IS": t_iid(grupos[0]),
                                "media_OOS_pct": 100 * moos, "media_post_pct": 100 * mpost,
                                "t_iid_post": t_iid(grupos[2]), "dif_pp": 100 * dif, "t_dif_nw": tdif,
                                "decaimiento": dec}
        p(f"{fac:5s} n(IS,OOS,post)={n}  media IS {100*mis:6.3f}% (t {t_iid(grupos[0]):5.2f})  "
          f"OOS {100*moos:6.3f}%  post {100*mpost:6.3f}% (t {t_iid(grupos[2]):5.2f})  "
          f"dif {100*dif:+6.3f} pp (t NW {tdif:5.2f})  decaimiento {dec:+.3f}")
        for k in sorted(s):
            t = tramo(k, base, pubs.get(base))
            if t is not None:
                panel.append((k, fac, t, s[k] / mis))
    b, ee, N, G = regresion_mp(panel)
    Dp = -b[2]
    prom = media([res["factores"][x]["decaimiento"] for x in facs])
    p(f"Regresion agrupada: a={b[0]:.4f}  b1={b[1]:+.4f} (ee {ee[1]:.4f})  b2={b[2]:+.4f} (ee {ee[2]:.4f})"
      f"  N={N} G={G}  =>  D=-b2={Dp:.4f}; t(b2)={b[2]/ee[2]:.2f}; promedio simple decaimientos={prom:.4f}")
    res.update({"a": b[0], "b1": b[1], "ee_b1": ee[1], "b2": b[2], "ee_b2": ee[2], "D": Dp,
                "N": N, "G": G, "promedio_simple": prom})
    if not bootstrap:
        return res
    # ------ bootstrap de bloques moviles de 12 meses calendario sobre el panel (re-estima media IS)
    meses = sorted({k for (k, *_ ) in panel}) if PANEL_EXTRA is None else list(PANEL_EXTRA)
    idx = {k: i for i, k in enumerate(meses)}
    M = len(meses)
    # por mes: lista de (j_factor, tramo, r)
    por_mes = [[] for _ in range(M)]
    for (k, fac, t, _y) in panel:
        por_mes[idx[k]].append((facs.index(fac), t, f[fac][k]))
    rng = random.Random(SEMILLA)
    nb = math.ceil(M / BLOQUE)
    Ds, decs = [], {x: [] for x in facs}
    excl = 0
    neg_is = {x: 0 for x in facs}
    J = len(facs)
    for _ in range(REPS):
        filas = []
        for _b in range(nb):
            s0 = rng.randrange(0, M - BLOQUE + 1)
            filas.extend(range(s0, s0 + BLOQUE))
        filas = filas[:M]
        sm = [[0.0, 0.0, 0.0] for _ in range(J)]
        cn = [[0, 0, 0] for _ in range(J)]
        for i in filas:
            for (j, t, r) in por_mes[i]:
                sm[j][t] += r
                cn[j][t] += 1
        ok = True
        mis = []
        for j in range(J):
            if cn[j][0] == 0 or cn[j][2] == 0:
                ok = False
                mis.append(None)
                continue
            m0 = sm[j][0] / cn[j][0]
            mis.append(m0)
            if m0 <= 0:
                neg_is[facs[j]] += 1
            decs[facs[j]].append(1 - (sm[j][2] / cn[j][2]) / m0)
        if not ok:
            excl += 1
            continue
        ytot = sum(sm[j][2] / mis[j] for j in range(J))
        npost = sum(cn[j][2] for j in range(J))
        Ds.append(1 - ytot / npost)
    lo, hi = pctl(Ds, 0.025), pctl(Ds, 0.975)
    p(f"Bootstrap bloques {BLOQUE}m, {REPS} reps, semilla {SEMILLA}, meses del panel {M} "
      f"({mes_str(meses[0])}..{mes_str(meses[-1])}); excluidas {excl}")
    p(f"  D agrupado = {Dp:.4f}  IC95% [{lo:.4f}, {hi:.4f}]  contiene 0: {lo <= 0 <= hi}  "
      f"contiene 0.58: {lo <= 0.58 <= hi}")
    res.update({"IC_D": [lo, hi], "excluidas": excl})
    for x in facs:
        l2, h2 = pctl(decs[x], 0.025), pctl(decs[x], 0.975)
        frac = neg_is[x] / REPS
        nota = "NO INFORMATIVO" if frac > 0.025 else ""
        p(f"  {x:5s} decaimiento {res['factores'][x]['decaimiento']:+.3f} IC95% [{l2:+.3f}, {h2:+.3f}]"
          f"  P(media IS*<=0)={frac:.4f} {nota}")
        res["factores"][x]["IC"] = [l2, h2]
        res["factores"][x]["frac_IS_no_pos"] = frac
    return res


def h1(D):
    f = D["f"]
    p("\n--- H1 / Condicion A")
    vent = {"SMB": ((1936, 1), (1975, 12)), "HML": ((1963, 7), (1990, 12)),
            "Mom": ((1965, 1), (1989, 12)), "RMW": ((1963, 7), (2013, 12)), "CMA": ((1963, 7), (2013, 12))}
    out = {}
    for fac, (a, b) in vent.items():
        x = [v for k, v in sorted(f[fac].items()) if a <= k <= b]
        out[fac] = {"media_pct": 100 * media(x), "t_iid": t_iid(x), "n": len(x)}
        p(f"{fac}: {mes_str(a)}..{mes_str(b)} n={len(x)} media {100*media(x):.3f}% t iid {t_iid(x):.2f}")
    mag = {}
    for fac, objetivo in FF2015.items():
        for var in ([fac, fac + "5"] if fac in ("SMB", "HML") else [fac]):
            x = [v for k, v in sorted(f[var].items()) if (1963, 7) <= k <= (2013, 12)]
            m = 100 * media(x)
            mag[var] = {"media_pct": m, "t_iid": t_iid(x), "dif_pp": m - objetivo,
                        "dentro_005": abs(m - objetivo) <= 0.05}
            p(f"H1-magnitud {var}: 1963-07..2013-12 media {m:.3f}% (t {t_iid(x):.2f}) vs FF2015 {objetivo} "
              f"dif {m-objetivo:+.3f} -> {'OK' if abs(m-objetivo) <= 0.05 else 'FUERA'}")
    falla_t = [x for x in ("HML", "Mom", "RMW", "CMA") if not (out[x]["media_pct"] > 0 and out[x]["t_iid"] >= 2)]
    mag_ok_5f = sum(mag[x]["dentro_005"] for x in ("SMB5", "HML5", "RMW", "CMA"))
    mag_ok_3f = sum(mag[x]["dentro_005"] for x in ("SMB", "HML", "RMW", "CMA"))
    p(f"Condicion A: fallan t>=2: {falla_t}; magnitud dentro de +-0.05: {mag_ok_5f}/4 (SMB/HML 5F), "
      f"{mag_ok_3f}/4 (SMB/HML 3F)")
    return {"ventanas": out, "magnitud": mag, "falla_t": falla_t, "mag_ok_5f": mag_ok_5f, "mag_ok_3f": mag_ok_3f}


def h4(D):
    f, mkt = D["f"]["Mom"], D["mkt"]
    p("\n--- H4 crashes de momentum")

    def acum24(k):
        prev = [mas_meses(k, -i) for i in range(1, 25)]
        if not all(x in mkt for x in prev):
            return None
        v = 1.0
        for x in prev:
            v *= 1 + mkt[x]
        return v - 1

    res = {}
    for nombre, (a, b) in {"1927-01..2026-07": ((1927, 1), FIN), "DM 1927-01..2013-03": ((1927, 1), (2013, 3))}.items():
        meses = [k for k in f if a <= k <= b]
        peor = sorted(meses, key=lambda k: f[k])[:15]
        n_oso = n_sube = n_sube_ex = 0
        p(f"[{nombre}] 15 peores meses de Mom:")
        for k in peor:
            a24 = acum24(k)
            oso = a24 is not None and a24 < 0
            n_oso += oso
            n_sube += mkt[k] > 0
            n_sube_ex += D["mktrf"][k] > 0
            p(f"  {mes_str(k)} Mom {100*f[k]:7.2f}%  mkt24 {('%7.2f%%' % (100*a24)) if a24 is not None else '   n/d'}"
              f"  mkt mes {100*mkt[k]:6.2f}%  oso={oso}")
        coinc = sum(mes_str(k) in DM15 for k in peor)
        p(f"  oso (mkt24<0): {n_oso}/15; mercado del mes>0 (Mkt total): {n_sube}/15 (Mkt-RF: {n_sube_ex}/15);"
          f" coincidencias con tabla 2 de DM: {coinc}/15")
        res[nombre] = {"peores": [mes_str(k) for k in peor], "oso": n_oso, "mkt_mes_pos": n_sube,
                       "mktrf_mes_pos": n_sube_ex, "coinc_DM": coinc}
    oso = [f[k] for k in sorted(f) if k <= FIN and (acum24(k) or 0) < 0 and acum24(k) is not None]
    norm = [f[k] for k in sorted(f) if k <= FIN and not (acum24(k) is not None and acum24(k) < 0)]
    p(f"Media Mom oso {100*media(oso):.3f}% (n {len(oso)}) vs normal {100*media(norm):.3f}% (n {len(norm)})")
    tot = res["1927-01..2026-07"]
    dm = res["DM 1927-01..2013-03"]
    conf = tot["oso"] >= 10 and tot["mkt_mes_pos"] >= 12 and dm["coinc_DM"] >= 8 and media(oso) < media(norm)
    p(f"H4: {'confirmada' if conf else 'no confirmada'}")
    res.update({"media_oso_pct": 100 * media(oso), "media_normal_pct": 100 * media(norm), "confirmada": conf})
    return res


def h5(D, col="HML"):
    s = D["f"][col]
    meses = sorted(s)
    idx, v, pico, kpico = {}, 1.0, 1.0, mas_meses(meses[0], -1)
    peor = (0.0, None, None)
    for k in meses:
        v *= 1 + s[k]
        idx[k] = v
        if v > pico:
            pico, kpico = v, k
        if (2007, 1) <= k <= (2020, 12):
            dd = v / pico - 1
            if dd < peor[0]:
                peor = (dd, kpico, k)
    dd, kp, kv = peor
    ult = meses[-1]
    rec = idx[ult] / idx[kv] - 1
    pico_val = idx[kp]
    dist = idx[ult] / pico_val - 1
    m0720 = media([s[k] for k in meses if (2007, 1) <= k <= (2020, 12)])
    nmes = (kv[0] - kp[0]) * 12 + kv[1] - kp[1]
    conf = dd <= -0.50 and m0720 < 0 and rec > 0 and dist < 0
    p(f"\n--- H5 muerte del value ({col}): pico {mes_str(kp)} -> valle {mes_str(kv)} ({nmes} meses) DD {100*dd:.1f}%;"
      f" media 2007-2020 {100*m0720:.3f}%/mes; valle->{mes_str(ult)} {100*rec:+.1f}%; bajo el pico {100*dist:+.1f}%"
      f" -> {'confirmada' if conf else 'no confirmada'}")
    return {"pico": mes_str(kp), "valle": mes_str(kv), "dd_pct": 100 * dd, "media_0720_pct": 100 * m0720,
            "recuperacion_pct": 100 * rec, "dist_pico_pct": 100 * dist, "confirmada": conf}


def estado(A, dec):
    lo, hi = dec["IC_D"]
    n_falla = len(A["falla_t"]) + (1 if A["mag_ok_5f"] < 3 else 0)
    todos_bajan = all(v["media_post_pct"] < v["media_IS_pct"] for v in dec["factores"].values())
    if dec["D"] <= 0 or n_falla >= 2:
        return "No replicado"
    if n_falla == 0 and lo > 0 and lo <= 0.58 <= hi and todos_bajan:
        return "Replicado"
    return "Replicado con diferencias"


def main():
    resultados = {}
    for vint in ("202608", "202607"):
        p("=" * 100)
        p(f"VINTAGE {vint}")
        D = cargar(vint)
        for k, v in D["info"].items():
            p(f"  {k}: {v['archivo']} {v['version_crsp']} sha256 {v['sha256']} n={v['n']} {v['primero']}..{v['ultimo']}"
              f" (se usa hasta {mes_str(FIN)})")
        r = {"datos": D["info"]}
        r["H1"] = h1(D)
        facs = ["SMB", "HML", "Mom", "RMW", "CMA"]
        r["principal"] = decaimiento(D, facs, "principal")
        r["estado"] = estado(r["H1"], r["principal"])
        p(f"ESTADO segun la regla del pre-registro: {r['estado']}")
        r["H4"] = h4(D)
        r["H5"] = h5(D, "HML")
        r["H5_5F"] = h5(D, "HML5")
        if vint == "202608":
            p("\n=== Sensibilidades (vintage 202608)")
            r["sens_5F"] = decaimiento(D, ["SMB5", "HML5", "Mom", "RMW", "CMA"], "SMB/HML del archivo 5F",
                                       bootstrap=True)
            r["sens_alt"] = decaimiento(D, facs, "fechas alternativas Banz 1979-06 / FF2015 2014-10",
                                        pubs={"SMB": (1979, 6), "RMW": (2014, 10), "CMA": (2014, 10)},
                                        bootstrap=False)
            fuertes = [x for x in facs if r["principal"]["factores"][x]["t_iid_IS"] >= 2]
            r["sens_t2"] = decaimiento(D, fuertes, "solo factores con t IS >= 2", bootstrap=True)
        resultados[vint] = r
    (AQUI / "resultados.json").write_text(json.dumps(resultados, indent=1, ensure_ascii=False, default=str))
    (AQUI / "salida.txt").write_text("\n".join(LINEAS) + "\n")


def conciliacion():
    """Agregado DESPUES de leer A (2026-10-05). No cambia ninguna linea anterior de la salida."""
    global SEMILLA
    import contextlib
    p("\n" + "=" * 100)
    p("[CONCILIACION] agregado despues de leer R03-salida.txt; las lineas anteriores son la salida ciega")
    D = cargar("202607")
    f = D["f"]
    p("t NW(6) de la media POST (A reporta t NW; la salida ciega imprimio t iid):")
    for fac in ["SMB", "HML", "Mom", "RMW", "CMA"]:
        x = [v for k, v in sorted(f[fac].items()) if tramo(k, fac) == 2]
        p(f"  {fac}: t NW post {media(x)/ee_nw(x):.2f}")
    # sensibilidad del IC del D agrupado a la semilla y al panel del bootstrap
    facs = ["SMB", "HML", "Mom", "RMW", "CMA"]
    base_sem = SEMILLA
    buf = []
    for sem in (20260925, 1, 2, 3, 4, 5):
        SEMILLA = sem
        with contextlib.redirect_stdout(io.StringIO()):
            n0 = len(LINEAS)
            r = decaimiento(D, facs, f"semilla {sem}")
            del LINEAS[n0:]
        buf.append((sem, r["IC_D"]))
    SEMILLA = base_sem
    for sem, (lo, hi) in buf:
        p(f"  panel 1936-01..2026-07, semilla {sem}: IC95 D [{100*lo:.1f}%, {100*hi:.1f}%]")
    # panel de A: 1201 meses 1926-07..2026-07 (meses sin tramo entran como filas vacias)
    meses_todos = sorted(D["mkt"])
    global PANEL_EXTRA
    PANEL_EXTRA = meses_todos
    with contextlib.redirect_stdout(io.StringIO()):
        n0 = len(LINEAS)
        r = decaimiento(D, facs, "panel 1201")
        del LINEAS[n0:]
    PANEL_EXTRA = None
    p(f"  panel 1926-07..2026-07 (1201 meses, como A), semilla {SEMILLA}: IC95 D "
      f"[{100*r['IC_D'][0]:.1f}%, {100*r['IC_D'][1]:.1f}%]; por factor: "
      + "; ".join(f"{x} [{100*v['IC'][0]:.1f}, {100*v['IC'][1]:.1f}] P(IS<=0)={v['frac_IS_no_pos']:.4f}"
                  for x, v in r["factores"].items()))
    mk, mo = D["mkt"], f["Mom"]
    norm = []
    for k in sorted(mo):
        prev = [mas_meses(k, -i) for i in range(1, 25)]
        if all(x in mk for x in prev):
            v = 1.0
            for x in prev:
                v *= 1 + mk[x]
            if v - 1 >= 0:
                norm.append(mo[k])
    p(f"  H4(d) media Mom 'normal' solo con 24m completos (como A, 1928-07..2026-07): {100*media(norm):.3f}% n={len(norm)}")


if __name__ == "__main__":
    main()
    conciliacion()
    (AQUI / "salida.txt").write_text("\n".join(LINEAS) + "\n")
