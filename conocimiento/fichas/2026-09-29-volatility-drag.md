# Ficha de estudio: volatility drag, de la identidad a los ETF apalancados reales

> Bloque de trabajo continuo, 29-sep-2026 (19:09 CDMX). Fase 0. Tema "Crecimiento geométrico y matemática del compuesto" (cap. 01), que estaba en Documentado. El paso pendiente era un "ejercicio propio de volatility drag con datos French".
> Código: `conocimiento/fichas/codigo/2026-09-29-volatility-drag.py` (stdlib + `herramientas`, ~2 s). Salida reproducida dos veces con idéntico resultado.

## 1. Pregunta
¿Se cumple con datos reales la regla del cap. 01, **G ≈ A − σ²/2**, y su extensión al apalancamiento, **g(L) ≈ r_f + L·μ − L²·σ²/2** con máximo en L* = μ/σ²? ¿Cuánto se aleja un ETF 3x real (UPRO) de esa fórmula?

## 2. Fuentes y acceso
| Fuente | Acceso |
|---|---|
| Kenneth French Data Library, `F-F_Research_Data_Factors` mensual y anual (sha256 593f4fbef031…) | Íntegro, 1926-07 a 2026-08 (1,202 meses; 99 años calendario 1927-2025) |
| French, `F-F_Research_Data_Factors_daily` (sha256 2f29e2254606…) | Íntegro, 1926-07-01 a 2026-08-31 (26,317 días) |
| Yahoo Finance chart v8, SPY y UPRO (cierre ajustado) | Íntegro, 2009-06-25 a 2026-09-28 (4,340 días comunes) |

Rendimiento de mercado = Mkt-RF + RF, como lo construye French. Ninguna fuente es información privilegiada.

## 3. Resultados
**3.1 La identidad (mercado de EUA, 100 años)**

| Medida | A (aritm.) | σ | G | Drag observado | σ²/2 |
|---|---|---|---|---|---|
| Mensual, anualizado (A×12; 12·ln(1+G)) | 11.59% | 18.32% | 9.87% log (10.38% compuesto) | 1.72 pp | 1.68 pp |
| Años calendario (99) | 12.19% | 19.74% | 10.27% | 1.92 pp | 1.95 pp |

- La aproximación falla por **0.04 pp** en mensual y por **0.03 pp** en anual.
- Por década, el drag observado se aleja de σ²/2 entre **−0.19 y +0.13 pp**. El drag va de 0.73 pp (años cincuenta, σ 11%) a 6.27 pp (años treinta, σ 36%). El drag no es una constante: es la varianza del periodo.

**3.2 Apalancamiento diario sintético (sin costos; 1926-2026)**
- μ en exceso = 8.18%, σ = 17.46%, r_f = 3.14%, con lo que **L* = μ/σ² = 2.68**.

| L | g observado (log/año) | Fórmula | CAGR | MDD |
|---|---|---|---|---|
| 1 | 9.79% | 9.79% | 10.28% | −84.1% |
| 1.5 | 11.96% | 11.98% | 12.71% | −94.6% |
| 2 | 13.36% | 13.40% | 14.29% | −98.4% |
| 3 | 13.77% | 13.95% | 14.76% | −99.9% |
| 4 | 10.87% | 11.46% | 11.48% | −100.0% (práctica) |

- La fórmula acierta hasta L = 2 (0.04 pp o menos). En 3x y 4x la sobrestima por 0.2-0.6 pp, porque ignora la asimetría y las colas gruesas, que pesan más con L alto.
- El crecimiento es casi plano entre 2x y 3x y cae a partir de ahí, como predice la parábola.
- **Cualquier L ≥ 2 habría perdido 98% o más en 1929-1932.** El "óptimo" de crecimiento es inservible sin filtro ni cortacircuitos.

**3.3 ETF real: UPRO (3x S&P) contra SPY, 2009-2026**
- SPY: g = 14.04% log (CAGR 15.07%), σ = 17.0%.
- UPRO: g = 28.29% log (CAGR 32.69%), σ = 51.0%, beta diaria 2.989.
- La fórmula −2·r_f + 3·A − 9σ²/2 da 30.50%. **El real quedó 2.22 pp/año debajo**: gasto de 0.91% más el financiamiento de los swaps por encima de r_f, y la diferencia de seguimiento.
- "3 × el crecimiento de SPY" (42.1%) sobrestima a UPRO por 13.8 pp/año: ése es el drag del apalancamiento (3σ² más el costo del dinero prestado) más los costos.
- **Límite:** la muestra de UPRO no incluye 2000-2002 ni 2008. Es el periodo más favorable posible para un 3x.

## 4. Lo que cambia para el sistema (inferencias, no reglas)
1. **G ≈ A − σ²/2 queda comprobada** como herramienta de cálculo, con error de 0.2 pp o menos en cualquier década. Puede usarse sin simulación para 1x-2x.
2. **L* es muy sensible a μ.** Con σ = 17.5%: μ = 8.2% → L* 2.68; 6% → 1.97; 4% → 1.31; 2% → 0.66; 0 → 0. Con los costos de UPRO (~1.1 pp por unidad de apalancamiento adicional), el L* histórico baja a ~2.3. Si la prima esperada es baja, como sugiere un 10a de 5.2%, el apalancamiento óptimo por crecimiento queda **debajo de 1.5x**.
3. **Para el comité del 2-oct:** un 3x rinde más solo si μ se sostiene y si el filtro o los cortacircuitos cortan la cola (R06 y AC-07). Sin eso, la historia de 100 años dice −99.9%. En una temporada de 4 meses, el drag de un 3x con σ de 51% es de ~13 pp anualizados (~4 pp en la temporada), y ese costo depende de la varianza realizada, no de acertar la dirección. La prima, en cambio, no está asegurada.

## 5. Preguntas abiertas
- Medir la brecha de 2.2 pp de UPRO por tramos de tasa: el financiamiento del swap debería encarecerse con r_f alto, como hoy.
- Repetir 3.2 con el filtro SMA200 para ver cuánto del drag y de la cola recorta, y conectarlo con R06.
