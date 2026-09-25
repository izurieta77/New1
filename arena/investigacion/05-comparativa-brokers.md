# 05. Comparativa de brókers y decisión final para la cuenta arena (20,000 MXN)

**Fecha de corte:** 2026-09-25.
**Insumos:** `arena/investigacion/brokers/B1-gbm-linea-base-.md` (B1), `B2-casas-de-bolsa-y-apps-mexicanas.md` (B2), `B3-interactive-brokers-para-residentes-en-mexico.md` (B3) y `B4-fiscalidad-comparada-y-otros-brokers-extranjeros.md` (B4), los cuatro ya verificados (cada uno trae su propia sección "Verificacion" del 2026-09-25). Herramienta: `herramientas/costos_broker.py`, con sus tests en `herramientas/tests/test_costos_broker.py`.
**Cuenta:** `arena-claude`, capital 20,000 MXN, perfil `arena_agresivo` (`config/parametros.json`). Límite duro de rotación: `operaciones_max_mes = 8` (96 operaciones/año) y `rotacion_max_mensual_x_capital = 1.5`. Orden mínima de la estrategia: 5,000 MXN.

**Etiquetas:** **[H]** hecho con fuente (viene de B1-B4) · **[C]** cálculo propio, mostrado, sobre datos con fuente · **[I]** inferencia · **[R]** recomendación. Nada en este documento se inventa: todo número sale de B1-B4 o de una corrida de `costos_broker.py` que se puede repetir.

---

## 0. Resumen (8 líneas, para el memorándum)

1. **[R] Recomendación: quedarse en GBM esta temporada.** Ningún bróker gana lo suficiente para justificar el cambio, dado lo que la cuenta realmente necesita hoy.
2. **[H]** Ninguna prueba del laboratorio tiene la etiqueta "ventaja demostrada" (`laboratorio/tabla-maestra.md`): 0 de 12. Nada de lo que hoy mueve el rendimiento requiere ETFs de momentum internacional, UCITS ni opciones.
3. **[C] Escenario medio (48 operaciones/año, orden de 5,000 MXN), costo anual (12 meses) que sale de la cuenta (TWR):** GBM **1,104 MXN (5.52%)**; Actinver Trade **1,046 MXN (5.23%,** solo el primer año**)**; Kuspit optimista **888 MXN (4.44%,** sin verificar**)**; Kuspit prudente **1,194 MXN (5.97%,** peor caso**)**; Finamex **2,236 MXN (11.18%)**; IBKR Tiered **399 MXN (1.99%)**; Firstrade **244 MXN (1.22%,** solo entrada, sin retiro**)**.
4. **[H/I]** IBKR es, con mucho, el más barato para el TWR (rompe el empate con GBM desde solo ~3 operaciones/año), pero solo tiene el 10% del art. 129 garantizado en **acciones individuales listadas en el SIC**; en **ETFs** (justo lo que usa el perfil `arena_agresivo`: apalancados y de momentum) el régimen fiscal fuera de México es un hueco no resuelto por el SAT (B4 §1.3).
5. **[R] Condición exacta que cambiaría la recomendación:** si se confirma por escrito (SAT, criterio adicional, o dictamen de un contador con respaldo legal) que los ETFs listados en el SIC tributan al 10% definitivo del art. 129 al venderse fuera de México igual que las acciones, **o** si la estrategia se restringe a acciones individuales listadas en el SIC, cambiar a **IBKR Pro Tiered, cuenta de margen**: ya gana en TWR desde ~3 operaciones al año y ahorra ~700 MXN (~3.5 puntos de TWR) en el escenario medio a 12 meses.
6. **[H]** La fiscalidad no decide el marcador: el ISR se paga en la declaración anual, fuera de la cuenta, en las dos rutas. Lo que sí entra a la cuenta es la retención automática de GBM sobre dividendos (37% sin W-8BEN, 19% con) contra el pago mensual manual del dueño con un extranjero (10% de EUA + 10% de México).
7. **[R] Nota de comparabilidad:** si en el futuro la cuenta se muda de bróker mientras las demás IAs siguen en GBM, el marcador debe reportar dos cifras: el TWR neto real del bróker nuevo y el TWR que habría dado con los costos de GBM (0.29%/lado + IVA + la desviación del SIC), como ya piden B2 §6.3 y B3 §11.
8. **[H]** Los 25 tests de `herramientas/tests/test_costos_broker.py` pasan (`python3 -m unittest herramientas.tests.test_costos_broker`), y las cifras de este documento salen de correr la misma herramienta, no de un cálculo aparte.

---

## 1. Verificación de la herramienta (paso 1 de la tarea)

**[H] Corrida de los tests** (2026-09-25, desde `/home/user/New1`):

```
$ python3 -m unittest herramientas.tests.test_costos_broker
----------------------------------------------------------------------
Ran 25 tests in 0.010s

OK
```

Los 25 casos pasan, incluidos los que contrastan la herramienta contra las cifras de B2 §3 (GBM, Actinver, Kuspit y Finamex a R = 6 idas y vueltas) y de B3 §3.2 (costo por lado de IBKR Tiered y Fixed).

**[H] Qué calcula `costo_total()` (ver el docstring del módulo y `herramientas/costos_broker.py`):**
- **`torneo`** (MXN y `torneo_pct` = fracción del capital): lo que sale de la cuenta y mueve el TWR — comisión + IVA + cuotas de terceros y regulatorias + desviación cambiaria del SIC (ruta "sic") o conversión de entrada (ruta "extranjero") + fondeo + cuotas fijas + W-8BEN + retención de dividendos dentro de la cuenta + arrastre por liquidación − rendimiento del efectivo ocioso.
- **`dueno`** (MXN y `dueno_pct`): `torneo` + salida (conversión final, retiro, recepción del banco) + impuesto de dividendos pagado por fuera + diferencial de ISR sobre ganancias realizadas + costo de cumplimiento (contador).
- Para el **capital de 20,000 MXN**, **rotación** expresada en operaciones/año (`operaciones_anuales`), y **orden mínima de 5,000 MXN** (`orden_promedio_mxn`), la herramienta ya trae estos valores como valores por defecto de la clase `Uso`, que coinciden con los de la tarea.

**[H] Verificación contra el límite de la arena.** Con orden de 5,000 MXN y 8 operaciones/mes (el tope duro de `operaciones_max_mes`), la rotación mensual de un lado es `(8×5,000×0.5)/20,000 = 1.0`, dentro del límite `rotacion_max_mensual_x_capital = 1.5` del perfil `arena_agresivo`. 96 operaciones/año es, por tanto, el techo real de la cuenta, y es el escenario "alta" de la tarea.

---

## 2. Tabla de costo anual por bróker, 3 escenarios de rotación, 2 horizontes (paso 2)

**[C] Supuestos de la corrida** (los de la tarea + los de B1-B4, mostrados para que se pueda repetir):
- Capital 20,000 MXN, orden promedio 5,000 MXN (orden mínima de la arena).
- Tipo de cambio 17.70 MXN/USD (Wise, API pública, 25-sep-2026 06:15 UTC; B1 [21], B4 [36]).
- Desviación implícita del SIC: 0.17%/lado (mediana entre 0.23% y 0.27% aprox. medidos por B1 en SPMO y MTUM, tomando ~0.17 como valor conservador del rango 0.1%-0.25% que cita B1 §9; el propio B1 corrigió esta cifra hacia una mediana de ~0.25%, así que 0.17% es el extremo **optimista** del rango — ver nota de sensibilidad más abajo).
- 1 depósito y 1 retiro en la temporada (para IBKR y Firstrade, ruta "extranjero").
- Ganancia realizada = 0 (no se mete el diferencial de ISR sobre utilidades en esta tabla; se trata aparte en la §4, porque para el TWR del torneo no pesa — B1 §8, B2 §4, B3 resumen 13).
- Comando exacto: `python3 herramientas/costos_broker.py --tc 17.70 --desviacion 0.0017`.

**Comando de reproducción exacta:**
```
cd /home/user/New1
python3 herramientas/costos_broker.py --tc 17.70 --desviacion 0.0017
```

### 2.1 Costo dentro de la cuenta — lo que mueve el TWR del torneo (`torneo`)

| Bróker | Baja, 12 op/año — 6 m | Baja, 12 op/año — 12 m | Media, 48 op/año — 6 m | Media, 48 op/año — 12 m | Alta, 96 op/año — 6 m | Alta, 96 op/año — 12 m |
|---|---|---|---|---|---|---|
| GBM Trading MX/SIC (línea base) | 138 (0.69%) | 276 (1.38%) | 552 (2.76%) | **1,104 (5.52%)** | 1,104 (5.52%) | 2,208 (11.04%) |
| Actinver Trade (con mes gratis, año 1) | 124 (0.62%) | 262 (1.31%) | 494 (2.47%) | **1,046 (5.23%)** | 988 (4.94%) | 2,092 (10.46%) |
| Actinver Trade (sin promoción, año 2+) | 138 (0.69%) | 276 (1.38%) | 552 (2.76%) | 1,104 (5.52%) | 1,104 (5.52%) | 2,208 (11.04%) |
| Kuspit (0.20% sin IVA, sin mantenimiento — optimista, no verificado) | 111 (0.56%) | 222 (1.11%) | 444 (2.22%) | **888 (4.44%)** | 888 (4.44%) | 1,776 (8.88%) |
| Kuspit (0.20% + IVA, mantenimiento 0.99% — peor caso) | 235 (1.18%) | 471 (2.35%) | 597 (2.99%) | **1,194 (5.97%)** | 1,080 (5.40%) | 2,159 (10.80%) |
| Finamex Trading | 902 (4.51%) | 1,805 (9.02%) | 1,118 (5.59%) | **2,236 (11.18%)** | 1,406 (7.03%) | 2,811 (14.06%) |
| Interactive Brokers Pro Tiered | 81 (0.40%) | 126 (0.63%) | 217 (1.09%) | **399 (1.99%)** | 399 (1.99%) | 762 (3.81%) |
| Interactive Brokers Pro Fixed | 148 (0.74%) | 260 (1.30%) | 485 (2.43%) | 936 (4.68%) | 936 (4.68%) | 1,836 (9.18%) |
| Firstrade / Schwab Intl. (solo entrada, sin retiro) | 200 (1.00%) | 206 (1.03%) | 219 (1.10%) | **244 (1.22%)** | 244 (1.22%) | 295 (1.47%) |

### 2.2 Costo para el dueño — incluye salida a pesos y diferencias fiscales (`dueno`)

| Bróker | Baja, 12 op/año — 6 m | Baja, 12 op/año — 12 m | Media, 48 op/año — 6 m | Media, 48 op/año — 12 m | Alta, 96 op/año — 6 m | Alta, 96 op/año — 12 m |
|---|---|---|---|---|---|---|
| GBM Trading MX/SIC | 138 (0.69%) | 276 (1.38%) | 552 (2.76%) | **1,104 (5.52%)** | 1,104 (5.52%) | 2,208 (11.04%) |
| Actinver Trade (con mes gratis) | 124 (0.62%) | 262 (1.31%) | 494 (2.47%) | **1,046 (5.23%)** | 988 (4.94%) | 2,092 (10.46%) |
| Kuspit (optimista) | 111 (0.56%) | 222 (1.11%) | 444 (2.22%) | **888 (4.44%)** | 888 (4.44%) | 1,776 (8.88%) |
| Kuspit (peor caso) | 235 (1.18%) | 471 (2.35%) | 597 (2.99%) | **1,194 (5.97%)** | 1,080 (5.40%) | 2,159 (10.80%) |
| Finamex Trading | 902 (4.51%) | 1,805 (9.02%) | 1,118 (5.59%) | **2,236 (11.18%)** | 1,406 (7.03%) | 2,811 (14.06%) |
| Interactive Brokers Pro Tiered | 116 (0.58%) | 162 (0.81%) | 253 (1.26%) | **434 (2.17%)** | 434 (2.17%) | 798 (3.99%) |
| Interactive Brokers Pro Fixed | 183 (0.92%) | 296 (1.48%) | 521 (2.60%) | 971 (4.85%) | 971 (4.85%) | 1,871 (9.36%) |
| Firstrade / Schwab Intl. (con salida a MXN por Wise) | 871 (4.36%) | 878 (4.39%) | 890 (4.45%) | **915 (4.58%)** | 915 (4.58%) | 966 (4.83%) |

**[C] Lectura de las dos tablas:**
- **Para el TWR (§2.1),** IBKR Tiered es el más barato de los brókers con acceso amplio de instrumentos en todos los escenarios y horizontes. Firstrade/Schwab, si nunca se retira a pesos, es aún más barato, pero solo cubre EUA (sin BMV) y sin acceso a la BMV/SIC.
- **Para el dueño (§2.2),** la salida penaliza mucho a Firstrade/Schwab (retiro fijo de US$25 más la conversión de Wise, ~4.3%-4.6% siempre, casi independiente de la rotación), mientras que a IBKR le pesa poco (~35-40 MXN de salida fija sobre 20,000).
- **Kuspit "optimista" contra "peor caso"** difiere en ~300 MXN al año (1.5 puntos) según si cobra IVA y el mantenimiento del 0.99% anual — B2 marca esto expresamente como **no verificado**, contradicción entre los propios canales oficiales de Kuspit.
- **Sensibilidad de la desviación del SIC (afecta solo a GBM, Actinver, Kuspit y Finamex, que operan vía SIC):** con 0.17%/lado (usado arriba) GBM cuesta 1,104 MXN a 12m/48ops; con la mediana medida por B1 de ~0.25%/lado, sube a **~1,368 MXN (6.84%)**. Esto **agranda** la ventaja de IBKR, porque IBKR no lleva esa desviación (B3 resumen 6).

---

## 3. El "valor del acceso": ¿hace falta hoy? (paso 3)

**[H] Ninguna prueba del laboratorio tiene la etiqueta "ventaja demostrada".** De `laboratorio/tabla-maestra.md` (actualizada el 2026-09-25): de 12 pruebas, **0 tienen "ventaja demostrada"**, 3 son "oportunidad investigable" (R01, V02, AC-03), 5 están "descartada" y 4 siguen "en curso". La tabla lo dice explícitamente: **"Ninguna prueba cumple las cinco condiciones. La única doble implementación con segunda fuente concordante que existe es para factores académicos largo-corto (AC-01 y AC-03), que no se pueden comprar en GBM"** (`laboratorio/tabla-maestra.md`, línea 87).

**[H] V02 (momentum internacional, el caso que más se acerca a "necesitar" acceso extra) da resultado negativo en su versión operable.** Del README de V02:
- El factor académico WML (largo-corto, sin costos, en USD, no comprable en GBM) sí es significativo fuera de EUA — pero eso **no es un instrumento**, es un cálculo académico.
- **"H4 (ETFs). Inconclusa en los 10 pares y en todas las sensibilidades"**: ninguno de los 6 ETFs de momentum probados (EEMO, PIE, IMTM, PIZ, IDMO, IMOM) le ganó de forma significativa a su comparable de mercado (EEM, EFA, VEA), en MXN y neto de costos de GBM. Los dos de mercados emergentes (EEMO, PIE) quedaron **por debajo** de su comparable.
- **"Con el criterio pre-registrado, ninguno de los 6 ETFs de momentum queda verificado como listado en el SIC"** (V02, sección "SIC"). Es decir: ni siquiera se puede comprar en GBM hoy.
- La propia sección "Conclusiones que NO se sostienen" de V02 dice: *"Que exista hoy una forma verificada de capturar momentum emergente desde el SIC. No hay listado verificado, y los dos ETFs que existen le rindieron menos a un inversionista en MXN que EEM."*

**[R] Conclusión de este punto, dicha explícitamente como pide la tarea:** **hoy ninguna ventaja demostrada requiere ETFs de momentum internacional (IMTM, IDMO, EEMO, PIE), UCITS ni opciones.** V02 es la prueba más cercana a necesitarlos y su propio resultado dice que la versión con ETFs reales no tiene ventaja significativa y, además, esos ETFs de momentum ni siquiera están verificados en el SIC (ni en GBM ni, por construcción, hace falta un bróker extranjero para "no tenerlos"). El acceso que dan IBKR, Firstrade o Schwab a ese universo (además de opciones, que tampoco usa ninguna estrategia con etiqueta positiva) **vale como opción a futuro, no como rendimiento probado.** Si en el futuro una prueba nueva obtiene "ventaja demostrada" y esa ventaja depende de un instrumento fuera del catálogo de GBM (por ejemplo, si se repite V02 con un ETF que sí demuestre ventaja, o si se abre una prueba de opciones con ventaja), esa es la señal que reabre la pregunta del bróker.

**[I] Matiz:** el perfil `arena_agresivo` (`config/parametros.json`) sí permite ETFs apalancados (`etf_apalancado_max = 0.5`) y B1 §4.3 confirma que SOXL, TQQQ, SPXL y otros ya están listados en la BMV/SIC. Eso significa que la estrategia agresiva de la arena **ya tiene acceso a los apalancados en GBM**, sin necesitar ningún bróker extranjero. Lo que falta en GBM (IMTM, IDMO, EEMO, PIE, opciones, UCITS confirmados en la app) es justo lo que V02 no demuestra que agregue valor.

---

## 4. Fiscalidad real (paso 4)

**[H] Retención automática contra declaración propia — el contraste central de B1/B2 contra B3/B4:**

| | Casa de bolsa mexicana (GBM, Actinver, Kuspit, Finamex) | Bróker extranjero (IBKR, Firstrade, Schwab) |
|---|---|---|
| ISR sobre ganancias de venta | **10% definitivo, art. 129 LISR.** El intermediario calcula la ganancia/pérdida y entrega constancia. Sin retención en la venta; se paga en la declaración anual | **Igual, 10% definitivo, PERO solo para acciones extranjeras listadas en el SIC** (criterio SAT 37/ISR/N). Sin constancia: el dueño calcula y guarda los estados de cuenta |
| ISR sobre dividendos del extranjero | GBM **retiene** el 10% adicional mexicano y da constancia | **Nadie retiene.** El dueño paga por su cuenta, a más tardar el día 17 del mes siguiente al dividendo (art. 142 fr. V) |
| Retención de EUA sobre dividendos | 30% sin W-8BEN / 10% con W-8BEN (igual en ambas rutas) | Igual |
| W-8BEN | 75 USD + IVA en el SIC de GBM (gratis en Actinver) | Gratis, obligatorio al abrir la cuenta |
| Compensación de pérdidas | Solo contra ganancias del art. 129, en el ejercicio o los 10 siguientes | Igual si el instrumento cae en el art. 129; si no, 3 años (enajenación de bienes) |

**[H] La corrección de B1 sobre el criterio SAT 37/ISR/N (el hallazgo fiscal central de toda la serie).** B1 y B2 habían inferido, en su primera versión, que vender en NYSE o Nasdaq con un bróker extranjero "no parece caber en el art. 129". **Eso era incorrecto y ya está corregido en los cuatro documentos.** El criterio normativo **37/ISR/N** (Anexo 7 de la RMF 2026, DOF 09-01-2026) dice textualmente que las ganancias por vender "acciones emitidas por sociedades extranjeras listadas en el apartado de valores autorizados para cotizar en el Sistema Internacional de Cotizaciones [...] están sujetas a una tasa del 10% en los términos del artículo 129, fracción I de la Ley del ISR, **con independencia de que su enajenación no se realice a través de un intermediario del mercado de valores mexicano**" (B1 §5, B3 §10.2, B4 §1.2, cita cotejada palabra por palabra contra el PDF oficial del SAT). El propio art. 129 LISR prevé el caso: quien opera con "entidades financieras extranjeras" no autorizadas conforme a la LMV calcula su propia ganancia o pérdida y conserva los estados de cuenta.

**Consecuencia práctica:** si la cuenta compra en IBKR (o Firstrade/Schwab) **acciones individuales que están listadas en el SIC** (NVDA, MSFT, AAPL, MA, LLY, AVGO, XOM, AMD, según el catálogo que use la estrategia), el ISR es **exactamente el mismo 10% que en GBM.** IBKR no tiene desventaja fiscal en ese universo, solo carga administrativa (cálculo propio, sin constancia).

**[I] Lo que sigue sin resolver — el hueco de los ETFs (B4 §1.3).** El criterio 37 habla solo de "**acciones**". La fracción II del art. 129 (la que cubre ETFs, "títulos que representen índices accionarios") exige que la venta se haga "en las bolsas de valores" concesionadas conforme a la LMV — es decir, en México. Con un bróker extranjero eso no se cumple literalmente. Hay una opinión profesional (IMCP, *Fisco Actualidades* 122) que sostiene que un ETF constituido como "sociedad" y listado en el SIC caería en la fracción I igual que una acción, pero **no hay criterio ni regla del SAT que lo confirme**, y muchos ETFs de EUA no son "sociedades" en sentido estricto (son *trusts*). Si el ETF **no** cae en el art. 129, pasa al régimen general de enajenación de bienes: tarifa progresiva de hasta 35% (art. 152) y un posible **pago provisional de 20% sobre el monto bruto de cada venta, en 15 días** (art. 126) — un problema de liquidez real para una cuenta de 20,000 MXN que rota 48-96 veces al año, aunque no afecte el TWR del torneo (el ISR no sale de la cuenta durante la temporada).

**[C] Esto es exactamente lo que hace que IBKR no sea una decisión trivial para esta cuenta:** el perfil `arena_agresivo` permite y usa ETFs apalancados (SOXL, TQQQ, SPXL) además de acciones. Esos ETFs, comprados vía IBKR en NYSE/Nasdaq en lugar del SIC, caen en el hueco fiscal no resuelto. Comprados vía GBM/SIC, caen limpiamente en el 10% de la fracción II (B1 confirma que están listados en la BMV).

---

## 5. Recomendación final (paso 5)

### 5.1 La decisión

**[R] Quedarse en GBM para la cuenta de la competencia (20,000 MXN) en esta temporada.**

**Por qué, en orden de peso:**

1. **[H] No hay ninguna ventaja demostrada que GBM no pueda ejecutar hoy** (§3). El universo que la estrategia agresiva ya usa —acciones y ETFs (incluidos apalancados) listados en el SIC/BMV— está disponible en GBM. Lo que un bróker extranjero añade (ETFs de momentum sin listar en el SIC, UCITS, opciones) no tiene, hoy, ninguna prueba con "ventaja demostrada" ni siquiera "confirmada" en su versión operable (V02 es la más cercana y da resultado negativo).
2. **[C] El ahorro de las casas mexicanas alternativas es marginal y parcialmente incierto.** Kuspit "optimista" ahorra ~216 MXN al año (1.08 pp) contra GBM en el escenario medio, pero su tarifa exacta (IVA, mantenimiento, catálogo del SIC, órdenes stop) **no está verificada** — en el peor caso (Kuspit "prudente") **sale más caro que GBM en el escenario alto** (2,159 contra 2,208, casi empatado, y peor en el bajo: 471 contra 276). Actinver Trade solo gana el primer año (mes gratis); desde el segundo año cuesta lo mismo que GBM. Ninguna alternativa mexicana cambia el juego (B2 lo dice explícitamente: "ninguna casa mexicana cambia el juego").
3. **[H/I] IBKR sí gana claramente en costo puro (TWR), pero introduce un riesgo fiscal real sobre justo el tipo de instrumento (ETFs apalancados) que la estrategia agresiva usa** (§4). Ese riesgo no golpea el TWR del torneo (el ISR se paga fuera de la cuenta), pero sí puede golpear la liquidez real del dueño si el SAT exige el pago provisional de 20% en 15 días sobre cada venta de un ETF fuera del SIC — un problema serio para una cuenta que rota 48-96 veces al año.
4. **[I] Simplicidad y comparabilidad.** GBM es el bróker de todas las demás IAs rivales (`config/parametros.json` → `rivales`). Quedarse ahí evita ajustar el marcador y evita la carga operativa de IBKR (W-8BEN, cuenta de margen para no perder por T+1, cálculo fiscal propio, pago mensual del 10% de dividendos, riesgo del numeral 3 del art. 129 sobre ejecución fuera de bolsa — B4 §1.2, no verificado).

### 5.2 La condición exacta que haría cambiar la recomendación

**[R]** Cambiar a **IBKR Pro Tiered, en cuenta de margen** (para no perder ~0.5-0.7 puntos al año por la espera de liquidación T+1 de una cuenta de efectivo — B3 §7), si se cumple **cualquiera** de estas dos condiciones:

- **(a) Fiscal:** se confirma, por escrito y con respaldo (un criterio adicional del SAT, una consulta resuelta, o un dictamen de contador que cite fundamento legal, no solo opinión) que los ETFs listados en el SIC tributan al 10% definitivo del art. 129 al venderse fuera de México, igual que las acciones — cerrando el hueco que hoy deja abierto B4 §1.3. Esto eliminaría el riesgo fiscal sin sacrificar el uso de los ETFs apalancados que el perfil `arena_agresivo` permite.
- **(b) Operativa:** la estrategia se restringe, por decisión propia, a **acciones individuales listadas en el SIC** (sin ETFs vía IBKR; los ETFs se seguirían comprando en GBM/SIC si hace falta usarlos). En ese caso el régimen fiscal ya está resuelto hoy (criterio 37/ISR/N) y la única razón para no cambiar sería la carga operativa.

Con cualquiera de las dos, la ventaja de costo ya es clara y se puede citar con esta misma herramienta: IBKR Tiered rompe el empate con GBM en **~3 operaciones al año** (torneo) y ahorra **~700 MXN (~3.5 puntos de TWR)** frente a GBM en el escenario medio (48 operaciones/año, 12 meses) — ver §2.1.

**[R] Lo que NO cambiaría la recomendación:** un ahorro de ~1 punto porcentual de una casa mexicana (Kuspit o Actinver) no es, por sí solo, motivo para migrar: es menor que el ruido de una sola operación de la estrategia, y ninguna de las dos tiene su catálogo de ETFs apalancados ni sus órdenes stop/OCA verificados (B2 §7), que sí son necesarios para el perfil `arena_agresivo`.

### 5.3 Nota de comparabilidad (obligatoria si la cuenta cambia de bróker en el futuro)

**[R]** Si en cualquier temporada futura esta cuenta se muda de bróker mientras las demás IAs de la competencia se quedan en GBM, el marcador **debe reportar dos cifras, no una**:

1. El **TWR neto real** con los costos del bróker nuevo.
2. El **TWR que habría dado la misma cartera con los costos de GBM** (0.29% por lado con IVA + la desviación cambiaria del SIC medida en B1, ~0.17%-0.25%/lado), para que la comparación contra las IAs que se quedan en GBM no mezcle el efecto de la estrategia con el efecto del bróker.

En la bitácora del torneo, cada operación debe anotar su costo real y el costo equivalente en GBM (B2 §6.3, B3 §11 ya dan el mismo criterio). Con `herramientas/costos_broker.py`, esto se calcula llamando `costo_total()` dos veces por período — una con el `Broker` real y otra con `catalogo()["gbm_sic"]` — y reportando ambos `torneo_pct`.

---

## 6. Fuentes

Todas las cifras y citas de este documento vienen de:
- **B1** (`arena/investigacion/brokers/B1-gbm-linea-base-.md`): línea base de GBM (0.29%/lado con IVA, desviación del SIC, texto del art. 129, criterio 37/ISR/N).
- **B2** (`arena/investigacion/brokers/B2-casas-de-bolsa-y-apps-mexicanas.md`): Actinver Trade, Kuspit, Finamex y el resto de las casas mexicanas; tabla de costo de temporada y puntos de equilibrio.
- **B3** (`arena/investigacion/brokers/B3-interactive-brokers-para-residentes-en-mexico.md`): tarifas de IBKR Pro Tiered/Fixed, conversión de divisas, fondeo/retiro, T+1 en cuenta de efectivo, régimen fiscal corregido.
- **B4** (`arena/investigacion/brokers/B4-fiscalidad-comparada-y-otros-brokers-extranjeros.md`): mapa fiscal completo por instrumento, el hueco de los ETFs, Firstrade/Schwab/tastytrade, fricción de conversión con Wise.
- **`laboratorio/tabla-maestra.md`** y **`laboratorio/replicas/V02-momentum-internacional/README.md`**: estado de las pruebas del laboratorio y resultado de la única prueba con ETFs de momentum internacional.
- **`config/parametros.json`**: límites del perfil `arena_agresivo` (rotación, operaciones/mes, ETFs apalancados).
- **`herramientas/costos_broker.py`** y **`herramientas/tests/test_costos_broker.py`**: cálculo de costos y su verificación, corridos el 2026-09-25 para este documento.

Cada afirmación con **[H]** remite a la sección de B1-B4 citada entre paréntesis; los números con **[C]** salen de la corrida de `costos_broker.py` reproducible con el comando de la §2.
