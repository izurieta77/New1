#!/usr/bin/env python3
"""Ejercicio de la ficha 2026-10-18 (ETF spot de ether: ETHA sin staking vs. ETHB con staking).

Entradas:
  argv[1] = JSON de historial diario de validatorqueue.com (variable `historical_data`
            incrustada en el HTML; fuente de datos: beaconcha.in). Se extrae con:
            re.search(r'const historical_data = (\\[.*?\\]);', html, re.S)
Cifras fijas (SEC EDGAR, CIK 0002099103, grado A):
  - 10-Q al 30-jun-2026 (acc. 0001437749-26-027003): staking income 2T 1,194,785 USD;
    sponsor's fee incl. Sponsor's Staking Portion 2T 419,914 USD; ratio de gastos antes
    de exención 0.30% anualizado; NII 0.69% y gastos tras exención 0.17% (anualizados);
    250,585 ETH stakeados = 86.9% de la posición; 22,400,000 acciones; NAV 20.51.
  - Prospecto 424B3 del 11-mar-2026 (acc. 0001437749-26-007771): 18% de la recompensa
    bruta va al patrocinador + agente (Coinbase Prime); stakea 70-95%; comisión 0.25%,
    exención a 0.12% por 12 meses desde el 12-mar-2026 sobre los primeros 2.5 mil M USD.
Uso: python3 -I 2026-10-18-etf-ether-staking.py vq_hist.json
"""
import json
import statistics as st
import sys
from datetime import date

H = json.load(open(sys.argv[1]))
H = [r for r in H if r.get("date")]
by = {r["date"]: r for r in H}
hoy = H[-1]

# 1) Cola de salida: espera = cola / (256 ETH por época × 225 épocas por día)
EPOCAS_DIA = 86400 / (32 * 12)          # 225
CHURN = 256                              # ETH por época (tope de EIP-7251)
esp = hoy["exit_queue"] / (CHURN * EPOCAS_DIA)
print(f"[1] {hoy['date']}: cola de salida {hoy['exit_queue']:,} ETH -> espera {esp:.2f} d "
      f"(sitio: {hoy['exit_wait']} d); entrada {hoy['entry_queue']:,} ETH ({hoy['entry_wait']} d); "
      f"APR {hoy['apr']}%; stakeado {hoy['staked_amount']:,} ETH")
assert abs(esp - hoy["exit_wait"]) < 0.02, "la espera no cuadra con la cola"

# 2) Rendimiento neto teórico (pp/año) con el APR de hoy
apr = hoy["apr"] / 100
print("[2] Rendimiento neto anual sobre el NAV (APR de hoy):")
for f in (0.70, 0.869, 0.95):
    for fee, et in ((0.0012, "exención 0.12%"), (0.0025, "sin exención 0.25%")):
        net = apr * f * (1 - 0.18) - fee
        print(f"    stake {f:.1%}, {et}: ETHB {net:.3%} | ETHA -0.250% | ventaja ETHB {net + 0.0025:.3%}")

# 3) Rendimiento realizado en el 2T-2026 (10-Q), dos métodos
ingreso, fee_bruto, ratio_fee = 1_194_785, 419_914, 0.0030
dias = (date(2026, 6, 30) - date(2026, 3, 31)).days      # 91
an_prom = fee_bruto / (ratio_fee * dias / 365)           # activo neto medio implícito
m1 = ingreso / an_prom * 365 / dias
m2 = 0.0069 + 0.0017                                     # NII + gastos tras exención
print(f"[3] Activo neto medio implícito 2T: {an_prom/1e6:,.1f} M USD; ingreso por staking "
      f"anualizado / activo neto: método 1 {m1:.3%}, método 2 {m2:.3%}")
apr_2t = st.mean(by[d]["apr"] for d in by if "2026-04-01" <= d <= "2026-06-30" and by[d]["apr"])
ent_2t = st.mean(by[d]["entry_wait"] for d in by if "2026-03-12" <= d <= "2026-06-30")
teor = apr_2t / 100 * 0.869
print(f"    APR medio de la red en el 2T: {apr_2t:.2f}%; teórico con 86.9% stakeado: {teor:.3%}; "
      f"realizado/teórico = {m1/teor:.0%}; espera media de entrada 12-mar->30-jun: {ent_2t:.1f} d")

# 4) Liquidez: días para convertir ETH stakeado en ETH retirable hoy
barrido = 7.2  # días, sitio, 18-oct-2026
total = esp + 27 / 24 + barrido
mx = max(H, key=lambda r: r["exit_wait"])
print(f"[4] Desstakear hoy: {esp:.1f} d de cola + 1.1 d de retraso + {barrido} d de barrido = {total:.1f} d. "
      f"Colchón sin stakear al 30-jun: {1-0.869:.1%}. Máximo histórico de espera de salida: "
      f"{mx['exit_wait']} d ({mx['date']}, {mx['exit_queue']:,} ETH)")

# 5) Tasa base para el pronóstico: ¿la cola de salida a t+29 queda debajo de la de t?
ds = sorted(by)
def tasa(filtro):
    n = k = 0
    for i, d in enumerate(ds):
        j = i + 29
        if j >= len(ds):
            break
        a, b = by[d]["exit_queue"], by[ds[j]]["exit_queue"]
        if filtro(a):
            n += 1
            k += b < a
    return k, n
for nom, fl in (("todas", lambda a: True), ("cola > 500k", lambda a: a > 500_000),
                ("cola > 800k", lambda a: a > 800_000)):
    k, n = tasa(fl)
    print(f"[5] t+29 < t ({nom}): {k}/{n} = {k/n:.1%}" if n else f"[5] {nom}: sin casos")
ult30 = [by[d]["exit_queue"] for d in ds[-30:]]
print(f"    últimos 30 días: mín {min(ult30):,}, máx {max(ult30):,}, hace 29 d {by[ds[-30]]['exit_queue']:,}")
