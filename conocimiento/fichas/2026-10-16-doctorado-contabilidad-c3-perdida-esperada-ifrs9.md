# Ficha · Doctorado en contabilidad C3: pérdida crediticia esperada (IFRS 9) y el efecto escalón

> Trabajo continuo del 15-oct-2026 (19:10 CDMX). Área con cobertura "Sin" en `doctorados/ESTADO.md`. Fase 0: no recomienda inversiones.

## Pregunta
¿Cómo calcula un banco su provisión por pérdida esperada bajo IFRS 9, y por qué puede saltar de golpe aunque ningún crédito haya dejado de pagar? Sirve para leer las provisiones en los post-mortems de bancos (JPM, BAC, WFC, GS, MS y GFNORTE).

## Fuente y nivel de acceso
- **IFRS Foundation, página oficial de IFRS 9** (consultada el 16-oct-2026): objetivo; clasificación en costo amortizado, FVOCI y FVTPL (prueba de modelo de negocio y SPPI); vigencia desde el 1-ene-2018. **Resumen oficial, grado A** en lo que dice; no describe las etapas.
- **BIS, FSI Connect, "IFRS 9 and expected loss provisioning – Executive Summary"** (13-dic-2017): tres etapas, base de intereses por etapa y arreglos transitorios de capital de Basilea. **Grado B**, resumen de un regulador.
- **No se leyó** el texto de la norma: EUR-Lex respondió vacío y el texto de la IFRS Foundation exige registro. La presunción refutable de 30 días de atraso (párr. 5.5.11) y el enfoque simplificado para cuentas por cobrar comerciales (5.5.15) se citan **de memoria** y quedan por verificar.

## Lo que dicen las fuentes
| Etapa | Cuándo | Pérdida que se reconoce | Base de los intereses |
|---|---|---|---|
| 1 | Desde la originación, sin aumento significativo del riesgo | Esperada a **12 meses** | Importe bruto |
| 2 | Aumento significativo del riesgo de crédito (se mide con la probabilidad de incumplimiento, no con el monto de la pérdida) | Esperada **de por vida** | Importe bruto |
| 3 | Crédito deteriorado | Esperada de por vida | **Costo amortizado (neto de la provisión)** |

La pérdida esperada a 12 meses **no** es el faltante de efectivo de los próximos 12 meses: es la parte de la pérdida de por vida que viene de incumplimientos posibles en esos 12 meses (definición de IFRS 9, citada por fuentes secundarias).

## Derivación
Pérdida esperada = Σₜ PD marginal(t) × LGD × EAD(t) × factor de descuento(t). En la etapa 1 la suma se corta en el año 1; en las etapas 2 y 3 abarca toda la vida. Pasar de la etapa 1 a la 2 cambia el horizonte **y** la PD al mismo tiempo: de ahí el escalón.

## Ejercicio numérico (comprobado)
Código: `conocimiento/fichas/codigo/2026-10-16-c3-perdida-esperada-ifrs9.py` (aserciones). Préstamo de 1,000 amortizable a 5 años, LGD 45% y tasa efectiva 8%; supuestos ilustrativos.
- Etapa 1 (PD 1%, 12 meses): **4.17** por cada 1,000.
- Misma PD, pero de por vida: 11.20, solo por cambiar el horizonte.
- Etapa 2 (PD 4%, de por vida): **43.18**, unas 10 veces la etapa 1.
- **Cartera de 100,000:** si solo 10% migra a la etapa 2, la provisión pasa de **417 a 807 (×1.94)**, sin que nadie haya dejado de pagar.
- **Etapa 3:** con una provisión de 450 sobre 1,000, el ingreso por intereses es 44 (sobre el neto) y no 80 (sobre el bruto).

## Evidencia y límites
- **Prociclicidad (inferencia):** las migraciones a la etapa 2 se concentran cuando empeora el pronóstico macro, así que las provisiones suben justo al entrar a la recesión. Basilea dio arreglos transitorios para suavizar el golpe al capital (BIS). No medí la magnitud con datos.
- **US GAAP (ASC 326, CECL)** reconoce desde el inicio la pérdida de por vida, sin etapas. Por eso los bancos de EUA (JPM, BAC) no tienen el escalón de la etapa 2. No se leyó ASC 326; queda pendiente.

## Contraejemplo
Una cartera de tarjetas con PD anual de 15% y vida corta: la diferencia entre 12 meses y de por vida es pequeña porque casi toda la vida cae dentro del primer año. El escalón importa en créditos largos (hipotecas, crédito empresarial).

## Uso en el sistema
En los post-mortems de bancos que reportan en NIIF (GFNORTE, emisoras mexicanas), un salto de provisiones con cartera vencida estable puede ser **migración de etapas por pronóstico macro**, no pérdidas realizadas. Hay que leer la nota de etapas antes de atribuirlo a deterioro real.

## Segunda comprobación
La etapa 1 se verifica a mano: 0.01 × 0.45 × 1,000 / 1.08 = 4.1667 (aserción en el código).

## Estado nuevo
C3 pasa de "Sin" a "Parcial" en `doctorados/ESTADO.md`: deterioro cubierto con ficha y ejercicio. Faltan arrendamientos del lado del arrendador, la clasificación de instrumentos en detalle, ASC 326 y el texto de la norma.
