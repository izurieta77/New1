# Arbitraje · 2026-10-08 · Efectivo real GBM: 5,040.15 contra 5,040.16

Origen: hallazgo 1.2 de `bitacora/revisiones/2026-10-07.md`.

## Posiciones

- **Libro (`bitacora/real/operaciones.csv`):** el precio está guardado como 91.6600 USD y la comisión como 0.7973 USD, con tipo de cambio 17.985. Al reconstruir el costo en pesos queda 3 × 91.66 × 17.985 = 4,945.52, más 14.34 = 4,959.85. El efectivo resulta 5,040.15.
- **Dueño y GBM:** el correo de GBM de la orden 116707880 (Llena, 7-oct) dice 3 títulos a 1,648.50 MXN, importe 4,945.50 y comisión 12.36 + IVA 1.98 = 14.34. El total es 4,959.84 y cuadra con la baja del disponible de 20,399.99 a 15,440.15. El efectivo resulta 5,040.16.

## Fuente primaria

La confirmación de GBM que reportó el dueño, transcrita en la nota de la propia fila y en `competencia/gbm-real-2026-10-07.md`. La orden se ejecutó en pesos (SIC). El precio en USD es solo un equivalente: 1,648.50 / 17.985 = 91.659716…

## Fallo

**Gana la cifra de GBM: el efectivo es 5,040.16 y el costo total 4,959.84.** El centavo de diferencia salía de redondear el precio equivalente en USD.

## Correcciones

- En `bitacora/real/operaciones.csv` el precio queda en 91.6597164304 USD y la comisión en 0.7973311093 USD. La fila lleva una nota fechada. `construir_libro` reconstruye ahora un efectivo de 5,040.1600.
- En `bitacora/real/equity.csv`, fila del 7-oct: efectivo 5,040.16, posiciones 4,927.73 (sin cambio) y equity 9,967.89 (antes 9,967.87). El índice queda en 99.6789 con la base al fondeo (`2026-10-08-base-twr.md`).
- `competencia/marcador.md`, `competencia/rivales.csv` y `bitacora/briefs/2026-10-07.md` llevan una nota.
- Fila nueva en `conocimiento/registro-de-errores.md`.

Esta diferencia no cambia ninguna decisión.
