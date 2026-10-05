# Ficha: tasa base de las ganancias que definen Diamante, Platino y Oro

> Laboratorio, 5-oct-2026. Fase 0. Sirve para calibrar la "probabilidad honesta de alcanzar el objetivo" que cada candidato del radar debe reportar (`arena/investigacion/13-radar-niveles-pre-registro.md`, adenda de hoy). No es una predicción: es qué tan común fue cada ganancia en el pasado.
> Código: `conocimiento/fichas/codigo/2026-10-05-tasa-base-ganancias.py` (stdlib + `herramientas`, ~50 s). Las cifras de UPRO salen de una comprobación aparte con la misma lógica (grado D hasta que se versione).

## 1. Definiciones del dueño
- **Diamante:** más de +40% en 2 a 3 meses. **Platino:** más de +50% en 3 a 5 meses. **Oro:** +20% a +30% en 5 a 7 meses.

## 2. Resultado (2016-2026, cierre ajustado de Yahoo, sin costos ni impuestos)
Se mide, desde cada día de inicio, si el precio **termina** arriba del umbral al plazo y si lo **toca** en algún cierre dentro del plazo.

| Regla | Universo (85 series de EUA y México) termina / toca | BTC y ETH termina / toca | UPRO 2009-2026 termina / toca |
|---|---|---|---|
| Diamante, > +40% en 2 meses | 1.6% / 2.4% | 19.3% / 27.6% | 2.1% / 3.3% |
| Diamante, > +40% en 3 meses | 3.2% / 4.9% | 26.8% / 38.4% | 4.2% / 7.1% |
| Platino, > +50% en 3 meses | 1.8% / 2.8% | 21.2% / 31.7% | 1.8% / 3.1% |
| Platino, > +50% en 5 meses | 4.6% / 6.7% | 30.1% / 44.2% | 7.7% / 10.9% |
| Oro, ≥ +20% en 5 meses | 22.8% / 35.0% (en la banda de +20% a +30%: 10.1%) | 46.0% / 63.9% | 43.8% / 63.1% |
| Oro, ≥ +20% en 7 meses | 29.9% / 45.3% (en la banda: 11.5%) | 51.9% / 72.7% | — |

- **Acciones grandes:** un Diamante o un Platino es un evento de 2% a 5% de las ventanas. Un Oro es mucho más común (23% a 30% de las ventanas terminan arriba de +20%), porque el mercado de 2016-2026 fue alcista.
- **Mediana por empresa:** 2.4% de las ventanas de 3 meses tocan +40%. **15 de las 85 series no tuvieron una sola ventana** que lo hiciera. Las que más: SNDK (78%, con historia corta posterior a su escisión), GEV, PLTR y AMD (34% a 37%), TSLA, NVDA, CRWD y MU (20% a 28%).
- **Cripto:** BTC y ETH dieron esas ganancias 5 a 10 veces más seguido que las acciones grandes, en una muestra que incluye los auges de 2017 y de 2020-2021. Por eso el radar cripto pone el objetivo contra su propio ciclo, no contra la media.
- **UPRO** (3x del S&P 500): el Diamante y el Platino también son raros; su ventaja es el Oro (+20% en 5 meses, 44% de las ventanas), con la cola de caída que ya conocemos.

## 3. Límites
- **Sesgo de supervivencia:** el universo es la lista actual de empresas grandes; las que se hundieron o salieron no están. Sobrestima las tasas.
- **Régimen:** 2016-2026 fue alcista para acciones y cripto; las tasas de un mercado lateral o bajista serían menores.
- Las ventanas se traslapan: el número de ventanas no es el número de eventos independientes.
- Sin costos, impuestos ni efecto del tipo de cambio.

## 4. Lo que cambia para el sistema (inferencia)
- Un candidato **Diamante** (> +40% en 2-3 meses) no se justifica con la tasa base: necesita un **catalizador específico con fecha** (un reporte, una aprobación, una fusión), porque la tasa de fondo es de un solo dígito en acciones grandes.
- Un candidato **Oro** puede apoyarse en la tasa base y en el filtro de tendencia, pero la banda de +20% a +30% es angosta: lo normal es quedarse corto o pasarse.
- La probabilidad honesta de alcanzar el objetivo debe partir de estas tasas y moverse **solo** con evidencia propia del candidato.
