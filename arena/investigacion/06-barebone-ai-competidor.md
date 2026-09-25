# Barebone AI: qué es, qué evidencia tiene y cómo competir contra ella

Fecha: 25-sep-2026 · Método: investigación con WebSearch/WebFetch al sitio oficial (barebone.ai y subpáginas), fichas de App Store/Google Play, LinkedIn del fundador, Caplight (base de datos de startups) y reseñas de terceros (agent-finder.co, mwm.ai, quasa.io). Cada afirmación abajo lleva su tipo de fuente y confiabilidad, según la regla de `conocimiento/registro-de-errores.md` y `.claude/agents/verificador.md`.

## 1. Qué es, en una frase

Un terminal de investigación de inversión con IA (preguntas en lenguaje natural, análisis tipo "escritorio institucional") que **no gestiona portafolios ni ejecuta operaciones** — confirmado en tres fuentes independientes entre sí: el propio sitio ("Research-only tool with no trade execution capability"), una reseña de terceros, y el propio fundador en LinkedIn ("Barebone does not create trading algorithms"). Compite en la categoría de copiloto de research/señales, no en la de toma de decisión con control de riesgo — no es 1:1 comparable con nuestro sistema, que sí aspira a decidir con veto de riesgo.

## 2. Producto y arquitectura declarada [sitio_oficial_barebone / media-alta]

- 20+ "research skills" (cada una descrita como "a dedicated AI analyst"), 11+ modelos analistas, 70+ fuentes de datos institucionales (cifras de la ficha de tienda, no verificadas una por una).
- **No revelan qué modelo de IA usan.** Ni GPT, ni Claude, ni Gemini — solo "a proprietary architecture that selects the right combination of AI models". Caja negra total.
- Funciones: precios de entrada/salida ("When to Buy and Sell"), rastreo de smart money (13F de superinversores, Form 4 de insiders, trades del Congreso de EUA), monitoreo de portafolio 24/7, acceso de solo lectura a la cuenta conectada (no puede mover fondos ni ejecutar).
- Fundada en 2025, San Francisco, ~4 empleados, sin ronda de financiamiento pública (Caplight). Tráfico web +234% en abr-2026 y +79% m/m en may-2026 (Caplight), desde base pequeña (2.2K → 13K visitas/mes).

## 3. Fundadores: parcialmente verificable, no del todo [prensa_o_terceros / alta para lo confirmado]

Solo un fundador tiene identidad pública verificable de forma cruzada: **Brian Yu Fung Tam** — economía en LSE, analista de verano en Warburg Pincus (2019), ~3 años en Goldman Sachs (equipo Hybrid Capital, desde 2020), confirmado por un podcast independiente ("Geeks of the Valley") y su perfil de LinkedIn. El sitio afirma "built by ex-Goldman Sachs investment bankers" **en plural**; una reseña de terceros menciona un segundo cofundador ("an AI engineer formerly at Hanson Robotics") que **nunca aparece nombrado en ninguna fuente**. Bandera roja de verificación, no de fraude necesariamente — pero la pluralidad no está sostenida.

## 4. Evidencia de resultados: la pieza más débil [mixto, ver detalle]

- **Cero cifras de rendimiento en el sitio oficial, /about, /mission o los Términos de Servicio.** Ninguna.
- Las únicas dos cifras existen solo en LinkedIn, fuera del sitio oficial:
  - +77.3% en 2025 (vs. S&P 500 +18.44%, Nasdaq +22.63%), calculado como diferencia simple de tamaño de portafolio entre dos fechas, sobre ~150 operaciones **ejecutadas por humanos** siguiendo señales de la IA. Sin auditor externo, sin garantía de que el portafolio citado sea representativo (riesgo de cherry-picking).
  - +41% en 3 días con una acción china (Minimax) tras su IPO — un caso puntual, con el propio descargo "This doesn't happen every time. AI isn't magic."
- **Descargo legal textual (Términos de Servicio, §21):** *"we do not provide financial advice or investment advice... We are an AI tool and may make mistakes. You should consult with a qualified financial advisor..."* No está registrada como asesor de inversión (RIA) ante la SEC ni opera como broker-dealer.
- Un revisor externo independiente (agent-finder.co) señala explícitamente: **"we haven't verified long-term monitoring accuracy over a multi-month portfolio"** — no hay track record de terceros.
- La página "Best AI Investing Apps" que posiciona a Barebone como #1 está **autopublicada por la propia Barebone** en su dominio, sin aviso de conflicto de interés — no es una comparativa independiente pese al formato.
- No se localizó ninguna cobertura de prensa financiera de referencia (Bloomberg, TechCrunch, Forbes) que evalúe sus resultados de forma propia.
- Reseñas de usuarios: patrón mixto — elogios por ahorro de tiempo, pero quejas repetidas y concretas sobre alucinaciones e información incorrecta.
- Métricas inconsistentes entre sus propias páginas: 30,000+ / 50,000+ / 100,000+ usuarios según la página; 4.5 vs. 4.8 en calificación de App Store; un agregador externo reporta 3.5-4.0★ con 14 de 52 reseñas de una sola estrella.

## 5. Precios [tienda_de_apps / alta]

El sitio **no publica precios** (`barebone.ai/pricing` da 404). Los precios reales solo están en la ficha de App Store:

| Plan | Semana | Mes | Año |
|---|---|---|---|
| Barebone Plus | $3.99 | $15.00 | $179.99 |
| Barebone Pro | $7.99 | $29.00 | $209–$349 |

Prueba gratuita de 7 días; cancelación desde la tienda de apps, efectiva al final del periodo pagado (no inmediata). Reseñas de usuarios reportan haber sido dirigidos, tras un cuestionario largo, a pagar $20-40/mes — cifras distintas a las oficiales, posible A/B testing de paywall.

## 6. Fortalezas reales frente a nuestro sistema

- Cobertura empaquetada amplia y ya en producción (13F, insiders, Congreso, 70+ fuentes).
- Founder story parcialmente verificable y creíble (LSE + Goldman Sachs para Brian Tam).
- Tracción de usuarios y app funcional, con precios reales cobrando hoy.

## 7. Debilidades explotables

- Cero evidencia auditada de resultados — es exactamente el punto donde nuestro sistema ya tiene más rigor (registro de errores, doble ejecución independiente, examen de titulación, verificación adversarial con etiqueta de fuente).
- Caja negra de modelo subyacente.
- Su propio ToS los exime de responsabilidad por la fiabilidad de las señales; no son un asesor de inversión registrado.
- Métricas de usuarios y calificaciones inconsistentes entre sus propias páginas.

## 8. Qué copiar y qué no

**Copiar:** ampliar nuestra cobertura de 13F/insiders/trades del Congreso si no está completa; empaquetar hallazgos del comité en unidades claras y nombradas (al estilo "skills"); una interfaz conversacional/móvil para consumir los memorandos del comité.

**No copiar:** opacidad de precios, cifras de rendimiento sin auditar publicadas solo en redes sociales, caja negra del modelo, inconsistencia de métricas entre páginas propias.

## 9. Veredicto: dónde es realista "superarlos"

No en usuarios ni tráfico — ya tienen tracción y nosotros empezamos hoy. El terreno medible y alcanzable: **track record auditado y calibrado públicamente** (Brier score, portafolio de papel con metodología replicable y fuente primaria citada por cifra) — algo que Barebone tiene en cero pese a llevar meses operando y cobrando. Segundo terreno: comunicar la distinción categórica entre "decisión con veto de riesgo cuantificado" y "solo research sin responsabilidad legal" (su propio ToS los exime de esa responsabilidad; nuestro sistema no se exime, se audita).

## Qué no se pudo verificar de forma independiente

No pude confirmar el segundo cofundador que menciona una reseña de terceros, ni auditar directamente el portafolio de LinkedIn del founder (no hay acceso a su cuenta de corretaje), ni encontrar cobertura de prensa financiera de peso. Todo lo anterior queda marcado como "no localizado", no como "no existe", siguiendo la regla del sistema.
