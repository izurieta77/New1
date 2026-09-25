# 32 · 2026 Crypto Crime Report (Chainalysis)

- **Estado:** estudiado. **Acceso:** sección (capítulos principales íntegros en el blog; el PDF no).
- **Grupo:** G4, Riesgo, fraude, hackeos y seguridad. **Autor de la ficha:** `analista-cripto`, 25-sep-2026.
- **Etiquetas:** [H] hecho con fuente · [I] inferencia o cálculo propio · [O] opinión.
- **Cálculos:** `scratchpad/g4/calc/cifras_g4.py` (fuera del repositorio; las fórmulas van en el texto).

## 1. Ficha

| Campo | Valor |
|---|---|
| Año | Capítulos publicados del 18-dic-2025 al 5-mar-2026, más actualizaciones de 2026. Los datos son de 2025. |
| Autor | Chainalysis Team, empresa privada de análisis de blockchain |
| Tipo | Reporte anual publicado por capítulos: el blog es gratis y el PDF pide registro |
| Nivel | Principiante-Intermedio |
| Costo | Gratis. El PDF se descarga con un formulario. |
| Idioma | Inglés. La página del reporte ofrece también coreano, japonés y chino simplificado. |
| URL | https://www.chainalysis.com/reports/crypto-crime-2026/ |
| Conflictos de interés | **Altos.** Chainalysis vende software de cumplimiento e investigación a gobiernos, exchanges y bancos (Reactor, KYT). Varios capítulos cierran promoviendo sus productos: Hexagate, "ahora parte de Chainalysis", en los casos de Venus, Drift y KelpDAO; Alterya en el de estafas. Le conviene que el problema se vea grande y sus herramientas, eficaces. La metodología es propietaria y no se puede replicar desde fuera. |

## 2. Acceso real (25-sep-2026)

**Leí íntegro el texto de estos capítulos del blog:**

| Capítulo | Fecha | URL |
|---|---|---|
| Introducción: volumen ilícito | 8-ene-2026 | https://www.chainalysis.com/blog/2026-crypto-crime-report-introduction/ |
| Robos y hackeos (incluye Bybit y Corea del Norte) | 18-dic-2025 | https://www.chainalysis.com/blog/crypto-hacking-stolen-funds-2026/ |
| Estafas | 13-ene-2026 | https://www.chainalysis.com/blog/crypto-scams-2026/ |
| Lavado: redes chinas (CMLN) | 27-ene-2026 | https://www.chainalysis.com/blog/2026-crypto-money-laundering/ |
| Sanciones | 5-mar-2026 | https://www.chainalysis.com/blog/crypto-sanctions-2026/ |

**Piezas posteriores relacionadas que también leí:**
- Drift, 9-abr-2026: https://www.chainalysis.com/blog/lessons-from-the-drift-hack/
- KelpDAO, 23-abr-2026: https://www.chainalysis.com/blog/kelpdao-bridge-exploit-april-2026/
- Ataques con violencia física, 6-ago-2026: https://www.chainalysis.com/blog/violent-crypto-wrench-attacks-2026/

**No leí:**
- el PDF completo;
- los capítulos de ransomware, darknet, trata de personas e infraestructura.

**Contraste externo:** TRM Labs, vía CoinDesk (27-ene-2026).

## 3. Lo esencial

**Volumen ilícito**
1. [H] En 2025, las direcciones ilícitas recibieron **al menos US$154 mil millones**, +162% anual. Es una cota inferior (Introducción).
2. [H] El salto lo explica un **+694% en el valor recibido por entidades sancionadas: US$104 mil millones** (capítulo de sanciones). [I] Son el 67.5% del total. Sin sancionados, el ilícito habría pasado de ~US$44 a ~US$50 mil millones (+13%). Cálculo propio: 2024 revisado (57.2) menos sancionados implícitos de 2024 (104/7.94 = 13.1).
3. [H] La participación ilícita "aumentó ligeramente pero sigue **debajo de 1%**". El denominador son las entradas a servicios conocidos, sin transferencias internas (Introducción, nota 2).
4. [H] **Las cifras se revisan al alza.** 2024 se reportó en US$40.9 mil millones y hoy se estima en US$57.2 mil millones (Introducción, nota 1). [I] Son +40% en un año, así que las comparaciones interanuales son frágiles.
5. [H] **Las stablecoins son el 84% del volumen ilícito** (Introducción).

**Robos y hackeos**

6. [H] De enero a inicios de diciembre de 2025 se robaron **más de US$3.4 mil millones**. **Bybit, en febrero de 2025, aportó US$1.5 mil millones** (capítulo de robos). [I] Bybit sola es el 44% del año.
7. [H] **Corea del Norte robó al menos US$2.02 mil millones**: +51%, o US$681 millones más que en 2024.
   - Hizo un récord de **76% de los compromisos de servicios**, con **74% menos ataques conocidos**.
   - Su acumulado estimado llega a US$6.75 mil millones.
8. [H] **Las pérdidas se concentran en las colas.** Los 3 mayores hackeos son el 69% de las pérdidas de servicios, y el mayor supera por primera vez **1,000 veces** la mediana.
9. [H] **Los servicios centralizados pierden por ataques a la "infraestructura de llaves privadas y procesos de firma"**, que pueden "eludir controles de cold wallet". Explicaron el 88% de las pérdidas del 1T-2025.
   - Corea del Norte infiltra **trabajadores de TI** en exchanges y custodios, y ahora también se hace pasar por reclutadores e inversionistas.
10. [H] **Carteras personales:** 158,000 incidentes y al menos 80,000 víctimas.
    - El monto bajó a **US$713 millones**, desde US$1.5 mil millones en 2024.
    - Son el 20% del valor robado; serían el 37% sin Bybit.
    - Ethereum y Tron tienen las tasas más altas por cada 100 mil carteras.
11. [H] **DeFi:** el TVL se recuperó, pero las pérdidas por hackeo siguieron bajas en 2024-2025. En el caso Venus (sep-2025):
    - el monitoreo alertó 18 horas antes;
    - el protocolo se pausó en 20 minutos;
    - los fondos se recuperaron completos en 12 horas.
12. [H] **Así lava Corea del Norte** (ciclo de unos 45 días en 3 olas):
    - más de 60% del volumen se mueve en transferencias menores a US$500 mil;
    - prefiere servicios de lavado en chino, puentes y mezcladores;
    - los exchanges centralizados reciben fondos en la ola 2 (días 6-10, +32%) y en la ola 3 (días 20-45, +50%).

**Estafas**

13. [H] Las estafas recibieron **al menos US$14 mil millones on-chain** en 2025, con una proyección de más de US$17 mil millones (capítulo de estafas).
    - El pago promedio subió de US$782 a **US$2,764** (+253%).
    - La **suplantación de identidad creció 1,400%**.
    - Las estafas con vínculo on-chain a proveedores de IA sacan US$3.2 millones por operación, contra US$719 mil del resto (4.5 veces).
14. [H] **Caso de exchange: suplantación del soporte de Coinbase.**
    - Un exagente de soporte en India fue arrestado por presuntos sobornos. La filtración expuso datos de **casi 70,000 clientes** (capítulo de estafas).
    - Coinbase lo confirmó en su 8-K del 14-may-2025. Estimó un costo de US$180-400 millones ([SEC EDGAR](https://www.sec.gov/Archives/edgar/data/1679788/000167978825000094/coin-20250514.htm)).

**Lavado**

15. [H] **Redes chinas de lavado (CMLN):**
    - procesaron US$16.1 mil millones en 2025, unos US$44 millones diarios;
    - son ~20% del lavado conocido;
    - el lavado on-chain total pasó de US$10 mil millones (2020) a más de US$82 mil millones (2025).
    - [H] El uso de exchanges centralizados para lavar va a la baja, "posiblemente porque los exchanges pueden congelar fondos" (capítulo de lavado).

**Sanciones**

16. [H] **A7A5**, un token respaldado en rublos, movió **US$93.3 mil millones** en menos de un año.
    - Grinex, sucesor de Garantex, procesó ≥US$4.76 mil millones.
    - Las redes ligadas a la Guardia Revolucionaria iraní (IRGC) recibieron más de US$3 mil millones, >50% del valor recibido por entidades iraníes en el 4T-2025.
    - **Nobitex** fue hackeado por más de US$90 millones en junio de 2025 (capítulo de sanciones).

**Aplicación de la ley**

17. [H] **Reino Unido:** incautación de más de 61,000 BTC y sentencia de 11 años y 8 meses (nov-2025) por el lavado de un fraude en China (2014-2017).
    - [H] **EUA:** cargos contra el presidente de Prince Group. Es **acusado**, no sentenciado en EUA; lo arrestaron en Camboya en enero de 2026 y lo extraditaron a China.
    - Hubo decomisos por más de US$15 mil millones y OFAC designó 146 objetivos (capítulo de estafas).

**Ataques con violencia física**

18. [H] **"Wrench attacks":** récord de **US$58 millones** en 2025 y más de US$30 millones en el 1S-2026. El intento de extracción sumó US$180 millones en 2025.
    - Tasa de éxito: 26% en 2026, contra 49% en 2025.
    - Francia es el foco, y **una filtración de registros de la agencia tributaria francesa amplió el universo de víctimas**.
    - Recomendaciones:
      - no revelar tenencias;
      - usar custodia segura;
      - no ligar la actividad on-chain a la identidad;
      - tomar medidas de seguridad física (actualización del 6-ago-2026).

**Juicio y lectura**

19. [O] Chainalysis sostiene que la transparencia de blockchain es una "ventaja estructural" para los investigadores (capítulo de sanciones).
20. [I] **Para quien invierte vía exchange, en 2025 el riesgo de hackeo dominante no fue el código DeFi**, sino la operación de servicios centralizados: llaves, firmas, personas y proveedores. El "blind signing", o firma a ciegas, es el patrón de Bybit (ver ficha 22).

## 4. Qué cambia para invertir

### Riesgo de exchange (lección de FTX aplicada a Binance)
- [I] **FTX fue fraude interno y no hackeo, y este reporte no lo cubre** (ver ficha 17).
  - Lo que aporta es otro riesgo de contraparte: **los exchanges grandes son el blanco preferente** de Corea del Norte (76% de los compromisos de servicios).
  - Sus pérdidas son raras pero enormes.
  - La pregunta clave deja de ser "¿es solvente?" y pasa a ser "¿aguanta un hackeo del tamaño de Bybit sin congelar retiros?".
- [H] **Contraejemplo útil: Bybit.**
  - Perdió US$1.46 mil millones el 21-feb-2025 (401,347 ETH más derivados de ETH).
  - Procesó el 99.994% de más de 350,000 solicitudes de retiro en 10 horas.
  - En dos días consiguió US$1.23 mil millones en ETH con préstamos puente, depósitos y compras OTC.
  - Fuente: [cronología oficial de Bybit](https://www.bybit.com/en/learn/this-week-in-bybit/bybit-security-incident-timeline).
- [H] **Para Binance, el tema del reporte que importa es sanciones.**
  - Chainalysis documenta US$104 mil millones hacia sancionados y el peso de Irán.
  - Según Bloomberg (22-sep-2026, vía [CoinDesk](https://www.coindesk.com/policy/2026/09/22/binance-probed-by-u-s-federal-prosecutors-for-sanctions-violations-bloomberg)), la fiscalía de Manhattan investiga si Binance permitió operaciones que violan sanciones a Irán. **No hay cargos.** Binance dice tener "tolerancia cero".
- **Qué vigilar:**
  - el comunicado y los retiros del exchange en las primeras 24 horas de un incidente;
  - si la pérdida cabe en su fondo de protección (ver la lista de señales).

### Riesgo de stablecoin
- [H] El 84% del ilícito ocurre en stablecoins. Por eso los emisores **congelan**: Circle y Tether bloquearon ~US$318 mil del hackeo a Bitget el 25-sep-2026 ([CoinDesk](https://www.coindesk.com/markets/2026/09/25/circle-and-tether-step-in-to-freeze-hacker-wallet-after-massive-bitget-crypto-heist)).
- [I] Es una protección, pero también un riesgo para fondos legítimos que pasen por direcciones marcadas.
- [I] **Para la cuenta:** la ruta MXN→USDT→BTC deja USDT unos minutos en el exchange. Conviene minimizar ese tiempo y no guardar la reserva en USDT (el comité ya la fijó en MXN).

### Hackeos de exchanges y de puentes
- [H] **Servicios centralizados:** llaves, firmas e infiltración de personal (puntos 9 y 12).
- [H] **Puentes: KelpDAO** (18-abr-2026, ~US$292 millones).
  - No hubo error de contrato. El puente tenía **un solo verificador (1 de 1)** que leía de nodos RPC comprometidos, y eso liberó rsETH contra una quema que nunca ocurrió.
  - Chainalysis lo resume como "cualquier '1 de 1' debe tratarse como riesgo activo".
- [I] **Para quien tiene BTC:** no mantener BTC "envuelto" o puenteado en otras cadenas sin necesidad.

### Autocustodia
- [H] Salir del exchange elimina el riesgo de contraparte, pero **el individuo se vuelve el blanco**:
  - 158,000 incidentes en carteras personales;
  - récord de ataques físicos;
  - la filtración de datos fiscales en Francia muestra que cualquier base KYC filtrada puede volverse una lista de objetivos.
- [I] **Reglas prácticas:**
  - no publicar tenencias;
  - separar la identidad de las direcciones;
  - no aceptar "soporte" entrante;
  - con montos chicos, el riesgo físico es marginal, pero el phishing no.

### Cómo leer una prueba de reservas
- [I] El reporte no trata la prueba de reservas (PoR). Su implicación indirecta: **una PoR es una foto de solvencia**, no de seguridad operativa ni de cumplimiento.
  - No detecta llaves comprometidas, personal infiltrado ni exposición a sanciones.
  - Por eso se complementa con flujos on-chain, estado de retiros y acciones regulatorias.

## 5. Contrapuntos y límites
- **Cotas inferiores que cambian:** 2024 subió 40% en un año. Las cifras de 2025 también subirán.
- **Discrepancias con TRM Labs** ([CoinDesk, 27-ene-2026](https://www.coindesk.com/policy/2026/01/27/criminal-use-of-crypto-spikes-after-years-of-steady-decline-trm-report-says)):

| Concepto | Chainalysis | TRM Labs |
|---|---|---|
| Ilícito 2025 | US$154 mil millones, "<1%" del volumen | US$158 mil millones, 1.2% del volumen |
| A7A5 | US$93.3 mil millones | US$72 mil millones |
| Hackeos 2025 | US$3.4 mil millones (incluye carteras personales) | "casi US$3 mil millones" en ~150 incidentes |

  - Las definiciones y las atribuciones difieren.
- **Nobitex:** Chainalysis da "más de US$90 millones" y ZachXBT, US$81.7 millones (ficha 08).
- **"Ilícito" no significa "fraude contra inversionistas".** Dos tercios son flujos de sancionados (Rusia, Irán), irrelevantes para el riesgo de estafa de un inversionista minorista pero relevantes para el **riesgo regulatorio de los exchanges que los procesan**.
- **Atribución a Corea del Norte:**
  - Chainalysis la hace con análisis propio.
  - Para Bybit, el **FBI la confirmó** (PSA del 26-feb-2025, "TraderTraitor").
  - Para Drift (abr-2026), Chainalysis aclara que la atribución estaba "pendiente".
- **Conflicto comercial:** los casos "resueltos" que se citan (Venus, KelpDAO) destacan herramientas de la propia Chainalysis.

## 6. Autoexamen

**1. ¿Por qué los US$154 mil millones de 2025 no significan que "el crimen cripto se triplicó"?**
- US$104 mil millones (67.5%) son valor recibido por sancionados (+694%), sobre todo por el esquema ruso A7A5.
- Sin ese componente, el ilícito sube ~13%.
- Además es una cota inferior que se revisa al alza: 2024 pasó de 40.9 a 57.2.
- Fuentes: Introducción (8-ene-2026) y capítulo de sanciones (5-mar-2026).

**2. ¿Qué parte del robo de 2025 fue Bybit y qué implica para medir el riesgo de hackeo de un exchange?**
- US$1.5 de 3.4 mil millones, el 44%. Los 3 mayores hackeos suman el 69% de las pérdidas de servicios, y el mayor es más de 1,000 veces la mediana.
- El riesgo es de cola: los promedios anuales engañan y hay que preguntar si el exchange sobrevive a un evento extremo.
- Fuente: capítulo de robos (18-dic-2025).

**3. Según Chainalysis, ¿cuánto dura el ciclo típico de lavado de Corea del Norte y en qué ventanas llegan fondos a exchanges centralizados? ¿Por qué le importa a un exchange?**
- Son ~45 días. Hay entradas en la ola 2 (días 6-10, +32%) y en la ola 3 (días 20-45, +50%).
- Un exchange que no bloquea esas direcciones puede recibir fondos robados, lo que es exposición regulatoria.
- Fuente: capítulo de robos.

**4. ¿Qué pasó en 2025 con el valor robado a carteras personales y qué recomienda Chainalysis contra los ataques físicos?**
- Hubo 158,000 incidentes y 80,000 víctimas, pero el monto bajó a US$713 millones (desde US$1.5 mil millones): más víctimas, montos menores.
- Contra ataques físicos: no revelar tenencias, usar custodia segura, no ligar la identidad a la actividad on-chain y tomar medidas de seguridad física.
- Fuentes: capítulo de robos; ataques físicos (6-ago-2026).

## 7. Grado de evidencia: **B**
- **Por qué no A:**
  - la metodología es propietaria;
  - hay un conflicto comercial explícito;
  - las revisiones son grandes (+40% en 2024);
  - la cifra agregada de "ilícito" mezcla sanciones con fraude.
- **Por qué no C:** es la fuente primaria de sus propias estimaciones, con fechas, notas metodológicas y cotas declaradas. Varios hechos puntuales están corroborados por terceros: el FBI en Bybit, el Tesoro en sanciones y los tribunales en el Reino Unido.
- **Uso:** B para hechos puntuales corroborados. **C para comparaciones interanuales de agregados.**
