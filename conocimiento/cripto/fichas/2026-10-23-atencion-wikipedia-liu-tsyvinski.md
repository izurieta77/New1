# Ficha de avance · 23-oct-2026 · ¿La atención predice el rendimiento de BTC? Liu y Tsyvinski (§4.2) puestos a prueba con visitas a Wikipedia, 2015-2026

> Corrida de las 08:17 CDMX (14:2x UTC), estudio profundo. Nivel **Doctorado** (literatura de factores cripto), grupo G5 (mercado, on-chain e institucional).
>
> **Por qué este tema.** Es el siguiente de la cola académica que fijó el plan (Liu-Tsyvinski momentum → Makarov-Schoar → Griffin-Shams → **atención como predictor**). La ficha del 19-oct dejó pendiente la §4.2 del WP, que es el segundo factor propio de BTC según el paper. Además viene al caso: la atención pública a bitcoin está en mínimos de la serie (abajo, §3.4) mientras el precio cae; hay que saber si eso es señal o ruido.

## 0. Preguntas de hoy

1. ¿Qué afirma el paper sobre la atención, con sus números?
2. ¿Sobrevive fuera de su muestra (jun-2018 a oct-2026) con un proxy público y reproducible?
3. ¿Qué cambia para el filtro, para el pronóstico y para la lectura del pulso?

## 1. Acceso y fuentes (declarado)

- **Liu, Y. y Tsyvinski, A. "Risks and Returns of Cryptocurrency".** NBER WP 24877 (ago-2018); *Review of Financial Studies* 34(6):2689-2727 (2021). [PDF de NBER](https://www.nber.org/system/files/working_papers/w24877/w24877.pdf), descargado hoy (653 KB). **Acceso: sección.** Se leyeron íntegros la introducción (págs. 2-3), la §2 (datos) y la **§4.2 (págs. 23-28, tablas 19-25)**, más el párrafo de Twitter (tablas 26-27) y la apertura de la §4.3 (atención negativa). No se cotejó la versión publicada en la RFS.
- **Kristoufek, L. (2013). "BitCoin meets Google Trends and Wikipedia".** *Scientific Reports* 3:3415, [doi:10.1038/srep03415](https://doi.org/10.1038/srep03415); acceso abierto (CC BY-NC-SA, PMC3849639). **Acceso: solo el resumen** (Europe PMC). Es el antecedente que usa Wikipedia como medida de atención.
- **Datos de la prueba (A en datos):**
  - visitas diarias al artículo "Bitcoin" de la Wikipedia en inglés, agente `user`, todas las plataformas: [Wikimedia REST API](https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Bitcoin/daily/20150701/20261022), 4,132 días (1-jul-2015 a 22-oct-2026);
  - cierres diarios de BTC-USD de Yahoo (chart v8), vela UTC.
- **Google Trends no se pudo usar:** su endpoint respondió **429** y no tiene API pública estable. Por eso el proxy es Wikipedia, que además es reproducible por cualquiera (Trends cambia la muestra en cada descarga).
- **Conflictos de interés:** ninguno declarado en el WP (académicos de Yale).

## 2. Lo que dice el paper [H, grado A en el texto del WP]

Muestra de BTC: 1-ene-2011 a 31-may-2018 (CoinDesk). Medida: búsquedas en Google de "Bitcoin" de la semana **menos el promedio de las cuatro semanas previas**, normalizada.

- **Tabla 19 (regresión semanal):** una σ más de búsquedas sube el rendimiento **+1.84 pp a 1 semana (t 2.17; bootstrap 1.76) y +2.30 pp a 2 semanas (t 2.81; 2.07)**. A 3-7 semanas no es significativa. R² de 0.01-0.02.
- **Tabla 20 (quintiles):** a 1 semana, el quintil alto rinde **11.20% semanal** (Sharpe 0.48) y el bajo 1.07%; diferencia **+10.13 pp**. **Tabla 22 (cortes con los primeros 2 años, sin mirar adelante):** diferencia de **+7.39 pp** a 1 semana.
- **Tabla 25:** la atención **sigue** al precio: la desviación de búsquedas se asocia con R_t y R_{t−1} (t 2.9-4.2). La causalidad va en los dos sentidos.
- **Twitter (tabla 26):** una σ más de tuits suma +2.50 pp a 1 semana. **Atención negativa (§4.3):** la razón "Bitcoin hack"/"Bitcoin" resta 2.75 pp la semana siguiente.
- **Ripple y Ethereum:** +10.86 pp y +4.36 pp a 1 semana por σ.

## 3. Ejercicio numérico: réplica con Wikipedia, 2015-2026 (comprobado en Python)

Script [`2026-10-23-atencion-wikipedia-liu-tsyvinski.py`](2026-10-23-atencion-wikipedia-liu-tsyvinski.py) (`python3 -I ...`, solo biblioteca estándar), corrido el 23-oct ~14:3x UTC. Son **589 semanas** lunes-domingo (12-jul-2015 a 18-oct-2026). La atención de la semana t se mide como en LT, contra el promedio de las 4 previas, en dos versiones: **niveles** (`a_lvl`, el diseño literal) y **logaritmo** (`a_log`, robusta a la caída de nivel de Wikipedia). Regresión R_{t+h} = a + b·z_t, con t de Newey-West (rezagos h+3); b está en pp de rendimiento semanal por una σ de atención. Las dos cifras clave (b a 1 semana en niveles, traslape y fuera de muestra) se recalcularon aparte con numpy y coinciden: +2.75 y −0.43.

### 3.1 Regresión

| Tramo | Medida | h=1 | h=2 | h=3 | h=4 |
|---|---|---|---|---|---|
| **Paper** (Google, 2011-may-2018) | niveles | **+1.84 (t 2.17)** | **+2.30 (2.81)** | +1.04 (1.25) | +0.59 (0.72) |
| Traslape con LT (ago-2015 a may-2018, 147 sem.) | niveles | **+2.75 (t NW 2.99)** | +1.14 (0.77) | +0.73 (0.61) | +1.45 (2.90) |
| Traslape con LT | log | +1.57 (1.27) | +0.81 (0.68) | +1.55 (1.81) | +1.59 (2.51) |
| **Fuera de muestra** (jun-2018 a oct-2026, 438 sem.) | niveles | **−0.43 (−0.99)** | −0.43 (−0.80) | +0.72 (2.20) | +0.96 (2.14) |
| Fuera de muestra | log | **−0.16 (−0.42)** | −0.16 (−0.40) | +0.39 (1.17) | +0.98 (2.52) |
| Era 2022+ (ene-2022 a oct-2026, 251 sem.) | niveles | +0.37 (0.98) | −0.15 (−0.49) | +0.25 (0.70) | +0.19 (0.65) |
| Era 2022+ | log | +0.19 (0.45) | −0.08 (−0.25) | +0.03 (0.08) | +0.27 (0.84) |

Controlando por R_t (momentum), los b casi no cambian; R_t a 1 semana fuera de muestra es +0.116 (t NW 2.5), igual que en la ficha del 19-oct.

### 3.2 Quintiles sin mirar adelante (cortes con la ventana previa, ≥104 semanas), fuera de muestra

| Quintil de atención | R_{t+1} medio | t | Sharpe semanal | n |
|---|---|---|---|---|
| Q1 (baja) | +1.67% | 1.94 | 0.21 | 84 |
| Q2 | +1.83% | 2.26 | 0.26 | 77 |
| Q3 | +0.05% | 0.07 | 0.01 | 107 |
| Q4 | −0.17% | −0.15 | −0.02 | 84 |
| Q5 (alta) | +1.35% | 1.45 | 0.16 | 85 |
| **Q5 − Q1** | **−0.32 pp (t −0.25)** | | | contra **+7.39 pp** del paper (tabla 22) |

Incondicional: +0.89% semanal (n = 437).

### 3.3 ¿La atención sigue al precio? (tabla 25)

z(a_log)_t sobre R_t y R_{t−1}: en el traslape, +0.018 y +0.022 σ por pp (t NW 2.4 y 3.6; R² 0.11); fuera de muestra, +0.004 (t 0.5) y +0.019 (t 2.8; R² 0.03). La atención **todavía reacciona** al rendimiento de la semana anterior, pero mucho menos.

### 3.4 Lectura de hoy

| Semana al | Visitas | a_log | z (fuera de muestra) | Percentil histórico | R semanal |
|---|---|---|---|---|---|
| 27-sep | 34,390 | +0.516 | +2.21 | 97 | +4.09% |
| 4-oct | 18,156 | −0.250 | −1.07 | 15 | +2.39% |
| 11-oct | 25,872 | +0.114 | +0.49 | 79 | −3.24% |
| **18-oct** | **15,738** | **−0.416** | **−1.78** | **4** | −1.99% |
| 19-22 oct (parcial, 4 días) | 2,216/día | −0.417 | | | |

### 3.5 Lectura [I]

1. **El método sí replica dentro de la muestra.** Con Wikipedia en lugar de Google, en el tramo que comparte con el paper, una σ de atención suma **+2.75 pp** a la semana siguiente (t 2.99), del orden del +1.84/+2.16 del paper. El proxy sirve: no es que Wikipedia mida otra cosa.
2. **Fuera de muestra desaparece donde el paper lo encontró.** A 1 y 2 semanas, b es **negativo y no significativo** (−0.43 y −0.16), y la diferencia de quintiles pasa de +7.39 pp a **−0.32 pp**. En 2022-2026 todo es cero.
3. **El h = 4 positivo no cuenta.** Fuera de muestra aparece b ≈ +1 pp a 4 semanas (t 2.1-2.5), pero (a) el paper no lo encontró en ese horizonte (t 0.72), (b) se probaron 4 horizontes × 2 medidas × 3 tramos = 24 regresiones, donde uno o dos t > 2 son lo esperado por azar, y (c) en 2022+ se esfuma (t 0.65-0.84). Es minería de datos, no un factor.
4. **Por qué decae [I, grado C]:** lo más probable es una mezcla de publicación y arbitraje (el paper circuló desde 2018), cambio de clientela (ETF e instituciones no buscan "Bitcoin" en Wikipedia para comprar) y deterioro del proxy (el tráfico humano a Wikipedia cae con los resúmenes de IA y el filtro de bots de Wikimedia cambió; ver §5). No se puede separar una causa de otra con estos datos.
5. **Hoy:** la atención está en el **percentil 4** de su historia (semana al 18-oct) y la semana en curso va igual. En 2017-18 eso habría sido una señal bajista; fuera de muestra, el quintil bajo rindió **+1.67%** a la semana siguiente, más que el incondicional (no significativo). **No es señal en ninguna dirección.**

## 4. Qué cambia para invertir [O]

- **Filtro de la cuenta:** nada. La atención no entra en el filtro SMA200 ni en el tamaño de posición.
- **Pulso:** no se agrega la atención como indicador del régimen. Se anota como contexto (la "gente" no está mirando), sin peso.
- **Contra las narrativas:** "nadie habla de bitcoin, es el piso" y "todos hablan de bitcoin, es el techo" son, en 2018-2026, ruido medido. Quien las use como regla debe mostrar un historial fuera de muestra (regla de escepticismo: grado D sin historial).
- **Factores que siguen en pie** después de cuatro papers: el momentum a 1 semana sobrevive débil (19-oct); la prima por país es un problema de liquidez (21-oct); la emisión de USDT sigue a la demanda (22-oct); la atención no predice (hoy). Ninguno justifica operar más seguido que el filtro.

## 5. Contrapuntos y límites

- **Proxy distinto:** Wikipedia en inglés no es Google mundial. El traslape (+2.75 pp) sugiere que miden lo mismo, pero puede haber divergido después de 2018 (Wikipedia pierde tráfico humano). Si alguien consigue Google Trends semanal 2018-2026 por vía legal, hay que repetir.
- **Clasificación de bots:** Wikimedia introdujo el agente `automated` en 2020 (de memoria; no se verificó hoy en su documentación); parte del tráfico que antes contaba como `user` dejó de contar. Eso mete un quiebre de nivel; la versión en log contra las 4 semanas previas lo atenúa, no lo elimina.
- **Spike del 27-sep (34,390, percentil 97):** no se investigó su causa (puede ser un evento o tráfico no humano mal clasificado).
- **Rendimiento:** Yahoo BTC-USD (agregado), no un exchange; simple, no logarítmico. No se replicaron Twitter ni la "atención negativa" (hackeos).
- **Muestra:** 438 semanas fuera de muestra; potencia baja para efectos de ~1 pp semanal (σ semanal ~8-9%).

## 6. Autoexamen

1. ¿Cómo mide LT la atención? → Búsquedas de la semana menos el promedio de las 4 previas, normalizado.
2. ¿Cuánto vale el efecto en el paper? → +1.84 pp a 1 semana y +2.30 pp a 2 semanas por σ; Q5−Q1 de +10.13 pp (+7.39 sin mirar adelante).
3. ¿Por qué el h = 4 fuera de muestra no se toma como hallazgo? → No es el horizonte del paper, salió entre 24 pruebas y desaparece en 2022+.
4. ¿Qué dice la atención en mínimos de hoy? → Nada operable: fuera de muestra, el quintil bajo no rinde menos.
5. ¿Por qué Wikipedia y no Google Trends? → Trends no tiene API pública estable (429) y cambia la muestra en cada descarga; Wikipedia es pública y reproducible.

## 7. Estado

- **Estado:** Documentado con comprobación (§4.2 del WP leída íntegra; réplica en Python con datos primarios y una segunda vía de cálculo).
- **Grado:** A en lo que dice el WP; B en la réplica (proxy distinto al del paper); C en la explicación del decaimiento.
- **Pendientes (cola del Doctorado):**
  - criptografía poscuántica en bitcoin (podcast Unchained, 22-oct; BIP-360 y propuestas de migración);
  - repetir con Google Trends semanal si hay vía legal estable, y con la atención negativa ("Bitcoin hack");
  - cotejar la versión de la RFS (tablas de atención).
- **Pronóstico del día:** P0172 (ETH/BTC), sin relación directa con esta ficha: la atención no da señal que pronosticar.
