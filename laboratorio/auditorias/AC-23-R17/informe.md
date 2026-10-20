# AC-23-R17: ejecución B independiente (20-oct-2026)

Lo único que se leyó fue el pre-registro `laboratorio/replicas/R17-volatilidad-objetivo-upro.md` (commit 1a3bdda). No se abrieron `R17.py`, `R16.py`, `R11.py` ni sus salidas. El código, `b.py`, está escrito desde cero y usa solo la biblioteca estándar. Se corre con `python3 -I b.py`; la sensibilidad, con `--deriva`.

## Datos (B, distinta de A)

| Serie | A (pre-registro) | B (esta ejecución) |
|---|---|---|
| Precio del índice (filtro, SMA200) | Yahoo `^GSPC` | CBOE `SPX_History` (desde 1975) |
| Rendimiento total | Yahoo `^SP500TR` | SPX + dividend yield mensual de multpl / 252. Se usa el último fin de mes publicado antes del día. **Es sintético y aproximado.** |
| VIX | Yahoo `^VIX` | CBOE `VIX_History` (cierre) |
| rf | FRED DTB3 | FRED DTB3 hasta el 2026-10-08 y, del 09 al 16-oct, Treasury 13 semanas con descuento bancario (5 días) |

- Los archivos se copiaron de `AC-22-R16/datos/` y sus sha256 coinciden; están en `datos/SHA256SUMS`.
- `datos/` se añadió a `.gitignore`.

## Método (según el pre-registro)

- **3x:** r3 = 3·r_TR − 2·rf − 0.91%/252. rf diaria = DTB3/100/252, del cierre previo.
- **Filtro con histéresis sobre SPX:**
  - salida si el SPX está por debajo de SMA200 × 0.97 o si VIX ≥ 25;
  - entrada si el SPX está por encima de la SMA200 y VIX < 25.
- **Momento de la decisión:** se usa el estado al cierre de t−1, se decide al cierre de t y el peso se aplica al rendimiento de t+1.
- **Volatilidad:** desviación estándar muestral (n−1) de r3 en t−20…t−1, × √252. Peso objetivo w* = min(1, objetivo/volatilidad).
- **Rebalanceo:**
  - entrada y salida del filtro, al día;
  - ajuste de peso solo en días hábiles que caen en viernes y si |w*−w| > 10 pp. Un viernes feriado no se recorre.
- **Costo:** 0.10% × |Δw|, cargado al cierre de la decisión. "Cambios" = días con Δw ≠ 0.
- **Métricas:**
  - CAGR con 252 días por año;
  - Sharpe = media(r−rf)/sd × √252;
  - MDD sobre la riqueza diaria.

## Decisiones propias declaradas (el pre-registro no las fija)

1. **Inicio de la evaluación: 1990-10-01**, porque H1 dice "1990-10".
   - B tiene SPX desde 1975, así que el filtro existe desde el 1990-01-02. Como sensibilidad se reporta "desde 1990-01": el Sharpe es menor (V0 0.472, por el arranque en 1990), pero la ΔMDD y la ΔSharpe no cambian.
2. **Peso constante entre ajustes** (rebalanceo implícito diario y sin costo hacia w). Como sensibilidad, `--deriva` deja que el peso derive con los rendimientos: ΔMDD +1.9 pp y ΔSharpe −0.006. El veredicto no cambia.
3. **BH3x sin costos de transacción.**

## Resultados (periodo completo, 1990-10-01 a 2026-10-16)

Ver `salida.txt`, con los tres periodos, y `b-resultados.json`.

| Variante | CAGR | Vol | Sharpe | MDD | Exp. | Cambios |
|---|---|---|---|---|---|---|
| V0 | 15.15% | 32.6% | 0.516 | −73.5% | 0.75 | 217 |
| VT30 | 12.91% | 25.9% | 0.498 | −60.8% | 0.62 | 522 |
| **VT45** | 14.44% | 30.7% | 0.509 | −72.0% | 0.71 | 304 |
| VT60 | 15.38% | 32.1% | 0.525 | −73.0% | 0.74 | 235 |
| BH 3x | 18.04% | 54.0% | 0.531 | −98.0% | 1.00 | 0 |

**Subperiodos**

| Periodo | VT45 frente a V0 | Sharpe (VT45 / V0) | MDD (VT45 / V0) |
|---|---|---|---|
| 1990-2008 | ΔMDD +1.5 pp, ΔSharpe −0.010 | 0.430 / 0.440 | −72.0% / −73.5% |
| 2009-hoy | ΔMDD +4.0 pp, ΔSharpe −0.006 | 0.586 / 0.592 | −45.3% / −49.3% |

**La MDD de V0 y la de VT45 son el mismo episodio:** pico el 1998-07-17 y valle el 2003-04-16. Es un mercado bajista lento con rebotes de volatilidad baja en los que el filtro vuelve a entrar. Ahí la volatilidad objetivo de 45% casi no recorta: el 3x rara vez supera 45% de volatilidad realizada cuando el filtro está encendido (VIX < 25).

## Veredicto (§2)

VT45 frente a V0, periodo completo: **ΔMDD = +1.5 pp (< 5 pp)** y ΔSharpe = −0.008 (dentro de −0.03).

- **H1 refutada**, porque la mejora de MDD no llega al umbral. Estado según B: **"No replicado"**.
- **H2: no** (el Sharpe de VT45 es menor que el de V0).
- Solo VT30 consigue un recorte de MDD grande (+12.7 pp), pero con ΔSharpe −0.018 y 2.2 puntos menos de CAGR. Es informativo: no es la variante principal.

## Diferencias esperables frente a A

- **Nivel de V0:** el TR sintético de multpl frente a `^SP500TR` y el SPX de CBOE frente a `^GSPC` pueden mover el nivel. El pre-registro cita, de R16, V0 con Sharpe 0.537 y MDD −73.7%; B obtiene 0.516 y −73.5%.
- **Tamaño del margen:** las diferencias de las deltas deberían ser pequeñas. La ΔMDD de B (+1.5 pp) está 3.5 pp por debajo del umbral, un margen amplio frente a diferencias de datos de ese tipo.
