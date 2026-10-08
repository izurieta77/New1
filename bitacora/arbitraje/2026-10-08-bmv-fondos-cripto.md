# Arbitraje · 2026-10-08 · Dato del dueño: "desde abril de 2024 BMV y BIVA prohíben listar fondos extranjeros con cripto"

Origen: entrada del 8-oct en `bitacora/decisiones-pendientes.md` (commit `50df64d`), que la marcó "sin verificar". Esa nota dice: "no encontré esa norma en fuentes públicas; la BMV solo está considerando futuros y un ETF de cripto".

## Posiciones

- **Dueño:** desde abril de 2024 la BMV y BIVA prohíben listar fondos extranjeros con cripto, y por eso IBIT no se compra por el SIC.
- **Nota del 8-oct:** no encontró la norma; cita prensa según la cual la BMV estaba "considerando" un ETF de cripto.

## Fuente primaria

1. Aviso de la **Bolsa Mexicana de Valores** "Reforma al RI BMV (SIC)" (`bmv.com.mx/docs-pub/MARCO_NORMATIVO/CTEN_MNRR/COMUNICADO 3-REFORMAS-Reforma al RI-BMV (SIC).pdf`, descargado el 8-oct-2026, sha256 `c8f242dc…2adc`). Dice que la CNBV, "mediante oficio número 312-2/42112/2024 de fecha 15 de abril de 2024", autorizó la reforma y que esta "entrará en vigor el día 17 de abril de 2024". Texto adicionado a la disposición **4.019.00** del Reglamento Interior: "no serán susceptibles de listarse en el Sistema Internacional de Cotizaciones, aquellos valores que sean emitidos por vehículos de inversión colectiva, listados y cotizados [...] en las bolsas de valores de mercados del exterior, que [...] contenga uno o más activos virtuales, o bien, que busquen replicar el comportamiento de dichos activos virtuales, independientemente de la denominación que se le otorgue, a menos que las autoridades financieras prevean de manera expresa la posibilidad de listar dichos activos a través de Disposiciones de carácter general."
2. **Reglamento Interior de la BMV vigente, versión 08-08-2025** (`bmv.com.mx/docs-pub/MARCO_NORMATIVO/CTEN_MNRST/REGLAMENTO INTERIOR BMV VIGENTE-20250808.pdf`, sha256 `71a1e28b…bdede`): la disposición 4.019.00 conserva ese texto.
3. **BIVA:** no se encontró su reglamento interior ni un aviso con texto equivalente (búsqueda web del 8-oct). **Sin verificar.**

## Fallo

- **BMV: el dueño tiene razón (grado A, fuente primaria).** Desde el 17-abr-2024, el SIC de la BMV no admite fondos extranjeros con activos virtuales ni fondos que los repliquen, salvo que las autoridades lo autoricen expresamente con disposiciones de carácter general. La frase "la BMV solo está considerando futuros y un ETF de cripto" sale de prensa anterior a la reforma y queda superada.
- **BIVA: sigue abierto.** Falta leer su reglamento interior (sección de valores extranjeros o SIC) o un aviso suyo de 2024.
- **Regla de la cartera:** no cambia. No se compra IBIT ni ningún fondo cripto por el SIC. Lo fiscal de una cuenta en EUA sigue siendo asunto del dueño con su contador. Esta conciliación no decide nada sobre la dirección de la inversión.
- **Marcador de fuentes:** es un acierto del dueño como fuente directa. `datos/fuentes-del-dueno.csv` registra cuentas o fuentes externas, no al dueño, así que no se agregó fila. Lo anota la próxima rutina de inteligencia si el orquestador lo decide.
