# Ficha · Doctorado contabilidad C2 · Ingresos por construcción en concesiones (CINIIF 12 con NIIF 15): por qué el "ingreso total" de los aeropuertos no se pronostica con tráfico

**Pregunta.** En el post-mortem de ASUR (23-oct), los ingresos totales salieron 9.3% arriba de nuestro punto, y casi todo el error vino de la línea de "construcción". ¿Qué norma la crea, qué margen tiene y cómo debe pronosticarse para los aeropuertos y otras concesionarias del universo (ASUR, GAP, OMA, PINFRA)?

## Fuente y nivel de acceso
| Fuente | Acceso | Grado |
|---|---|---|
| **AASB Interpretation 12 *Service Concession Arrangements*** (PDF de aasb.gov.au, `INT12_08-15.pdf`, sha256 `04c38984…`). Dice: "For-profit entities complying with AASB Interpretation 12 also comply with IFRIC 12" | **Lectura íntegra** de los §12-§20 (consenso) | A (texto equivalente a la CINIIF 12) |
| NIIF 15 (AASB 15), a la que remiten los §13-§15 | No se leyó hoy en texto íntegro | nv |
| ASUR 3T26: ingresos 10,420.5; construcción 2,591.1; EBITDA 4,719.3; margen ajustado 60.3% | Evento relevante de la BMV del 22-oct (`empresas/ASURB.MX/post-mortem-2026-10-23.md`) | A |

## Derivación (texto literal)
1. **§12:** el operador "acts as a service provider". Construye o mejora la infraestructura (servicio de construcción) y la opera (servicio de operación).
2. **§13-§14:** el ingreso de **cada** servicio, incluida la construcción, se reconoce conforme a la NIIF 15. Por eso aparece un **ingreso por construcción** aunque el dinero lo ponga el propio operador.
3. **§15-§17:** la contraprestación por construir es un **activo financiero**, si hay un derecho incondicional a cobrar al concedente (§16), o un **activo intangible**, si es el derecho a cobrar a los usuarios (§17). En los aeropuertos mexicanos, que cobran TUA y tarifas a los usuarios, predomina el **intangible**.
4. **§19:** durante la construcción, las dos se clasifican como **activo de contrato**.
5. **Consecuencia** (inferencia, consistente con lo que reporta ASUR): el ingreso por construcción va con un **costo de construcción casi igual**, de margen ≈ 0. Lo que lo mueve es el **capex comprometido del Plan Maestro de Desarrollo**, no el tráfico.

## Ejercicio comprobado (`fichas/codigo/2026-10-26-c2-ifric12-asur.py`)
- **ASUR 3T26:** los ingresos sin construcción son **7,829.4**. El margen EBITDA es **60.3%** sobre ingresos sin construcción, que cuadra con el ajustado que reporta ASUR (`assert`), y **45.3%** sobre ingresos totales.
- **Sensibilidad:** con el mismo EBITDA, si la construcción pasa de 1,000 a 3,500, el margen sobre el total cae de 53.4% a 41.7%, **sin ningún cambio operativo**.
- **Error de nuestro pronóstico:** −9.31% sobre el total y **−2.29% sin construcción**. Esos 7.6 puntos del ingreso los explica la construcción, que supusimos en ~1,800 contra 2,591.1 real.
- **Segunda comprobación:** la descomposición del error se verifica con un `assert`.

## Evidencia y límites
- Los márgenes y crecimientos de "ingresos totales" de las concesionarias **no son comparables entre trimestres** si el capex cambia. El consenso de "ingresos" de los proveedores a veces incluye la construcción y a veces no; ya nos pasó con Q.MX y ASUR.
- **Límites:**
  - no leí la NIIF 15 íntegra, ni la NIF D-1 / INIF 17 mexicana;
  - no revisé la nota contable de ASUR que dice qué parte es activo financiero y qué parte es intangible;
  - el "margen ≈ 0" de construcción sale de la práctica reportada, no del texto de la CINIIF 12.

## Contraejemplo
Si el contrato tuviera un **pago garantizado del concedente** (§16), lo que se reconoce es un activo financiero. La construcción podría tener margen y su ingreso podría parecerse más a un flujo operativo. Es el caso de algunas carreteras con pago por disponibilidad, posible en PINFRA, y no el de los aeropuertos con tarifa al usuario.

## Estado nuevo
- **C2: de Parcial a Parcial,** con texto íntegro de la CINIIF 12 y un caso real comprobado. Falta leer la NIIF 15 completa para cubrir el área.
- **En `estado-de-dominio.csv`:** se agrega el tema "Ingresos en concesiones (CINIIF 12)" como **Comprendido con comprobación**.
- **Regla para las fichas de las concesionarias** (ASUR, GAP, OMA, PINFRA): pronosticar **por separado** los ingresos sin construcción, que dependen del tráfico y las tarifas, y la construcción, que depende del Plan Maestro de Desarrollo. El binario de "ingresos > consenso" debe declarar cuál de los dos usa el consenso.
