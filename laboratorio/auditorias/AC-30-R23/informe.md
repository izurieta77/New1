# AC-30 · Ejecución B independiente de R23 (U0 contra U13.5, UPRO real y deriva del S&P)

Auditor-de-replicas, 2026-10-31. Código propio (`ac30.py`, biblioteca estándar; sin leer ni importar `R16.py`, `R18.py`, `R21.py` ni `R23.py`). Reglas tomadas de los pre-registros `.md` de R16/R18/R20/R21/R23. Salida en `salida.txt`, cifras en `resultados.json`, sensibilidades en `variantes.txt`. Nada se descargó.

## Datos (las cachés declaradas por el pre-registro)
- `R16-datos/series.json` sha256 `42339a50…466b` (^GSPC, ^SP500TR, ^VIX, DTB3); `R12-datos/series.json` `44d25f4e…d466` (^NDX); `R20-datos/series.json` `94226cbe…ee65` (UPRO adjclose).
- Muestra: 9,065 días de rendimiento, 1990-10-17 a 2026-10-16 (igual que A). rf medio 2.627%; CAGR del S&P TR 11.61%. Filtro V0 encendido 74.7% de los días.
- Fuera de muestra: 4,353 días, 2009-06-29 a 2026-10-16. El pre-registro decía "a 2026-10-23", pero la caché de R16 (señal) termina el 16-oct; A también cortó ahí. Control: brecha aritmética UPRO real − sintético sin brecha en esa ventana = −1.593 pp/año (R20-A: −1.592).

## Convenciones propias de B (donde el pre-registro deja libertad)
- Filtro: estado al cierre de t−2 aplicado al rendimiento de t; arranque con la condición de entrada en el primer día con SMA200; DTB3 con último dato hacia adelante.
- Rebalanceo al cierre del último día hábil del mes (el primer rendimiento del mes se gana a pesos objetivo).
- CAGR con años calendario (días/365.25). Ventana de toque: 126 puntos consecutivos de la curva (t..t+125).

## Tabla clave (B; entre paréntesis A de `R23-resultados.json`)
| Bloque | Mezcla | CAGR % | MDD % | P(−12%,126d) % | P(−20%,126d) % |
|---|---|---|---|---|---|
| 1990-2026 sint.+brecha | U0-efectivo | 11.244 (11.253) | −53.60 (−53.60) | 21.73 (21.87) | 7.97 (8.04) |
| | U0-SPYM | 12.347 (12.357) | −58.33 (−58.33) | 25.31 (25.46) | 9.31 (9.37) |
| | U13.5 | 13.073 (13.083) | −57.00 (−57.00) | 30.23 (30.43) | 12.48 (12.60) |
| μ = 5% | U13.5 − U0-ef | −0.230 (−0.232) | | +11.04 (+11.14) | +4.78 |
| **μ = 7%** | **U13.5 − U0-ef** | **+0.380 (+0.379)** | | **+10.05 (+10.14)** | +4.66 |
| μ = 9% | U13.5 − U0-ef | +1.002 (+1.001) | | +10.33 (+10.42) | +4.62 |
| μ = 11% | U13.5 − U0-ef | +1.635 (+1.634) | | +9.44 (+9.51) | +4.52 |
| μ = 13% | U13.5 − U0-ef | +2.279 (+2.278) | | +7.27 (+7.32) | +4.10 |
| μ* de empate | | **5.76% (5.76%)** | | | |
| OOS 2009-26 UPRO real | U0-efectivo | 13.584 (13.611) | −26.37 (−26.37) | 18.80 (18.95) | 3.36 (3.41) |
| | U0-SPYM | 15.399 (15.429) | −30.59 (−30.59) | 22.75 (22.92) | 5.13 (5.18) |
| | U13.5 | 16.012 (16.044) | −28.81 (−28.81) | 30.29 (30.51) | 9.22 (9.32) |
| OOS sint.+brecha | U13.5 | 15.993 (16.025) | −28.81 | 30.29 (30.51) | 9.22 (9.32) |

Niveles por μ (B): U0-efectivo 5.86 / 7.50 / 9.13 / 10.75 / 12.37%; U13.5 5.63 / 7.88 / 10.13 / 12.39 / 14.65%; P(−12%) de U13.5 34.6 / 33.3 / 32.8 / 31.2 / 28.9% contra 23.6 / 23.2 / 22.5 / 21.7 / 21.6% de U0-efectivo. ΔCAGR en μ = 5.5% −0.08, 6.0% +0.07, 6.5% +0.23 pp.

## Veredictos de B (umbrales literales del pre-registro)
- **H1 sostenida:** con μ = 7%, ΔCAGR = +0.38 pp (≥ 0.30, así que no se sostiene por esa rama) pero ΔP(−12%) = +10.05 pp > 3.0. La objeción del abogado del diablo se mantiene por la cola, no por el rendimiento.
- **H2 refutada:** μ* = 5.76%, por debajo del 6% del rango [6%, 12%]. Es un margen de 0.24 pp de μ; con mis convenciones y con las de A sale 5.76%.
- **H3 sostenida:** OOS con UPRO real, U13.5 gana +2.43 pp de CAGR (> 1.0) y suma +11.49 pp a P(−12%) (≥ 3.0). Gana con mucha más cola.
- **H4 sostenida:** |CAGR real − sintético + brecha| = 0.019 pp ≤ 0.50. El sintético con brecha por tramos reproduce al UPRO real dentro de la mezcla; P(−12%), P(−20%) y MDD son idénticos entre real y sintético.

## Comparación con A y explicación de cada diferencia
- Veredictos H1-H4: **idénticos** (sostenida / refutada / sostenida / sostenida). μ* 5.76% en ambas.
- ΔCAGR con μ = 7%: B +0.380 vs A +0.379 (0.001 pp ≤ 0.15). ΔP(−12%): B +10.05 vs A +10.14 (0.09 pp ≤ 1.0). **Criterio de "Replicado" cumplido.**
- Diferencias de nivel, todas de convención y verificadas (`variantes.txt`, bloque [f]):
  1. CAGR: B usa años calendario; A usa 252 días/año. Con 252 d B reproduce A al milésimo (11.253 / 12.357 / 13.083; OOS 13.611 / 15.429 / 16.044). Vale −0.01 pp en 1990-2026 y −0.03 pp en OOS.
  2. P(−12%) y P(−20%): B usa 126 puntos (t..t+125); A usa 127 (t..t+126, la lectura literal de R18 "dentro de t+1..t+126"). Con 127 puntos B reproduce A al centésimo en las 12 celdas (21.87 / 25.46 / 30.43; OOS 18.95 / 22.92 / 30.51; P(−20%) 8.04 / 9.37 / 12.60) y con 8,940 ventanas. Vale 0.1-0.2 pp; no toca ningún umbral.
  3. MDD, δ y μ*: coinciden sin ajuste alguno.
- Rebalanceo al cierre del primer día del mes en vez del último (variante [c]): +0.04 pp de CAGR, P(−12%) sin cambio. No explica nada de A y no mueve veredictos.

## Lectura
- El UPRO al 13.5% frente a efectivo a rf cuesta ~10 pp de P(−12%, 126 d) en cualquier μ de 5 a 11% y ~4.5 pp de P(−20%); su premio en CAGR depende casi linealmente de μ: −0.23 pp (5%), +0.38 (7%), +1.0 (9%), +1.6 (11%), +2.3 (13%). El empate está en μ ≈ 5.8% (por debajo del rango pre-registrado de H2, lo que dice que el 3x filtrado y mezclado pierde su ventaja algo más tarde de lo que se esperaba, no antes).
- La comparación relevante para W44 (U0-efectivo, no U0-SPYM) muestra una cola mayor que la nota exploratoria de R21 (+8.5 pp en 1990-2026 frente a +5.0 pp), porque el 13.5% en efectivo también amortigua lo que antes hacía SPYM.
- H4 valida el sintético con brecha de R20 dentro de la mezcla: no es necesario tener UPRO real para 1990-2008.

## Estado
**Replicado** (H1-H4 concordantes; ΔCAGR a 0.001 pp y ΔP(−12%) a 0.09 pp del de A). Independencia: de código sí; de datos no (las cachés son las que declara el pre-registro, "nada se descarga"). Sin commit por parte de B.
