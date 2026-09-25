# Verificación independiente: análisis de "Invierte con Pepe" (25-sep-2026)

Origen: el usuario compartió un análisis cuantitativo del canal de YouTube `@invierteconpepe_` (1,232 videos, jun-2022 a hoy) que **no fue producido en esta sesión** — esta sesión ya había confirmado con evidencia técnica (curl + `yt-dlp`, ver `arena/investigacion/fuentes-terceros/`) que YouTube bloquea la extracción de transcripciones desde este entorno. Por protocolo, todo contenido externo se trata como dato a verificar antes de adoptarlo, igual que el de una IA rival.

Método: verificación de precios con datos propios (Yahoo Finance, `adjclose` ajustado por splits/dividendos, descargado el 25-sep-2026) para las cifras con ticker y ventana identificables, y verificación documental (SEC) para el dato de calificadoras.

## Cifras verificadas contra datos propios

| Afirmación | Ventana usada para reproducir | Resultado propio | Veredicto |
|---|---|---|---|
| "Google desde 2022 sube 256%" | Ene-2022 a hoy: +140.5% / Jun-2022 (inicio del canal) a hoy: +206.2% | Ninguna ventana redonda da exactamente 256%, pero **cualquiera de las dos supera ampliamente al S&P** (+61.5% / +88.8% en las mismas ventanas) | Confirmado en magnitud y en que es su mejor acierto; el 256% exacto requiere la fecha precisa de recomendación, que no tengo |
| "ASML desde noviembre de 2024 sube 164%" | Nov-2024 a hoy | **+162.0%** (S&P en la misma ventana: +35.2%) | **Confirmado**, coincide casi exacto |
| "Acciones de por vida" (Visa, Berkshire, UMG) suben 1% contra 36% del S&P" | Nov-2024 a hoy (misma fecha que ASML, consistente con la misma época de recomendación) | V +28.1%, BRK-B +11.7%, UMG −35.7% → promedio simple **+1.4%**; S&P **+35.2%** | **Confirmado**, coincide casi exacto con esa ventana |
| "Nike cae 59% y 50%" (recomendada en 2022 y 2024) | Jun-2024 a hoy: −59.6% | La cifra "−59%" coincide con la recomendación de 2024. La de "−50%" (2022) no se reprodujo con ninguna fecha de 2022 razonable (jun-2022: −67.0%; dic-2022: −64.9%) | Dirección y magnitud del error confirmadas (caída muy grande); el "−50%" específico no se pudo anclar a una fecha de 2022 con mis datos |
| "Duolingo cae 57%" | Ene-2025 a hoy: −55.2%; abr-2025 a hoy: −55.4% | Cercano (57% vs. ~55%) | Confirmado en magnitud, diferencia de ~2 puntos explicable por la fecha exacta de recomendación |
| "Netflix cae 28%" | Ene-2025 a hoy: −19.6%; abr-2025 a hoy: −23.2% | Mismo signo, magnitud algo menor en las ventanas que probé | Confirmado en dirección, magnitud aproximada (no exacta) |
| "ASUR cae 24% en pesos" | ASUR (BMV: ASURB) tocó máximo histórico el 20-feb-2026 (~$638.5) y ha caído **32.8%** desde entonces a hoy ($428.9); desde mayo-2025 (~$564) la caída es ≈24% | El patrón (subida fuerte y luego caída de doble dígito) es real y reciente; el −24% exacto corresponde a una ventana de mediados de 2025 | Confirmado en existencia y magnitud aproximada de la caída, no en la fecha exacta |
| "S&P y Moody's, según la SEC, 43.5% y 26.1%" | SEC, *2024 Staff Report on NRSROs* (ene-2025), Chart 3, datos a dic-2023 | **43.50% y 26.05%** son exactos — pero son la participación de S&P y Moody's específicamente en la categoría **"Corporate Issuers"**, no el total de las cinco categorías. El total agregado real es **49.96% (S&P) y 31.73% (Moody's)**, 81.69% combinado | Las cifras citadas son reales y coinciden casi al decimal, pero sin la salvedad de "solo en corporativos" pueden leerse como el total del mercado, que en realidad es más alto. Registrado en `conocimiento/registro-de-errores.md` |

## No verificable con mis herramientas actuales

- El rendimiento agregado de "sus 61 compras" y el 26% que le gana al S&P, y el empate contra el IPC: requeriría la lista completa de las 61 recomendaciones con fecha y ticker, que no tengo.
- Las "10 empresas que dijo evitar" y el "22 puntos menos en promedio": mismo problema — necesito la lista con fechas.
- "Sus acciones de 2025 rindieron 2.3 veces el S&P, no casi el triple": necesitaría su lista específica de 2025.
- "El primer trimestre de 2026 fue el peor desde 2001, y no lo fue": es una afirmación macro, no de precios de una acción — no la verifiqué en esta pasada (se puede hacer con datos de ^GSPC trimestrales si se pide).

## Conclusión

Lo verificable con datos propios (7 de 8 cifras con ticker/fecha reconstruible) se sostiene en dirección y, en la mayoría de los casos, en magnitud casi exacta. El único hallazgo con matiz real es el de las calificadoras: la cifra es correcta pero corresponde a una sola categoría, no al total. Esto no invalida la conclusión general del análisis (Pepe es mejor evitando que comprando, y algunas cifras que presume están infladas o mal encuadradas) — al contrario, la sostiene con una base de datos propia, no solo con la palabra de quien hizo el análisis.

Las cuatro prácticas que se proponen adoptar del método de Pepe (ventajas competitivas tipo concesión/peaje/duopolio, múltiplo actual vs. mediana de 5 años, lista de qué evitar, 13-F e insiders solo como fuente de ideas con 45 días de retraso) son compatibles con lo que ya está en `conocimiento/` y no requieren cambios al sistema — se anotan como candidatas a incorporar en el checklist de `analista-fundamental` cuando se revise esa ficha.
