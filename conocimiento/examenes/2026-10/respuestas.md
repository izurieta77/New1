# Examen mensual de titulación, octubre 2026: respuestas

Libro cerrado: solo el repositorio /home/user/New1 y python3. No se leyó conocimiento/examenes/. Cuando algo no viene en la base, se marca como inferencia.

---

## 1. Inmunización con dos cupones cero (3 y 10 años)
**Fuente:** no está en la base (no hay Redington ni inmunización). Las fórmulas de duración y convexidad vienen de conocimiento/04-maestria-renta-fija-tasas-macro.md §2.2 y conocimiento/01-licenciatura-fundamentos.md. Lo demás es inferencia con la teoría estándar.
- (a) VP = 10,000,000 / 1.08^6 = **6,301,696 MXN**.
- (b) La duración Macaulay de un cupón cero es su plazo. Hay que resolver w3 + w10 = 1 y 3·w3 + 10·w10 = 6, lo que da w10 = 3/7 y w3 = 4/7.
  - Bono a 3 años: **57.14% = 3,600,969 MXN** (nominal a vencimiento: 3,600,969 × 1.08^3 = 4,536,184).
  - Bono a 10 años: **42.86% = 2,700,727 MXN** (nominal a vencimiento: 2,700,727 × 1.08^10 = 5,830,667).
- (c) Condición de Redington: valor presente igual, duración igual y **convexidad (o dispersión) de los activos mayor que la del pasivo**. Es equivalente a Σ w_i (t_i − D)² > 0.
  - Dispersión: Σw·t² = 4/7·9 + 3/7·100 = 48, contra 6² = 36 del pasivo, así que M² = **12 > 0**.
  - Convexidad modificada, t(t+1)/(1.08)²: activos **46.30** contra pasivo **36.01**.
  - **Sí la cumple.** Ojo: eso protege solo ante desplazamientos paralelos y pequeños; los cambios de pendiente sí pueden afectar.

## 2. ETF del S&P 500 en MXN, con y sin cobertura
**Fuente:** conocimiento/16-macro-global-divisas-y-el-peso.md §2.1 y conocimiento/11-mexico-mercado-instrumentos-fiscalidad.md (CIP: F/S = (1+i_MXN)/(1+i_USD)).
- (a) Sin cobertura: (1.08 × 18.36/17.00) − 1 = 1.08 × 1.08 − 1 = **16.64%**.
- (b) Forward: F = 17.00 × 1.07/1.045 = **17.4067**.
- (c) Se vende a plazo 1 USD a 17.4067 y los 0.08 USD de ganancia, que quedan descubiertos, se cambian al spot de 18.36. Valor final: 17.4067 + 0.08 × 18.36 = 18.8755 MXN, así que el rendimiento es **11.03%**. Equivale aproximadamente a 8% + diferencial de 2.4% + la ganancia cambiaria sobre la utilidad no cubierta.

## 3. Volatilidad y contribución al riesgo (60/40)
**Fuente:** conocimiento/07-doctorado-riesgo-sizing-portafolio-backtesting.md §2.5 (contribución = w_i·(Σw)_i) y conocimiento/02-maestria-portafolio-y-asset-pricing.md.
- (a) σ² = 0.36·0.0225 + 0.16·0.0625 + 2·0.6·0.4·0.3·0.15·0.25 = 0.0081 + 0.0100 + 0.0054 = 0.0235, así que **σ = 15.33%**.
- (b) Contribuciones:
  - A: 0.6 × (0.6·0.0225 + 0.4·0.01125) = 0.6 × 0.018 = 0.0108, que es el **45.96%** de la varianza.
  - B: 0.4 × (0.4·0.0625 + 0.6·0.01125) = 0.4 × 0.03175 = 0.0127, que es el **54.04%**.

## 4. Efecto disposición (Odean 1998)
**Fuente:** conocimiento/08-doctorado-conductuales-microestructura-pronostico.md §2.2 y tabla de literatura (línea de Odean 1998).
- **Definición:** es la tendencia a vender demasiado pronto las acciones que ganan y a retener demasiado tiempo las que pierden (Shefrin-Statman 1985). Se mide así:
  - PGR = ganancias realizadas / (ganancias realizadas + ganancias en papel);
  - PLR = lo mismo con pérdidas.
- **Odean (1998), con 10,000 cuentas:** **PGR = 0.148** y **PLR = 0.098**.
  - La razón PGR/PLR es **≈ 1.51** y la diferencia es de 0.05.
  - En diciembre se invierte (0.108 contra 0.128), por impuestos.
  - Costo: la ganadora que se vende rinde +2.4% sobre el mercado al año siguiente y la perdedora que se retiene, −1.0%, una diferencia de 3.4 pp.

## 5. Perold y Sharpe (1988)
**Fuente:** no está en la base (el repo solo cita Perold-Schulman 1988, sobre coberturas cambiarias). Respondo por inferencia con la teoría estándar.
- **Comprar y mantener:** pago **lineal**. No compra ni vende. En tendencia queda en medio; en oscilación es neutral.
- **Mezcla constante:** compra lo que baja y vende lo que sube, así que su pago es **cóncavo** (es como vender convexidad u opciones). **Gana en mercados que oscilan sin tendencia** (con reversión) y pierde con tendencia.
- **CPPI:** compra lo que sube y vende lo que baja, así que su pago es **convexo** (replica un put protector). **Gana en mercados con tendencia** (alcista o bajista) y pierde con el "serrucho".
- Las estrategias convexas y las cóncavas son contrapartes: una compra el seguro que la otra vende.

## 6. Ley fundamental de la gestión activa
**Fuente:** conocimiento/02-maestria-portafolio-y-asset-pricing.md (Grinold 1989: IR ≈ IC·√BR, con TC).
- IR = 0.05 × √100 = **0.50**.
- Con TC = 0.6: IR = 0.6 × 0.50 = **0.30**.

## 7. Duración y convexidad, +150 pb
**Fuente:** conocimiento/04-maestria-renta-fija-tasas-macro.md §2.2 y conocimiento/01-licenciatura-fundamentos.md (ΔP/P ≈ −D*·Δy + ½·C·Δy²).
- Solo con duración: −7 × 0.015 = −10.50%.
- Ajuste por convexidad: ½ × 60 × 0.015² = +0.675%.
- Total: **≈ −9.83%**.

## 8. Cota de Hansen-Jagannathan
**Fuente:** conocimiento/06-doctorado-asset-pricing-empirico-y-anomalias.md §2.2.
- La desigualdad es **σ(m)/E(m) ≥ |E(R^e)|/σ(R^e)**, con E(m) = 1/R_f.
- Sharpe = 0.06/0.18 = 0.3333 y E(m) = 1/1.02 = 0.9804.
- Entonces σ(m) ≥ 0.3333 × 0.9804 = **0.327** (≈ 32.7% anual).

## 9. Acertijo de la prima de riesgo
**Fuente:** conocimiento/06-doctorado-asset-pricing-empirico-y-anomalias.md §2.1 y §2.3 (prima ≈ γ·Cov(Δc, r); Mehra-Prescott).
- γ = 0.06 / (0.02 × 0.18 × 0.2) = 0.06/0.00072 = **≈ 83**.
- **Por qué es un acertijo:** con aversiones razonables (de 1 a 10), el consumo es tan suave y tan poco correlacionado con la bolsa que el modelo genera una prima minúscula. Mehra-Prescott: con γ = 10, apenas 1.4 pp contra 6.18% observada.
- Además, un γ tan alto dispara la tasa libre de riesgo (12.7% con γ = 10, contra 0.8% observada). Ése es el *risk-free rate puzzle*.

## 10. Descomposición de Campbell-Shiller
**Fuente:** conocimiento/06-doctorado-asset-pricing-empirico-y-anomalias.md §2.5.
- La identidad es dp_t ≈ const + Σρ^{j−1}(r_{t+j} − Δd_{t+j}), más un término de burbuja que se descarta.
- Las dos fuentes de variación son:
  1. noticias sobre **rendimientos futuros**, es decir, tasas de descuento;
  2. noticias sobre el **crecimiento futuro de dividendos**.
- Cochrane (2008, 2011): el crecimiento de dividendos no es predecible. Por lo tanto, **≈ 100% de la variación se atribuye a tasas de descuento (rendimientos) y ≈ 0% a dividendos**. Su cita: "toda la variación de P/D corresponde a variación de tasas de descuento".

## 11. Prueba GRS
**Fuente:** conocimiento/20-metodos-cuantitativos-y-econometria.md §2.4.
- **Hipótesis:** H₀: α_i = 0 para las N carteras **conjuntamente**. Equivale a que los factores estén en la frontera eficiente (las carteras no suben el Sharpe alcanzable).
- **Estadístico:** J = ((T−N−K)/N)·α̂'Σ̂⁻¹α̂/(1 + μ̄'Ω̂⁻¹μ̄), que se distribuye **F(N, T−N−K)** con errores normales iid.
- Con los datos de la pregunta: **F(25, 572)**, porque 600 − 25 − 3 = 572.

## 12. Corrección de Shanken
**Fuente:** conocimiento/20-metodos-cuantitativos-y-econometria.md §2.4 (multiplicar por 1 + λ'Σ_f⁻¹λ).
- Factor = 1 + (0.005/0.045)² = 1 + 0.012346 = **1.0123** (la varianza crece 1.23%).
- El error estándar se multiplica por √1.0123 = **1.0062**, es decir, crece **≈ 0.62%**.

## 13. Harvey, Liu y Zhu (2016)
**Fuente:** conocimiento/06-doctorado-asset-pricing-empirico-y-anomalias.md §2.6 y §7.
- Hay que exigir **t > 3.0** (en vez de 2).
- **Por qué:** cientos de factores se probaron sobre los mismos datos (pruebas múltiples o data mining). Al corregir por esas pruebas (Bonferroni, Holm, BHY), el umbral de 1.96 deja una tasa de falsos descubrimientos muy alta. Para que un factor nuevo sea creíble, el listón tiene que subir.

## 14. Riesgo de largo plazo (Bansal-Yaron 2004)
**Fuente:** conocimiento/06-doctorado-asset-pricing-empirico-y-anomalias.md §2.4. La condición IES > 1 es inferencia: la base solo da la calibración ψ ≈ 1.5.
- **Ingredientes:**
  1. Preferencias de **Epstein-Zin**, que separan γ de la IES (ψ).
  2. Un **componente pequeño y muy persistente** en el crecimiento esperado del consumo y los dividendos: x_{t+1} = ρx_t + …, con ρ ≈ 1.
  3. **Volatilidad estocástica** (σ_t variable).
- **Condición:** se necesita **IES (ψ) > 1**. Además se requiere γ > 1/ψ, es decir, preferencia por la resolución temprana de la incertidumbre.
  - Con ψ > 1, las buenas noticias de crecimiento suben la razón precio-dividendo; domina el efecto sustitución sobre el efecto riqueza.
  - Así el riesgo de largo plazo tiene precio positivo y alto. La calibración típica es ψ ≈ 1.5 y γ ≈ 10.

## 15. Black-Litterman: Π = δΣw
**Fuente:** conocimiento/07-doctorado-riesgo-sizing-portafolio-backtesting.md §2.6.
- Σ = [[0.0256, 0.016], [0.016, 0.04]], con cov = 0.5·0.16·0.20 = 0.016.
- Σw = [0.0256·0.6 + 0.016·0.4, 0.016·0.6 + 0.04·0.4] = [0.02176, 0.0256].
- Π = 2.5·Σw = **[5.44%, 6.40%]**.

## 16. DeMiguel, Garlappi y Uppal (2009)
**Fuente:** conocimiento/07-doctorado-riesgo-sizing-portafolio-backtesting.md §2.6 y conocimiento/02-maestria-portafolio-y-asset-pricing.md.
- **Qué compara:** 14 modelos de optimización (media-varianza muestral, bayesianos, con restricciones, mínima varianza, etc.) contra la regla ingenua **1/N**, en 7 bases de datos y fuera de muestra.
- **Qué concluye:** **ninguno** le gana consistentemente a 1/N en Sharpe, equivalente cierto ni rotación. El error de estimación de las medias se come la ganancia de optimizar.
- **Datos necesarios:** con 25 activos harían falta **≈ 3,000 meses** (≈ 250 años); con 50 activos, ≈ 6,000.

## 17. Sharpe deflactado: máximo esperado
**Fuente:** conocimiento/07-doctorado-riesgo-sizing-portafolio-backtesting.md §2.10 y conocimiento/fichas/2026-09-29-dsr-minbtl.md (E[max Z] con N = 10 → 1.575).
- E[max SR] = √V·[(1−γ)Φ⁻¹(1−1/N) + γΦ⁻¹(1−1/(Ne))], con γ = 0.5772.
- Con N = 10, el corchete vale (0.4228)(1.2816) + (0.5772)(1.7894) = **1.5746**.
- V = 0.5: √0.5 × 1.5746 = **≈ 1.11**.
- V = 1: **≈ 1.57**.

## 18. Volatility drag con apalancamiento diario
**Fuente:** conocimiento/07-doctorado-riesgo-sizing-portafolio-backtesting.md §2.1 y conocimiento/fichas/2026-09-29-volatility-drag.md (g(L) ≈ r_f + Lμ − L²σ²/2; L* = μ/σ²).
- σ² = 0.0289.
- g(1) = 0.03 + 0.06 − 0.01445 = **7.56%**.
- g(3) = 0.03 + 0.18 − 9·0.0289/2 = 0.03 + 0.18 − 0.13005 = **8.00%**.
- L* = 0.06/0.0289 = **2.08**, con g(L*) = 0.03 + 0.06²/(2·0.0289) = **9.23%**. Todo esto es antes de costos.

## 19. Kelly binario
**Fuente:** conocimiento/07-doctorado-riesgo-sizing-portafolio-backtesting.md §2.2 y conocimiento/fichas/2026-09-25-kelly-fraccional.md.
- f* = p − q/b = 0.55 − 0.45 = **10%** del capital.
- Medio Kelly da **75%** del crecimiento máximo, por la fórmula 2c − c² con c = 0.5.
  - Cálculo exacto binario: G(0.05)/G(0.10) = **74.9%**, con G(0.10) = 0.005008 por apuesta.

## 20. PSR
**Fuente:** conocimiento/07-doctorado-riesgo-sizing-portafolio-backtesting.md §2.10 (fórmula del PSR).
- SR diario = 1/√252 = 0.06299.
- Con normalidad, γ₃ = 0 y γ₄ = 3, así que el denominador es √(1 + 0.5·SR²) = 1.00099.
- z = 0.06299 × √84 / 1.00099 = 0.5773.
- PSR = Φ(0.577) = **≈ 0.72**: solo 72% de confianza de que el Sharpe verdadero sea > 0, lejos del 95%.
