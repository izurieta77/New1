# Ficha · Doctorado en contabilidad C7 · Valuación por ingreso residual: identidad, excedente limpio y qué descuenta el precio de Visa (28-oct-2026)

**Pregunta:** ¿cuándo da el modelo de ingreso residual (RIV) el mismo valor que el descuento de dividendos? ¿Qué lo rompe en la práctica (excedente sucio)? ¿Qué crecimiento del ingreso residual descuenta hoy el precio de Visa?

**Por qué este tema:** es miércoles y toca un doctorado (REGLAS §0d). El área menos cubierta, D11 (abuso y razón de negocios), no tiene fuente primaria alcanzable hoy: el Semanario Judicial de la SCJN (sjf2.scjn.gob.mx) responde 403 con desafío antibots y la búsqueda no localizó tesis con registro digital. Paso a C7, que está en Parcial y sirve para las fichas de empresas (sección "Qué descuenta el precio").

## Fuente y nivel de acceso
- **Ohlson (1995)**, *Contemporary Accounting Research* 11(2), 661-687: **no leído** (sin copia legal localizada). Las ecuaciones se toman de una reproducción secundaria.
- **Spilioti y Karathanassis**, "An empirical application of the clean-surplus valuation model: the case of the London Stock Exchange", EFMA 2005: **lectura de §1-§2** (PDF íntegro). Reproduce los tres supuestos de Ohlson:
  - (1) valor = VP de dividendos;
  - (2) excedente limpio, y_t = y_{t−1} + x_t − d_t;
  - (3) dinámica lineal de la información.
  - Con (1)-(2), P_t = y_t + Σ R^{−τ} E[x^a_{t+τ}], con x^a_t = x_t − (R − 1) y_{t−1}. **Grado B** para la identidad, porque es álgebra verificable; **C** para la evidencia empírica del paper.
- **Datos:** SEC companyfacts de Visa (CIK 1403161, XBRL de 10-K), leído hoy con el User-Agent por defecto del repo (sin correo); 8-K del 27-oct (acciones diluidas del 4T FY26: 1,882 M); Yahoo (cierre del 27-oct: 401.86).

## Supuestos y derivación
- De (2): d_t = x_t − (y_t − y_{t−1}). Se sustituye en el VP de dividendos y se suma por partes; con y_T/R^T → 0, queda **P_0 = y_0 + Σ R^{−t} (x_t − r·y_{t−1})**.
- **La identidad no necesita ningún supuesto contable** más allá del excedente limpio. Las recompras cuentan como distribución (d incluye recompras netas de emisiones).
- **En estado estacionario** (ROE y crecimiento g constantes): P = B + (ROE − r)·B / (r − g). Despejando, **g = r − (ROE − r)·B / (P − B)**.

## Ejercicio comprobado (`fichas/codigo/2026-10-28-c7-ingreso-residual-visa.py`)
1. **Plan sintético de 30 años más terminal** (ROE de 18% a 9%, pago creciente): DDM = RIV = **210.381032**; diferencia de 1.4e−13.
2. **Contraejemplo, excedente sucio:** un ORI de −2 por año que no pasa por la utilidad. RIV − DDM = **20.5473** = VP exacto del ORI en 30 años (20.5473). El RIV sobrevalúa justo lo que el ORI le quita al libro.
3. **Visa, excedente limpio por año** (ΔB − (X − D − recompras)): el residuo sin ORI es de **+0.2 a +1.1 mil M USD por año** desde 2010.
   - Encaja con los pagos en acciones que se abonan al capital: es la partida "sucia" típica de una emisora con mucha compensación en acciones.
   - 2008 es la reestructuración y la OPI: el residuo de 34.3 mil M suma la OPI (ProceedsFromIssuanceOfCommonStock 19.1 mil M) y las acciones emitidas en la reorganización de oct-2007 (StockIssued, no monetario, 17.9 mil M), menos ajustes. [Verificador W44, 30-oct-2026: antes decía "OPI (emisión de 34 mil M)"; fuente: SEC companyfacts, 10-K FY2010.]
   - El ORI llegó a −2.81 mil M (2022, tipo de cambio).
4. **Qué descuenta el precio** (B FY25 de 37.9 mil M; ROE de 51.3%; r = 9%, supuesto):
   - capitalización de 756 mil M ⇒ **g perpetuo del ingreso residual ≈ 6.8%** (5.7% con r = 8%; 7.8% con r = 10%);
   - **segunda comprobación:** Gordon sobre distribuciones con pago = 1 − g/ROE da los mismos 756 mil M.
   - [Verificador W44, 30-oct-2026: insumos FY25 confirmados en companyfacts (B 37,909 M; X 20,058 M; B FY24 39,137 M), así como 1,882 M de acciones diluidas del 4T FY26 y el cierre de 401.86 del 27-oct (Yahoo). Pero el mismo 8-K del 27-oct ([q42026earningsrelease.htm](https://www.sec.gov/Archives/edgar/data/1403161/000140316126000126/q42026earningsrelease.htm)) ya trae el **FY26**: patrimonio de 36,111 M al 30-sep-2026 y utilidad de 23,504 M, lo que da un ROE de 62.0%. Con esos datos (r = 9%), **g ≈ 6.3%** (5.3% con r = 8%; 7.4% con r = 10%), con un pago implícito de 90% (D1 de 20.1 mil M). El 6.8% es correcto con los datos FY25, pero mezcla el libro de hace un año con el precio y las acciones de oct-2026. Cálculo propio.]

## Evidencia empírica y límites
- Con ROE de 51% el libro casi no informa: el 95% del valor es VP del ingreso residual.
- El supuesto que pesa es g: con P = 756, un g de 6.8% para siempre equivale a que Visa crezca más que la economía nominal indefinidamente. [Inferencia] El precio descuenta que la ventaja de la red se mantiene.
- **Inconsistencia que detecta el modelo:** en estado estacionario el pago implícito sería de 87% (1 − 6.8/51.3), con distribuciones de 16.9 mil M. Visa distribuyó 22.9 mil M en FY25 (25.6 mil M en FY26, contra una utilidad de 23.5 mil M; 8-K del 27-oct, [Verificador W44]), más de lo que gana: el libro baja y el ROE sube por construcción. **Con recompras mayores a la utilidad, el ROE no es una variable exógena.** Se debe modelar el ingreso residual sobre el capital invertido operativo, no sobre el patrimonio contable (Penman; no leído).
- La evidencia empírica de Ohlson citada en el EFMA (Bernard 1995: 68% contra 29% de los dividendos; Penman-Sougiannis 1998; Francis-Ohlson-Oswald 2000) es **de segunda mano**: no se usa como prueba.

## Contraejemplo
- **Empresas con patrimonio negativo o casi nulo por recompras** (p. ej., Visa en 2007 con −0.5 mil M): el RIV con ROE sobre patrimonio contable no está definido. Hay que pasar a ingreso residual operativo (ReOI) o volver al DCF.

## Qué cambia
- **Para las fichas de empresas:** en "Qué descuenta el precio" se puede agregar el g implícito del ingreso residual junto al DCF inverso, con la advertencia de excedente sucio (ORI y pagos en acciones) y de ROE inflado por recompras.
- **Ninguna regla ni pronóstico.**

## Estado nuevo
- **C7 (valuación basada en contabilidad, ingreso residual):** de *Parcial* a **Parcial con comprobación**: identidad comprobada, contraejemplo cuantificado y caso real con datos XBRL.
- **Falta para Comprobada:** Ohlson (1995) y Penman en texto íntegro, y una prueba fuera de muestra (por ejemplo, el g implícito contra el rendimiento posterior).
