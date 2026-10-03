# Artefacto de riesgo de la decisión W40 (2-oct-2026)

Scripts del gestor de riesgo que sostienen las cifras de `bitacora/decisiones/2026-10-02-CARTERA-W40-modo-C-moderado.md`. Se archivaron el 3-oct a raíz del hallazgo bloqueante de la revisión de calidad del 2-oct. Originalmente vivían en el scratchpad de la sesión.

- `fetch.py`: descarga de Yahoo (`yahoo_historia`): ^GSPC, ^NDX, ^VIX, MXN=X, ^IRX, UPRO, SPY y QQQ. Resultado en `hist.pkl`.
- `dexmxus.pkl`: USD/MXN de FRED DEXMXUS (con MXN=X donde falta). Huellas en `SHA256SUMS.txt`.
- `sim.py`: temporadas de 82 días hábiles que arrancan con el filtro encendido (^GSPC > SMA200 × 1.03 y VIX < 25). UPRO sintético 3x con financiamiento 2 × ^IRX y gasto, calibrado contra UPRO real 2010+ (CAGR 30.14% sintético contra 29.67% real). En MXN y en USD. Salida en `salida_sim.txt`.
- `stop.py`: igual que `sim.py`, con el stop de −11.2% del UPRO al cierre. Salida en `salida_stop.txt`.
- `tail.py` y `val.py`: escenarios de cola estáticos y validación de límites.

**Reproducción (3-oct-2026):** `python3 sim.py` y `python3 stop.py` dentro de esta carpeta reproducen las cifras citadas:
- 23.5 / 2.6 / 0 / 0% sin stop (1994-2026, MXN, mediana +6.3%);
- 13.8 / 0.6 / 0 / 0% con stop (1994-2026);
- 10.5 / 0.2% con stop (2004-2026).

**Corrección:** en esta misma salida, la mediana de la cartera A (56/27/0/16) es **+4.9%** (1994-2026) y **+4.1%** (2004-2026), no "+5.2-5.9%" como decía la decisión. Su P(−12%) es 8.9% (1994-2026) y 5.3% (2004-2026).
