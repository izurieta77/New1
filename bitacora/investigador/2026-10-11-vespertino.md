# Investigador, corrida vespertina · 2026-10-11 (20:12 CDMX; 02:12 UTC del 12-oct)

**Barrido corto, turno de reglas de riesgo** (los dos anteriores fueron fiscales). **Resultado: nada que cambie una regla.**

## Búsquedas (API de arXiv, q-fin.PM/RM/TR, orden por fecha)
1. drawdown · 2. volatility targeting · 3. trend following · 4. position sizing / Kelly.
- Candidato ya revisado: Hsieh, arXiv:2609.23272 (control de drawdown), barrido del 27-sep, grado C; sin novedad.
- Nuevo revisado: **arXiv:2610.01325** (Kien y Huynh, 1-oct-2026), "PPO-HRAP: Proximal Policy Optimization with a Hybrid Regime-Aware Policy for Risk-Controlled Trading". Leído el resumen completo.

## Evaluación de 2610.01325
- **Qué dice:** un agente de aprendizaje por refuerzo mezcla su acción con una exposición objetivo derivada del régimen (penaliza aumentos de drawdown condicionados al VIX). En SPY, ventana de prueba 2020-2022, reporta 8.48% anual, Sharpe 0.64 y caída máxima de 18.47% contra 34.10% de comprar y mantener; cinco semillas en SPY y una sola corrida en QQQ y DIA.
- **Por qué no cambia nada:** una sola ventana de prueba de tres años, robustez fuera de SPY de una sola corrida (los autores lo admiten), rotación alta y sin costos de implementación realistas declarados. Riesgo alto de sobreajuste. **Grado D.**
- **Lo único útil:** es otro ejemplo de que condicionar la exposición a la volatilidad implícita (VIX) recorta la caída máxima, en línea con la salida por VIX ≥ 25 de la regla de UPRO. No es evidencia nueva: no supera lo que ya replicamos en el laboratorio (filtro SMA, V04/R04).

## Acción
- Sin cambios a capítulos ni al registro de errores.
