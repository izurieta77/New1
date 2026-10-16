#!/usr/bin/env python3
"""Ficha 16-oct-2026 (Doctorado fiscal D9): umbrales de la LFPIORPI (texto vigente, última reforma DOF 16-07-2025)
en pesos con la UMA 2026 (diaria 117.31, vigente del 1-feb-2026 al 31-ene-2027; fuente secundaria, se comprueba
que es la UMA 2025 de 113.14 actualizada 3.69%). Corre con python3 -I; las aserciones son la comprobación."""
UMA_2025, UMA_2026 = 113.14, 117.31
assert abs(UMA_2025 * 1.0369 - UMA_2026) < 0.01   # 117.3149 -> 117.31

UMBRALES = {  # (artículo y fracción, veces UMA, qué dispara)
    "17 V construcción/desarrollo con compraventa de inmuebles (aviso)": 8025,
    "17 V Bis recursos para desarrollo inmobiliario (aviso)": 8025,
    "17 VI metales y piedras preciosas, joyas, relojes (identificación)": 805,
    "17 XV arrendamiento de inmuebles, mensual (identificación: más de)": 1605,
    "17 XV arrendamiento de inmuebles, mensual (aviso)": 3210,
    "17 XVI activos virtuales: operación por cliente (aviso)": 210,
    "17 XVI activos virtuales: comisión cobrada (aviso)": 4,
    "32 I efectivo prohibido: derechos reales sobre inmuebles": 8025,
    "32 II efectivo prohibido: vehículos": 3210,
    "32 III efectivo prohibido: relojes, joyería, metales, arte": 3210,
}
pesos = {k: v * UMA_2026 for k, v in UMBRALES.items()}
for k, p in pesos.items():
    print(f"{k:70s} {UMBRALES[k]:>5} UMA = {p:>13,.2f} MXN")
assert round(pesos["17 XVI activos virtuales: operación por cliente (aviso)"], 2) == 24635.10
assert round(pesos["32 II efectivo prohibido: vehículos"], 2) == 376565.10
assert round(pesos["32 I efectivo prohibido: derechos reales sobre inmuebles"], 2) == 941412.75
# Caso: la cuenta real de Binance del dueño (~5,000 MXN) queda muy debajo del umbral de aviso de 24,635.10 por operación.
assert 5000 < pesos["17 XVI activos virtuales: operación por cliente (aviso)"]
print("Comprobaciones OK")
