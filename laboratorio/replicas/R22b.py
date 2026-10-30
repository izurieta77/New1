"""R22b (ejecución A corregida de R22): pronóstico de la tasa efectiva trimestral con etiquetas XBRL unidas
periodo a periodo y el 4T reconstruido (anual − 9 meses). Pre-registro: R22b-tasa-efectiva-corregida.md (mismo commit).
Datos: SEC companyfacts (data.sec.gov; User-Agent por defecto del repo, sin correo). Reproduce: python3 laboratorio/replicas/R22b.py"""
import csv, json, os, statistics as st, sys, datetime as dt, math, random
BASE = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join(BASE, "..", "..")
sys.path.insert(0, os.path.join(RAIZ, "herramientas"))
import edgar  # noqa: E402

CACHE = os.path.join(BASE, "R22b-datos")
IMP = "IncomeTaxExpenseBenefit"
PRE = ["IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
       "IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments"]
EXCLUIR = {"BRK-B", "SPCX"}
CIK_FIJO = {"GE": [40545], "XOM": [34088, 2115436]}   # GE: efts falla con "GE"; XOM: predecesora + nueva tenedora
DESDE_OBJ, FIN_OBJ = "2022-01-01", "2026-09-30"


def hechos(cik):
    os.makedirs(CACHE, exist_ok=True)
    f = os.path.join(CACHE, f"{cik}.json")
    if not os.path.exists(f):
        open(f, "wb").write(edgar._get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"))
    return json.load(open(f)).get("facts", {}).get("us-gaap", {})


def duraciones(facts, tag):
    """{(inicio, fin): valor} de todas las duraciones; gana el último presentado."""
    out = {}
    for u in sorted(facts.get(tag, {}).get("units", {}).get("USD", []), key=lambda z: z.get("filed", "")):
        if u.get("start"):
            out[(u["start"], u["end"])] = u["val"]
    return out


def dias(a, b):
    return (dt.date.fromisoformat(b) - dt.date.fromisoformat(a)).days


def trimestrales(d):
    """{fin: valor} de trimestres: duraciones de 80-100 días, más el 4T reconstruido = anual (350-380 días) − 9M (260-290)."""
    q = {fin: v for (ini, fin), v in d.items() if 80 <= dias(ini, fin) <= 100}
    q4 = {}
    for (ini, fin), v in d.items():
        if 350 <= dias(ini, fin) <= 380 and fin not in q:
            nueve = [w for (i2, f2), w in d.items() if i2 == ini and 260 <= dias(i2, f2) <= 290]
            if nueve:
                q4[fin] = v - nueve[-1]
    return q, q4


def serie(ticker):
    ciks = CIK_FIJO.get(ticker) or [edgar.cik_de_ticker(ticker)]
    imp, pre, imp4, pre4 = {}, {}, {}, {}
    for cik in ciks:
        F = hechos(cik)
        a, a4 = trimestrales(duraciones(F, IMP))
        imp.update(a); imp4.update(a4)
        for tag in PRE:                       # unión periodo a periodo: la primera etiqueta con dato gana
            b, b4 = trimestrales(duraciones(F, tag))
            for k, v in b.items(): pre.setdefault(k, v)
            for k, v in b4.items(): pre4.setdefault(k, v)
    s = {}
    for fuente_i, fuente_p, es4 in ((imp, pre, False), (imp4, pre4, True)):
        for fin, x in fuente_i.items():
            if fin in fuente_p and fuente_p[fin] > 0:
                r = x / fuente_p[fin]
                if 0.0 <= r <= 0.60 and fin not in s:
                    s[fin] = (r, es4)
    return dict(sorted(s.items()))


def evaluar(series, con4):
    E = {k: [] for k in ("ultimo", "mediana4", "media4", "mediana8", "fija21")}
    pares = []
    for t, s in series.items():
        fechas = [f for f in s if con4 or not s[f][1]]
        for i, fin in enumerate(fechas):
            if not (DESDE_OBJ <= fin <= FIN_OBJ): continue
            f0 = dt.date.fromisoformat(fin)
            h = [s[f][0] for f in fechas[:i] if (f0 - dt.date.fromisoformat(f)).days <= 460]
            h8 = [s[f][0] for f in fechas[:i] if (f0 - dt.date.fromisoformat(f)).days <= 830]
            if len(h) < 4: continue
            real = s[fin][0]
            e = {"ultimo": h[-1], "mediana4": st.median(h[-4:]), "media4": st.mean(h[-4:]), "fija21": 0.21}
            for k, v in e.items(): E[k].append(abs(real - v) * 100)
            if len(h8) >= 8: E["mediana8"].append(abs(real - st.median(h8[-8:])) * 100)
            pares.append((abs(real - h[-1]) * 100, abs(real - e["mediana4"]) * 100, real))
    mejor = sum(1 for a, b, _ in pares if b < a); peor = sum(1 for a, b, _ in pares if b > a); n = mejor + peor
    # prueba de signos binomial exacta, dos colas
    k = min(mejor, peor); p = min(1.0, 2 * sum(math.comb(n, j) for j in range(0, k + 1)) / 2 ** n) if n else 1.0
    random.seed(22); dif = sorted(st.mean(random.choices([a - b for a, b, _ in pares], k=len(pares))) for _ in range(4000))
    return {"objetivos": len(pares), "MAE_pp": {k: round(st.mean(v), 3) for k, v in E.items() if v},
            "n": {k: len(v) for k, v in E.items()}, "signos": {"mejor": mejor, "peor": peor, "p_exacta": round(p, 5)},
            "IC95_dif_MAE": [round(dif[100], 3), round(dif[3899], 3)],
            "error_UPA_pct_mediana4": round(st.mean(b / 100 / (1 - r) for _, b, r in pares) * 100, 2)}


def main():
    tick = [r["ticker"] for r in csv.DictReader(open(os.path.join(RAIZ, "empresas", "universo.csv")))
            if r["mercado"] == "US" and r["ticker"] not in EXCLUIR]
    series, fallidos = {}, []
    for t in tick:
        try:
            s = serie(t)
            if s: series[t] = s
        except Exception as e:
            fallidos.append(f"{t}: {e}")
    sin4, con4 = evaluar(series, False), evaluar(series, True)
    res = {"emisoras_con_serie": len(series), "fallidos": fallidos, "sin_4T": sin4, "con_4T": con4}
    res["H1_sin4T_signos_p_lt_0.05_y_mediana4_mejor"] = sin4["signos"]["p_exacta"] < 0.05 and sin4["MAE_pp"]["mediana4"] < sin4["MAE_pp"]["ultimo"]
    res["H2_sin4T_MAE_mediana4_le_3"] = sin4["MAE_pp"]["mediana4"] <= 3.0
    res["H3_con4T_signos_p_lt_0.05_y_mediana4_mejor"] = con4["signos"]["p_exacta"] < 0.05 and con4["MAE_pp"]["mediana4"] < con4["MAE_pp"]["ultimo"]
    print(json.dumps(res, indent=1, ensure_ascii=False))
    json.dump(res, open(os.path.join(BASE, "R22b-resultados.json"), "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
