# Decisión: cartera inicial real de la cuenta arena-claude en GBM (20,000 MXN)

- **Fecha de decisión:** 25-sep-2026, después del cierre. La hora queda sellada por el commit de este archivo, antes de cualquier precio de ejecución.
- **Ejecución:** lunes 28-sep-2026, en real, por el dueño en la app de GBM. Decisión del dueño del 25-sep-2026 (`config/parametros.json` → `prioridad_actual.excepcion_cuenta_arena`).
- **Temporada:** 28-sep-2026 a 28-ene-2027 (4 meses).
- **Perfil:** `arena_agresivo`. Tope absoluto del dueño: 10,000 MXN.
- **Estado de este documento:** completo. Comité, verificador y gestor de riesgo (aprueba con cambios, ya aplicados). Boletas en `bitacora/boletas/2026-09-28.md`.

## Tesis y cómo se refutaría

**Tesis:** en 4 meses, el TWR lo decide sobre todo la exposición y el control de pérdidas, no la selección. Ningún análisis mostró ventaja sobre beta 1:
- el cuantitativo midió 78 temporadas: la ventaja neta de las variantes tácticas y apalancadas no es significativa (t entre −1.17 y −0.31);
- el laboratorio tiene 0 de 13 estrategias con ventaja demostrada.

Por eso la cartera es beta de EUA sin apalancar (S&P 500 más Nasdaq-100), con liquidez en MXN. Tiene la menor probabilidad de salir del juego y deja espacio para subir exposición cuando haya datos de los rivales (modo torneo).

**Se refuta si, al 28-dic-2026:**
- la cuenta toca −12%. El modelo daba ~3% de probabilidad suponiendo stops por línea. Sin ellos, que es lo que se ejecuta tras la enmienda del gestor de riesgo, da 15-17%. Ver abajo. O bien
  - **[Corregido 2026-09-25, auditoría 2026-W39]** El 3% (M1 con stops, 3.4%) y el 15-17% (M3 sin stops: 15.2% en 1999-2026 y 16.7% antes de 2016) salen de métodos distintos; la brecha no es solo el efecto de los stops. Mismo método, sin stops → con stops: M1 5.6% → 3.4%; M2 8.9% → 4.5%; M3 15.2% → 4.7%; M3c 6.5% → 2.9%. Sin stops el rango honesto es **6-15%** según el método (16.4% en un recálculo independiente con SPY/QQQ × DEXMXUS 2000-2026; 9.1% con 2011-2026). Además, el modelo mide 4 meses (85 días, al 28-ene-2027), no al 28-dic-2026 (64 días). Ver `bitacora/semanal/2026-W39-verificacion.md`.
- quedamos 3 pp o más atrás de un rival con beta ≤ 1.2 sin que haya un choque de mercado que lo explique.

## Dictámenes (3 líneas cada uno)

- **Macro, confianza 60. Voto: B, variante con SPYM 7 + SPXL 1 + efectivo.**
  - Régimen mixto: tendencia y crédito a favor; bono de 10 años en ~5.18% (máximo desde 2007) y tasa real de 2.76% en contra.
  - ~~Cada +100 pb del bono restó 7.9% al S&P en 2026 (cálculo propio, grado C).~~ **[Corregido 2026-09-25, auditoría 2026-W39]** Sensibilidad de alta frecuencia, no efecto acumulado: en 2026 el bono subió ~+99 pb y el S&P **ganó** +12.3% (FRED DGS10 y SP500, 2-ene a 24-sep). La pendiente depende de la especificación: cambios diarios −8.1% por +100 pb (t NW −4.8); cambios semanales −6.2% (viernes, t −1.6, no significativa) a −8.7% (miércoles, t −3.1); cambios mensuales −3.6% (n = 8, t −0.7); en niveles diarios el signo se invierte (+18%, correlación espuria de tendencias). Cálculo propio, grado C. Ver `bitacora/semanal/2026-W39-verificacion.md`.
  - El USD amortigua en MXN.
- **Geopolítico, confianza 55. Voto: C, con SPYM 5 + TQQQ 4 + XLE 5.**
  - El eje de riesgo es Ormuz → WTI → Fed → tasa real → NDX; XLE funcionó como cobertura en 2026.
  - Registró P0006-P0010.
  - Advierte un posible hueco a la baja el lunes por el ultimátum iraní del fin de semana.
- **Fundamental, confianza 60. Voto: B moderado, con SPYM 5 + SPXL 1 + QQQM 1.**
  - Ninguna acción le gana al índice con evidencia: NVDA, LRCX, GE, XOM, MRK y GMEXICOB, evaluadas.
  - S&P con P/U adelantado de 19.2, pero CAPE de 41.3; la valuación no sirve para decidir cuándo entrar a 4 meses.
- **Abogado del diablo, confianza 70. Voto: A ejecutable, con SPYM 7 + QQQM 1 + Smart Cash.**
  - B y C no sobreviven: con 50% en 3x, P(−12%) ≈ 39%, con la misma mediana que A.
  - Riesgos operativos: títulos enteros, hueco del lunes, stops poco confiables en SIC.
  - Detectó un error en `portafolio.py` (cortacircuitos estándar en la arena). Ya se corrigió en el commit d66f602.
- **Cuantitativo, confianza 55. Voto: C′, con SPYM 5 + XLE 5 + QQQM 1.**
  - Para A: mediana +5.9%, p10 −4.4%, P(−12%) 3%, P(−20%) 0%.
  - Para B1: mediana +7.0%, P(−12%) 19%.
  - Ninguna candidata tiene ventaja sobre beta 1. Simulación en `arena/modelos/cartera_inicial_simulacion.py`.

## Votos y regla aplicada

La regla del skill `comite-de-inversion` es para una tesis. Aquí se eligió entre candidatas, así que se aplicó **por componente**:

| Componente | Votos | ¿Sobrevive al abogado del diablo? | Resultado |
|---|---|---|---|
| SPYM (S&P 500) | 5 de 5 | Sí | **Entra** |
| QQQM (Nasdaq-100) | 3 de 5 (fundamental, abogado del diablo, cuantitativo) | Sí | **Entra** |
| SPXL (S&P 3x) | 2 de 5 | No: "no sobrevive" y sin 4 votos con confianza ≥ 60 | Fuera |
| TQQQ (Nasdaq 3x) | 1 de 5 | No | Fuera |
| XLE (energía) | 2 de 5 | No: C no sobrevive y tiene 0 votos con confianza ≥ 60 | Fuera |

Confianza media del comité: 60. El umbral es 55.

**Decisión: cartera A**, con SPYM y QQQM en títulos enteros y el resto en liquidez en MXN.

## Disenso (se conserva íntegro)

- **Macro y fundamental** quieren una línea de SPXL: más mediana y 46% de probabilidad de quedar primero contra 28% de A, en el campo F1 del cuantitativo. Queda como la primera opción para subir exposición en modo torneo cuando haya reportes de los rivales.
- **Geopolítico y cuantitativo** quieren XLE como cobertura de Ormuz: correlación de −0.25 con el S&P a 60 días. Se descarta por ahora: un acuerdo en Ormuz la castiga, y la regla del abogado del diablo no se supera.
- **Condición del abogado del diablo:** nada apalancado hasta tener 6 reportes semanales de los rivales y el ETF verificado en la app de GBM.

## Pronósticos del comité

| ID | Autor | Pregunta | p | Resuelve |
|---|---|---|---|---|
| P0006-P0010 | analista geopolítico | Ormuz, ataque de EUA, retiro del T-MEC, calificación de México | ver `pronosticos.csv` | nov-2026 a mar-2027 |
| P0011 | macro | S&P > 7,743.41 al 28-mar-2027 | 0.72 | 28-mar-2027 |
| P0012 | fundamental | ^GSPC > 7,743.41 el 28-ene-2027 | 0.63 | 28-ene-2027 |
| P0013 | abogado del diablo | S&P con caída de 10% o más desde su máximo antes del 28-ene-2027 | 0.25 | 28-ene-2027 |
| P0014 | cuantitativo | La cuenta real no toca −12% | 0.90 | 28-ene-2027 |

## Verificación de cifras (verificador, 25-sep-2026)

Ninguna corrección cambia la decisión. Tipo de fuente en cada fila, según el protocolo.

| # | Afirmación | Resultado | Fuente | Tipo |
|---|---|---|---|---|
| 1 | SPYM y QQQM cotizan en SIC a ≈1,606 y ≈5,435 MXN, a menos de 0.3% del precio de EUA × tipo de cambio | **Verificado.** Cierres del 25-sep: 1,605.94 y 5,436.74. En el mismo minuto: −0.01% y +0.14%. Ambas ACTIVAS en BMV (fichas 34716 y 36356). | Yahoo v8 (diario y 1 minuto); fichas de BMV | base estadística |
| 2 | VOO.MX ~12,614 MXN (~63% de la cuenta) | **Corregido.** 12,614 era el máximo intradía. El cierre fue 12,580.84 = 62.9% de la cuenta, 63.1% con comisión. Sigue sin caber bajo el tope de 60% por posición. | Yahoo v8 | base estadística y cálculo propio |
| 3 | 7 SPYM + 1 QQQM ≈ 16,677 MXN; remanente ~3,300 | **Verificado.** 16,678.32 + 48.37 de comisión = 16,726.69. Remanente: **3,273 MXN (16.4%)**. Comisión 0.25% + IVA = 0.29%. | Guía de Servicios GBM jul-2026, págs. 18-19 | filing regulatorio y cálculo propio |
| 4 | Bono de 10 años en ~5.18%, máximo desde 2007 | **Verificado (≈).** ^TNX: 5.184%; Tesoro (CMT): 5.17%. Antes de 2026, el último dato ≥ 5.17% fue el 6-jul-2007. | Yahoo, home.treasury.gov, FRED | base estadística |
| 5 | CPI de EUA a agosto: 3.4% a/a | **Verificado.** El 3.71% del capítulo 04 era falso: venía de un rezago de 13 meses en FRED por el hueco de oct-2025. Se corrigió (commit 11eddf1). | API de BLS, CUUR0000SA0; comunicado del 11-sep | base estadística y reporte narrativo |
| 6 | Smart Cash de GBM | **Existe.** Paga 4.00% a 4.75% según la inversión total en GBM; para 20k aplicaría 4.00% (inferencia). No encontré la tabla de tramos: la página de preguntas frecuentes da 404. | FAQ y Guía de GBM, pág. 7 | reporte narrativo |

**Sin verificar:** que SPYM aparezca en la app de GBM. QQQM solo tiene un indicio. Por eso la boleta incluye una verificación previa y una alternativa.

## Tamaño, stop, criterio de salida y boletas (gestor de riesgo, con veto)

**Veredicto del gestor de riesgo: APRUEBA CON CAMBIOS.** Voto a favor. Los cuatro cambios quedaron aplicados, como se detalla abajo.

**Estado de riesgo al decidir:** libros vacíos (drawdown 0, sin rachas, P&L 0). La cuenta opera en real por `excepcion_cuenta_arena`; el patrimonio principal sigue en fase 0.

### Tamaño: el menor de tres métodos

| Método | Resultado |
|---|---|
| Por stop, con 600 MXN de riesgo (3%) | 7 SPYM (stop −5.3%) y 1 QQQM (stop −11%) |
| Volatilidad objetivo de 20% (Regla 18.4) | No limita |
| Kelly | No limita: A = 0.36× Kelly; en el escenario conservador M2, 1.15× |

| Línea | Títulos | MXN (cierres del 25-sep) | Peso |
|---|---|---|---|
| SPYM (S&P 500) | 7 | 11,256 | 56.3% |
| QQQM (Nasdaq-100) | 1 | 5,429 | 27.1% |
| Smart Cash (liquidez en MXN) | — | ~3,270 | ~16.4% |

### Validaciones

- **`etf_indice_max` (0.6) se aplica por posición:** OK. Si se aplicara a la suma daría 83.4% y la cartera A no cabría. Pero el perfil permite estar 100% invertido y el apalancamiento bruto ≤ 1.0x ya topa la exposición total. `validar_orden` todavía no revisa este límite; se comprobó a mano. Quedó escrito en `config/parametros.json` (`nota_concentracion`).
- **QQQM se clasifica como ETF de índice amplio**, no como sector. Si se etiquetara "tecnología", fallaría `sector_max` de 25%.
- **Sin problema en:**
  - orden mínima;
  - límites de pérdida y cortacircuitos;
  - número de operaciones: 2 de 8 al mes;
  - costos: 100 MXN o menos, frente a +1.85% esperado por temporada sobre CETES.
- **Filtro de apalancados:** no aplica.

### Stop: enmienda a la regla

- **Los ETF de índice 1x van sin stop por línea.** Todo lo táctico, sectorial, de acción individual o apalancado sí lleva stop registrado en GBM desde la entrada.
- **Registro:** la enmienda está en `config/parametros.json` → `excepcion_cuenta_arena.enmiendas`, con el texto anterior, el motivo y el costo reconocido.
- **Autoría:** la regla original la escribió el orquestador. El dueño aprobó "la cartera que apruebe el comité", no un tipo de stop, y puede revertir la enmienda.

**Motivo:**
- En ventanas de 85 días (1999-2026), un stop de −5.3% en SPYM se toca al cierre en 32% de los casos. De esos toques, 58% terminan arriba del stop, y en 10% lo dispara solo el tipo de cambio.
- Con stops, la probabilidad de quedar arriba del rival 1 baja de 46% a 38% (simulación M3).
- Los stops en SIC son poco confiables: el 24-sep SPYM y QQQM no tuvieron ninguna operación en el SIC. Además hay huecos, vigencia máxima de 30 días y días con el SIC cerrado y NYSE abierta.

**Si el dueño prefiere stop:** stop limitada al precio de ejecución − 85 MXN por título de SPYM y − 598 MXN en QQQM. Son ~600 MXN de riesgo por línea (3%). Se renueva cada 30 días.

### Corrección de cifras de riesgo: sin stops

El 3% de probabilidad de tocar −12% que usa la tesis (cuantitativo) supone stops. **Sin stops:**
- P(tocar −12%) = 15-17% (M3);
- P(tocar −20%) = 2.6%;
- peor caso simulado: −27.5%; nunca tocó −35%.

El pronóstico P0014 (p = 0.90 de no tocar −12%) queda registrado tal como se hizo, y se califica igual. El post-mortem debe anotar que se emitió suponiendo stops.

### Qué protege la cuenta sin stop por línea

- **Cortacircuitos del perfil sobre el TWR:**

  | Nivel | Acción |
  |---|---|
  | −12% | Reducir 50% lo táctico. Hoy no hay nada táctico. |
  | −20% | Vender lo que esté bajo su SMA200 y sin apalancados |
  | −28% | Pausa de 2 semanas y post-mortem |
  | −35% | Todo a CETES o liquidez |

- **Tope absoluto del dueño:** 10,000 MXN.
- **Estrés de un S&P −20% en MXN:** la cartera A cae 17.4% (−3,479 MXN). Cruza el −12%, pero no llega a −20%, y le quedan 6,521 MXN de margen al tope. Para tocar −35%, las acciones tendrían que caer 42%.
- **Escenarios de cola:**

  | Escenario | Efecto en la cartera A |
  |---|---|
  | Un día como el 16-mar-2020 | −6.95% (−1,389 MXN); el peso amortigua |
  | La semana del 2 al 8 de abril de 2025 | −9.46% (−1,892 MXN). Con stops se habría vendido todo antes del rebote del 9-abr, cuando A iba en −0.4%. |
  | Peso +20% | −13.9% (−2,781 MXN). El máximo visto en 85 días fue +19.6% (2009). |

### Criterio de salida

- **Por regla, sin comité:** los cortacircuitos y el tope de 10,000 MXN.
- **Por decisión:** solo el comité semanal (el primero es el viernes 2-oct-2026) puede rebalancear o subir exposición en modo torneo.
  - Por disenso, la primera opción para subir exposición es una línea de SPXL.
  - Condición: 6 reportes semanales de los rivales y el ETF verificado en la app de GBM.

### Boletas y condición de validez

- **Boleta real:** `bitacora/boletas/2026-09-28.md`, ejecución manual del dueño en GBM.
- **Registro sombra en papel:** `bitacora/ordenes-pendientes.csv` (O0001 y O0002), con la misma condición de validez.
- **Condición de validez a las 08:45 CDMX del lunes:** SPYM en NYSE > 88.98 USD (−2% frente al cierre del viernes, 90.80) y VIX < 25. La decisión se tomó con VIX en 14.87.
- **Si no se cumple: EN ESPERA.** No se compra. El martes 29-sep se reevalúa a la misma hora con la misma regla. Si tampoco se cumple, decide el comité del viernes 2-oct.
