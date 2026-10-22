# Decisor · corrida vespertina · 2026-10-21 (19:27 CDMX; corrida 01:29 UTC del 22-oct)

**Resultado: nada amerita actuar antes del viernes.** No hay orden nueva (REGLAS §4).

**Revisión:**
- **Alertas Altas del día (`bitacora/alertas.md`):**
  - **Cruce +2% en pesos** de UPRO, QQQM y BTC: es una ganancia, sobre todo por el peso, y ninguna regla se dispara.
  - **Polymarket 4641065 (Irán):** bajó de 0.815 a 0.70. No hay confirmación primaria de un ataque de EUA y no hay regla de cartera atada a ese mercado. Queda informativa.
- **Supervisión (7 corridas):** sin cortacircuitos. Papel 20,830 (DD −0.3%) y real GBM 10,140 (DD 0.0%) en la última. UPRO 152.01 contra un stop de 135.76 (le falta ~10.7%). FX-1 OK todo el día.
- **FX-1, lectura de la noche (`fx_alerta.py`, 01:27 UTC):**
  - **AVISO**, el dólar sube: USD/MXN 18.7045; Δ1 +1.52% (umbral 1.49%) contra 18.4244 del 20-oct; Δ10 +4.06%; σd 0.74%.
  - **Fuente:** cierres diarios de Yahoo `MXN=X` como sustituto del FIX (no hay BANXICO_TOKEN). La referencia es provisional.
  - **Efecto por cada 1% del dólar:** papel ±198 MXN; real ±51; papel-binance ±43; real-binance ±21; total ±312.
  - **Sin acción; va al brief de mañana.** Ayer (20-oct) la lectura fue OK (Δ1 +0.06%), así que no hay dos AVISOS seguidos en la misma dirección.
  - La ALERTA sigue lejos (≥ 19.0473). Lo de Irán puede seguir presionando al peso esta noche.
- **Cripto:** filtro **ENCENDIDO**, colchón +19.47% (00:44 UTC). En contraparte, no hay ROJA ni disparador.
- **Boleta VT:** sigue EN ESPERA hasta que el dueño confirme por escrito. Nadie asume un llenado.
- **Laboratorio:** R18 ya tiene su adenda con el perfil `arena_agresivo`. P(−12%) es ~21%, no 48% (`79543d5`). El comité lee la adenda.

**Para el comité del 23-oct:** sin cambios a la lista mínima de `bitacora/decisiones-pendientes.md` (puntos a-g, con R18 corregido).
