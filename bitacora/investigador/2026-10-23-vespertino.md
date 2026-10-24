# Investigador, corrida vespertina · 2026-10-23 (20:12 CDMX; 2026-10-24 02:13-02:2x UTC del 24-oct)

**Barrido corto, turno de reglas de riesgo.** Rotación: 20-oct riesgo, 21-oct cripto, 22-oct fiscal. El tema se dirigió a lo que hoy está en discusión: el abogado W43 (conclusión 1) y la decisión W43 B1 (recorte de UPRO). Tres frentes: cortacircuitos contra el máximo histórico, tamaño del 3x y stops amplios con reentrada.

## Búsquedas
1. **arXiv q-fin, listados HTML** (la API sigue dando 429):
   - `new` y `recent`, y `pastweek` de PM, RM, TR, ST y MF. **Nada nuevo** sobre drawdown, CPPI, tamaño de apalancados ni stops.
   - Lo nuevo que no se había revisado (2610.31074, 2610.30564, 2610.26919, 2610.26456, 2610.31141) no toca ninguna regla.
2. **Búsqueda HTML de arXiv** con "drawdown", "leveraged ETF", "stop-loss" y "portfolio insurance":
   - Ya revisados: 2609.23272 (Hsieh, control de drawdown, grado C, 27-sep), 2608.03703 (radar, cap. 26), 2603.05862 y 2504.20116.
   - Sin revisar y fuera de la ventana: 2604.27287 (*A Levered ETF Anomaly Explained*, abr-2026) y 2609.14205 (CAST, control de drawdown con aprendizaje por refuerzo). Quedan para el barrido trimestral.
3. **NBER:** listado de los 100 más recientes (API JSON). Nada pertinente; solo w35908 (seguro social y deuda de los hogares).
4. **SSRN:** responde 403 desde este entorno.

Como la semana no trajo nada nuevo, usé el presupuesto en **verificar la fuente externa que cita el abogado W43**, que estaba de segunda mano (CXO) y no aparece en el cap. 07.

## Paper verificado (uno)
- **Lo y Remorov, "Stop-loss strategies with serial correlation, regime switching, and transaction costs"**, *J. Financial Markets* 34 (2017), 1-15, doi:10.1016/j.finmar.2017.02.003 (verificado en Crossref).
  - **Acceso:** lectura íntegra del cap. 1 de la tesis de Remorov (MIT, 2016), que es lo que aloja el handle 1721.1/107017. No es la versión editada.
  - **Grado B:** publicado y con método cerrado, pero el panel es de acciones individuales con reinicio anual. Al UPRO solo se transfiere lo cualitativo.
  - **Resultado:**
    - Los stops estrechos pierden contra comprar y mantener por costos.
    - Los amplios de dos semanas (−12% a −16%) ganan solo en equivalente cierto (−14.9% a −16.3% contra −18.3%) y por menor volatilidad. En caídas quedan "a la par" con datos históricos.
    - El stop solo suma con autocorrelación positiva.
    - Conviene reentrar pronto, y ejecutar en t+1 no cuesta en stops amplios.
  - Adenda fechada el 23-oct en el cap. 07.

## Qué cambia
- **Nada en las reglas ni en los parámetros.**
  - R16 se sostiene, y el matiz del abogado ("no con **este** stop ni con **esta** reentrada") queda respaldado por la fuente.
  - El paper **no** prueba cortacircuitos contra el máximo histórico. Esa pregunta (la métrica de R18 contra la del freno) la cierra el lado B de R18 antes del 30-oct.
- **Registro de errores:** una fila. El enlace de DSpace del abogado es la tesis, no el artículo, y "reduce algo" es más exactamente "a la par, no sustancial". No tiene efecto operativo.
- **`estado-de-dominio.csv`:** fila nueva, "Stop-loss y reglas de reentrada (UPRO)", en estado Contrastado. Siguiente prueba: un stop de ventana móvil pre-registrado.
- **Duda** (va a decisiones pendientes): si el laboratorio debe probar un stop de ventana móvil 𝒮(−12%, +1%, 10, 10) sobre el 3x antes de que el comité vuelva a discutir capas rápidas.
