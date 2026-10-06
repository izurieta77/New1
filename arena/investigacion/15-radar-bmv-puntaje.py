"""Puntaje y niveles del radar BMV (15-radar-bmv-2026-10-05.md). Solo biblioteca estandar.

Uso:
    python3 arena/investigacion/15-radar-bmv-puntaje.py          # lee los dos CSV de entrada y escribe 15-radar-bmv-2026-10-05-puntaje.csv

Entradas:
  * 15-radar-bmv-2026-10-05-datos.csv     (15-radar-bmv-datos.py: Yahoo chart v8, corte 5-oct-2026)
  * 15-radar-bmv-supuestos.csv            (capturado a mano de las fichas empresas/<T>/ficha.md ya verificadas)
  * historia de 10 anios (Yahoo chart v8, cierre ajustado) para las tasas base y la simulacion.

Metodo (resumen; el detalle y los supuestos estan en el .md):
  * Objetivo (escenario favorable) = reversion COMPLETA del multiplo actual (P/U o P/VL de la ficha, movido con el
    precio de hoy) a su media historica de la ficha, mas dividendos con fecha dentro del plazo. Sin multiplo verificable
    o con multiplo ya sobre su media: sin objetivo (None).
  * Plazo 7 meses = 147 sesiones. Stop = 1.25 * sigma_diaria60 * sqrt(63), acotado a [8%, 25%].
  * Tasa base: ventanas de 10 anios de la emisora y del grupo (todas las .MX acciones), con inicio cada 3 sesiones:
    toca +20/+30% en 147 sesiones, +40% en 63, +50% en 105. Simulacion objetivo/stop/tiempo con cierres:
    objetivo o stop al primer cierre que los cruza; si ninguno, sale a las 147 sesiones. Valor esperado = suma de resultados
    ponderados - costo de ida y vuelta (0.58% comision con IVA + spread supuesto).
  * Sesgos: la muestra son emisoras que SIGUEN cotizando (supervivencia: sesga hacia arriba); cierre ajustado de Yahoo (puede
    omitir dividendos en .MX: sesga hacia abajo); stop por cierre sin deslizamiento (optimista); ventanas traslapadas (no
    independientes: no hay intervalos de confianza).
"""
from __future__ import annotations

import csv
import math
import statistics
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
from herramientas.datos import yahoo_serie  # noqa: E402

DIR = RAIZ / "arena/investigacion"
CAP = 20000.0
RIESGO = 0.03
TOPE_POS = 0.30
H7, H5, H3 = 147, 105, 63
COM = 0.0058  # 0.25% + IVA por lado


def leer(p):
    with open(p, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def hist(t):
    for k in range(3):
        try:
            return [c for _, c in yahoo_serie(t, "10y", "1d", cache_horas=12)]
        except Exception:  # noqa: BLE001
            time.sleep(2)
    return []


def toca(px, h, x, paso=3):
    """Fraccion de ventanas con maximo >= +x dentro de h sesiones."""
    n = k = 0
    for i in range(0, len(px) - h, paso):
        n += 1
        if max(px[i + 1:i + h + 1]) / px[i] - 1 >= x:
            k += 1
    return (k / n if n else None), n


def sim(px, h, T, S, paso=3):
    n = ph = ps = 0
    suma = 0.0
    for i in range(0, len(px) - h, paso):
        n += 1
        out = None
        for j in range(1, h + 1):
            r = px[i + j] / px[i] - 1
            if r >= T:
                out = T
                ph += 1
                break
            if r <= -S:
                out = -S
                ps += 1
                break
        if out is None:
            out = px[i + h] / px[i] - 1
        suma += out
    if not n:
        return None
    return {"pT": ph / n, "pS": ps / n, "pExp": 1 - (ph + ps) / n, "ev_bruto": suma / n, "n": n}


def pts_ratio(r):
    return 0 if r < 2 else 10 if r < 3 else 18 if r < 5 else 25


def pts_asim(a):
    return 15 if a >= 3 else 10 if a >= 2 else 6 if a >= 1.5 else 0


def main():
    datos = {r["ticker"]: r for r in leer(DIR / "15-radar-bmv-2026-10-05-datos.csv") if r["estado"] == "ok"}
    sup = {r["ticker"]: r for r in leer(DIR / "15-radar-bmv-supuestos.csv")}
    hs = {}
    for t in datos:
        hs[t] = hist(t)
        time.sleep(0.5)
    # tasas base del grupo (solo acciones .MX, no FIBRA ni ETF)
    grupo = [t for t in datos if sup[t]["clase"] in ("IPC", "otra") and len(hs[t]) > 1800]
    g = {}
    for nombre, h, x in (("p20_7m", H7, 0.20), ("p30_7m", H7, 0.30), ("p40_3m", H3, 0.40), ("p50_5m", H5, 0.50)):
        k = n = 0
        for t in grupo:
            p, m = toca(hs[t], h, x)
            if p is not None:
                k += p * m
                n += m
        g[nombre] = k / n
    filas = []
    for t, d in datos.items():
        s = sup[t]
        px = hs[t]
        precio = float(d["precio"])
        p24 = float(d["precio_24sep"]) if d["precio_24sep"] else precio
        vol = float(d["vol60"])
        liq = float(d["liq30_mxn_mm"])
        cs = float(d["spread_cs_pct"]) / 100
        base_sp = 0.001 if t == "NAFTRAC.MX" else 0.003 if liq >= 100 else 0.006 if liq >= 20 else 0.010
        spread = max(base_sp, cs)
        costo = COM + spread
        # objetivo
        T = None
        if s["mult_tipo"] != "none" and s["mult_ficha"]:
            actual = float(s["mult_ficha"]) * precio / p24
            rev = float(s["mult_media5"]) / actual - 1
            if rev > 0:
                T = rev + (float(s["div_ps_7m"] or 0) / precio)
        S = min(0.25, max(0.08, 1.25 * (vol / math.sqrt(252)) * math.sqrt(63)))
        Tsim = T if T else 0.25
        sm = sim(px, H7, Tsim, S) if len(px) > H7 + 200 else None
        r20, n20 = toca(px, H7, 0.20) if len(px) > H7 + 200 else (None, 0)
        r30, _ = toca(px, H7, 0.30) if len(px) > H7 + 200 else (None, 0)
        r40, _ = toca(px, H3, 0.40) if len(px) > H3 + 200 else (None, 0)
        r50, _ = toca(px, H5, 0.50) if len(px) > H5 + 200 else (None, 0)
        ev_net = (sm["ev_bruto"] - costo) if sm else None
        ratio = ev_net / costo if ev_net is not None else 0
        asim = (T / S) if T else (Tsim / S)
        # puertas
        pos_val = min(TOPE_POS * CAP, RIESGO * CAP / S)
        tit = int(pos_val // precio)
        p3 = precio <= TOPE_POS * CAP
        p4 = T is not None and ev_net is not None and ev_net >= 2 * costo and ev_net > 0
        p1 = s["p1"] == "S"
        # puntaje
        edge_pts = min(10, pts_ratio(ratio)) if p4 else 0  # tope: edge no validado fuera de muestra
        ev_pts = 5
        cat_pts = 10 if s["reporte_conf"] == "S" else 2
        asim_pts = pts_asim(asim) if T else 0
        liq_pts = 3 if liq >= 20 else 0
        cos_pts = 5 if costo <= 0.007 else 3 if costo <= 0.012 else 0
        rho = max(float(d["rho60_spy_mxn"] or 0), float(d["rho120_5d_spy_mxn"] or 0), 0)
        cor_pts = 10 if rho < 0.3 else 6 if rho < 0.6 else 2 if rho < 0.8 else 0
        geo_pts = {"bajo": 10, "medio": 5, "alto": 0}[s["geo"]]
        n_an = s["n_analistas"]
        own_pts = 5 if (p1 or (n_an.isdigit() and int(n_an) <= 3)) else 2
        crowd = 0
        if float(d["dist_sma200"]) > 0.15 or float(d["ret_12m"] or 0) > 0.40:
            crowd = -8
        if t in ("GMEXICOB.MX", "GFNORTEO.MX", "AMXB.MX", "FEMSAUBD.MX", "WALMEX.MX"):
            crowd = max(-10, min(0, crowd - 3))
        total = edge_pts + ev_pts + cat_pts + asim_pts + liq_pts + cos_pts + cor_pts + geo_pts + own_pts + crowd
        puertas = p1 and p3 and p4 and (T is not None)
        if puertas and T >= 0.20 and asim >= 2 and total >= 55:  # Oro: ver adenda del pre-registro
            nivel = "Oro"
        else:
            nivel = "Sin nivel"
        falla = []
        if not p1:
            falla.append("P1")
        if not p3:
            falla.append("P3")
        if not p4:
            falla.append("P4")
        if T is None:
            falla.append("objetivo<20%")
        elif T < 0.20:
            falla.append("objetivo<20%")
        if T and asim < 2:
            falla.append("asimetria<2:1")
        fila = {
            "ticker": t, "clase": s["clase"], "fecha": d["fecha"], "precio": precio, "dist_sma200": d["dist_sma200"],
            "sma200": d["sma200"], "ret_3m": d["ret_3m"], "ret_12m": d["ret_12m"], "vol60": vol, "liq30_mxn_mm": liq,
            "spread_cs_pct": d["spread_cs_pct"], "spread_supuesto_pct": round(100 * spread, 2),
            "costo_ida_vuelta_pct": round(100 * costo, 2), "objetivo_pct": None if T is None else round(100 * T, 1),
            "plazo_meses": 7, "stop_pct": round(100 * S, 1), "asimetria": round(asim, 2) if T else None,
            "p20_7m": None if r20 is None else round(r20, 3), "p30_7m": None if r30 is None else round(r30, 3),
            "p40_3m": None if r40 is None else round(r40, 3), "p50_5m": None if r50 is None else round(r50, 3),
            "n_ventanas": n20,
            "sim_pObjetivo": None if not sm else round(sm["pT"], 3), "sim_pStop": None if not sm else round(sm["pS"], 3),
            "sim_pTiempo": None if not sm else round(sm["pExp"], 3),
            "ev_bruto_pct": None if not sm else round(100 * sm["ev_bruto"], 2),
            "ev_neto_pct": None if ev_net is None else round(100 * ev_net, 2),
            "objetivo_de_sim_pct": round(100 * Tsim, 1),
            "titulos_20k": tit, "pos_mxn_20k": round(tit * precio), "perdida_stop_mxn_20k": round(tit * precio * S),
            "titulos_10k": int(min(0.30 * 10000, 0.03 * 10000 / S) // precio),
            "P1": "S" if p1 else "N", "P2": "C", "P3": "S" if p3 else "N", "P4": "S" if p4 else "N", "P5": "S", "P6": "S",
            "pts_edge": edge_pts, "pts_evidencia": ev_pts, "pts_catalizador": cat_pts, "pts_asimetria": asim_pts,
            "pts_liquidez": liq_pts, "pts_costos": cos_pts, "pts_correlacion": cor_pts, "pts_riesgo_reg": geo_pts,
            "pts_ventaja": own_pts, "pen_crowding": crowd, "puntaje": total, "rho_usada": round(rho, 2),
            "nivel": nivel, "falla": ";".join(falla),
        }
        filas.append(fila)
    filas.sort(key=lambda r: (-r["puntaje"], r["ticker"]))
    with open(DIR / "15-radar-bmv-2026-10-05-puntaje.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)
    print("grupo (n=%d emisoras):" % len(grupo), {k: round(v, 3) for k, v in g.items()})
    with open(DIR / "15-radar-bmv-2026-10-05-grupo.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["metrica", "valor", "emisoras"])
        for k, v in g.items():
            w.writerow([k, round(v, 4), len(grupo)])
    for r in filas:
        print(f"{r['ticker']:14}{r['puntaje']:4} {r['nivel']:9} T={r['objetivo_pct']} S={r['stop_pct']} as={r['asimetria']} "
              f"p20={r['p20_7m']} evN={r['ev_neto_pct']} cost={r['costo_ida_vuelta_pct']} falla={r['falla']}")


if __name__ == "__main__":
    main()
