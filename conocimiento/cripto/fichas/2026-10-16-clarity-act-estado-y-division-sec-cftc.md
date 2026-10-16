# Ficha de avance · 16-oct-2026 · Frontera regulatoria (EUA): CLARITY Act (H.R. 3633), estado legislativo, división SEC/CFTC y rendimiento sobre stablecoins

> Corrida de las 08:17 CDMX (14:20 UTC), estudio profundo.
>
> **Por qué este tema.** Es el pendiente (a) de la ficha de ayer (`2026-10-15-mica-stablecoins-y-transicion-casp.md` §8) y la última pieza que faltaba en la fila de Frontera "Regulación: GENIUS, CLARITY, MiCA, Circular 4/2019 de Banxico" (`00-plan-de-estudio.md`). Además, P0019 (ley de estructura de mercado firmada antes del 1-ene-2027, p=0.04) se apoyaba hasta hoy en prensa ("cloture fallido 49-50 según prensa"). No existía ficha de CLARITY en `fichas/`.

## 0. Pregunta de hoy, acotada

1. ¿En qué estado legislativo está H.R. 3633 al 16-oct-2026, según el registro primario del Senado?
2. ¿Qué texto está en el calendario del Senado y cómo reparte el trabajo entre la SEC y la CFTC?
3. ¿Qué dice ese texto sobre el rendimiento que los exchanges pagan sobre stablecoins, la disputa que dejó abierta GENIUS 4(a)(11)?
4. ¿Qué implica todo esto para P0019 y para el precio de Kalshi?

## 1. Acceso y fuentes (declarado)

- **Texto aprobado por la Cámara (EH), íntegro:** `govinfo.gov/content/pkg/BILLS-119hr3633eh/html/BILLS-119hr3633eh.htm` (353,842 bytes; sha256 `d6256df1…2b2048`). GPO publica el mismo texto que congress.gov. "Passed the House of Representatives July 17, 2025."
- **Texto reportado en el Senado (RS), íntegro:** `govinfo.gov/content/pkg/BILLS-119hr3633rs/html/BILLS-119hr3633rs.htm` (889,841 bytes; sha256 `9ea670eb…5c20a5`). Calendar No. 423. Reportado el **1-jun-2026** por el senador Scott (Banking) "with an amendment" que sustituye todo el texto tras la cláusula de promulgación. Para leer solo el sustituto se quitaron las etiquetas `<DELETED>`.
- **Votación nominal del Senado:** `senate.gov/legislative/LIS/roll_call_votes/vote1192/vote_119_2_00234.xml` (sha256 `b17cd1ad…20a5`) y el índice de votaciones de la sesión `roll_call_lists/vote_menu_119_2.xml` (256 votaciones; la última es la 00256, del 30-sep).
- **Límite de acceso:** `congress.gov` (HTML) dio 403 y su API (DEMO_KEY) dio 429. No se pudo leer la lista "All Actions". El texto se tomó de GPO y el estado de las votaciones del Senado, del propio Senado. Las acciones que no son votaciones nominales (mociones por consentimiento unánime, avisos) **no** quedan cubiertas.
- **Mercados:** API pública de Kalshi (`api.elections.kalshi.com`, serie KXCRYPTOSTRUCTURE) y API Gamma de Polymarket, consultadas a las 14:26 UTC.
- **Secundario (grado C):** la aprobación del texto de la CFTC en el Comité de Agricultura del Senado (Digital Commodity Intermediaries Act, 12-11 en línea partidista, finales de ene-2026; [ABA Banking Journal](https://bankingjournal.aba.com/2026/01/senate-ag-committee-advances-digital-commodity-bill)). No se leyó ese texto.

## 2. Estado legislativo [H, grado A salvo que se diga]

| Fecha | Hecho | Fuente |
|---|---|---|
| 17-jul-2025 | La Cámara aprueba H.R. 3633 ("CLARITY Act of 2025"). | EH, GPO |
| 18-sep-2025 | El Senado lo recibe y lo turna a Banking. | RS, GPO |
| ene-2026 | Agricultura del Senado aprueba su texto de la CFTC, 12-11 (grado C). | ABA |
| 1-jun-2026 | Banking reporta H.R. 3633 con un sustituto completo, Calendar No. 423. | RS, GPO |
| 15-sep-2026, 14:19 | **Cloture sobre la moción para proceder: rechazada, 49-50** (requisito 3/5). | Senado, voto 00234 |
| 30-sep → 16-oct | Ninguna votación nominal posterior sobre H.R. 3633; la última votación del Senado es del 30-sep. | Senado, índice |
| 3-ene-2027 | Fin del 119.º Congreso: el proyecto muere si no se promulga (faltan **79 días**). | 20.ª Enmienda |

**Desglose del voto 00234 (contado del XML):** 49 republicanos a favor; en contra 44 demócratas, 2 independientes y **4 republicanos (Collins, Hawley, Moran y Tillis)**; 1 demócrata no votó. Cero votos demócratas a favor. [I, B] El voto en contra de Tillis encaja con el procedimiento para presentar una moción de reconsideración (hay que votar con el lado ganador); la prensa lo reporta así, pero el índice del Senado no registra ninguna votación sobre esa moción.

## 3. Qué dice el texto reportado en el Senado [H, A]

**Título corto y armado.** El sustituto se llama "Digital Asset Market Clarity Act". El título I se cita como "Lummis-Gillibrand Responsible Financial Innovation Act of 2026". Tiene 9 títulos: valores (I), finanzas ilícitas (II), DeFi (III), banca (IV), sandbox (V), desarrolladores (VI), quiebra (VII), protección al cliente (VIII) y otros (IX).

**División SEC/CFTC.** Es la diferencia de fondo con la versión de la Cámara:
- **Cámara (EH):** trae los dos lados en un solo texto. El título III es la SEC; el título IV, "Registration for digital commodity intermediaries at the Commodity Futures Trading Commission", da a la CFTC la jurisdicción sobre transacciones de *digital commodities* y el registro de exchanges, brokers y dealers (secs. 401-406). La sec. 205 trae la prueba de "mature blockchain system".
- **Senado (RS, Banking):** solo trae el lado de valores. Crea el **"ancillary asset"** en una nueva sec. 4B de la Securities Act de 1933: un *network token* "cuyo valor depende de los esfuerzos empresariales o de gestión" de su originador, con exención de registro y obligaciones de divulgación. **No** trae el registro de exchanges de la CFTC, aunque lo da por hecho: la sec. 201 aplica la Ley de Secreto Bancario a "any digital commodity exchange registered, or required to register, under that Act". [I, B] El lado de la CFTC vive en el texto de Agricultura y habría que fusionarlo en el pleno; eso no se ha hecho en ninguna votación registrada.
- **Sec. 105(b)(2) del Senado, la "cláusula ETP" [H, A]:** un *network token* **no es ancillary asset ni valor** si el 1-ene-2026 era el activo principal de un ETP listado en una bolsa nacional y no registrado bajo la Investment Company Act. [I, C] En esa fecha cumplían al menos BTC y ETH; muy probablemente también SOL, XRP, LTC, HBAR, DOGE y LINK, por los lanzamientos de oct-dic-2025 que recuerdo y que **no verifiqué hoy**.

**Rendimiento sobre stablecoins (sec. 404 del Senado) [H, A].**
- Prohíbe a todo "covered party" (cualquier proveedor de servicios de activos digitales y sus afiliadas, **excepto** el emisor permitido) pagar "directa o indirectamente" interés o rendimiento a un "restricted recipient" (cliente que es persona de EUA), en dos casos: (A) solo por tener la stablecoin, o (B) sobre el saldo, de forma "económica o funcionalmente equivalente" al interés de un depósito bancario.
- **Excepción:** las recompensas por "actividades o transacciones de buena fe" que no equivalgan a un depósito. La SEC, la CFTC y el Tesoro deben definir esa frontera por regla conjunta en un año, con una lista no exhaustiva de recompensas permitidas.
- La versión de la Cámara **no** trae esta prohibición: 0 apariciones de "interest or yield" en el EH.
- **Comparación [H, A]:**

| Norma | A quién prohíbe pagar rendimiento |
|---|---|
| GENIUS 4(a)(11) | Solo al emisor |
| MiCA 50(2) | Al emisor y a los CASP; prohíbe todo beneficio ligado al tiempo de tenencia |
| CLARITY Senado 404 | A los exchanges y sus afiliadas, frente a clientes de EUA; permite recompensas por actividad |

  [I] El Senado quedó a medio camino entre GENIUS y MiCA: el punto de "actividad de buena fe" es lo que los bancos ven como resquicio y los exchanges como mínimo aceptable.

**Otros puntos con efecto en el inversionista [H, A].**
- **Sec. 605 ("Keep Your Coins Act"):** ninguna agencia federal puede prohibir ni restringir la autocustodia en un *self-hosted wallet* para fines lícitos.
- **Sec. 906 (vigencia):** **360 días** después de la promulgación. Si una disposición requiere regla, rige la fecha más tardía entre esos 360 días y 60 días después de que la regla final se publique en el Federal Register.

## 4. Ejercicio numérico (Python, verificado dos veces)

Script fuera del repositorio: `scratchpad/clarity_calc.py`, que lee el XML del voto 00234.
- **Método A:** conteo por partido de cada `<member>`.
- **Método B:** conteo literal de las etiquetas `<vote_cast>`.
- Los dos dan 49 y 50.

Salida real:

```
A) yeas 49 nays 50 R 53 D+I 47 faltan 11 D/I necesarios si votan los 53 R: 7
   chequeo 49 50
B) dias hasta fin del 119.o Congreso 79
   firma 2026-12-18 vigencia general 2027-12-13 plazo regla 404 2027-12-18 vigencia 404 minima 2028-02-16
   firma 2027-06-30 vigencia general 2028-06-24 plazo regla 404 2028-06-30 vigencia 404 minima 2028-08-29
C) Kalshi KXCRYPTOSTRUCTURE, medios y riesgo condicional por tramo
   2026-12-01 medio 0.030 cond. tramo 0.030 mensual 0.0200
   2027-01-01 medio 0.059 cond. tramo 0.030 mensual 0.0294
   2027-04-01 medio 0.080 cond. tramo 0.022 mensual 0.0076
   2027-07-01 medio 0.125 cond. tramo 0.049 mensual 0.0166
   2027-10-01 medio 0.135 cond. tramo 0.011 mensual 0.0038
   2028-01-01 medio 0.295 cond. tramo 0.185 mensual 0.0654
D) P0019 Brier si 0 nuestro 0.0016 mercado 0.0035
D) P0019 Brier si 1 nuestro 0.9216 mercado 0.8855
```

**Lectura:**
- **(A)** Con los 53 republicanos alineados, hacen falta **7 votos demócratas o independientes**. El 15-sep hubo cero.
- **(B)** Aun firmada en el *lame duck*, la ley no regiría antes de **dic-2027**. La prohibición de rendimiento iría a **feb-2028** si la regla conjunta se publica justo al vencer su plazo de un año (la línea "vigencia 404 mínima" supone ese caso; con una regla temprana, rige a los 360 días). **Para 2026-2027 no hay efecto operativo directo**: el canal es solo de expectativas.
- **(C)** La curva de Kalshi es poco coherente. Pone 1.1% en el tramo jul-oct-2027 y luego 18.5% en oct-2027 → ene-2028. Es otra pregunta ("legislation", serie 27JAN) con poca liquidez. **No uso el tramo de 2028** como señal.
- **(D)** P0019 (0.04) está por debajo del medio de Kalshi (5.9%; bid 5.0, ask 6.8, último 5.1) y de Polymarket ("H.R. 3633 signed into law in 2026", 6.05%). Si no se firma, ganamos 0.0019 de Brier frente al mercado; si se firma, perdemos 0.036.

## 5. Qué cambia para invertir

- **[I] P0019 se mantiene en 0.04.** Hoy hay evidencia primaria de que:
  - no hubo ninguna votación nominal desde el 15-sep;
  - faltan 7 votos de la oposición;
  - quedan 79 días calendario, con elecciones el 3-nov en medio;
  - además, el texto del Senado todavía no está fusionado con el de Agricultura.

  El mercado (5-6%) paga una pequeña prima por un *lame duck* sorpresa. No veo base para moverme hacia él ni para bajar más. No se edita la fila (es de `analista-geopolitico`); queda como nota.
- **[I] Para `arena-claude-binance` (desde México):** sin efecto a 30 días. La prohibición de la sec. 404 aplica a clientes que son personas de EUA y no regiría antes de 2028.
- **[I] Para la cuenta GBM (ETP de BTC/ETH en el SIC):** la cláusula 105(b)(2) blinda a BTC y ETH como "no valores". El riesgo regulatorio de los ETP que podemos comprar es bajo con o sin CLARITY. Lo que la ley movería es el apetito por altcoins con ETP y por los exchanges de EUA (COIN), no a BTC directamente.
- **[I, C] Canal de precio:** una aprobación sorpresa sería un catalizador positivo de corto plazo para el sector (exchanges y altcoins con ETP más que BTC). Que la ley muera el 3-ene-2027 ya está casi todo en precio (mercados al ~94% de "no").

## 6. Contrapuntos y límites

- **Sin congress.gov** (403/429), así que no hay "All Actions". Una moción por consentimiento unánime, una nueva moción de cloture **presentada** (no votada) o un acuerdo de calendario no aparecerían en el índice de votaciones. Grado B en "sin movimiento desde el 15-sep".
- El texto de Agricultura (CFTC) **no se leyó**; la descripción del lado de la CFTC del Senado es grado C.
- La lista de tokens amparados por la sec. 105(b)(2), más allá de BTC y ETH, es de memoria (grado C).
- El sustituto de Banking es el texto **reportado**. Lo que se vote en el pleno sería probablemente otro sustituto (Banking más Agricultura más ajustes de ética y DeFi). La disputa de ética que reporta la prensa (DLA Piper, defirate) **no** se verificó en el texto.

## 7. Autoexamen (5 preguntas, respuestas en la ficha)

1. ¿Cuál fue el resultado y el umbral del voto 00234? (Cloture sobre la moción para proceder, rechazada 49-50; requería 3/5.)
2. ¿Qué título de la versión de la Cámara da a la CFTC el registro de exchanges de *digital commodities*? (Título IV, secs. 401-406.)
3. ¿Qué es un "ancillary asset" en el texto del Senado? (Un *network token* cuyo valor depende de los esfuerzos empresariales o de gestión de su originador; nueva sec. 4B de la Securities Act de 1933.)
4. ¿A quién prohíbe pagar rendimiento sobre stablecoins la sec. 404 del Senado y qué excepción tiene? (A los proveedores de servicios de activos digitales y sus afiliadas, frente a clientes de EUA; excepto las recompensas por actividad o transacción de buena fe que no equivalgan a un depósito.)
5. ¿Cuándo regiría la ley si se firmara el 18-dic-2026? (13-dic-2027 en general; la sec. 404, el 16-feb-2028 si la regla sale justo al vencer el plazo.)

## 8. Estado y pendientes

- **Estado:** "Documentado con comprobación" para el texto de CLARITY (EH y RS de GPO) y el voto 00234 (XML del Senado, dos métodos). La fila de regulación de la Frontera queda **completa en sus cuatro piezas** (GENIUS, MiCA, Circular 4/2019 y CLARITY).
- **Pendientes:**
  - (a) leer el texto de Agricultura del Senado (Digital Commodity Intermediaries Act);
  - (b) reintentar congress.gov "All Actions" (sin clave, o con otra red);
  - (c) verificar la lista de ETP vigentes al 1-ene-2026 (formularios 8-A y 19b-4 en EDGAR) para la sec. 105(b)(2);
  - (d) revisar el índice de votaciones del Senado al volver del receso (P0134);
  - (e) los pendientes heredados: normas técnicas de la EBA, ANPRM de la CFTC 2026-20888, Federal Register (P0117) y la CNBV para IFPE.

**Grado global:**
- **A:** texto de la ley (GPO) y voto (Senado).
- **B:** "sin movimiento desde el 15-sep" (solo votaciones nominales) y la lectura de la fusión pendiente con Agricultura.
- **C:** los tokens amparados por la cláusula ETP más allá de BTC/ETH, y el canal de precio.
