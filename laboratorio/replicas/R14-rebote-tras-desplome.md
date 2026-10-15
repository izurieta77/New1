# Réplica R14: ¿rebotan los índices después de un desplome de un día?

> Fase 0: formación. No recomienda inversiones. Las secciones 1 a 9 son el pre-registro, escrito el 2026-10-15 antes de calcular cualquier rendimiento posterior a un desplome con estos datos. La hora real es la del commit que lo agrega (`git log` de este archivo).

| Campo | Valor |
|---|---|
| ID | `R14` (script `laboratorio/replicas/R14.py`; salida `R14-salida.txt`) |
| Hallazgo que se prueba | La intuición detrás del pronóstico P0126 (15-oct-2026): "tras una caída de un día mayor a 7%, lo usual es un rebote parcial". También la literatura de reversión de corto plazo en índices tras caídas extremas (sin un artículo único; conocimiento previo: el sesgo de "comprar el pánico"). |
| Pre-registro escrito el | 2026-10-15, antes de cualquier corrida |
| Responsable | A: orquestador. B: `auditor-de-replicas`, código desde cero |
| Estado | en curso |

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
