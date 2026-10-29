"""R22 (ejecución A): ¿qué regla pronostica mejor la tasa efectiva trimestral de impuestos (ETR)?
Universo: emisoras de EUA de empresas/universo.csv (XBRL de la SEC, companyconcept). Pre-registro:
R22-tasa-efectiva-pronostico.md (mismo commit). Reproduce: python3 laboratorio/replicas/R22.py
User-Agent: el de herramientas/edgar.py por defecto (sin correo); solo data.sec.gov."""
import csv, json, os, statistics as st, sys, datetime as dt, math, random
BASE = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join(BASE, "..", "..")
sys.path.insert(0, os.path.join(RAIZ, "herramientas"))
import edgar  # noqa: E402

CACHE = os.path.join(BASE, "R22-datos")
IMP = "IncomeTaxExpenseBenefit"
PRE = ["IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
       "IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments",
       "IncomeLossFromContinuingOperationsBeforeIncomeTaxesDomestic"]
EXCLUIR = {"BRK-B", "SPCX"}           # aseguradora con ETR atípica y ticker sin XBRL propio
DESDE_OBJ = "2022-01-01"               # trimestres objetivo con fin >= esta fecha
FIN_OBJ = "2026-09-30"


def concepto(cik, tag):
    os.makedirs(CACHE, exist_ok=True)
    f = os.path.join(CACHE, f"{cik}_{tag}.json")
    if not os.path.exists(f):
        try:
            raw = edgar._get(f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik:010d}/us-gaap/{tag}.json")
        except edgar.ErrorSEC as e:
            if getattr(e, "codigo", None) == 404 or "404" in str(e):
                open(f, "w").write("{}"); return {}
            raise
        open(f, "wb").write(raw)
    return json.load(open(f))


def trimestres(js):
    """{fin: valor} de duraciones de 80-100 días; gana el último presentado."""
    out = {}
    for u in sorted(js.get("units", {}).get("USD", []), key=lambda z: z.get("filed", "")):
        if not u.get("start"): continue
        d = (dt.date.fromisoformat(u["end"]) - dt.date.fromisoformat(u["start"])).days
        if 80 <= d <= 100:
            out[u["end"]] = u["val"]
    return out


def serie_etr(ticker):
    cik = edgar.cik_de_ticker(ticker)
    imp = trimestres(concepto(cik, IMP))
    pre = {}
    for t in PRE:
        p = trimestres(concepto(cik, t))
        if len(p) > len(pre): pre = p
    s = {}
    for fin, x in imp.items():
        if fin in pre and pre[fin] > 0:
            r = x / pre[fin]
            if 0.0 <= r <= 0.60:          # filtro pre-registrado
                s[fin] = r
    return dict(sorted(s.items()))


def reglas(hist):
    """hist: lista de ETR anteriores (más reciente al final), solo de los últimos 15 meses para 4 y 27 meses para 8."""
    out = {"ultimo": hist[-1]}
    if len(hist) >= 4:
        out["mediana4"] = st.median(hist[-4:]); out["media4"] = st.mean(hist[-4:])
    if len(hist) >= 8:
        out["mediana8"] = st.median(hist[-8:])
    out["fija21"] = 0.21
    return out


def main():
    tick = [r["ticker"] for r in csv.DictReader(open(os.path.join(RAIZ, "empresas", "universo.csv")))
            if r["mercado"] == "US" and r["ticker"] not in EXCLUIR]
    errores = {k: [] for k in ("ultimo", "mediana4", "media4", "mediana8", "fija21")}
    pares = []   # (|e_ultimo|, |e_mediana4|) en las mismas observaciones
    usados, fallidos = [], []
    for t in tick:
        try:
            s = serie_etr(t)
        except Exception as e:
            fallidos.append(f"{t}: {e}"); continue
        fechas = list(s)
        n0 = 0
        for i, fin in enumerate(fechas):
            if not (DESDE_OBJ <= fin <= FIN_OBJ): continue
            f_fin = dt.date.fromisoformat(fin)
            hist = [s[f] for f in fechas[:i] if (f_fin - dt.date.fromisoformat(f)).days <= 460]
            hist8 = [s[f] for f in fechas[:i] if (f_fin - dt.date.fromisoformat(f)).days <= 830]
            if len(hist) < 4: continue
            R = reglas(hist); R8 = reglas(hist8) if len(hist8) >= 8 else {}
            real = s[fin]
            for k in ("ultimo", "mediana4", "media4", "fija21"):
                errores[k].append(abs(real - R[k]) * 100)
            if "mediana8" in R8:
                errores["mediana8"].append(abs(real - R8["mediana8"]) * 100)
            pares.append((abs(real - R["ultimo"]) * 100, abs(real - R["mediana4"]) * 100, real))
            n0 += 1
        if n0: usados.append((t, n0))
    res = {"emisoras": len(usados), "observaciones": len(pares), "usados": usados, "fallidos": fallidos}
    res["MAE_pp"] = {k: round(st.mean(v), 3) for k, v in errores.items() if v}
    res["mediana_AE_pp"] = {k: round(st.median(v), 3) for k, v in errores.items() if v}
    res["n_por_regla"] = {k: len(v) for k, v in errores.items()}
    # prueba de signos pareada (dos colas) mediana4 contra último
    mejor = sum(1 for a, b, _ in pares if b < a); peor = sum(1 for a, b, _ in pares if b > a); n = mejor + peor
    z = (mejor - n / 2) / math.sqrt(n / 4) if n else 0
    p = math.erfc(abs(z) / math.sqrt(2))
    res["signos_mediana4_vs_ultimo"] = {"mejor": mejor, "peor": peor, "z": round(z, 2), "p_dos_colas": round(p, 4)}
    # bootstrap por emisora no se hace; IC de la diferencia de MAE por remuestreo de observaciones
    random.seed(22); difs = sorted(st.mean(random.choices([a - b for a, b, _ in pares], k=len(pares))) for _ in range(4000))
    res["dif_MAE_ultimo_menos_mediana4_IC95"] = [round(difs[100], 3), round(difs[3899], 3)]
    # traducción a UPA: error relativo de UPA ≈ |Δτ| / (1 − τ)
    res["error_UPA_pct_mediana4"] = round(st.mean(b / 100 / (1 - r) for _, b, r in pares) * 100, 2)
    res["H1_mediana4_mejor_que_ultimo"] = (res["MAE_pp"]["mediana4"] < res["MAE_pp"]["ultimo"]) and p < 0.05
    res["H2_MAE_mediana4_le_3pp"] = res["MAE_pp"]["mediana4"] <= 3.0
    print(json.dumps(res, indent=1, ensure_ascii=False))
    json.dump(res, open(os.path.join(BASE, "R22-resultados.json"), "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
