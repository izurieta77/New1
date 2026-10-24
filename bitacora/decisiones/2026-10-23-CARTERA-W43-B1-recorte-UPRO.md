# Decisión de cartera · comité semanal W43 · viernes 23-oct-2026

> Skill `comite-de-inversion`. El orquestador preside con el rol de `decisor`. Pasaron 5 días hábiles desde la decisión W42 del 16-oct (REGLAS §4). Fase 0, con la excepción de la cuenta arena. El expediente con la tesis y el contexto está en `bitacora/comite/2026-10-23-expediente.md` (commit `98b707a`).

## Decisión
1. **Papel GBM: B1, vender 1 de los 2 UPRO.**
   - Orden **O0006** en `bitacora/ordenes-pendientes.csv`: lunes 26-oct, vela de 14:45 UTC, 1 título fijo. Se anula si antes saltan el stop o el filtro.
   - El UPRO restante conserva el stop de **135.76 USD** y el filtro. El efectivo resultante (~3,750 MXN, 18.6%) **no se reasigna**.
2. **Real GBM: A-real. No se emite ninguna boleta.**
   - Antes de la siguiente, el dueño debe confirmar tres cosas: (a) el efectivo disponible en GBM; (b) los movimientos desde el 7-oct; (c) si la orden VT del 19-oct se llenó.
   - Cuando estén confirmadas, el comité del 30-oct evalúa B2' con un índice 1x que no duplique SPYM: **VEA** (cuantitativo) o **IVOO** (macro), con RSP como alterna, y una `validar_orden` nueva.
   - **Advertencia que sigue vigente:** "si ya tienes 1 VT del 19-oct, no captures otra".
3. **Real Binance: A, mantener.** BTC se queda en 40%. B3 se rechaza por su propia regla: el cierre de 81,294 está debajo de 87,396.
4. **C (rotar): rechazada.** Rotar por una pérdida de −0.56% en el SIC es sobreoperar sin una tesis que se pueda refutar.

## Respuesta al dueño ("¿qué vendemos y a dónde movemos todo?")
- **Del libro de Claude no se vende nada en tu cuenta real**, que va en verde: +0.44% en GBM y +0.21% en Binance. Solo se recorta un UPRO del papel, para bajar el riesgo de cola (lo que mide R18).
- **Opinión, no orden:** la pérdida de −128.80 MXN del 22-oct viene de NVDA (ChatGPT, −286) y de UBER (sin atribuir, −120). Vender todo hoy daría un resultado fiscal de −262 MXN, sin ISR, así que vender no ahorra impuestos. Y le pagas ~0.58% de comisión de ida y vuelta a un día de −1.2% del S&P.
- **Antes de mover nada:** confirma el efectivo disponible y si VT se ejecutó. Faltan ≈3,150 MXN por conciliar en la cuenta compartida.

## Tesis y cómo se refuta
- **Tesis de B1:** con el UPRO al 26.6%, P(tocar −12% en 63 días) ≈ 21%; con 13.3%, ≈ 16.4% (R18 + adenda; A y B concuerdan).
  - El stop está a 6.1%, y R16 dice que el stop no protege. **El tamaño es la palanca**: R16-R18 lo muestran y el abogado del diablo lo nota.
  - El costo es una comisión de 7.79 MXN.
- **Refutación al 20-nov:** que el papel con un UPRO rinda menos que el contrafactual con dos (`competencia/marcador.md`, reconstruible) **y** que no haya tocado −12%. Va con el pronóstico **P0173**.
- **Disenso (cuantitativo, se conserva):**
  - A en papel: B1 cambia el Sharpe en ≈0 y su edge neto no se distingue de cero (±1 pp al año).
  - Cambiaría a B1 si el ^GSPC cierra bajo su SMA200 (7,291) o si el VIX pasa de 22 con UPRO < 140.

## Dictámenes (3 líneas cada uno)
- **Macro (62): B1 / A-real / A.**
  - Régimen mixto. El petróleo (~110) y la tasa real en el percentil 99 golpean la duración larga: IA y chips, que el UPRO triplica.
  - P(S&P toca −2% en 5 sesiones) ≈ 40%. El peso débil amortigua en MXN.
  - Si se confirma el efectivo: IVOO.
- **Cuantitativo (60): A / A-real / A.**
  - El filtro es in-sample y salió de minería de variantes. R16-R18 son "No replicado" y R19 "Replicado": son calibración, no alfa.
  - B1 baja P(−12%) 4.6 pp con ΔSharpe ≈ 0.
  - Candidatos de B2': VEA (correlación con SPYM de 0.80, 12-1 +20.1%) y RSP (0.68). VT duplica (0.96).
- **Geopolítico (60): B1 / A-real / A.**
  - Polymarket 4641065 cerró en **0.725** a las 21:13 UTC, debajo de 0.735, tras la respuesta "Absolutely" del embajador Barrack sobre un ataque en fin de semana (B).
  - Estima P(ataque antes del 31-oct) en ≈ 0.30. Un hueco de apertura el lunes puede ejecutar el stop por debajo de 135.76.
  - Se registró **P0174** (el alto el fuego dura hasta el 31-oct; p 0.70).
- **Cripto (85 en Binance; 60 en papel): A / B1 / A-real.**
  - B3 no cumple: el cierre está 7.5% debajo de 87,396.
  - Flujos de ETF de −635.5 M el 22-oct (B). E9 en ÁMBAR.
  - Con BTC en la salida del filtro, la cuenta pierde ≈ −5.2%.
- **Abogado del diablo:**

  | Opción | Veredicto | Confianza |
  |---|---|---|
  | A-papel | Sobrevive con condiciones | 50 |
  | **B1** | **Sobrevive** | **65** |
  | B2' | No sobrevive hoy | 85 |
  | A-real | Sobrevive | 85 |
  | B3 | No sobrevive | 95 |
  | A-Binance | Sobrevive | 75 |
  | C | No sobrevive | 90 |

  - Sesgos señalados: anclaje y statu quo, y confirmación (citar R18 sin tocar el tamaño).
  - Un Brier de 0.1979 con n = 74 no prueba habilidad: harían falta ~348.

## Votos y confianzas
| Agente | Papel | Real GBM | Binance | Confianza |
|---|---|---|---|---|
| analista-macro | **B1** | A-real | A | 62 / 80 / 85 |
| analista-cuantitativo | A | A-real | A | 60 / 85 / 85 |
| analista-geopolitico | **B1** | A-real | A | 60 / 85 / 90 |
| abogado-del-diablo | **B1** | A-real | A | 60 / 80 / 80 |
| analista-cripto (extra; no vota en papel, como en la W42) | (B1) | (A-real) | A | 60 / 80 / 85 |
| gestor-de-riesgo | APRUEBA B1 | APRUEBA A-real | APRUEBA A | sin veto |

- **Papel:** 3 a 1 por B1; la confianza media de los que votaron B1 es 60.7 (mínimo 55). El abogado dice que B1 "sobrevive". **Aprobada.**
- **Real GBM y Binance:** unánimes.

## Gestor de riesgo (resumen)
- **B1:**
  - Venta de 1 UPRO = 144.04 × 18.6480 = **2,686.06 MXN**; comisión 7.79.
  - Pesos después de la venta: UPRO 13.3% (máximo 50%), SPYM 41.3% y QQQM 26.8% (máximo 60%), efectivo 18.6% (el perfil no fija tope).
  - `validar_orden` sin violaciones. 3.ª operación de octubre (máximo 8); rotación 0.57x (máximo 1.5x); orden ≥ 2,500.
- **Stop:** se queda en 135.76. La pérdida con stop baja de 309 MXN (1.5%) a **154 MXN** (0.77%; 162 con comisión).
- **Cola:**

  | Escenario | Con 2 UPRO | Con 1 UPRO (B1) |
  |---|---|---|
  | Un día tipo 16-mar-2020 | −17.7% (DD ≈ −21%, cruza −20%) | **−13%** (DD ≈ −16%; cruza −12%, no −20%) |
  | Una semana tipo abril de 2025 | −15.5% | −11.3% |

- **Reasignar el efectivo** cabe hasta 2 SPYM (57.8%), pero no se recomienda: devuelve la beta que B1 quita.
- **Discrepancia anotada:** `rutinas/REGLAS-MOTOR.md` §4 dice tope de 10,000 MXN y `config/parametros.json` dice 5,000 (el que usa `riesgo.py`). Va a decisiones-pendientes; no se cambió nada.

## Verificación (orquestador, 23-oct ~22:55 UTC, antes del commit)
- **Venta:** 1 UPRO = 144.04 × 18.6480 = 2,686.06 MXN; comisión 0.29% = 7.79.
- **Pesos después de la venta**, sobre 20,185.64: UPRO 13.31%, SPYM 41.32%, QQQM 26.80%, efectivo 18.58%.
- **Pérdida con stop de 1 UPRO:** (144.04 − 135.76) × 18.6480 = 154.41 MXN.
- **Precios:** Yahoo chart v8, cierre del 23-oct, el mismo de `portafolio.py valuar` del cierre.

## Pronósticos registrados
- **P0173:** índice del papel ≥ 100.967150 al 20-nov; p 0.52 (claude).
- **P0174:** Polymarket 4641065 resuelve SÍ; p 0.70 (geopolítico).
- **Vigentes:** P0127 (UPRO > 135.76 el 30-oct, p 0.82) y P0164 (BTC ≥ 85,000 el 5-nov, p 0.24).

## Nota 2026-10-23 23:1x UTC (auditoría semanal W43, `bitacora/semanal/2026-W43-abogado.md`)
- **La dirección de B1 se refuerza; la cifra que la sostenía no era la correcta.**
  - Contra el máximo histórico de la cuenta, que es como mide el cortacircuitos, P(−12%) ≈ 25% a 63 días con 26.9% contra ≈ 17% con 13.5%, y ≈ 45% contra ≈ 30% a 126 días. B1 quita **8-15 pp**, no 4.6.
  - **B1 no protege la cola profunda:** −20% en 12 meses ≈ 25-27% con cualquier peso, y un día tipo 1987 ≈ −24%.
- El argumento fiscal de la respuesta al dueño ("vender no paga ISR") sigue en pie para hoy. El costo fiscal de largo plazo de la mezcla está subestimado en R19 (~1.0-1.2 pp por año).
- **El Brier de 0.1979 no prueba habilidad** ni se distingue de 0.20.

## Correcciones de la revisión del 23-oct
[Nota del orquestador, 24-oct-2026 01:1x UTC (trabajo continuo), por la revisión del 23-oct §1.1-§1.7, `bitacora/revisiones/2026-10-23.md`]
- **§1.1 VT:** el registro vigente es el del fallo 2026-10-22 §3: **0 VT en la cuenta, cosa conocida por las capturas del 22-oct; boleta CADUCADA desde el 23-oct, sin ejecución registrada.**
  - En esta decisión, "estado desconocido" y "advertencia que sigue vigente" (L10-L12) no aplican.
  - El punto (c) de la petición al dueño se reemplaza por la fórmula del fallo §3.4: "si ves VT en tu portafolio, no captures: repórtalo".
- **§1.2 Expediente incompleto:** lo que faltaba está en la adenda de `bitacora/comite/2026-10-23-expediente.md`. **Ratificación (fallo §4 k):** para el **libro de Claude**, el comité ratifica la opción **(A) mantener** de las respuestas al dueño del 22-oct. Las opciones (B) recortar NVDA y UBER y (C) todo a CETES son de posiciones ajenas o de toda la cuenta: quedan como opinión, no como decisión.
- **§1.3 / §1.5 Efectivo:** donde dice "sin confirmar desde el 22-oct" y "+0.44% en GBM", la redacción única es: **"efectivo 5,040.16 registrado; última confirmación del dueño el 7-oct; en duda desde la captura del 22-oct (la cuenta compartida no cuadra)"**. El +0.44% se calcula con ese efectivo registrado.
- **§1.4 Refutación verificable:** se registró **P0175** antes de ejecutar O0006. Pregunta: ¿al 20-nov el índice real queda debajo del contrafactual con 2 UPRO **y** no tocó −12% contra su máximo histórico? p 0.45. La fórmula del contrafactual está escrita en el criterio. P0173 queda solo como pronóstico de dirección.
- **§1.6 Alcance del −262 MXN:** son las **seis emisoras de la cuenta compartida que se veían en la captura**, no el libro de Claude ni el ejercicio completo. Si hubo otras enajenaciones en 2026 (AMKR, quizá VISTA o GFNORTE), la constancia cambia. La conclusión, que vender no ahorra ISR, se sostiene.
- **§1.7 Horas (reincidente):** las horas de este archivo se corrigen con `git log`:
  - la decisión entró en `22e1b07` a las **22:54:30 UTC**;
  - la verificación de la L91 fue anterior a ese commit;
  - la "Nota 23:1x UTC" entró en `85c5670` a las **22:56:38 UTC**.
  - **Regla:** la hora de una nota se toma de `date -u` al escribirla, y ninguna nota dice una hora posterior a su commit.
