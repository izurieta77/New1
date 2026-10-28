# AC-28 · Ejecución B independiente de R21 (R18 con la brecha UPRO de R20)

> Auditor de réplicas, 28-oct-2026. Fase 0: no recomienda inversiones. No se hizo commit; integra el orquestador.

## 1. Método
- **Orden de lectura:** primero el pre-registro de R21, R18 (md y `R18.py`, para la definición de la mezcla), R20 (md, para la brecha) y la definición del filtro V0 de R16 (`filtro`). Con eso escribí `ac28_r21.py` desde cero y lo corrí. **Solo después** abrí `R21.py` y `R21-resultados.json`.
- **Código:** `ac28_r21.py`, solo biblioteca estándar. No importa R16, R18 ni R21. Descarga con urllib, User-Agent "Mozilla/5.0" y timeout de 60 s.
- **Construcción propia:**
  - Filtro V0 reimplementado: SMA200 de ^GSPC sobre su propio calendario (días con ^GSPC y VIX). Sale si el precio < 0.97·SMA o VIX ≥ 25; entra si precio > SMA y VIX < 25.
  - La señal del cierre de t−2 de ese calendario se aplica al rendimiento del día t.
  - Los rendimientos se calculan entre días consecutivos que tienen todas las series.
  - DTB3 se arrastra con el último dato ≤ d.
- **Mezcla (la de R18):**
  - SPYM = ^SP500TR − 0.02%/252.
  - QQQM = ^NDX (precio) − 0.15%/252, con peso de 26.8%.
  - Efectivo a DTB3/252, con peso de 5.3%.
  - UPRO = 3·r_TR − 2·rf − 0.91%/252 con el filtro encendido; T-bill con el filtro apagado.
  - SPYM absorbe el resto. Rebalanceo al primer día de cada mes, antes de aplicar el rendimiento de ese día.
- **Brecha:** se resta g/252 **solo los días con el UPRO invertido**.
  - Constante: g = −1.59.
  - Por tramos, según el DTB3 del día: −1.31 si < 0.5%, −1.54 si está entre 0.5% y 3%, −2.30 si ≥ 3%.
- **Métrica:** para cada inicio t, ¿la curva cae ≥ nivel bajo su máximo desde t dentro de t+1..t+H? Se cuentan todas las ventanas completas (t = 0..N−H).
- **CAGR:** base calendario (365.25 días). También se reporta con base 252, que es la de A.
- **Periodo:** el de R18. Del 1990-10-17 al 2026-10-16, 9,065 días.

## 2. Fuentes y sha256 (ver `salida.txt` / `resultados.json`)
| Archivo | Origen | sha256 |
|---|---|---|
| yahoo_GSPC.json | Yahoo chart v8, bajado hoy | `da8434730971b560dcf84332dbf00fa014264fd99a42d41c0a27b6ce0273acf1` |
| yahoo_SP500TR.json | Yahoo chart v8, bajado hoy | `3f451e11e53c43388481f842a36709243f0d2bd6d770418dc6079f088b6dec8e` |
| yahoo_VIX.json | Yahoo chart v8, bajado hoy | `d710e40e14ef85c6a4d018858b04dcbbe4295d4ad60ec20cb4e9d9f738d5b5eb` |
| yahoo_NDX.json | Yahoo chart v8, bajado hoy | `5de5fbec0a46b14908f869df5d8421eda7b306a58cb22f379ffe5469353a37f4` |
| cboe_VIX_History.csv | CBOE, bajado hoy (sensibilidad) | `6da7f149324ec456c80f6d7e96c90b5d3bcaa3d0f6a4274f7840542db9809265` |
| fred_DTB3.csv | **Copia** de `AC-27-R20/datos/fred_DTB3.csv` (27-oct, llega al 23-oct) | `bbf5cf79827f89fdc123f14e8d567fcfa327a3e33fc00836b952e0da6e8038b3` |
| fred_NASDAQ100.csv | **Copia** de `AC-26-R19b/datos/NASDAQ100.csv` (26-oct; sensibilidad) | `48b13530971b07714e0cd32db5bacfdbfa94380b1b2207c846843ea08a56e06d` |

- **FRED no respondió:** "Remote end closed connection" con urllib y curl, en HTTP/2 y HTTP/1.1. Por eso DTB3 y NASDAQ100 son copias guardadas por auditorías previas, y las dos cubren el corte del 16-oct.
- **Reproducción por resultados, no por hash:** las series de Yahoo y CBOE crecen cada día y Yahoo revisa datos, así que el hash de una nueva descarga no coincidirá con este. `--sin-descarga` reutiliza `datos/`.
- **Límite de la independencia:**
  - en la corrida principal, el proveedor es el mismo que el de A (Yahoo para ^SP500TR, ^GSPC, ^VIX y ^NDX), pero bajado por mí;
  - la sensibilidad cambia ^NDX por FRED NASDAQ100 y ^VIX por CBOE;
  - no hubo fuente alternativa para el S&P TR.

## 3. Resultados B (corrida principal, 9,065 días; ventanas: 9,003 a 63 d y 8,940 a 126 d)
| Peso | Modo | P(−12%) 63 d | P(−20%) 63 d | P(−12%) 126 d | P(−20%) 126 d | CAGR (cal.) | CAGR (252) |
|---|---|---|---|---|---|---|---|
| U13.5 | sin brecha | 16.43% | 4.19% | 30.11% | 12.58% | 13.287% | 13.297% |
| U13.5 | constante | 16.45% | 4.25% | 30.12% | 12.60% | 13.104% | 13.114% |
| U13.5 | tramos | 16.45% | 4.25% | **30.43%** | 12.60% | 13.074% | **13.083%** |
| U27 | sin brecha | 21.02% | 3.05% | 40.91% | 12.00% | 14.115% | 14.125% |
| U27 | constante | 21.26% | 3.05% | 42.14% | 12.00% | 13.749% | 13.759% |
| U27 | tramos | 21.28% | 3.05% | 42.16% | 12.11% | 13.688% | 13.698% |

- **Datos adicionales:**
  - el UPRO está invertido 6,773 de 9,065 días (74.7%);
  - la MDD de la mezcla es −56.9% / −57.0% con U13.5 y −55.6% / −55.7% con U27;
  - la volatilidad es 19.1% con U13.5 y 20.3% con U27.
- **Sensibilidad de fuente (FRED NASDAQ100 + CBOE VIX, 9,060 días):** todas las celdas quedan a ≤ 0.03 pp de la principal. ΔP = +0.31 pp y ΔCAGR = −0.213 pp.
- **Control:** sin brecha, B reproduce R18 (9,065 días; P(−12%, 63 d) = 16.4% / 21.0%; P(−20%, 63 d) = 4.2% / 3.1%).

## 4. Veredicto B (umbral literal, U13.5)
- **H1:** ΔP(−12%, 126 d) tramos − sin brecha = **+0.31 pp** (+0.313). Como ≤ 1.0 pp, **SOSTENIDA**.
- **H2:** ΔCAGR = **−0.213 pp por año** en base calendario (−0.214 en base 252). Como está dentro de [−0.30, −0.10], **SOSTENIDA**.
- **Informativo:** con U27, ΔP(−12%, 126 d) = +1.25 pp y ΔCAGR = −0.43 pp. Orden de magnitud de H2: 0.135 × ~1.9 pp × 74.7% de los días invertido ≈ −0.19 pp.

## 5. Comparación con A (`R21-resultados.json`, `R21.py` sha256 `dfcb7675…a00f`, coincide con el pre-registro)
| Medida (U13.5) | A | B | Diferencia |
|---|---|---|---|
| P(−12%, 126 d) sin brecha / tramos | 30.12 / 30.43 | 30.11 / 30.43 | ≤ 0.01 pp |
| ΔP(−12%, 126 d) (H1) | +0.31 pp | +0.31 pp | 0.00 (límite: ±0.5) |
| CAGR sin brecha / tramos | 13.297 / 13.083 | 13.297 / 13.083 (base 252) | 0 |
| ΔCAGR (H2) | −0.214 | −0.214 (252) / −0.213 (cal.) | ≤ 0.001 |
| U27 P(−12%, 126 d) sin / const. / tramos | 40.91 / 42.14 / 42.16 | 40.91 / 42.14 / 42.16 | 0 |
| P(−20%, 126 d), las 6 celdas | 12.59 / 12.60 / 12.60 / 12.00 / 12.00 / 12.12 | 12.58 / 12.60 / 12.60 / 12.00 / 12.00 / 12.11 | ≤ 0.01 pp |

**Las diferencias son todas ≤ 0.01 pp. Explicación:**
1. **Número de ventanas.** La función `prob` de `R21.py` recorre `range(0, len(eq) − H − 1)`, así que omite la última ventana completa (8,939 en vez de 8,940 a 126 d). La `prob_toque` de R18 sí la incluía. Esto mueve la tercera cifra decimal. Es un detalle menor de A, sin efecto en los veredictos.
2. **Base del CAGR.** A usa 252 por año de rendimientos y B reporta además la base calendario (−0.01 pp en el nivel, 0.001 en la Δ). Con la base 252, B coincide con A al milésimo.
3. **Datos.** La descarga de Yahoo de hoy y la caché de R16 al 16-oct dan los mismos 9,065 días, y los resultados coinciden celda por celda. Cambiar a CBOE VIX + FRED NASDAQ100 mueve ≤ 0.03 pp.

No hay diferencias de alineación de la señal, de costos ni de recorte de fechas que superen la tolerancia.

## 6. Estado propuesto
- **"Replicado".** B concuerda con A en H1 (sostenida) y en H2 (sostenida), y su ΔP(−12%, 126 d) = +0.31 pp queda a 0.00 pp de A (tolerancia ±0.5).
- **Salvedades:**
  - la independencia es de código, no de proveedor, para el S&P TR (Yahoo en ambos);
  - DTB3 y NASDAQ100 vienen de copias de auditorías previas, porque FRED estuvo caído;
  - siguen vigentes los sesgos declarados en el pre-registro: pesos de R18 en lugar de los del libro, brecha de 2009-2026 aplicada a 1990-2008 y métrica contra el máximo de la ventana, no el histórico.
- **Lectura:** con el peso vigente, la brecha realista del UPRO casi no mueve las colas (+0.3 pp a 126 días) y cuesta ~0.21 pp por año de CAGR a la mezcla. Con U27 serían +1.25 pp y −0.43 pp por año.
