# Arbitraje · 2026-10-08 · Marcador y rivales.csv frente a los libros del cierre del 7-oct

Origen: hallazgos 2.3, 2.4, 2.5 y 2.6 de `bitacora/revisiones/2026-10-07.md`.

## Hechos cotejados contra los archivos

| Punto | Marcador o rivales.csv | Libro o fuente | Fallo |
|---|---|---|---|
| 2.3 Papel GBM | 6-oct: 20,541.14 / +3.18% | `bitacora/equity.csv`, fila del 7-oct: 20,460.32 (commit `6e0a989`) | Gana el libro. Fila actualizada al 7-oct: +2.30% con base al fondeo |
| 2.3 Papel Binance | 6-oct: 10,142.05 / +0.99% | `bitacora/papel-binance/equity.csv`, fila del 7-oct: 10,028.72 | Gana el libro: +0.29% |
| 2.4 Real GBM | Boleta "condicionada a fondeo y a que el ticker aparezca"; 0 días | `bitacora/real/operaciones.csv` (ejecución del 7-oct); `bitacora/boletas/2026-10-05.md` L39 (cerrada) | Gana el libro: boleta cerrada (G1 ejecutada, G2 cancelada) y 1 día invertido |
| 2.5 Cierre de rivales GBM | 9,983.26 (ChatGPT) y 9,968.06 (Grok) "al cierre" | No hay respaldo en `competencia/`, `datos/entrada-dueno/` ni `rivales.csv`, que solo tienen el corte de ~10:45 (9,979.39 y 9,962.09) | **Sin fuente archivada.** Se marcan así en el marcador y no se borran. La conciliación los **reprodujo exactos** con cierres públicos de Yahoo del 7-oct (NVDA 237.47; GFNORTEO.MX 189.17; VISTAA.MX 1,172.85; AMKR 52.27; FSLR 180.13) × USD/MXN 17.9595 (≈ MXN=X de las 21:30 UTC, el mismo tipo de cambio con que se valuó el libro real de Claude: 3 × 91.46 × 17.9595 = 4,927.73). No se agregaron filas a `rivales.csv` por los rivales: REGLAS §5 dice que solo entra lo que reporte el dueño |
| 2.6 Filas de Claude en `rivales.csv` | Las últimas eran del 28-sep (GBM, sin fondear) y del 30-sep (Binance) | `bitacora/real/equity.csv` (9,967.89) y `bitacora/real-binance/equity.csv` (4,982.10), ambos del 7-oct | Se agregan las dos filas del 7-oct, con fuente y precios |

## Verificación independiente de la valuación de cierre (tolerancia 0.1%)

| Libro | Cálculo con Yahoo del 7-oct | Registrado | Diferencia |
|---|---|---|---|
| Papel GBM | (5 × 91.46 + 311.94 + 2 × 155.16) × 17.959 = 19,387.8 | 19,388.36 | 0.003% |
| Real GBM | 3 × 91.46 × 17.9595 = 4,927.73 | 4,927.73 | 0 |
| Papel Binance | 0.002698 × BTC ≈ 83,219 × 17.9595 | 4,032.28 | Coherente con BTC-USD 1h de 21:00-22:00 UTC (83,110-83,197) |
| Real Binance | 0.001325 × 83,217 × 17.9595 | 1,980.27 | El mismo BTC implícito que el papel |

## Corrección hacia adelante

- `rutinas/diaria-cierre.md`, paso 5, nota fechada del 8-oct con cinco instrucciones:
  - actualizar las cuatro filas de Claude y la fecha del encabezado;
  - usar el índice de cada CSV;
  - archivar la hora, los precios y el USD/MXN de toda valuación de cierre de los rivales;
  - agregar las filas de Claude a `rivales.csv`;
  - describir las boletas reales con su estado actual.
- Hay una fila en `conocimiento/registro-de-errores.md`.
