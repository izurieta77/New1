# Arbitraje · 2026-10-10 · P0027 y P0031: cláusula "si falta, último dato previo" (y cotejo de P0033 y P0082)

Materia: dos rutinas leen el mismo criterio de dos formas, con duda anotada (revisor, 9-oct, punto 3).

## Posiciones
- **Pre-apertura del 9-oct** (brief L19 y L27): no aplicar la cláusula mientras la serie todavía vaya a tener dato del día. Dejó los tres abiertos.
- **Vigía de las 15:05 del 9-oct** (`a73b2a8`, 21:15 UTC): aplicó la cláusula ese mismo día. P0027 = SÍ con DEXMXUS del 2-oct (18.1920 > 17.90); P0031 = NO con DGS10 del 8-oct (5.22 < 5.30).
- **Cierre del 9-oct y W41:** los dan por abiertos, pero la W41 los cuenta en su Brier (n = 21).

## Fuente primaria
- **Criterio literal** (`bitacora/pronosticos.csv`): P0027 "FRED DEXMXUS **del 2026-10-09** (si falta, último dato hábil previo) > 17.90"; P0031 "FRED DGS10 **del 2026-10-09** (si falta, último dato previo) >= 5.30".
- **El mismo archivo distingue "falta" de "rezago":** P0034 escribe expresamente "si falta ese día exacto (fin de semana o feriado, **o rezago de publicación**), se usa el último dato publicado". P0027 y P0031 no incluyen el rezago.
- **FRED, `fredgraph.csv`, consultado el 10-oct ~03:00 UTC:** DEXMXUS llega al 2026-10-02 (18.1920). Es la serie H.10, que se publica por semana, así que la semana del 5 al 9-oct todavía no sale. DGS10 llega al 2026-10-08 (5.22). El 9-oct fue día hábil en EUA para las dos series, así que **las dos tendrán observación de esa fecha**. El lunes 12-oct es feriado federal (Columbus Day); se espera el dato desde el 13-oct.
- **P0033:** FRED SP500 2026-10-09 = **7,811.54** (coincide con Yahoo ^GSPC 7,811.54) > 7,683.69 → **SÍ**. Bien resuelto en `6e8b2f5`.
- **P0082:** Deribit `public/ticker?instrument_name=BTC-PERPETUAL`, `open_interest` = 827,296,870 a las 01:28 UTC del 10-oct (`6e8b2f5`). En mi consulta de las 03:01 UTC: 827,456,780. Las dos están ≥ 715,272,526.5 y caen el 10-oct UTC → **SÍ**. Bien resuelto. Menor: la probabilidad tiene 2 decimales (0.80) y el resto del archivo usa 4.

## Fallo
1. **"Si falta" quiere decir que la serie no tiene observación de esa fecha** (fin de semana, feriado, día sin mercado), no que el dato aún no se haya publicado. Gana la lectura de la pre-apertura. La interpretación contraria permitiría resolver con un dato de 7 días antes de la fecha que el pronóstico pregunta, y el propio CSV, cuando quiso cubrir el rezago, lo escribió (P0034).
2. **P0027 y P0031 vuelven a abiertos** (resultado y fecha_resuelto en blanco, con nota fechada en la fila). Se resuelven cuando FRED publique el 9-oct. Si al vencer el plazo razonable la fecha sigue sin observación, entonces sí aplica la cláusula.
3. **P0033 SÍ y P0082 SÍ** quedan como están.
4. **Brier recalculado** (`python3 herramientas/pronosticos.py puntuar`, 10-oct): global **0.2116, n = 21** (claude 0.2571, n = 8; vigía 0.1955, n = 12; cripto 0.0400, n = 1). La n = 21 de la W41 (0.224) contaba P0027 y P0031; la de hoy cuenta P0033 y P0082 en su lugar.
5. El cierre del 9-oct tenía razón al darlos por abiertos. La línea de la revisión del brief ("ya están resueltos") se corrigió con nota.

## Correcciones
`bitacora/pronosticos.csv` (P0027 y P0031), `bitacora/briefs/2026-10-09.md` (sección Revisión), `bitacora/semanal/2026-W41.md` (nota en g) y `conocimiento/registro-de-errores.md`.
