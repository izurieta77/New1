# Decisor, corrida vespertina · sábado 17-oct-2026 (19:27 CDMX; corrida 2026-10-18 01:28 UTC)

**Resultado: nada amerita actuar antes del viernes. Sin orden, sin boleta nueva, sin rebalanceo** (REGLAS §4).

Revisé:
- **`bitacora/alertas.md`:** sin filas nuevas del 17-oct.
- **Supervisión:** no hay archivo del día (sábado, NYSE y BMV cerradas; no es falla). Último estado conocido del UPRO de papel: 146.43 contra un stop de 135.76 (colchón 7.29%). Sin cortacircuitos.
- **FX-1, lectura de la noche (`fx_alerta.py`, solo lectura):** **OK**, sin AVISO ni ALERTA. USD/MXN 18.4790 (Yahoo MXN=X, fijo desde el viernes 21:00 UTC); Δ1 +0.49%, Δ10 +2.31%, σd 0.75%. ALERTA si llega a ≥ 19.0473 o ≥ 19.3505 (Δ10). Efecto por cada 1% del dólar: papel ±191 MXN, real ±50 MXN, papel-binance ±41 MXN.
- **Cripto (`bitacora/cripto/2026-10-17.md`):** filtro de `cripto_binance` **ENCENDIDO**. Recálculo de las 18:42: SMA200 72,464.47, salida 70,290.54; BTC ~81,469, colchón ~+15.9%. Sin cruces.
- **Inteligencia (`bitacora/inteligencia/2026-10-17.md`):** urgencia alta, ninguna. Hay tres temas a vigilar en la reapertura:
  - HR Ratings bajó a México a BBB (15-oct);
  - la crisis política y de deuda en Francia;
  - un récord de ataques en Ormuz (presión al alza del crudo el domingo).
  Ninguno tiene un disparador cumplido.
- **Laboratorio de hoy:** R12 (trabajo continuo) quedó en **"No replicado"**, así que la condición VIX ≥ 25 del filtro del UPRO se queda. No cambia nada de la cartera; es insumo del comité del 23-oct.

**Pendiente que sigue en pie:** boleta VT del lunes 19-oct. La captura el dueño solo si el semáforo de la supervisión de las 08:40 la da por VIGENTE.
