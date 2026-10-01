# Examen mensual de titulación · octubre 2026 · PREGUNTAS (sin clave)

> Generado el 1-oct-2026 por la rutina 5. Nivel CFA III y examen doctoral de asset pricing. 20 preguntas de 3 puntos (60 en total). La clave está cifrada en `clave.enc` y sus huellas en `compromiso.json`, en el mismo commit que este archivo y antes de cualquier respuesta. Libro cerrado: solo la base del repositorio y cálculos en Python. Responde con el procedimiento y la cifra final en cada inciso.

**Bloque A · Gestión de portafolios (CFA III)**
1. Un fondo debe pagar 10,000,000 MXN dentro de 6 años. La curva es plana en 8% anual efectivo. Lo inmuniza con dos bonos cupón cero, a 3 y a 10 años. (a) ¿Cuál es el valor presente del pasivo? (b) ¿Qué peso en valor y cuántos pesos van a cada bono para igualar valor presente y duración? (c) ¿Qué condición de dispersión o convexidad debe cumplir el portafolio y la cumple?
2. Un inversionista en MXN compra 1 USD de un ETF del S&P 500 a USD/MXN 17.00. En un año, el ETF rinde +8% en USD y el tipo de cambio cierra en 18.36. Tasas a 1 año: MXN 7.0% y USD 4.5%. (a) ¿Cuál es el rendimiento sin cobertura en MXN? (b) ¿Cuál es el forward a 1 año por paridad cubierta? (c) ¿Cuál es el rendimiento en MXN si cubrió con ese forward exactamente el principal inicial (1 USD)?
3. Una cartera tiene 60% en el activo A (σ 15%) y 40% en B (σ 25%), con correlación 0.3. (a) ¿Cuál es su volatilidad? (b) ¿Qué porcentaje de la varianza aporta cada activo (contribución al riesgo)?
4. Sesgo conductual: define el efecto disposición y da las dos cifras centrales de Odean (1998), PGR y PLR, con su razón.
5. Perold y Sharpe (1988) comparan comprar y mantener, la mezcla constante y CPPI. ¿Qué forma tiene el pago de cada una (lineal, cóncava, convexa) y cuál gana en un mercado con tendencia y cuál en uno que oscila sin tendencia?
6. Ley fundamental de la gestión activa: con IC = 0.05 y 100 apuestas independientes al año, ¿cuál es el IR? ¿Y con un coeficiente de transferencia de 0.6?
7. Un bono tiene duración modificada de 7 y convexidad de 60. Si el rendimiento sube 150 pb, ¿cuál es el cambio porcentual aproximado del precio, con duración y convexidad?

**Bloque B · Asset pricing doctoral**
8. Cota de Hansen-Jagannathan: con prima de mercado de 6% anual, volatilidad del exceso de 18% y tasa libre bruta de 1.02, ¿cuál es la cota inferior de σ(m)? Escribe la desigualdad.
9. Acertijo de la prima de riesgo con utilidad CRRA y consumo lognormal: si E(R^e) ≈ γ·σ(Δc)·σ(r)·ρ, con σ(Δc) = 2%, σ(r) = 18%, ρ = 0.2 y prima de 6%, ¿qué aversión al riesgo γ hace falta? ¿Por qué es un acertijo?
10. Descomposición de Campbell-Shiller del cociente dividendo-precio: ¿qué dos fuentes de variación puede tener el log(D/P) y qué fracción le atribuye la evidencia (Cochrane) a cada una?
11. Prueba GRS (Gibbons, Ross y Shanken, 1989): ¿qué hipótesis prueba? ¿Cuál es la distribución del estadístico con T = 600 meses, N = 25 carteras y K = 3 factores (grados de libertad)?
12. Corrección de Shanken (1992) a Fama-MacBeth con un factor: λ = 0.5% mensual y σ_f = 4.5% mensual. ¿Cuál es el factor que multiplica la varianza y cuánto se infla el error estándar?
13. Según Harvey, Liu y Zhu (2016), ¿qué umbral de estadístico t debe exigirse hoy a un factor nuevo y por qué?
14. Riesgo de largo plazo (Bansal y Yaron, 2004): ¿cuáles son sus tres ingredientes y qué condición sobre la elasticidad de sustitución intertemporal (IES) necesita?
15. Black-Litterman: con δ = 2.5, dos activos (σ 16% y 20%, ρ = 0.5) y pesos de mercado de 0.6 y 0.4, calcula los excesos de rendimiento implícitos Π = δΣw.
16. DeMiguel, Garlappi y Uppal (2009): ¿qué compara su estudio, qué concluye y cuántos meses de datos harían falta, aproximadamente, para que la media-varianza muestral le gane a 1/N con 25 activos?

**Bloque C · Riesgo, sizing y validación (con la base del sistema)**
17. Sharpe deflactado: con N = 10 pruebas independientes sin habilidad y varianza del Sharpe entre pruebas V = 0.5, ¿cuál es el máximo esperado del Sharpe (aproximación de Bailey-López de Prado)? ¿Y con V = 1?
18. Volatility drag con apalancamiento diario: con μ (exceso) = 6%, σ = 17% y r_f = 3% anual, calcula el crecimiento geométrico aproximado g(L) para L = 1 y L = 3, y el apalancamiento que maximiza el crecimiento.
19. Kelly: en una apuesta binaria a la par con p = 0.55, ¿qué fracción de Kelly completo corresponde? ¿Qué fracción del crecimiento máximo se obtiene con medio Kelly?
20. PSR: una estrategia con Sharpe anual de 1.0 se mide en 85 días hábiles, con rendimientos normales. ¿Cuál es el PSR contra SR* = 0? Usa 252 días al año.
