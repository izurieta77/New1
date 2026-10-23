# 00 — Inventario normativo verificado y plan de estudio (fase 2 del doctorado fiscal y contable)

> Corte: **23-oct-2026**. Escrito por el agente de inventario (fase 2). El Código Fiscal de la Federación (CFF) lo estudian otros siete agentes; aquí solo se descargó para comparar la huella. Caso de diseño: **persona moral pequeña de servicios con flotilla de vehículos, en el Estado de México, y su dueño persona física**. No hay datos personales del dueño.
>
> **Convenciones.** **A** = dato leído hoy en el documento oficial descargado. **B** = dato leído en el índice oficial, o que combina dos fuentes oficiales. **C** = fuente secundaria (prensa especializada, despachos). **D** = no verificado. "UR" = última reforma que aparece en la portada del PDF. Las páginas son las que cuenta `pypdf` y coinciden con el "1 de N" de la portada, salvo la excepción anotada. Las huellas son **sha256 del archivo descargado**. Cada archivo se bajó **dos veces** (23-oct-2026), en descargas independientes, y las dos huellas coinciden (verificado con `sha256sum`), salvo las páginas HTML del DOF, que el servidor genera de nuevo en cada visita (ver §1.4).
>
> **Dónde están las descargas:** `/tmp/claude-0/-home-user-New1/71a68d03-d176-5c12-820e-5e61b63b431d/scratchpad/leyes/` (subcarpetas `pdf/`, `rmf/`, `risat/`, `cinif/`). Es una carpeta temporal de la sesión, **no del repositorio**. Para reproducir, bájelas de nuevo de la URL y compare el sha256.

---

## 0. Resumen

- **Descargados y con huella: 27 de los 28 ordenamientos pedidos**, más 5 documentos extra útiles para el caso: CFF (para comparar), Reglamento de la LSS en materia de afiliación y recaudación (RACERF), Ley Federal del ISAN, Anexo 1 y Anexo 24 de la RMF, y la versión anticipada de la 4a modificación a la RMF.
- **Falló 1:** el **Código Financiero del Estado de México y Municipios**. Los servidores `legislacion.edomex.gob.mx`, `finanzas.edomex.gob.mx` y `edomex.gob.mx` cortaron la conexión (curl 35, "connection reset") por HTTPS, y el primero respondió **503** por HTTP y por WebFetch. No se usó una copia de terceros. **Impuesto sobre nóminas y tenencia del Edomex: D, no verificados.**
- **Parcial: el Reglamento Interior del SAT (RISAT).** Diputados no lo publica en su lista de reglamentos (que solo cubre reglamentos de leyes). Se bajó del DOF el **texto original (DOF 24-08-2015)** y el **decreto de reforma de DOF 21-12-2021**. No hay texto compilado oficial a la mano, y puede haber reformas que no se encontraron (D).
- **El "Anexo 1-A" ya no existe en la RMF 2026 [A].** La regla 1.4, fracción II de la RMF 2026 dice: "Anexo 2, que contiene los trámites fiscales". La regla 1.3 dice que en el Anexo 2 están "las fichas de trámites fiscales". Se descargó el **Anexo 2**. El cap. 30 ya lo había anotado.
- **NIF 2026:** el listado oficial de CINIF pide iniciar sesión (redirige a `usuario_login.php?info=DENIED`), y el libro es de paga. La lista del §4.1 se armó con conocimiento previo, y se marcan con A los dos únicos datos leídos hoy en cinif.org.mx.

---

## 1. Inventario

### 1.1 Leyes federales (fuente: Cámara de Diputados, `https://www.diputados.gob.mx/LeyesBiblio/`)

La fecha "Índice" sale de la tabla de leyes vigentes de Diputados (`index.htm`, leída hoy). Cuando no coincide con la portada del PDF es porque el índice registra una **actualización de cantidades** y no una reforma de la ley (B).

| # | Ordenamiento | URL (relativa a `LeyesBiblio/`) | UR en el documento | Índice Diputados | Págs. | sha256 | Estado |
|---|---|---|---|---|---|---|---|
| L1 | Ley del Impuesto sobre la Renta (LISR) | `pdf/LISR.pdf` | DOF 01-04-2024 | 01/04/2024 | 313 | `803c2875c09c751c1966b8eb4dca99f460b237da4ef67ee04b4fa325d8c2f786` | OK |
| L2 | Ley del IVA (LIVA) | `pdf/LIVA.pdf` | DOF 12-11-2021 | 12/11/2021 | 128 | `f2b5b1770441a6a4e48f3ade408f9ff7a3e9c81bd5d529e52484f49e4a8e91a6` | OK |
| L3 | Ley del IEPS (LIEPS) | `pdf/LIEPS.pdf` | DOF 07-11-2025 (cuotas actualizadas por Acuerdo DOF 22-12-2025) | 22/12/2025 | 165 | `32639ede8448f91e6ddde556d4b8bceaf349b904bc21631f06e1c8a7a3d416f4` | OK |
| L4 | Ley Federal de Derechos (LFD) | `pdf/LFD.pdf` | DOF 07-11-2025 (cantidades actualizadas por RMF DOF 28-12-2025) | 28/12/2025 | 565 | `64b08a1ff8e5c71759acf550cf9c8df7eb343ea679a2c2663d0eef3db19f10df` | OK |
| L5 | Ley de Ingresos de la Federación 2026 (LIF 2026) | `pdf/LIF_2026.pdf` | Nueva ley DOF 07-11-2025, vigente desde 01-01-2026, sin reformas | — | 47 | `a305ca23bba43cddf2275067af29bb0ba35def7aedbbb0d3fc4557da9067a82c` | OK |
| L6 | Ley Federal de los Derechos del Contribuyente (LFDC) | `pdf/LFDC.pdf` | Nueva ley DOF 23-06-2005, sin reformas anotadas | — | 7 | `70f871ee9f8791063f9da9df9eab93b68efc1f2878f8024299bb5cd93b238658` | OK |
| L7 | Ley Federal de Procedimiento Contencioso Administrativo (LFPCA) | `pdf/LFPCA.pdf` | DOF 09-06-2026 | 09/06/2026 | 80 | `d2a25adcb45f622bbbf2a4e58f1139fb5236961fe86de3dd9ad9de2dfa21d54e` | OK |
| L8 | Ley Orgánica del Tribunal Federal de Justicia Administrativa (LOTFJA) | `pdf/LOTFJA.pdf` | DOF 16-10-2025 | — | 40 | `b32c33fa4ed071dc8bea1ad69ce8510cdb05016967e9e4fcb60f10c6f2216628` | OK |
| L9 | Ley Aduanera | `pdf/LAdua.pdf` | DOF 19-11-2025 (cantidades actualizadas por RGCE DOF 27-12-2025) | 27/12/2025 | 220 | `43927095d22ff7bc7780e78132d2160b5050b5f76026b539daec32be09d7341d` | OK |
| L10 | Ley de los Impuestos Generales de Importación y de Exportación (LIGIE) | `pdf/LIGIE_2022.pdf` | Nueva ley DOF 07-06-2022; UR DOF 29-12-2025; fracciones de la tarifa modificadas por decreto DOF 13-10-2026 | 13/10/2026 ("nueva modificación") | 894 | `955510d7ea82cf42d18c72e3146f999af254c0fda5eda3f12a1fd1c10e9864ce` | OK. Es la versión vigente: la de 2022 sustituyó a la de 2020 |
| L11 | Ley de Coordinación Fiscal (LCF) | `pdf/LCF.pdf` | DOF 03-01-2024 | 03/01/2024 | 98 | `5c89d48167a4e1170c69e0b1e0294260b806a30d861275d8dca09b0334cd09d4` | OK |
| L12 | Ley del Servicio de Administración Tributaria (LSAT) | `pdf/93_041218.pdf` | DOF 04-12-2018 | 04/12/2018 | 29 | `ba54c4384528c6b47fbb3f641cb57dd089a9f1770306b45776ad1711eaca21d5` | OK. `pdf/LSAT.pdf` da 404; el índice enlaza `93_041218.pdf` |
| L13 | Ley Federal de Presupuesto y Responsabilidad Hacendaria (LFPRH), solo referencia | `pdf/LFPRH.pdf` | DOF 09-04-2026 | 09/04/2026 | 125 | `ce45c7c0c4e9099691e6e24bd2456d0b6f71f91ab27eedd5c4f2190b66d47741` | OK |
| L14 | Ley del Seguro Social (LSS) | `pdf/LSS.pdf` | DOF 15-01-2026 | 15/01/2026 | 181 | `8a28a16e1dce1f8e666f4cce5ed19745bc912b2ab1ca49787d5d4bef229398ed` | OK |
| L15 | Ley del INFONAVIT | `pdf/LIFNVT.pdf` | DOF 21-02-2025 | 21/02/2025 | 93 | `9ee6e5ef336dee5700726bd3c570d24f91fc458136e298ae2e3806bd12217912` | OK |
| L16 | Ley Federal para la Prevención e Identificación de Operaciones con Recursos de Procedencia Ilícita (LFPIORPI) | `pdf/LFPIORPI.pdf` | DOF 16-07-2025 | 16/07/2025 | 39 | `2e35228bd3100a3a137f313359833c4836f2b4b6d4e52e1ce4fe58a970cd768f` | OK |
| L17 | Ley de Amparo | `pdf/LAmp.pdf` | DOF 16-10-2025 | 16/10/2025 | 119 | `05560493ac2b17b9e77eeb9741843176ee0fde76f05e75f853465b13621be78d` | OK |
| L18 | Ley Orgánica de la Procuraduría de la Defensa del Contribuyente (LOPRODECON) | `pdf/LOPDC.pdf` | DOF 11-05-2022 | — | 19 | `7dc8f2201fdeb8039371254e3b2606c158f4cd480e29ce074a65eb375a19475c` | OK. **Huella distinta de la del cap. 29** (ver §1.4) |
| L19 | Código Penal Federal (CPF), solo referencia | `pdf/CPF.pdf` | DOF 13-03-2026 | 13/03/2026 | 353 | `a2d80c4383c5fbc8453cf290c19b7853eb0a5a05d1e366572da384edfafda88c` | OK |
| L20 | Ley Federal del Trabajo (LFT), para la PTU | `pdf/LFT.pdf` | DOF 14-05-2026 | 14/05/2026 | 457 | `12f09393a1951a91c3f57f579bf611b034edf1a5f78cdbfb828e23ff3a9acbf7` | OK |
| X1 | *Comparación:* Código Fiscal de la Federación | `pdf/CFF.pdf` | DOF 09-04-2026 | — | 377 | `be7427b20d3552775ab42018f8f87578078770095bf8cf46322c25e36ee3aa7d` | OK; misma huella que en el cap. 29 |
| X2 | *Extra (flotilla):* Ley Federal del Impuesto sobre Automóviles Nuevos | `pdf/LFISAN.pdf` | DOF 12-11-2021 | — | 44 | `ef658aa6a3b15e99a4d19edaa6713598a37523f4179ae69a4462bcb8ca870eb1` | OK |

### 1.2 Reglamentos (fuente: `https://www.diputados.gob.mx/LeyesBiblio/regley/`, salvo el RISAT, que viene de `https://dof.gob.mx/`)

| # | Ordenamiento | URL | UR en el documento | Índice `regla.htm` | Págs. | sha256 | Estado |
|---|---|---|---|---|---|---|---|
| R1 | Reglamento del CFF (RCFF) | `regley/Reg_CFF.pdf` | Nuevo reglamento DOF 02-04-2014, sin reformas anotadas | 02/04/2014 | 40 | `649a06c9d35578dcf2626ce7961b8eca08e62c7fe97424ab97fce2c92cde4248` | OK |
| R2 | Reglamento de la LISR (RLISR) | `regley/Reg_LISR_060516.pdf` | Original DOF 08-10-2015; UR DOF 06-05-2016 | igual | 93 | `0538fd2fa3da9705370350b1e25a1656cc681d2c489545334079e1b35360d6e3` | OK |
| R3 | Reglamento de la LIVA (RLIVA) | `regley/Reg_LIVA_250914.pdf` | Original DOF 04-12-2006; UR DOF 25-09-2014 | igual | 16 | `4f46c1f92fb5682281a7679836e517de95975786fa5326848a331c9eb946cc5f` | OK |
| R4 | Reglamento de la LIEPS | `regley/Reg_LIEPS.pdf` | Nuevo reglamento DOF 04-12-2006, sin reformas | 04/12/2006 | 4 | `cb15a70b51a87cff0f6d329d5e8a97617d71c955e46da65921037a77a83ca5f4` | OK |
| R5 | Reglamento de la Ley Aduanera | `regley/Reg_LAdua.pdf` | Original DOF 20-04-2015; UR DOF 23-02-2026 (cantidades actualizadas hasta DOF 27-12-2025) | igual | 90 | `bcdfcd9073014aec4aefbacc01c9dd5b1f97f0da0c4556f0f506d20f12d77812` | OK |
| R6a | Reglamento Interior del SAT (RISAT), texto original | `https://dof.gob.mx/nota_detalle.php?codigo=5404927&fecha=24/08/2015` | DOF 24-08-2015 (en vigor a los 90 días naturales, con excepciones; transitorio primero) | no está en `regla.htm` | HTML | `522dc1594072ce0efa25144921d0f7fa33b62fea4e94ce93b9df251dedd89ef4` (primera descarga; no se reproduce, §1.4) | **Parcial** |
| R6b | Decreto que reforma el RISAT (y el de la SHCP, y expide el de la ANAM) | `https://dof.gob.mx/nota_detalle.php?codigo=5639045&fecha=21/12/2021` | DOF 21-12-2021 | — | HTML | `6be94bee99cdc965c7a052df405cd42720ff044266ab9373fde0974c53b28635` (primera descarga) | Parcial. Que el RISAT 2015 sigue vigente lo apoya la RMF 2026, que se funda en el "8 del Reglamento Interior del Servicio de Administración Tributaria" (A). Puede haber otras reformas: D |
| X3 | *Extra (nómina):* Reglamento de la LSS en materia de Afiliación, Clasificación de Empresas, Recaudación y Fiscalización (RACERF) | `regley/Reg_LSS_MACERF.pdf` | UR DOF 15-07-2005 | — | **111** (la portada dice "1 de 113") | `78fb70d213053e46d3e739b9d80bf7da733d80f27446af7d5812fc6de80533c9` | OK. Faltan 2 páginas respecto de la portada o la numeración salta: revisar antes de citar |

### 1.3 Resolución Miscelánea Fiscal 2026 (fuente: SAT, `https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/` + la ruta)

| # | Documento | Ruta (relativa al minisitio) | Fecha en el documento | Págs. | sha256 |
|---|---|---|---|---|---|
| M1 | RMF 2026 | `documentos2026/rmf/rmf/RMF_2026-DOF-28122025.pdf` | DOF domingo 28-12-2025 | 666 | `6f71ce0cccf430171fe858c5d244b1c321fa68306f962d44ec4977858a52919a` |
| M2 | 1a Resolución de Modificaciones (y Anexos 1, 2, 3, 9, 14, 15, 21, 22 y 29) | `documentos2026/rmf/rmf/1aRM_RMF2026.pdf` | DOF jueves 09-07-2026 (los anexos modificados, DOF 17-07-2026) | 17 | `ff4b0ed8957f4ff5cbb678f8fdd2e4da84b3a4a96d259027ed0d817c255e6e37` |
| M3 | 2a Resolución de Modificaciones y Anexo 2 | `documentos2026/rmf/rmf/2aRM_RMF2026_01102026.pdf` | DOF jueves 01-10-2026, edición vespertina | 2 | `e46db09fcbc46d87259b28a8683fe5a611bde9854a16d271bf35a5217cd9ed5b` |
| M4 | 3a Resolución de Modificaciones y Anexo 7 | `documentos2026/rmf/rmf/3aRM_RMF2026_DOF_02102026.pdf` | DOF viernes 02-10-2026, edición vespertina | 1 | `ad76e833fa529562767539bcf682a4d88d0f22d193ec11100b87826d130ff77b` |
| M5 | Compilado de la RMF con la 1a modificación (no tiene valor legal: lo dice su propia nota) | `documentos2026/rmf/compiladas/Compilado_Primera_Modificacion_a_la-Resolucion_Miscelanea_Fiscal_para_2026.pdf` | Compilado del SAT; no incluye la 2a ni la 3a | 857 | `edd1ae82fe16ba96e79a591d26a29cc3b91e104713d63e2395a7212546da9718` |
| M6 | **Anexo 2, Trámites Fiscales** (sustituye al antiguo Anexo 1-A) | `documentos2026/rmf/anexos/Anexo-2-RMF-2026_DOF-28122025.pdf` | DOF lunes **29**-12-2025, edición vespertina (el nombre del archivo dice 28122025) | 670 | `ea38b1fa101a8fb07a4b913589aad3f0cda85e67345581cbe199fa016a4c7e1d` |
| M7 | Anexo 1, Formas oficiales fiscales | `documentos2026/rmf/anexos/Anexo-1-RMF-2026_DOF-28122025.pdf` | DOF 28-12-2025 | 182 | `acbfb10b4f4dca4493c53a5980916296f13b104ac89b8fbfb5a428a7923425c2` |
| M8 | Compilado del Anexo 1 con la 1a modificación | `documentos2026/rmf/compiladas/Compilado_PrimeraModificacion_Anexo1_RMF2026-17072026.pdf` | compilado al 17-07-2026 | 580 | `95914126797e34567d72049b11e5c077421162d620e92167ede6212ae1f939de` |
| M9 | **Anexo 24, Contabilidad en medios electrónicos** | `documentos2026/rmf/anexos/Anexo_24_RMF2026-13012026.pdf` | DOF martes 13-01-2026 (publicado junto con los Anexos 17, 21, 22, 23, 27, 28 y 30) | 37 | `689d323d0a5fe517c69abf05c246b054445febb865b2da185cbb9079bcc166e2` |
| M10 | 4a Resolución de Modificaciones, **tercera versión anticipada** (portal SAT, regla 1.3; **no publicada en el DOF**) | `documentos2026/rmf/anticipadas/4aRM_RMF2026-Tercera_version_anticipada_22102026.pdf` | 22-10-2026; toca los Anexos 1, 2 y 15 | 5 | `9436089ff14dcabc8c358c03ebf106df21f4aa18c8404b8345ffd494d21586ee` |

**No descargados, pero listados en la página del SAT (A):** Anexos 3 a 30 de la RMF 2026 y sus modificaciones, y la RGCE 2026 con su 1a y 2a modificación. Para el caso importan sobre todo el Anexo 5 (cantidades actualizadas), el Anexo 20 (CFDI) y el Anexo 3 (criterios no vinculativos). Los caps. 30 a 33 ya bajaron o leyeron algunos.

### 1.4 Fallos e incidencias (no se inventa nada)

| Qué | Resultado |
|---|---|
| Código Financiero del Estado de México y Municipios (ISN, tenencia) | **FALLÓ.** Conexión cortada (curl 35) con `legislacion.edomex.gob.mx`, `finanzas.edomex.gob.mx` y `edomex.gob.mx`; HTTP 503 por HTTP y por WebFetch. Volver a intentar desde otra red, o pedir al dueño el PDF del portal del Edomex (y bajar la Gaceta del Gobierno del Edomex con la reforma de 2026). |
| `LeyesBiblio/pdf/LSAT.pdf` | 404. Resuelto con `pdf/93_041218.pdf`, que es el que enlaza el índice. |
| RISAT | Diputados no lo compila. Hay base y una reforma del DOF; falta un texto compilado oficial. Las páginas HTML del DOF cambian de bytes en cada visita (una segunda descarga dio otro sha256, `2577a815…`, para la misma nota de 2015): su huella identifica el archivo guardado, no el documento. |
| Listado de NIF vigentes en cinif.org.mx | Pide sesión (302 a `usuario_login.php?info=DENIED`). El libro NIF 2026 cuesta $500 (no se compró ni se descargó nada de paga). |
| LOPRODECON | El cap. 29 anotó el 6-oct `abd471f5…`; hoy se obtuvo `7dc8f220…` en dos descargas iguales, con la misma UR (DOF 11-05-2022). Diputados pudo haber regenerado el PDF, o el cap. 29 tiene un error. **No se editó el cap. 29**; queda para la conciliación. Las otras seis huellas del cap. 29 (CFF, LFPCA, Amparo, LFDC, LIF 2026, LISR) coinciden byte por byte. |
| RACERF | 111 páginas reales contra "1 de 113" en la portada. |

---

## 2. Qué ya cubre el repositorio (revisados los caps. 11, 27, 29-33 y `doctorados/ESTADO.md`)

| Ordenamiento | Cobertura actual | Dónde | Hueco para el caso |
|---|---|---|---|
| CFF | Capítulo (D2), letra verificada el 6-oct; lo trabajan siete agentes | cap. 29, cap. 33 (materialidad) | — (fuera de este inventario) |
| LISR Título II (PM) | Capítulo, centrado en una **estación de servicio** | cap. 32 | Deducción de **flotilla**: art. 36 fr. II, tope de **$175,000.00** para automóviles (A, p. 62 del PDF); art. 34 fr. VI, **25%** para automóviles, autobuses y camiones de carga (A, p. 60); arrendamiento y combustible; **RESICO PM** (Título VII, Cap. XII, arts. 206 y siguientes, A, p. 249); PTU como deducción; no deducibles |
| LISR Título IV (PF) | Capítulo para el inversionista (SIC, intereses, dividendos) | caps. 11, 27, ficha D8 | Dueño como **socio**: dividendos y CUFIN desde el lado de la PF, salarios y asimilados, préstamos de socios y presunción de dividendos, uso personal de vehículos de la empresa |
| LIVA | Capítulo (D6) | cap. 32 | La tasa de retención por **autotransporte** que el cap. 32 dejó en nv: el RLIVA art. 3 fr. II dice **4%** (A, leído hoy). Falta acreditamiento proporcional en erogaciones parcialmente deducibles (LIVA art. 5 fr. I, A en la letra) y servicios con retención |
| LIEPS | Capítulo, solo combustibles automotrices | cap. 32 | Para una empresa de servicios casi no aplica, salvo en el precio del combustible y en los estímulos de la LIF |
| LIF 2026 | Parcial: art. 20 (estímulos al diésel) y tasas de recargos | caps. 29 y 32 | Estímulo de diésel para **transporte** (art. 20 fr. IV) si la flotilla es de carga o de pasajeros; tasa de retención de intereses |
| LFD | Sin | — | Solo derechos puntuales (por ejemplo placas federales, si las hubiera); prioridad baja |
| LFDC, LFPCA, LOTFJA, Amparo, LOPRODECON | Capítulo de defensa (D3) | cap. 29 §7 | Lo cubren los agentes del CFF y de defensa; aquí solo se agregan las huellas |
| Ley Aduanera, LIGIE, RLA | Menciones | caps. 29-32 | No aplican al caso, salvo que se importen vehículos o refacciones |
| LCF | Sin | — | Solo para entender por qué el Edomex cobra nómina y tenencia (sistema de coordinación). Referencia |
| LSAT y RISAT | Menciones | caps. 29-31 | Competencia de las autoridades que firman los actos (base de nulidad por incompetencia): lo usan los de defensa |
| LFPRH, CPF | Menciones (CPF por delitos fiscales vía CFF) | cap. 29 | Solo referencia |
| LSS, RACERF, Ley del INFONAVIT | **Sin** (menciones en los caps. 32 y 33) | — | **Hueco grande:** cuotas obrero-patronales, prima de riesgo de trabajo (los choferes elevan la siniestralidad), SBC e integración, INFONAVIT 5%, dictamen IMSS, REPSE si hubiera subcontratación |
| LFT (PTU) | Parcial: PTU en el cap. 32 desde la LISR | cap. 32 | Arts. 117 y siguientes LFT (A: art. 117 en la p. 30); topes, plazos, trabajadores con derecho |
| LFPIORPI | Parcial (D9): arts. 17 y 32, umbrales 2026 | ficha 16-oct | **Vehículos:** compraventa de vehículos y prohibición de pagar en efectivo arriba del umbral, que importa al **comprar** la flotilla |
| LFISAN | Sin | — | Al comprar autos nuevos, el ISAN está en el precio (no lo entera el comprador): saber leerlo en la factura |
| RMF 2026 | Leída por partes, regla por regla (2.1.6, 2.6, 2.7, 2.8.1.5-2.8.1.6, 11.7.1) | caps. 30-33 | Reglas de **contabilidad electrónica**, devoluciones y compensación, CFDI de nómina, carta porte (si transportan bienes propios) |
| Anexo 2 (antes 1-A) | Identificado y citado por número de ficha | caps. 30 y 31 | Fichas que tocan al caso: avisos al RFC, devoluciones, contabilidad, e.firma |
| Anexo 24 | **No leído** (cap. 30 §2.6 y trampa 11) | cap. 30 | Leído en parte hoy (A): catálogo de cuentas con **código agrupador del SAT**, balanza de comprobación, pólizas del periodo, auxiliar de folios de comprobantes, auxiliares de cuenta y subcuenta |
| Reglamentos RLISR, RLIVA, RCFF | Marcados nv en los caps. 29 y 32 | — | Ya descargados: se puede cerrar la lista de nv del cap. 32 (coeficiente de utilidad, 4% de autotransporte) |
| Código Financiero del Edomex | **Sin** | — | Descarga fallida: ISN y tenencia **D** |
| NIF | Contabilidad: 0 Comprobada, 1 Capítulo, 9 Parcial, 1 Sin (`ESTADO.md`) | fichas C1, C3, C4, C5, C8, C9 | Para la pyme: C-6 (flotilla), D-3 (PTU diferida), D-4 (impuestos a la utilidad), D-5 (arrendamientos) y la conciliación contable-fiscal: **nada escrito** |

---

## 3. Plan de estudio para el caso (PM pequeña de servicios con flotilla en el Edomex, y su dueño PF)

**Tamaño total del corpus descargado:** unas 7,600 páginas. El estudio útil es mucho menor. Las cifras de "Tamaño" son páginas del PDF que hay que leer completas, sin contar anexos de tarifas.

### 3.1 Las cinco prioridades

1. **P1. LISR de la persona moral aplicada a la flotilla, con su reglamento.** Hay que leer: LISR Título II (arts. 9-89, unas 120 págs.), RESICO PM (arts. 206-215, unas 8 págs.) y RLISR en lo de deducciones e inversiones (unas 40 págs.). Lo primero es decidir el **régimen** (general contra RESICO PM) y la deducción de vehículos (arts. 25, 27, 28, 31-36): tope por automóvil, 25% anual, arrendamiento, combustible pagado por medio electrónico, viáticos y uso personal (no deducible). Ejercicios verificables: depreciación fiscal de una camioneta de $600,000 con y sin tope, coeficiente de utilidad y pagos provisionales, y pérdida en la venta de un vehículo usado.
2. **P2. IVA de la empresa de servicios.** Hay que leer: LIVA completa (128 págs., ya capítulo para gasolinera) y RLIVA (16 págs.). Temas: acreditamiento y su proporción en erogaciones parcialmente deducibles (art. 5 fr. I: el IVA del automóvil sobre el tope), retenciones del art. 1-A (servicios de PF, **autotransporte al 4%**, servicios con retención), saldo a favor, devolución o compensación, DIOT. Ejercicios: IVA acreditable de un auto de $500,000 + IVA con tope de $175,000; declaración mensual con retenciones.
3. **P3. Nómina y seguridad social (el hueco más grande).** Hay que leer: LSS (Título II, régimen obligatorio: cuotas, SBC, riesgos de trabajo; unas 90 págs.), RACERF (prima de riesgo y clasificación; unas 60 págs.), Ley del INFONAVIT (aportaciones, arts. 29-30 y relacionados; unas 15 págs.), LFT (PTU, arts. 117-131; jornada y salario de choferes), LISR Título IV Cap. I (salarios, subsidio) y CFDI de nómina en la RMF. Falta el **ISN del Edomex**, que no se pudo descargar. Ejercicios: integración del SBC de un chofer con prestaciones, cuota patronal mensual, prima de riesgo tras un siniestro y PTU con topes.
4. **P4. Cumplimiento operativo en la RMF 2026 y contabilidad electrónica.** Hay que leer: RMF Título 2 (CFF: RFC, buzón, CFDI, contabilidad, devoluciones; unas 200 págs. del compilado), Anexo 24 (37 págs.), las fichas del Anexo 2 que use el caso (unas 40 fichas) y el Anexo 20 (CFDI, si se descarga). Junto con eso va la **conciliación contable-fiscal** y la **NIF D-4** (§4.3), porque la contabilidad electrónica es la balanza que la autoridad cruza contra declaraciones y CFDI. Ejercicios: mapear un catálogo de 40 cuentas al código agrupador, cuadrar la balanza contra ISR e IVA del mes y cruzar los CFDI emitidos contra los ingresos contables.
5. **P5. El dueño persona física frente a su empresa.** Hay que leer: LISR Título IV (dividendos art. 140 y CUFIN art. 77; salarios; préstamos de socios), CFF (cubierto por los otros agentes), LFPIORPI (compra de vehículos y límites de efectivo) y LFISAN (lectura de la factura). Temas: cómo saca dinero el dueño (sueldo, dividendo, reembolso, préstamo) y su costo fiscal total combinado PM + PF; uso de vehículos de la empresa; operaciones entre partes relacionadas. Ejercicios: costo total de entregar $100,000 netos al dueño por cada vía; dividendo con y sin CUFIN; ISR por dividendo que no viene de CUFIN.

### 3.2 Fases

| Fase | Contenido | Ordenamientos | Tamaño aprox. | Cómo se comprueba |
|---|---|---|---|---|
| F0 (hecha hoy) | Inventario, huellas, cobertura | todos | — | Este archivo; descargar de nuevo y comparar el sha256 |
| F1 | P1 y P2 (ISR e IVA de la PM con flotilla) | LISR II y VII-XII, RLISR, LIVA, RLIVA, LIF 2026 (estímulos y recargos) | ~320 págs. | 10 ejercicios con aserciones en Python (deducción con tope, pagos provisionales, IVA proporcional, retenciones del 4% por autotransporte y de dos terceras partes del IVA, que da 10.6667%, por servicios de PF; RLIVA art. 3 fr. I y II, A) |
| F2 | P3 (nómina y seguridad social) | LSS, RACERF, Ley del INFONAVIT, LFT, LISR IV-I, ISN del Edomex (pendiente de descarga) | ~250 págs. | Cálculo de SBC, cuotas y PTU contra las tablas oficiales del año (UMA 2026 por verificar) |
| F3 | P4 (RMF operativa, contabilidad electrónica, NIF y conciliación) | RMF Título 2 y 3, Anexos 2, 20 y 24, NIF C-6, D-3, D-4, D-5 | ~350 págs. RMF + NIF (de paga) | Conciliación contable-fiscal anual completa de un caso inventado, con impuesto diferido |
| F4 | P5 (dueño PF) | LISR IV, LFPIORPI, LFISAN | ~80 págs. | Matriz de costo total por vía de retiro, con aserciones |
| F5 | Defensa y referencia | LFPCA, LOTFJA, Amparo, LOPRODECON, LFDC, LSAT, RISAT, CPF | ~400 págs. | La coordinan los agentes del CFF; aquí, solo competencia de autoridades y plazos |
| F6 | Fuera del caso (solo mapa) | Ley Aduanera, LIGIE, RLA, LIEPS más allá de combustibles, LFD, LCF, LFPRH | >1,800 págs. | Ficha de una página por ley: qué regula y cuándo le tocaría al negocio |

### 3.3 Reglas del estudio

- Toda cifra en pesos de la LISR, del CFF o de la LFD **se confirma en la RMF 2026 y su Anexo 5** (cantidades actualizadas) antes de usarla.
- Antes de citar un artículo se descarga de nuevo y se compara la huella con la de este inventario. Si cambió, hubo reforma o el PDF se regeneró: se lee la portada.
- La versión anticipada de la 4a modificación (M10) **no es derecho vigente** hasta que salga en el DOF.
- Edomex: nada sobre ISN ni tenencia se da por hecho hasta tener el Código Financiero de fuente oficial.

---

## 4. Plan de contabilidad

### 4.1 NIF vigentes en 2026 (lista por serie; nombres solamente, sin contenido de paga)

**Verificado hoy en cinif.org.mx (A):** el libro electrónico "NIF 2026" reúne las "NIF vigentes al 1.º de enero de 2026, incluyendo las nuevas NIF, las Mejoras a las NIF 2026". Destaca la **nueva NIF B-1, "Bases para la preparación de los estados financieros"**, y la **NIF B-3, "Estado de resultado integral"**. **Fuente secundaria (C, Veritas):** las dos se promulgaron en diciembre de 2025 con **vigencia obligatoria desde el 1-ene-2028** y aplicación anticipada desde el 1-ene-2027. Si es así, en 2026 todavía rigen la B-1 anterior ("Cambios contables y correcciones de errores") y la B-3 anterior. El listado oficial pide sesión: **la lista que sigue es conocimiento previo (D en lo que toca a 2026)** y hay que cotejarla con el índice del libro NIF 2026.

- **Serie A, marco conceptual:** NIF A-1, Marco Conceptual de las Normas de Información Financiera (desde 2023 unifica las antiguas A-1 a A-8).
- **Serie B, estados financieros en su conjunto:** B-1 Cambios contables y correcciones de errores (vigente en 2026; sustituida por la nueva B-1 en 2028, C); B-2 Estado de flujos de efectivo; B-3 Estado de resultado integral; B-4 Estado de cambios en el capital contable; B-5 Información financiera por segmentos; B-6 Estado de situación financiera; B-7 Adquisiciones de negocios; B-8 Estados financieros consolidados o combinados; B-9 Información financiera a fechas intermedias; B-10 Efectos de la inflación; B-11 Disposición de activos de larga duración y operaciones discontinuadas; B-12 Compensación de activos financieros y pasivos financieros; B-13 Hechos posteriores a la fecha de los estados financieros; B-14 Utilidad por acción; B-15 Conversión de monedas extranjeras; B-16 Estados financieros de entidades con propósitos no lucrativos; B-17 Determinación del valor razonable.
- **Serie C, conceptos específicos de los estados financieros:** C-1 Efectivo y equivalentes de efectivo; C-2 Inversión en instrumentos financieros; C-3 Cuentas por cobrar; C-4 Inventarios; C-5 Pagos anticipados; **C-6 Propiedades, planta y equipo** (flotilla); C-7 Inversiones en asociadas, negocios conjuntos y otras inversiones permanentes; C-8 Activos intangibles; C-9 Provisiones, contingencias y compromisos; C-10 Instrumentos financieros derivados y relaciones de cobertura; C-11 Capital contable; C-12 Instrumentos financieros con características de pasivo y de capital; C-13 Partes relacionadas; C-14 Transferencia y baja de activos financieros; C-15 Deterioro en el valor de los activos de larga duración; C-16 Deterioro de instrumentos financieros por cobrar; C-17 Propiedades de inversión; C-18 Obligaciones asociadas con el retiro de propiedades, planta y equipo; C-19 Instrumentos financieros por pagar; C-20 Instrumentos financieros para cobrar principal e interés; C-21 Acuerdos con control conjunto; C-22 Criptomonedas.
- **Serie D, problemas de determinación de resultados:** D-1 Ingresos por contratos con clientes; D-2 Costos por contratos con clientes; **D-3 Beneficios a los empleados** (PTU causada y diferida); **D-4 Impuestos a la utilidad**; **D-5 Arrendamientos** (flotilla arrendada); D-6 Capitalización del resultado integral de financiamiento; D-8 Pagos basados en acciones. (La D-7, contratos de construcción, se eliminó al entrar la D-1 y la D-2; D.)
- **Serie E, actividades especializadas:** E-1 Actividades agropecuarias; E-2 Donativos recibidos u otorgados por entidades con propósitos no lucrativos.
- **Otros pronunciamientos:** Interpretaciones (INIF), Orientaciones (ONIF), Mejoras a las NIF 2026 y las Normas de Información de Sostenibilidad (NIS A-1, NIS B-1; A en cinif.org.mx, libro NIS 2024).

**Orden de estudio para el caso:** A-1 → B-6, B-3 y B-2 (los tres estados) → **C-6** (vida útil contable contra el 25% fiscal) → **D-5** (arrendamiento de unidades: derecho de uso contra renta deducible) → **D-3** (PTU) → **D-4** → C-9 y C-15 → B-13 → C-13 (operaciones con el dueño).

### 4.2 Contabilidad electrónica (Anexo 24 RMF 2026, A en la estructura leída hoy)

- **Base legal:** CFF art. 28 fr. IV (ingreso mensual de la información contable en el portal del SAT) y RMF 2026, reglas 2.8.1.5 y 2.8.1.6 (leídas en el cap. 30).
- **Contenido según el Anexo 24 (DOF 13-01-2026):** A. Catálogo de cuentas, con a) código agrupador del SAT; B. Balanza de comprobación (normal y complementaria, con fecha de modificación); C. Pólizas del periodo; D. Auxiliar de folios de comprobantes fiscales; E. Auxiliares de cuenta y subcuenta; F. y siguientes (por leer). El código agrupador se ordena por naturaleza (100 Activo, 100.01 Activo a corto plazo, 101 Caja, 102 Bancos…), y cada cuenta del catálogo propio se asocia "por naturaleza y preponderancia". La especificación técnica de los XML está en un documento técnico del portal (no descargado).
- **Por estudiar (F3):** periodicidad y plazos de envío de catálogo y balanza (reglas 2.8.1.x), cuándo se entregan pólizas (solo a requerimiento o en devoluciones), y la balanza de cierre del ejercicio.

### 4.3 Relación contabilidad-fiscal

- **Conciliación contable-fiscal:** el puente entre la utilidad contable (NIF) y el resultado fiscal (LISR art. 9). Partidas típicas del caso: depreciación contable contra deducción fiscal con tope y tasa del 25%; la parte no deducible de autos, arrendamiento y combustible pagado en efectivo; ajuste anual por inflación (fiscal) contra B-10 (contable); PTU pagada (deducible al pagarse) contra PTU devengada; provisiones no deducibles hasta que se pagan; multas y recargos; el 47% o 53% de los pagos exentos al trabajador (art. 28 fr. XXX LISR, por verificar). Hay que saber la diferencia con la "conciliación entre el resultado contable y el fiscal" de la declaración anual y del dictamen o ISSIF (CFF 32-A y 32-H, que estudian los agentes del CFF).
- **Impuestos diferidos (NIF D-4):** método de activos y pasivos sobre diferencias temporales entre valor contable y valor fiscal. Ejemplo canónico del caso: flotilla con valor contable mayor que el fiscal por el tope de $175,000 (diferencia **permanente** en lo que excede el tope, que no genera diferido) y por la tasa del 25% contra la vida útil contable (diferencia **temporal**, que sí lo genera). Agregar PTU diferida (D-3) y pérdidas fiscales por amortizar (activo diferido sujeto a recuperabilidad). La ficha C5 del 11-oct ya trabajó NIC 12 en código: reutilizarla y pasarla a NIF D-4.
- **Ejercicio de cierre (F3, verificable):** a partir de una balanza inventada de la PM, sacar la utilidad contable, conciliarla con el resultado fiscal, calcular ISR causado, diferido y PTU, y cuadrar el catálogo contra el código agrupador del Anexo 24. Aserciones: utilidad contable − partidas = resultado fiscal; ISR diferido = (diferencias temporales netas) × 30%.

---

## 5. Registro de verificación (23-oct-2026)

- Doble descarga con huella idéntica: los 28 PDF de Diputados (`pdf/`, incluidos los extras) y los 10 PDF del SAT (`rmf/`). HTML del DOF: no reproducible byte por byte (dinámico).
- Fechas: la UR de cada PDF se leyó en la portada (`pypdf`, `python3 -I`) y se cotejó con el índice `index.htm` / `regla.htm` de Diputados. Las cuatro diferencias (LIEPS, LFD, Ley Aduanera, LIGIE) son actualizaciones de cantidades o de tarifa registradas por el índice, y la propia portada las anota.
- Páginas: el número de `pypdf` coincide con el "1 de N" de la portada en todos los PDF de Diputados, salvo el RACERF (111 contra 113).
- Comparación con el repo: seis huellas del cap. 29 coinciden; la de LOPRODECON no (§1.4).
- No verificado (D): Código Financiero del Edomex (ISN, tenencia); texto compilado del RISAT; lista oficial de NIF 2026; Anexos 5 y 20 de la RMF 2026 (no descargados aquí); art. 28 fr. XXX LISR (47%/53%).
