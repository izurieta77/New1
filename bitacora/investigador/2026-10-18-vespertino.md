# Investigador, corrida vespertina · 2026-10-18 (20:12 CDMX; 2026-10-19 02:15 UTC del 19-oct)

**Barrido corto, turno de prima cripto.** Rotación: 16-oct fiscal, 17-oct reglas de riesgo.

## Búsquedas
- **La API de arXiv respondió HTTP 429 ("Rate exceeded")**, igual que el 15 y el 17-oct.
- **Alternativa que funcionó:** el listado HTML `arxiv.org/list/q-fin/new` (26 papers nuevos). Lo filtré por términos cripto y salieron dos:
  - **2610.21491** (Cha et al., NEST): ya lo había calificado la auditoría W42 (grado C).
  - **2610.21540**: nuevo.

## Paper verificado (uno)
- **Cha, Kim, Yeo, Sung, Lee, Son, Seo y Lee, arXiv:2610.21540** (15-oct-2026), "Pricing the Unprovable: Ambiguity, Turnstile Runs, and the Verifiability Discount in Crypto Protocols".
  - **Leído:** el HTML completo (44 mil caracteres): introducción, modelo (§3), caso Orchard (§5), panel entre eventos (§6), limitaciones (§8) y conclusión (§9).
  - **Qué dice:** reparar una falla en un protocolo privado (Zcash Orchard, jun-2026) no prueba que no se haya explotado antes. El mercado descuenta esa duda no resoluble, el "descuento por verificabilidad".
  - **Modelo:** con un "turnstile" (las salidas de cada pool están limitadas a su saldo registrado), salir primero traslada el posible faltante a quienes se quedan, así que la presión de salida crece con la exposición no resuelta.
  - **Evidencia:** en Orchard, la mayor caída y la mayor salida neta del pool coinciden con el reconocimiento de que no se podía descartar el abuso pasado, no con la reparación. Los autores lo llaman "directional, not causal".
  - **Panel de 40 eventos:** la pérdida reportada y la exposición no resuelta están correlacionadas (Pearson 0.86 entre 38 eventos), en parte porque la exposición se codifica a partir de la pérdida. Con el reloj corregido, el piloto **no identifica ni el signo** de la pendiente.
  - **Grado C:** modelo teórico más un caso; la muestra de 14 casos es intencional.

## Qué cambia
**Nada.** No hay adenda ni corrección. El argumento ya está implícito en la regla de riesgo de exchange de cripto/04: un reporte de prueba de reservas sin faltante no prueba que no haya faltante, y en una corrida pierde el último en salir. El paper lo formaliza para protocolos de privacidad; no aporta una medida aplicable a la cuenta Binance.

## Nota operativa
La API de arXiv falló 3 de las últimas 4 noches. El listado HTML `/list/q-fin/new` sí respondió. Lo anoto en `decisiones-pendientes.md` como alternativa; no edito el procedimiento.
