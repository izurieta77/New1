# Post-mortem · Cemex (CEMEXCPO.MX) · 3T26 (reportado el 26-oct-2026, antes de la apertura)

> Rutina de cierre, 26-oct-2026. Los pronósticos se registraron el 25-sep en `empresas/CEMEXCPO.MX/pronosticos.csv` y en la §8 de `ficha.md`, antes del resultado, y no se modifican. Las resoluciones están en `empresas/CEMEXCPO.MX/resoluciones.csv`. Sin posición: no hay decisión de cartera ni votos del comité que evaluar, solo pronósticos. No se ejecutó `herramientas/pronosticos.py resolver` ni se tocaron `bitacora/pronosticos.csv` ni `competencia/calibracion-agentes.csv`.

## 1. Resultado real (fuente primaria)
**Fuente:** Cemex, 6-K del 26-oct-2026 en SEC EDGAR (CIK 1076378, accession 0001193125-26-430975):
- Anexo 1, comunicado: [d110472dex1.htm](https://www.sec.gov/Archives/edgar/data/1076378/000119312526430975/d110472dex1.htm) (sha256 `d969b033…`).
- Anexo 2, reporte trimestral con el estado de resultados en miles de US$: [d110472dex2.htm](https://www.sec.gov/Archives/edgar/data/1076378/000119312526430975/d110472dex2.htm) (sha256 `a518018f…`).
- Anexo 3, presentación (diapositivas en imagen; guía en la p. 18): [d110472dex3.htm](https://www.sec.gov/Archives/edgar/data/1076378/000119312526430975/d110472dex3.htm).

Estado de resultados del 3T26 (anexo 2, en US$ M; los porcentajes son contra el 3T25):
- **Ventas: 4,590.4** (4,590,392 miles; +8%, +5% comparable). Por región: México 1,299 (+16%), EUA 1,373 (+5%), EMEA 1,435 (+4%) y SCAC 333 (+12%).
- **UAFIDA de operación: 990.2** (+12%, +9% comparable), con margen de 21.6% (+0.8 pp). Por región: México 480 (margen de 37.0%), EUA 259 (−4%), EMEA 257 (+4%) y SCAC 62 (−5%).
- D&A: 338. Utilidad de operación antes de otros gastos: 652.0 (margen de 14.2%).
- **Otros gastos, neto: +25.9, una ganancia** (contra −95.1 en el 3T25).
- Gasto financiero: −102.9. Otros financieros: −14.8, que incluyen cambiario −7.4, instrumentos +8.8, ingreso financiero +9.4 y VPN −25.5. Asociadas: +20.2.
- **Utilidad antes de impuestos: 580.3. Impuesto: −170.9, tasa efectiva de 29.45%** (33.5% en el 3T25; 28.9% en 9M26; cálculos propios).
- Utilidad de operaciones continuas: 409.4. Discontinuas: +1.5. Minoritario: −3.5. **UN controladora: 407.5** (+55%).
- **UPA por ADS de operaciones continuas: básica 0.28 y totalmente diluida 0.28** (0.16 en el 3T25), con 1,458 M ADS diluidos (1 ADS = 10 CPO).
- **Nota de definición:** el reporte solo publica la UPA por ADS de operaciones continuas. Por eso aplica la regla del criterio ("si solo se publica la de operaciones continuas, se usa esa") y el resultado es **0.28**. El total controlador da el mismo número (407.5 / 1,458 = 0.279, cálculo propio). Esta UPA es **por ADS en US$, no por CPO**: por CPO serían ~US$0.028.
- **Guía 2026 (p. 18 de la presentación):** UAFIDA +16-17% a/a, que ahora se describe como "like to like for ongoing operations" y asume un USD/MXN de 18.25-18.50 en el 4T26. Otros conceptos: costo de energía por tonelada "low-single digit" al alza, capex de mantenimiento de ~900, impuestos en efectivo de ~400 y capital de trabajo de 50-100. La guía de volumen (p. 20) baja concreto premezclado en el consolidado, México, EUA y EMEA, y baja cemento en Europa.

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error nuestro | Error del consenso | Puntuación |
|---|---|---|---|---|---|---|
| Ventas 3T26 (US$ M) | 4,490 (4,320-4,660) | 4,456.6 | 4,590.4 | −2.19% | −2.91% | Dentro del 80% |
| UPA diluida 3T26 (US$ por ADS) | 0.22 (0.14-0.29) | 0.21 CX (0.30 vía CPO) | 0.28 | −21.43% | −25.0% CX (+7.1% CPO) | Dentro del 80%, en el borde |
| P(ventas > 4,456.6) | 0.60 | — | Sí | — | — | Brier 0.1600 |
| P(UAFIDA ≥ 950) | 0.55 | — | Sí (990.2) | — | — | Brier 0.2025 |

Brier promedio de los binarios: **0.1813**. Ambos binarios acertaron la dirección, pero con poca convicción (0.60 y 0.55). El punto de ventas fue mejor que el consenso. El punto de UPA fue apenas mejor que el consenso de CX y peor que el de CEMEXCPO.MX (0.03 por CPO = 0.30 por ADS).

## 3. Matriz y lectura
- **Ventas: buen proceso, buen resultado con sesgo bajista.** México salió clavado (1,299 contra ~1,300) y EMEA cerca (1,435 contra ~1,425). El error se concentró en EUA (1,373 contra ~1,320; +5% con más volumen de cemento y agregados) y en SCAC (333 contra ~300). El supuesto de "EUA estancado" (cadena C) fue demasiado pesimista para el trimestre.
- **UPA: resultado dentro del intervalo, pero con un error de punto grande (−21%) y en el borde superior.** Puente del pretax, cálculo propio: nuestro supuesto implicaba ~445 (955 − 340 − 50 − 100 − 20) y el real fue 580 (+135). Se explica así:
  - **Otros gastos (+76):** se supusieron −50 y hubo una ganancia de +26, probablemente por la venta de activos de Atlanta, aunque el reporte no lo atribuye explícitamente (inferencia).
  - **UAFIDA (+35).**
  - **Cambiario (+13).**
  - **Partidas financieras no modeladas, neto (+13):** asociadas +20, instrumentos +9, ingreso financiero +9 y VPN −26.
  - **D&A (+2) y gasto financiero (−3).**
  - **La tasa jugó en contra:** 29.45% contra 28% supuesta, ~−8 M o ~−0.006 por ADS.
  
  Es buena estimación operativa, pero la línea de "otros gastos" se modeló con un supuesto mecánico, y en Cemex esa línea es volátil y de signo cambiante (−95 en el 3T25, ~−493 de deterioro en el 4T25).
- **Binarios (0.60 y 0.55): buena dirección, poca convicción.** El argumento de México con peso fuerte (+8% cambiario) se cumplió y llevó a la UAFIDA a 990, 35 arriba del punto implícito (~955). Con un punto de UAFIDA de 955 y un umbral de 950, 0.55 era coherente; el error estuvo en el punto, no en la probabilidad.
- **Qué se sabía el 25-sep:** el tipo de cambio del trimestre, la guía de +16-17% (que exigía un 2S fuerte), la venta de Atlanta (anunciada en el trimestre) y el historial de "otros gastos".
- **Qué no se podía saber:** el signo de "otros gastos" del trimestre y la tasa efectiva exacta.
- **Escenario (§7):** la UAFIDA de 9M26 es de 2,802 (+22%). Para el rango base de 2026 (3,570-3,620), el 4T26 necesita 768-818 (cálculo propio). La emisora reitera +16-17%, ahora en términos comparables. EUA crece en ventas, pero su margen cae a 18.9% (−1.7 pp). **Lectura (inferencia):** el resultado es consistente con el escenario base; no se cambian probabilidades sin revisar la ficha.

## 4. Lecciones (cada una cambia algo concreto)
1. **Tasa efectiva de impuestos (lección recurrente; tercer caso en una semana, tras AMX el 21-oct y BOLSA el 22-oct):** 29.45% real contra 28% supuesto; 33.5% en el 3T25 y 28.9% en 9M26. Regla para la §8 de toda ficha: anotar la tasa efectiva de los últimos 4 trimestres y de los 9M junto al supuesto, y usar la mediana, no una cifra redonda. Aquí la tasa no fue la causa principal del error, pero se volvió a fijar sin historial.
2. **"Otros gastos" en emisoras con desinversiones activas:** cuando hay ventas de activos anunciadas o cerradas en el trimestre (Atlanta, Francia, Colombia), modelar esa línea en un rango que incluya ganancia, no un −50 fijo. Además, ensanchar el p90 de la UPA: el real (0.28) quedó a 0.01 del borde.
3. **Definición de UPA:** el criterio previó correctamente que Cemex solo publica la UPA de operaciones continuas y fijó la unidad (US$ por ADS; 1 ADS = 10 CPO). Se mantiene como plantilla. El consenso por CPO (0.03) se redondea demasiado para ser útil: convertirlo a ADS y anotar el redondeo.
4. **Segmento EUA:** contrastar el supuesto de ventas con los datos mensuales de cemento del USGS antes de fijar el punto (checklist de la §8 para cementeras con exposición a EUA).

No hay errores de hecho que registrar en `conocimiento/registro-de-errores.md`: el comunicado no repite las cifras del 2T26 de la ficha, y el 3T25 (ventas de 4,245, UAFIDA de 882, UPA de 0.16) coincide con la tabla de la ficha.
