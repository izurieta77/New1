# Reconocimiento técnico: 7 perfiles de TikTok (finanzas/fiscal), 25-sep-2026

Encargo del usuario: "ve todos los TikTok's" de 7 personajes. No tengo modalidad de video/audio (no puedo "ver" ni "escuchar" literalmente). Esta ficha documenta qué pude extraer por texto y qué no, como due diligence de fuentes antes de usarlas para nada del despacho fiscal o de la arena de inversión.

## Método
1. Descarga cruda de las 7 páginas de perfil (HTTP 200, ~372 KB c/u) y parseo del bloque JSON embebido `__UNIVERSAL_DATA_FOR_REHYDRATION__` → perfil, bio, verificación, seguidores, conteo de videos.
2. `yt-dlp 2026.08.19` (extractor `tiktok:user`) contra el listado de cada perfil → títulos, descripciones, timestamp, vistas/likes/comentarios/guardados de los posts más recientes.
3. Intento de subtítulos/transcripción por video individual (`--write-auto-sub`) → bloqueado.

## Resultado por cuenta (bio/seguidores/videos, verificado del JSON de perfil)

| Cuenta | Nombre | Verificado | Seguidores | Videos | Bio (tal cual) |
|---|---|---|---|---|---|
| mariobeltranmx | Mentor Fiscal \| MB | No | 245,900 | 4,068 | Doctor en Ciencias de lo Fiscal (IEE) y Contador Público Certificado (IMCP) |
| marioreynaguajardo | Mario Reyna Guajardo | No | 391,200 | 657 | Céd. Prof. 11445996, Abogado Fiscalista, Legal Enterprise Firm |
| spuentecoach | Sergio Puente Coach Financiero | No | 303,500 | 1,337 | Estrategias de retiro y jubilación |
| ernestodelbunker | Ernesto del Búnker. | No | 153,300 | 309 | "El Conde de Montecristo" — contenido de estilo/motivación, no perfil fiscal declarado |
| gerardovoficial | Gerardo V | No | 48,100 | 278 | Consultorías propias (quantiveconsult.com), comunidad Skool |
| abolawlex | abolawlex | No | 9,488 | 210 | Lic. y MDF. J. Neptuno Martínez — Abogado de impuestos y Defensa Fiscal |
| arellanesrojas | Arellanes \| Abogado | No | 5,116 | 48 | Amparo, fiscal y administrativo |

Ninguna cuenta trae la palomita azul de verificación de TikTok. Un título o cédula en la biografía es una afirmación no verificada por mí — se trataría igual que cualquier "track record declarado" de `conocimiento/10-evidencia-practicantes-track-records-foros-x.md`: no es evidencia hasta auditarla contra el registro público correspondiente (p. ej. cédula profesional en la SEP, registro ante el IEE si aplica).

## Lo que sí pude leer (2 de 7 cuentas, antes de que el límite de tasa cortara el resto)

`mariobeltranmx`, últimos 5 posts (título/descripción, vistas, likes):
- "¿Cuándo detectar las diferencias del SAT?" — 1,850 vistas, 100 likes
- "IVA retenido enterado fuera de plazo ¿acreditable?" — 4,555 vistas, 255 likes
- "Control interno en los CFDI de ingresos PUE" — 8,423 vistas, 345 likes
- "Las asociaciones religiosas y el ISR" — 4,664 vistas, 245 likes
- "¿Se incluye el IEPS en la base del IVA?" — 5,921 vistas, 345 likes

Son títulos de tema, no el desarrollo ni la postura técnica del video — eso solo está en el audio.

## Lo que NO pude obtener
- **Transcripción o subtítulos de ningún video.** TikTok no expone pistas de subtítulos automáticas vía `yt-dlp` para descarga individual desde este entorno; la extracción por video individual devolvió error ("Unexpected response from webpage request").
- **Listado de posts de 5 de las 7 cuentas** (marioreynaguajardo, gerardovoficial, abolawlex, arellanesrojas, spuentecoach): después de 2 cuentas consecutivas, TikTok empezó a devolver respuestas vacías/anómalas — limitación de tasa por IP, consistente con los marcadores anti-bot ("Verify to continue"/captcha) vistos en la descarga cruda inicial de 2 perfiles.
- No hay forma de "ver" el video (imagen en movimiento) ni "oír" el audio: sin esas dos modalidades, no puedo evaluar tono, lenguaje corporal, ni el contenido hablado real — solo lo que el título/descripción en texto dice.

## Conclusión y recomendación

Puedo hacer reconocimiento de metadatos (quién dice ser, cuántos seguidores, de qué temas habla por título) pero no puedo "ver" los videos en el sentido que pide el usuario, y TikTok limita la extracción incluso de metadatos después de pocas peticiones seguidas.

Alternativa que sí funciona con el mismo rigor que el resto del sistema: si el usuario comparte capturas de pantalla, enlaces puntuales o transcribe/resume una afirmación específica de alguno de estos personajes (p. ej. una postura fiscal, una recomendación de inversión o retiro), la reviso con el mismo protocolo de verificación de dos fuentes que se aplica a todo el sistema (`herramientas`/`conocimiento/registro-de-errores.md`) antes de incorporarla al despacho fiscal o a la arena.

Quedan registradas como fuentes pendientes de monitoreo, no como fuentes validadas.
