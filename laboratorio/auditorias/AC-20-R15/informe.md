# AC-20-R15: ejecución B independiente de R15 (USD/MXN después de un episodio FX-1)

- **Auditor:** `auditor-de-replicas` (ejecución B). Fecha: 2026-10-16 (UTC).
- **Independencia:** solo leí el pre-registro (§1-9) de `laboratorio/replicas/R15-fx1-episodio-peso.md`. No leí `R15.py` ni `R15-salida.txt`. El código es propio: `b.py` (stdlib; se corre con `python3 -I b.py`). La salida completa está en `salida.txt`.
- Sin commit ni push.

## 1. Fuente (descargada el 2026-10-16 a las 17:50 UTC)

| Serie | Archivo (`datos/`) | Vía | Periodo | sha256 |
|---|---|---|---|---|
| FIX Banxico (SF43718), columna "Determinación" | `banxico_fix_19911112_20261015.html.gz` (HTML original comprimido con gzip; 177 KB) | POST público sin token a `https://www.banxico.org.mx/tipcamb/tipCamIHAction.do` con `idioma=sp&fechaInicial=01/11/1991&fechaFinal=15/10/2026&salida=HTML` (formulario de `tipCamMIAction.do`). User-Agent genérico, sin correo. | 1991-11-12 a 2026-10-15 | gz: `91ae031b1abdb07afcfdd218ec659a5dbb739d0d7b065b69917839f86b989bb2`; HTML sin comprimir: `3f134f536040edfc95c8dbd2afdc396bbee14ee4c903a5a15ae0419b95d2c904` |

- La fuente es distinta de la de A (FRED DEXMXUS, mediodía de Nueva York). El FIX se determina en México hacia el mediodía, con calendario de días hábiles mexicano.
- La consulta del SIE con `consultaSerieGrafica.do` devolvió 400. El formulario `tipCamIHAction.do` sí da la historia completa: tiene 4 columnas apiladas (Fecha, Determinación, Publicación DOF, Para solventar obligaciones). Uso la columna **Determinación**: es el FIX de ese mismo día, sin el desfase de publicación en el DOF.
- **Limpieza (§7):** son 8,779 días con dato. Se descartan 334 días de lunes a viernes marcados N/E (feriados mexicanos); los fines de semana no cuentan. Los días hábiles son los renglones de la serie limpia. Revisé los saltos diarios mayores a 8%: los nueve caen entre dic-1994 y mar-1995 (crisis del tequila) y no hay rastro de redenominación (la serie ya está en nuevos pesos desde 1991).

## 2. Definiciones implementadas
- **Evento:** X_t ≥ 1.06 × min(X_{t−15..t−1}). El espejo es X_t ≤ 0.94 × max(X_{t−15..t−1}).
- **Episodio:** un evento se une al episodio si está a menos de 20 días hábiles del evento anterior (agrupación encadenada). Cuenta el primer día. Como sensibilidad, reporto también la agrupación anclada al primer día del episodio.
- **Cambio posterior:** X_{t+h}/X_t − 1, con h = 10 o 20 días hábiles. La ventana empieza en t (§5). Los episodios sin ventana completa se excluyen: el 2026-09-29 solo entra en h = 10.
- **t:** media/(sd/√n) sobre episodios. **Incondicional:** media de X_{t+h}/X_t − 1 sobre todos los días del periodo, con ventanas traslapadas.
- **"+3% adicional":** para el veredicto uso el cambio **punto a punto** al final de la ventana (≥ +3%). Como información también reporto si se toca +3% en algún día de la ventana (máximo de X_{t+1..t+h}).
- **"Desde 1996":** la serie se corta en 1996-01-01 antes de buscar eventos. Filtrar los episodios de la serie completa por fecha da exactamente lo mismo.

## 3. Resultados al alza (FX-1)

| Variante | Episodios (con ventana) | Media posterior | Mediana | Media incondicional | t | Frec. +3% punto a punto (incond.) | Frec. +3% en algún día (incond.) |
|---|---|---|---|---|---|---|---|
| Completa, 10 d | 43 (43) | +0.86% | −0.13% | +0.24% | +0.83 | 16.3% (7.9%) | 18.6% (12.1%) |
| Completa, 20 d | 43 (42) | +1.36% | +0.31% | +0.48% | +1.11 | 23.8% (14.1%) | 38.1% (23.7%) |
| Desde 1996, 10 d | 39 (39) | −0.05% | −0.13% | +0.14% | −0.09 | 15.4% (7.7%) | 17.9% (12.0%) |
| **Desde 1996, 20 d (principal)** | 39 (38) | **+0.16%** | −0.29% | **+0.28%** | **+0.17** | **21.1%** (14.0%) | 36.8% (24.2%) |

Hay 324 eventos en la serie completa y 240 desde 1996. Con la agrupación anclada al primer día salen 51 episodios en la serie completa y 43 desde 1996. Las conclusiones no cambian: en la principal, la media es +0.09%, t = +0.10 y la frecuencia es 19.0%.

**Espejo a la baja (informativo, 20 días):** en la serie completa hay 12 episodios, con media de +0.10%, t = +0.07 y frecuencia de −3% punto a punto de 33.3%. Desde 1996 hay 10 episodios, con media de −0.50%, t = −0.33 y frecuencia de 40%. La muestra es muy chica.

## 4. Veredicto (§2, principal: 20 días desde 1996)
- **H1 (reversión): REFUTADA.** La media posterior (+0.16%) no es menor que la incondicional (+0.28%), por poco, y el t es +0.17, mayor que −1.0. Tampoco se sostiene en ninguna de las otras tres variantes: el mejor t es −0.09.
- **H2 (no continuación): SOSTENIDA.** El 21.1% de los episodios sube otro 3% o más, por debajo del 30%. Ojo: esa frecuencia es 1.5 veces la incondicional (14.0%) y, medida como máximo dentro de la ventana, llega a 36.8%.
- **Estado según §2: "Replicado con diferencias"** (se sostiene H2, no H1). En lo sustantivo, después de un episodio FX-1 no hay reversión sistemática: el resultado se parece a una caminata aleatoria con colas gruesas a la alza (1994, 2008 y 2020).

## 5. Puntos a cotejar con A (sin haber visto su resultado)
- **Fechas de episodio:** el FIX y el DEXMXUS se miden a horas distintas y con calendarios de feriados distintos (MX frente a EUA). Algunos episodios pueden moverse un día o aparecer y desaparecer en el borde del 6%. Por ejemplo, el episodio de 2026 me sale el 2026-09-29, no el 28-sep que menciona el pre-registro.
- **Inicio de la serie:** el FIX arranca el 1991-11-12, antes que DEXMXUS (1993-11-08), pero el primer episodio sigue siendo de 1994 (1994-03-09), así que la serie completa no debería diferir por eso.
- **Agrupación:** si A ancla al primer día en lugar de encadenar, el número de episodios sube (43 → 51 en la serie completa), pero el veredicto no cambia.
