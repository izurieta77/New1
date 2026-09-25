---
name: ficha-empresa
description: Crea o actualiza la ficha de una empresa (IPC, EUA u otra) con datos primarios, expediente de 10 puntos, cadena causal, qué descuenta el precio, escenarios y pronósticos registrados antes de su próximo reporte.
---
# Ficha de empresa

1. Datos:
   - **EUA:** `python3 herramientas/dossier.py TICKER` (EDGAR + precios).
   - **México:** reporte trimestral en BMV o Emisnet, relación con inversionistas, y 20-F/6-K si la emisora reporta ante la SEC.
2. Escribe o actualiza `empresas/<TICKER>/ficha.md` con estas secciones:
   1. Negocio y segmentos.
   2. Último reporte contra el consenso.
   3. Tabla financiera de 8 trimestres y 5 años.
   4. Expediente de 10 puntos.
   5. Cadena causal (acontecimiento → exposición → efecto económico → estado financiero → valuación → precio).
   6. Qué descuenta el precio (múltiplos y DCF inverso).
   7. Escenarios a 12 meses con probabilidades que suman 100%.
   8. Pronósticos del próximo reporte: punto e intervalo de 80% para ingresos y UPA, más pronósticos binarios.
   9. Catalizadores.
   10. Fuentes.
3. Registra los pronósticos en `empresas/<TICKER>/pronosticos.csv` y en los ledgers de `bitacora/` con `herramientas/pronosticos.py`.
4. Pasa la ficha por el subagente `verificador`.
5. Actualización: nunca sobrescribas un pronóstico anterior. Si cambias de opinión, agrega una actualización fechada.

Regla: la ficha es investigación. No contiene recomendaciones de compra o venta mientras el sistema esté en fase 0.
