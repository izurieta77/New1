# Decisor, corrida vespertina: 2-oct-2026 (viernes, 19:27 CDMX; 01:30 UTC del 3-oct)

**Nada amerita actuar antes del lunes.** La decisión de cartera del comité W40 sigue en pie. Lo único urgente era el hallazgo bloqueante de la revisión de calidad, y ya está cerrado.

- **Hallazgo bloqueante (revisión del 2-oct):** las cifras de riesgo de la decisión W40 no tenían un artefacto reproducible en el repo.
  - **Atendido:** archivé los scripts y datos del gestor de riesgo en `arena/modelos/comite_w40_riesgo/` (README, `sim.py`, `stop.py`, salidas y SHA256) y los volví a correr.
  - **Se reproducen exactamente:** P(−12/−20%) de 23.5/2.6% sin stop y 13.8/0.6% con stop, y mediana de +6.3%.
  - **Error de etiqueta corregido:** la mediana de la cartera A era +4.9% (1994-2026), no "+5.2-5.9%". Quedó una nota en la decisión y la alerta está cerrada.
  - **La decisión no cambia.** La ficha "costo del apetito" (con prima de 4%, el modo C crece ~0.9 pp menos) queda para el comité del 9-oct junto con esta cifra histórica.
- **Hallazgos menores de la revisión, corregidos:**
  - el pendiente de tipo de cambio en REGLAS §7 ahora marca 1 de 5 puntos resuelto;
  - el marcador ya dice que la boleta del 30-sep quedó ANULADA.
- **Carteras:** papel GBM 20,441.67 (índice 102.68, DD 0%), papel Binance 10,129.95 (índice 100.87) y real Binance ~5,000. Sin cortacircuitos ni tope en juego.
- **Lunes 5-oct:** O0004 y O0005 se ejecutan en papel si el filtro sigue encendido (^GSPC 7,722.72 contra un umbral de entrada de 7,442.59). La boleta real depende del fondeo y del ticker. No se genera ninguna orden nueva.
- **Irán/Ormuz:** sigue en ALTA y sin regla disparada. El fin de semana no hay mercado en EUA; BTC 84,620 y filtro encendido.
