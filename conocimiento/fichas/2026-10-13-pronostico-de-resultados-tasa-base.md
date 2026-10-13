# Ficha · 13-oct-2026 · Pronóstico de resultados empresariales: la tasa base de sorpresas y su costo en Brier

> Laboratorio del martes (tema no doctoral). Se eligió "Pronóstico de resultados empresariales" porque está en Documentado (el nivel más bajo de los temas no doctorales) y porque hoy se resuelven los primeros pronósticos de resultados del 3T26 (JPM, WFC, GS, JNJ, UNH y AMX).

## 1. Pregunta

¿Con qué frecuencia una empresa del S&P 500 reporta ventas y UPA arriba del consenso, y cuánto cuesta en Brier no partir de esa tasa base al pronosticar "ingresos > consenso"?

## 2. Fuente y acceso

**FactSet, *Earnings Insight* del 31-jul-2026** (PDF oficial, `advantage.factset.com`, sha256 `d50f94b1…`). Texto extraído y leído en las secciones de *scorecard* (lectura de sección). Citas literales:
- EPS: "86% have reported actual EPS above estimates, which is above the **5-year average of 78%** and above the **10-year average of 76%**."
- Ingresos: "77% of S&P 500 companies have reported actual revenues above estimates, which is above the **5-year average of 70%** and above the **10-year average of 68%**."
- Tamaño de la sorpresa de ingresos: promedio de **1.9%** a 5 años y **1.6%** a 10 años. EPS: **7.0%** a 5 años y **7.4%** a 10 años.

Grado **A** para las cifras (fuente primaria del proveedor del consenso).

## 3. Derivación

- Si la sorpresa estandarizada (real − consenso)/σ sigue N(μ, 1) y la probabilidad de superar el consenso es q, el sesgo implícito del consenso es μ = Φ⁻¹(q). Con q = 0.70 (ingresos), **μ ≈ 0.52 σ**: el consenso de ventas sale, en promedio, medio error típico por debajo del dato. Es la evidencia de la "gestión de expectativas" (las empresas guían a la baja para ganarle al consenso).
- El Brier esperado de pronosticar p cuando la probabilidad real es q es q(1−p)² + (1−q)p², mínimo en p = q.

## 4. Ejercicio (código: `codigo/2026-10-13-tasa-base-sorpresas.py`, con aserciones)

| Pronóstico | Brier esperado con q = 0.70 |
|---|---:|
| 0.50 (moneda al aire) | 0.2500 |
| 0.57 | 0.2269 |
| 0.70 (tasa base) | **0.2100** |

**Nuestros ocho pronósticos de "ingresos > consenso" del 3T26** (25-sep): media **0.512**, contra la tasa base de 0.70. Sin información específica, partir de 0.50 cuesta unas **0.04 de Brier por pronóstico**. El BAC en 0.13 solo se justifica con información muy fuerte.

## 5. Evidencia y primer caso

- **JPM (hoy, 13-oct):** ingresos reportados de 50,172 M contra un consenso de 50,847 M → **no superó**. Un caso no refuta la tasa base. Nuestro 0.50 queda mejor que el 0.70 en este caso (Brier 0.25 contra 0.49), pero la tasa base gana en promedio.
- **Límite de la tasa base:** depende de qué se mida. JPM tiene ingresos "reportados" y "administrados" (50,907 M, base equivalente fiscal); el consenso suele estar en base administrada. Si el criterio dice "reportados", la comparación es contra un consenso que se construyó en otra base. Para bancos, esa diferencia (~1.5%) es casi igual a la sorpresa típica.

## 6. Contraejemplo y segunda comprobación

- **Contraejemplo:** en recesiones o choques (2008, 2020), la tasa de sorpresas positivas de ingresos baja; la tasa base no es estable por régimen.
- **Segunda comprobación:** el 77% del 2T26 (dato del mismo informe) cae dentro de un rango razonable alrededor del 70% a 5 años; y el μ implícito de 0.52 σ es coherente con una sorpresa media de +1.9% en ingresos si σ ≈ 3.6% (1.9 / 0.52).

## 7. Qué cambia

- **Regla de trabajo propuesta (para la skill `ficha-empresa`):** los pronósticos binarios de "ventas o UPA arriba del consenso" parten de la tasa base (≈0.70 ventas, ≈0.78 UPA) y solo se alejan de ella con información específica escrita en la ficha; además, el criterio debe declarar si el dato es reportado o administrado, igual que el consenso. Se anota para el comité; no se modifica la skill sin aprobación.

## 8. Estado nuevo

"Pronóstico de resultados empresariales": de **Documentado** a **Comprendido con comprobación**.
