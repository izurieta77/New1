# Investigador, corrida vespertina · 2026-10-25 (20:12 CDMX; escrita a las 2026-10-26 02:17 UTC del 26-oct)

**Barrido corto, turno fiscal** (doctorados, una de cada tres). Rotación: 22-oct fiscal, 23-oct riesgo, 24-oct cripto, 25-oct fiscal.

## Búsquedas
1. **LISR vigente en la Cámara de Diputados (fuente primaria, HTTP 200):** `LeyesBiblio/pdf/LISR.pdf`, 3,021,915 bytes. Su sha256 `803c2875c09c…` es **idéntico** al de la copia congelada en V05 (última reforma DOF 01-04-2024). La LISR no ha cambiado desde abril de 2024.
2. **Lectura íntegra de los arts. 5 y 142 fr. V** en `laboratorio/replicas/V05-spiva-y-fiscalidad-sic/datos/legal/LISR.txt`, más el art. 140 para contrastar.
3. **Convenio México-EUA, art. 10** (texto del IRS congelado en V05): 10% "in other cases" y 15% durante los primeros cinco años.
4. **GBM** (FAQ congeladas en V05): las retenciones en el orden de la ley. "ISR anual del 35%" es la tarifa máxima, no una tasa fija (trampa ya anotada en el cap. 27).
5. **No consultado:**
   - la RMF 2026;
   - el Senado, por el Paquete 2027: sin fuente primaria nueva esperable antes del pleno del 27-oct; en la corrida del 22-oct, `senado.gob.mx` dio 403.

## Hallazgo (grado A, por la letra de la ley y el tratado; la fórmula es cálculo propio)
**Los dividendos de EUA vía SIC pagan tres capas, no dos:**
1. **EUA:** 10% con W-8BEN y 30% sin él.
2. **México:** 10% definitivo sobre el neto (art. 142 fr. V).
3. **México:** **acumulación a la tasa marginal**, acreditando solo hasta la tasa del tratado. Según el art. 5, el excedente se acredita solo después del procedimiento amistoso y no es deducible.

**Resultado:**
- τ_div = **t_m + 9 pp con W-8BEN** (39% con t_m = 30%; **44% con 35%**);
- τ_div = **t_m + 27 pp sin W-8BEN** (57% y 62%).

Verificado con dos métodos en un script del scratchpad, fuera del repo (cálculo paso a paso y forma cerrada).

**Corrige lo nuestro:**
- El 20% central de R19b ("10% EUA + 10% México") omite la capa 3. Solo es correcto con t_m ≈ 11%. **R19b no se editó.**
- Pregunta 3 del cap. 27: no todo el impuesto de EUA es acreditable sin W-8BEN.
- §6.3 regla 1: la comparación con el UCITS de acumulación solo contaba la retención en origen.

## Qué cambia
- **R19b:** el arrastre central está subestimado. [Estimación por interpolación lineal de su propia tabla, τ_int = 20%] ~1.43 pp con t_m = 30% y ~1.47 pp con 35%, contra 1.26. H1b (≥1.0 pp) se sostiene con más margen. La corrida con τ_div correcto queda para el laboratorio.
- **Reglas:**
  - §6.2 regla 3 (no tramitar el W-8BEN en la arena) se sostiene: el ahorro real es de 18 puntos del dividendo, ~0.18 pp al año.
  - §6.3 regla 1 podría invertirse: el UCITS de acumulación ganaría ~0.29 pp al año, si se sostiene la inferencia de §2.7. Queda en decisiones pendientes.
- **Para la cartera:** nada inmediato. **Ningún parámetro cambia.**
- **Archivos:**
  - adenda del 2026-10-25 en el cap. 27;
  - una fila en el registro de errores;
  - fila de "Fiscalidad 2026 y SIC" en estado-de-dominio;
  - entrada en decisiones pendientes: la t_m del dueño, R19b-bis, el UCITS y si el patrimonio real tiene W-8BEN.
