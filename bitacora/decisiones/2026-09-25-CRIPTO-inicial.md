# Decisión: cartera cripto inicial real de la cuenta `arena-claude-binance` (10,000 MXN)

- **Fecha de decisión:** 25-sep-2026, después del cierre de NYSE. La hora queda sellada por el commit de este archivo, antes de cualquier precio de ejecución.
- **Ejecución:** lunes 28-sep-2026, en real, por el dueño en la app de Binance. Solo spot. Decisión del dueño del 25-sep-2026: 10,000 MXN por IA, que cuentan para la competencia.
- **Temporada:** 28-sep-2026 a 28-ene-2027.
- **Perfil:** `cripto_binance`. Tope del dueño: pérdida de 5,000 MXN.
- **Estado de este documento:** decisión del comité tomada. Faltan el dimensionamiento del gestor de riesgo (con veto) y el informe del verificador, que se agregan abajo.

## Tesis y cómo se refutaría

**Tesis:** en 4 meses no hay ventaja demostrada entre las variantes cripto. Con la cartera A en GBM:
- P(quedar primero) es 36.9% para 100% BTC, 37.2% con filtro SMA200 y 36.2% sin cripto (cuantitativo, 9 métodos; el error estándar es de 5-9 pp);
- la cripto aporta 80-88% de la varianza de la cuenta combinada con 33% del capital.

Por eso la cuenta cripto se juega por **supervivencia y desempate por menor caída**: BTC como única moneda, reserva en MXN, un filtro de tendencia, sin ETH y sin compra de caídas.

**Se refuta si, al 28-dic-2026:**
- la cuenta cripto tocó −30%; o
- quedó 5 pp o más debajo de un 100% BTC comprar-y-mantener medido en papel, sin haber tenido una caída máxima al menos 10 pp menor.

## Dictámenes (3 líneas cada uno)

- **Abogado del diablo, confianza 70. Voto: en contra de K1-K4 tal como están.**
  - Tasa base (BTC en MXN, ventanas de 122 días desde 2018): tocó −30% en 26.5% de las ventanas y −50% en 3.7%.
  - K2 le ganó a K1 solo en 25% de las ventanas. K4 (comprar caídas) sube P(−30%) de 12.8% a 19.2%.
  - Prefiere 65% BTC / 35% MXN: tocó −30% en 8.5% de las ventanas; peor caso −38.7%.
  - Condiciones:
    - cortacircuitos que vendan (ya aplicados, commit c31a2c9);
    - ruta MXN→USDT→BTC con límite;
    - sin stops en pares MXN;
    - plan por si Binance restringe México.
- **Macro, confianza 60. Voto: K4 con freno (55% BTC, 20% ETH, 25% USDC).**
  - Régimen mixto: VIX 14.9 y spread HY 2.73% a favor; tasa real de 2.85% y bono a 10 años en 5.18% en contra. En 2026, BTC pierde 1.1% por cada +10 pb semanales de tasa real.
  - Con la tasa real subiendo 40 pb o más, P(−50%) fue 13% en K1 y 0% en K4 con freno (n≈5, grado C).
  - Riesgo: la Fed del 28-oct y una tasa real mayor a 3.1%.
- **Analista cripto, confianza 55. Voto: K4 modificada (60% BTC en dos tramos, 20% ETH, 20% reserva en −10%).**
  - Régimen alcista: +18.5% sobre la SMA200, flujos a ETFs de +2,560 M USD en septiembre.
  - En estados como el de hoy, P(tocar −20%) es K1 51%, K3 65% y K4 37%. Según él, K3 duplica lo que ya hacen los cortacircuitos.
  - Verificó pares con MXN, OCO, comisión de 0.10%, SPEI por Medá y la migración de Funding a Spot desde el 29-sep.
- **Cuantitativo, confianza 45. Voto: K3, 100% BTC con salida total bajo la SMA200.**
  - K2 y K4 quedan debajo de K1 en los 9 métodos. K1 y K3 empatan estadísticamente. La compra de caídas es grado D (t = 1.05).
  - BTC cae 20% o más desde su máximo en 61-82% de las temporadas.
  - Simulación en `arena/modelos/cripto_inicial_simulacion.py`.
- **Geopolítico, confianza 60. Voto: K3 con destino 65% BTC / 35% MXN, sin ETH.**
  - Escalonado: 4,000 MXN el 28-sep, 1,500 tras el FOMC del 28-oct y 1,000 tras el 4-nov. BTC no fue refugio en 10 choques militares (2022-26).
  - Contraparte: el DOJ investiga a Binance por sanciones a Irán, sin cargos (Bloomberg vía CryptoTimes, pendiente de verificar). Binance no tiene licencia mexicana (inferencia).
  - Contingencia: abrir y probar Bitso, con disparadores definidos.

## Votos y regla aplicada (por componente, como en la cartera de GBM)

| Componente | A favor | ¿Sobrevive al abogado del diablo? | Resultado |
|---|---|---|---|
| BTC | 5 de 5 (confianza media 58) | Sí | **Entra** |
| ETH | 2 de 5 (macro 60, analista cripto 55) | No: "no sobrevive" y no hay 4 votos con confianza ≥ 60 | Fuera |
| Compra de caídas o reserva que compra | 2 de 5 (macro, analista cripto) | No: "no sobrevive" | Fuera |
| Filtro SMA200 (reducir o pausar bajo la SMA200) | 3 de 5 (cuantitativo, macro, geopolítico) | Sí, con condiciones (whipsaw; el dueño ejecuta a mano) | **Entra**. La forma exacta la fija el gestor de riesgo. |
| Efectivo en MXN o en stablecoin | MXN: abogado, geopolítico y analista cripto; USDC: macro | — | **MXN** |
| Exposición y escalonamiento | Abogado 65% y geopolítico 65% escalonado; cuantitativo 100%; macro y analista cripto 55-60% en BTC | — | La fija el gestor de riesgo |

**Decisión:** BTC como única moneda, con reserva en MXN, filtro SMA200 y sin ETH ni compra de caídas. Tamaño, escalonamiento, stop y boletas quedan a cargo del gestor de riesgo.

## Disenso (se conserva íntegro)

- **Macro y analista cripto** quieren 20% en ETH y una reserva que compre caídas. El macro argumenta que USDC protege en MXN porque el USD/MXN subió en 9 de 10 crisis.
- **El cuantitativo** quiere 100% BTC con salida total bajo la SMA200. Cambia a K1 si GBM sube a beta 1.3 o más y el comité acepta la deriva histórica.
- **El analista cripto** sostiene que el filtro SMA200 duplica los cortacircuitos y empeora la mediana (K3: −6.0% contra −0.2% de K1 en estados como el de hoy).
- **El geopolítico** acepta K4 solo con ETH ≤ 5%, efectivo en MXN y compras únicamente tras choques militares.

## Riesgos no de mercado y contingencia

- **[I] Regulación en México:** Binance no tiene licencia mexicana. El SPEI pasa por Medá, su IFPE [H, FAQ de Binance].
- **[H] Precedentes:**
  - UE: "solo retiros" desde el 1-jul-2026, con 6 días de aviso;
  - Brasil, 2022: 18 días sin PIX.
- **[P] Estimaciones del geopolítico:** Binance restringe México, 3%; SPEI caído más de 7 días, 5%; cargos del DOJ, 6%.
- **Contingencia** (el detalle operativo lo fija el gestor de riesgo):
  - abrir y probar una cuenta en Bitso;
  - disparadores: aviso de Binance, SPEI caído más de 48 h, o acción de CNBV, FinCEN, OFAC o DOJ;
  - respuesta: vender a MXN y retirar por SPEI; si falla, mover BTC a Bitso.

## Pronósticos del comité

| ID | Autor | Pregunta | p | Resuelve |
|---|---|---|---|---|
| P0015 | abogado del diablo | BTC-USD cierra en 67,236 o menos algún día antes del 28-ene-2027 | 0.40 | 28-ene-2027 |
| P0016 | macro | BTC-USD sobre su SMA200 el 28-dic-2026 | 0.67 | 28-dic-2026 |
| P0017 | analista cripto | BTC-USD > 84,084.40 el 28-dic-2026 | 0.55 | 28-dic-2026 |
| P0018 | cuantitativo | BTC-USD cae 20% o más desde su máximo acumulado antes del 28-ene-2027 | 0.70 | 28-ene-2027 |
| P0019 | geopolítico | Se promulga una ley de estructura de mercado cripto en EUA antes del 1-ene-2027 | 0.04 | 1-ene-2027 |

## Tamaño, stop, criterio de salida y boletas

*Pendiente del gestor de riesgo, con veto. Se agrega en este mismo archivo.*

## Verificación de cifras

*Pendiente del verificador. Se agrega en este mismo archivo.*
