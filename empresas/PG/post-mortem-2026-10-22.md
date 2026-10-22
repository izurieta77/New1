# Post-mortem · The Procter & Gamble Company (PG) · 1T FY27 (jul-sep 2026; reportado el 22-oct-2026, antes de la apertura)

> Rutina de cierre, 22-oct-2026. Los pronósticos se registraron el 25-sep en `empresas/PG/pronosticos.csv`, antes del resultado, y no se modifican. Las resoluciones están en `empresas/PG/resoluciones.csv`. Fase 0.

## 1. Resultado real (fuente primaria)
8-K del 22-oct-2026, ex. 99.1 ([SEC](https://www.sec.gov/Archives/edgar/data/0000080424/000008042426000250/fy2627q1jas8-kexhibit991.htm)).

| Concepto | 1T FY27 | Comparación |
|---|---|---|
| **Ventas netas** | **US$23,276 M** | +4.0%; tipo de cambio 0%; adquisiciones 0% |
| **Orgánicas** | **+4.0%** | volumen +2.4%, mezcla +1.1%, precio +0.4% |
| Por segmento (orgánico) | Beauty +5.4%, Grooming +4.5%, Fabric & Home +4.8%, Baby/Fem/Family +3.0%, Health Care +2.7% | |
| Margen bruto core | 50.0% | **−150 pb**: materias primas −140, reinversión −140, mezcla −50; productividad +120, aranceles (costos menores y recuperaciones) +50, precio +20 |
| Margen operativo core | 25.9% | −80 pb |
| UPA diluida | 1.97 | +1% |
| **UPA core** | **2.00** | +1%; sin tipo de cambio 1.99 (plana); reestructura de 0.03 excluida |
| Flujo operativo / retorno al accionista | 5.8 mil M / 3.9 mil M | dividendos 2.6, recompras 1.3 |
| Guía FY27 | orgánico 1-3% (sin cambio); total 2-4% (antes 1-3%, por Thorne desde el 1-oct); UPA core de 0 a +3% sobre 6.89 (sin cambio) | |

- **Reacción (Yahoo chart v8, secundaria):** cierre de **165.59, +5.6%** contra 156.84 del 21-oct, en un día de S&P −1.2% y Nasdaq a la baja.

## 2. Pronósticos contra resultado
| Pronóstico | Nuestro (p10-p90) | Consenso | Real | Error nuestro | Error del consenso | Puntuación |
|---|---|---|---|---|---|---|
| Ventas netas | 22,500 (22,100-22,950) | 22,749 | 23,276 | −3.33% | −2.26% | **Fuera del 80%, por arriba** |
| UPA core | 1.90 (1.83-1.97) | 1.887 | 2.00 | −5.00% | −5.65% | **Fuera del 80%, por arriba** |
| P(ventas > 22,749) | 0.30 | — | Sí | — | — | Brier **0.4900** |
| P(UPA core > 1.887) | 0.60 | — | Sí | — | — | Brier 0.1600 |

Brier promedio de los binarios: **0.3250**. Es el peor de la semana de reportes, después de TSLA (0.52 en un solo binario).

## 3. Matriz y lectura
- **Ventas: mal proceso, mal resultado.**
  - **El punto:** supuse orgánico ~+1% (la guía anual de 1-3% "acelerando de semestre a semestre") y tipo de cambio de −0.5%. El orgánico fue +4.0% con **volumen +2.4%**, y el tipo de cambio fue 0.
  - **El binario:** lo puse en 0.30, por debajo de 0.5, porque creía que el consenso no incorporaba las divisas. Era una apuesta contra el consenso con evidencia débil (una inferencia mía del §5 de la ficha). El consenso también se quedó corto, pero menos.
- **UPA: buen binario, punto tímido.** Superar 1.887 salió Sí. El punto 1.90 quedó dentro del margen de mi propio razonamiento, pero el p90 (1.97) era demasiado estrecho para una empresa que el año pasado entregó 1.99. El techo del rango quedó debajo del dato del año anterior.
- **Qué se sabía el 25-sep:**
  - la guía de UPA del 1T ("caída de al menos 5%") era conservadora por diseño;
  - P&G superó el consenso en la mayoría de los trimestres recientes;
  - el 4T FY26 tuvo orgánico 0% con base débil, así que la comparación del 1T FY27 era fácil.
- **Qué no se podía saber:** el volumen +2.4% (después de trimestres planos) y que las recuperaciones arancelarias sumaran 50 pb.
- **Escenario:** el orgánico de +4% en el 1T pone el año en el **alcista** de la ficha (≥3%), aunque la empresa no movió la guía orgánica. Margen bruto −150 pb, presionado por materias primas (petróleo y Ormuz) y reinversión. Lo sostiene el volumen, no el precio.

## 4. Lecciones (cada una cambia algo concreto)
1. **No apostar contra el consenso con una inferencia propia no verificada.** Aquí fue "el consenso no incorpora las divisas". El 0.30 salió de esa inferencia. Regla: un binario abajo de 0.45 contra el consenso exige una evidencia citada (guía explícita, dato de mitad de trimestre). Si no la hay, se parte de la tasa base de "supera el consenso" de la emisora. Se suma a la regla de la tasa base del post-mortem de GE (20-oct).
2. **El p90 no puede quedar debajo del dato del mismo trimestre del año anterior** cuando la guía anual es de crecimiento (UPA core 1.99 en 1T FY26 contra un p90 de 1.97). Checklist de las fichas de consumo básico.
3. **Las guías trimestrales "de al menos −X%" de P&G son pisos, no centros.** Igual que con PM (lección 1 del 21-oct), el patrón de la empresa importa más que la letra de la guía.
4. **IEEPA y aranceles:** el comunicado cita "recognized recoveries" arancelarias por +50 pb de margen bruto. Va al checklist de importadoras (lección de RTX del 20-oct): pedir en cada 8-K el monto de recuperaciones arancelarias.

No hay errores de hecho para `conocimiento/registro-de-errores.md`; son errores de pronóstico ya puntuados. Los binarios son del orquestador (autor claude), no votos de comité, así que no se actualiza `competencia/calibracion-agentes.csv`.
