"""R19b (ejecución A): R19 con las dos omisiones que señaló la auditoría W43:
(1) impuesto a los dividendos de la manga S&P (retención total τ_div sobre el dividendo, que se reinvierte neto);
(2) efectivo en MXN a la tasa de CETES (FRED INTGSTMXM193N, mensual) con impuesto τ_int sobre el interés nominal.
QQQM (Nasdaq-100 de precio) y UPRO no generan dividendos en el modelo (sesgo declarado: subestima un poco).
Pre-registro: R19b-dividendos-y-efectivo-mxn.md (mismo commit). Reproduce: python3 laboratorio/replicas/R19b.py"""
import csv, json, os, sys
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import R16, R18, R19  # noqa: E402


def cetes():
    filas = list(csv.reader(open(os.path.join(BASE, "R19-datos", "INTGSTMXM193N.csv")).read().splitlines()))[1:]
    m = {d[:7]: float(v) / 100 for d, v in filas if v not in ("", ".")}
    ult = max(m)
    return m, ult


def filas_b(tau_div, tau_int, cash_mxn=True):
    D, ndx, _ = R18.cargar()
    fechas, px, op, lo, tr, vix, rf = D
    base = R19.datos()[0]                      # mismas filas, filtros y FX que R19
    idx = {d: i for i, d in enumerate(fechas)}
    tasa, ult = cetes()
    out, fx_prev = [], None
    for f in base:
        i = idx[f["d"]]
        div = (tr[i] / tr[i - 1]) - (px[i] / px[i - 1])          # rendimiento por dividendo del día
        g = dict(f)
        g["rs"] = f["rs"] - tau_div * div
        if cash_mxn:
            r_mx = tasa.get(f["d"][:7], tasa[ult]) / 252
            r_mx_net = r_mx * (1 - tau_int)
            fxc = f["fx"]
            # efectivo en MXN expresado en USD: cambia con el tipo de cambio
            g["rf"] = (1 + r_mx_net) * (fx_prev / fxc) - 1 if fx_prev else r_mx_net
        out.append(g); fx_prev = f["fx"]
    return out


def correr(tau_div, tau_int, modo, cash_mxn=True):
    cpi, _ = R19.cpi_mensual()
    bruto = filas_b(0.0, 0.0, cash_mxn)
    neto = filas_b(tau_div, tau_int, cash_mxn)
    pre = R19.simular(bruto, cpi, modo, impuestos=False)
    post = R19.simular(neto, cpi, modo, impuestos=True)
    return pre["cagr"], post["cagr"], (pre["cagr"] - post["cagr"]) * 100


def main():
    res = {}
    print("R19b A · arrastre total = CAGR MXN sin ningún impuesto − CAGR con ISR art. 129 + dividendos + intereses")
    print("| Variante | τ_div | τ_int | efectivo | CAGR pre | CAGR post | Arrastre (pp/año) |")
    print("|---|---|---|---|---|---|---|")
    for modo in ("M", "A", "F", "B"):
        for tau_div in (0.10, 0.20, 0.30):
            for tau_int in (0.0, 0.20):
                if modo != "M" and not (tau_div == 0.20 and tau_int == 0.20):
                    continue
                pre, post, arr = correr(tau_div, tau_int, modo)
                res[f"{modo}_{tau_div}_{tau_int}"] = dict(pre=pre, post=post, arrastre_pp=arr)
                print(f"| {modo} | {tau_div:.0%} | {tau_int:.0%} | MXN (CETES) | {pre:.2%} | {post:.2%} | {arr:.2f} |")
    # Control: R19 original (efectivo T-bill USD, sin impuestos a dividendos ni intereses)
    pre, post, arr = correr(0.0, 0.0, "M", cash_mxn=False)
    res["control_R19_M"] = dict(pre=pre, post=post, arrastre_pp=arr)
    print(f"| Control R19 (M) | 0% | 0% | T-bill USD | {pre:.2%} | {post:.2%} | {arr:.2f} |")
    central = res["M_0.2_0.2"]["arrastre_pp"]
    rango = [res[f"M_{d}_{i}"]["arrastre_pp"] for d in (0.10, 0.20, 0.30) for i in (0.0, 0.20)]
    h1b = central >= 1.0
    h2b = (res["M_0.2_0.2"]["arrastre_pp"] - res["F_0.2_0.2"]["arrastre_pp"]) >= 0.3
    res["hipotesis"] = {"H1b_central>=1.0": h1b, "H2b_M-F>=0.3": h2b, "rango_M": [min(rango), max(rango)]}
    print(f"H1b (central M ≥ 1.0 pp): {h1b} ({central:.2f}) · rango M {min(rango):.2f}-{max(rango):.2f} · H2b (M − F ≥ 0.3): {h2b}")
    json.dump(res, open(os.path.join(BASE, "R19b-resultados.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
