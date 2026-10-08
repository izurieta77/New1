# Arbitraje · 2026-10-08 · Pendientes de hechos, registros y reglas abiertos más de 24 h en `decisiones-pendientes.md`

| Entrada | Tipo | Fallo y fuente | Acción |
|---|---|---|---|
| 6-oct y 7-oct, P0024 (WTI FRED del 2-oct) sin dato | Hecho | FRED `DCOILWTICO` (`fredgraph.csv`, consultado el 8-oct ~03:00 UTC): 2026-10-02 = **97.89**, que es ≥ 93.00, así que se resuelve **SÍ**. Cumple el criterio literal (primer dato publicado de esa fecha calendario). `pronosticos.csv` ya dice resultado=1 y fecha_resuelto 2026-10-07: correcto | Cerrados los dos; el brief del 7-oct se corrigió (decía "sin pronósticos resueltos"). Brier al 7-oct: 0.2365 con n = 13. Con P0070 (BEA, déficit de agosto 105.6 mil M, mayor que 88.6, así que NO; verificado en bea.gov) queda en 0.2412 con n = 14 |
| 7-oct, nombre del archivo de podcasts | Regla | Ya la cerró el orquestador (`rutinas/inteligencia.md` §1c, fecha de CDMX) | Marcado como cerrado |
| 5-oct, `estrategias/catalogo.md` no existe | Regla que choca con el repo | La carpeta `estrategias/` no existe; la función de catálogo la cumple `laboratorio/tabla-maestra.md` | Corregido `rutinas/trimestral-investigacion.md` §3 con nota fechada |
| 5-oct, Newsquawk/UKMTO tanquero LNG | Hecho | Ya lo cerró el vigía el 6-oct (entrada propia, Estado: Cerrado) | Marcada como cerrada la entrada original |
| 1-oct, severidad Irán/Ormuz "abierto" | Seguimiento | El estado vivo está en `bitacora/alertas.md` | Cerrado como punto de decisiones |
| 7-oct, revisión: base del TWR y letras del CFF | Registro y hecho | `2026-10-08-base-twr.md` y `2026-10-08-incisos-cff-82-xxv.md` | Cerrado |
| 7-oct, "UPRO no está en GBM" y "~10,400 MXN extra" | Registro superado | UPRO está en GBM USA, sin orden stop (10:17-10:22). Los ~10,400 MXN son de ChatGPT y de Grok (`competencia/gbm-real-2026-10-07.md`) | Notas de "superado" en la boleta L35, en `decisiones-pendientes.md` y en `bitacora/supervision/2026-10-07.md` L23, sin borrar nada. También se corrigió la fórmula "× 1.003" de esa línea (hallazgo 1.7) |
| 8-oct, BMV/BIVA y fondos cripto | Hecho | `2026-10-08-bmv-fondos-cripto.md` | BMV cerrado (A); BIVA abierto |
| Errata "17-oct" (vigía, mora GFNORTEO) | Registro | Decía 17-oct; es 7-oct | Corregido con nota |

## Lo que no se tocó (se escala o sigue abierto)

- **Comité del 9-oct (dirección y parámetros):**
  - destino del ~27% que iba a UPRO;
  - efectivo ocioso;
  - "stop mental" para UPRO vía GBM USA;
  - BTC 40→65% y tramo 2;
  - banda FX y cobertura;
  - `filtro_apalancados` y VIX;
  - radar de niveles;
  - regla "Kawa";
  - UPRO en el SIC;
  - exchange cripto y plan B.
- **Dueño:**
  - escalación del papel Binance (`2026-10-03-papel-binance-tercera-vez.md`);
  - doctorados;
  - asunto fiscal SGM;
  - propuesta sobre el Brier;
  - paquete del 6-oct.
- **Menos de 24 h:** el matiz Ormuz del analista cripto y la mora automotriz de GFNORTEO, que no tiene fuente primaria porque la CNBV no responde.
- **Herramienta:** `portafolio.py registrar` sigue sin `--subclase` (pendiente técnico conocido).
