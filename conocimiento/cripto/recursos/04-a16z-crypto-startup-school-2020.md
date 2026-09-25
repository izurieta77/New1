# 04 · a16z Crypto Startup School 2020

> Ficha de estudio del grupo G3 DeFi, escrita por `analista-cripto` el 25-sep-2026. Es formación, no recomendación.
> **Acceso:** temario de las 14 clases y descripciones oficiales. **No encontré diapositivas ni transcripciones oficiales**, y no vi los videos.
> **Estado:** resumen.
> **Capítulo de síntesis:** [03-defi-mecanica-riesgos-y-academia.md](../03-defi-mecanica-riesgos-y-academia.md).

## 1. Ficha

| Campo | Dato |
|---|---|
| Año | 2020. Anunciado el 8-nov-2019. Clases presenciales desde finales de febrero de 2020 en Menlo Park, que pasaron a remotas en marzo. Videos publicados cada semana del 13-may al 17-jun-2020. |
| Autor | a16z crypto (Andreessen Horowitz). Ponentes: Chris Dixon, Dan Boneh, Balaji Srinivasan, Josh Williams, Brian Armstrong, Ali Yahya, Sam Williams, Tina Ferguson, Robert Leshner, Jesse Walden, Tom Preston-Werner, Jutta Steiner, Nitya Subramanian y Brian Brooks. |
| Tipo | Curso para fundadores: 14 videos, ~10 h 34 min en total (cálculo propio), y un "*supplementary course reader*" que no localicé. |
| Nivel | Intermedio |
| Costo | Gratis: "*There is no charge and we don't take equity*". |
| Idioma | Inglés |
| URL | [Anuncio (8-nov-2019)](https://a16z.com/introducing-a16z-crypto-startup-school/) · [Videos disponibles (12-may-2020)](https://a16zcrypto.com/posts/article/crypto-startup-school-online/) |

**Conflictos de interés:**

- a16z crypto es un **fondo de capital de riesgo que invierte en cripto**.
- Su propio anuncio dice que los ponentes son "*other members of the a16z Crypto team and portfolio*": socios del fondo (Dixon, Yahya, Walden) y fundadores de empresas del sector, como Armstrong (Coinbase) y Leshner (Compound).
- El descargo de a16z advierte que parte de la información "*has been obtained from third-party sources, including from portfolio companies*".
- El índice del dueño ya lo pide: "*tómalo con la perspectiva de un fondo de capital de riesgo*".

## 2. Acceso real (consultado el 25-sep-2026)

| Fuente | Qué contiene | Nivel |
|---|---|---|
| Anuncio de Chris Dixon en a16z.com (8-nov-2019) | Objetivo, duración y gratuidad | Íntegro |
| Post "*Videos Now Live*" en a16zcrypto.com (12-may-2020) | Cohorte, módulos y alianza con TechCrunch | Íntegro |
| 4 notas semanales de TechCrunch (13-may, 27-may, 10-jun y 24-jun-2020), de Zoran Basich | Descripción de cada semana. Son textos cortos que presentan los videos. | Íntegro |
| Lista de los 14 videos (canal de TechCrunch), con título, duración y vistas, tomada de `ytInitialData` de una lista pública de YouTube (creada por un usuario, "João Faraco") | Temario | Solo metadatos |
| Jesse Walden, "*Progressive Decentralization: A Playbook for Building Crypto Applications*", a16z (8-ene-2020) | Texto oficial del ponente de las clases 9 y 14. **No es la clase.** | Íntegro |

**No localicé:**

- diapositivas ni transcripciones oficiales;
- el "*course reader*". La página original `a16z.com/crypto-startup-school` hoy redirige al acelerador CSX;
- ninguna copia archivada: Internet Archive no es accesible desde aquí;
- los videos: YouTube bloquea yt-dlp. No usé subtítulos automáticos porque no son transcripciones oficiales.
- Un repositorio de GitHub no oficial con notas del curso devolvió 403.

**Nivel: resumen.**

**Temario** (14 videos del canal de TechCrunch; vistas al 25-sep-2026):

| # | Clase | Ponente | Duración | Vistas |
|---|---|---|---|---|
| 1 | Crypto Networks and Why They Matter | Chris Dixon (a16z) | 38:15 | 141K |
| 2 | Blockchain Primitives: Cryptography and Consensus | Dan Boneh (Stanford) | 56:37 | 127K |
| 3 | Applications: Today & 2025 | Balaji Srinivasan | 50:45 | 139K |
| 4 | Opportunities for Crypto in Gaming | Josh Williams | 39:35 | 35K |
| 5 | Setting Up and Scaling a Crypto Company | Brian Armstrong (Coinbase) | 42:26 | 231K |
| 6 | Crypto Business Models | Ali Yahya (a16z) | 45:43 | 90K |
| 7 | Mechanism Design 101 | Sam Williams | 54:00 | 42K |
| 8 | Managing Distributed Workforces | Tina Ferguson | 27:46 | 7K |
| 9 | Deep Dive on Decentralization | Robert Leshner (Compound) y Jesse Walden | 1:02:18 | 28K |
| 10 | Building Companies and Developer Communities | Tom Preston-Werner con Chris Dixon | 48:46 | 12K |
| 11 | Secure Smart Contract Development | Jutta Steiner | 56:57 | 12K |
| 12 | Products and Protocol | Nitya Subramanian | 17:28 | 13K |
| 13 | Token Securities Framework and Launching a Network | Brian Brooks | 55:00 | 21K |
| 14 | Fundraising and Deal Structure | Jesse Walden | 38:28 | 40K |

## 3. Lo esencial

Etiquetas: [H] hecho con fuente · [I] inferencia · [O] opinión del autor.

1. **[H] Diseño del programa** (anuncio, 8-nov-2019): "*a seven-week program that will kick off in late February 2020*", con los videos y materiales en línea después. Objetivo: compartir lo aprendido en "*almost seven years*" invirtiendo en cripto, sobre producto, organización, *go-to-market* y regulación.
2. **[H] Cohorte:** 45 estudiantes elegidos entre "*thousands of applications*". Presentaron sus proyectos al final (post del 12-may-2020).
   - Inconsistencia de las propias fuentes: el anuncio dice siete semanas; el post de mayo, "*six weeks of sessions*"; TechCrunch dice "*seven-week*" en sus primeras notas y "*six-week*" en la última.
3. **[H] Módulos declarados:** fundamentos de cripto como plataforma de cómputo, desarrollo de producto, seguridad, construcción de organización, *go-to-market*, modelos de negocio, buenas prácticas regulatorias y levantamiento de capital (post del 12-may-2020).
4. **[H] Semana 1** (TechCrunch, 13-may-2020):
   - Dixon da un panorama y habla del "*potential for crypto networks to lead a new wave of innovation*".
   - Boneh introduce "*the cryptographic foundation of blockchains*".
5. **[H] Semana 3** (TechCrunch, 27-may-2020): "*how to capture value and design proper incentives within the decentralized framework*": efectos de red y diseño de mecanismos (clases de Yahya y de Sam Williams).
6. **[H] Semana 4** (TechCrunch, 10-jun-2020): "*building companies by growing communities of users, developers and employees in a decentralized context*".
7. **[H] Semana final** (TechCrunch, 24-jun-2020): Brooks, "*former Coinbase Chief Legal Officer*", llama a cripto "*most perfect intersection of tech and finance*" y advierte que los constructores deben lidiar con la regulación financiera tradicional.
8. **[H] Descentralización progresiva** (Walden, 8-ene-2020), en tres etapas:
   1. encaje producto-mercado, con un equipo central y "*admin privileges on smart contracts*": actualizaciones, apagado y parámetros;
   2. participación de la comunidad, con código abierto, recompensas y restricciones técnicas. Ejemplo: en Compound v2.2 las actualizaciones "*take effect 48 hours after they are pushed*";
   3. descentralización suficiente, con una distribución amplia del token.
9. **[H] Modelo de negocio** (Walden): comisión por uso, como una API. Uniswap protege su comisión con el efecto de red de la liquidez (cambiarse cuesta). Los protocolos deben ser "*minimally extractive*".
10. **[O] Tesis legal de a16z** (Walden, citando a Scott Kupor): "*post-network launch — provided that the network is sufficiently decentralized — the nature of the token can change from security to non-security*". Es una **tesis del fondo**, no un criterio establecido; Walden mismo pide consultar a un abogado.
11. **[H] Errores de orden que señala Walden:**
    - repartir el token antes de tener producto crea "*a community of speculators*";
    - saltarse la participación real produce "*decentralization theater*".
12. **[I] Qué dice el temario sobre DeFi.** No hay clases sobre AMM, préstamos y liquidaciones, stablecoins, oráculos o MEV. Lo más cercano:
    - seguridad de contratos (Steiner);
    - diseño de mecanismos (Sam Williams);
    - descentralización, con el fundador de Compound (Leshner).
    - [I] El curso se grabó antes del "DeFi Summer": la liquidez incentivada de COMP arrancó en mayo de 2020 según Finematics ([03](03-finematics.md)). Clasificarlo en el grupo DeFi es generoso.
13. **[I] Llaves de administrador = riesgo de gobernanza.**
    - La etapa 1 de Walden recomienda privilegios de administrador y la 2, *timelocks*. Para quien invierte, esas son las "*admin keys*" y el riesgo de gobernanza que enumeran Finematics y Harvey ([03](03-finematics.md), [07](07-defi-and-the-future-of-finance.md)).
    - El ataque de gobernanza con flash loan a Beanstalk (17-abr-2022, $182 M) muestra el otro extremo: gobernanza "descentralizada" que se puede comprar por una transacción.
14. **[H] Recepción** (metadatos de YouTube, 25-sep-2026): la clase más vista es la de Armstrong (231K) y la menos vista, la de Ferguson (7K). Las de contenido técnico o legal más útiles para riesgo (Steiner 12K; Brooks 21K) tuvieron poca audiencia.
15. **[I] Mecánica que exige este estudio y el recurso no cubre:** x·y = k y pérdida impermanente, factor de salud y liquidaciones, Terra y USDC/SVB, ataques de oráculo y flash loan, y MEV. Todo está en [06](06-decentralized-finance-mooc.md) y en el capítulo §2. **No atribuyo a este curso nada de eso.**

## 4. Qué cambia para invertir

- **[I] Lente de fondo de capital de riesgo.** El curso enseña cómo un proyecto captura valor para su token (modelos de negocio, diseño de mecanismos). Eso sirve para valuar tokens de protocolos, no BTC.
  - Para una cuenta spot de BTC, lo aprovechable es el mapa de riesgos de gobernanza y regulación: llaves de administrador, *timelocks* y la pregunta de si un token es un valor. Esa pregunta afecta listados, ETF y custodios.
- **[I] Cascadas de liquidación.** No se tratan. Ver el capítulo §4 (10-oct-2025: más de $19 mil M liquidados en perpetuos contra ~$180 M en Aave; BTC −14.5% dentro del día).
- **[I] Por qué no usamos rendimientos DeFi.**
  - Según el propio manual de Walden, un protocolo joven depende de un equipo central con llaves de administrador. Cualquier rendimiento ahí incluye riesgo de gobernanza y de equipo.
  - Nuestro mandato es spot.
- **[I] Señales a vigilar** (derivadas del curso):
  1. protocolos con llaves de administrador y sin *timelock*;
  2. "teatro de descentralización": participación baja en gobernanza;
  3. tokens repartidos sobre todo a inversionistas antes de que haya uso real;
  4. cambios regulatorios sobre qué token es un valor.

## 5. Contrapuntos y límites

- **Acceso mínimo:** no pude evaluar el contenido real de las clases. Esta ficha resume el temario, las descripciones oficiales y un texto de un ponente.
- **Sesgo estructural:** lo produce un fondo que invierte en el sector, con ponentes de su portafolio. Su objetivo explícito es formar fundadores, no advertir a inversionistas.
- **Envejecimiento:**
  - es anterior al DeFi Summer, a Terra, a FTX y al Merge;
  - la tesis de la "transmutación" del token es una apuesta legal del fondo, no un hecho;
  - el título "*Applications: Today & 2025*" hace una proyección a 2025 que no puedo evaluar sin el video.
- **Qué no está probado:** que la "descentralización suficiente" cambie la naturaleza jurídica de un token, y que el efecto de red proteja las comisiones de un protocolo que cualquiera puede copiar (bifurcar). Harvey lo discute como "*vampirism*" en [07](07-defi-and-the-future-of-finance.md).

## 6. Autoexamen

1. **¿Cuáles son las tres etapas de la descentralización progresiva y qué pasa si se invierte el orden?**
   - *Respuesta:* 1) encaje producto-mercado con control central; 2) participación de la comunidad; 3) descentralización suficiente con distribución amplia del token.
   - Repartir el token primero crea una comunidad de especuladores; saltarse la etapa 2 produce "*decentralization theater*".
   - *Fuente:* Walden (a16z, 8-ene-2020).
2. **¿Por qué la afirmación de que un token puede dejar de ser un valor con suficiente descentralización debe etiquetarse como [O] y no como [H]?**
   - *Respuesta:* es la interpretación legal de un fondo interesado (Kupor y Walden), no una regla establecida. La SEC ya había dictaminado en 2017 que los tokens de The DAO eran valores (Release 34-81207), y el propio texto pide consultar a un abogado.
   - *Fuente:* Walden (2020); [SEC](https://www.sec.gov/files/litigation/investreport/34-81207.pdf).
3. **¿Qué clases del temario tocan el riesgo DeFi y qué le falta al curso para este estudio?**
   - *Respuesta:* Steiner (contratos seguros), Sam Williams (diseño de mecanismos) y Leshner con Walden (descentralización).
   - Le faltan AMM, liquidaciones, stablecoins, oráculos y MEV.
   - *Fuente:* temario (títulos de los 14 videos).
4. **¿Cómo debe cambiar el conflicto de interés de a16z la forma de usar el curso?**
   - *Respuesta:* sirve como fuente de cómo piensan los fondos y los fundadores sobre tokens y gobernanza (grado D para decisiones de inversión), no como evidencia de que los modelos funcionen.
   - Toda cifra o tesis se contrasta con una fuente primaria o académica ([06](06-decentralized-finance-mooc.md)).
   - *Fuente:* post de a16z ("*team and portfolio*") y su descargo.

## 7. Grado de evidencia: **D** para decisiones de inversión; **A** para los datos del programa

- **A:** los datos del programa (fechas, cohorte, ponentes, duraciones) vienen de páginas oficiales.
- **D:** el contenido que pude ver es la perspectiva de un fondo con intereses en el sector, sin datos ni método visibles en lo que leí. Además, no vi las clases.
- **Revisión pendiente:** si aparecen transcripciones o diapositivas oficiales, releer las clases 7, 9, 11 y 13.
