# Réplica R13: anomalía de devengos (Sloan, 1996), antes y después de publicarse

> Fase 0: formación. No recomienda inversiones. Las secciones 1 a 9 son el pre-registro, escrito el 2026-10-14 (≈17:55 UTC) antes de calcular cualquier rendimiento con estos datos. El ID R12 queda reservado para la propuesta del comité sobre la condición de VIX del filtro del UPRO (R11).

| Campo | Valor |
|---|---|
| ID | `R13` (script `laboratorio/replicas/R13.py`; registro `R13-variantes.csv`; salida `R13-salida.txt`) |
| Artículo original | Sloan, R. G. (1996). "Do Stock Prices Fully Reflect Information in Accruals and Cash Flows about Future Earnings?" *The Accounting Review* 71(3): 289-315 |
| Artículos de contraste | Green, Hand y Soliman (2011), "Going, Going, Gone? The Apparent Demise of the Accruals Anomaly", *Management Science* 57(5); McLean y Pontiff (2016), *Journal of Finance* 71(1) (caída promedio de las anomalías tras publicarse) |
| Fecha de publicación | Julio de 1996 (revista) |
| Pre-registro escrito el | 2026-10-14, antes de cualquier corrida |
| Responsable | A: orquestador (laboratorio). B: `auditor-de-replicas`, código desde cero |
| Estado | en curso |

**Conocimiento previo declarado (el pre-registro no es ciego):**
1. De memoria, sin verificar contra el PDF: Sloan reporta un rendimiento de cobertura de ~10% anual (decil de devengos bajos menos decil alto) en 1962-1991.
2. Green, Hand y Soliman (2011) documentan que la anomalía se debilita mucho después de 2000.
3. McLean-Pontiff estiman una caída promedio de ~58% en el rendimiento de las anomalías después de publicarse; R03 del laboratorio encontró caídas similares en cinco factores.
4. No he visto ninguna cifra del archivo de French que se usa aquí.

---

## PRE-REGISTRO (secciones 1 a 9; no se editan después de la primera corrida)

### 1. Hipótesis previa y mecanismo
- **H1 (antes de publicarse):** el portafolio largo-corto **decil de devengos bajos menos decil alto** (ponderado por valor) tiene un rendimiento medio mensual **positivo con t Newey-West(6) ≥ 2.0** entre 1963-07 y 1996-06.
- **H2 (después de publicarse):** entre 1996-07 y el último mes disponible, la media cae **al menos 50%** contra el tramo anterior y **no es significativa** (t NW < 2.0).
- **Mecanismo (Sloan):** el mercado fija precios con la utilidad total y no distingue que el componente de devengos es menos persistente que el de flujo de efectivo; las empresas con devengos altos decepcionan después.

### 2. Criterio de refutación
- **H1 refutada** si la media 1963-07 a 1996-06 es ≤ 0 o su t NW(6) < 2.0. Con H1 refutada: **No replicado**.
- **H2 refutada** si la media posterior es mayor que 50% de la anterior **o** su t NW(6) ≥ 2.0. Con H1 sostenida y H2 refutada: "Replicado con diferencias" (la anomalía sobrevive a la publicación).
- **Replicado:** H1 y H2 se sostienen.

### 3. Datos y licencia
- **A:** Kenneth French Data Library, `Portfolios_Formed_on_AC` (ordenamientos univariados por AC/B, deciles y quintiles, VW y EW, mensuales), versión CRSP indicada en el encabezado del archivo, sha256 registrado. Factores `F-F_Research_Data_5_Factors_2x3` para alfa (sensibilidad).
- **B:** la elige el auditor. Idealmente, otra construcción de la señal, por ejemplo Open Source Asset Pricing (Chen y Zimmermann), señal "Accruals".
- **Uso académico; se descarga con `herramientas/datos_historicos.py`.**

### 4. Universo
Acciones de NYSE, AMEX y NASDAQ en CRSP con datos de Compustat (construcción de French). **Diferencia de definición declarada:**
- **French:** cambio en capital de trabajo operativo por acción de t−2 a t−1, dividido entre el valor en libros por acción.
- **Sloan:** devengos de balance, incluida la depreciación, divididos entre los activos totales promedio.

### 5. Fecha de disponibilidad
French forma los portafolios a fin de junio con datos contables del año fiscal t−1 (rezago ≥ 6 meses). Sin información futura.

### 6. Periodo
- Antes de publicarse: 1963-07 a 1996-06.
- Después de publicarse: 1996-07 hasta el último mes del archivo.
- Subperiodo informativo, sin criterio: 2001-01 en adelante (Green, Hand y Soliman).

### 7. Limpieza
Valores −99.99 o −999 se tratan como faltantes y se reportan.

### 8. Regla y variantes planeadas (N = 4)
- **Principal:** VW, Lo 10 − Hi 10.
- **Variantes:** EW, Lo 10 − Hi 10; VW, Lo 20 − Hi 20 (quintiles); EW, Lo 20 − Hi 20.
- **Sensibilidad (no cuenta en N):** alfa CAPM y FF5 de la principal en cada tramo.

### 9. Costos y comparación simple
- **Costos:** el largo-corto no es operable en GBM (no hay ventas en corto de acciones del SIC para persona física). Se reporta bruto y con un costo supuesto de 1% anual (rebalanceo anual de dos piernas).
- **Comparación simple:** el mercado (Mkt-RF) en el mismo tramo.
- USD, sin impuestos.

---

## RESULTADOS (se llenan después de correr)

### Desviaciones del pre-registro

### 10. Variantes probadas

### 11. Resultados

### 12. Sensibilidad

### 13. Diferencia frente al artículo

### 14. Conclusiones permitidas

### 15. Conclusiones que NO se sostienen

### 16. Estado y reproducción
