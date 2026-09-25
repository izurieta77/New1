# 05 · The Week On-chain (Glassnode)

> Ficha de recurso · Grupo G5 (mercado, on-chain, stablecoins e institucional) · Estudiada el 25-sep-2026 por `analista-cripto` · **Acceso: sección** · **Grado global: C** (métricas propias de Glassnode); **B** en precio realizado y MVRV, que reproduje con datos gratuitos.
>
> **Etiquetas:**
> - **[H]** hecho con fuente y edición o página;
> - **[I]** inferencia o interpretación (digo si es del autor o nuestra);
> - **[O]** opinión o pronóstico del autor.
>
> **Grados:**
> - **A:** identidad o dato oficial;
> - **B:** evidencia sólida con salvedades;
> - **C:** muestra corta o no reproducible;
> - **D:** narrativa sin historial auditado.

## 1. Ficha

| Campo | Dato |
|---|---|
| Año | 2020: la serie semanal existe desde mar-2020 según el índice. Leí las semanas 31 a 38 de 2026 |
| Autor | Equipo de investigación de Glassnode. Las ediciones 31, 32 y 34-38 las firma Frederik Theissen; la 33, CryptoVizArt y Chris Beamish |
| Tipo | Boletín semanal de análisis on-chain, de derivados y de flujos |
| Costo | El boletín es gratis. Los datos que lo sostienen (Glassnode Studio y API) son de pago |
| URL | Boletín: https://research.glassnode.com/tag/newsletter/ · Definiciones: https://docs.glassnode.com/further-information/metric-guides |
| **Conflictos de interés** | Glassnode vende datos. Cada edición trae el anuncio "Ready to get ahead of markets… Try Glassnode. Sign up or talk to sales", así que tiene incentivo a presentar sus métricas como indispensables. Las métricas "entity-adjusted" y por cohorte son **propietarias** y no se pueden reproducir gratis. Glassnode es coautor del recurso 34 con Coinbase, que es un exchange. En lo que revisé no encontré posiciones propias en cripto declaradas |

## 2. Acceso real

- **Leído completo (texto):** las ediciones de 2026 que siguen. Descargué el HTML de research.glassnode.com y **no vi las gráficas**.
  - semana 31, 5-ago: "Priced For Nothing, Reacting To Everything";
  - semana 32, 12-ago: "Trigger Happy";
  - semana 33, 19-ago: "Yields Anchor, Capitulation Grinds";
  - semana 34, 26-ago: "Squeeze into Supply";
  - semana 35, 2-sep: "Doubt at the Boundaries";
  - semana 36, 9-sep: "The Ceiling Everyone Can See";
  - semana 37, 16-sep: "Breakdown into Thin Support";
  - semana 38, 23-sep: "Escape Velocity".
- **Definiciones, leídas completas en Markdown de docs.glassnode.com:**
  - MVRV Ratio, MVRV-Z, STH-MVRV y Realized Capitalization;
  - SOPR y STH-SOPR;
  - NUPL y Supply held by LTH/STH;
  - el aviso "Exchange Data Transparency Notice".
- **No leí:** el archivo 2020-2026 completo. Tampoco usé Glassnode Studio, que es de pago.
- **Nivel: sección.**

## 3. Lo esencial

### Definiciones (docs.glassnode.com)

- **[H] Capitalización realizada:** vale cada UTXO al precio de la última vez que se movió. Es "el costo base agregado" de la red y le quita peso a las monedas perdidas o dormidas (guía *Realized Capitalization*; según la guía, la acuñó Antoine Le Calvez en sep-2018 y la formulación original está en coinmetrics.io). **Precio realizado = capitalización realizada ÷ oferta.**
- **[H] MVRV = capitalización de mercado ÷ capitalización realizada.**
  - La guía dice que valores > 3.5 "generally served as a strong signal for late stage bull cycles" y que < 1 señala capitulación y acumulación.
  - La crearon Mahmudov y Puell en oct-2018 (guía *MVRV Ratio*).
- **[H] NUPL = (capitalización de mercado − capitalización realizada) ÷ capitalización de mercado** (guía *NUPL*).
  - [I, nuestra] Por álgebra, **NUPL = 1 − 1/MVRV**. Con el MVRV basta para tener el NUPL no ajustado por entidad.
  - Esta versión **no es** la NUPL ajustada por entidad que usa el recurso 34.
- **[H] SOPR:** valor en USD de los UTXO gastados en el día al gastarse, dividido entre su valor al crearse (guía *SOPR*).
  - Mayor que 1: en promedio se vendió con ganancia.
  - Menor que 1: se vendió con pérdida.
  - STH-SOPR solo toma salidas de menos de 155 días (guía *STH-SOPR*).
- **[H] Tenedor de corto plazo (STH):** monedas con menos de 155 días, con una transición suave de 10 días de ancho.
  - La clasificación se hace por entidad, con la fecha promedio de compra ponderada por volumen.
  - Excluye los saldos en exchanges: LTH + STH + exchanges = oferta circulante (guía *Supply held by LTH/STH*).
  - **Costo base STH** = precio realizado de esa cohorte (STH-MVRV: MVRV de los UTXO de menos de 155 días).
- **[H] Flujos y saldos en exchanges:** salen de etiquetar direcciones de tres fuentes: direcciones verificadas, etiquetas externas y clustering.
  - El aviso dice que los saldos son "largely… lower bounds of the true balance" y que "may undergo retrospective revisions".
  - Coinbase, Kraken, Bitstamp y Gate, entre otros, **no** publican direcciones verificadas en la tabla de ese aviso.
- **[H] True Market Mean:** "the average price paid by investors who are still active" (semana 37). En lo que revisé no encontré una guía pública de esta métrica.

### Números de agosto y septiembre de 2026

- **[H] Precio realizado y mediana (semana 32):**
  - precio realizado agregado ≈ **US$52.8 mil**;
  - mediana del precio realizado: **US$63.0 mil**.
- **[H] Costo base STH:**
  - US$68.5 mil (semana 33);
  - US$70.0 mil (semana 34);
  - ≈ US$71 mil (semana 35);
  - **US$71.3 mil** (semana 37, dato del 15-sep).
- **[H] True Market Mean:** US$75.8 mil (semana 33) → 76.6 (semana 36) → 76.7 (semana 37) → **77 mil** (semana 38).
- **[H] "Mean MVRV price" = US$96.7 mil (semana 38).** Es el precio realizado multiplicado por el MVRV promedio de largo plazo: el nivel donde la ganancia del tenedor promedio vuelve a su norma histórica.
- **[H] Un bear market "de pérdidas anchas pero someras" (semanas 38 y 33):**
  - en este mercado bajista el precio **nunca cerró un día debajo del precio realizado**;
  - la NUPL nunca fue negativa;
  - la pérdida no realizada relativa tocó ≈ 0.25, contra > 0.6 en ciclos previos;
  - el cociente de ganancia/pérdida realizada (SMA de 90 días) iba en 0.75, cuando el agotamiento de vendedores históricamente llega debajo de 0.5.
- **[H] aSOPR:** pasó casi todo el bear un poco debajo de 1.0. La media de 7 días tocó 1.0 **nueve veces** desde el techo de octubre, y las nueve veces los vendedores aprovecharon para salir (semana 32).
- **[H] ETF de BTC en EUA:**
  - junio de 2026 fue su **peor mes registrado**: devolvieron ≈ 65.8 mil BTC, contra más de 218 mil BTC absorbidos en su mejor mes de finales de 2024 (semana 31);
  - entraron US$2.23 mil M durante el short squeeze de agosto (semana 34);
  - salieron US$334 M del 8 al 14-sep (semana 37);
  - entraron ≈ US$1.3 mil M en los 5 días siguientes (semana 38).
- **[H] Punto de equilibrio del complejo de ETF ≈ US$86 mil** (semana 36):
  - cerró debajo de ese nivel 228 sesiones seguidas;
  - su pérdida latente máxima fue ≈ US$18 mil M el 5-feb-2026;
  - al 7-sep era ≈ US$3.9 mil M.
- **[H] Tesorerías corporativas (semana 37):**
  - costo base de US$80.5 mil;
  - compras netas de ≈ 5.9 mil BTC en 3 meses, contra 89 mil BTC solo en julio de 2025.
- **[H] Stablecoins (semana 37):** ≈ US$301 mil M, planas en la semana y ≈ 4% debajo del pico de abril de 2026.
- **[H] Cambio de posición neta en exchanges:**
  - en 2026 hubo entradas netas la mayoría de los días (semana 32);
  - a mediados de septiembre el saldo a 30 días ya era de salida neta (semana 37).
- **[O] Tesis de la semana 38:**
  - la siguiente prueba está en US$95-97 mil (opciones más el mean MVRV price);
  - si el precio pierde 84 mil, vuelve a verse 77 mil.

## 4. Qué cambia para invertir

- **El precio realizado y el MVRV salen robustos entre proveedores. [H, cálculo propio]**
  - **Coin Metrics** comunitario, 24-sep-2026: MVRV **1.5773**, precio realizado **US$53,500.49** (= 84,386.58 ÷ 1.5773).
  - Glassnode (semana 32) daba 52.8 mil y Coin Metrics el 10-ago daba 52,719.84: diferencia de 0.15%.
  - **BGeometrics** (bitcoin-data.com), 18-sep, versión gratis con 7 días de retraso: 52,850.93, contra 53,247.55 de Coin Metrics: diferencia de 0.75%.
- **El "mean MVRV price" se reproduce, pero depende de la ventana. [H, cálculo propio]**
  - Con Coin Metrics, el MVRV promedio desde 2011 es 1.812, que da **US$96,726** al 21-sep: igual que el 96.7 mil de Glassnode.
  - Con la historia desde 2014 da 91.9 mil; desde 2010, 104.7 mil.
  - Es una zona de referencia, no un número exacto.
- **El costo base STH y nuestra SMA200 coinciden hoy. [I, nuestra]** El costo base STH es US$71,636 (BGeometrics, 18-sep) y la SMA200 de 200 cierres de Coin Metrics es US$70,848. El filtro SMA200 de la cuenta Binance y la línea on-chain más citada son casi el mismo nivel, así que no son dos confirmaciones independientes.
- **Qué tiene evidencia y qué es narrativa:**
  - **Descripción robusta (grado A-B):** el precio realizado y el MVRV como medida de la ganancia o pérdida agregada.
  - **Señal con poca muestra (grado C):**
    - MVRV < 1: en 7 episodios desde 2011, el rendimiento a 12 meses tuvo mediana de +122.7%. Pero son solo 7 episodios (ver cap. 05 §4).
    - MVRV intermedio, como hoy: **sin ventaja** a 30-120 días.
  - **Narrativa hasta probarla (grado D):** los umbrales del Sell-Side Risk Ratio, "Market Compass", "Accumulation Trend Score", True Market Mean y las zonas de liquidez. En lo que revisé, Glassnode no publica pruebas fuera de muestra de estas métricas.
  - **Flujos a exchanges (grado D como señal de timing):**
    - Con Coin Metrics, el saldo en exchanges **subió 46,954 BTC el 13-ago-2026** con un flujo neto de solo +3,192 BTC. Es reetiquetado de direcciones, no compras ni ventas.
    - Del 1-jul al 24-sep los flujos netos suman **−141,806 BTC** y aun así el saldo **subió 38,778 BTC**.
    - Glassnode (semana 32) veía entradas netas la mayor parte del año. El signo depende de la base de etiquetas de cada proveedor.
- **ETF: el comprador marginal de este ciclo es procíclico.** [I, nuestra] Vendió en junio, cerca del mínimo (58,525 al cierre del 30-jun, según Coin Metrics), y compró en el squeeze de agosto y en septiembre. Los flujos de ETF confirman el movimiento, no lo anticipan.
- **Uso en la rutina de 4 h:**
  - leer la edición de cada miércoles como contexto;
  - tomar solo niveles que se puedan reproducir: precio realizado, MVRV y costo base STH de BGeometrics;
  - no disparar operaciones con métricas propietarias.

## 5. Contrapuntos y límites

- **Hace falta una historia cada semana.** Los niveles se mueven: la banda de 83-86 mil era "el techo que todos ven" el 9-sep y el 23-sep ya era soporte. Leída ex post, cualquier ruptura parece explicada.
- **Los datos se revisan.** Cada edición avisa: "the most recent daily points remain subject to revision".
- **Las métricas por entidad dependen de clustering propietario** (guía LTH/STH) y no se pueden auditar.
- **Los umbrales fijos se degradan.** Los picos de MVRV por ciclo, con Coin Metrics, fueron:
  - 7.74 (2011), 5.88 (2013), 4.72 (2017), 3.96 (2021) y 2.78 (2024);
  - el techo de precio del 6-oct-2025 llegó con MVRV de solo 2.29.
  - La regla "> 3.5 = techo" de la guía no se activó en este ciclo.
- **No hay historial auditado de aciertos del boletín.** En lo que revisé no encontré una evaluación sistemática de sus lecturas.
- **No vi las gráficas.** Todos los números salen del texto.

## 6. Autoexamen

1. **Coin Metrics comunitario responde 403 a `CapRealUSD`. ¿Cómo obtienes gratis el precio realizado y el NUPL?**
   - *Respuesta:* capitalización realizada = `CapMrktCurUSD / CapMVRVCur`; precio realizado = eso ÷ `SplyCur`, que equivale a `PriceUSD / CapMVRVCur`. NUPL = 1 − 1/MVRV.
   - Al 24-sep-2026: 84,386.58 / 1.5773 = **53,500**; NUPL 0.366.
   - *Fuente:* guías de Glassnode (NUPL y MVRV) y la API de Coin Metrics, consultada el 25-sep-2026.
2. **¿Qué es un STH en Glassnode y qué mide su costo base?**
   - *Respuesta:* una entidad cuya fecha promedio de compra, ponderada por volumen, tiene menos de 155 días (transición de 10 días). Excluye los saldos en exchanges.
   - Su costo base es el precio realizado de esa cohorte: US$71.3 mil al 15-sep (semana 37).
   - *Fuente:* guía *Supply Held by LTH/STH* y semana 37.
3. **El SOPR diario es 1.0076 (BGeometrics, 18-sep). ¿Qué dice y qué no dice?**
   - *Respuesta:* en promedio, las monedas movidas ese día se vendieron con 0.76% de ganancia sobre su costo.
   - No dice quién vende ni anticipa el precio. La semana 32 muestra que, en un mercado bajista, 1.0 funcionó como techo (nueve rechazos).
   - *Fuente:* guía SOPR; semana 32.
4. **¿Por qué no usar el saldo en exchanges como señal de venta o compra?**
   - *Respuesta:* son etiquetas incompletas y revisables ("lower bounds", "retrospective revisions").
   - Con Coin Metrics, el saldo saltó +46,954 BTC en un día con flujo neto de +3,192 BTC. Y el signo difiere entre proveedores: Glassnode veía entradas, Coin Metrics salidas.
   - *Fuente:* Exchange Data Transparency Notice; cálculo propio con Coin Metrics.

## 7. Grado de evidencia

- **A:** las definiciones, que son identidades contables.
- **B:** los niveles de precio realizado y MVRV; coinciden con Coin Metrics y BGeometrics con ±1% de diferencia.
- **C:** las cohortes (STH/LTH) y el costo base STH, reproducibles solo con proveedores de terceros y con retraso.
- **D:** umbrales y narrativas semanales usados como señal de timing.
- **Global: C.**
