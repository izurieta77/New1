COMITÉ SEMANAL DE CARTERA · viernes 30-oct-2026 (W44). Repo /home/user/New1 (rama claude/investment-strategy-routines-19ep76). Fase 0, con la excepción de la cuenta arena (config/parametros.json). Decisiones vigentes: bitacora/decisiones/2026-10-02-CARTERA-W40-modo-C-moderado.md, 2026-10-16-CARTERA-*, 2026-10-23-CARTERA-W43-B1-recorte-UPRO.md (O0006 ejecutada el 26-oct a 147.28). Última decisión de cartera: 23-oct (5 días hábiles) → toca comité.

TESIS A EVALUAR (statu quo): "Mantener sin cambios la cartera de papel GBM y la real hasta el comité del 6-nov".

1. **Papel GBM** (cierre 30-oct, `bitacora/equity.csv`):
   - 20,111.52 MXN, índice 100.56; DD −3.69% desde el pico (nuevo máximo de DD; pico 103.48 el 29-oct… y 9-oct). TWR +0.56% desde el 28-sep contra benchmark 50% S&P TR MXN + 50% CETES +2.13%, S&P TR MXN +3.68% (USD −2.04%), IPC +7.37%, CETES +0.57%. Semana −0.41%.
   - Posiciones: 5 SPYM (41.5%), 1 QQQM (26.5%), 1 UPRO (13.2%) y 3,799.05 de efectivo (18.9%). USD/MXN 18.7435.
   - **UPRO 141.21, 4.0% sobre el stop de 135.76.** Filtro: ^GSPC 7,580.07 contra salida 7,090.46 (SMA200 7,309.76 × 0.97), colchón 6.9%; VIX 19.42 < 25.
   - Perfil `arena_agresivo`: siguiente cortacircuitos −12%, a ~8.3 pp.
2. **Real GBM** (`bitacora/real/equity.csv`): 10,041.86 MXN (índice 100.42; DD −1.17%): 3 SPYM + efectivo registrado 5,040.16 **sin confirmar desde el 22-oct**. A-real vigente: sin boleta hasta que el dueño confirme efectivo y atribución (VOO, NFLX, UBER…).
3. **Binance (papel y real):** papel 9,874.86 (índice 98.75; 0.002698 BTC + 5,996.44 MXN); real 4,906.54 (índice 98.13; 0.001325 BTC + 3,001.83 MXN). BTC-USD 76,820. **Hackeo a Binance el 29-oct (US$5.3–6.3 mil M según bitácora), retiros 0/990 desde el 30-oct.** O0007 (vender en papel las 0.002698 BTC si a las 00:00 UTC del 31-oct siguen suspendidos) está pendiente. Hay tres reglas de contingencia en conflicto: parametros.json (ROJA = retiros MXN o BTC suspendidos > 24 h), lista-senales-de-alerta.md §3 (una ROJA activa la contingencia) y nota del dueño para la cuenta real ("retirar, no vender").

**Rivales (TWR al 30-oct):** ChatGPT GBM −1.88% / Binance −6.82%; Grok GBM −0.90% / Binance −4.80%. Claude real GBM +0.42%, Binance −1.87%. **Claude va adelante del mejor rival** → regla del modo torneo: reducir varianza.

**ALTERNATIVAS:**
- **(A)** Statu quo en papel GBM.
- **(U0)** Papel: vender el último UPRO (13.2%) → efectivo/CETES; ataca la varianza ahora que vamos adelante y que R20 dice que el 3x real empata al 1x con μ ≈ 11.2% a r = 3.8%.
- **(R1x)** Papel: rotar el UPRO a 3 SPYM adicionales (misma beta del S&P, sin acarreo 3x).
- **(Bx)** Binance: unificar regla de contingencia; ratificar, adelantar o anular O0007.
- **(A-real)** Sin boleta real hasta confirmación del dueño.

**EVIDENCIA DEL LABORATORIO DE LA SEMANA** (`laboratorio/tabla-maestra.md`):
- **R20** (Replicado, AC-27): UPRO real rinde −1.59 / −1.55 pp/año bajo el sintético 3x; −2.30 / −2.22 con tasa ≥ 3%. Con r = 3.8% y σ = 17%, el 3x empata al 1x con μ ≈ 11.2% antes del filtro (ficha 2026-10-27-acarreo-3x-por-tasas).
- **R21** (Replicado, AC-28): con UPRO al 13.5% la brecha sube P(−12%, 126 d) +0.31 pp y cuesta −0.21 pp/año; nota exploratoria contra U0: +0.73 pp CAGR a cambio de +5.0 pp de P(−12%).
- **R19b** (AC-26): el ISR del SIC cuesta ≥1.26 pp/año (piso; ~1.4–1.5 con art. 142 fr. V); rebalanceo mensual ~0.3 pp de impuestos.
- **R22b** (Replicado): tasa efectiva = mediana de 4 trimestres mejor que el último (plantilla de fichas, no cartera).

**CONTEXTO DE LA SEMANA:** FOMC 28-oct sin cambio (Warsh); PIB 3T26 ≥ 3.05% (SÍ); 10a ^TNX 4.93%; Brent 112.33 (Ormuz sin reapertura); ^GSPC −1.82% el 30-oct; Brasil (Lula reelecto; EWZ 32.46); elecciones intermedias de EUA el 3-nov; PCE 30-oct.
