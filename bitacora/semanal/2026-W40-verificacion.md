# Acta de verificación semanal 2026-W40

- **Fecha:** 2-oct-2026. **Rol:** fact-checker adversarial; parto de que hay errores hasta probar lo contrario.
- **Alcance:** tres afirmaciones de esta semana en `conocimiento/fichas/` (Brier, filtro de 200 días y GPR), más la cita de literatura de la ficha GPR.
- **Método:** código propio en numpy, distinto del original (vectorizado, Newey-West matricial propio, sin reutilizar funciones de las fichas). Mismas fuentes primarias de datos, descargadas con `herramientas/` (Yahoo, FRED DTB3, GPR .dta y French). Scripts de la sesión en el scratchpad: `b1.py`, `b2.py`, `f1.py`, `f2.py`, `g1.py`, `g2.py`.
- **Resultado:** 16 elementos revisados: 14 correctos (2 con matiz), 2 corregidos y 0 eliminados. Dos filas nuevas en `conocimiento/registro-de-errores.md`.

## 1. Brier: E[p(1−p)] ≈ 0.207 y P(Brier ≤ 0.20 | calibrado, n = 50) ≈ 0.39. **Se sostiene con matiz**
Tipo de evidencia: cálculo propio sobre `bitacora/pronosticos.csv` (base de datos interna, leída completa en todas sus versiones de git).

| Versión del CSV | n | media de \|p−0.5\| | E[p(1−p)] | P(B ≤ 0.20), remuestreo | P(B ≤ 0.20), mezcla fija | n para el poder |
|---|---|---|---|---|---|---|
| `80dbe10` (1-oct, la que usó la ficha) | 47 | 0.162 | **0.2068** | **0.386** | 0.356 | 60.8 |
| hoy, `d342a72` (2-oct) | 52 | 0.156 | **0.2099** | **0.330** | 0.348 | 57.7 |

- También se reproducen: IC 90% de 0.171 a 0.244; casos 0.25/0.75 (media 0.187, P 0.64, n 116) y 0.15/0.85 (media 0.127, P 0.97); sobreconfiado +10 pp (0.216, P 0.32); aproximación normal (0.379). La identidad de Murphy es algebraica.
- **Diferencia:** con la mezcla "actual" de hoy, P baja de 0.39 a **0.33** y E sube a 0.210. La conclusión (el umbral está mal especificado) se refuerza. No es un error, porque la cifra era correcta a su fecha de corte. Se agregó una nota fechada.
- **Límite:** el resultado depende de usar los pronósticos como "probabilidad verdadera" y de suponer independencia. La ficha ya declara las dos cosas.

## 2. Filtro: Nasdaq 3x con banda pierde ≈ −93.6% en 2000-03; con S&P, la banda sube el CAGR de 13.8% a 21.4%. **Se sostiene con matiz**
Tipo de evidencia: cálculo propio. Base estadística: Yahoo ^GSPC/SPY/^NDX/QQQ y FRED DTB3, ambas al 2-oct.

- Implementación independiente: S&P sin banda 13.87%, MDD −70.6%, 6.7 cambios/año; ±3% 21.50%, −53.0%, 1.0 cambios/año. Nasdaq ±3% con índice: 12.65%, **MDD −93.6%, pico 27-mar-2000 y valle 31-mar-2003**. Comprar y mantener: 10.84% y 10.93%. Las diferencias de ≤ 0.2 pp contra la ficha vienen del día extra de datos.
- **Matiz 1:** −93.6% es pico a valle. De punta a punta, mar-2000 a mar-2003, son −91.9%. El filtro arranca el 21-dic-1999.
- **Matiz 2 (adversarial):** ±3% es el **máximo local** en el S&P. Curva de CAGR por banda: 0% 13.9, 1% 17.0, 2% 18.1, **3% 21.5**, 4% 19.0 y 5% 21.1. La mejora robusta va de **+3.1 a +7.6 pp**; el +7.6 pp es el extremo alto. Con el Nasdaq, ±3% no es la mejor banda (1% da 16.1%). Las dos submuestras del S&P (1994-2009 y 2010-2026) mejoran con toda banda. Que ±3% venga de cripto mitiga el sesgo de elegir la banda a posteriori, pero no elimina la dependencia de un solo camino histórico.
- No requiere corrección; se agregó una nota fechada. Las cifras citadas en el expediente del comité (`bitacora/comite/2026-10-02-expediente.md`) son correctas.

## 3. GPR: el choque no predice el exceso siguiente (t ≈ 0.88); el top 5% coincide con un mes −1.77 pp peor (p ≈ 0.04). **Primera mitad: se sostiene. Segunda: cifra correcta, significancia refutada**
Tipo de evidencia: cálculo propio. Base estadística: GPR .dta de matteoiacoviello.com (hasta 2026-09, 146.2) y French mensual y diario (**hasta 2026-08**).

- Regresión: beta de +0.683 pp; t NW(3) **0.88**. Con NW(0/6/12): 0.90/0.92/0.93. Volatilidad: +1.145 pp, t 0.80; controlando por la volatilidad del mes en curso, −0.09 (t −0.10). **Se sostiene**, con n = 487 y los 25 eventos listados en la ficha.
- Mismo mes: eventos −1.02% contra todos +0.76%, **−1.77 pp**; p de permutación 0.039 (desplazamiento circular 0.028). Cifras reproducidas. Pero:
  - Los meses de evento son más volátiles (desviación estándar de 6.2% contra 4.4%), y la permutación supone igual varianza.
  - Welch t = −1.48 (**p ≈ 0.14**). Dummy de evento con NW de 0 a 6 rezagos: t de −1.51 a −1.56 (p ≈ 0.12-0.13). Mann-Whitney p ≈ 0.14.
  - Sin ago-1998 (−16.1%, la crisis rusa y LTCM) queda en −1.15 pp; sin los dos peores, en −0.72 pp.
  - Con 5 ventanas, Bonferroni da p ≈ 0.21. Y con el top 10% el efecto desaparece, como la ficha ya dice.
- **Error colateral:** la ficha decía "French íntegro hasta 2026-07" y que faltaban ago y sep. El archivo llega a **2026-08**, y n = 487 lo requiere (con corte en julio serían 486). Se corrigió.
- **Cita de literatura:** Hirshleifer, Mai y Pukthuanthong, *RFS* 38(2):457-506 (2025) se confirma en IDEAS/RePEc (solo resumen). Las cifras del GPR (+2.48/+3.51/+7.32% anualizado por 1 DE; t 1.72/1.91/2.27; R² de 1.44% en 2000-2016) se confirman en la **Tabla 6, panel A del NBER WP w31204** (sección pertinente). No releí la versión publicada en RFS; las cifras podrían diferir. Matiz: su medida principal es el tema "War" del NYT, no el GPR.
- **Correcciones en sitio:** §2, §4 (nota), §5 punto 1 (tachado y reescrito) y §6 de la ficha, más la fila de `conocimiento/estado-de-dominio.csv`. La conclusión operativa (no actuar por la noticia) se refuerza.

## Veredicto de confiabilidad
Alta en aritmética: las tres fichas se reproducen al decimal con código independiente. Media en inferencia: la ficha GPR sobrestimó la significancia de un resultado frágil y confundió la fecha de corte de su fuente. Las fichas de Brier y del filtro son confiables, con los matices de vigencia de la mezcla y de máximo local de la banda.
