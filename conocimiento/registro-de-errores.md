# Registro de errores

| Fecha | Archivo | Afirmación anterior | Evidencia | Corrección | Efecto |
|---|---|---|---|---|---|
| 2026-09-25 | herramientas/tablero.py; bitacora/briefs/2026-09-25-tablero.md; reportes al dueño | VIX de 14.21 y USD/MXN de 17.25 presentados como datos del día; diagnóstico "RISK-ON" | FRED VIXCLS estaba al 22-sep y DEXMXUS al 18-sep (rezago de publicación). Yahoo ^VIX = 15.67 al 24-sep; MXN=X = 17.71 al 25-sep. Señalado por un sistema rival y verificado por nosotros | El tablero agrega Yahoo ^VIX, usa la fuente más reciente para el régimen y marca como rezagado todo dato de más de 3 días | El diagnóstico cambia de RISK-ON a MIXTO / TRANSICIÓN (versión corregida en 2026-09-25-tablero-v2.md; la original se conserva) |
