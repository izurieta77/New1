#!/usr/bin/env python3
"""AC-29-R22: ejecucion B independiente de R22 (pronostico de la tasa efectiva trimestral).

Construccion propia, distinta de A:
  - CIK por la busqueda de entidades de efts.sec.gov (no company_tickers.json).
  - Datos del endpoint companyfacts COMPLETO (no companyconcept).
  - Utilidad antes de impuestos: se combinan las etiquetas alternativas periodo a periodo
    (la de mas trimestres manda; las demas solo rellenan huecos).
  - Variante adicional: 4T reconstruido = anual (10-K) - 9 meses acumulados (10-Q del 3T),
    para impuesto y utilidad antes de impuestos.
Solo biblioteca estandar. User-Agent sin correo. <= ~7 solicitudes/s.
"""
import csv, json, math, os, random, statistics, sys, time, urllib.request, gzip
from datetime import date, timedelta

RAIZ = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(RAIZ, "datos")
REPO = os.path.abspath(os.path.join(RAIZ, "..", "..", ".."))
UA = "SistemaInversionNew1/1.0 investigacion"
INI_OBJ, FIN_OBJ = date(2022, 1, 1), date(2026, 9, 30)
SEMILLA, NBOOT = 20261029, 10000
ETIQ_PRETAX = [
    "IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
    "IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments",
    "IncomeLossFromContinuingOperationsBeforeIncomeTaxesDomestic",  # nunca deberia ganar; se excluye abajo
]
# La etiqueta "Domestic" es solo la parte domestica: NO se usa (seria un error de concepto).
ETIQ_PRETAX = ETIQ_PRETAX[:2] + ["IncomeLossBeforeIncomeTaxes", "IncomeLossFromContinuingOperationsBeforeIncomeTaxes"]
ETIQ_TAX = ["IncomeTaxExpenseBenefit"]
# ExxonMobil Holdings Corp (CIK 2115436, ticker XOM en efts) es la nueva tenedora; la historia
# XBRL esta en Exxon Mobil Corp (CIK 34088). Se unen ambas.
PREDECESORAS = {"XOM": [34088]}
# Emisoras con objetivos en la ejecucion A (R22-resultados.json), solo para la seccion de atribucion.
A_EMISORAS = ["COST", "KO", "PM", "AMZN", "TSLA", "CVX", "CAT", "GEV", "RTX", "LLY", "MRK", "META", "JPM", "MA",
              "BAC", "MS", "GS", "WFC", "AAPL", "AVGO", "MU", "AMD", "PLTR", "CSCO", "LRCX", "DELL", "PANW", "ANET", "TXN"]

_ultimo = [0.0]
def get(url):
    espera = 0.15 - (time.time() - _ultimo[0])
    if espera > 0: time.sleep(espera)
    for intento in range(5):
        _ultimo[0] = time.time()
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                b = r.read()
                if r.headers.get("Content-Encoding") == "gzip": b = gzip.decompress(b)
                return b
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and intento < 4: time.sleep(2 * (intento + 1)); continue
            raise

def cache_json(nombre, url):
    ruta = os.path.join(DATOS, nombre)
    if os.path.exists(ruta):
        return json.load(open(ruta))
    d = json.loads(get(url)); json.dump(d, open(ruta, "w")); return d

def cik(ticker):
    t = ticker.replace(".", "-").upper()
    ruta = os.path.join(DATOS, f"efts_{t}.json")
    for intento in range(6):
        q = t if intento < 2 else t.lower()  # respaldo: la consulta en minusculas
        d = cache_json(f"efts_{t}.json", f"https://efts.sec.gov/LATEST/search-index?keysTyped={q}")
        if "hits" in d: break
        os.remove(ruta); time.sleep(2)  # error del buscador (p. ej. 'GE' devolvia ConnectionError)
    for h in d["hits"]["hits"]:
        tks = [x.strip().upper() for x in h["_source"].get("tickers", "").split(",")]
        if t in tks: return int(h["_id"])
    raise RuntimeError(f"sin CIK para {ticker}")

def F(s): return date.fromisoformat(s)

def ultimos_por_periodo(hechos):
    """{(inicio, fin): valor} con el hecho de 'filed' mas reciente (desempate: accn)."""
    m = {}
    for h in hechos:
        if "start" not in h: continue
        k = (F(h["start"]), F(h["end"]))
        clave = (h.get("filed", ""), h.get("accn", ""))
        if k not in m or clave > m[k][0]: m[k] = (clave, float(h["val"]), h.get("form", ""))
    return {k: (v[1], v[2]) for k, v in m.items()}

def series(facts, etiquetas):
    usg = facts.get("facts", {}).get("us-gaap", {})
    out = []
    for e in etiquetas:
        if e in usg and "USD" in usg[e]["units"]:
            out.append((e, ultimos_por_periodo(usg[e]["units"]["USD"])))
    return out

def dur(k): return (k[1] - k[0]).days

def trimestres(periodos, con_q4):
    """{fin: valor} de trimestres directos (80-100 dias) y, opcional, 4T reconstruidos."""
    q = {k[1]: v[0] for k, v in periodos.items() if 80 <= dur(k) <= 100}
    q4 = {}
    if con_q4:
        anuales = {k: v for k, v in periodos.items() if 350 <= dur(k) <= 380 and v[1].startswith("10-K")}
        nueve = {k: v[0] for k, v in periodos.items() if 245 <= dur(k) <= 290}  # 36-40 semanas (COST: 12+12+12)
        for (ini, fin), (va, _) in anuales.items():
            cands = [(k, v) for k, v in nueve.items() if k[0] == ini and 75 <= (fin - k[1]).days <= 125]  # 4T de 12-17 semanas
            if not cands: continue
            k9, v9 = max(cands, key=lambda x: x[0][1])
            if any(abs((fin - f).days) <= 5 for f in q): continue  # ya hay 4T directo
            q4[fin] = va - v9
    return q, q4

def combinar(lista, con_q4):
    """Une etiquetas por fecha de fin: manda la de mas trimestres; las demas rellenan."""
    hechas = []
    for e, per in lista:
        q, q4 = trimestres(per, con_q4)
        hechas.append((len(q), e, q, q4))
    hechas.sort(key=lambda x: -x[0])
    res, origen = {}, {}
    for _, e, q, q4 in hechas:
        for f, v in list(q.items()) + list(q4.items()):
            if not any(abs((f - g).days) <= 5 for g in res):
                res[f] = v; origen[f] = (e, "4T" if f in q4 and f not in q else "Q")
    return res, origen, [x[1] for x in hechas]

def una_etiqueta(lista, con_q4):
    """Emulacion de la regla de A: una sola etiqueta, la de mas trimestres, sin rellenar."""
    mejor = max(lista, key=lambda x: len(trimestres(x[1], con_q4)[0]), default=None)
    return combinar([mejor] if mejor else [], con_q4)

ETIQ_A = ["IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
          "IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments",
          "IncomeLossFromContinuingOperationsBeforeIncomeTaxesDomestic"]  # lista de A, solo para la atribucion

def etr_serie(facts, con_q4, emular_a=False):
    tax, otax, _ = combinar(series(facts, ETIQ_TAX), con_q4)
    if emular_a:
        pre, opre, orden = una_etiqueta(series(facts, ETIQ_A), con_q4)
    else:
        pre, opre, orden = combinar(series(facts, ETIQ_PRETAX), con_q4)
    pts = []
    for f, p in pre.items():
        t = next((tax[g] for g in tax if abs((g - f).days) <= 5), None)
        if t is None: continue
        es4 = opre[f][1] == "4T" or next(otax[g][1] for g in tax if abs((g - f).days) <= 5) == "4T"
        valido = p > 0 and 0.0 <= t / p <= 0.60
        pts.append({"fin": f, "etr": t / p if p else None, "valido": valido, "q4": es4})
    pts.sort(key=lambda x: x["fin"])
    return pts, (orden[0] if orden else None)

def pronosticos(pts):
    val = [p for p in pts if p["valido"]]
    out = []
    for p in val:
        if not (INI_OBJ <= p["fin"] <= FIN_OBJ): continue
        h4 = [x["etr"] for x in val if p["fin"] - timedelta(days=460) <= x["fin"] < p["fin"]]
        if len(h4) < 4: continue
        h8 = [x["etr"] for x in val if p["fin"] - timedelta(days=830) <= x["fin"] < p["fin"]]
        r = {"fin": p["fin"].isoformat(), "real": p["etr"], "q4": p["q4"],
             "ultimo": h4[-1], "mediana4": statistics.median(h4[-4:]),
             "media4": sum(h4[-4:]) / 4, "fijo21": 0.21,
             "mediana8": statistics.median(h8[-8:]) if len(h8) >= 8 else None}
        out.append(r)
    return out

def p_signos(n_gana, n):
    k = min(n_gana, n - n_gana)
    cola = sum(math.comb(n, i) for i in range(k + 1))
    return min(1.0, 2 * cola / 2 ** n)

def analizar(obs):
    random.seed(SEMILLA)
    reglas = ["ultimo", "mediana4", "media4", "mediana8", "fijo21"]
    res = {"n_objetivos": len(obs), "n_emisoras": len({o["tk"] for o in obs}), "reglas": {}}
    for r in reglas:
        sub = [o for o in obs if o[r] is not None]
        if not sub: res["reglas"][r] = {"n": 0}; continue
        ea = [100 * abs(o[r] - o["real"]) for o in sub]
        upa = [100 * abs(o[r] - o["real"]) / (1 - o["real"]) for o in sub]
        res["reglas"][r] = {"n": len(sub), "MAE_pp": round(sum(ea) / len(ea), 4),
                            "mediana_EA_pp": round(statistics.median(ea), 4),
                            "error_UPA_medio_pct": round(sum(upa) / len(upa), 4),
                            "error_UPA_mediano_pct": round(statistics.median(upa), 4)}
    s8 = [o for o in obs if o["mediana8"] is not None]
    res["submuestra_mediana8"] = {"n": 0} if not s8 else {"n": len(s8), **{r: round(sum(100 * abs(o[r] - o["real"]) for o in s8) / len(s8), 4) for r in reglas}}
    eu = [100 * abs(o["ultimo"] - o["real"]) for o in obs]
    em = [100 * abs(o["mediana4"] - o["real"]) for o in obs]
    gana_m = sum(1 for a, b in zip(eu, em) if b < a); gana_u = sum(1 for a, b in zip(eu, em) if a < b)
    n = gana_m + gana_u
    res["signos"] = {"gana_mediana4": gana_m, "gana_ultimo": gana_u, "empates": len(obs) - n,
                     "p_dos_colas": p_signos(gana_m, n)}
    d = [a - b for a, b in zip(eu, em)]
    N = len(d); bs = []
    for _ in range(NBOOT):
        bs.append(sum(d[random.randrange(N)] for _ in range(N)) / N)
    bs.sort()
    res["dif_MAE_ultimo_menos_mediana4"] = {"punto": round(sum(d) / N, 4),
        "IC95_iid": [round(bs[int(0.025 * NBOOT)], 4), round(bs[int(0.975 * NBOOT) - 1], 4)]}
    # bootstrap por emisora (conglomerados), robustez
    por = {}
    for o, x in zip(obs, d): por.setdefault(o["tk"], []).append(x)
    g = list(por.values()); bc = []
    for _ in range(2000):
        m = [g[random.randrange(len(g))] for _ in range(len(g))]
        bc.append(sum(sum(x) for x in m) / sum(len(x) for x in m))
    bc.sort()
    res["dif_MAE_ultimo_menos_mediana4"]["IC95_conglomerado_emisora"] = [round(bc[50], 4), round(bc[1949], 4)]
    mae_u, mae_m = res["reglas"]["ultimo"]["MAE_pp"], res["reglas"]["mediana4"]["MAE_pp"]
    h1 = mae_m < mae_u and res["signos"]["p_dos_colas"] < 0.05 and gana_m > gana_u
    h2 = mae_m <= 3.0
    res["H1"] = h1; res["H2"] = h2
    res["veredicto"] = (f"H1 {'se cumple' if h1 else 'no se cumple'}: MAE mediana-4 {mae_m:.3f} pp vs ultimo "
                        f"{mae_u:.3f} pp, signos p={res['signos']['p_dos_colas']:.2e}. "
                        f"H2 {'se cumple' if h2 else 'no se cumple'}: MAE mediana-4 {mae_m:.3f} pp vs umbral 3.0 pp.")
    return res

def main():
    tks = [r["ticker"] for r in csv.DictReader(open(os.path.join(REPO, "empresas", "universo.csv")))
           if r["mercado"] == "US" and r["ticker"] not in ("BRK-B", "SPCX")]
    salida = {"fuente": "SEC companyfacts (data.sec.gov) + efts entity search", "ua": UA,
              "universo": tks, "emisoras": {}}
    obs = {False: [], True: []}; emu = []
    for tk in tks:
        c = cik(tk)
        ciks = [c] + PREDECESORAS.get(tk, [])
        facts = {"facts": {"us-gaap": {}}}
        for ci in ciks:  # une los hechos de la emisora y de su predecesora (si la hay)
            fj = cache_json(f"companyfacts_CIK{ci:010d}.json", f"https://data.sec.gov/api/xbrl/companyfacts/CIK{ci:010d}.json")
            for con, v in fj.get("facts", {}).get("us-gaap", {}).items():
                dst = facts["facts"]["us-gaap"].setdefault(con, {"units": {}})
                for u, lst in v["units"].items(): dst["units"].setdefault(u, []).extend(lst)
        info = {"cik": ciks}
        for q4 in (False, True):
            pts, etq = etr_serie(facts, q4)
            pr = pronosticos(pts)
            for o in pr: o["tk"] = tk
            obs[q4] += pr
            info["con4T" if q4 else "sin4T"] = {"trimestres": len(pts), "validos": sum(p["valido"] for p in pts),
                                                "objetivos": len(pr), "etiqueta_pretax_con_mas_trimestres": etq}
        pts, _ = etr_serie(facts, False, emular_a=True)
        pr = pronosticos(pts)
        for o in pr: o["tk"] = tk
        info["emulacion_A_objetivos"] = len(pr)
        emu += pr
        salida["emisoras"][tk] = info
        print(tk, c, info["sin4T"]["objetivos"], info["con4T"]["objetivos"], info["sin4T"]["etiqueta_pretax_con_mas_trimestres"], file=sys.stderr)
    salida["sin_4T_comparable_con_A"] = analizar(obs[False])
    salida["con_4T_reconstruido"] = analizar(obs[True])
    # Atribucion de diferencias con A (no son parte del veredicto)
    A29 = set(A_EMISORAS)
    salida["atribucion"] = {
        "B_restringido_a_las_29_emisoras_de_A": analizar([o for o in obs[False] if o["tk"] in A29]),
        "B_solo_14_emisoras_que_A_pierde": analizar([o for o in obs[False] if o["tk"] not in A29]),
        "emulacion_regla_etiqueta_de_A_29_emisoras": analizar([o for o in emu if o["tk"] in A29]),
    }
    solo4 = [o for o in obs[True] if o["q4"]]
    salida["con_4T_reconstruido"]["n_objetivos_4T"] = len(solo4)
    if solo4:
        salida["con_4T_reconstruido"]["MAE_en_objetivos_4T"] = {r: round(sum(100 * abs(o[r] - o["real"]) for o in solo4) / len(solo4), 4)
                                                               for r in ("ultimo", "mediana4", "media4", "fijo21")}
    json.dump(salida, open(os.path.join(RAIZ, "resultados.json"), "w"), indent=1, ensure_ascii=False, default=str)
    for k in ("sin_4T_comparable_con_A", "con_4T_reconstruido"):
        r = salida[k]; print(k, r["n_objetivos"], r["n_emisoras"], json.dumps(r["reglas"]), r["signos"], r["dif_MAE_ultimo_menos_mediana4"], r["veredicto"])

if __name__ == "__main__":
    main()
