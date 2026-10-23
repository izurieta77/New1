COMITÉ SEMANAL DE CARTERA · viernes 23-oct-2026 (W43). Repo /home/user/New1 (rama claude/investment-strategy-routines-19ep76). Fase 0, con la excepción de la cuenta arena (config/parametros.json; decisiones vigentes: bitacora/decisiones/2026-10-02-CARTERA-W40-modo-C-moderado.md y 2026-10-16-CARTERA-W42-mantener-y-VT.md). Pasaron 5 días hábiles desde la W42 (REGLAS §4). NO edites archivos ni hagas commit; solo devuelve tu dictamen.

TESIS A EVALUAR (statu quo): "Mantener sin cambios la cartera de papel y la real hasta el comité del 30-oct".

1. **Papel GBM** (cierre del 23-oct; `bitacora/equity.csv`, `portafolio.py reporte`):
   - Valor 20,193.43 MXN, índice 100.97. DD −3.30% desde el pico del 9-oct (máximo −3.35%). Lleva −1.07 pp contra su benchmark 50/50 (+2.03%) desde el 28-sep.
   - Posiciones: 5 SPYM (41.3%), 1 QQQM (26.8%), 2 UPRO (26.6%) y 1,071.96 de efectivo.
   - **UPRO 144.04, 6.1% sobre el stop de 135.76** (bastan −5.75% de UPRO, o ≈ −2% del S&P en un día). Filtro: ^GSPC 7,623.68 contra una salida de 7,072.58 (SMA200 7,291.31 × 0.97), colchón 7.8%; VIX 19.45 < 25.
   - Perfil `arena_agresivo`: el siguiente nivel de cortacircuitos es −12%, a 8.7 pp.
2. **Real GBM** (`bitacora/real/equity.csv`):
   - Valor 10,044.35 MXN, índice 100.44: 3 SPYM + efectivo **registrado** de 5,040.16, **sin confirmar desde el 22-oct**.
   - **Boleta VT del 19-oct:** caducó sin línea VIGENTE y su **estado es desconocido**. La captura del dueño del 22-oct no muestra VT, pero tampoco hay confirmación literal.
   - **La cuenta compartida no cuadra:** faltan ≈3,150 MXN para pagar lo no registrado (NFLX, UBER, LULU y fracciones en USA; falta AMKR). Ver `competencia/conciliacion-cuenta-gbm-2026-10-22.md`.
3. **Real Binance:** 5,010.50 MXN, índice 100.21: 0.001325 BTC (40%) + 3,001.83 MXN. Filtro BTC encendido: BTC 81,294 contra una salida de 70,650.78 (colchón ~15%), vol30 25.7%. **La condición de B3 (cierre > 87,396) no se cumple.**

**Pregunta literal del dueño (22-oct):** "¿Qué carajos vamos a hacer? ¿Qué vendemos y a dónde movemos todo para no seguir perdiendo?"
- Pérdida contra costo en el SIC a las 10:45 del 22-oct: −128.80 MXN (−0.56%), casi toda en NVDA (−286, ChatGPT) y UBER (−120, sin atribuir).
- El libro de Claude va en verde.
- **Lo que el comité decide** es solo el libro de Claude. Sobre las demás posiciones puede dar una opinión, no una orden.

**ALTERNATIVAS:**
- **(B1)** Papel: reducir UPRO de 2 a 1 título (≈13% del papel).
- **(B2')** Real GBM: emitir una boleta nueva en un índice 1x que no duplique SPYM. Candidatos que el dueño ya vio en el SIC: VOO (duplica el S&P), IVOO (empresas medianas de EUA), VEA/RSP de la W42, o VT si aparece por ticker. **Condicionada** a que el dueño confirme el efectivo disponible y el estado de VT.
- **(B3)** Binance: subir BTC de 40% a 65% (condición: vol30 ≤ 45% y cierre > 87,396).
- **(C)** Rotar a otra cosa.
- **(A-real)** No emitir ninguna boleta real hasta que el dueño confirme el efectivo y la atribución.

**EVIDENCIA DEL LABORATORIO DE LA SEMANA** (`laboratorio/tabla-maestra.md`):
- **R16** (stop fijo del UPRO): no agrega protección; Sharpe de 0.537 a 0.394.
- **R17** (volatilidad objetivo de 45%): ΔMDD +1.5 pp con ΔSharpe −0.008. Ninguna de las dos se replicó.
- **R18 + adenda del 22-oct** (perfil `arena_agresivo`), con UPRO al 26.9%:
  - P(tocar −12% en 63 días) ≈ **21%** (A 21.0, B 21.4);
  - P(−20%) 3.5% (B) y P(−28%) 0.6% (B);
  - con UPRO al 13.5%, P(−12%) ≈ 16.4%, unos −4.6 pp;
  - **la lectura del 48% era del −8% del perfil estándar y NO aplica.**
- **R19 + AC-25** (Replicado): el ISR del SIC (10%) cuesta ~0.8 pp al año en MXN a la mezcla. El rebalanceo mensual suma menos de 0.2 pp, y la parte cambiaria de la ganancia gravable es ~7%. Vender todo el SIC hoy daría un resultado fiscal de −262 MXN, **sin ISR** (ficha del 22-oct).
- **Lectura común de R16-R18:** el riesgo del 3x se controla con el tamaño, no con capas rápidas.

**CONTEXTO DE LA SEMANA:**
- **Mercado:**
  - Venta de IA y chips: el 22-oct NQ −1.6%, SMH −6%, META −7% y INTC −8%; el S&P −1.2% el 22-oct y −0.5% el 23-oct (7,623.68).
  - VIX 19.45. 10a ~4.97%.
  - Brent 110-113, en máximos de cinco meses. Planes de ataque de EUA e Israel contra Irán después de las intermedias del 3-nov (prensa, B). Polymarket da 0.775 a que el alto el fuego dure hasta el 31-oct.
- **Fed:** 92.5% a que no hay cambio el 28-oct.
- **Peso:** USD/MXN 18.65 (Δ10 +1.8%; FX-1 OK; AVISO el 21-oct).
- **Paquete fiscal:** LIF 2027 y LISR aprobadas por Diputados el 13-oct; el Senado vota ~27-oct.
- **Reportes mexicanos:** 16 de 21 puntos dentro del rango; la sorpresa que se repite es la tasa efectiva.
- **Rivales reales al 23-oct** (los de GBM son **del registro, no confirmados**):

  | Cuenta | Rendimiento |
  |---|---|
  | Claude GBM | +0.44% |
  | ChatGPT GBM | −0.32% |
  | Grok GBM | −0.00% |
  | Claude Binance | +0.21% |
  | ChatGPT Binance | −1.99% |
  | Grok Binance | +0.39% |

  Diferencias menores a 1 pp contra una regla de 5 pp: **no hay modo torneo**.
- **Pronósticos:** el Brier global llega a 0.1979 (n = 74). El abogado del diablo lo audita hoy.

**PIDO:** un dictamen con:
1. un voto por cuenta (papel: A o B1; real GBM: A-real o B2' con el instrumento; Binance: A o B3);
2. una confianza de 0 a 100;
3. 3 líneas de argumento con cifras;
4. una frase para responderle al dueño "¿qué vendemos?", que distinga el libro de Claude de lo demás.

Responde en español, en 15 líneas o menos.
