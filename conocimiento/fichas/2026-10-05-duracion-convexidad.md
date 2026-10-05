# Ficha de estudio: duración y convexidad, de la fórmula al ETF real (TLT)

> Laboratorio, 5-oct-2026. Fase 0. Tema "Renta fija: duración y curva" (cap. 04), que estaba en Documentado. El siguiente paso anotado era "comprobar duración/convexidad de un bono M". Relevancia hoy: el 10a de EUA está en 5.28% (+45 pb en un mes) y la cartera no tiene bonos. Esta ficha da la herramienta para dimensionar el riesgo de tasa si el comité considera duración (TLT o Mbonos) como cobertura.
> Código: `conocimiento/fichas/codigo/2026-10-05-duracion-convexidad.py` (stdlib + `herramientas`, ~3 s).

## 1. Pregunta
(a) ¿Las fórmulas de duración modificada y convexidad coinciden con el cambio exacto de precio? (b) ¿Cuál es la duración efectiva *observada* de TLT frente al rendimiento a 20 años, y es estable? (c) ¿La convexidad se puede medir con datos diarios?

## 2. Fuentes y acceso
| Fuente | Acceso |
|---|---|
| Fórmulas estándar de precio, Macaulay, modificada y convexidad (Fabozzi; cap. 04 §2) | Derivación propia, verificada con diferencias finitas |
| Yahoo TLT (cierre ajustado, que incluye cupones) | Íntegro, 2002-07-31 a 2026-10-01 (6,037 días con dato de FRED) |
| FRED DGS20 (rendimiento constante a 20 años) | Íntegro |

## 3. Resultados
**3.1 Bono tipo Mbono** (10 años, cupón semestral de 8%, rendimiento de 9%). Precio 93.496, Macaulay 6.95, **modificada 6.655** y **convexidad 58.3**. Las dos cifras coinciden con diferencias finitas a 4 decimales.

| Δy | Cambio real | Solo duración | Duración + convexidad |
|---|---|---|---|
| +100 pb | −6.373% | −6.655% | −6.363% |
| +200 pb | −12.216% | −13.310% | −12.144% |
| −200 pb | +14.557% | +13.310% | +14.476% |

- Con ±200 pb, la duración sola se equivoca en ~1.1-1.2 pp; con la convexidad, el error baja a 0.07-0.08 pp.

**3.2 TLT frente a DGS20** (regresión de r − y/252 sobre Δy y Δy²):

| Periodo | Duración empírica | Convexidad empírica | R² |
|---|---|---|---|
| 2002-2026 | **15.55** | 379 | 0.898 |
| 2002-2011 | 13.80 | 441 | 0.914 |
| 2012-2019 | 17.09 | −94 | 0.924 |
| 2020-2026 | 17.33 | 873 | 0.893 |
| Días con \|Δy\| ≥ 15 pb (n = 97) | 15.75 | −1,164 | 0.928 |

- **Segunda comprobación (analítica):** un bono a 25 años con cupón de 4% (proxy de la cartera de TLT) tiene duración modificada de 16.5, 15.3 y 14.9 y convexidad de 355, 318 y 305 con rendimientos de 3%, 4.5% y 5%. La duración empírica (15.5-17.3) cae en ese rango.
- **La duración es estable y se mide bien. La convexidad no.** Cambia de signo entre periodos, porque Δy² diario es diminuto y el ruido lo domina. Solo el promedio de 24 años (379) coincide con el valor teórico (~300-350).

**3.3 Días extremos (2020-2026)**, predicción −D·Δy + C/2·Δy² con D y C del periodo: error absoluto medio de **0.94 pp**. El peor caso es el 16-mar-2020: TLT subió +6.47% contra +3.83% predicho, porque la liquidez del Tesoro se rompió y la base ETF/NAV se disparó.

## 4. Lo que cambia para el sistema (inferencias, no reglas)
1. **Regla de bolsillo verificada:** TLT pierde o gana ~**16% por cada 100 pb** del rendimiento a 20 años, más ~1.6-1.9 pp de convexidad a favor con ±100 pb. Con el 10a en 5.28%, +50 pb costarían ~7.6% en TLT.
2. **En un Mbono a 10 años**, cada 100 pb mueven ~6.4-6.7%. La convexidad pesa poco por debajo de 100 pb.
3. **La convexidad se toma de la fórmula y no se estima de datos diarios:** la estimación empírica no es estable.
4. **En estrés de liquidez,** el ETF puede desviarse varios pp de lo que dicta la duración (marzo-2020), así que no es una cobertura exacta.

## 5. Límites
- DGS20 no es el rendimiento exacto de la cartera de TLT, que va de 20 a 30 años y cambia de composición.
- Usé la duración de Macaulay del bono con cupón y la tasa del mismo día, no la curva completa.
- No se modeló el Mbono real con precios de Banxico (no hay fuente primaria abierta con serie diaria de precios de Mbonos en este entorno).

## 6. Estado nuevo
"Renta fija: duración y curva" pasa de **Documentado** a **Comprendido con comprobación**.
