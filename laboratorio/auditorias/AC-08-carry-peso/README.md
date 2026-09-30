# AC-08: ¿un diferencial Banxico–Fed de 3% o menos anticipa una depreciación del peso de ~14%?

> Formación y vigilancia. No es una recomendación. Cifras históricas del FIX de Banxico (pesos por dólar; subir = peso más débil).

| Campo | Valor |
|---|---|
| Origen | Podcast "Peso vs. dólar: ¿es momento de comprar dólares?" (El Arte de Invertir, invitado Comet, grabado el lunes 28-sep-2026), transcrito por el dueño el 30-sep. Tesis: "con diferencial ≤3% el peso se depreció ~14% en casi todos los casos de 20 años". |
| Fecha | 2026-09-30, ~09:00-09:30 CDMX |
| Réplica A | `replicaA/`: diferencial de **política** = objetivo de Banxico (SF61745; antes de 2008 fondeo SF43773 redondeado) − límite superior de la Fed (DFEDTAR / DFEDTARU). Diario 2005-2026. Principal: `analisis.py`; régimen: `regimen.py`; cruce contra B: `verifica.py`. |
| Réplica B | `replicaB/`: diferencial de **mercado** = CETES 28 (SF43936) − T-bill 3m (DTB3). Semanal 2006-2026. Principal: `analisis.py` (episodios, tasa base, regresión Newey-West) con `salida.txt`; robustez (money-market act/360, T-bill 4 semanas, persistencia) en `robustez.py` / `robustez.txt`. Código escrito sin ver A. |
| Verificador | `verificador/`: código propio, re-ejecuta cifras clave de A y B; agrega pares (BRL, ZAR, CAD, dólar amplio), CFTC y prueba de desplazamiento circular. |
| Datos | Banxico SIE con `herramientas/banxico.py` (requiere `BANXICO_TOKEN` en el entorno; el token nunca va a git) y FRED CSV. Los CSV/JSON descargados no se versionan (`.gitignore`); se regeneran con `fetch*.py` y `fred.py`. |

## Resultado

**No sostenida en su forma literal.** Sobrevive solo como sesgo de riesgo, no como regla.

| Medida | Cruces hacia abajo de 3% (regímenes independientes y terminados) | Cambio del FIX a 12 meses | Máxima depreciación en 12 meses |
|---|---|---|---|
| Política (A) | 24-feb-2006 · 6-jun-2014 | +5.4% · +21.7% | 9.6% · 21.7% |
| Mercado (B) | 23-feb-2006 · 12-jun-2014 (· 8-oct-2015, mismo régimen) | +5.3% · +18.7% (· +16.6%) | 9.5% · 20.9% (· 19.9%) |

- **n = 2 regímenes, con resultados opuestos.** 2006-07: 22 meses con diferencial ≤3 (mínimo 1.75) y el peso casi plano. 2014-16: +46% en el tramo ≤3, pero con desplome del petróleo, dólar global fuerte y alza de la Fed; en el mismo lapso el real brasileño, con carry de dos dígitos, cayó 41% y el rand 18.7%.
- **Tasa base 2006-2025:** P(cambio a 12m ≥ 14%) = 20%; P(máxima depreciación en 12m ≥ 14%) = 34%. Condicionado a diferencial ≤3 sube a 46-47% y 51-53%, pero todo el efecto viene de 2014-16 y no es significativo (prueba de desplazamiento circular p = 0.07-0.26; regresión Newey-West a 12m t = −0.67).
- **No es monótona:** con diferencial ≤2.5 (casi todo 2006-07) la mediana a 12m fue −1.5 a −2.0%.
- **Las grandes depreciaciones ocurrieron con carry ancho:** 2008-09 +55% (diferencial 6.0-8.0), COVID +35% (5.25-6.75), 2016-17 +27.5% (3.25-5.0), 2024-25 +27% (5.25-5.75).
- **De dónde sale el "~14%":** la media de dos casos (13.5%) o la mediana de la máxima depreciación agrupando semanas ≤3 (14.5%). Ninguna respalda "casi todos los casos".

## Hoy (30-sep-2026)

| Dato | Valor |
|---|---|
| Diferencial de política | 2.50 (Banxico 6.50 − Fed 4.00; alza de la Fed decidida el 16-sep) |
| Diferencial de mercado | 1.91 (CETES 28 6.01 − T-bill 3m 4.10): **mínimo semanal desde 2005**, sin precedente en la muestra |
| FIX | 18.071 (29-sep); +7.1% desde 16.875 (4-sep); +5.1% en 8 días hábiles desde el alza de la Fed, ventana que solo 1.8% de las de 8 días desde 2006 superó |
| Episodio actual | Cruce de 3% el 27-mar-2026: +0.02% en los seis meses siguientes, con apreciación hasta 16.87 en medio |
| Después de depreciaciones ≥5% en un mes (28 episodios desde 2006) | Mediana del mes siguiente −0.3%, de los tres siguientes −1.5%; cola derecha gruesa (2008, 2020) |
| CFTC, neto largo especulativo en MXN | 94,732 (8-sep) → 75,167 contratos (22-sep), aún en el percentil 73 de 2006-2026: queda margen para más salida de carry |

## Qué sí apoya el mecanismo [I]

Desde el 4-sep el peso (+6.4%) se depreció más que sus pares (COP +5.0, CLP +4.4, CAD +3.0, ZAR +2.6, DXY +2.1, BRL +1.4) y el posicionamiento especulativo se está reduciendo: es coherente con una salida de carry propia del peso. La literatura (Brunnermeier, Nagel y Pedersen 2009; Menkhoff et al. 2012; Lustig, Roussanov y Verdelhan 2011; Burnside et al. 2011; Fama 1984) respalda el riesgo de desplome de las monedas de carry en choques globales de aversión al riesgo o de liquidez, no una regla de umbral.

## Errores encontrados por el verificador

- A: rangos del diferencial en las grandes depreciaciones citados de forma imprecisa (sin cambio de conclusión); fecha de la Fed: decisión 16-sep, efectiva 17-sep.
- B: la "mediana 16.6%" de tres cruces cuenta dos veces el régimen 2014-16; por régimen es 12.0%. Etiqueta "2013-16" sin semanas de 2013.
- Ambas: no controlaban por pares ni usaban una prueba que respete la autocorrelación (el verificador las agregó).

## Etiqueta

**descartada** como regla de pronóstico ("≤3% ⇒ ~14%"). El diferencial y la velocidad del FIX quedan como **variables de vigilancia** (ver la regla de alerta de tipo de cambio en `rutinas/supervision.md`).
