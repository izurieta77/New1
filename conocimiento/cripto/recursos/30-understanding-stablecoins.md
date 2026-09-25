# 30 · Understanding Stablecoins (FMI, Departmental Paper 25/09)

> Ficha de recurso · Grupo G5 · Estudiada el 25-sep-2026 por `analista-cripto` · **Acceso: íntegro** (PDF oficial de 56 páginas, leído completo) · **Grado global: B**; **A** en la descripción de las leyes.
>
> **Etiquetas:**
> - **[H]** hecho con fuente y página;
> - **[I]** inferencia (digo si es del autor o nuestra);
> - **[O]** opinión del autor.
>
> **Grados:** A = identidad o dato oficial · B = evidencia sólida con salvedades · C = muestra corta o no reproducible · D = narrativa.
>
> **"p. N"** es la página **impresa** del documento. En el PDF corresponde a la página N + 3.

## 1. Ficha

| Campo | Dato |
|---|---|
| Año | 2025. Departmental Paper No. 25/09, diciembre de 2025; el PDF se creó el 1-dic-2025 y la URL tiene fecha 2-dic |
| Autor | Fondo Monetario Internacional, Departamento de Mercados Monetarios y de Capital. Quince autores: Tobias Adrian, Parma Bains, Marianne Bechara, Eugenio Cerutti, Stephanie Forte, Federico Grinberg, Alessandro Gullo, Martina Hengge, Agnija Jekabsone, Kathleen Kao, Tommaso Mancini Griffoli, Soledad Martinez Peria, Marcello Miccoli, Marco Reuter y Nobuyasu Sugimoto. Coordinaron Miccoli y Sugimoto |
| Tipo | Documento departamental de síntesis. Él mismo dice que "largely summarizes the state of play without developing new policy lines" (p. 3) |
| Costo | Gratis. ISBN 9798229026994 (WebPDF) |
| URL | https://www.imf.org/en/publications/departmental-papers/issues/2025/12/02/understanding-stablecoins-570602 · PDF: https://www.imf.org/-/media/files/publications/dp/2025/english/usea.pdf |
| **Conflictos de interés** | No tiene interés financiero en los activos. Sí tiene un **sesgo institucional**: su mandato es la estabilidad y la soberanía monetaria, por eso resalta riesgos como la sustitución de moneda y los flujos de capital. Entre sus recomendaciones está no dar a las criptos curso legal (p. 33). Las opiniones "do not necessarily represent the views of the IMF" |

## 2. Acceso real

- **Cómo lo obtuve:** la página HTML de imf.org responde 403 (bloqueo del CDN) y el PDF de elibrary responde con un desafío anti-bots. Obtuve el **PDF oficial** desde la URL de imf.org con la herramienta de lectura web: 56 páginas, sha256 `06621b8c…0af06`.
- **Qué leí:** con `pypdf`, el texto completo de las 56 páginas: resumen, 9 secciones, 6 recuadros, 2 tablas y referencias.
- **Figuras revisadas a mano:** 2, 3 y 4 (pp. 15-16) y 7 (p. 24).
- **Nivel: íntegro.**

## 3. Lo esencial

- **[H] Siete rasgos definen a una stablecoin (p. 8):**
  - emisor privado;
  - denominación en una moneda existente;
  - valor expresado en esa moneda;
  - mecanismo de estabilidad: reservas o algoritmo;
  - **sin remuneración directa**;
  - transferible entre pares;
  - registrada en blockchains públicas.
  - El documento se enfoca en las stablecoins respaldadas por activos financieros en moneda fiduciaria.
- **[H] Tamaño:** la emisión se duplicó desde 2024, a **≈ US$300 mil M en sep-2025**. Eso es solo ≈ **7%** de la capitalización cripto (la mitad de su peso de 2022) y 0.5% de la bolsa de EUA (p. 14).
- **[H] ≈ 80% de las transacciones con stablecoins las hacen bots y sistemas automáticos** de arbitraje y rebalanceo (Visa Onchain Analytics, últimos 3 meses a nov-2025; p. 14, nota 17).
- **[H] Concentración:**
  - USDT y USDC tienen ≈ **90%** del mercado;
  - Tether está domiciliada en **El Salvador** y Circle en EUA;
  - negociaron **US$23 billones** en 2024, +90% contra 2023 (pp. 14-15);
  - el **97%** de la emisión está atada al dólar (p. 15).
- **[H] Reservas (p. 15; figura 2):**
  - USDC: 40% en T-bills, 45% en reportos (reverse repos) a un día con Treasuries y el resto en depósitos. BlackRock las administra, con plazo promedio de 14 días y rendimiento ≈ 4%.
  - Tether: ≈ 75% en Treasuries de corto plazo (incluidos reportos), ≈ **5% en bitcoin** y una proporción similar en oro.
- **[H] Canje limitado (p. 9, nota 12):** USDC y USDT piden registro y cobran comisión. **USDT exige un canje mínimo de US$100,000.** Quien no está registrado solo puede vender en el mercado secundario. La paridad la sostienen **arbitrajistas** con acceso al canje (Ma, Zeng y Zhang 2025, NBER 33882).
- **[H] Paridad (p. 16; figura 3):**
  - ≈ **99% de las desviaciones intradía quedaron dentro de 1%**;
  - excepciones: USDC cotizó **12% abajo** en mar-2023 (Silicon Valley Bank) y USDT perdió la paridad en may-2022 (Terra);
  - en ambos casos pasaron ≈ **2 días** debajo de 1;
  - Circle tenía ≈ US$3.3 mil M en SVB y USDC tocó ≈ US$0.88 (p. 25, nota 36).
- **[H] Riesgo de corrida:** los grandes emisores no dan derecho de canje a todos los tenedores en todas las circunstancias. Eso crea una **ventaja para el primero que sale** y, en una corrida, ventas forzadas de T-bills y reportos (pp. 23-24).
- **[H] Pagos transfronterizos:**
  - los flujos de stablecoins superaron a los de criptos sin respaldo a inicios de 2022 (p. 16);
  - suman ≈ US$1.5 billones (2024) frente a ≈ US$1,000 billones de pagos transfronterizos globales (p. 17, recuadro 2).
- **[H] Proyecciones a 2030 entre US$0.5 y 3.7 billones (p. 19, nota 22):**
  - Citi: escenario base de 1.5 billones en 2030;
  - Standard Chartered: 2 billones en 2028;
  - J.P. Morgan: 500 mil M en 2028;
  - Tesoro de EUA: 2 billones en 2028;
  - Bessent: 3.7 billones.
- **[H] Costo:** mandar US$500 con stablecoins costaba US$5-10, contra US$20-30 por las vías tradicionales (Adams et al. 2023). Las comisiones de entrada y salida son "quite substantial" (p. 20, nota 24).
- **[H] T-bills (p. 24, nota 33):**
  - las stablecoins tienen ≈ **2% de los T-bills** en circulación;
  - +US$3.5 mil M de emisión bajan el rendimiento **2 pb** y −3.5 mil M lo suben **6-8 pb**, un efecto asimétrico (Ahmed y Aldasoro 2025, BIS WP 1270).
- **[H] Sustitución de moneda (p. 26):** de 2020 a 2024, las tenencias de stablecoins pasaron de casi cero a 1.5% de los depósitos totales en África y Medio Oriente y a **2.7% en América Latina y el Caribe**. Los depósitos en moneda extranjera son el 20% y el 25%, respectivamente.
- **[H] Cinco elementos comunes de las regulaciones (p. 40):**
  1. emisor autorizado;
  2. respaldo 1:1 con activos líquidos en la misma moneda;
  3. segregación de las reservas;
  4. derecho legal de canje;
  5. **prohibido pagar intereses**.
- **[H] Diferencias entre GENIUS y MiCA (pp. 40-41, notas 70-73):**
  - GENIUS **no** deja emitir directamente a los bancos comerciales (solo por medio de una subsidiaria); MiCA sí deja a las instituciones de crédito;
  - MiCA exige una entidad en la UE; GENIUS acepta emisores extranjeros con un régimen comparable;
  - GENIUS reforma la ley de quiebras para dar prioridad a los tenedores.
- **[H] MiCA (pp. 42-43; notas 78-79):**
  - en vigor desde jun-2023;
  - separa los tokens de dinero electrónico (una sola moneda) de los tokens referenciados a activos;
  - umbrales de emisor "significativo": €5 mil M de capitalización, 10 M de tenedores y 2.5 M de transacciones o €500 M al día;
  - prohíbe intereses tanto al emisor como a los proveedores de servicios cripto (CASP);
  - capital: el mayor de €350 mil, ¼ de los gastos fijos o 2% de las reservas (3% si es significativo);
  - liquidez: ≥ 30% en efectivo o equivalentes (60% si es significativo), ≥ 20% con vencimiento diario (40%) y 30% a una semana (60%);
  - auditoría del respaldo cada 6 meses.
- **[H] GENIUS (p. 44):**
  - reservas en efectivo, depósitos a la vista, cuenta en la Fed, T-bills, fondos de mercado de dinero gubernamentales y ciertos reportos;
  - sin rehipotecar las reservas, salvo excepciones;
  - régimen estatal para emisores de menos de US$10 mil M;
  - certificación mensual de las reservas, examinada por un contador público;
  - las "payment stablecoins" **no son** depósitos, valores ni commodities;
  - la ley no da acceso a los sistemas de pago de la Fed.
  - Tether "is domiciled in El Salvador and not subject to a full, independent audit or 1:1 backing… at this time".
- **[H] Propuesta del Reino Unido para stablecoins sistémicas (pp. 45-46, nota 89):**
  - ≥ 40% de las reservas en depósitos sin remuneración en el Banco de Inglaterra y hasta 60% en gilts de corto plazo;
  - canje a la par el mismo día;
  - límites de tenencia de £20 mil por persona y £20 M por empresa.
- **[H] La revisión de pares del FSB (oct-2025) encontró pocos marcos alineados por completo** (p. 35). Brechas en gestión de riesgos, colchones de capital y planes de resolución. La cooperación transfronteriza es "fragmented, inconsistent, and insufficient" (p. 40).
- **[O] Conclusión del FMI:** MiCA es la regulación más completa hoy. La primera línea de defensa contra la sustitución de moneda son las políticas macro sólidas, no la regulación de stablecoins (p. 47).

## 4. Qué cambia para invertir

- **El riesgo de paridad es de colas cortas con dos mecanismos distintos.**
  - Uno es el **banco o custodio de las reservas**: USDC en 2023.
  - El otro es el **contagio del ecosistema**: USDT con Terra en 2022.
  - Hay un tercero que el FMI no cubre: la **congelación de liquidez en DeFi**. En abr-2026, el exploit de KelpDAO dejó los mercados de USDC y USDT de Aave al 100% de utilización ≈ 135 horas, según CoinDesk del 20 y 21-abr-2026. La stablecoin mantuvo su paridad, pero el depósito quedó atrapado.
  - [I, nuestra] Para la cuenta de Binance, **la reserva va en MXN** (decisión del comité) y USDT se usa solo de paso en la ruta MXN→USDT→BTC. El FMI da dos motivos: el canje mínimo de US$100 mil y la falta de auditoría completa de Tether (pp. 9 y 44).
  - **Adenda (25-sep-2026, G4):** el dato del FMI (dic-2025) quedó desactualizado el 13-ago-2026, cuando Tether anunció una opinión sin salvedades de KPMG EUA sobre sus estados de 2025 (confirmada por KPMG). No cambia la decisión: el colchón de Tether sigue delgado (2.2% de sus pasivos) y una caída conjunta de 16.7% en BTC y oro lo borra (ver `conocimiento/cripto/04-riesgos-fraude-hackeos-y-seguridad.md`, contradicción #11). El canje mínimo de US$100 mil sí sigue vigente.
- **Las stablecoins miden la liquidez en dólares dentro de cripto.**
  - Con DefiLlama, la oferta creció **+49.6% en 2025** (205.9 → 308.0 mil M) y **+1.9% en 2026** al 25-sep (313.9), con pico de 322.4 el 17-may-2026.
  - [I, nuestra] Una oferta plana significa que no entran dólares nuevos. Glassnode (semana 37) usa una banda de crecimiento a 30 días de 1.5-2.9% como "combustible"; eso es grado C.
- **Hoy las stablecoins son parte de la plomería del mercado de Treasuries.** Una corrida vendería T-bills y reportos (p. 24) y el efecto en tasas es asimétrico (+6-8 pb por cada −US$3.5 mil M). Es un canal de contagio en ambos sentidos entre cripto y el mercado monetario de EUA.
- **Regulación:**
  - GENIUS es ley desde el 18-jul-2025 (ficha 35), pero su implementación va en 2026-2027: la propuesta de FinCEN y OFAC sobre AML de emisores se publicó en el Federal Register el 10-abr-2026.
  - Por la categoría de CoinGecko al 25-sep-2026, las stablecoins marcadas como "GENIUS Act compliant" suman US$75.5 mil M de un total de US$292.7 mil M: ≈ 26%. **USDT (US$183.75 mil M) domina y el FMI dice que no tiene auditoría completa.** Etiquetado de un tercero; no lo verifiqué contra listas oficiales.
- **Contexto para México:** en la categoría de CoinGecko las stablecoins en MXN apenas suman ≈ US$0.26 M. En la región, la sustitución avanza por la vía del USD (2.7% de los depósitos en América Latina, p. 26).

## 5. Contrapuntos y límites

- **Datos de sep-nov-2025.** Después la oferta se estancó: +1.9% en 2026 con DefiLlama. El documento no alcanza a ver la desaceleración.
- **Síntesis sin análisis nuevo** (p. 3). No modela la probabilidad de corrida ni el tamaño de una pérdida de paridad; es cualitativo.
- **Varias cifras son de terceros** (CoinGecko, Visa Onchain Analytics, Chainalysis) o de trabajos "forthcoming".
- **Sesgo hacia el riesgo macro.** Casi no trata el riesgo de contraparte para el usuario (exchanges, congelamientos de fondos, DeFi) ni compara con los riesgos del sistema bancario tradicional.
- **La proporción USD varía por fuente:** 97% (FMI, p. 15), 99.8% (a16z con Artemis, lám. 23) y 99.1% (categoría de CoinGecko, 25-sep-2026). Depende de qué monedas cuenta cada una.

## 6. Autoexamen

1. **¿Por qué un minorista con USDT puede vender debajo de US$1 aunque Tether sea solvente?**
   - *Respuesta:* el canje directo pide registro, comisión y un **mínimo de US$100,000**, así que el minorista depende del mercado secundario. La paridad la mantienen arbitrajistas con acceso al canje y, bajo estrés, gana el que sale primero.
   - *Fuente:* FMI p. 9, nota 12, y p. 23; Ma, Zeng y Zhang (NBER 33882).
2. **Da los cinco elementos comunes de las regulaciones y dos diferencias entre GENIUS y MiCA.**
   - *Respuesta:* emisor autorizado; 1:1 con activos líquidos en la misma moneda; segregación; derecho de canje; sin intereses.
   - Diferencias: MiCA deja emitir a las instituciones de crédito y GENIUS solo por medio de una subsidiaria. MiCA exige una entidad en la UE y GENIUS acepta extranjeros con régimen comparable.
   - *Fuente:* pp. 40-41, notas 70-71.
3. **¿Qué parte de los T-bills tienen las stablecoins y cuál es el efecto estimado de ±US$3.5 mil M de emisión?**
   - *Respuesta:* ≈ 2%. +3.5 mil M baja el rendimiento 2 pb; −3.5 mil M lo sube 6-8 pb.
   - *Fuente:* p. 24 y nota 33 (Ahmed y Aldasoro 2025).
4. **¿Qué dice la evidencia sobre las pérdidas de paridad de USDT y USDC?**
   - *Respuesta:* ≈ 99% de las desviaciones intradía quedaron dentro de 1%. USDC cayó 12% (≈ US$0.88) en mar-2023 por SVB y USDT perdió la paridad en may-2022 por Terra. En ambos casos pasaron ≈ 2 días debajo de 1.
   - *Fuente:* p. 16, figura 3, y p. 25, nota 36.

## 7. Grado de evidencia

- **A:** el resumen de las leyes (MiCA, GENIUS, Japón y la propuesta del Reino Unido).
- **B:** los datos de mercado citados de terceros, cuyo orden de magnitud cuadra con DefiLlama, CoinGecko y a16z.
- **C:** las proyecciones de terceros a 2030, con un rango de 7×.
- **Global: B.**
