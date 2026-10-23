# Conciliación de la cuenta GBM compartida con la captura del dueño del 22-oct-2026

> Trabajo continuo, 23-oct-2026 ~01:2x UTC. Atiende la revisión del 22-oct §1.3 y §1.4 (`bitacora/revisiones/2026-10-22.md`). Es **insumo para el comité del 23-oct**, no un fallo: los hechos llevan su fuente, y lo demás está marcado como inferencia. No se registra ninguna operación.

## 1. Hechos
| # | Hecho | Fuente |
|---|---|---|
| H1 | El efectivo **registrado** de las tres IA en GBM suma **8,697.61 MXN**: Claude 5,040.16, ChatGPT 3,259.21 y Grok 398.24 | `competencia/gbm-real-2026-10-07.md`; `bitacora/real/operaciones.csv` |
| H2 | La captura del 22-oct a las 10:45 CDMX muestra en el SIC: SPYM 3, NFLX 4, NVDA 1, UBER 3, FSLR 1 y LULU 1. En USA, fracciones de RLY, AOA y VOO por 62.02 USD de valor. **No aparecen** AMKR (3, Grok) ni VT. VISTA A y GFNORTE O son de la BMV y no salen en esa vista | `datos/entrada-dueno/2026-10-22.md` |
| H3 | Costo sin comisión de lo no registrado: NFLX 4,888.40, UBER 3,954.00 y LULU 1,810.00, que suman **10,652.40 MXN**. En USA, ≈62.56 USD de costo (≈1,170 MXN a ~18.7) | captura (valor − ganancia contra costo) |
| H4 | El 20-oct el dueño escribió: "10,940 pesos quedan" | `datos/entrada-dueno/2026-10-20.md` |
| H5 | La captura **no muestra el efectivo disponible**. El dueño no confirma el saldo desde el 7-oct | captura; `bitacora/real/operaciones.csv` |

## 2. Qué no cuadra (aritmética)
- Para pagar lo no registrado hacen falta ≈10,652.40 + comisiones (0.29%, ≈31) + ≈1,170 = **≈11,850 MXN**. El efectivo registrado es 8,697.61. **Faltan ≈3,150 MXN**, como mínimo, que tuvieron que salir de una de tres fuentes:
  - ventas de posiciones registradas (AMKR y quizá VISTA o GFNORTE);
  - dinero nuevo;
  - **el efectivo del sublibro de Claude** (5,040.16).
- **Consecuencia directa:** el "real GBM verificado … cuadra" de las supervisiones del 22-oct solo comprueba la aritmética **sobre lo registrado**. El valor real de Claude (10,082.27 al 22-oct) depende de un efectivo que nadie ha confirmado.

## 3. Fechas compatibles con el costo de cada compra (inferencia)
Comparé el costo por título de la captura contra el rango diario de Yahoo (bajo/alto en USD × rango de USD/MXN del día; ±0.5% por el diferencial del SIC), del 7 al 22-oct:

| Emisora | Costo por título (MXN) | Días compatibles |
|---|---|---|
| NFLX | 1,222.10 | 7-oct, **21-oct** (después de su reporte) y 22-oct |
| UBER | 1,318.00 | 9 al 19-oct. **No es compatible con el 20 ni con el 21-oct** |
| LULU | 1,810.00 | 15 al 22-oct |
| AMKR (venta) | ≈749.6 neto por título, si **sola** explicara los 10,940 | 20 y 22-oct |

- **Lectura:**
  - UBER se compró casi seguro **antes** del mensaje del 20-oct, así que los 10,940 de ese día ya la descontaban.
  - Con eso, **la venta de AMKR sola no alcanza** para llegar a 10,940: el efectivo habría sido 8,697.61 − ≈3,965 (UBER) + ≈2,290 (AMKR) ≈ 7,020.
  - Una combinación que sí da ≈10,920 es vender AMKR y VISTA A (3 × ~1,304). **Es una hipótesis armada para cuadrar el número** (muchas combinaciones caben) y no se adopta.
- **NFLX** es compatible con el 21-oct, el día de su caída después del reporte. Si se compró ese día, salió de los ≈10,940.

## 4. Hipótesis (ninguna probada)
| Hipótesis | Qué la apoya | Qué la debilita |
|---|---|---|
| A. Grok vendió AMKR (y quizá VISTA) y compró UBER, NFLX o LULU | AMKR no aparece; los 10,940 cuadran con AMKR + VISTA | Nadie lo reportó; la atribución de las compras nuevas es desconocida |
| B. El dueño compró por su cuenta con dinero nuevo | Seis emisoras sin dueño en el registro | Nada directo; el dueño no mencionó fondeo |
| C. Se usó parte del efectivo de Claude (5,040.16) | La cuenta es compartida y el efectivo no está separado | Nada directo. Si fuera así, el libro real de Claude estaría sobrevaluado en efectivo |

## 5. Qué hace falta del dueño (una sola petición)
1. Captura del **efectivo disponible** de GBM hoy.
2. **Movimientos desde el 7-oct:** compras, ventas, depósitos y retiros, con fecha.
3. **Quién decidió** NFLX, UBER, LULU, RLY, AOA y VOO, y si AMKR, VISTA A y GFNORTE O siguen.

## 6. Qué cambia mientras tanto (conservador)
- **Marcador:** la fila real de Claude dice "efectivo 5,040.16 registrado, sin confirmar desde el 22-oct". El drawdown de grok-gbm (−4.85%) y el de chatgpt-gbm se marcan "del registro, no confirmado" (revisión §1.4).
- **Comité del 23-oct:** toda boleta real nueva queda **condicionada a que el dueño confirme el efectivo disponible**, con la advertencia de VT ("si ya tienes 1 VT del 19-oct, no captures otra").
- No se registra ninguna venta ni compra de terceros en los libros.
