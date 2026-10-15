# Réplica R14: ¿rebotan los índices después de un desplome de un día?

> Fase 0: formación. No recomienda inversiones. Las secciones 1 a 9 son el pre-registro, escrito el 2026-10-15 antes de calcular cualquier rendimiento posterior a un desplome con estos datos. La hora real es la del commit que lo agrega (`git log` de este archivo).

| Campo | Valor |
|---|---|
| ID | `R14` (script `laboratorio/replicas/R14.py`; salida `R14-salida.txt`) |
| Hallazgo que se prueba | La intuición detrás del pronóstico P0126 (15-oct-2026): "tras una caída de un día mayor a 7%, lo usual es un rebote parcial". También la literatura de reversión de corto plazo en índices tras caídas extremas (sin un artículo único; conocimiento previo: el sesgo de "comprar el pánico"). |
| Pre-registro escrito el | 2026-10-15, antes de cualquier corrida |
| Responsable | A: orquestador. B: `auditor-de-replicas`, código desde cero |
| Estado | **Replicado** (15-oct-2026, A y AC-19 concordantes); el efecto viene de los desplomes dentro de episodios ya en marcha. Etiqueta: descartada como regla operable |

**Conocimiento previo declarado:**
- Sé que tras el 19-oct-1987 y el 16-mar-2020 hubo rebotes fuertes en días siguientes, y que en 2008 hubo varios desplomes seguidos de más caídas.
- No he calculado ninguna cifra con estos datos.

## PRE-REGISTRO (secciones 1 a 9; no se editan después de la primera corrida)

### 1. Hipótesis previa y mecanismo
- **H1:** en cuatro índices (S&P 500, Nasdaq Composite, Nikkei 225 y KOSPI), después de un día con rendimiento ≤ −5% (un "desplome"), el rendimiento acumulado de los **11 días hábiles siguientes** (del cierre del desplome al cierre del día +11) es **positivo en más de 55%** de los eventos agrupados.
- **H2:** su media es **mayor** que la media incondicional de 11 días del mismo índice.
- **Mecanismo:** liquidación forzada y venta por pánico que se revierte cuando se normaliza la liquidez.

### 2. Criterio de refutación
- **H1 refutada** si la frecuencia agrupada de 11 días positivos es ≤ 55%.
- **H2 refutada** si la media agrupada del exceso (11 días tras el desplome menos la media incondicional del índice) es ≤ 0, o si su t (con eventos agrupados en grupos para no contar dos veces un mismo episodio, ver §8) es < 1.0.
- Las dos se sostienen: "Replicado". Solo una: "Replicado con diferencias". Ninguna: "No replicado".

### 3. Datos y licencia
- **A:** Yahoo chart v8 diario (`^GSPC`, `^IXIC`, `^N225`, `^KS11`), con `period1`/`period2` para obtener barras diarias, sin dividendos (índices de precio).
- **B:** la elige el auditor (por ejemplo, Stooq, FRED `SP500` y `NASDAQCOM` para EUA, o la serie del propio mercado).

### 4. Universo
Cuatro índices de precio. Sesgo declarado: son índices de mercados que sobrevivieron y crecieron.

### 5. Fecha de disponibilidad
El evento se conoce al cierre del día del desplome; la ventana empieza en ese cierre. Sin información futura.

### 6. Periodo
Toda la historia diaria disponible en la fuente A para cada índice, hasta el 14-oct-2026. El 15-oct-2026 (KOSPI −7.6%) **no entra**: es el caso que motivó la pregunta.

### 7. Limpieza
Días sin cierre o con cierre repetido (cero exacto por feriado mal marcado) se descartan y se reportan.

### 8. Regla y variantes planeadas
- **Principal:** umbral −5%, horizonte de 11 días hábiles.
- **Episodios:** los desplomes separados por menos de 11 días hábiles en el mismo índice forman un **episodio**; para la t se usa el promedio por episodio, no por día. También se reporta "solo el primer desplome de cada episodio".
- **Variantes declaradas (N = 4):** umbral −5% y −7%, por horizontes de 11 y 22 días.

### 9. Costos y comparación simple
- Sin costos: es una pregunta de pronóstico (P0126), no una estrategia operable desde GBM; no hay ETFs de KOSPI ni de Nikkei en la cuenta.
- **Comparación:** la media incondicional de 11 (o 22) días del mismo índice y la frecuencia incondicional de rendimientos positivos.

---

## RESULTADOS (se llenan después de correr)

### Desviaciones del pre-registro
- **Inicio de las series en A:** con `period1=0`, Yahoo arranca en 1970 (^GSPC) aunque tiene datos desde 1927. B usó ^GSPC desde 1927-12 y FRED NIKKEI225 desde 1949. Por eso A tiene menos eventos en el S&P (27 contra 87) y en el Nikkei (52 contra 56).
- **Fechas de los índices asiáticos:** A y B fechan cada barra por su sello UTC, que en Asia cae el día local anterior. El cierre del KOSPI del 15-oct (−7.6%) aparece con fecha 14-oct, pero no entra como evento porque no tiene ventana completa. Las fechas de eventos asiáticos están corridas un día; los rendimientos no cambian.
- **Descartes de A:** 658 cierres repetidos del Nikkei (sobre todo en la historia antigua de Yahoo). B, con FRED, no los tiene.

### 10. Variantes probadas
Las 4 declaradas (−5% y −7%; 11 y 22 días). N = 4.

### 11. Resultados

| Variante | A (Yahoo): eventos / episodios | A: positivos | A: exceso por episodio (t) | A: solo el primer desplome (positivos / exceso / t) | B: eventos / episodios | B: positivos | B: exceso (t por episodio) | B: solo el primero |
|---|---|---|---|---|---|---|---|---|
| **−5%, 11 d** | 208 / 110 | **65.9%** | +3.44% (**5.40**) | 62.7% / +1.03% / **1.31** | 272 / 148 | **64.0%** | +2.35% (**6.17**) | 60.1% / +0.97% / **1.40** |
| −5%, 22 d | 208 / 110 | 62.5% | +3.41% (3.52) | 62.7% / +1.25% / 1.17 | 272 / 148 | 62.5% | +2.77% (4.05) | 61.5% / +0.99% / 1.10 |
| −7%, 11 d | 62 / 38 | 64.5% | +4.02% (2.71) | 57.9% / +1.35% / 0.80 | 83 / 54 | 63.9% | +2.99% (3.47) | 57.4% / +1.53% / 1.13 |
| −7%, 22 d | 62 / 38 | 59.7% | +3.35% (1.63) | 55.3% / +0.97% / 0.43 | 83 / 54 | 60.2% | +3.25% (2.34) | 53.7% / +1.18% / 0.71 |

- **Frecuencia incondicional de 11 días positivos:** 56-60% según el índice.
- **B por índice, solo el primer desplome (−5%, 11 d):** S&P t 0.12; Nasdaq exceso −2.4% (t −1.32).

### 12. Sensibilidad
- La t por evento en B es 4.04, menor que la t por episodio (6.17): los episodios largos (1929, 2008 y KOSPI) concentran muchos desplomes con rebotes grandes.
- **Solo el primer desplome de cada episodio:** frecuencia de 54-63% (cerca de la incondicional) y t de 0.4-1.4 en todas las variantes, en A y en B.

### 13. Diferencia frente al supuesto
No hay artículo. A y B difieren por el inicio de las series (1927 contra 1970 en el S&P; 1949 contra 1965 en el Nikkei) y la fuente (FRED contra Yahoo en Nasdaq y Nikkei). Mismo signo y mismo veredicto en las 4 variantes.

### 14. Conclusiones permitidas
- En promedio, después de un día de −5% o peor, los 11 días siguientes rinden más que lo normal en los cuatro índices agrupados (64-66% positivos; exceso de +2.3% a +3.4% por episodio, t 5.4-6.2).
- Ese efecto viene de **los desplomes que ocurren con el pánico ya en marcha** (dentro de episodios). El **primer** desplome de un episodio no rebota más de lo normal (t 1.3-1.4 en la principal; S&P t 0.12; Nasdaq en contra).

### 15. Conclusiones que NO se sostienen
- Que "comprar el desplome" sea una regla: el primer desplome es indistinguible de lo normal, y en el momento no se sabe si abre un episodio largo.
- Que P0126 (KOSPI > 5,554.22 el 30-oct, p 0.55) tenga un apoyo fuerte. El 15-oct es, hasta donde se sabe, un primer desplome; la frecuencia relevante es de 57-63%, así que 0.55 está algo bajo pero dentro del rango. **No se edita P0126** (registrado antes de la réplica).

### 16. Estado y reproducción
**Estado: Replicado** (H1 y H2 sostenidas en A y en B, las dos con el criterio del §2). **Etiqueta: descartada** como regla operable: el efecto no aparece en el primer desplome y no hay ETFs de KOSPI ni de Nikkei en la cuenta. Sirve para calibrar pronósticos.

**Reproducción:** `python3 laboratorio/replicas/R14.py` (A) y `python3 -I laboratorio/auditorias/AC-19-R14/b.py` (B). Los datos (~5 y ~4 MB) no se versionan; sus sha256 están en las salidas.

