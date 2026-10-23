# Ficha · Doctorado contabilidad C5 · ¿Por qué la tasa efectiva de las emisoras mexicanas no es 30%? NIC 12 §41, §47, §34 y §81(c)

**Pregunta.** En los post-mortems del 21 y 22-oct, la tasa efectiva fue la sorpresa de la UPA en AMX, BMV y Alpek (Alpek: 15.2% contra 28% supuesto). ¿Qué dice la NIC 12 sobre las causas posibles, y cómo debe pronosticarse la tasa?

## Fuente y nivel de acceso
| Fuente | Acceso | Grado |
|---|---|---|
| **AASB 112 *Income Taxes*, compilación F2021C00853** (legislation.gov.au, PDF de 52 páginas, sha256 `04570e44…c14e`), que dice: "For-profit entities complying with AASB 112 also comply with IAS 12". Para empresas con fines de lucro, el texto es la NIC 12 | **Lectura íntegra** de los §5 (definiciones), §34-36 (pérdidas fiscales), §41 (moneda funcional distinta de la fiscal), §47-49 (tasa promulgada) y §81(c)-(e) (conciliación de la tasa) | A (texto equivalente) |
| EUR-Lex, Reglamento (UE) 2023/1803 | **Sin acceso hoy:** respondió HTTP 202 con un desafío anti-bots. La ficha C4 del 19-oct sí lo leyó | — |
| LISR art. 9 (30%) y deducción de inversiones actualizada por INPC | Ficha C5 del 11-oct y cap. 32 | A (texto) |
| Alpek 3T26: impuestos 466 M sobre 3,067 M antes de impuestos (15.2%) | `empresas/ALPEKA.MX/post-mortem-2026-10-22.md` (XBRL de la BMV) | A en la cifra; **la conciliación del §81(c) no está en el trimestral** |
| USD/MXN al 30-jun-2026 (17.4490) y al 30-sep-2026 (18.0609) | FRED DEXMXUS (`laboratorio/replicas/R19-datos/`) | A |

## Derivación
1. **Tasa efectiva = gasto por impuestos / utilidad contable**, y el gasto incluye el corriente y el diferido (§5). Todo lo que mueve el diferido sin mover la utilidad mueve la tasa.
2. **§41, literal:** las partidas no monetarias se miden en la moneda funcional. Si la base fiscal está en otra moneda, "changes in the exchange rate give rise to temporary differences" y el diferido resultante "is charged or credited to profit or loss". Es el caso de una subsidiaria mexicana con **moneda funcional USD** y base fiscal en MXN.
   - **Si el peso se deprecia,** la base fiscal en USD cae, aparece un pasivo diferido y **sube la tasa**.
   - **Si el peso se aprecia,** aparece un activo diferido y baja la tasa, si se reconoce (§24).
   - **La actualización por INPC de la base fiscal compensa** cuando la inflación iguala a la depreciación.
3. **§34-35:** el activo por pérdidas fiscales se reconoce solo si es probable usarlo. Reconocer (o dar de baja) pérdidas de años previos mueve la tasa de un trimestre sin relación con la operación.
4. **§47:** se miden con la tasa promulgada. Un cambio de ley (por ejemplo, la reforma a la LISR que está en el Senado) revalúa todo el saldo diferido de golpe.
5. **§81(c):** la emisora debe conciliar su tasa efectiva con la tasa aplicable; §81(e) añade las diferencias y las pérdidas no reconocidas. **Esa conciliación es la fuente para pronosticar la tasa**, y viene en las notas **anuales**, no en el trimestral.

## Ejercicio comprobado (`fichas/codigo/2026-10-23-c5-nic12-tasa-efectiva-fx.py`)
Activo no monetario de 1,000 USD, utilidad de 200 USD y tasa de 30%:

| Caso | Diferido | Tasa efectiva |
|---|---|---|
| El peso se deprecia de 17.00 a 18.70 | +27.27 USD | **43.6%** |
| El peso se aprecia de 17.00 a 16.00 | −18.75 | **20.6%** |
| Se aprecia, pero el activo no se reconoce (§24) | 0 | 30.0% |
| Se deprecia 10% y el INPC sube 10% | 0 | 30.0% |
| USD/MXN real del 3T26 (17.449 → 18.061) | +10.17 | **35.1%** |

**Sensibilidad:** cada 1% que sube el dólar agrega **+0.6, +1.5 y +3.0 pp** a la tasa cuando la base fiscal es 2, 5 y 10 veces la utilidad.

## Evidencia y contraejemplo
- **Alpek es un contraejemplo de la regla simple.** En el 3T26 el peso se **depreció** 3.5%, y con el §41 la tasa de una subsidiaria con moneda funcional USD habría **subido**. Alpek reportó **15.2%**. Por lo tanto, otra partida dominó. Candidatas, sin verificar:
  - reconocer pérdidas fiscales (§34);
  - el ajuste anual por inflación (LISR art. 44) sobre su deuda;
  - la mezcla de jurisdicciones (EUA al 21%, Brasil y Argentina);
  - la moneda funcional: **no verifiqué la de sus subsidiarias** (nv).
- **Lección:** el tipo de cambio da la dirección **de una** partida, no de la tasa total. Sin la conciliación del §81(c), el pronóstico de la tasa debe partir del promedio de los últimos 4 trimestres y de la conciliación anual, no del 30% de ley.

## Límites
- Las cifras son ilustrativas. El activo es un solo bloque, no hay partidas permanentes y la utilidad en USD es fija.
- No toca las partidas monetarias. En una entidad con moneda funcional USD, la deuda en MXN genera una diferencia cambiaria contable distinta de la fiscal (ganancia o pérdida cambiaria acumulable).
- No leí NIF D-4 ni ASC 740 (pendientes desde la ficha del 11-oct).
- El texto es la versión australiana compilada a 2021. Las modificaciones posteriores de la NIC 12 (Pilar Dos, 2023) no están, y no tocan los §34, §41, §47 ni §81(c).

## Segunda comprobación
Por fórmula cerrada: diferido = T × valor × (1 − (1 + INPC) × fx0 / fx1). Da lo mismo en los cinco casos (`assert`).

## Estado nuevo
- **C5 (impuestos diferidos): queda Parcial en `ESTADO.md`,** pero sube en profundidad:
  - el texto íntegro de los párrafos clave ya está leído (antes solo el resumen oficial);
  - hay un mecanismo comprobado con código y un contraejemplo real.
- **Faltan:** pensiones (NIC 19), pagos basados en acciones (NIIF 2) y NIF D-4.
- **Fila "Doctorado contabilidad C4-C5" en `estado-de-dominio.csv`:** de Documentado a **Comprendido con comprobación** en la parte de impuesto diferido. La fila agrupa C4 y C5, y la evidencia lo distingue.
- **Regla para las fichas de empresa** (se suma a la lección de los post-mortems): en la §8, anotar la tasa efectiva de los últimos 4 trimestres, la moneda funcional de las subsidiarias principales y la conciliación del §81(c) del último informe anual.
