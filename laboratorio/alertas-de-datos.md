# Alertas de datos y de método (registro vivo)

Cada réplica y cada ficha deben revisar esta lista antes de publicar sus cifras. Cuando una alerta se confirma o se descarta en nuestros propios datos, se anota aquí con fecha y archivo.

| # | Fecha | Alerta | Origen | Qué hacer | Estado |
|---|---|---|---|---|---|
| 1 | 2026-09-25 | En Yahoo, el `adjclose` de NAFTRAC y posiblemente de otras emisoras .MX omite dividendos (reportado para 2021). Esto subestima el rendimiento total del IPC. | Auditoría de otro sistema, compartida por el dueño | Comparar contra el S&P/BMV IPC Total Return (S&P DJI) o reconstruir dividendos con avisos de derechos de BMV/Emisnet. Tratar cualquier rendimiento de .MX tomado de Yahoo como **piso** hasta verificarlo. | Por verificar en R04, R08 y V04 |
| 2 | 2026-09-25 | No confundir el cambio entre dos fechas fijas con la caída máxima de pico a valle. Por ejemplo, el S&P en MXN en 2008: la cifra de −21.6% es entre fechas fijas; la de −31% (mensual) o −38% (diario) es la caída máxima con dividendos. | Idem | Reportar siempre las dos medidas con fechas y frecuencia. | Por verificar en R08 y V04 |
| 3 | 2026-09-25 | Regla de media móvil con señal en USD aplicada a un activo medido en MXN. Si el tipo de cambio y el precio no se alinean en la misma fecha, se mezclan dos variaciones. | Idem | Alinear las fechas del precio, el tipo de cambio y la señal. Reportar por separado la variante con señal en USD y la variante con señal en MXN. | Por verificar en R01 y V04 |
| 4 | 2026-09-25 | La rentabilidad (RMW) desde 2000 puede ser significativa con French y no con AQR ni con Hou-Xue-Zhang. | Idem | Resolver con la auditoría ciega AC-02 (tres fuentes). | En curso (AC-02) |
| 5 | 2026-09-25 | Media mensual × 12 no es rendimiento compuesto. En factores volátiles la diferencia es grande: MOM de EUA de oct-2006 a 2025 da +1.06% como media × 12 y −0.26% compuesto. | Precisión recibida y verificada por nosotros | Reportar siempre ambos. | Aplicada en V01 |
| 6 | 2026-09-25 | La t convencional (IID) y la t con Newey-West son estimadores distintos. | Precisión recibida | Reportar ambas. | Aplicada en V01 |
