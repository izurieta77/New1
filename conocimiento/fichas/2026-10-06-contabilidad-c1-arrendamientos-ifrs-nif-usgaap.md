# Ficha · Doctorado contabilidad C1 · Marco de normas (NIF / NIIF-IFRS / US GAAP) a través de un caso: arrendamientos

**Pregunta.** Dos empresas con el mismo contrato de arrendamiento y los mismos flujos, una bajo IFRS y otra bajo US GAAP, ¿muestran la misma utilidad, EBITDA y deuda? Si no, ¿cómo se compara una emisora mexicana (IFRS) con una de EUA (US GAAP) antes de usar EV/EBITDA o deuda/EBITDA?

## Fuente y nivel de acceso real
| Fuente | Acceso | Grado |
|---|---|---|
| IFRS Foundation, página de IFRS 16 (resumen oficial): "single lessee accounting model", activos y pasivos por todo arrendamiento de más de 12 meses salvo activo de bajo valor; activo por derecho de uso y pasivo por arrendamiento | Resumen oficial leído hoy (no el texto íntegro de la norma, que es de acceso restringido) | B |
| FASB, ASU 2016-02 / ASC 842 | **No accesible** (403 desde este entorno). El tratamiento del contrato operativo (un solo costo de arrendamiento lineal en resultados, con activo y pasivo en balance) es de conocimiento general, **sin verificar aquí** | C |
| CINIF, NIF D-5 "Arrendamientos" | El sitio lo anuncia (curso en línea de 3 horas); **el texto de la NIF es de pago, no leído**. Que D-5 siga el modelo único del arrendatario como IFRS 16 es lo que se espera, **sin verificar aquí** | C |
| Qué normas usan las emisoras de la BMV | No verificado aquí (se cree que la CNBV exige IFRS a las emisoras; falta la disposición) | C |

## Supuestos y derivación
Arrendamiento de 5 años, pago anual vencido de 100, tasa de descuento 8%.
- Pasivo inicial = VP de los pagos = 100 × (1 − 1.08⁻⁵) / 0.08 = **399.27**; activo por derecho de uso = 399.27.
- **IFRS 16 (modelo único):** gasto = depreciación lineal (399.27/5 = 79.85) + interés sobre el saldo del pasivo. El gasto total es mayor al inicio y menor al final.
- **ASC 842, contrato operativo (a verificar):** un solo costo lineal de 100 por año, dentro de gastos de operación; activo y pasivo también en balance.
- El gasto total de los 5 años es el mismo (500 = pagos), cambia el calendario.

## Ejercicio numérico (código: `fichas/codigo/2026-10-06-arrendamientos-ifrs16-asc842.py`)
| Año | Depreciación | Interés | Gasto IFRS 16 | Pasivo final |
|---|---|---|---|---|
| 1 | 79.85 | 31.94 | 111.80 | 331.21 |
| 2 | 79.85 | 26.50 | 106.35 | 257.71 |
| 3 | 79.85 | 20.62 | 100.47 | 178.33 |
| 4 | 79.85 | 14.27 | 94.12 | 92.59 |
| 5 | 79.85 | 7.41 | 87.26 | 0.00 |
Total IFRS 16 = 500.00 = pagos totales. **Segunda comprobación:** el VP se calculó por suma de flujos y por fórmula cerrada (coinciden a 1e-9) y el pasivo se agota exactamente en el año 5.

## Qué cambia para el inversionista
1. **EBITDA:** bajo IFRS 16 el costo del arrendamiento sale por completo del EBITDA (depreciación e interés quedan debajo); en el contrato operativo de US GAAP queda **dentro** de gastos operativos. La misma empresa tiene EBITDA 100 mayor en IFRS (por este contrato).
2. **Deuda:** IFRS 16 suma 399.27 de pasivo financiero; en US GAAP el pasivo operativo también está en balance, pero suele quedar fuera de la "deuda financiera" en las comparaciones. EV/EBITDA y deuda/EBITDA solo son comparables si se ajusta el mismo concepto en ambos lados.
3. **Utilidad:** en el primer año IFRS 16 reporta 11.80 más de gasto que el costo lineal; en el quinto, 12.74 menos. Las empresas con muchos arrendamientos nuevos parecen menos rentables al principio.
4. **Relación con la cartera del dueño:** QQQM, SPYM y UPRO contienen empresas de EUA (US GAAP); una emisora mexicana (p. ej. de la lista de vigilancia: ASUR B, AMX) reporta en IFRS. Un múltiplo cruzado sin ajuste mezcla definiciones.

## Límites
Un solo contrato, pago constante y tasa fija: no hay pagos variables, opciones de renovación ni arrendamientos de bajo valor. US GAAP y NIF D-5 no se leyeron en texto oficial. Ni IFRS ni US GAAP son iguales en arrendamientos financieros (donde ASC 842 coincide con el modelo de IFRS 16).

## Contraejemplo
Un contrato de 11 meses queda fuera del modelo (exención de 12 meses): el pago va a gasto lineal, sin pasivo. Una empresa con puros contratos cortos no cambia de EBITDA.

## Estado nuevo
**Documentado con comprobación** (IFRS 16 por resumen oficial grado B + ejercicio comprobado en Python; ASC 842 y NIF D-5 pendientes de texto oficial). Siguiente prueba: leer el texto íntegro de NIF D-5 y IFRS 16; construir la tabla completa NIF/IFRS/US GAAP (C1) y un caso con una emisora del universo.
