# Arbitraje · 2026-10-09 · Marcador y rivales.csv del cierre del 8-oct: reincidencia del paso 5

Origen: hallazgos 1.3, 1.4 y 1.5 de `bitacora/revisiones/2026-10-08.md`. Hay un antecedente: el fallo `2026-10-08-marcador-cierre.md` agregó las notas a-e al paso 5 de `rutinas/diaria-cierre.md`.

## Posiciones y fuente primaria

| Punto | Marcador o rivales.csv (cierre `3f107ca`) | Libro o fuente | Fallo |
|---|---|---|---|
| Nota (a), renglón "Actualizado" y papel | "2026-10-07"; papel GBM +2.30% / 102.30; papel Binance +0.29% / 100.29 | `bitacora/equity.csv` 8-oct: 102.532207 (20,506.44). `bitacora/papel-binance/equity.csv` 8-oct: 100.005354 (10,000.54) | Gana el libro: **+2.53%** y **+0.01%** |
| Nota (b), filas reales | "+0.05% sobre 10,000", "−0.63% sobre 5,000"; fuente `operaciones.csv` / `binance-real-…md`; drawdown "—" | `bitacora/real/equity.csv` 8-oct: 100.049975 (DD −0.32% el 7-oct). `bitacora/real-binance/equity.csv`: 99.365210 (DD −0.63%) | Gana el libro: índice y drawdown del CSV, que es la fuente |
| Nota (e), días invertidos | 9 en las seis filas reales | GBM real: compras del 7-oct, así que el 8-oct son 2 días | Se corrige. Regla escrita en el marcador: días con posición contando el de la compra (GBM en días hábiles y Binance en días naturales). Papel GBM 9, papel Binance 11, real GBM 2, real Binance 10, rivales GBM 2 y rivales Binance 10 |
| Nota (c), cierres de los rivales | 9,917.90; 10,112.43; 4,844.38; 4,912.08 "Yahoo 2d", sin precios, sin tipo de cambio y sin la etiqueta "sin fuente archivada" que puso la conciliación del 8-oct | Yahoo 1d del 8-oct × USD/MXN 18.17 (brief L35); BTC 81,660 y ETH 2,476 (brief L36) | **Se reproducen a ±0.02%** (tolerancia 0.1%). Se conservan las cifras y los insumos quedan en `competencia/valuacion-real-2026-10-08.md`. No van a `rivales.csv` porque REGLAS §5 solo admite ahí lo que reporta el dueño (criterio del fallo del 8-oct; REGLAS manda sobre la nota c) |
| Nota (d), `rivales.csv` | Sin filas del 8-oct | `real/equity.csv` y `real-binance/equity.csv` del 8-oct | Se agregan las filas del 8-oct de `arena-claude` (10,005.00) y `arena-claude-binance` (4,968.26) |

## Verificación independiente de la valuación (tolerancia 0.1%)
Corte de las 21:10-21:15 UTC del 8-oct (Yahoo 5m: MXN=X 18.175, BTC 81,721). Cierres 1d: SPYM 91.07, QQQM 307.85, UPRO 153.13.
- **Papel GBM:** (5 × 91.07 + 307.85 + 2 × 153.13) = 1,069.46 USD × 18.1722 = 19,434.48. Coincide con lo registrado; con 18.175 da +0.014%.
- **Real GBM:** 3 × 91.07 × 18.1722 = 4,964.84 (exacto).
- **Papel y real Binance:** el BTC implícito es 1,484,096 y 1,484,098 MXN/BTC (≈81,678 USD × 18.1722), el mismo corte. Diferencia contra el corte de las 21:15: +0.03%.

## Diagnóstico de procedimiento
**Segunda noche seguida (7 y 8-oct) en que la rutina de cierre no sigue el paso 5 del marcador.** Las notas a-e ya estaban en `rutinas/diaria-cierre.md` desde la madrugada del 8-oct, antes de esta corrida, y el cierre las omitió todas. No es un problema de redacción del procedimiento, sino de cumplimiento. Es la **primera reincidencia**. Si se repite una tercera noche, se escala al dueño según el criterio que ya se usó con el papel Binance (`2026-10-03-papel-binance-tercera-vez.md`). Por ahora no se escala. Se pide al supervisor vespertino que revise el marcador contra los cuatro `equity.csv` en cada cierre.

## Correcciones
`competencia/marcador.md` (L5 y L11-L18, con nota fechada), `competencia/rivales.csv` (dos filas), `competencia/valuacion-real-2026-10-08.md` (nuevo, respaldo de insumos) y `conocimiento/registro-de-errores.md`.
