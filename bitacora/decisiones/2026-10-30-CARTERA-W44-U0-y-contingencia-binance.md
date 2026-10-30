# Comité semanal de cartera W44 · viernes 30-oct-2026 · U0 (vender el último UPRO) y contingencia Binance unificada

> Preside: decisor (rol aplicado por el orquestador). Expediente: `bitacora/comite/2026-10-30-expediente.md`. Fase 0: el papel decide; lo real solo se propone al dueño. Última decisión de cartera: W43 (23-oct), 5 días hábiles → toca comité.

## Tesis aprobada y cómo se refuta
- **Papel GBM: U0.** Vender 1 UPRO (13.2% del libro) el lunes 2-nov a las 14:45 UTC (O0008). El efectivo (~32%) no se reasigna. No se vuelve a entrar al UPRO sin un **R23 pre-registrado** (U0 contra U13.5, μ de 5/7/9/11%, r 3.8%, fuera de muestra 2009-2026 con UPRO real).
  - **Por qué:** R20 deja al 3x sin ventaja de acarreo con tasas ≥3% (empate con μ ≈ 11.2%); R21 no compara contra U0 (su +0.73 pp es exploratorio, dentro de muestra, t ≈ 1). El stop está a 4.0% y P(tocarlo en 10 sesiones) ≈ 45-50% (cuant; abogado 46% a 5 sesiones), con la elección del 3-nov y riesgo de ataque a Irán después (12%) abriendo con hueco. En la cola de 2020, A cae −12.8% (cruza el cortacircuitos de −12%); U0, −8.2% (gestor).
  - **Refutación:** P0208 (UPRO cierra el 20-nov < 141.21; p 0.52). Si UPRO sube y R23 muestra que U13.5 supera a U0 en ≥0.3 pp de CAGR con μ = 7% sin sumar más de 3 pp a P(−12%), la decisión se revierte.
- **Binance (papel y real): anular O0007; regla única "retirar, no vender".** Con todos los rieles cerrados (endpoint A 22:50 UTC: 0/990 retiros; BTC, USDT y MXN/SPEI cerrados), vender BTC a MXN dentro de Binance cambia un derecho por otro frente al mismo deudor: no reduce contraparte. La exposición de mercado sigue bajo el filtro SMA200 (BTC 76,968 vs salida 70,952.67, encendido), stops y topes.
- **Real GBM: A-real** sin boleta (efectivo y atribución sin confirmar por el dueño).

## Dictámenes (3 líneas cada uno)
- **Macro (U0, 63):** PCE subyacente sep 3.1% a/a, general 3.65%; 10a 4.93% y tasa real en p98 a 5 años: prima acciones-CETES casi nula en corto plazo. Con σ ≈ 19% el umbral 3x/1x sube a ≈12.5-13%. VE 1 semana: U0 +0.02 pp, R1x −0.15, A −0.18. Binance: anular O0007 (70); A-real (85).
- **Cuantitativo (R1x' = vender UPRO y comprar 2 SPYM, 55):** la diferencia entre las tres es ruido; decisión de riesgo, no de edge. Corrige el expediente: la regla del torneo NO se activa (pide ≥5 pp; vamos +1.46 pp sobre Grok) y 3 SPYM violan `etf_indice_max` (66.3%). U0 aceptable; en contra de A.
- **Geopolítico (U0, 65):** elecciones ya en el precio (Cámara D 93.5%); riesgo asimétrico es Irán después del 3-nov (12% de ataque 4-6 nov); Banxico mantiene 85%. Binance: ~50% de reapertura al 6-nov contra 0.75 de P0204. R1x segunda opción (55); A en contra (30).
- **Abogado del diablo (U0; "B1 no se sostiene" como razón para seguir con UPRO):** R20/R21 solo prueban que la brecha no cambia colas, no que el 3x aporte; con μ de Vanguard (~4-5%) el 3x pierde. Binance: "precio de pánico" era falso (E9 VERDE); la razón válida es contraparte. Pide R23 y contingencia por estado del riel (`bitacora/semanal/2026-W44-abogado.md`).
- **Analista cripto (Binance A → C, 80):** sin descuento contra el mercado externo; reloj de 24 h se cumple entre 00:04 y 02:10 UTC del 31-oct. Propone la regla única (abajo). Confirmar Bitso nivel ≥2 con CLABE; no cambiar contraseñas el día de la reapertura; cuidado con phishing.
- **Gestor de riesgo (U0 a favor; R1x' condicionada a exactamente 2 SPYM; A abstención; sin violaciones vigentes):** bruto por suma de valores 0.81x con A (el 107.6% de delta es informativo, no límite; falta escribir la definición en parámetros). Operaciones: U0 = 1/8 en noviembre, rotación 0.13x. Binance: cortacircuitos lejos (−3.8% vs −20%); aprueba anular O0007 con condiciones.
- **Verificador** (cifras clave): hackeo oficial ≈ US$6.3 mil M (Security Incident Update #2, 19:33 UTC, A); guía oficial de reapertura ≈34 h por fases (≈05:30 UTC del 1-nov); prueba de reservas inicial el 2-nov.

## Votos y regla de decisión
| Agente | Voto | Confianza |
|---|---|---|
| Macro | U0 | 63 |
| Geopolítico | U0 | 65 |
| Abogado del diablo | U0 | — (veredicto: A no sobrevive) |
| Cuantitativo | R1x' (también vende el UPRO) | 55 |
| Gestor de riesgo | U0 preferida; sin veto | — |

Vender el UPRO: 4 de 4. U0 frente a R1x': 3 a 1, confianza media 61 (≥55) → **aprobada**. El gestor no veta.

## Disenso (se conserva)
- **Cuantitativo:** prefiere conservar beta con 2 SPYM (beta ≈0.87 contra 0.71 de U0); pierde 0.2-0.55 pp/año menos que U0 si μ es alto. Cambiaría a U0 si la ventaja sobre el mejor rival llega a ≥5 pp o si el VIX cierra ≥22.
- **Geopolítico:** O0007 se podía ratificar como reducción de varianza (modo torneo) etiquetándola así; no prevaleció porque el papel debe sombrear al real.
- **Macro:** U0 pierde la cobertura cambiaria de ese 13.2%.

## Tamaño, stop y salida
- O0008: 1 UPRO, ≈2,647 MXN, comisión ≈7.7 MXN, realiza ≈ −122 a −130 MXN (sin ISR). Efectivo ≈ 6,438 MXN (32%). SPYM queda en ≈41.5% y QQQM en ≈26.5%: sin stop por línea (enmienda del 25-sep); cortacircuitos del perfil `arena_agresivo` vigentes.
- Si el stop o el filtro se activan antes del lunes, la venta la manda esa regla y O0008 queda absorbida.

## Regla única de contingencia de contraparte (propuesta; el texto de `config/parametros.json` lo ratifica el dueño)
1. **Fuente única:** `config/parametros.json` (`cripto_binance.contingencia_contraparte`). `lista-senales-de-alerta.md` §3 y la decisión del 25-sep la citan.
2. **Disparo:** cualquier ROJA (E1-E10 o `disparadores_roja`). El de "retiros MXN o BTC suspendidos > 24 h" corre desde la primera evidencia **A** fechada (endpoint) de BTC o MXN cerrados, no desde pausas parciales.
3. **Al activarse:** cero depósitos, alerta alta, boleta urgente al dueño, verificar el plan B (Bitso) y lectura del catálogo del CMS de Binance cada corrida (lección del verificador W44).
4. **Respuesta por riel:** abre BTC → retirar en especie a Bitso en la primera hora; abre solo SPEI → vender con límite y retirar en el acto; abren ambos → retirar ambos; todo cerrado → no convertir por contraparte.
5. **Mercado:** el filtro SMA200, los stops y los topes siguen mandando y pueden ordenar una venta interna por su cuenta.
6. **Papel:** registra el retiro como transferencia a un sublibro Bitso al precio del minuto, menos comisiones de red.
7. **Salida:** saldo fuera, o prueba de reservas nueva + 7 días sin corrida (E1 > −2.1%). Volver a Binance lo decide el dueño. Si al 7-nov sigue todo cerrado: escalar (respaldo de saldos, ticket) y revisar solvencia contra E1 y P0207.

## Boleta real (solo propuesta al dueño)
`bitacora/boletas/2026-10-30.md`: Binance real, retirar al reabrir (no vender); GBM real sin boleta.

## Pronósticos registrados
- P0208: UPRO cierra el 20-nov < 141.21 (0.52).
- P0209: EUA impacta territorio iraní entre el 4 y el 6-nov (0.12).
- P0210: Banxico mantiene el 5-nov (0.85; mercado 0.815-0.835).
- Ya vigentes: P0204 (Binance reabre BTC el 6-nov, 0.75), P0206 (UPRO toca el stop al 13-nov, 0.35), P0207 (E1).
