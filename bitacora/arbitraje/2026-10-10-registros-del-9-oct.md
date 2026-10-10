# Arbitraje · 2026-10-10 · Registros del 9-oct: brief de pre-apertura, latidos y pendientes de más de 24 h

Materia: cifras repetidas que no coinciden entre archivos, latidos faltantes y dudas abiertas en `bitacora/decisiones-pendientes.md`.

## 1. Brief del 9-oct (`bitacora/briefs/2026-10-09.md`)
- **L7, umbral de FX-1.** El brief decía "18.4375 (a 0.9%)" y la supervisión L16 dice 18.4733, con el mismo σd de 0.67%. Recalculado: 18.08737 × exp(0.6676% × √10) = 18.4733. Para que saliera 18.4375 haría falta un σd de 0.61%. **Gana 18.4733**, a 1.1% de 18.27. Es la misma confusión de umbral que se falló el 9-oct (`2026-10-09-umbral-fx1.md`).
- **L24, rendimiento del papel.** El brief decía "+3.01% del periodo". Con base 100 al fondeo eran **+2.53%** al 8-oct (índice 102.5322). Esa corrección la había hecho la conciliación a las 03:20 UTC, antes de la pre-apertura (12:57 UTC). Al cierre del 9-oct, `bitacora/equity.csv` da **+4.41%** (104.414749 = 20,882.95 / 20,000).
- **L10 y L13**, hallazgos menores de la revisión. L10: el petróleo "tras ataques en Ormuz" no fue un hecho del día (inteligencia de las 07:05). L13: la salida del filtro cripto vigente era 69,679.66 (71,834.70 × 0.97), no 69,542.
- **Sección Revisión.** Decía "P0027 y P0031 ya están resueltos"; vuelven a abiertos (fallo `2026-10-10-clausula-ultimo-dato.md`).

**Fallo:** todas las correcciones van con nota fechada. No se reescribió ninguna línea.

## 2. Latidos (REGLAS §3)
- **Auditoría semanal W41** (`cd6edb4`, `2216312` y `a73dec3`, de 22:47 a 22:55 UTC): ningún commit tocó `estado-rutinas.md`. Es la primera vez para esta rutina. Queda anotado en `bitacora/bloqueos.md` y no se fabrica el latido retroactivo.
- **`c933a40`** (orquestador, 07:05 UTC): es una entrada manual y no una rutina; no dejó latido. Su encabezado decía "09:00 CDMX aprox." y en realidad fue a la 01:05 CDMX. Queda corregido con nota.
- **Investigador vespertino** (`6468550`, 02:12 UTC del 10-oct): **sí dejó latido** ("2026-10-10 02:14 UTC · investigador-vespertino · OK"). No es la tercera noche, así que no hay escalación. Su fila en `bloqueos.md` queda **cerrada**.
- **Menor (reincide):** varios latidos llevan una hora posterior a la de su commit (cierre 21:45 en un commit de las 21:39; trabajo continuo 01:20 en uno de las 01:10). Lo dejo anotado y no corrijo líneas viejas.

## 3. Valuación: reescritura de la fila del 8-oct en los cuatro `equity.csv`
`a8c5582` cambió el índice del 8-oct en los cuatro CSV; por ejemplo, 102.532207 pasó a 102.532200 y 100.049975 a 100.050000. Equity, efectivo y posiciones no cambiaron. Sin flujos, el índice exacto es equity / aportación × 100, así que el valor nuevo es el exacto. La diferencia de ≤ 0.00003% viene del encadenamiento con decimales. **OK**, dentro de la tolerancia, y no se corrige nada.

## 4. Pendientes de más de 24 h (hechos, registros y reglas)
- **BIVA, prohibición del SIC para fondos con cripto:** sigue **abierto**. `biva.mx/empresas/marco_normativo` es una aplicación de una sola página y su HTML no trae el reglamento. La búsqueda solo devuelve los documentos de la BMV (oficio CNBV 312-2/42112/2024). **Falta:** el Reglamento Interior de BIVA vigente.
- **Mora automotriz de GFNORTEO (CNBV):** sigue **abierto**. `portafolioinfo.cnbv.gob.mx` volvió a fallar por certificado ("unable to get local issuer certificate"), igual que el 7-oct.
- **Vigía (9-oct 11:05), ¿cruzar 2% en pesos por ganancia cuenta como Alta?:** tiene menos de 24 h. La regla no distingue la dirección y la vigía la aplicó literal, así que no hay desacuerdo que arbitrar. Queda como propuesta de redacción para quien mantenga `rutinas/inteligencia.md`.
- **Primera RMF 2026 y art. 70-A CFF** (investigador vespertino, 10-oct): tiene menos de 24 h; es verificación en el DOF y queda para el verificador.
- Los demás puntos abiertos son de comité o del dueño: papel Binance, SGM, propuesta del Brier, metas y la agenda del comité. **No los toco.**
