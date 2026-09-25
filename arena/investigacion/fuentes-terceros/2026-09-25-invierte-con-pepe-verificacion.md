# Verificación independiente: análisis de "Invierte con Pepe" (25-sep-2026)

Origen: el usuario compartió un análisis cuantitativo del canal de YouTube `@invierteconpepe_` (1,232 videos, jun-2022 a hoy) que **no fue producido en esta sesión** — esta sesión ya había confirmado con evidencia técnica (curl + `yt-dlp`, ver `arena/investigacion/fuentes-terceros/`) que YouTube bloquea la extracción de transcripciones desde este entorno. Por protocolo, todo contenido externo se trata como dato a verificar antes de adoptarlo, igual que el de una IA rival.

Método: verificación de precios con datos propios (Yahoo Finance, `adjclose` ajustado por splits/dividendos, descargado el 25-sep-2026) para las cifras con ticker y ventana identificables, y verificación documental (SEC) para el dato de calificadoras.

## Cifras verificadas contra datos propios

Tipo de fuente en cada fila: **cálculo propio** (precio bajado por mí de Yahoo Finance y calculado con Python) o **reporte narrativo** (documento SEC en prosa, con su fecha de corte propia).

| Afirmación | Tipo de fuente | Ventana usada para reproducir | Resultado propio | Veredicto |
|---|---|---|---|---|
| "Google desde 2022 sube 256%" | Cálculo propio | Ene-2022 a hoy: +140.5% / Jun-2022 (inicio del canal) a hoy: +206.2% | Ninguna ventana redonda da exactamente 256%, pero **cualquiera de las dos supera ampliamente al S&P** (+61.5% / +88.8% en las mismas ventanas) | Confirmado en magnitud y en que es su mejor acierto; el 256% exacto requiere la fecha precisa de recomendación, que no tengo |
| "ASML desde noviembre de 2024 sube 164%" | Cálculo propio | Nov-2024 a hoy | **+162.0%** (S&P en la misma ventana: +35.2%) | **Confirmado**, coincide casi exacto |
| "Acciones de por vida" (Visa, Berkshire, UMG) suben 1% contra 36% del S&P" | Cálculo propio | Nov-2024 a hoy (misma fecha que ASML, consistente con la misma época de recomendación) | V +28.1%, BRK-B +11.7%, UMG −35.7% → promedio simple **+1.4%**; S&P **+35.2%** | **Confirmado**, coincide casi exacto con esa ventana |
| "Nike cae 59% y 50%" (recomendada en 2022 y 2024) | Cálculo propio | Jun-2024 a hoy: −59.6% | La cifra "−59%" coincide con la recomendación de 2024. La de "−50%" (2022) no se reprodujo con ninguna fecha de 2022 razonable (jun-2022: −67.0%; dic-2022: −64.9%) | Dirección y magnitud del error confirmadas (caída muy grande); el "−50%" específico no se pudo anclar a una fecha de 2022 con mis datos |
| "Duolingo cae 57%" | Cálculo propio | Ene-2025 a hoy: −55.2%; abr-2025 a hoy: −55.4% | Cercano (57% vs. ~55%) | Confirmado en magnitud, diferencia de ~2 puntos explicable por la fecha exacta de recomendación |
| "Netflix cae 28%" | Cálculo propio | Ene-2025 a hoy: −19.6%; abr-2025 a hoy: −23.2% | Mismo signo, magnitud algo menor en las ventanas que probé | Confirmado en dirección, magnitud aproximada (no exacta) |
| "ASUR cae 24% en pesos" | Cálculo propio | ASUR (BMV: ASURB) tocó máximo histórico el 20-feb-2026 (~$638.5) y ha caído **32.8%** desde entonces a hoy ($428.9); desde mayo-2025 (~$564) la caída es ≈24% | El patrón (subida fuerte y luego caída de doble dígito) es real y reciente; el −24% exacto corresponde a una ventana de mediados de 2025 | Confirmado en existencia y magnitud aproximada de la caída, no en la fecha exacta |
| "S&P y Moody's, según la SEC, 43.5% y 26.1%" | Reporte narrativo (SEC) | *2024 Staff Report on NRSROs* (ene-2025), Chart 3, datos a dic-2023 | **43.50% y 26.05%** son exactos — pero son la participación de S&P y Moody's específicamente en la categoría **"Corporate Issuers"**, no el total de las cinco categorías. El total agregado real es **49.96% (S&P) y 31.73% (Moody's)**, 81.69% combinado | Las cifras citadas son reales y coinciden casi al decimal, pero sin la salvedad de "solo en corporativos" pueden leerse como el total del mercado, que en realidad es más alto. Registrado en `conocimiento/registro-de-errores.md` |

## No verificable con mis herramientas actuales

- El rendimiento agregado de "sus 61 compras" y el 26% que le gana al S&P, y el empate contra el IPC: requeriría la lista completa de las 61 recomendaciones con fecha y ticker, que no tengo.
- Las "10 empresas que dijo evitar" y el "22 puntos menos en promedio": mismo problema — necesito la lista con fechas.
- "Sus acciones de 2025 rindieron 2.3 veces el S&P, no casi el triple": necesitaría su lista específica de 2025.
- "El primer trimestre de 2026 fue el peor desde 2001, y no lo fue": es una afirmación macro, no de precios de una acción — no la verifiqué en esta pasada (se puede hacer con datos de ^GSPC trimestrales si se pide).

## Segunda ronda (25-sep-2026): corrección del propio usuario sobre las calificadoras

El usuario compartió una versión corregida y ampliada del análisis (278 llamadas en 122 videos, con cita literal, tasa base aleatoria y prueba de significancia), de nuevo **no producida en esta sesión** y sin acceso mío a su script (`/workspace/bolsa/conocimiento/youtube/invierteconpepe/verificacion/v2/reproducir.sh` no existe en este entorno — no puedo ejecutarlo ni reproducirlo). Verifiqué lo único con fuente primaria pública: el dato de las calificadoras.

Bajé directamente el reporte de la SEC publicado en **abril de 2026** (`2025-ocr-staff-report-compliant-4-24-26.pdf`, tipo de fuente: **reporte narrativo** — solo revisé este índice, no el de bases estadísticas, error que se corrige más abajo) y confirmé:

- **Cubre datos al 31-dic-2024, no al 31-dic-2025.** Texto literal: "the calendar year ending December 31, 2024". Esto confirma la afirmación del usuario de que la SEC **todavía no ha publicado** datos a diciembre de 2025 — cualquier cifra "a 2025" (como los conteos de 1,077,798 / 684,055 / 2,192,543 que el usuario marca como no verificables) no puede venir de un reporte oficial existente.
- **Los tres "grandes" NRSRO (Fitch + Moody's + S&P) suman 93.38% del total a dic-2024**, texto literal: "The large NRSROs accounted for 93.38% of all the ratings outstanding as of December 31, 2024, a small decrease from their share of 94.15% of all the ratings outstanding as of December 31, 2023." El 94.15% de 2023 coincide exactamente con lo que yo mismo extraje del reporte anterior en la primera ronda de esta verificación.
- Las cifras individuales de S&P y Moody's para 2024 están en un gráfico (Chart 5) sin texto extraíble por `pypdf`, así que no pude leer el 80.99% dígito por dígito. Pero es consistente: 93.38% (los tres grandes) − 80.99% (S&P+Moody's) = 12.39% para Fitch, cifra razonable frente al 12.46% que Fitch tenía en 2023.

**Veredicto: la corrección del usuario sobre las calificadoras se sostiene** con la fuente primaria más reciente que existe — no pude confirmar el dígito exacto de la partición S&P/Moody's de 2024 por una limitación técnica de extracción (gráfico vs. tabla de texto), pero el total de los tres grandes y la ausencia de datos 2025 sí quedaron confirmados letra por letra contra el PDF oficial.

Las cifras estadísticas del núcleo del análisis (tasas base aleatorias, significancia, 278 llamadas etiquetadas) siguen sin verificación independiente de mi parte: no tengo el dataset ni el script, y no puedo ejecutar código fuera de este entorno. Si se comparte el CSV/JSON de las 278 llamadas con cita, fecha, ticker y bolsa, lo puedo correr contra mis propios precios igual que hice con las 8 cifras de la primera ronda.

## Corrección de mi propio error (25-sep-2026, misma noche): sí existe publicación a diciembre de 2025

En la segunda ronda afirmé que el reporte más reciente de la SEC llegaba solo a datos de dic-2024 y que "cualquier cifra a 2025... no puede venir de un reporte oficial existente". **Eso era falso.** Solo revisé el índice de "Staff Reports" (el documento narrativo en PDF, con su propio ciclo de publicación de ~4 a 16 meses de rezago) y no revisé el índice separado de "Statistics & Data Visualizations" de la SEC, que se actualiza con otro calendario.

Evidencia, bajada y verificada dígito por dígito el 25-sep-2026 — tipo de fuente: **base estadística** (serie de datos con calendario de actualización propio, distinta del reporte narrativo citado arriba):

- URL: `https://www.sec.gov/files/sec-stats-nrsros-20260630.xlsx` (nombre de archivo con fecha 30-jun-2026, hoja "Stats Table"), enlazado desde `https://www.sec.gov/data-research/statistics-data-visualizations/.../nrsros-number-outstanding-credit-ratings-rating-category-nrsro-2024`, que **redirige** a la versión "...-2025" y cuyo texto dice literalmente: *"This data visualization shows the total aggregate number of outstanding credit ratings by rating category and by NRSRO as of December 31, 2025."*
- Fila "Jan 1, 2025 - Dec 31, 2025" de esa hoja: **S&P 1,077,798 · Moody's 684,055 · total 2,192,543.** Estas tres cifras coinciden exactas, dígito por dígito, con las que el usuario había marcado como "no verificables" en la ronda anterior.
- (1,077,798 + 684,055) / 2,192,543 = **80.36%** — coincide exacto con el dato que el usuario reportó.
- Triangulación con la fila de dic-2024 de la misma hoja: S&P 1,066,386 + Moody's 674,813 + Fitch 266,519 = 2,007,718 / 2,150,014 = **93.38%**, que coincide exacto con el 93.38% citado en el texto del *Staff Report* narrativo de abril-2026 para "the large NRSROs" a dic-2024. Dos publicaciones independientes de la SEC dan el mismo número — la hoja de estadísticas es confiable.
- La misma fila de dic-2024 da S&P+Moody's = **80.99%**, que también coincide exacto (no solo "razonable por resta", como concluí antes) con la primera cifra que un rival había dado.

**Los dos rivales tenían razón, cada uno con una fecha de corte distinta** (80.99% a dic-2024, 80.36% a dic-2025); ninguno inventó el dato. Mi error no fue de aritmética sino de cobertura: dije "no existe" habiendo revisado solo una de las dos series que publica la SEC. Corregido en `conocimiento/registro-de-errores.md`.

## Cierre de la comprobación (25-sep-2026) y control añadido

El usuario cerró la comprobación con la misma lectura: el reporte narrativo (abril-2026) analiza certificaciones al 31-dic-2024; la página oficial de estadísticas y visualizaciones (actualizada 30-jun-2026) ya incorpora los conteos a dic-2025 (S&P 1,077,798; Moody's 684,055; total 2,192,543; 80.36% conjunto). Coincide con lo verificado arriba.

Se adopta un quinto control para la v3 de la base y para el verificador del sistema (`.claude/agents/verificador.md`): **toda conclusión debe declarar su tipo de fuente** — reporte narrativo, base estadística, filing regulatorio o cálculo propio — para no volver a mezclar fecha de publicación, fecha de corte y universo estadístico. Aplicado retroactivamente a las tablas de este documento.

## Conclusión

Lo verificable con datos propios (7 de 8 cifras con ticker/fecha reconstruible) se sostiene en dirección y, en la mayoría de los casos, en magnitud casi exacta. El único hallazgo con matiz real es el de las calificadoras: la cifra es correcta pero corresponde a una sola categoría, no al total. Esto no invalida la conclusión general del análisis (Pepe es mejor evitando que comprando, y algunas cifras que presume están infladas o mal encuadradas) — al contrario, la sostiene con una base de datos propia, no solo con la palabra de quien hizo el análisis.

Las cuatro prácticas que se proponen adoptar del método de Pepe (ventajas competitivas tipo concesión/peaje/duopolio, múltiplo actual vs. mediana de 5 años, lista de qué evitar, 13-F e insiders solo como fuente de ideas con 45 días de retraso) son compatibles con lo que ya está en `conocimiento/` y no requieren cambios al sistema — se anotan como candidatas a incorporar en el checklist de `analista-fundamental` cuando se revise esa ficha.
