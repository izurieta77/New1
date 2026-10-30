# Decisor · corrida vespertina · 2026-10-29, jueves (19:27 CDMX; corrida 01:29 UTC del 30-oct)

**Resultado: una alerta de contraparte amerita preparar la respuesta antes del viernes, pero no ejecutarla todavía.** Para GBM no hay nada que actuar: no hay órdenes, ni cortacircuitos, y FX-1 está OK.

## Binance: hackeo y retiros pausados (alerta Alta del 30-oct 00:50 UTC)
- **Hecho (B, varias fuentes independientes):** Binance pausó retiros desde ≈21:50 UTC del 29-oct por un posible hackeo de US$5.3-5.8 mil M, más que el SAFU (~US$1.16 mil M). Señales **A2 y A11 en ROJA**. BTC 77,016 (−5.1% en 24 h). El libro BTC/MXN funciona (E9 0.105%, VERDE).
- **Las tres reglas escritas no coinciden:**
  1. `conocimiento/cripto/lista-senales-de-alerta.md` §3: "una ROJA activa la contingencia" (vender a MXN y retirar por SPEI; si falla, mover el BTC a Bitso);
  2. `config/parametros.json` → `contingencia_contraparte.disparadores_roja`: "retiros en MXN o BTC suspendidos **más de 24 h**". **Vence ≈21:50 UTC del 30-oct; hoy van ~3.5 h**;
  3. `bitacora/decisiones/2026-09-25-CRIPTO-inicial.md`: "SPEI caído más de 48 h, o aviso o acción de autoridad".
- **Qué decidí y por qué:**
  - Con los retiros pausados, **vender BTC a MXN dentro de Binance no saca el dinero del riesgo de contraparte**: solo cambia BTC por pesos en la misma plataforma, a un precio deprimido por el pánico. La protección real es **retirar**, y eso solo lo puede hacer el dueño cuando reabran.
  - Rige la regla más específica y con fecha (parámetros, 24 h). Mientras tanto se deja **armada** la respuesta, para no tener que improvisarla.
- **Papel (`papel-binance`):** orden **O0007 CONDICIONAL** en `bitacora/ordenes-pendientes.csv`.
  - Vender las 0.002698 BTC solo si a las **21:50 UTC del 30-oct** los retiros siguen suspendidos (fuente A o B fechada).
  - Si reabrieron, se anula. La ejecuta la rutina cripto.
- **Real (cuenta compartida; requiere confirmación del dueño): boleta de contingencia, sin cambio contra la recomendación de la alerta.**
  1. **Revisa ya en la app** si están abiertos los retiros de MXN (SPEI) y de BTC.
  2. **Si el SPEI está abierto:** retira los ~3,002 MXN de efectivo.
  3. **Si el retiro de BTC está abierto:** manda los 0.001325 BTC por Lightning u on-chain a Bitso (o a Mercado Pago si Bitso no está lista). **No vendas en Binance** si puedes retirar el BTC.
  4. **Si todo sigue pausado a las 21:50 UTC del 30-oct:** contingencia ROJA completa en cuanto reabra (vender a MXN con límite y SPEI, en paralelo Lightning).
  5. **No cambies contraseñas** ese día: Bitso bloquea retiros 24 h después de un cambio.
- **Pendiente para el gestor de riesgo y el comité W44 (hoy viernes):** unificar las tres reglas en una sola. La de `lista-senales` §3 contradice a los parámetros.

## Resto de la revisión
- **Alertas Altas:** además de la de Binance, una de UPRO (−2% en pesos en el post-mercado del 29-oct, ya revertida). La multa SGM sigue Abierta: **hoy, viernes 30-oct, es el último día seguro para la ficha 9/LIF**.
- **Supervisión (último corte del 29-oct):** sin cortacircuitos. Papel con DD de −0.8%; real GBM en su máximo.
- **FX-1, lectura de la noche (`fx_alerta.py`, 01:28 UTC):** **OK**. USD/MXN 18.8720; Δ1 +1.29%; Δ10 +2.21%. Va al brief como dato: el dólar sube dos días seguidos.
- **Cripto:** el filtro sigue **ENCENDIDO** (cierre del 29-oct en 77,991.89 contra una salida de 70,952.67, +9.9%). La caída por el hackeo no dispara el filtro.
