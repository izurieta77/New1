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
| Estado | **Replicado** (14-oct-2026, A y AC-18 concordantes; etiqueta: descartada como fuente de rendimiento) |

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
- Ninguna en A. B usó como segunda fuente Open Source Asset Pricing (release de oct-2025, datos hasta 2024-12). Su señal no resta la depreciación y excluye acciones con precio < 5. Como cotejo usó French con código propio.

### 10. Variantes probadas
Las 4 declaradas (VW y EW, deciles y quintiles). N = 4. Ninguna agregada. Registro en `R13-variantes.csv`.

### 11. Resultados
Largo-corto Lo−Hi, % mensual, bruto. "Pre" = 1963-07 a 1996-06; "post" = 1996-07 al final.

| Serie | A (French, hasta 2026-08): pre (t NW6) | A: post (t NW6) | Caída | B (OSAP, hasta 2024-12): pre (t NW6) | B: post (t NW6) | Caída |
|---|---|---|---|---|---|---|
| **VW deciles (principal)** | **0.414 (3.29)** | **0.163 (0.93)** | **60.6%** | **0.488 (3.10)** | **0.107 (0.59)** | **78.0%** |
| EW deciles | 0.416 (4.90) | 0.266 (1.95) | 36.0% | 0.666 (6.23) | 0.103 (0.89) | 84.6% |
| VW quintiles | 0.382 (3.61) | 0.167 (1.20) | 56.3% | 0.265 (2.02) | 0.159 (1.00) | 40.1% |
| EW quintiles | 0.368 (5.19) | 0.211 (2.09) | 42.7% | 0.456 (4.97) | 0.084 (0.85) | 81.5% |

- **Principal desde 2001-01:** A 0.062 (t 0.34); B 0.024 (t 0.13).
- **Con costo de 1% anual:** A pre 0.331 (2.63) y post 0.080 (0.45); B pre 0.405 (2.57) y post 0.024 (0.13).
- **Alfa CAPM:** A pre 0.472 (3.93) y post 0.178 (1.01); B pre 0.621 (4.30) y post 0.066 (0.34).
- **Alfa FF5:** A pre 0.445 (3.85) y post 0.118 (0.69); B pre 0.439 (2.83) y post 0.170 (0.91).
- **Mercado (Mkt-RF):** pre 0.467 (t 2.05); post 0.749 (t 3.11).
- **B con los datos de French y su propio código:** reproduce a A (0.414 / 0.163 / 60.6%). En el periodo común hasta 2024-12, post 0.146 (t 0.81) y caída de 64.7%.

### 12. Sensibilidad
- **Ponderado por igual:** en French conserva t ≈ 2 después de 1996 (1.95 y 2.09); en OSAP no (0.85-0.89). La supervivencia en acciones pequeñas depende de la construcción.
- **Señales distintas:** correlación mensual OSAP-French de la principal de solo 0.40, y aun así las dos dan el mismo veredicto.

### 13. Diferencia frente al artículo
- **Artículo (Sloan, tabla 6):** +10.4% anual (t 4.71) en el primer año, ajustado por tamaño, ponderado por igual, NYSE/AMEX, 1962-1991.
- **A (VW, ×12):** ~5.0% anual, más pequeño porque pondera por valor, usa otra definición (ΔCTO/libro) e incluye NASDAQ.
- **B (EW deciles):** 0.666 × 12 ≈ 8.0%, más cerca del artículo.
- Diferencias explicadas por la ponderación, la definición y el universo.

### 14. Conclusiones permitidas
- **Antes de publicarse:** la anomalía existe en dos construcciones independientes (t NW 3.1-3.3 en la principal).
- **Después de publicarse:** el portafolio ponderado por valor pierde 61-78% y deja de ser significativo. Desde 2001 es prácticamente cero.
- **El alfa FF5 de antes de 1996 sigue significativo en A y B:** los factores de inversión no absorben toda la anomalía en estos datos (contra la lectura de Wu, Zhang y Zhang, de la que solo se leyó el resumen).

### 15. Conclusiones que NO se sostienen
- Que la anomalía sea explotable hoy en grandes empresas.
- Que sobreviva en pequeñas: solo una de dos fuentes lo muestra.
- Que se pueda operar desde GBM: no hay ventas en corto en el SIC.
- Que sea prima por riesgo: no se probó (Sloan concentra más de 40% del rendimiento en los anuncios).

### 16. Estado y reproducción
**Estado: Replicado** (H1 y H2 sostenidas en A y en B; rige la más conservadora y las dos coinciden). **Etiqueta: descartada** como fuente de rendimiento: ninguna versión es significativa después de publicarse con la segunda fuente, y no es operable. Se conserva como filtro de calidad de utilidades en las fichas de empresas (cap. 03 §2.10). Reproducción: `python3 laboratorio/replicas/R13.py` (A) y `python3 -I laboratorio/auditorias/AC-18-R13/b.py` (B). Los datos de B (~180 MB) no se versionan: URL y sha256 en `AC-18-R13/informe.md`.
