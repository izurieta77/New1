#!/usr/bin/env python3
"""Redimensionamiento GBM a 10,000 MXN (gestor de riesgo, 29-sep-2026; salida en salida_redimensionamiento_2026_09_29.txt): reutiliza el motor de arena/modelos/cartera_inicial_simulacion.py
(mismo corte de datos 25-sep-2026, misma semilla, cache forzada) con capital 10,000 y titulos enteros."""
import sys, time, json
from datetime import date
from pathlib import Path
import numpy as np
RAIZ = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(RAIZ))
from herramientas import datos as hd
_orig = hd.descargar
def _desc(url, encabezados=None, timeout=hd.TIMEOUT_S, reintentos=hd.REINTENTOS, cache_horas=None):
    return _orig(url, encabezados, timeout, reintentos, cache_horas=10**6)  # cache del 25-sep, sin red
hd.descargar = _desc
sys.path.insert(0, str(RAIZ / "arena" / "modelos"))
import cartera_inicial_simulacion as sim
sim.descargar = _desc
CAP = 10_000.0
sim.CAPITAL = CAP
CAMINOS = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
SEM = 20260925
t0 = time.time()
D = sim.cargar_datos()
f = D["fechas"]; N = len(f)
cal = sim.calendario_temporada(); T = len(cal)
print(f"Datos cargados de cache ({time.time()-t0:.0f}s). Corte {sim.CORTE}. T={T} dias. fx_hoy(25-sep)={D['fx_hoy']:.4f}")
B = {"fechas": f, "rfx": np.full(N, np.nan), "x": {}, "nivel": {}, "sma": {}, "r01": {}, "fin_mes_niveles": {}}
B["rfx"][1:] = D["FX"][1:] / D["FX"][:-1] - 1
niveles = {"SPX": D["SPY"], "NDX": D["QQQ"]}; niveles.update({s: D[s] for s in sim.SECTORES})
for k, niv in niveles.items():
    B["nivel"][k] = niv; B["x"][k] = sim.excesos(niv, D["RF"]); B["sma"][k] = sim.estado_sma(niv)
for k in ("SPX", "NDX"):
    B["r01"][k] = sim.estado_r01(niveles[k], f)
    fm = [i for i in range(N - 1) if f[i + 1].month != f[i].month]
    B["fin_mes_niveles"][k] = niveles[k][fm]
B["vix"] = D["^VIX"]; B["r_real"] = {}
for k, tk in (("SPX3", "SPXL"), ("NDX3", "TQQQ")):
    rr = np.full(N, np.nan); rr[1:] = D[tk][1:] / D[tk][:-1] - 1; B["r_real"][k] = rr
B["regimen_hoy"] = B["sma"]["SPX"] & (B["vix"] < 20)
B["regimen"] = np.zeros(N, bool); B["regimen"][1:] = B["sma"]["SPX"][:-1] & (B["vix"][:-1] < 20)
B["i_min"] = next(i for i in range(N) if not np.isnan(D["QQQ"][i]) and not np.isnan(D["XLK"][i])) + 252
B["rf_hoy"] = D["RF_hoy"]
dias_temp = (cal[-1] - date(2026, 9, 25)).days
B["cash_d"] = (1 + sim.CETES_28 * dias_temp / 360) ** (1 / T) - 1
B["arrastre"] = {"SPX": 0.0214, "NDX": 0.0277}
mom121 = {s_: D[s_][-22] / D[s_][-253] - 1 for s_ in sim.SECTORES}
B["top_sectores_hoy"] = tuple(sorted(sim.SECTORES, key=lambda s_: -mom121[s_])[:2])
print("top sectores 12-1:", B["top_sectores_hoy"])   # de salida_cartera_inicial.txt (no se usan: sin apalancados)

# ---- precios de referencia (MXN por titulo)
PX_28 = {"SPYM": 1609.0, "QQQM": 5395.0}     # referencia del orquestador / semaforo 28-sep 08:45
PX_29 = {"SPYM": 89.94 * 18.053, "QQQM": 303.83 * 18.053}  # NYSE cierre 29-sep x MXN=X 23:25 UTC (Yahoo)
def w(px, tk, n): return n * px[tk] / CAP
def cand(px):
    c = {}
    c["a 2 SPYM + 1 QQQM"] = [("SPX1", "SPYM", 2), ("NDX1", "QQQM", 1)]
    c["b 3 SPYM"] = [("SPX1", "SPYM", 3)]
    c["c 5 SPYM (viola 60%)"] = [("SPX1", "SPYM", 5)]
    c["d 4 SPYM (viola 60% por 4pp)"] = [("SPX1", "SPYM", 4)]
    c["e1 1 QQQM solo"] = [("NDX1", "QQQM", 1)]
    c["e2 1 SPYM + 1 QQQM"] = [("SPX1", "SPYM", 1), ("NDX1", "QQQM", 1)]
    out = {}
    for k, ls in c.items():
        out[k] = {"lineas": [{"activo": a, "w": w(px, tk, n), "titulos": n} for a, tk, n in ls], "cb": True}
    return out
cands = cand(PX_28)
# referencia: A original a 20k (precios 25-sep como en la corrida original)
cands["REF A 7 SPYM+1 QQQM @20k"] = {"lineas": [{"activo": "SPX1", "w": 7*1608.0/20000, "titulos": 7},
                                                {"activo": "NDX1", "w": 1*5428.6/20000, "titulos": 1}], "cb": True}
rivales = {"R1 beta 1 S&P (100%)": {"lineas": [{"activo": "SPX1", "w": 1.0}], "cb": False},
           "R2 mixta 50% S&P + 50% CETES": {"lineas": [{"activo": "SPX1", "w": 0.5}], "cb": False},
           "R3 agresiva 50% TQQQ + 50% QQQ": {"lineas": [{"activo": "NDX3", "w": 0.5}, {"activo": "NDX1", "w": 0.5}], "cb": False}}
campos = {"F1 {R1,R2}": ["R1 beta 1 S&P (100%)", "R2 mixta 50% S&P + 50% CETES"]}

# ---- beta (MXN y USD) de QQQ vs SPY, 2011-09-26 a 2026-09-25
i0 = f.index(date(2011, 9, 26))
def rets(a): return a[1:] / a[:-1] - 1
spy_usd, qqq_usd, fx = D["SPY"][i0:], D["QQQ"][i0:], D["FX"][i0:]
r_spy_m, r_qqq_m = rets(spy_usd * fx), rets(qqq_usd * fx)
r_spy_u, r_qqq_u = rets(spy_usd), rets(qqq_usd)
ok = ~np.isnan(r_spy_m) & ~np.isnan(r_qqq_m)
beta_m = np.cov(r_qqq_m[ok], r_spy_m[ok])[0, 1] / np.var(r_spy_m[ok])
beta_u = np.cov(r_qqq_u[ok], r_spy_u[ok])[0, 1] / np.var(r_spy_u[ok])
vol_spy_m = np.std(r_spy_m[ok]) * np.sqrt(252); vol_qqq_m = np.std(r_qqq_m[ok]) * np.sqrt(252)
print(f"\nBeta QQQ vs SPY 2011-2026: en MXN {beta_m:.2f}, en USD {beta_u:.2f}. Vol anual en MXN: SPY {vol_spy_m:.1%}, QQQ {vol_qqq_m:.1%}")

# ---- pesos, beta de cartera, orden minima, concentracion
print("\n## Carteras a 10,000 MXN (precios de referencia 28-sep: SPYM 1,609 / QQQM 5,395)")
print(f"{'cartera':34s} {'inv%':>6s} {'SPYM%':>6s} {'QQQM%':>6s} {'beta_SP_MXN':>11s} {'MXN inv':>8s} {'comis':>6s} {'efectivo':>8s} {'lineas<5000':>11s} {'max_pos>60%':>11s} {'vol_MXN':>8s}")
for k, e in cands.items():
    if k.startswith("REF"): continue
    ws = {l["activo"]: l["w"] for l in e["lineas"]}
    inv = sum(ws.values()); wsp = ws.get("SPX1", 0); wq = ws.get("NDX1", 0)
    beta = wsp * 1.0 + wq * beta_m
    mxn = inv * CAP; com = mxn * 0.0029
    lineas_chicas = [round(l["w"]*CAP) for l in e["lineas"] if l["w"]*CAP < 5000]
    maxpos = max(ws.values())
    vol = np.sqrt((wsp*vol_spy_m)**2 + (wq*vol_qqq_m)**2 + 2*wsp*wq*vol_spy_m*vol_qqq_m*np.corrcoef(r_spy_m[ok], r_qqq_m[ok])[0,1])
    print(f"{k:34s} {inv:6.1%} {wsp:6.1%} {wq:6.1%} {beta:11.2f} {mxn:8.0f} {com:6.0f} {CAP-mxn-com:8.0f} {str(lineas_chicas):>11s} {('SI '+f'{maxpos:.1%}') if maxpos>0.6 else 'no':>11s} {vol:8.1%}")
print("Con precios del 29-sep (NYSE x MXN=X 18.053): SPYM %.1f, QQQM %.1f MXN -> a: inv %.1f%%, QQQM %.1f%%; d: %.1f%%; b: %.1f%%; lim SPYM x1.003 %.1f, tope +2%% %.1f; lim QQQM x1.003 %.1f, tope +2%% %.1f" % (
    PX_29["SPYM"], PX_29["QQQM"], (2*PX_29["SPYM"]+PX_29["QQQM"])/CAP*100, PX_29["QQQM"]/CAP*100, 4*PX_29["SPYM"]/CAP*100, 3*PX_29["SPYM"]/CAP*100,
    PX_29["SPYM"]*1.003, PX_29["SPYM"]*1.02, PX_29["QQQM"]*1.003, PX_29["QQQM"]*1.02))

# ---- escenarios de cola (datos reales, en MXN)
def idx(d): return f.index(d)
def ret_mxn(tk, d0, d1):
    return (D[tk][idx(d1)] * D["FX"][idx(d1)]) / (D[tk][idx(d0)] * D["FX"][idx(d0)]) - 1
esc = {"16-mar-2020 (dia)": (date(2020, 3, 13), date(2020, 3, 16)),
       "2-8 abr 2025 (semana)": (date(2025, 4, 1), date(2025, 4, 8))}
print("\n## Escenarios de cola (rendimientos reales en MXN: SPY/QQQ x DEXMXUS)")
for nom, (d0, d1) in esc.items():
    rs, rq = ret_mxn("SPY", d0, d1), ret_mxn("QQQ", d0, d1)
    rfx = D["FX"][idx(d1)] / D["FX"][idx(d0)] - 1
    print(f"  {nom}: SPY {rs:+.2%}, QQQ {rq:+.2%} en MXN (USD/MXN {rfx:+.2%})")
    for k, e in cands.items():
        ws = {l["activo"]: l["w"] for l in e["lineas"]}
        eff = ws.get("SPX1", 0) * rs + ws.get("NDX1", 0) * rq
        cap = 20000 if k.startswith("REF") else CAP
        print(f"     {k:34s} {eff:+.2%} = {eff*cap:+,.0f} MXN")
print("  Peso +20% (USD/MXN x0.80, acciones sin cambio): perdida = % invertido x 20%")
for k, e in cands.items():
    inv = sum(l["w"] for l in e["lineas"]); cap = 20000 if k.startswith("REF") else CAP
    print(f"     {k:34s} {-inv*0.2:+.2%} = {-inv*0.2*cap:+,.0f} MXN")
# S&P -20% en MXN (estres usado en la decision del 25-sep)
print("  S&P -20% en MXN (QQQ x beta MXN): ")
for k, e in cands.items():
    ws = {l["activo"]: l["w"] for l in e["lineas"]}; cap = 20000 if k.startswith("REF") else CAP
    eff = -0.2 * (ws.get("SPX1", 0) + beta_m * ws.get("NDX1", 0))
    print(f"     {k:34s} {eff:+.1%} = {eff*cap:+,.0f} MXN; -35% de la cuenta = {0.35*cap:,.0f} MXN; tope provisional 5,000")

# ---- simulacion
def resumen(res, titulo):
    print(f"\n### {titulo}")
    print(f"{'cartera':34s} {'mediana':>8s} {'p10':>7s} {'p90':>7s} {'P-12%':>6s} {'P-20%':>6s} {'P-28%':>6s} {'P-35%':>6s} {'P<0':>5s} {'F1 1o':>6s} {'>R1':>5s} {'>R2':>5s} {'dia-5%':>6s}")
    for k, r in res.items():
        if k.startswith("_"): continue
        print(f"{k:34s} {r['med']:+8.1%} {r['p10']:+7.1%} {r['p90']:+7.1%} {r['p12']:6.1%} {r['p20']:6.1%} {r['p28']:6.1%} {r['p35']:6.1%} {r['pneg']:5.0%} {r['F1 {R1,R2}']:6.1%} {r['vs R1']:5.0%} {r['vs R2']:5.0%} {r['fdia']:6.1%}")
resultados = {}
t1 = time.time()
D1 = sim.construir_bootstrap(B, T, CAMINOS, SEM, conservador=False, condicionar=True, cal=cal)
resultados["M1"] = sim.evaluar(cands, rivales, campos, D1, SEM); del D1
resumen(resultados["M1"], f"M1 bootstrap 2011-2026, regimen de hoy, deriva historica ({CAMINOS} caminos)")
D2 = sim.construir_bootstrap(B, T, CAMINOS, SEM + 1, conservador=True, condicionar=True, cal=cal)
resultados["M2"] = sim.evaluar(cands, rivales, campos, D2, SEM + 1); del D2
resumen(resultados["M2"], "M2 bootstrap deriva conservadora (prima 5%, peso sin deriva)")
D3 = sim.construir_ventanas(B, T)
resultados["M3"] = sim.evaluar(cands, rivales, campos, D3, SEM + 2)
resumen(resultados["M3"], f"M3 ventanas moviles 1999-2026 ({D3['P']} ventanas)")
D3c = sim.construir_ventanas(B, T, solo_regimen=True)
resultados["M3c"] = sim.evaluar(cands, rivales, campos, D3c, SEM + 3)
resumen(resultados["M3c"], f"M3c ventanas en el regimen de hoy ({D3c['P']} ventanas)")
print(f"\nTiempo simulacion: {time.time()-t1:.0f}s")
print("\n## Resumen P-12% | P-20% (M1 | M2 | M3 | M3c) y mediana M3")
for k in cands:
    print(f"{k:34s} P-12%: " + " | ".join(f"{resultados[m][k]['p12']:.1%}" for m in ("M1","M2","M3","M3c")) +
          "   P-20%: " + " | ".join(f"{resultados[m][k]['p20']:.1%}" for m in ("M1","M2","M3","M3c")) +
          f"   med M3 {resultados['M3'][k]['med']:+.1%}  F1 1o M3 {resultados['M3'][k]['F1 {R1,R2}']:.0%}")
json.dump({m: {k: {kk: (float(vv) if not isinstance(vv, np.ndarray) else None) for kk, vv in r.items() if not isinstance(vv, np.ndarray)} for k, r in res.items() if not k.startswith("_")} for m, res in resultados.items()},
          open(Path(__file__).parent / "resultados_redimensionamiento_2026_09_29.json", "w"), indent=1)
