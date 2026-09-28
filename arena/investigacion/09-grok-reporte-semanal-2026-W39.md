# Rival Grok: reporte semanal al arrancar la semana del 28-sep-2026 (registro de inteligencia)

**Registrado:** domingo 27-sep-2026, 19:20 CDMX, sesión principal. **Fuente:** texto que Grok le entregó al dueño y que el dueño reenvió íntegro al chat. **Identificación [H]:** el propio texto dice "No tengo cifras de ChatGPT ni de Claude", así que es el tercer participante: **Grok**.

## Lo que reporta Grok (hechos según su propio texto)

| Tema | Dato |
|---|---|
| Cartera | **De práctica, sin dinero real.** "Al máximo de agresividad que permiten tus topes" (el dueño le dio topes; no dice cuáles) |
| Valor al cierre del 25-sep | 29,814.93 MXN: GBM 19,893.69 + Binance 9,921.24 (arrancó con 20,000 + 10,000 → **−0.62%** combinado, −0.53% GBM, −0.79% Binance) |
| GBM | 60% SMH (ETF de semiconductores), 28% SPYL (S&P 500), 12% en cuatro acciones (no las nombra) |
| Binance | 60% BTC, 40% stablecoins |
| Método | "v1.2", re-simulado con el mismo resultado; "queda firme" |
| Descartadas con datos | compras de directivos, momentum en la BMV, estacionalidad por mes en México, rally pre-FOMC |
| En investigación | rebote post-reportes trimestrales; estacionalidad por mes en EUA |
| Adoptado "de los rivales" | expediente por empresa con controles; comparar cada estrategia contra comprar-y-mantener (ambos son formatos nuestros: `ficha-empresa` y `laboratorio/tabla-maestra.md`) |
| Contra el S&P 500 en MXN | GBM iba 1.71 pp abajo el primer día |
| Otros frentes | costos de ETFs; ranking parcial de fondos (GBM y Scotia; Banorte y Valmex bloquean); "lo de la gasolinera"; dos módulos de doctorado fiscal |
| Pendientes que le pide al dueño | cifras de ChatGPT y Claude; protocolo v1.7 de "Maquiavelo" (es de ChatGPT); publicación de "la app" en Vercel, URL y `APP_REPLY_KEY`; tokens de Banxico y ALFRED; si pone en papel Traxión o manda ese efectivo a SPYL |

## Verificación y correcciones

1. **Falso sobre nosotros:** "dejé fuera el modo de Claude que mete todo a Bitcoin con apalancamiento de 3 veces". [H] Nunca propusimos Bitcoin apalancado. El modo D de nuestra simulación (`arena/modelos/meta_dueno_40_60_200.py`) era 100% ETF 3x del **Nasdaq** + 100% BTC **al contado**, se presentó como la opción a NO elegir, y el dueño eligió el modo C (≤50% ETF 3x con filtro + BTC al contado con filtro, por comité). Grok está leyendo resúmenes de nuestro trabajo (el dueño los comparte) y los transmite con errores. [I] Consecuencia: todo lo que Grok diga "de Claude" hay que verificarlo contra nuestro git, no aceptarlo.
2. **Su cartera, contra nuestras reglas:** 60% en un solo ETF sectorial. [H] SMH tuvo caídas de −35% a −45% en ventanas de 4 meses (2018-4T, 2020-1T, 2022). Con 60% del libro, una caída así cuesta 21-27% de GBM (4,200-5,400 MXN): cabe dentro de un tope de 10,000, pero es una apuesta de sector, no de mercado. Bajo nuestro perfil no pasaría (`sector_max` 0.25). Su 60% BTC es más que nuestro 40% inicial y menos que el 100% que autoriza nuestro modo C.
3. **Descartes:** [H] coinciden con lo nuestro en lo comparable: compras de directivos (`conocimiento/15`, sin ventaja replicable), estacionalidad en México (R04/AC-04 no la sostienen ni en EUA). El rally pre-FOMC (Lucca-Moench 2015) nosotros lo tenemos documentado, no replicado: su descarte con datos es un dato útil que **no adoptamos sin ver su prueba**.
4. **SPYL en SIC:** [I] es el ticker del SPDR S&P 500 UCITS (Europa). Que esté disponible en GBM/SIC no lo verificamos. Nosotros usamos SPYM.
5. **"1.71 pp abajo el primer día"** contra el S&P en pesos: [I] consistente con 60% SMH en un día en que los semiconductores cayeron más que el índice; un día no dice nada, como él mismo reconoce.
6. **Sharpe con el ajuste de Lo (2002):** lo mismo que ChatGPT anunció; nosotros ya lo tenemos en `conocimiento/07` §224 y §353.

## Qué es de ellos y no nuestro

Vercel, `APP_REPLY_KEY`, tokens de Banxico/ALFRED y Traxión/SPYL son asuntos entre Grok y el dueño. [I] Un token de Banxico (SIE, gratuito) sí nos serviría para reemplazar el proxy de CETES 28 del marcador por la serie oficial; si el dueño lo comparte, se usa. No se pide nada más.

## Marcador

Sus cifras son de **papel**. Se registran en `competencia/rivales.csv` con cuenta `grok-gbm-papel` y `grok-binance-papel` para que no entren al marcador de cuentas reales. Al 25-sep ninguna de las tres IAs tenía dinero real; nosotros entramos el 28-sep.
