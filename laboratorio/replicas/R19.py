"""R19 (ejecución A): costo del ISR del SIC (LISR art. 129, 10% definitivo) sobre la mezcla de papel GBM, en MXN.
Mezcla de R18 (SPYM 41%, QQQM 26.8%, UPRO 26.9% con filtro V0, efectivo 5.3%), 1994-2026.
Pre-registro: R19-isr-sic-mezcla-papel.md (mismo commit). Datos: cachés de R16/R12 y R19-datos (FRED DEXMXUS y MEXCPIALLMINMEI).
Reproduce: python3 laboratorio/replicas/R19.py"""
import csv, hashlib, json, math, os, sys
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import R16  # noqa: E402
import R18  # noqa: E402

TASA, COM = 0.10, 0.0025 * 1.16         # art. 129; comisión GBM 0.25% + IVA por operación
PESOS = {"S": None, "Q": 0.268, "U": 0.269, "C": 0.053}   # S = resto
INICIO = "1994-01-03"
INFL_EXTRAP = 0.04                      # inflación anual supuesta después del último dato de MEXCPIALLMINMEI


def fred(nombre):
    ruta = os.path.join(BASE, "R19-datos", nombre + ".csv")
    raw = open(ruta, "rb").read()
    filas = [r for r in csv.reader(raw.decode().splitlines())][1:]
    return [(d, float(v)) for d, v in filas if v not in ("", ".")], hashlib.sha256(raw).hexdigest()


def cpi_mensual(infl=INFL_EXTRAP):
    serie, sha = fred("MEXCPIALLMINMEI")
    c = {d[:7]: v for d, v in serie}
    ult = max(c); y, m = map(int, ult.split("-")); v = c[ult]
    while (y, m) < (2027, 1):
        m += 1
        if m == 13: y, m = y + 1, 1
        v *= (1 + infl) ** (1 / 12); c[f"{y:04d}-{m:02d}"] = v
    return c, sha


def mes_menos(ym, k):
    y, m = map(int, ym.split("-")); m -= k
    while m <= 0: y, m = y - 1, m + 12
    return f"{y:04d}-{m:02d}"


def datos():
    D, ndx, sha_r18 = R18.cargar()
    fechas, px, op, lo, tr, vix, rf = D
    sen = R16.filtro(px, vix)
    fx_s, sha_fx = fred("DEXMXUS")
    fx = dict(fx_s)
    filas, ult_fx = [], None
    fx_ord = sorted(fx)
    j = 0
    for i in range(2, len(fechas)):
        d, d0 = fechas[i], fechas[i - 1]
        while j < len(fx_ord) and fx_ord[j] <= d:
            ult_fx = fx[fx_ord[j]]; j += 1
        if d < INICIO or ult_fx is None or d not in ndx or d0 not in ndx or sen[i - 2] is None:
            continue
        if d > fx_ord[-1]:
            break
        r1 = tr[i] / tr[i - 1] - 1
        filas.append(dict(d=d, rs=r1 - R18.GASTO_SPYM, rq=ndx[d] / ndx[d0] - 1 - R18.GASTO_QQQM,
                          ru=3 * r1 - 2 * rf[i] - R18.GASTO_UPRO, rf=rf[i], on=sen[i - 2] == 1, fx=ult_fx))
    return filas, {"r16_r12": sha_r18, "DEXMXUS": sha_fx}


class Lote:
    """Costo promedio por emisora: costo 'real' = suma de MXN pagados / INPC(mes de compra − 1)."""
    def __init__(self):
        self.usd = 0.0; self.real = 0.0; self.nom = 0.0; self.cost_usd = 0.0

    def compra(self, usd, fx, cpi_ref):
        mxn = usd * fx
        self.usd += usd; self.real += mxn / cpi_ref; self.nom += mxn; self.cost_usd += usd

    def venta(self, frac, fx, factor_num, usd_val):
        """Vende la fracción frac de la posición (valor usd_val antes de vender). Devuelve (ganancia fiscal MXN,
        ganancia nominal MXN sin INPC, ganancia en USD × FX de venta)."""
        if frac <= 0 or self.usd <= 0: return 0.0, 0.0, 0.0
        venta_mxn = frac * usd_val * fx
        costo_act = max(frac * self.real * factor_num, frac * self.nom)   # art. 17-A: factor >= 1 (en agregado)
        g_fis = venta_mxn - costo_act
        g_nom = venta_mxn - frac * self.nom
        g_usdfx = (frac * usd_val - frac * self.cost_usd) * fx
        self.usd *= 1 - frac; self.real *= 1 - frac; self.nom *= 1 - frac; self.cost_usd *= 1 - frac
        return g_fis, g_nom, g_usdfx


def simular(filas, cpi, modo, wu=0.269, impuestos=True):
    """modo: 'M' rebalanceo mensual + filtro; 'A' rebalanceo anual (enero) + filtro; 'F' solo filtro; 'B' 100% S&P TR."""
    if modo == "B":
        w = {"S": 1.0, "Q": 0.0, "U": 0.0, "C": 0.0}
    else:
        w = {"S": 1 - wu - 0.268 - 0.053, "Q": 0.268, "U": wu, "C": 0.053}
    v = {k: 0.0 for k in w}                       # valores en USD
    lotes = {k: Lote() for k in ("S", "Q", "U")}
    st = dict(neto=0.0, perdidas=[], pend=None, imp_total=0.0, gnom=0.0, gusd=0.0, comis=0.0)
    f0 = filas[0]; fx0 = f0["fx"]
    capital_usd = 1.0 / fx0                       # 1 MXN inicial
    u_on = f0["on"] and wu > 0

    def cpi_ref(d): return cpi[mes_menos(d[:7], 1)]
    def factor_num(d): return cpi[mes_menos(d[:7], 2)]

    def realizar(k, frac, d, fx):
        g, gn, gu = lotes[k].venta(frac, fx, factor_num(d), v[k])
        st["neto"] += g; st["gnom"] += gn; st["gusd"] += gu

    def comprar(k, usd, d, fx):
        lotes[k].compra(usd, fx, cpi_ref(d))

    def comision(usd):
        c = abs(usd) * COM; st["comis"] += c; return c

    # Compra inicial
    d, fx = f0["d"], fx0
    for k in ("S", "Q", "U", "C"):
        monto = capital_usd * w[k]
        if k == "U" and not u_on:
            v["C"] += monto; continue
        if k == "C":
            v["C"] += monto; continue
        c = comision(monto); v[k] = monto - c
        comprar(k, v[k], d, fx)
    mes, anio = d[:7], d[:4]
    for idx, f in enumerate(filas[1:], 1):
        d, fx = f["d"], f["fx"]
        # Cierre de ejercicio: al cambiar de año se calcula el impuesto del año anterior (se paga en abril)
        if d[:4] != anio:
            if impuestos:
                base = st["neto"]
                # pérdidas arrastradas (10 años, sin actualizar)
                st["perdidas"] = [(a, p) for a, p in st["perdidas"] if int(anio) - a <= 10]
                if base > 0:
                    for i_p, (a, p) in enumerate(st["perdidas"]):
                        uso = min(p, base); base -= uso; st["perdidas"][i_p] = (a, p - uso)
                        if base <= 0: break
                    st["pend"] = TASA * max(base, 0.0)
                elif base < 0:
                    st["perdidas"].append((int(anio), -base))
                st["neto"] = 0.0
            anio = d[:4]
        # Pago del impuesto en el primer día hábil de mayo (declaración anual de abril): venta pro rata
        if impuestos and st["pend"] and d[5:7] >= "05":
            imp_usd = st["pend"] / fx
            tot = sum(v.values())
            frac = min(imp_usd / tot, 1.0)
            for k in ("S", "Q", "U"):
                if v[k] > 0:
                    realizar(k, frac, d, fx)
                    c = comision(v[k] * frac); v["C"] += v[k] * frac - c; v[k] *= 1 - frac
            v["C"] -= imp_usd                  # el pago sale del efectivo (que ya recibió lo vendido)
            st["imp_total"] += st["pend"]; st["pend"] = None
        # Filtro del 3x
        if modo != "B" and wu > 0 and f["on"] != u_on:
            if not f["on"]:                        # salida: vende todo UPRO
                realizar("U", 1.0, d, fx)
                c = comision(v["U"]); v["C"] += v["U"] - c; v["U"] = 0.0
            else:                                  # reentrada: compra con el peso objetivo del total
                tot = sum(v.values()); monto = min(tot * wu, v["C"]) if modo == "F" else tot * wu
                c = comision(monto); v["C"] -= monto; v["U"] = monto - c
                comprar("U", v["U"], d, fx)
            u_on = f["on"]
        # Rebalanceo
        reb = (modo == "M" and d[:7] != mes) or (modo == "A" and d[:4] != mes[:4])
        if reb:
            tot = sum(v.values())
            obj = {k: tot * w[k] for k in w}
            if not u_on:
                obj["C"] += obj["U"]; obj["U"] = 0.0
            for k in ("S", "Q", "U"):                  # primero ventas
                if v[k] > obj[k] + 1e-15:
                    frac = (v[k] - obj[k]) / v[k]
                    realizar(k, frac, d, fx)
                    c = comision(v[k] - obj[k]); v["C"] += v[k] - obj[k] - c; v[k] = obj[k]
            for k in ("S", "Q", "U"):                  # después compras
                if v[k] < obj[k] - 1e-15:
                    monto = obj[k] - v[k]; c = comision(monto); v["C"] -= monto; v[k] += monto - c
                    comprar(k, monto - c, d, fx)
        mes = d[:7]
        # Rendimientos del día
        v["S"] *= 1 + f["rs"]; v["Q"] *= 1 + f["rq"]
        v["U"] *= 1 + (f["ru"] if u_on else 0.0)
        v["C"] *= 1 + f["rf"]
    # Liquidación final
    d, fx = filas[-1]["d"], filas[-1]["fx"]
    for k in ("S", "Q", "U"):
        if v[k] > 0:
            realizar(k, 1.0, d, fx)
            c = comision(v[k]); v["C"] += v[k] - c; v[k] = 0.0
    final_mxn = v["C"] * fx
    if impuestos:
        base = st["neto"]
        st["perdidas"] = [(a, p) for a, p in st["perdidas"] if int(anio) - a <= 10]
        for i_p, (a, p) in enumerate(st["perdidas"]):
            if base <= 0: break
            uso = min(p, base); base -= uso
        imp = TASA * max(base, 0.0) + (st["pend"] or 0.0)
        st["imp_total"] += imp; final_mxn -= imp
    anios = (dia(filas[-1]["d"]) - dia(filas[0]["d"])) / 365.25
    return dict(final=final_mxn, cagr=final_mxn ** (1 / anios) - 1, anios=anios, imp_total=st["imp_total"],
                gnom=st["gnom"], gusd=st["gusd"], comis_usd=st["comis"])


def dia(s):
    import datetime
    return datetime.date.fromisoformat(s).toordinal()


def main():
    filas, shas = datos()
    cpi, sha_cpi = cpi_mensual()
    shas["MEXCPIALLMINMEI"] = sha_cpi
    out = {"periodo": [filas[0]["d"], filas[-1]["d"]], "n_dias": len(filas), "sha256": shas, "variantes": {}}
    print(f"R19 A · {filas[0]['d']} a {filas[-1]['d']} · {len(filas)} días")
    print("| Variante | CAGR MXN antes de ISR | CAGR después de ISR | Arrastre (pp/año) | ISR pagado / capital inicial | Parte cambiaria de la ganancia nominal realizada |")
    print("|---|---|---|---|---|---|")
    for modo, nombre in (("M", "Vigente, rebalanceo mensual + filtro"), ("A", "Rebalanceo anual + filtro"),
                         ("F", "Solo filtro (sin rebalanceo)"), ("B", "100% S&P TR, compra y mantén")):
        pre = simular(filas, cpi, modo, impuestos=False)
        post = simular(filas, cpi, modo, impuestos=True)
        arr = (pre["cagr"] - post["cagr"]) * 100
        fxp = 1 - post["gusd"] / post["gnom"] if post["gnom"] > 0 else float("nan")
        out["variantes"][modo] = dict(nombre=nombre, cagr_pre=pre["cagr"], cagr_post=post["cagr"], arrastre_pp=arr,
                                      isr_sobre_capital=post["imp_total"], parte_fx=fxp, final_pre=pre["final"],
                                      final_post=post["final"])
        print(f"| {nombre} | {pre['cagr']:.2%} | {post['cagr']:.2%} | {arr:.2f} | {post['imp_total']:.2f}x | {fxp:.1%} |")
    # Sensibilidad a la inflación extrapolada
    sens = {}
    for infl in (0.0, 0.08):
        c2, _ = cpi_mensual(infl)
        pre = simular(filas, c2, "M", impuestos=False); post = simular(filas, c2, "M", impuestos=True)
        sens[str(infl)] = (pre["cagr"] - post["cagr"]) * 100
    out["sensibilidad_inflacion_extrapolada_M_pp"] = sens
    M, F = out["variantes"]["M"], out["variantes"]["F"]
    h1 = M["arrastre_pp"] >= 1.0
    h2 = (M["arrastre_pp"] - F["arrastre_pp"]) >= 0.3
    h3 = M["parte_fx"] >= 0.30
    out["hipotesis"] = {"H1_arrastre_M>=1.0pp": h1, "H2_M-F>=0.3pp": h2, "H3_parte_fx>=30%": h3,
                        "M-F_pp": M["arrastre_pp"] - F["arrastre_pp"]}
    print(f"Sensibilidad (M): inflación extrapolada 0% → {sens['0.0']:.2f} pp; 8% → {sens['0.08']:.2f} pp")
    print("H1 (arrastre M ≥ 1.0 pp):", h1, "| H2 (M − F ≥ 0.3 pp):", h2, f"({M['arrastre_pp'] - F['arrastre_pp']:.2f})",
          "| H3 (parte cambiaria ≥ 30%):", h3)
    json.dump(out, open(os.path.join(BASE, "R19-resultados.json"), "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
