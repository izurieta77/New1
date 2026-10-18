#!/usr/bin/env python3
"""AC-21-R12, ejecución B (independiente). Código desde cero, solo stdlib.

Uso: python3 -I b.py  (lee datos/ junto a este archivo)

Fuentes (FRED fredgraph CSV, descargadas 2026-10-18 01:13 UTC; sha256 en datos/SHA256SUMS):
  NASDAQ100 (diario desde 1986-01-02), VIXCLS (desde 1990-01-02), DTB3, VXOCLS (1986-2021).
  Prueba secundaria: SPX_History_cboe.csv (CBOE, copia de AC-17-R11/datos).

Convenciones B:
  - Panel = días con NDX y VIX (se descartan y reportan los que tienen solo uno).
  - SMA200 = media de los últimos 200 cierres del panel, incluido t.
  - Señal al cierre t -> posición ejecutada al cierre t+1 -> gana el rendimiento de t+2.
  - 3x(d) = 3*r_NDX(d) - 2*rf(d) - 0.0095/252 ; rf(d) = DTB3 del día hábil previo /100/252
    (DTB3 rellenado hacia adelante si falta).
  - Costo 0.10% por lado, cargado el día en que cambia la posición ejecutada.
  - Fuera del mercado gana rf(d).
  - Estado inicial: fuera; se entra cuando se cumple la regla de entrada.
  - Primer rendimiento evaluado: 2 días después de la primera SMA200.
"""
import csv, math, os, sys, json

AQUI = os.path.dirname(os.path.abspath(__file__))
DAT = os.path.join(AQUI, "datos")
FIN = "2026-10-16"
COSTO = 0.001
GASTO = 0.0095


def leer_fred(nombre):
    out = {}
    with open(os.path.join(DAT, nombre + ".csv"), newline="") as f:
        r = csv.reader(f)
        next(r)
        for fila in r:
            if len(fila) < 2:
                continue
            v = fila[1].strip()
            if v in ("", "."):
                continue
            out[fila[0]] = float(v)
    return out


def leer_cboe_spx():
    out = {}
    with open(os.path.join(DAT, "SPX_History_cboe.csv"), newline="") as f:
        r = csv.reader(f)
        next(r)
        for fila in r:
            m, d, y = fila[0].split("/")
            out["%s-%s-%s" % (y, m, d)] = float(fila[1])
    return out


def panel(precio, vol, desde, hasta):
    fp = {d for d in precio if desde <= d <= hasta}
    fv = {d for d in vol if desde <= d <= hasta}
    comunes = sorted(fp & fv)
    solo_p = sorted(fp - fv)
    solo_v = sorted(fv - fp)
    return comunes, solo_p, solo_v


def rf_diaria(fechas, dtb3):
    """rf(d) usa el último DTB3 publicado ANTES de d (conocido al cierre d-1)."""
    claves = sorted(dtb3)
    j = 0
    ult = None
    out = []
    for d in fechas:
        while j < len(claves) and claves[j] < d:
            ult = dtb3[claves[j]]
            j += 1
        out.append((ult if ult is not None else 0.0) / 100.0 / 252.0)
    return out


def senales(px, vix, regla, umbral=25.0, banda=0.03, n=200, sostener=1):
    """Devuelve lista de estados (1 invertido / 0 fuera) decididos al cierre t; None antes de SMA."""
    est = [None] * len(px)
    s = 0.0
    estado = 0
    for t in range(len(px)):
        s += px[t]
        if t >= n:
            s -= px[t - n]
        if t < n - 1:
            continue
        sma = s / n
        p = px[t]
        if regla == "sma":
            salir = p < sma * (1 - banda)
            entrar = p > sma * (1 + banda)
        else:
            vix_alto = all(vix[t - k] >= umbral for k in range(sostener)) if t - sostener + 1 >= 0 else False
            salir = p < sma * (1 - banda) or vix_alto
            entrar = p > sma * (1 + banda) and vix[t] < umbral
        if estado == 1 and salir:
            estado = 0
        elif estado == 0 and entrar:
            estado = 1
        est[t] = estado
    return est


def simular(fechas, px, est, rf, palanca=3.0, gasto=GASTO):
    """Rendimientos diarios de la estrategia desde el día i0 = primer señal + 2."""
    t0 = next(i for i, e in enumerate(est) if e is not None)
    i0 = t0 + 2
    rets, rfs, pos_d, fd = [], [], [], []
    salidas = entradas = 0
    for d in range(i0, len(px)):
        r_idx = px[d] / px[d - 1] - 1.0
        r3 = palanca * r_idx - (palanca - 1.0) * rf[d] - gasto / 252.0
        pos = est[d - 2]          # ejecutada al cierre d-1 (señal de d-2)
        nueva = est[d - 1]        # se ejecuta al cierre d
        r = r3 if pos == 1 else rf[d]
        if nueva != pos:
            r -= COSTO
            if nueva == 0:
                salidas += 1
            else:
                entradas += 1
        rets.append(r); rfs.append(rf[d]); pos_d.append(pos); fd.append(fechas[d])
    return {"fechas": fd, "r": rets, "rf": rfs, "pos": pos_d}


def bh(fechas, px, est, rf, palanca=3.0, gasto=GASTO):
    t0 = next(i for i, e in enumerate(est) if e is not None)
    i0 = t0 + 2
    rets, rfs, fd = [], [], []
    for d in range(i0, len(px)):
        r_idx = px[d] / px[d - 1] - 1.0
        rets.append(palanca * r_idx - (palanca - 1.0) * rf[d] - gasto / 252.0)
        rfs.append(rf[d]); fd.append(fechas[d])
    # compra al cierre i0-1: un costo de entrada
    rets[0] -= COSTO
    return {"fechas": fd, "r": rets, "rf": rfs, "pos": [1] * len(rets)}


def metricas(res, desde="0000", hasta="9999"):
    idx = [i for i, d in enumerate(res["fechas"]) if desde <= d <= hasta]
    if len(idx) < 3:
        return None
    r = [res["r"][i] for i in idx]
    rf = [res["rf"][i] for i in idx]
    pos = [res["pos"][i] for i in idx]
    eq = 1.0; pico = 1.0; mdd = 0.0
    for x in r:
        eq *= (1 + x)
        pico = max(pico, eq)
        mdd = min(mdd, eq / pico - 1)
    d0, d1 = res["fechas"][idx[0]], res["fechas"][idx[-1]]
    # años por conteo de días hábiles (252)
    anios = len(r) / 252.0
    cagr = eq ** (1 / anios) - 1 if eq > 0 else -1.0
    ex = [a - b for a, b in zip(r, rf)]
    m = sum(ex) / len(ex)
    sd = math.sqrt(sum((x - m) ** 2 for x in ex) / (len(ex) - 1))
    sharpe = m / sd * math.sqrt(252) if sd > 0 else float("nan")
    # salidas = transiciones 1->0 de la posición dentro del tramo
    sal = sum(1 for k in range(1, len(pos)) if pos[k - 1] == 1 and pos[k] == 0)
    inv = sum(pos) / len(pos)
    return {"desde": d0, "hasta": d1, "dias": len(r), "cagr": cagr, "sharpe": sharpe,
            "mdd": mdd, "salidas": sal, "invertido": inv}


def tabla(titulo, resultados, tramos, out):
    out.append("")
    out.append("== %s ==" % titulo)
    for nom_t, (a, b) in tramos:
        filas = [(k, metricas(v, a, b)) for k, v in resultados]
        m0 = filas[0][1]
        out.append("-- %s: %s a %s (%d días) --" % (nom_t, m0["desde"], m0["hasta"], m0["dias"]))
        out.append("%-26s %8s %7s %8s %8s %9s" % ("variante", "CAGR", "Sharpe", "MDD", "salidas", "%invert"))
        for k, m in filas:
            out.append("%-26s %7.2f%% %7.3f %7.1f%% %8d %8.1f%%" % (
                k, 100 * m["cagr"], m["sharpe"], 100 * m["mdd"], m["salidas"], 100 * m["invertido"]))
    return out


def correr(precio, vol, dtb3, desde, hasta, etiqueta, out, tramos, variantes):
    fechas, solo_p, solo_v = panel(precio, vol, desde, hasta)
    out.append("")
    out.append("[%s] panel %s a %s: %d días comunes; descartados %d con precio sin vol, %d con vol sin precio" % (
        etiqueta, fechas[0], fechas[-1], len(fechas), len(solo_p), len(solo_v)))
    if solo_p:
        out.append("   precio sin vol: " + ", ".join(solo_p[:15]) + (" ..." if len(solo_p) > 15 else ""))
    if solo_v:
        out.append("   vol sin precio: " + ", ".join(solo_v[:15]) + (" ..." if len(solo_v) > 15 else ""))
    px = [precio[d] for d in fechas]
    vx = [vol[d] for d in fechas]
    rf = rf_diaria(fechas, dtb3)
    res = []
    for nom, kw in variantes:
        est = senales(px, vx, **kw)
        res.append((nom, simular(fechas, px, est, rf)))
    est0 = senales(px, vx, regla="sma")
    res.append(("B&H 3x", bh(fechas, px, est0, rf)))
    tabla(etiqueta, res, tramos, out)
    return res


VARIANTES = [
    ("V0 vigente (VIX>=25)", dict(regla="vix", umbral=25.0)),
    ("V1 solo SMA200 +-3%", dict(regla="sma")),
    ("V2 VIX>=25 2 cierres", dict(regla="vix", umbral=25.0, sostener=2)),
    ("V3 VIX>=30", dict(regla="vix", umbral=30.0)),
]


def veredicto(res, a, b, out, etiqueta):
    m0 = metricas(dict(res)["V0 vigente (VIX>=25)"], a, b)
    m1 = metricas(dict(res)["V1 solo SMA200 +-3%"], a, b)
    h1_sharpe = m1["sharpe"] > m0["sharpe"]
    h1_mdd = (m1["mdd"] - m0["mdd"]) >= -0.03
    h1 = h1_sharpe and h1_mdd
    red = 1 - m1["salidas"] / m0["salidas"] if m0["salidas"] else float("nan")
    h2 = red >= 0.40
    if h1 and h2:
        est = "Replicado"
    elif h1:
        est = "H1 sostenida, H2 refutada (caso no previsto en §2)"
    elif h2:
        est = "No replicado (H1 refutada; H2 sostenida)"
    else:
        est = "No replicado (H1 y H2 refutadas)"
    out.append("")
    out.append("== Veredicto %s (V1 contra V0) ==" % etiqueta)
    out.append("Sharpe V1 %.3f vs V0 %.3f -> %s" % (m1["sharpe"], m0["sharpe"], "V1 mayor" if h1_sharpe else "V1 NO mayor"))
    out.append("MDD V1 %.1f%% vs V0 %.1f%% (dif %+.1f pp) -> %s" % (
        100 * m1["mdd"], 100 * m0["mdd"], 100 * (m1["mdd"] - m0["mdd"]), "ok (no peor en >3 pp)" if h1_mdd else "peor en >3 pp"))
    out.append("H1: %s" % ("sostenida" if h1 else "REFUTADA"))
    out.append("Salidas V1 %d vs V0 %d -> reducción %.0f%% -> H2 %s" % (
        m1["salidas"], m0["salidas"], 100 * red, "sostenida" if h2 else "REFUTADA"))
    out.append("Estado según §2: %s" % est)
    return {"h1": h1, "h2": h2, "estado": est}


def main():
    out = ["AC-21-R12 ejecución B (b.py). Fuentes: FRED NASDAQ100, VIXCLS, DTB3; VXOCLS + CBOE SPX (secundaria)."]
    ndx = leer_fred("NASDAQ100")
    vix = leer_fred("VIXCLS")
    dtb3 = leer_fred("DTB3")
    vxo = leer_fred("VXOCLS")
    out.append("NASDAQ100 FRED: %s a %s (%d obs); VIXCLS: %s a %s; DTB3 hasta %s; VXOCLS %s a %s" % (
        min(ndx), max(ndx), len(ndx), min(vix), max(vix), max(dtb3), min(vxo), max(vxo)))
    out.append("Nota: FRED aún no publica el 2026-10-16; el último cierre común es el anterior.")
    tramos = [("Completo", ("0000", FIN)), ("1990-2008", ("1990-01-01", "2008-12-31")),
              ("2009-hoy", ("2009-01-01", FIN))]
    res = correr(ndx, vix, dtb3, "1990-01-02", FIN, "Nasdaq-100 3x sintético (principal)", out, tramos, VARIANTES)
    v = veredicto(res, "0000", FIN, out, "periodo completo")
    v8 = veredicto(res, "1990-01-01", "2008-12-31", out, "1990-2008 (informativo)")
    v9 = veredicto(res, "2009-01-01", FIN, out, "2009-hoy (informativo)")

    # Sensibilidad: SMA200 calculada con la historia de NDX desde 1986 (la señal existe desde 1990-01-02)
    out.append("")
    out.append("== Sensibilidad: SMA200 con historia NDX desde 1986 (no pre-registrada) ==")
    fechas_all = sorted(ndx)
    px_all = [ndx[d] for d in fechas_all]
    sma = {}
    s = 0.0
    for i, p in enumerate(px_all):
        s += p
        if i >= 200:
            s -= px_all[i - 200]
        if i >= 199:
            sma[fechas_all[i]] = s / 200
    fechas, _, _ = panel(ndx, vix, "1990-01-02", FIN)
    px = [ndx[d] for d in fechas]; vx = [vix[d] for d in fechas]; rf = rf_diaria(fechas, dtb3)
    sm = [sma[d] for d in fechas]
    def sen2(umbral, usar_vix, sostener=1):
        est = []; e = 0
        for t in range(len(px)):
            alto = all(vx[t - k] >= umbral for k in range(sostener)) if t >= sostener - 1 else False
            salir = px[t] < sm[t] * 0.97 or (usar_vix and alto)
            entrar = px[t] > sm[t] * 1.03 and (not usar_vix or vx[t] < umbral)
            if e == 1 and salir: e = 0
            elif e == 0 and entrar: e = 1
            est.append(e)
        return est
    res2 = [("V0 vigente (VIX>=25)", simular(fechas, px, sen2(25, True), rf)),
            ("V1 solo SMA200 +-3%", simular(fechas, px, sen2(25, False), rf)),
            ("V2 VIX>=25 2 cierres", simular(fechas, px, sen2(25, True, 2), rf)),
            ("V3 VIX>=30", simular(fechas, px, sen2(30, True), rf)),
            ("B&H 3x", bh(fechas, px, sen2(25, False), rf))]
    tabla("Nasdaq-100, SMA con historia previa, desde 1990-01-04", res2, tramos[:1], out)

    # Secundaria: S&P 500 (CBOE) con VXO, 1986-1989
    spx = leer_cboe_spx()
    tr = [("1986-1989", ("0000", "1989-12-31"))]
    res3 = correr(spx, vxo, dtb3, "1986-01-02", "1989-12-31", "Secundaria S&P 500 3x con VXO 1986-1989", out, tr, VARIANTES)
    veredicto(res3, "0000", "1989-12-31", out, "secundaria S&P/VXO (informativa)")

    txt = "\n".join(out)
    print(txt)
    with open(os.path.join(AQUI, "salida.txt"), "w") as f:
        f.write(txt + "\n")
    js = {}
    for k, r in res:
        js[k] = {t: metricas(r, a, b) for t, (a, b) in tramos}
    js["_veredicto"] = {"completo": v, "1990-2008": v8, "2009-hoy": v9}
    with open(os.path.join(AQUI, "b-resultados.json"), "w") as f:
        json.dump(js, f, indent=1)


if __name__ == "__main__":
    main()
