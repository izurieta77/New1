# Ficha · Doctorado en derecho fiscal D9: antilavado (LFPIORPI), umbrales vigentes y qué toca al dueño

> Laboratorio del 16-oct-2026 (viernes, turno de doctorado, REGLAS §0d). Fase 0: no recomienda inversiones; tampoco es dictamen jurídico.

## Pregunta
¿Qué umbrales de la Ley antilavado vigente (LFPIORPI, reforma del DOF del 16-jul-2025) aplican a las actividades del dueño y de sus cuentas: cripto, inmuebles, construcción, vehículos y efectivo? ¿Cuánto son en pesos de 2026?

## Fuente y nivel de acceso
- **LFPIORPI, texto vigente de la Cámara de Diputados** (`diputados.gob.mx/LeyesBiblio/pdf/LFPIORPI.pdf`, 39 páginas, "Última reforma DOF 16-07-2025"). **Lectura de los artículos 17 (fracciones I a XVI) y 32. Grado A.**
- **UMA 2026:** diaria 117.31, vigente del 1-feb-2026 al 31-ene-2027, según fuentes secundarias (Alegra, IDC). **Grado B.** Se comprueba aritméticamente: 113.14 × 1.0369 = 117.31. No se leyó el DOF del 9-ene-2026. [Corregido 16-oct-2026, auditoría semanal: verificado en fuente primaria. DOF 9-ene-2026, aviso del INEGI "Unidad de medida y actualización" (dof.gob.mx/nota_detalle.php?codigo=5778072&fecha=09/01/2026, firmado el 8-ene): diaria $117.31, mensual $3,566.22, anual $42,794.64, vigentes a partir del 1-feb-2026; coincide con el comunicado INEGI 1/26. Pasa a **Grado A**.]

## Lo que dice la ley (A)
- **Art. 17 XVI (reformado en 2025):** es actividad vulnerable el intercambio habitual y profesional de **activos virtuales** por plataformas que no son entidades financieras, incluidas las que operan con mexicanos desde otra jurisdicción. El aviso procede cuando una operación de un cliente es **≥ 210 UMA**, o cuando la comisión cobrada es **≥ 4 UMA**. La obligación es **de la plataforma**, no del usuario.
- **Art. 17 V y V Bis:** la construcción o desarrollo de inmuebles **con compraventa de los propios bienes**, y la recepción de recursos para un desarrollo inmobiliario, dan aviso desde **8,025 UMA**.
- **Art. 17 XV (arrendamiento):** se identifica al cliente desde una renta mensual de **más de 1,605 UMA**; el aviso procede desde **3,210 UMA mensuales**.
- **Art. 32 (prohibición de efectivo):** inmuebles desde 8,025 UMA; vehículos, relojes, joyería, metales y arte desde 3,210 UMA. Las demás fracciones están en el texto.

## Ejercicio numérico (comprobado)
Código: `conocimiento/fichas/codigo/2026-10-16-d9-lfpiorpi-umbrales.py` (aserciones).

| Supuesto | UMA | Pesos 2026 |
|---|---:|---:|
| Aviso cripto, operación por cliente (17 XVI) | 210 | 24,635.10 |
| Aviso cripto, comisión (17 XVI) | 4 | 469.24 |
| Joyas y metales, identificación (17 VI) | 805 | 94,434.55 |
| Arrendamiento, identificación (17 XV) | > 1,605 al mes | 188,282.55 |
| Arrendamiento, aviso (17 XV) | 3,210 al mes | 376,565.10 |
| Construcción o desarrollo con compraventa, aviso (17 V y V Bis) | 8,025 | 941,412.75 |
| Efectivo prohibido: vehículos o joyería (32 II y III) | 3,210 | 376,565.10 |
| Efectivo prohibido: inmuebles (32 I) | 8,025 | 941,412.75 |

## Qué toca al dueño (inferencia, para revisar con su contador o abogado)
- **Binance real (~5,000 MXN):** la obligación de aviso es de la plataforma. Una operación del dueño de ≥ 24,635 MXN haría que la plataforma lo reporte. No es ilegal ni lo sanciona a él, pero conviene tener el soporte del origen de los fondos.
- **Construcción y remodelación:** la fracción V exige que haya **compraventa de los propios inmuebles**. Un servicio de remodelación a terceros, sin vender el inmueble, no encaja en V según la lectura literal. Un desarrollo propio para vender o rentar sí (V y V Bis).
- **Gasolinera:** la venta de combustibles **no aparece** entre las actividades vulnerables del art. 17 (busqué "combustible" en el texto: 0 resultados). Su riesgo es fiscal y de controles volumétricos (cap. 33), no de avisos LFPIORPI.
- **Efectivo:** ningún vehículo de 376,565.10 MXN o más ni inmueble de 941,412.75 MXN o más se puede pagar en efectivo, aunque se deposite en un banco. [Corregido 16-oct-2026, auditoría semanal: decía "de más de"; el art. 32 I-II dice "igual o superior", así que el umbral exacto ya está prohibido.]

## Límites
- No se leyeron el Reglamento ni las Reglas de Carácter General (plazos de aviso, identificación y expediente), ni el art. 17 XVI completo sobre la información del originante y del receptor.
- La UMA 2026 viene de fuente secundaria. [Corregido 16-oct-2026, auditoría semanal: ya se verificó en el DOF; ver Fuente.]

## Contraejemplo
Un inversionista que compra 30,000 MXN de BTC en una sola orden en una plataforma registrada en México genera un aviso de la plataforma, aunque la operación sea perfectamente lícita. El aviso no es una sanción: el umbral mide exposición a reporte, no ilegalidad.

## Segunda comprobación
- Las cifras en pesos son el producto UMA × veces, con aserciones en el código.
- Las veces UMA se copiaron del texto extraído del PDF oficial (fracciones V, V Bis, VI, XV y XVI del art. 17; I-III del art. 32).

## Estado nuevo
D9 sigue **Parcial**: se cubren las actividades vulnerables y la restricción de efectivo con el texto vigente, pero faltan la LMV y la CNBV, el reglamento y las reglas. En `estado-de-dominio.csv` se agrega el tema como **Documentado con comprobación**.
