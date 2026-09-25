# Examen diagnóstico — Sección S6: Laboratorio de datos (revelación de la clave y acta)

- **Sección:** S6, Laboratorio de datos: 12 preguntas de cálculo con datos congelados en `laboratorio/examen-datos/S6/`, de 5 puntos cada una (60 puntos).
- **Fecha:** 2026-09-25.
- **Acta redactada por:** árbitro, secretario y notario de revelación (subagente del flujo de trabajo).
- **Archivos de esta revelación:** `clave.json` (clave descifrada), `contrasena.txt` (contraseña) y esta acta, junto a `clave.enc` y `compromiso.json`.

## Protocolo con que se aplicó

1. **Compromiso público previo** (`PROTOCOLO.md` §2, mecanismo de S6–S7). La clave se cifró con AES-256-CBC (PBKDF2, 200,000 iteraciones, sal aleatoria) y se publicó en GitHub **antes** de que el sustentante respondiera, junto con la huella SHA256 del archivo cifrado, la del archivo en claro y una por pregunta. Cronología, según `git log` y el reflog local de `origin`:

   | Hecho | Commit | Hora del commit (UTC) | Push a `origin` (UTC) |
   |---|---|---|---|
   | Se agrega `S6/clave.enc` | `5909c877016a29138ecfd813f759ddc067aebafb` ("Avance de agentes") | 06:02:03 | 06:02:06 |
   | Se agrega `S6/compromiso.json` (huellas) | `6c526b632f145cdf84c61db4e1e41d00a1a8970a` | 06:02:26 | 06:02:47 |
   | Primer archivo de trabajo de S6 en el scratchpad compartido (`s6/common.py`) | — | 06:04:13 (mtime) | — |
   | Revelación de la contraseña y acta | este commit | — | — |

   **Observación de protocolo:** el cifrado y las huellas entraron en dos commits consecutivos (23 s de diferencia), no en uno solo como supone el paso 1 de `verificacion` en `compromiso.json`. No afecta la integridad: los dos commits están en `origin` antes de cualquier respuesta, y el árbol de `6c526b6` contiene el mismo blob de `clave.enc` que hay hoy (SHA256 `ed5f8e09…a2ab`). La hora del primer archivo de trabajo es un indicio, no una prueba: no verifiqué su autoría. La prueba de que el sustentante contestó después del compromiso es la auditoría del registro de su sesión.
2. **Libro cerrado** (`PROTOCOLO.md` §3). El sustentante contestó sin herramientas web ni red, sin acceso a `conocimiento/examenes/`, con la base del repositorio y los datos congelados de `laboratorio/examen-datos/S6/`. Re-verifiqué esos 11 archivos con `sha256sum -c SHA256SUMS.txt`: todos OK. La contraseña no aparece en ningún commit del repositorio (`git log --all -S`), ni en el árbol de trabajo, ni en el scratchpad compartido, así que el sustentante no pudo descifrar la clave. La auditoría del registro de la sesión del sustentante se publica aparte; esta acta no la sustituye.
3. **Calificación automática.** Compara un número extraído de la respuesta con el valor `numerica` ± `tolerancia` comprometido en la clave. Es un filtro, no la calificación. En esta sección marcó "fuera de tolerancia" 6 de 12 preguntas, y las 6 son falsos negativos del extractor: tomó otro número de la respuesta. Lo confirmé recalculando el valor comprometido con los datos congelados (tabla más abajo).
4. **Dos calificadores independientes (A y B)**, cada uno con la clave y la rúbrica, sin ver la nota del otro. Los dos recalcularon con python3 sobre los datos congelados.
5. **Arbitraje.** Si |A − B| ≤ 1, el puntaje es el promedio. Si difieren en más de 1, arbitra el secretario y justifica. **Resultado:** |A − B| = 0 en las 12 preguntas; no hubo arbitraje.
6. **Defensa oral.** Un examinador formuló dos repreguntas sobre S6-01, S6-02, S6-03 y S6-04; el sustentante respondió con cálculos propios y un juez fijó una deducción por lo que se cayó. **Puntaje final = máx(0, promedio de A y B − deducción).** Las otras 8 preguntas no tuvieron defensa oral.
7. **Umbral** (`PROTOCOLO.md` §1): 85 % o más en cada sección y 90 % o más global.

## Verificación de la revelación (notario)

Contraseña revelada (también en `contrasena.txt`): `d80452553e0dd009e475a02a39d0b6dae050a3a287238c6b73e5832e44b8cd93`

| Comprobación | Esperado (`compromiso.json`) | Obtenido | Resultado |
|---|---|---|---|
| SHA256 de `clave.enc` tomado de `6c526b6` | `ed5f8e0990380279db86b266a4ffdb400507ba3107dae38fd46f4163f33aa2ab` | `ed5f8e0990380279db86b266a4ffdb400507ba3107dae38fd46f4163f33aa2ab` | coincide |
| Descifrado con OpenSSL 3.0.13 (`-aes-256-cbc -pbkdf2 -iter 200000`) | sin error | sin error | correcto |
| SHA256 de `clave.json` descifrado | `8119ceecf65833cbc4f1c2ab16510c767073c64fdd2b1231b72cbfeee55549a8` | `8119ceecf65833cbc4f1c2ab16510c767073c64fdd2b1231b72cbfeee55549a8` | coincide |
| La serialización canónica (`json.dumps(..., sort_keys=True, ensure_ascii=False, indent=2)` + salto de línea) reproduce el archivo | idéntico | idéntico byte a byte | correcto |
| Huellas por pregunta | 12 | 12 de 12 coinciden (tabla siguiente) | correcto |
| Clave y rúbrica que usaron los calificadores A y B contra la descifrada | idénticas | 12 de 12 idénticas, carácter por carácter | correcto |
| `numerica` y `tolerancia` que usó la calificación automática | iguales | 12 de 12 iguales | correcto |

| Pregunta | SHA256 comprometido = recalculado |
|---|---|
| S6-01 | `080e55529c93212e4aba54510b1f6164130f0fec698f7f10f31b356c13f3fee0` |
| S6-02 | `291c02627cb8d841b37a145d99e96ef6e4815e531e609c5075b4c6a1ddf8ba4a` |
| S6-03 | `134b7d16fa94ea1d1714fb5cd4457f2a3e0355acc4f283ccafd60f092d8a845a` |
| S6-04 | `aec8990c7f7754ed6e75524a068de1c9303742e655582ab5169a71f627f5ce42` |
| S6-05 | `077986137d7fc0f0132f965e6476a274c69b22a62b5b66538d4b6dd4c15bb69b` |
| S6-06 | `70ef4937f1574734af500dbf29668ccf01f03cd5786cc8e67e44eb1bba9ce789` |
| S6-07 | `e34f1ee0ee5778e7a18aedf5ab78ded990fdcab351873118fc546ef0c4b23c65` |
| S6-08 | `f2a4f9f256645da3b8b7393729114f16fd21862bc4674ec04927e6287612ff9a` |
| S6-09 | `afb4da7a17ec448b4cc5a27c9c2df63ba70c80d6dc32559912ad16cfb941fabd` |
| S6-10 | `9067f40c6de384e4c3db53a3b7417e45ac39a04533c212a2fde2a5d0134c7d93` |
| S6-11 | `f9e0881cc11842518f8d875442ccf2fb291e2185096305574bb8dd032d905254` |
| S6-12 | `a9c8052ae7c6900c769bba821e737f443a7304eecc6b70c46163a1673b054fb9` |

Para verificarlo uno mismo, desde la raíz del repositorio:

```
git show 6c526b632f145cdf84c61db4e1e41d00a1a8970a:conocimiento/examenes/2026-09-25-diagnostico/S6/clave.enc > clave.enc
sha256sum clave.enc   # ed5f8e0990380279db86b266a4ffdb400507ba3107dae38fd46f4163f33aa2ab
openssl enc -d -aes-256-cbc -pbkdf2 -iter 200000 -in clave.enc -out clave.json \
  -pass file:conocimiento/examenes/2026-09-25-diagnostico/S6/contrasena.txt
sha256sum clave.json  # 8119ceecf65833cbc4f1c2ab16510c767073c64fdd2b1231b72cbfeee55549a8
python3 -c "import json,hashlib; K=['id','clave','numerica','tolerancia','rubrica']; [print(q['id'], hashlib.sha256(json.dumps({k:q[k] for k in K}, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()) for q in json.load(open('clave.json', encoding='utf-8'))]"
```

### Calificación automática: falsos negativos

| Pregunta | Esperado ± tol. | El extractor tomó | Qué número era | Recálculo del notario (datos congelados) | Lo que dice la respuesta |
|---|---|---|---|---|---|
| S6-01 | 3.386 ± 0.02 | 1.533 | la brecha de (d) | CAGR = 3.3858 % | "(c) ... CAGR = 3.207^(12/420) - 1 = 3.386 %" |
| S6-06 | 1.23 ± 0.02 | 0.704 | la fracción de (c) | t_NW del diferencial grande = 1.2317 | "BIG HiBM - BIG LoBM: media 0.169, SE_NW 0.138, t_NW 1.232" |
| S6-07 | -0.1476 ± 0.005 | -0.791 | t_d | d = C - A = -0.14757 (SE_d = 0.18645) | "d = C - A = -0.148" |
| S6-08 | 10.8 ± 0.3 | -0.449 | la diferencia neta M - A | arrastre de M = 10.797 pb (rotación 17.181 %) | "Arrastre 10.797 pb/ano" |
| S6-09 | -0.0015 ± 0.02 | -0.721 | el adelanto de Yahoo | rezago 0 de Yahoo MXN=X = -0.0015 (adelanto -0.7213) | "MXN=X: corr(r_t, f_t) = -0.002" |
| S6-10 | -49.47 ± 0.1 | -64.618 | el MDD en USD | MDD en MXN = -49.473 % (USD -64.617 %; 4,483 fechas, 46 excluidas) | "MDD = -49.473 %" (MXN) |

En las 6, la respuesta reporta el valor comprometido dentro de la tolerancia. La calificación automática no se usa para puntuar; los calificadores A y B llegaron a la misma conclusión por separado.

---

## S6-01 — Media mensual, media x12 frente a rendimiento anual compuesto (mercado japones en USD, factor regional) (laboratorio)

### Enunciado

Datos congelados en /home/user/New1/laboratorio/examen-datos/S6/. Antes de empezar, verifica las huellas con sha256sum -c SHA256SUMS.txt. Archivo: Japan_3_Factors_CSV.zip, SHA256 e116a250dff2e152d2c43359a99d1e478d7d3d94f35d3afb412af3a094f5db20. CSV interno: Japan_3_Factors.csv, primer bloque (mensual, filas yyyymm, antes de 'Annual Factors'), columnas Mkt-RF y RF en % mensual. Define el rendimiento total mensual del mercado japones en USD como R_t = (Mkt-RF)_t + RF_t. Ventana: 1991-01 a 2025-12, ambos meses incluidos (n = 420). Calcula: (a) la media aritmetica mensual de R_t en %; (b) la media x12; (c) el CAGR = [prod_t (1 + R_t/100)]^(12/n) - 1; (d) la brecha (b) - (c) en puntos porcentuales, y comparala con la aproximacion CAGR \~ 12\*mu - 12\*s^2/2, donde mu y s son la media y la desviacion estandar muestral mensual (denominador n-1) en decimales; (e) explica que numero debe usarse para proyectar riqueza terminal y cual para estimar el rendimiento esperado de un periodo, y por que la brecha es grande en esta serie. Reporta todo con 3 decimales.

### Clave (descifrada)

n = 420. (a) Media mensual = 0.4099 %/mes. (b) Media x12 = 4.919 %/anio. (c) Riqueza final prod(1+R/100) = 3.2073, CAGR = 3.386 %/anio. (d) Brecha = 4.919 - 3.386 = 1.533 pp. Desviacion estandar mensual s = 5.1646 % (anualizada s\*raiz(12) = 17.89 %). Aproximacion: 0.04919 - 12\*(0.051646^2)/2 = 0.04919 - 0.01600 = 3.318 %, a 0.07 pp del CAGR exacto; el residuo viene de terminos de orden superior (asimetria y curtosis de los rendimientos, y de que 12\*mu no es (1+mu)^12 - 1 = 5.031 %). (e) El CAGR (media geometrica) describe la tasa a la que efectivamente crecio la riqueza y es el insumo para proyectar la riqueza mediana. La media aritmetica es el estimador insesgado del rendimiento esperado de UN periodo, pero sobrestima el crecimiento compuesto por el arrastre de volatilidad, que es aproximadamente sigma^2/2 = 1.60 pp con sigma anual de 17.9 %. La brecha es grande porque la volatilidad de Japon en USD es alta (acciones mas yen). Nota: el RF de los factores regionales de French es la T-bill de EUA a 1 mes y todo esta en USD, asi que es la experiencia de un inversionista en dolares, no en yenes.

**Rúbrica:** 5 puntos. 1 pt: media mensual 0.410 (+/-0.002) y x12 4.92 (+/-0.02), con R = Mkt-RF + RF y n = 420. 1 pt: CAGR 3.386 (+/-0.02) con la formula geometrica correcta (no (1+media)^12 - 1). 1 pt: brecha 1.53 pp y aproximacion 3.32 %, explicando el residuo. 1 pt: distingue el uso de la media aritmetica (esperanza de un periodo) del de la geometrica (crecimiento y riqueza mediana). 1 pt: interpretacion del arrastre de volatilidad sigma^2/2 y aclaracion de que la serie esta en USD con RF de EUA. Si se usa una ventana o columna distinta, maximo 1 pt.

**Valor numérico comprometido:** 3.386 ± 0.02. **Huella SHA256:** `080e55529c93212e4aba54510b1f6164130f0fec698f7f10f31b356c13f3fee0` (coincide con el compromiso).

### Fuente

Kenneth R. French Data Library, https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Japan_3_Factors_CSV.zip (version 'created using the 202608 Bloomberg database'), descargado el 2026-09-25 hacia las 05:44 UTC. Descripcion de la construccion regional (USD, RF = T-bill de EUA a 1 mes): https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_3developed.html. Clave calculada con python3 propio.

### Respuesta del sustentante (completa)

VERIFICACION: `sha256sum -c SHA256SUMS.txt` en /home/user/New1/laboratorio/examen-datos/S6/ -> los 11 archivos OK (Japan_3_Factors_CSV.zip = e116a250...db20). DATOS: Japan_3_Factors.csv, primer bloque ('Annual Factors' empieza en la linea 445; mensual 199007-202608, 434 filas), columnas Mkt-RF y RF. R_t = (Mkt-RF)_t + RF_t. Ventana 1991-01 a 2025-12, n = 420, sin -99.99. Calculo propio en python3/numpy.

(a) Media aritmetica mensual = 0.410 %.

(b) Media x12 = 4.919 %.

(c) prod(1+R_t/100) = 3.207 -> CAGR = 3.207^(12/420) - 1 = 3.386 %.

(d) Brecha (b)-(c) = 4.919 - 3.386 = 1.533 pp. La s mensual es 5.165 % (17.891 % anualizada; en decimales mu = 0.0040988 y s = 0.0516464). La aproximacion 12\*mu - 12\*s^2/2 = 0.04919 - 0.01600 = 3.318 % implica una brecha de 1.600 pp. Su error contra el CAGR es -0.068 pp. La razon es que la formula aproxima la tasa logaritmica (continua): 12\*media(ln(1+R)) = 3.330 %, a solo 0.012 pp. Pasar de log a tasa discreta, exp(0.03330) - 1 = 3.386 %, agrega los 0.056 pp restantes. Los momentos superiores (asimetria +0.23, curtosis en exceso 0.70) explican el pequeno residuo.

(e) Rendimiento esperado de UN periodo (insumo de media-varianza o costo de capital): se usa la media aritmetica, que es el estimador insesgado de E[R]. Son 0.410 % mensual; 4.919 % como x12 o 5.031 % como (1+mu)^12 - 1. Riqueza terminal a varios anos (trayectoria tipica o mediana): se usa el CAGR/geometrico, W_T \~ (1.03386)^T. Compuestar la aritmetica sobrestima la riqueza tipica. El repo cita a Jacquier-Kane-Marcus (2003) en conocimiento/01-licenciatura-fundamentos.md (lineas 132 y 368): el pronostico insesgado de riqueza pondera ambas medias, y el peso de la geometrica crece con el horizonte T relativo a la muestra N (aqui N = 35 anos). La regla del sistema de reportar ambas esta en laboratorio/alertas-de-datos.md, alerta 5. Por que la brecha es grande aqui: es arrastre de varianza, \~sigma^2/2 al ano. La serie es acciones japonesas medidas en USD, asi que suma la volatilidad bursatil y la del yen/USD: sigma \~17.9 % anual da un arrastre de \~1.6 pp. Ese arrastre es casi un tercio de una media aritmetica baja (4.9 %). La brecha depende de la dispersion, no de la tendencia. Aun asi, el largo mercado bajista agrava la diferencia entre subperiodos (calculo propio: 2000-2009 da -2.076 % en media x12 y -3.684 % en CAGR). La riqueza toco un minimo de 0.596 en 2003-03.

### Calificación automática

Fuera de tolerancia (esperado 3.386, obtenido 1.533, tol. 0.02). **Falso negativo del extractor:** tomó la brecha de (d). Recálculo del notario: CAGR = 3.3858 %. La respuesta dice "(c) ... CAGR = 3.207^(12/420) - 1 = 3.386 %", dentro de la tolerancia. No se aplica ningún tope.

### Calificación

**Calificador A: 4.5/5.** Recalculé todo con python3 sobre Japan_3_Factors.csv, con el sha verificado. Resultados: n=420, media 0.40988 %, x12 4.9186 %, riqueza 3.20729, CAGR 3.38585 %, brecha 1.5327 pp, s=0.051646, aproximación 3.318 %, 12\*media(ln) 3.330 %, asimetría 0.229 y curtosis en exceso 0.702. Todo coincide con la clave y con la respuesta. El 'fuera de tolerancia' es un error de extracción: el calificador automático tomó 1.533, que es la brecha de (d). La respuesta reporta el CAGR de (c) como 3.386 %, idéntico a la clave, así que no aplico el tope de 2. Puntos 1 a 4 completos. El residuo de la aproximación está bien explicado (log contra discreto y momentos superiores), y la cita a Jacquier-Kane-Marcus en conocimiento/01, líneas 132 y 368, existe. Los datos extra (2000-2009: -2.076 y -3.684; mínimo 0.596 en 2003-03) están verificados. Descuento 0.5 en el punto 5: explica bien el arrastre sigma^2/2 y que la serie está en USD, pero nunca aclara que el RF es la T-bill de EUA, que la rúbrica pide de forma explícita.

**Calificador B: 4.5/5.** El 'fuera de tolerancia' es un falso negativo del extractor: tomó la brecha (1.533) en lugar del CAGR. La respuesta dice CAGR = 3.386 %, y yo lo recalculé con python3 sobre el zip congelado (sha OK): n=420, media 0.40988, x12 4.9186, W=3.2073, CAGR 3.3858, brecha 1.5327, s=5.1646, aproximación 3.318, 12\*media(ln)=3.330. La clave es correcta y la respuesta coincide con ella, así que califico por mérito y no aplico el tope de 2. (a)-(c) correctos: 1+1. (d) Brecha y aproximación correctas, y explica bien el residuo (log contra tasa discreta, asimetría 0.23 y curtosis 0.70, ambas verificadas): 1. (e) Distingue la media aritmética (E[R] de un periodo) de la geométrica (riqueza típica o mediana) y cita JKM en conocimiento/01, líneas 132 y 368 (verificado): 1. El arrastre sigma^2/2 = 1.6 pp está bien explicado y dice que la serie está en USD, con el yen incluido. No aclara que el RF es la T-bill de EUA a 1 mes, que la rúbrica pide expresamente: -0.5. Los cálculos extra (2000-2009: -2.076/-3.684; mínimo 0.596 en 2003-03) están verificados.

**Promedio A-B: 4.5/5** (|A − B| = 0; sin arbitraje).

### Defensa oral

**Repreguntas:**

1. Supongamos que permuto al azar el orden de los 420 meses. ¿Cuáles de tus cifras de (a) a (d) cambian y cuáles quedan igual? Con esa respuesta, defiende o retira la frase de que 'el largo mercado bajista agrava la diferencia' mientras sostienes que 'la brecha depende de la dispersion, no de la tendencia'. En 2000-2009, ¿la brecha entre media x12 y CAGR es mayor por la tendencia negativa o por la varianza de ese subperiodo? ¿Cómo lo demostrarías con los datos? Y el mínimo de riqueza de 0.596, ¿sobrevive a la permutación?
2. Dices que el CAGR sirve para la riqueza 'tipica o mediana' y que compuestar la aritmética sobrestima. Un fondo de pensiones tiene que cubrir un pasivo en valor esperado, no en mediana, a 50 años, y tu muestra es de N = 35 años. Bajo el razonamiento de Jacquier-Kane-Marcus, ¿qué peso le toca a cada media cuando T > N? ¿Qué significa económicamente que un peso quede fuera de [0,1]? ¿Qué cifra le darías al fondo, y por qué no es (1+mu)^T aunque (1+mu)^T sea E[W_T] bajo iid con mu conocida?

**Respuesta del sustentante:**

Base recalculada. Serie: mercado de Japón con retorno total en USD (Mkt-RF+RF de Japan_3_Factors), de 1991-01 a 2025-12, n=420. Media x12 = 4.92 %, CAGR = 3.39 %, brecha = 1.53 pp, sigma = 17.89 % y sigma^2/2 = 1.60 pp. La riqueza terminal es 3.21 y la mínima 0.596 (en 2003-03). El MDD es -58.1 %.

1) Permutación. Media, varianza, CAGR, brecha y riqueza terminal no cambian, ni en el último decimal. La media y la varianza no dependen del orden de los datos, y el CAGR depende solo del producto de (1+r_t), que es conmutativo. Cambia todo lo que depende de la trayectoria: la riqueza mínima, el MDD, sus fechas, cualquier cifra por subperiodo (2000-2009), las autocorrelaciones y los errores estándar NW.

Por eso retiro la frase 'el largo mercado bajista agrava la diferencia'. Si la brecha no cambia al permutar, el orden de los meses, que es justamente lo que define un mercado bajista largo, no puede agravarla. Lo que sí sostengo es esto: (i) el mercado bajista baja el nivel de ambas medias; (ii) empeora las métricas de trayectoria (riqueza mínima, MDD, tiempo bajo el agua); (iii) la brecha pesa más en relación con la media cuando la media es baja (1.53/4.92 = 31 %), pero eso es un efecto de cociente, no de diferencia; (iv) en los datos, los periodos bajistas suelen traer más volatilidad, y la volatilidad es la que mueve la brecha.

2) 2000-2009. Media x12 = -2.08 %, CAGR = -3.68 %, brecha = 1.61 pp, sigma = 18.33 % y sigma^2/2 = 1.68 pp. La brecha es mayor por la varianza, no por la tendencia. Lo demuestro con un contrafactual que deja fijas la secuencia y la varianza y solo cambia la media. Si desplazo los retornos del subperiodo a media cero, la brecha es 1.66 pp; si los desplazo a la media de toda la muestra (+4.92 %), es 1.61 pp. Mover la tendencia 7 pp al año cambia la brecha a lo más 0.05 pp. Ese residuo existe porque la tendencia entra solo en términos de segundo orden: el factor 1/(1+m)^2 y la convexidad de anualizar ((1+g)^12 frente a 12g). La brecha de 2000-2009 supera a la de toda la muestra por 0.08 pp, y (0.1833^2-0.1789^2)/2 = 0.08 pp. El exceso lo explica la varianza completa. Por décadas pasa lo mismo: los 1990 tienen media +6.6 %, sigma 23.7 % y brecha 2.64 pp; los 2000, media -2.1 %, sigma 18.3 % y brecha 1.61 pp; los 2010, media +8.4 %, sigma 12.5 % y brecha 0.51 pp. La brecha se ordena según sigma, no según la tendencia.

3) Riqueza mínima. Como número, 0.596 no sobrevive. En 20,000 permutaciones la mediana de la riqueza mínima es 0.79, con percentiles 5 %-95 % de 0.45 a 1.02. P(mín \<= 0.596) = 18 %, y en 8 % de las permutaciones la riqueza nunca baja de 1. El MDD observado (-58.1 %) queda en el percentil 35 (mediana -54.5 %). El orden real, con la caída concentrada en 1991-2003, profundizó el mínimo, pero no de forma extraordinaria (p aprox. 0.18). Con sigma = 18 % y 35 años, caídas del 40 % son comunes en cualquier orden. Nota: la permutación también destruye el agrupamiento de volatilidad, así que es un nulo iid.

4) Fondo de pensiones con T=50 y N=35. Con log-retornos iid y mu estimada, E[exp(T mu_hat)] = exp(T mu + T^2 sigma^2/(2N)). El estimador insesgado de E[W_T] es exp(T[mu_hat + (sigma^2/2)(1 - T/N)]). En términos de la media aritmética A y la geométrica G, eso equivale a pesos (1 - T/N) sobre A y T/N sobre G. Con T/N = 50/35 = 1.43, el peso sobre G es 1.43 y el peso sobre A es -0.43.

Que un peso quede fuera de [0,1] significa que ya no se interpola entre las dos medias, sino que se extrapola por debajo de la geométrica. Cuando el horizonte supera la muestra, el sesgo de Jensen por compuestar una media incierta (T^2 sigma^2/2N) excede toda la corrección por volatilidad (T sigma^2/2). El riesgo de estimación domina al riesgo de retorno, y hasta la media geométrica resulta optimista.

Cifras: G = 3.33 % log, sigma^2 = 0.0316 y A = 4.91 % log. La tasa insesgada es 3.33 % - 1.58 % x 0.43 = 2.65 % log, es decir, 2.69 % anual, y E[W_50] aprox. 3.8 por peso invertido. Para comparar: (1+media x12)^50 = 11.0, exp(50A) = 11.7 y (1+CAGR)^50 = 5.3. El factor de sesgo exp(T^2 sigma^2/2N) es aprox. 3.1.

¿Por qué no (1+mu)^T? Porque mu no se conoce. Sustituirla por mu_hat en una función convexa sesga el resultado hacia arriba, y el sesgo crece con T^2/N. Además, N es el lapso en años (35), no el número de meses: SE(mu_hat) = sigma/raíz(35) = 3.0 % anual. Con más o menos un error estándar, E[W_50] va de aprox. 0.8 a 17.

Al fondo le daría 2.7 % anual (aprox. 3.8x) como estimación puntual del valor esperado, siempre con esa banda. Para fondear el pasivo recomendaría algo más prudente. Si recuerdo bien, el estimador de JKM que minimiza el MSE usa (1 - 3T/N), y aquí daría una tasa negativa. También recomendaría una tasa basada en probabilidad de faltante: con sigma raíz(T) = 1.26, P(W_T \< E[W_T]) = Phi(0.63) aprox. 74 % aun conociendo mu. Fondear al valor esperado deja un faltante en cerca de 3 de cada 4 escenarios. Por último, es la historia de un solo país.

Cálculos en /tmp/claude-0/-home-user/90e882ac-d4b5-510a-b57d-7ad6cabb9a68/scratchpad/s1.py con /home/user/New1/laboratorio/examen-datos/S6/Japan_3_Factors_CSV.zip.

**Juicio: deducción de 0.5.** La defensa es sólida y reproduje sus cifras: n=420, media x12 = 4.919 %, CAGR = 3.386 %, sigma = 17.89 %, riqueza mínima 0.596 en 2003-03, y en 2000-2009 media -2.08 %, CAGR -3.68 %, sigma 18.33 %. Separa bien lo que no cambia al permutar (media, varianza, CAGR, brecha, riqueza terminal) de lo que depende de la trayectoria (mínimo, MDD, subperiodos). El contrafactual que desplaza la media muestra que la brecha la mueve la varianza, no la tendencia, y el orden por décadas según sigma lo confirma. En JKM obtiene bien los pesos (1-T/N) sobre A y T/N sobre G, que dan -0.43 y 1.43; la tasa de 2.65 % log (E[W50] aprox. 3.8), el factor de sesgo aprox. 3.1 y P(W\<E[W]) = Phi(0.63) aprox. 74 % también son correctos. Explica bien por qué no se usa (1+mu)^T. Quito medio punto porque tuvo que retirar 'el largo mercado bajista agrava la diferencia', una frase de la respuesta original que era falsa y contradecía su propia tesis de que la brecha depende de la dispersión. El núcleo de (a)-(e) se sostiene.

### Puntaje final

**4.0/5** = 4.5 (promedio de A y B) − 0.5 (defensa oral).

### Hueco

**Faltó en (e), según la rúbrica (A y B, −0.5):** decir que el RF de los factores regionales de French es la T-bill de EUA a 1 mes. La respuesta aclara que la serie está en USD e incluye el yen, pero no dice qué tasa libre de riesgo lleva, que es lo que convierte a R_t en la experiencia de un inversionista en dólares.

**Se cayó en la defensa (−0.5):** la frase "el largo mercado bajista agrava la diferencia". La brecha entre la media ×12 y el CAGR no cambia si se permutan los meses, así que no puede depender del orden, que es lo que define un mercado bajista largo. La frase contradecía la tesis correcta de la misma respuesta ("la brecha depende de la dispersión, no de la tendencia"). El sustentante la retiró y mostró con un contrafactual que en 2000-2009 la brecha la mueve la varianza.

**Base:** la construcción de los factores regionales de French (USD, RF = T-bill de EUA, Big = 90 % superior y Small = 10 % inferior de la capitalización, cortes de B/M 30/70 sobre las grandes) no está documentada en el repositorio. En S6-11 el sustentante la citó "de memoria". Conviene una ficha en `laboratorio/` con esas definiciones y su fuente.

---

## S6-02 — t con supuesto IID frente a Newey-West(6) e IC95 (HML de EUA en la 'decada perdida' del valor) (laboratorio)

### Enunciado

Archivo: /home/user/New1/laboratorio/examen-datos/S6/F-F_Research_Data_Factors_CSV.zip, SHA256 b840dba55d319f4818fc7300e65c52eff5f64870c8d495fa58ff5d4cd749f5eb. CSV interno: F-F_Research_Data_Factors.csv, bloque mensual (filas yyyymm antes de 'Annual Factors'), columna HML en % mensual. Ventana: 2007-01 a 2020-12 (n = 168). Definiciones: xbar es la media; s es la desviacion estandar muestral (n-1); SE_IID = s/raiz(n). Newey-West con 6 rezagos y kernel de Bartlett: gamma_j = (1/n) \* suma_{t=j+1..n} (x_t - xbar)(x_{t-j} - xbar); S = gamma_0 + 2 \* suma_{j=1..6} (1 - j/7) \* gamma_j; SE_NW = raiz(S/(n-1)), es decir, S/n con correccion n/(n-1). IC95 = xbar +/- 1.96\*SE. Calcula: xbar, s, t_IID, IC95_IID, t_NW, IC95_NW, la autocorrelacion de primer orden rho1 = gamma_1/gamma_0 y el cociente SE_NW^2/SE_IID^2. Despues, (i) di si cada metodo rechaza H0: E[HML] = 0 al 5 % bilateral; (ii) explica el mecanismo de la diferencia; (iii) discute que problema inferencial adicional crea elegir esta ventana justamente porque fue mala para el valor.

### Clave (descifrada)

n = 168; xbar = -0.4431 %/mes (-5.32 %/anio x12); s = 2.8845. SE_IID = 0.2225, t_IID = -1.991, IC95_IID = [-0.879, -0.007]: excluye 0, asi que con IID se 'rechaza' al 5 %. SE_NW(6) = 0.2552, t_NW = -1.736, IC95_NW = [-0.943, +0.057]: incluye 0, asi que no se rechaza. rho1 = 0.194 (rho2..rho6 = 0.053, 0.021, -0.056, -0.031, -0.178). Cociente de varianzas NW/IID = 1.315. Mecanismo: la autocorrelacion positiva de corto plazo del HML hace que la varianza de la media sea mayor que s^2/n. El SE IID subestima la incertidumbre y el t pasa de -1.99 a -1.74. Conclusion: con errores robustos, el mal desempenio del valor en 2007-2020, aunque grande en puntos, no es estadisticamente distinto de cero al 5 %. Problema adicional: la ventana se eligio ex post por ser la peor racha conocida (seleccion condicionada al resultado, o 'data snooping'), asi que ni siquiera el valor p nominal de NW es valido. Habria que prerregistrar la ventana, usar una ventana definida por un evento exogeno o corregir por busqueda sobre ventanas (por ejemplo, con el maximo de estadisticos de tipo sup-t).

**Rúbrica:** 5 puntos. 1 pt: xbar -0.443 y s 2.884. 1 pt: t_IID -1.99 e IC_IID [-0.879, -0.007]. 1 pt: t_NW -1.736 (+/-0.01) e IC_NW [-0.943, 0.057] con la convencion exacta (Bartlett, 6 rezagos, n/(n-1)). 1 pt: rho1 aprox. 0.19, cociente aprox. 1.31 y explicacion del mecanismo. 1 pt: conclusion correcta (IID rechaza y NW no) mas la critica de la seleccion de la ventana. Sin la correccion n/(n-1) sale t aprox. -1.741: se acepta con descuento de 0.5 pt si se declara.

**Valor numérico comprometido:** -1.736 ± 0.01. **Huella SHA256:** `291c02627cb8d841b37a145d99e96ef6e4815e531e609c5075b4c6a1ddf8ba4a` (coincide con el compromiso).

### Fuente

Kenneth R. French Data Library, https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip (version CRSP 202607), descargado el 2026-09-25 hacia las 05:44 UTC. Newey, W. y West, K. (1987), Econometrica 55(3): 703-708. Clave verificada con dos implementaciones propias en python3 (suma de autocovarianzas y forma matricial de Bartlett), que coinciden.

### Respuesta del sustentante (completa)

DATOS: F-F_Research_Data_Factors.csv (sha OK), bloque mensual 192607-202607, columna HML. Ventana 2007-01 a 2020-12, n = 168. Calculo propio con las definiciones del enunciado.

xbar = -0.443 %/mes; s = 2.884; SE_IID = 0.223; t_IID = -1.991; IC95_IID = [-0.879, -0.007].

gamma_0..6 = 8.271, 1.602, 0.435, 0.174, -0.461, -0.257, -1.472. S = 10.875; SE_NW = 0.255; t_NW = -1.736; IC95_NW = [-0.943, 0.057].

rho1 = gamma_1/gamma_0 = 0.194. Cociente SE_NW^2/SE_IID^2 = 1.315, que es identico a S/gamma_0 porque s^2 = gamma_0\*n/(n-1). SE_NW es 14.7 % mayor.

(i) IID: |t| = 1.991 > 1.96, rechaza H0 al 5 % (p = 0.046 normal; 0.048 con t de 167 gl), pero en la frontera. NW: |t| = 1.736 \< 1.96, no rechaza (p = 0.083); el IC incluye el 0.

(ii) Mecanismo: Var(xbar) = (gamma_0/n)\*[1 + 2\*suma w_j\*rho_j]. Con autocorrelacion positiva de corto plazo (rho1 = 0.194, rho2 = 0.053, rho3 = 0.021), las observaciones aportan menos informacion independiente que n = 168. Los meses malos de value vinieron en rachas. El factor ponderado por Bartlett es 1.315; rho6 = -0.178 compensa en parte. El SE IID supone independencia y subestima la incertidumbre. Ademas, el propio NW con 6 rezagos y n = 168 es un estimador ruidoso. El sistema exige reportar ambas t (laboratorio/alertas-de-datos.md, alerta 6).

(iii) Seleccion condicionada al resultado. Calculo propio: esta es la 2.a peor de las 1,034 ventanas moviles de 168 meses desde 1926 (percentil 0.19 %; la peor empieza en 2006-10). En toda la muestra, HML tiene media 0.355 %/mes (t_NW 3.14). Elegir la ventana despues de verla (fin en 2020-12, justo tras el valle de 2020-09) invalida los valores p nominales. Es data snooping: bajo una prima constante positiva, el minimo de muchas ventanas casi garantiza una t 'significativa' negativa. Tambien hay regresion a la media: 2021-01 a 2026-07 da +0.78 %/mes (t_NW 1.57). Lo correcto es fijar las ventanas antes de ver los datos (como hace el pre-registro de laboratorio/replicas/R03-primas-de-factores-pre-post-publicacion.md) o usar valores criticos que incorporen la busqueda: distribucion del minimo por bootstrap, o una prueba de cambio estructural con fecha desconocida tipo Andrews sup-F [Inferencia: referencia de memoria, no del repo]. Aun asi, la conclusion 'value fue negativo' queda al filo del 5 % incluso sin corregir.

### Calificación automática

Dentro de tolerancia (esperado -1.736, obtenido -1.736, tol. 0.01).

### Calificación

**Calificador A: 5.0/5.** Verificado con python3: xbar -0.44310, s 2.88448, SE_IID 0.22254, t_IID -1.991, IC [-0.879, -0.007], SE_NW 0.25519, t_NW -1.7364, IC [-0.943, 0.057], rho1 0.1937 y cociente 1.3149. Coincide con la clave y usa la convención exacta. La conclusión es correcta (IID rechaza y NW no), y el mecanismo está bien explicado con Var(xbar). La crítica de selección de ventana es sólida y también la verifiqué: es la 2.a peor de 1,034 ventanas, la peor empieza en 2006-10, la media de toda la muestra es 0.355 con t_NW 3.14, y 2021-01 a 2026-07 da 0.78 con t 1.57. Las citas a alertas-de-datos.md (alerta 6) y al pre-registro R03 existen. La referencia sup-F de Andrews está marcada honestamente como de memoria.

**Calificador B: 5.0/5.** Recalculé todo con python3: xbar -0.44310, s 2.88448, t_IID -1.991, SE_NW 0.25519, t_NW -1.7364, cociente 1.3149. IC y rho1 = 0.194 coinciden. Usa la convención exacta (Bartlett, 6 rezagos, n/(n-1)). Concluye bien: IID rechaza en la frontera y NW no. El mecanismo es correcto: la autocorrelación positiva infla Var(xbar), y rho6 negativo compensa en parte. La crítica a la selección de la ventana es sólida y está cuantificada: 2.a peor de 1,034 ventanas de 168 meses, con la peor en 2006-10 (verificado). Muestra completa: 0.355, t_NW 3.14. Periodo 2021-2026: +0.78, t 1.57 (verificado). Propone prerregistro o valores críticos que incorporen la búsqueda. Las citas del repo (alertas-de-datos alerta 6; pre-registro de R03) existen. Andrews sup-F es una referencia real y viene marcada como de memoria.

**Promedio A-B: 5.0/5** (|A − B| = 0; sin arbitraje).

### Defensa oral

**Repreguntas:**

1. Tu conclusión NW depende de 6 rezagos, y gamma_6 = -1.472 compensa buena parte de rho1. ¿Qué esperarías con 3 rezagos, con 12, o con la regla automática 4(n/100)^(2/9)? ¿La no-significancia se sostiene en todas? Si otro analista escoge el número de rezagos después de ver la t, ¿en qué se diferencia eso del problema de selección de ventana que criticas en (iii)? Y con un kernel uniforme truncado en lugar de Bartlett, ¿podría salir S negativo con estos gammas? ¿Por qué Bartlett lo impide?
2. Afirmas que bajo una prima constante positiva el mínimo de 1,034 ventanas 'casi garantiza' una t negativa significativa. Esas ventanas se traslapan casi por completo: ¿cuántas pruebas efectivamente independientes hay? ¿Eso fortalece o debilita tu corrección por data snooping? Ahora un contraejemplo: si la prima de value de verdad cayó tras su publicación (1992) o por intangibles no capitalizados, una t negativa en 2007-2020 sería señal y no selección. ¿Qué prueba distinguiría 'cambio estructural genuino' de 'escogí la peor ventana'? ¿Tu dato de 2021-2026 (t_NW 1.57) discrimina entre ambas hipótesis o no?

**Respuesta del sustentante:**

Base. HML de EUA, ventana 2007-01 a 2020-12 (n=168). Media -0.443 %/mes, t_iid = -2.00, rho1 = 0.194 (gamma1 = 1.602) y gamma6 = -1.472 (rho6 = -0.178).

1) Rezagos. Con Bartlett: L=1 da t=-1.83; L=3, -1.72; la regla automática, floor(4(168/100)^(2/9)) = floor(4.49) = 4, da -1.71; L=6, -1.74; L=12, -1.78; L=24, -1.74. La no-significancia al 5 % de dos colas se sostiene para todo L >= 1. Solo L=0 (iid) llega a -2.00.

Corrijo mi frase: con Bartlett y L=6, gamma6 pesa 1/7 y resta solo 0.42, contra +2.75 del rezago 1. Los rezagos 4 a 6 juntos restan 0.96 de los 3.57 que suman los rezagos 1 a 3. 'Compensa buena parte' es cierto solo con el kernel uniforme: ahí gamma6 resta 2.94 contra +3.20 del rezago 1, S = 8.31 y t = -1.99. Es decir, la conclusión es robusta al número de rezagos pero frágil al kernel.

Dos matices. (a) Una prueba de una cola (H1: mu \< 0) rechazaría con todos los L, porque t \< -1.645. Pero escoger una cola después de ver el signo es otra bifurcación. (b) Con valores críticos fixed-b (Kiefer-Vogelsang) para Bartlett con b = 7/168 aprox. 0.04, el crítico sube a más o menos 2.08 (lo cito de memoria), así que la prueba es aún menos significativa.

Escoger L después de ver la t es el mismo pecado que escoger la ventana: seleccionar por el resultado invalida el tamaño nominal de la prueba. La diferencia es de grado. Entre las especificaciones Bartlett con L >= 1, la t se mueve entre -1.71 y -1.83; entre ventanas, se mueve de -2.06 a +3.54. Además, para L existe una regla que se puede fijar de antemano. El remedio es el mismo en los dos casos: prerregistrar L y el kernel, reportar la tabla completa, o usar la distribución del máximo sobre especificaciones.

¿Puede salir S negativo con el kernel uniforme? Con estos gammas, S_unif > 0 para todo L \<= 94, y es negativo en L = 95-97. En L = n-1 vale exactamente 0, porque con datos centrados gamma0 + 2 suma(gamma_k) = (suma(y - ybar))^2/n = 0. Bartlett lo impide porque sus pesos 1 - k/(L+1) son la autocorrelación de una ventana rectangular. Su transformada, el kernel de Fejér, es no negativa, y S_B = integral de Fejér x periodograma >= 0; equivale a una suma de cuadrados de sumas por bloque. El kernel uniforme corresponde al de Dirichlet, que tiene lóbulos negativos.

2) Ventanas. 1,034 = 1201 - 168 + 1 ventanas de 14 años. Hay unas 7.1 ventanas sin traslape, pero para colas extremas el barrido equivale a unas 45-80 pruebas independientes en la simulación: ni 1,034 ni 7. Esto debilita mi afirmación. 'Casi garantiza' es falso bajo la prima histórica. Con la prima constante de toda la muestra (0.355 %/mes, E[t] por ventana = 1.30) y bootstrap iid, P(mín t \< -1.96) = 4.5 % y la mediana del mínimo es -0.74. Con bloques de 24 meses, P = 12.8 %. Solo con una prima cercana a cero se vuelve probable: 68 % con mu = 0, 41 % con mu = 0.10 y 21 % con mu = 0.20. El mínimo observado (t_iid = -2.06, ventana 2006-10 a 2020-09) tiene p aprox. 0.035 (iid) a 0.10 (bloques). Retiro 'casi garantiza'. Lo correcto es que la corrección por data snooping reduce la evidencia pero no la anula.

3) Cambio estructural contra 'peor ventana'. Las pruebas que distinguen:

(i) Fecha fijada antes de ver los datos, 1992-07: media previa 0.445, posterior 0.181, t_diff(NW6) = -1.11, no significativa.

(ii) Fecha desconocida con valores críticos corregidos por la búsqueda: el sup-Wald de Andrews (recorte de 15 %) vale 4.73 en 2006-08, contra un crítico de 5 % de aprox. 8.85. No hay quiebre. El t_diff = -2.02 con quiebre en 2007-01 viene de una fecha escogida con los datos.

(iii) Fuera de muestra: HML de Europa en 1990-2006 (ya publicado el efecto) promedia +0.645 (t 2.36), lo que contradice que la publicación lo haya matado. En 2007-2020, Europa da -0.31 (t -1.32) y Japón -0.14 (t -0.61).

(iv) Mecanismo: el value spread log(BE/ME alto/bajo) de 6_Portfolios_2x3 pasa de 1.38 en junio de 2007 (percentil 14) a 2.25 en junio de 2020 (percentil 95). Son +0.87 log, casi exactamente la pérdida log de HML (log 0.42 aprox. -0.87). La peor ventana va del spread más angosto al más ancho: es una revaloración, que baja el retorno realizado y sube el esperado.

La hipótesis de intangibles se probaría recalculando el BE con I+D y SG&A capitalizados. Esos datos no están en el repo.

4) 2021-2026 (n=67). Media 0.78 %/mes, SE_NW = 0.49, t aprox. 1.57. Rechaza que persista el nivel de 2007-2020 (z = 2.48 contra -0.443). No distingue entre prima intacta (z = 0.86 contra 0.355), prima reducida (z = 1.45 contra 0.063, la media de 1992-07 a 2020-12) y prima cero (z = 1.58). Además, ambas hipótesis predicen un rebote desde un spread ancho. Discrimina poco: solo descarta una prima permanentemente negativa.

Scripts: s2.py, s2b.py y s2c.py en el scratchpad.

**Juicio: deducción de 1.0.** Verifiqué las t de NW con Bartlett: L=1 da -1.83, L=3 -1.72, L=4 -1.71, L=6 -1.74, L=12 -1.78 y L=24 -1.74. El kernel uniforme con L=6 da S=8.31 y t=-1.99, y S_unif es negativo por primera vez en L=95-97. La no-significancia se sostiene para todo L>=1. La explicación de Fejér contra Dirichlet es correcta, y el crítico sup-Wald 8.85 de Andrews y el análisis del value spread y de 2021-2026 son de gran nivel. Aun así, dos afirmaciones de la respuesta original se caen y la propia defensa las retira. (1) 'gamma_6 compensa buena parte de rho1' es falso con Bartlett: el peso 1/7 hace que reste solo 0.42 contra +2.75; solo vale con kernel uniforme. Esto muestra que el original no había leído bien los pesos del estimador que usó. (2) Que el mínimo sobre las ventanas 'casi garantiza' una t significativa: con la prima histórica la probabilidad es 4.5-12.8 %, no casi segura. La conclusión principal (con NW no se rechaza al 5 % y hay data snooping) sigue en pie, pero el argumento cuantitativo de (iii) era erróneo.

### Puntaje final

**4.0/5** = 5.0 (promedio de A y B) − 1.0 (defensa oral).

### Hueco

**Ante A y B: sin pérdida.** Todo el cálculo es exacto y la conclusión es la de la clave.

**Se cayó en la defensa (−1.0):** dos afirmaciones cuantitativas.
- En (iii), que bajo una prima constante positiva el mínimo de 1,034 ventanas "casi garantiza" una t negativa significativa. Con la prima histórica, la probabilidad es 4.5 % (bootstrap iid) a 12.8 % (bloques de 24 meses). Las ventanas se traslapan y equivalen a unas 45-80 pruebas independientes, no a 1,034. La corrección por *data snooping* reduce la evidencia, pero no la anula.
- En (ii), el peso de gamma_6 en el estimador. Con Bartlett y 6 rezagos pesa 1/7 y resta 0.42 de S, contra +2.75 del rezago 1; solo con kernel uniforme "compensa buena parte".

**Observación del árbitro sobre la segunda afirmación:** la respuesta escrita dijo "rho6 = −0.178 compensa en parte", que es cierto. "Compensa buena parte" es la paráfrasis de la repregunta, que el sustentante aceptó y corrigió en la defensa. La deducción la fija el juez de la defensa y no la modifico, pero consta que una de sus dos causas descansa en esa paráfrasis. La otra causa ("casi garantiza") sí está en la respuesta y es errónea.

**Base:** la prueba sup-F/sup-Wald de Andrews y los valores críticos *fixed-b* de Kiefer-Vogelsang se citaron de memoria; no están en la base.

---

## S6-03 — Drawdown maximo pico-valle con fechas (HML de EUA, muestra completa) (laboratorio)

### Enunciado

Archivo: /home/user/New1/laboratorio/examen-datos/S6/F-F_Research_Data_Factors_CSV.zip, SHA256 b840dba55d319f4818fc7300e65c52eff5f64870c8d495fa58ff5d4cd749f5eb; CSV F-F_Research_Data_Factors.csv, bloque mensual, columna HML (% mensual). Ventana: toda la muestra mensual, 1926-07 a 2026-07 (n = 1201). Construye el indice de riqueza W_0 = 1 (cierre de 1926-06), W_t = W_{t-1}\*(1 + HML_t/100). Drawdown: DD_t = W_t / max_{0\<=s\<=t} W_s - 1, con W_0 incluido en el maximo acumulado. Reporta: (a) el drawdown maximo MDD = min_t DD_t en %; (b) el mes del pico (cierre de mes en que se alcanza el maximo previo) y el mes del valle; (c) los meses del pico al valle; (d) si hubo recuperacion al pico antes de 2026-07 y, si no, el drawdown vigente al cierre de 2026-07; (e) dos advertencias metodologicas sobre interpretar el MDD de un factor largo-corto capitalizado como si fuera una inversion.

### Clave (descifrada)

(a) MDD = -57.78 %. (b) Pico al cierre de 2006-12 (W = 48.548); valle al cierre de 2020-09 (W = 20.498). (c) 165 meses (13 anios y 9 meses). (d) No se recupero: W(2026-07) = 34.193, 29.57 % por debajo del pico de 2006-12. (e) Advertencias: (1) capitalizar un diferencial largo-corto de costo cero supone una estrategia totalmente colateralizada 1:1, rebalanceada cada mes, sin costos, sin costo de prestamo de acciones ni margen. No es invertible en GBM, que no permite ventas en corto, asi que el MDD no es el de ningun portafolio operable. (2) El MDD depende de la trayectoria, lo domina un solo episodio (la racha 2007-2020 del valor) y no tiene un error estandar sencillo. No sirve para inferir el riesgo futuro sin un modelo; una sola observacion extrema no es una distribucion. Contexto aceptable: el auge del crecimiento y de los intangibles, tasas bajas y la recuperacion del valor desde finales de 2020 sin alcanzar el pico.

**Rúbrica:** 5 puntos. 1 pt: MDD -57.78 (+/-0.05). 1 pt: pico 2006-12 y valle 2020-09. 1 pt: 165 meses y 'no recuperado', con drawdown vigente de aprox. -29.6 % en 2026-07. 1 pt: convencion correcta (capitaliza rendimientos decimales e incluye W_0). 1 pt: las dos advertencias (no invertible o colateral, y dependencia de un episodio o falta de error estandar). Un MDD calculado sobre la suma de rendimientos en lugar del producto vale 0 en el punto numerico.

**Valor numérico comprometido:** -57.78 ± 0.05. **Huella SHA256:** `134b7d16fa94ea1d1714fb5cd4457f2a3e0355acc4f283ccafd60f092d8a845a` (coincide con el compromiso).

### Fuente

Kenneth R. French Data Library, F-F_Research_Data_Factors_CSV.zip (CRSP 202607), https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip, descargado el 2026-09-25. Calculo propio en python3, verificado con numpy (cumprod y maximum.accumulate).

### Respuesta del sustentante (completa)

DATOS: F-F_Research_Data_Factors.csv, HML mensual 1926-07 a 2026-07, n = 1201, sin faltantes. W_0 = 1 (1926-06), W_t = W_{t-1}\*(1+HML_t/100); DD_t = W_t/max_{s\<=t} W_s - 1, con W_0 incluido. Calculo propio.

(a) MDD = -57.777 %.

(b) Pico al cierre de 2006-12 (W = 48.548); valle en 2020-09 (W = 20.498).

(c) 165 meses del pico al valle.

(d) No hubo recuperacion antes de 2026-07. El maximo posterior al valle fue W = 34.531 en 2022-12. Al cierre de 2026-07, W = 34.193 y el drawdown vigente es -29.570 %. Desde el valle subio +66.8 %, y aun necesita +41.98 % para volver al pico. Coincide con la cifra del sistema de -57.8 % de dic-2006 a sep-2020 (laboratorio/replicas/R03-primas-de-factores-pre-post-publicacion.md, verificacion C6). Otras caidas de la serie (calculo propio): -43.7 % (1933-08 a 1935-03) y -39.8 % (1998-05 a 2000-02).

(e) Advertencias:

1) HML es un rendimiento largo-corto de inversion cero. Capitalizarlo supone, sin decirlo, \$1 de capital que sostiene \$1 largo y \$1 corto rebalanceado cada mes. Ignora el interes del colateral, el costo de prestamo de los cortos, el margen y el financiamiento. El apalancamiento es arbitrario y el MDD no es lineal en el (calculo propio): 0.5xHML da -33.8 %, 1x da -57.8 % y 2x da -84.7 %. Con HML+RF (colateral en T-bills), el MDD es -52.5 %, el pico pasa a 2007-02 y el drawdown vigente es solo -5.4 %. La cifra depende de la convencion contable, no de una inversion real.

2) No es invertible ni ejecutable: es un portafolio de papel sin costos ni impacto, con rebalanceo anual en junio, acciones pequenas e iliquidas y ventas en corto. El SIC no permite cortos (conocimiento/26-radar-de-oportunidades.md, linea 53). Ademas, el MDD es un estadistico extremo de una sola trayectoria, sin error estandar. Tiende a crecer con la longitud de la muestra y depende del punto final. Con datos mensuales subestima las caidas intra-mes, y la historia puede cambiar con la version de CRSP (aqui 202607).

### Calificación automática

Dentro de tolerancia (esperado -57.78, obtenido -57.777, tol. 0.05).

### Calificación

**Calificador A: 5.0/5.** Verificado: MDD -57.777 %, pico 2006-12 (W 48.548), valle 2020-09 (W 20.498), 165 meses, W(2026-07) 34.193 y drawdown vigente -29.57 %. La convención es correcta: producto, con W_0 incluido. Los extras también cuadran: máximo posterior de 34.531 en 2022-12; 0.5x -33.8 % y 2x -84.7 %; HML+RF -52.5 % con pico en 2007-02 y vigente -5.4 %; caídas de -43.7 % (1935-03) y -39.8 % (2000-02). Las dos advertencias están completas: colateral/no invertible (con la cita, verificada, de que el SIC no permite cortos) y estadístico de una sola trayectoria sin error estándar. La cita a R03 C6/C13 existe.

**Calificador B: 5.0/5.** Verificado con python3: MDD -57.777 %, pico 2006-12, valle 2020-09, 165 meses, W final 34.193 y drawdown vigente -29.570 %. La convención es correcta (producto de rendimientos decimales, W_0 incluido). Las dos advertencias están completas: (1) largo-corto de costo cero capitalizado con colateral implícito, sin costos de préstamo ni margen, y con MDD no lineal en el apalancamiento (0.5x -33.8 %, 2x -84.7 %; HML+RF -52.5 % con pico en 2007-02 y vigente -5.4 %, todo verificado); (2) no es invertible, el SIC no permite cortos (conocimiento/26, línea 53, verificada) y el MDD es un estadístico extremo de una sola trayectoria, sin error estándar. La cita de R03 C6 (-57.8 %) existe.

**Promedio A-B: 5.0/5** (|A − B| = 0; sin arbitraje).

### Defensa oral

**Repreguntas:**

1. Dices que el MDD 'depende del punto final' y que con datos mensuales se subestiman las caídas intra-mes. Contesta sin recalcular: si la muestra empezara en 1963-07, ¿cambia el MDD, el pico o el valle? ¿Y si terminara en 2015-12? Luego, el HML mensual de Fama-French es la diferencia de los rendimientos mensuales de los portafolios largo y corto. No es la capitalización del HML diario. Entonces, ¿un índice construido con HML diario garantiza un MDD igual o más profundo que el mensual? ¿Puede salir menos profundo? ¿Por qué?
2. Con HML+RF el MDD casi no cambia (-52.5 % contra -57.8 %), pero el drawdown vigente pasa de -29.6 % a -5.4 %. Explica por qué el colateral afecta tanto más al drawdown vigente que al máximo. Piensa en qué tasas pagaba la T-bill entre 2007 y 2020 comparadas con las de después. ¿Qué supuesto realista sobre el colateral y el rebate de los cortos (tasa de préstamo, haircut, costo de posiciones difíciles de pedir prestadas) acercaría la versión 'invertible' a HML puro y no a HML+RF? Además, con rebalanceo mensual, ¿a partir de qué apalancamiento un solo mes de la muestra deja la riqueza en cero? ¿Cómo lo calcularías y qué te dice de la no linealidad que reportas?

**Respuesta del sustentante:**

Base (F-F, 1926-07 a 2026-07). Índice Prod(1+HML): MDD -57.8 %, pico 2006-12, valle 2020-09, sin recuperar; drawdown vigente -29.6 %. HML+RF: MDD -52.5 %, pico 2007-02, valle 2020-09; drawdown vigente -5.4 %.

1) Sin recalcular.

Si la muestra empieza en 1963-07, no cambian el MDD, el pico ni el valle, y tampoco el drawdown vigente. El pico (2006-12) y el valle (2020-09) son posteriores a 1963. El drawdown en t es W_t/max(W_s, s \<= t). Si el máximo hasta el valle ya se alcanzaba en 2006-12, restringir s >= 1963 no lo cambia. Todos los demás drawdowns solo pueden quedar iguales o menos profundos, porque el máximo sobre un subconjunto es menor o igual. Rebasar el índice no altera los cocientes.

Si la muestra termina en 2015-12, el valle de 2020-09 queda fuera. Entonces el MDD tiene que ser menos profundo y el valle tiene que cambiar. El pico puede seguir siendo 2006-12, con un valle antes de 2016, o puede ser otro episodio anterior. Eso es precisamente 'depende del punto final'.

Transparencia: después lo verifiqué con el script. Termina en -43.7 %, de 1933-08 a 1935-03, así que cambian los tres, y ese episodio además desaparecería si también se empezara en 1963-07.

HML diario. No garantiza un MDD igual o más profundo; puede salir menos profundo. El HML mensual es 1/2(SH+BH) - 1/2(SL+BL) calculado con retornos mensuales buy-and-hold. Prod(1+h_d) no es igual a Prod(1+a_d) - Prod(1+b_d). Son dos estrategias distintas: el índice diario rebalancea las patas a igual valor cada día, y el mensual deja que deriven dentro del mes. El teorema de que muestrear más fino da un MDD más profundo vale solo para el mismo proceso de riqueza observado con más frecuencia. El índice mensual no es una submuestra del diario.

En caídas con tendencia, como el rally growth de 2018-2020, la versión mensual deja que crezca la pata corta ganadora, lo que es convexidad en contra. La diaria recorta la exposición tras cada pérdida y puede perder menos. En mercados que se revierten pasa lo contrario. También difieren el arrastre por volatilidad (-1/2 suma h_d^2 contra términos cruzados mensuales) y el tratamiento de deslistes y vintage de datos.

La comprobación correcta es valuar a mercado diariamente la estrategia de rebalanceo mensual, con retornos diarios de los 6 portafolios y pesos que derivan. Sus valores a fin de mes coinciden con el índice mensual, y ese sí tiene un MDD mayor o igual.

2) Colateral. Aproximadamente, 1 + DD_{HML+RF}(t) = (1 + DD_HML(t)) x Prod_{pico..t}(1+RF), de modo que el efecto crece con el tiempo transcurrido desde el pico y con el nivel de tasas.

Hasta el valle, la T-bill promedió 3.1 % en 2007-08, 0.04 % en 2009-15 y 1.1 % en 2016-20, con acumulado de +12.5 %: 0.422 x 1.125 = 0.475, es decir, -52.5 %. Después, en 2021-2026-07 el acumulado es +19.2 % (3.8 % promedio en 2022-26): 0.704 x 1.125 x 1.192 = 0.944, aprox. -5.6 %. La cifra reportada es -5.4 % por el cambio del pico a 2007-02 y los términos cruzados. El MDD se alcanzó en la época de tasa cero; el drawdown vigente suma 19.5 años, incluidos cuatro con bills de 4-5 %. Cerca del 80 % de la 'casi recuperación' viene de los intereses, no del value.

¿Qué acerca la versión invertible a HML puro? Para HML+RF hace falta que el producto del corto financie íntegro el largo (rebate igual a RF) y que todo el capital gane RF sin haircut. En la realidad:

- Un inversionista minorista casi no recibe rebate por el corto, y su efectivo en la casa de bolsa gana muy por debajo de la T-bill.

- Con Reg-T, el colateral es el propio largo y el producto del corto queda retenido (margen de 150 % sobre el corto), así que no hay efectivo libre ganando RF.

- El largo apalancado paga tasa de margen de RF más un spread.

- Pedir prestado cuesta desde algunas décimas al año (general collateral) hasta varios puntos en nombres difíciles de pedir prestados, justo del tipo small growth de la pata corta.

- A eso se suman los costos de rotación.

El resultado para un minorista se parece a HML menos costos, o algo peor. Un institucional queda cerca de HML + RF menos spreads.

3) Ruina con apalancamiento k y rebalanceo mensual. La riqueza llega a cero si 1 + k h_t \<= 0, es decir, k\* = 1/|mín h|. El peor mes es -13.83 % (2020-03), así que k\* = 7.23 (7.24 con RF). Para un corto en HML, el mejor mes es +35.52 % (1932-07), así que |k| >= 2.82 (7.78 si solo se usa la muestra desde 1963).

La no linealidad: MDD(2x) = -84.7 %, no -115.6 %; MDD(3x) = -95.3 %; MDD(5x) = -99.8 %; MDD(6x) = -99.97 % (de 1927-05 a 1940-05). La secuencia arruina antes de llegar al umbral de un solo mes. El log de la riqueza terminal alcanza su máximo cerca de 3x (Kelly mu/sigma^2 = 2.8) y luego cae. Con datos mensuales, 7.23 es una cota superior: dentro del mes las pérdidas acumuladas y los margin calls muerden antes.

Script: s3.py en el scratchpad.

**Juicio: deducción de 0.** La defensa sostiene la respuesta, y confirmé sus cifras. Empezar en 1963-07 no cambia el MDD (-57.78 %), el pico (2006-12), el valle (2020-09) ni el drawdown vigente (-29.57 %). Terminar en 2015-12 cambia los tres: -43.67 %, de 1933-08 a 1935-03. El argumento sin recalcular (máximo sobre un subconjunto) es correcto, y además aclara que la verificación vino después. Responde bien lo del HML diario: no garantiza un MDD más profundo porque es otra estrategia (rebalanceo diario contra deriva mensual), y la afirmación sobre las caídas intra-mes solo vale para valuar a mercado la misma estrategia. La descomposición del colateral, (1+DD) aprox. (1+DD_HML) x Prod(1+RF), con RF acumulado de +12.5 % hasta el valle y +19.2 % después, explica por qué el MDD casi no cambia y el drawdown vigente sí: -52.47 % y -5.44 % verificados. Sus supuestos realistas sobre rebate, Reg-T y el costo de pedir prestado son adecuados. k\* = 1/0.1383 = 7.23 es correcto, el mejor mes es 1932-07 con +35.52 %, y los MDD apalancados coinciden: -84.7 %, -95.3 %, -99.8 % y -99.97 %.

### Puntaje final

**5.0/5** = 5.0 (promedio de A y B), sin deducción.

### Hueco

**Ninguno.** Cálculo exacto, convención correcta y las dos advertencias completas. En la defensa precisó que "con datos mensuales subestima las caídas intra-mes" vale solo para valuar a mercado diariamente la misma estrategia mensual, no para un HML construido con datos diarios, que es otra estrategia. El juez no descontó.

---

## S6-04 — Correlacion condicional en caidas y sesgo de condicionamiento (EUA frente a Europa) (laboratorio)

### Enunciado

Archivos en /home/user/New1/laboratorio/examen-datos/S6/: (1) F-F_Research_Data_Factors_CSV.zip, SHA256 b840dba55d319f4818fc7300e65c52eff5f64870c8d495fa58ff5d4cd749f5eb, bloque mensual, columna Mkt-RF: es X, el mercado de EUA. (2) Europe_3_Factors_CSV.zip, SHA256 529b7f1909b91343d02ad48b51f09dd137d38dd542f74d8c577c3872c2b6585a, CSV Europe_3_Factors.csv, bloque mensual, columna Mkt-RF: es Y, Europa, en USD menos la T-bill de EUA. Ventana: 1990-07 a 2025-12 (n = 426). Calcula: (a) la correlacion de Pearson rho de X y Y en toda la muestra; (b) rho_down en los meses con X \< 0 (reporta el numero de meses) y rho_up en los meses con X >= 0; (c) el benchmark de Boyer, Gibson y Loretan (1997) bajo normalidad bivariada: rho_A = rho \* [rho^2 + (1 - rho^2) \* Var(X)/Var(X | A)]^(-1/2), con varianzas muestrales (n-1) de X en la muestra completa y en el subconjunto A, para A = {X\<0} y A = {X>=0}; (d) interpreta: la correlacion en caidas, ¿es 'mayor' o 'menor' de lo esperado, y contra que referencia? (e) una prueba aproximada (z de Fisher) de rho_down contra su benchmark, y sus limitaciones.

### Clave (descifrada)

(a) rho = 0.7948 (n = 426). (b) Meses con X\<0: 154, rho_down = 0.7574. Meses con X>=0: 272, rho_up = 0.5625. (c) Var(X) = 19.18; Var(X | X\<0) = 10.16; cociente = 1.887, benchmark_down = 0.690. Cociente para X>=0 = 3.185, benchmark_up = 0.592. (d) La lectura ingenua ('en las caidas la correlacion baja, porque 0.757 \< 0.795') es incorrecta. Truncar X reduce mecanicamente su varianza y por lo tanto la correlacion condicional, aun con correlacion poblacional constante. La referencia correcta es el benchmark: en caidas se observa 0.757 contra 0.690 esperado, que es una correlacion MAYOR a la implicada por el condicionamiento. En alzas se observa 0.563 contra 0.592, algo menor. Esto es evidencia de correlacion asimetrica (Longin y Solnik 2001; Ang y Chen 2002): la diversificacion entre EUA y Europa rinde menos justo cuando mas se necesita. (e) z = (atanh 0.7574 - atanh 0.6901)\*raiz(154-3) = 1.75. Con p bilateral de aprox. 0.08 no se rechaza al 5 %: la evidencia es sugestiva, no concluyente. Limitaciones: la prueba trata el benchmark como conocido (fue estimado), supone observaciones independientes (hay heterocedasticidad condicional y agrupamiento de volatilidad) y supone normalidad (hay colas gruesas). Ademas, Y incluye el efecto de las monedas europeas contra el USD.

**Rúbrica:** 5 puntos. 1 pt: rho 0.795 y rho_down 0.757 (+/-0.005) con n = 154. 1 pt: rho_up 0.563. 1 pt: formula BGL y benchmark 0.690 (y 0.592). 1 pt: interpretacion correcta, comparando contra el benchmark y no contra la rho incondicional. 1 pt: z de Fisher aprox. 1.75 y sus limitaciones (benchmark estimado, dependencia, colas, moneda). Afirmar que 'la correlacion baja en crisis' sin el benchmark resta 2 pt.

**Valor numérico comprometido:** 0.757 ± 0.005. **Huella SHA256:** `aec8990c7f7754ed6e75524a068de1c9303742e655582ab5169a71f627f5ce42` (coincide con el compromiso).

### Fuente

Kenneth R. French Data Library: F-F_Research_Data_Factors_CSV.zip (CRSP 202607) y Europe_3_Factors_CSV.zip (Bloomberg 202608), https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/, descargados el 2026-09-25. Boyer, B., Gibson, M. y Loretan, M. (1997, rev. 1999), 'Pitfalls in Tests for Changes in Correlations', Federal Reserve IFDP 597, Teorema 1, ec. (1), verificada en https://www.federalreserve.gov/pubs/ifdp/1997/597/ifdp597.pdf. Longin y Solnik (2001), JF 56(2); Ang y Chen (2002), JFE 63(3).

### Respuesta del sustentante (completa)

DATOS: X = Mkt-RF de F-F_Research_Data_Factors.csv; Y = Mkt-RF de Europe_3_Factors.csv (bloque 199007-202608). Ventana 1990-07 a 2025-12, n = 426, fechas identicas y sin faltantes. Calculo propio.

(a) rho = 0.795.

(b) rho_down (X\<0) = 0.757 con 154 meses; rho_up (X>=0) = 0.563 con 272 meses.

(c) Var(X) = 19.177. Var(X|X\<0) = 10.160, cociente 1.887 -> benchmark BGL rho_down\* = 0.795\*[0.795^2 + (1-0.795^2)\*1.887]^(-1/2) = 0.690. Var(X|X>=0) = 6.021, cociente 3.185 -> rho_up\* = 0.592.

(d) Contra la correlacion incondicional (0.795), la de caidas es MENOR. Condicionar en un subconjunto de X con menor varianza reduce mecanicamente la correlacion (sesgo de truncamiento/heterocedasticidad), y por eso ambas condicionales quedan abajo de 0.795. Contra la comparacion ingenua caidas-vs-alzas (0.757 vs 0.563; z = 3.48), la asimetria parece enorme, pero esa referencia esta sesgada. La referencia correcta es el benchmark BGL: lo que daria una normal bivariada con correlacion constante dada la varianza condicional. Contra el, rho_down es MAYOR de lo esperado (+0.067) y rho_up es algo menor (-0.029). La mitad de la brecha ingenua (0.098 de 0.195) es mecanica; el exceso genuino en caidas es de \~0.07. Esto es consistente con Longin-Solnik (2001), citado en conocimiento/01-licenciatura-fundamentos.md (linea 153).

(e) z de Fisher: z = [atanh(0.7574) - atanh(0.6901)]\*raiz(154-3) = 1.745, p = 0.081 bilateral. No rechaza al 5 %. En alzas: z = -0.718, p = 0.473. Limitaciones: (1) el benchmark se estima con los mismos datos (rho y cociente de varianzas) y se trata como fijo, asi que el SE queda subestimado; (2) 1/raiz(n-3) supone pares iid normales bivariados, pero el subconjunto esta truncado en X y los rendimientos tienen colas pesadas (curtosis en exceso 1.09 y 1.46; asimetria -0.58 y -0.50) y agrupamiento de volatilidad; (3) la particion se hace solo por X, Y mezcla el tipo de cambio EUR/USD y hay cierres no sincronos; (4) se hacen dos pruebas (caidas y alzas). Sensibilidad (calculo propio adicional): un bootstrap iid de meses que re-estima el benchmark en cada replica da un IC95 de rho_down - benchmark de [0.008, 0.126], que excluye el 0. La conclusion es fronteriza y depende del metodo.

### Calificación automática

Dentro de tolerancia (esperado 0.757, obtenido 0.757, tol. 0.005).

### Calificación

**Calificador A: 5.0/5.** Verificado: rho 0.79484, rho_down 0.75740 (154 meses), rho_up 0.56253, Var 19.177/10.160/6.021, benchmarks BGL 0.6901 y 0.5917, z de Fisher 1.745. La interpretación es correcta: compara contra el benchmark BGL y explica que la caída respecto a la rho incondicional es mecánica, así que no incurre en la penalización. Las limitaciones están completas (benchmark estimado, dependencia y agrupamiento de volatilidad, colas, moneda, pruebas múltiples). Los extras verificados: z ingenua 3.48, curtosis 1.09/1.46 y asimetría -0.58/-0.50. Mi bootstrap da un IC de [0.0088, 0.1265], que coincide con el suyo. La cita a Longin-Solnik en conocimiento/01, línea 153, existe.

**Calificador B: 5.0/5.** Verificado con python3: rho 0.79484, 154 meses bajistas, rho_down 0.75740, rho_up 0.56253. Cocientes de varianza 1.887 y 3.185, benchmarks 0.6901 y 0.5917, z de Fisher 1.745. Todo coincide. La interpretación es la correcta: la comparación contra la rho incondicional y la comparación ingenua caídas-alzas están sesgadas; contra el benchmark BGL, rho_down es MAYOR (+0.067). No incurre en la penalización de 'la correlación baja en crisis', porque presenta esa lectura como sesgada. Las limitaciones están completas (benchmark estimado, dependencia y agrupamiento de volatilidad, colas y asimetría, moneda y cierres no síncronos, pruebas múltiples). La cita de Longin-Solnik en conocimiento/01, línea 153, existe.

**Promedio A-B: 5.0/5** (|A − B| = 0; sin arbitraje).

### Defensa oral

**Repreguntas:**

1. El benchmark BGL supone que Y es lineal en X, con un error de varianza constante independiente de X. Si Var(Y|X) aumenta cuando X es muy negativo (volatilidad común tipo GARCH), ¿tu 'exceso genuino' de \~0.07 es contagio o una violación del supuesto de homocedasticidad del benchmark? Otra pregunta: ¿obtendrías el mismo benchmark y la misma conclusión condicionando en Y\<0 en lugar de X\<0? Por último, Y está en USD y el dólar suele apreciarse en las crisis. ¿Cuánto del exceso de correlación en caídas podría ser el componente cambiario y no las acciones europeas? ¿Cómo lo aislarías?
2. En la limitación (1) dices que tratar el benchmark como fijo subestima el SE. Sin embargo, tu bootstrap, que sí re-estima el benchmark en cada réplica, da un intervalo que excluye el 0, mientras que la z de Fisher no rechaza. ¿Cómo reconcilias eso? Toma en cuenta la covarianza muestral entre rho_down y su propio benchmark, y explica si la limitación (1) apunta en la dirección correcta. ¿Qué esperarías de un bootstrap por bloques que preserve el agrupamiento de volatilidad? Además, tu partición en el signo de X (umbral 0), ¿prueba lo mismo que las correlaciones de excedencia en las colas de Longin-Solnik? ¿Qué predice la normal bivariada para esas correlaciones cuando el umbral se va a -infinito?

**Respuesta del sustentante:**

Base. X = Mkt-RF de EUA; Y = Mkt-RF de Europa en USD; datos mensuales de 1990-07 a 2026-07, n=433; rho = 0.795. Con X\<0 (n=158): rho_down = 0.759 y BGL = 0.688, así que el exceso es 0.071 (Fisher z = 1.87).

1) ¿Heteroscedasticidad o contagio? Descompongo rho_A = b_A sd(X|A)/raíz(b_A^2 Var(X|A) + s_A^2). La pendiente conjunta es b = 0.892 con s^2 = 8.92; en caídas (X\<0), b = 1.055 y s^2 = 8.27; en alzas (X>=0), b = 0.829 y s^2 = 9.16. En contrafactual: con la b conjunta y la s^2 de caídas, la correlación es 0.701 (+0.013); con la b de caídas y la s^2 conjunta, es 0.746 (+0.058). Alrededor de 80 % del exceso viene de una pendiente mayor en caídas, es decir, de no linealidad en E[Y|X] (los residuos medios son -0.59 en X \<= p10 y -0.50 en X > p90: la relación es cóncava). Solo cerca de 20 % viene de menor varianza residual.

La hipótesis tipo GARCH se cumple en los datos: la varianza residual por tramo de X es 13.5 en X \<= p10, 5.2, 7.4, 7.8, 10.3 y 12.2 en X > p90. Tiene forma de U y es casi simétrica. Pero una Var(Y|X) mayor en caídas baja rho_down respecto al benchmark: no puede fabricar un exceso positivo, y si acaso lo enmascara. El 0.07 viola la linealidad, no la homocedasticidad. Aun así, 'contagio' exige más: una beta que sube en crisis también puede venir de un factor global común con volatilidad variable.

Condicionando en Y\<0 (n=183): rho = 0.694 y BGL = 0.692, exceso 0.003, prácticamente cero. La conclusión no es invariante: bajo normalidad los papeles de X y Y son simétricos, y aquí no lo son. Los meses con Y\<0 incluyen caídas europeas propias o cambiarias sin caída en EUA. La diferencia de excesos es 0.069 con IC bootstrap [-0.007, 0.146], limítrofe, así que no afirmo una dirección.

Divisa. Y_usd aprox. Y_local + e, de modo que Cov(Y_usd, X | A) = Cov(Y_local, X | A) + Cov(e, X | A). Si el dólar se aprecia cuando X\<0, el término cambiario sube b_down en Cov(e, X|A)/Var(X|A). En examen-datos/S6 no hay EUR/USD ni índices europeos en moneda local (solo MXN), así que no lo puedo cuantificar y no invento cifras. Lo único que sugieren los datos: en 2008-10, Europa cae -22.0 frente a -17.2 de EUA medido en USD. Para aislarlo: traer H.10 (DEXUSEU, DEXUSUK, DEXSZUS) ponderados por capitalización; calcular Y_local = (1+Y_usd)/(1+e) - 1 y la versión cubierta (Y_local más la prima forward); repetir BGL sobre Y_local y sobre e; y estimar Y = a + b_d X 1(X\<0) + b_u X 1(X>=0) + c_d e 1(X\<0) + c_u e 1(X>=0), para ver qué parte de b_d - b_u absorbe la divisa.

2) Fisher contra bootstrap. El SE de Fisher con benchmark fijo es (1-rho^2)/raíz(n-3) = 0.034. El bootstrap iid (5,000 réplicas) da sd(rho_down) = 0.043 (más que Fisher, por colas gruesas y truncamiento), sd(BGL) = 0.040 y corr(rho_down, BGL) = 0.75. Por lo tanto sd(exceso) = raíz(0.043^2 + 0.040^2 - 2(0.75)(0.043)(0.040)) = 0.029, que es menor que 0.034. El IC percentil es [0.013, 0.127] y P(exceso \<= 0) = 0.9 %.

La submuestra de caídas es parte de la muestra total, así que el ruido de rho_down, de rho_total y del cociente de varianzas es común y se cancela en la diferencia. Mi limitación (1) apuntaba en la dirección equivocada. Fijar el benchmark ignora Var(BGL), lo que subestima el SE, pero también ignora la covarianza positiva, lo que lo sobrestima, y aquí domina la covarianza. La prueba de Fisher era conservadora.

Bootstrap por bloques circulares de 6, 12 y 24 meses: sd(rho_down) sube a 0.047-0.049, pero la correlación con el BGL también sube (0.80-0.84), y sd(exceso) queda en 0.026-0.031. Con bloques de 24, el IC es [0.011, 0.134]. El agrupamiento de volatilidad infla cada correlación, pero de forma común a ambas. Salvedad: pocas crisis (1998, 2001-02, 2008, 2020) dominan el resultado.

Longin-Solnik. La partición en el signo de X no prueba colas: compara mitades, y la mayoría de los meses con X\<0 son caídas leves. La correlación de excedencia condiciona en ambas variables más allá de un umbral theta (en unidades estandarizadas). Empírico contra normal con rho = 0.795:

- theta = -2: 0.72 (n=12) contra 0.35

- theta = -1.5: 0.65 contra 0.40

- theta = -1: 0.68 contra 0.46

- theta = -0.5: 0.79 contra 0.52

- theta = +0.5: 0.49 contra 0.52

- theta = +1: 0.33 contra 0.46

Es el patrón asimétrico de Longin-Solnik, y es una evidencia más fuerte que el exceso de 0.07, aunque con n chico.

Para la normal bivariada con |rho| \< 1, la correlación de excedencia tiende a 0 cuando theta tiende a -infinito (independencia asintótica en colas). Lo mismo le pasa a corr(X,Y | X \< theta): 0.62 en 0, 0.51 en -1, 0.41 en -2 y 0.32 en -3. Nota: el BGL empírico (0.688) supera al 0.619 normal porque la cola izquierda de X es más gruesa, de modo que el benchmark ya absorbe en parte la no normalidad de X.

Scripts: s4.py, s4b.py y s4c.py en el scratchpad.

**Juicio: deducción de 0.5.** Con la muestra a 2026-07 (n=433) reproduje sus cifras: rho = 0.795, rho_down = 0.759, BGL = 0.687 y z aprox. 1.89. Con Y\<0 (n=183) el exceso es de apenas 0.003, como afirma. La descomposición pendiente contra varianza residual es consistente: cerca de 80 % del exceso viene de una beta mayor en caídas. También argumenta bien que una varianza condicional en U casi simétrica no puede fabricar un exceso positivo, así que el 0.07 viola la linealidad y no la homocedasticidad, y reconoce que un factor global con volatilidad variable no equivale a contagio. Es honesto con la divisa: no tiene datos EUR/USD y propone cómo aislarla. Los valores de excedencia bajo la normal (0.35, 0.40, 0.46, 0.52) son correctos, igual que el límite cero cuando theta tiende a -infinito. Quito medio punto porque la limitación (1) del original, que fijar el benchmark subestima el SE, apuntaba en la dirección equivocada: la covarianza entre rho_down y el BGL (0.75) hace que la prueba de Fisher sea conservadora. La defensa lo retira bien, pero esa parte del original se cae.

### Puntaje final

**4.5/5** = 5.0 (promedio de A y B) − 0.5 (defensa oral).

### Hueco

**Ante A y B: sin pérdida.** Cálculo exacto, interpretación contra el benchmark BGL y sin caer en la penalización de "la correlación baja en crisis".

**Se cayó en la defensa (−0.5):** la limitación (1) de (e), "tratar el benchmark como fijo subestima el SE", apuntaba en la dirección equivocada. La respuesta ya tenía la evidencia en contra (su bootstrap, que re-estima el benchmark, excluía el 0 mientras Fisher no rechazaba) y no lo reconcilió. La correlación positiva entre rho_down y su propio benchmark (≈ 0.75) reduce la varianza de la diferencia, así que la prueba de Fisher con benchmark fijo resulta conservadora. Ninguno de los dos calificadores lo detectó.

**Nota:** en la defensa usó la muestra hasta 2026-07 (n = 433, 158 meses con X \< 0) en lugar de la ventana del examen (n = 426, 154 meses); el juez reprodujo sus cifras con esa muestra. No cambia nada de lo calificado.

---

## S6-05 — Rendimientos en MXN con tipo de cambio alineado (GLD en pesos) (laboratorio)

### Enunciado

Archivos en /home/user/New1/laboratorio/examen-datos/S6/: (1) yahoo_GLD_1d.json, SHA256 75bdedb2b98d7ebe0f72568e11dbc6da3063407cb025d8d680ed15b40e07dc8d. Estructura Yahoo chart v8: chart.result[0].timestamp (epoch UTC), convertido a fecha en America/New_York (meta.exchangeTimezoneName); precio = indicators.adjclose[0].adjclose (GLD no paga dividendos). (2) dbnomics_FED_H10_RXI_N.B.MX.csv, SHA256 9b35dd88d46767f89ad6e384d8934e9586670cc26637dbefff653cd27ab14502: columnas period y valor, en MXN por USD. Es la tasa 'noon buying rate' de Nueva York de la Fed (H.10), la misma fuente que FRED DEXMXUS. 'NA' marca un dato faltante. Regla de alineacion: para cada mes calendario, la fecha de cierre es la ULTIMA fecha del mes con precio de GLD Y tipo de cambio H.10 no faltante. P_MXN = P_USD \* FX en esa misma fecha. Rendimientos mensuales simples de 2005-01 a 2025-12 (base 2004-12; n = 252). Calcula: (a) los meses en que la fecha alineada no es el ultimo dia de negociacion de GLD, y por que; (b) el CAGR en USD, en MXN y del tipo de cambio, [P_fin/P_ini]^(12/n) - 1, y la identidad que los liga; (c) la volatilidad anualizada (desviacion estandar muestral mensual \* raiz(12)) en USD, en MXN y del tipo de cambio, y corr(r_USD, r_FX); (d) el drawdown maximo mensual (sobre los 253 cierres alineados) en USD y en MXN, con meses de pico y valle; (e) interpreta por que la volatilidad en MXN es mayor que en USD aunque la correlacion sea negativa, y senala un desalineamiento residual del metodo.

### Clave (descifrada)

(a) Dos meses: 2010-12 (se usa 2010-12-30, porque H.10 es NA el 2010-12-31) y 2021-12 (2021-12-30, porque H.10 es NA el 2021-12-31). En ambos casos es el feriado federal de EUA que se recorre al viernes 31 cuando Anio Nuevo cae en sabado: el NYSE abrio, pero la Fed no publico. (b) Extremos: 2004-12-31, GLD 43.80 y FX 11.154; 2025-12-31, GLD 396.31 y FX 18.0057. CAGR USD = 11.06 %; CAGR del tipo de cambio = 2.31 %; CAGR MXN = 13.62 %. Identidad: (1.11058)(1.02307) = 1.13620. (c) Volatilidad en USD 16.69 %, en MXN 18.24 % y del tipo de cambio 11.50 %; corr(r_USD, r_FX) = -0.215. (d) En USD, MDD = -42.91 % (pico 2011-08, valle 2015-12). En MXN, MDD = -34.45 % (pico 2011-11, valle 2014-10). (e) Var(r_MXN) aprox. Var_USD + Var_FX + 2 Cov = 278.6 + 132.2 - 82.7 = 328.1, es decir aprox. 18.1 % de volatilidad; el termino cruzado r_USD\*r_FX lleva la cifra exacta a 18.24 %. La correlacion negativa (el oro en USD sube cuando el peso se deprecia poco, y viceversa) solo compensa en parte la varianza propia del tipo de cambio, que es grande. En cambio, el peso redujo el drawdown y agrego unos 2.3 pp al anio de rendimiento en MXN. Desalineamiento residual: H.10 es la tasa del mediodia de NY y el cierre de GLD es a las 16:00 de NY, una diferencia de 4 horas. Se ignoran impuestos, la comision de GBM, el diferencial cambiario del SIC y la cotizacion GLD\*.MX.

**Rúbrica:** 5 puntos. 1 pt: identifica 2010-12 y 2021-12 con la causa correcta. 1 pt: CAGR MXN 13.62 (+/-0.03) mas USD 11.06, tipo de cambio 2.31 e identidad. 1 pt: volatilidades 16.69 / 18.24 / 11.50 y correlacion -0.215. 1 pt: MDD en ambas monedas con meses correctos. 1 pt: descomposicion de varianza y desalineamiento mediodia contra cierre. Si se alinea por separado (ultimo dia de GLD con el ultimo dia de FX), -1 pt.

**Valor numérico comprometido:** 13.62 ± 0.03. **Huella SHA256:** `077986137d7fc0f0132f965e6476a274c69b22a62b5b66538d4b6dd4c15bb69b` (coincide con el compromiso).

### Fuente

Yahoo Finance chart API, https://query1.finance.yahoo.com/v8/finance/chart/GLD?period1=0&period2=\<ahora>&interval=1d&events=div%2Csplits&includeAdjustedClose=true (User-Agent Mozilla/5.0), descargado el 2026-09-25 hacia las 05:44 UTC. Federal Reserve H.10 (serie RXI_N.B.MX, noon buying rates in New York; es la fuente de FRED DEXMXUS) via DBnomics, https://api.db.nomics.world/v22/series/FED/H10/RXI_N.B.MX?observations=1&format=csv, descargado el 2026-09-25 hacia las 05:49 UTC. FRED fredgraph.csv no respondio desde el entorno (conexion cerrada); el valor del 2026-03-27 (18.0240) coincide con el que publica FRED para DEXMXUS.

### Respuesta del sustentante (completa)

DATOS: yahoo_GLD_1d.json (5,496 dias, 2004-11-18 a 2026-09-24; timestamp -> America/New_York; adjclose sin nulos ni duplicados) y dbnomics_FED_H10_RXI_N.B.MX.csv ('NA' = faltante). Cierre del mes = ultima fecha con GLD y H.10 no faltante; P_MXN = P_USD\*FX. Son 253 cierres (2004-12 a 2025-12) y n = 252. Calculo propio.

(a) Solo en 2 meses la fecha alineada no es el ultimo dia de negociacion: 2010-12 (se usa 2010-12-30 en lugar del 31) y 2021-12 (2021-12-30 en lugar del 31). En el CSV, 2010-12-31 y 2021-12-31 son 'NA' (lineas 4476 y 7346). Ambos fueron viernes y el 1 de enero cayo en sabado. Por eso el feriado federal de Ano Nuevo se observo el viernes, la Fed no publico H.10 y el NYSE si opero [Inferencia sobre la causa, coherente con el calendario].

(b) CAGR USD = 11.058 % (43.80 -> 396.31). CAGR MXN = 13.620 %. CAGR FX = 2.307 % (11.154 -> 18.006). Identidad exacta, porque P_MXN = P_USD\*FX en las mismas fechas: (1+g_MXN) = (1+g_USD)(1+g_FX) -> 1.11058\*1.02307 = 1.13620.

(c) Volatilidad anualizada: USD 16.692 %, MXN 18.237 %, FX 11.498 %. corr(r_USD, r_FX) = -0.215.

(d) MDD mensual USD = -42.910 %, pico 2011-08, valle 2015-12, recuperacion 2020-07. MDD MXN = -34.449 %, pico 2011-11, valle 2014-10, recuperacion 2016-06. La depreciacion del peso de 2014-2015 amortiguo la caida en MXN.

(e) Varianza anualizada: Var_MXN \~ Var_USD + Var_FX + 2Cov = 0.02786 + 0.01322 - 0.00827 = 0.03281; la exacta es 0.03326 (el resto es el termino cruzado r_USD\*r_FX). La cobertura natural (2Cov = -0.83 puntos de varianza) es menor que la varianza que agrega el tipo de cambio (1.32). Para que la volatilidad en MXN fuera menor que en USD haria falta rho \< -sigma_FX/(2\*sigma_USD) = -0.344. La observada, -0.215, no es suficientemente negativa. Desalineamiento residual: adjclose de GLD es el cierre de NYSE a las 16:00 ET, mientras H.10 es la noon buying rate de las 12:00 ET. Hay 4 horas de diferencia, asi que P_MXN no es un precio que haya existido en un instante; ademas, en 2010-12 y 2021-12 el mes cierra un dia antes y el movimiento del dia 31 se pasa a enero. Tampoco es el precio de GLD en el SIC en pesos. Contexto del repo: laboratorio/alertas-de-datos.md, alertas 2 y 3.

### Calificación automática

Dentro de tolerancia (esperado 13.62, obtenido 13.62, tol. 0.03).

### Calificación

**Calificador A: 5.0/5.** Verificado con zoneinfo y alineación conjunta: 253 cierres; solo 2010-12 y 2021-12 cierran el día 30 (H.10 marca NA en las líneas 4476 y 7346, lo confirmé). CAGR USD 11.058, FX 2.307 y MXN 13.620, con identidad exacta. Volatilidades 16.692/18.237/11.498 y correlación -0.2154. MDD USD -42.91 % (2011-08 a 2015-12) y MXN -34.45 % (2011-11 a 2014-10). La descomposición de varianza es correcta, con el término cruzado y el umbral rho \< -sigma_FX/(2 sigma_USD), que es un buen extra. Explica el desfase mediodía contra 16:00 ET. Cumple todos los puntos.

**Calificador B: 5.0/5.** Verificado con python3 y zoneinfo: los meses desalineados son exactamente 2010-12 y 2021-12 (H.10 NA el 31), con la causa correcta (Año Nuevo en sábado observado el viernes). CAGR USD 11.058, MXN 13.620 y FX 2.307, con la identidad exacta. Volatilidades 16.692, 18.237 y 11.498; correlación -0.2154. MDD USD -42.91 % (2011-08 a 2015-12) y MXN -34.45 % (2011-11 a 2014-10). Todo coincide. La descomposición de varianza es correcta e incluye el término cruzado; el umbral rho \< -0.344 es un añadido válido. Señala el desfase de 12:00 contra 16:00 ET y el corrimiento de fin de mes. Alinea en conjunto, no por separado.

**Promedio A-B: 5.0/5** (|A − B| = 0; sin arbitraje).

### Defensa oral

No hubo defensa oral para esta pregunta (la defensa cubrió S6-01 a S6-04). Deducción: 0.

### Puntaje final

**5.0/5** = 5.0 (promedio de A y B), sin deducción.

### Hueco

**Ninguno.** Cumple los cinco puntos. Añade, correctamente, el umbral de correlación a partir del cual la volatilidad en MXN sería menor que en USD (rho \< −sigma_FX/(2·sigma_USD) = −0.344).

---

## S6-06 — Reconstruccion de HML y SMB de EUA desde sus 6 portafolios, y descomposicion de la prima de valor (laboratorio)

### Enunciado

Archivos en /home/user/New1/laboratorio/examen-datos/S6/: (1) 6_Portfolios_2x3_CSV.zip, SHA256 0b3f5ed2cb70809cbbc16cbb34355c5873b1076375bf45e3e6c6ddd9c5cb3e9c, CSV 6_Portfolios_2x3.csv, seccion 'Average Value Weighted Returns -- Monthly', columnas SMALL LoBM, ME1 BM2, SMALL HiBM, BIG LoBM, ME2 BM2, BIG HiBM (% mensual). (2) F-F_Research_Data_Factors_CSV.zip, SHA256 b840dba55d319f4818fc7300e65c52eff5f64870c8d495fa58ff5d4cd749f5eb, columnas SMB y HML. Reconstruye HML_rec = 1/2(SMALL HiBM + BIG HiBM) - 1/2(SMALL LoBM + BIG LoBM) y SMB_rec = 1/3(SMALL LoBM + ME1 BM2 + SMALL HiBM) - 1/3(BIG LoBM + ME2 BM2 + BIG HiBM). (a) En 1926-07 a 2026-07 (1201 meses), reporta el maximo de |HML_rec - HML| y de |SMB_rec - SMB|, y demuestra que la discrepancia es solo redondeo (los portafolios se publican con 4 decimales y los factores con 2). (b) En 1963-07 a 2025-12 (n = 750), calcula la media de HML_rec, y la media y el t de Newey-West de los diferenciales BIG HiBM - BIG LoBM y SMALL HiBM - SMALL LoBM. Usa NW con 6 rezagos, kernel de Bartlett, gamma_j = (1/n)\*suma (x_t - xbar)(x_{t-j} - xbar), S = gamma_0 + 2\*suma_{j=1..6}(1 - j/7)\*gamma_j y SE = raiz(S/(n-1)). (c) Calcula la fraccion de la media de HML que aporta la mitad de acciones pequenias, 1/2\*media(SMALL HiBM - SMALL LoBM)/media(HML_rec). (d) Explica la implicacion para un inversionista long-only de gran capitalizacion.

### Clave (descifrada)

(a) max|HML_rec - HML| = 0.0050 y max|SMB_rec - SMB| = 0.0050; correlaciones de 0.9999997 y 0.9999996. La cota por redondeo: los 4 insumos de HML tienen error de +/-0.00005 cada uno, lo que da 1/2\*4\*0.00005 = 0.0001, y el factor publicado a 2 decimales agrega +/-0.005, asi que la cota es 0.0051. Lo observado (0.0050) esta dentro de la cota: la reconstruccion es exacta salvo redondeo (lo mismo vale para SMB). (b) Media de HML_rec = 0.2861 %/mes (publicado: 0.2859). BIG HiBM - BIG LoBM: media 0.1694 %/mes, t_NW = 1.23 (t_IID 1.38), no significativo. SMALL HiBM - SMALL LoBM: media 0.4028 %/mes, t_NW = 2.82, significativo. (c) Mitad pequenia 0.2014 contra mitad grande 0.0847: la mitad pequenia aporta el 70.4 % de la media de HML. (d) La significancia historica de HML viene sobre todo de las acciones pequenias. La prima de valor en acciones grandes, que es lo que replica un ETF de valor de gran capitalizacion comprable en GBM, es de aprox. 2 % anual (x12) y no se distingue de cero con errores robustos. Ademas, el factor es largo-corto, sin costos y en USD. Es coherente con Fama y French (2012), Israel y Moskowitz (2013) y Loughran (1997).

**Rúbrica:** 5 puntos. 1 pt: formulas de reconstruccion correctas y maximos de 0.005. 1 pt: cota de redondeo (0.0051) y conclusion de exactitud. 1 pt: media de HML_rec 0.286 y t del diferencial grande 1.23 (+/-0.02). 1 pt: diferencial pequenio 0.403 con t 2.82 y fraccion de 70.4 %. 1 pt: implicacion para un inversionista long-only de gran capitalizacion. Usar la seccion equiponderada invalida los puntos numericos.

**Valor numérico comprometido:** 1.23 ± 0.02. **Huella SHA256:** `70ef4937f1574734af500dbf29668ccf01f03cd5786cc8e67e44eb1bba9ce789` (coincide con el compromiso).

### Fuente

Kenneth R. French Data Library: 6_Portfolios_2x3_CSV.zip y F-F_Research_Data_Factors_CSV.zip (CRSP 202607), https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/, descargados el 2026-09-25. Formulas SMB y HML textuales de https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_factors.html (verificado con WebFetch). Fama y French (1993), JFE 33: 3-56. Calculo propio en python3.

### Respuesta del sustentante (completa)

DATOS: 6_Portfolios_2x3.csv, seccion 'Average Value Weighted Returns -- Monthly' (lineas 15-1217, 192607-202607, 4 decimales verificados en el texto). F-F_Research_Data_Factors.csv, SMB y HML (2 decimales verificados). Calculo propio; la parte (a) se hizo con aritmetica Decimal exacta.

(a) En 1926-07 a 2026-07 (1,201 meses): max|HML_rec - HML| = 0.005, alcanzado en 7 meses empatados (1931-03, 1935-04, 1947-05, 1970-04, 1975-04, 1982-10 y 2021-12; p. ej. 2021-12: 3.2550 vs 3.25). max|SMB_rec - SMB| = 0.005 en 3 meses (1935-12, 1979-05 y 1986-06; p. ej. 1986-06: -0.9250 vs -0.93). Demostracion: cada portafolio tiene un error de redondeo |e_i| \<= 0.00005, y ambas reconstrucciones tienen suma de |pesos| = 2 (cuatro de 1/2, o seis de 1/3), asi que el error de reconstruccion es \<= 0.0001. El factor publicado tiene |e_f| \<= 0.005. La cota total es 0.0051 y el maximo observado (0.005) la respeta. Mas fuerte aun: al redondear HML_rec a 2 decimales se reproduce HML en 1,198/1,201 meses, y SMB en 1,199/1,201. Las 5 excepciones son empates exactos en x.xx50, donde el error de +/-0.0001 no decide el lado del redondeo. La media de |dif| es 0.0025, lo esperado para un error uniforme en +/-0.005. Es solo redondeo.

(b) En 1963-07 a 2025-12 (n = 750): media HML_rec = 0.286 %/mes (la publicada tambien es 0.286; t_NW 2.212). BIG HiBM - BIG LoBM: media 0.169, SE_NW 0.138, t_NW 1.232. SMALL HiBM - SMALL LoBM: media 0.403, SE_NW 0.143, t_NW 2.815.

(c) Fraccion de la mitad pequena = 0.5\*0.403/0.286 = 0.704 (70.4 %). Subperiodos (calculo propio): 1963-1991 da 0.607, y 1992-2025 da 0.850, con un diferencial grande de 0.063 (t 0.30).

(d) Un inversionista long-only de gran capitalizacion no cobra HML: solo accede a la pierna larga de las grandes. La prima de value entre grandes es de \~2.0 %/ano bruta y no significativa (t 1.23), y casi nula desde 1992. Frente al promedio de las grandes, BIG HiBM - promedio(BIG) = 0.127 %/mes (t 1.90), antes de TER, comisiones (0.29 % por lado en GBM, arena/investigacion/01-gbm-operativa-y-costos.md), impuestos y error de seguimiento. El 70 % de la media de HML viene de acciones pequenas, que son menos liquidas y tienen menos capacidad. Usar las t de HML para justificar una inclinacion value en grandes sobreestima la prima alcanzable [Inferencia].

### Calificación automática

Fuera de tolerancia (esperado 1.23, obtenido 0.704, tol. 0.02). **Falso negativo del extractor:** tomó la fracción de (c). Recálculo del notario: t_NW del diferencial grande = 1.2317. La respuesta dice "BIG HiBM - BIG LoBM: media 0.169, SE_NW 0.138, t_NW 1.232", dentro de la tolerancia. No se aplica ningún tope.

### Calificación

**Calificador A: 5.0/5.** Verificado: max|dif| 0.0050 en HML y en SMB; media HML_rec 0.28610 (t_NW 2.212); BIG 0.16940 con t_NW 1.2317; SMALL 0.40280 con t_NW 2.8152; fracción 0.70395. El 'fuera de tolerancia' es un error de extracción: el calificador tomó 0.704, que es la fracción de (c), en lugar del t del diferencial grande. La respuesta reporta t_NW 1.232, que coincide con la clave (1.23), así que no aplico el tope. La derivación de la cota de 0.0051 es correcta, y los extras están verificados (subperiodos 0.607/0.850, diferencial grande 1992+ 0.063 con t 0.30, BIG HiBM - promedio de BIG 0.127 con t 1.90). La implicación para un inversionista long-only de gran capitalización está bien argumentada, y la cita de costos de GBM existe.

**Calificador B: 5.0/5.** El 'fuera de tolerancia' es un falso negativo del extractor: tomó la fracción 0.704. La respuesta reporta t_NW = 1.232 para BIG HiBM - BIG LoBM, y mi recálculo en python3 da 1.2317; la clave es correcta y la respuesta coincide. (a) Máximos de 0.005 en ambos; cota 0.0001 + 0.005 = 0.0051 bien derivada, con la conclusión de redondeo puro. (b) HML_rec 0.2861; diferencial grande 0.1694, t 1.232; diferencial pequeño 0.4028, t 2.815 (verificado). (c) 70.4 %. (d) Buena implicación para un inversionista long-only de gran capitalización. Extras verificados: BIG HiBM - promedio de las grandes 0.127, t 1.90; subperiodos 0.607/0.850; diferencial grande en 1992-2025 de 0.063, t 0.30. La cita de costos de GBM existe. Usa la sección VW correcta.

**Promedio A-B: 5.0/5** (|A − B| = 0; sin arbitraje).

### Defensa oral

No hubo defensa oral para esta pregunta (la defensa cubrió S6-01 a S6-04). Deducción: 0.

### Puntaje final

**5.0/5** = 5.0 (promedio de A y B), sin deducción.

### Hueco

**Ninguno.** Cumple los cinco puntos. La calificación automática marcó "fuera de tolerancia" por un error de extracción (ver arriba).

---

## S6-07 — Comparacion de ventanas antes y despues de la publicacion (efecto tamanio: Banz 1981 con SMB) (laboratorio)

### Enunciado

Archivo: /home/user/New1/laboratorio/examen-datos/S6/F-F_Research_Data_Factors_CSV.zip, SHA256 b840dba55d319f4818fc7300e65c52eff5f64870c8d495fa58ff5d4cd749f5eb; CSV F-F_Research_Data_Factors.csv, bloque mensual, columna SMB (% mensual). Banz, 'The relationship between return and market value of common stocks', se publico en el Journal of Financial Economics 9(1): 3-18, en marzo de 1981, con una muestra de acciones del NYSE de 1936 a 1975. Define tres ventanas: A = 1936-01 a 1975-12 (muestra de Banz, n = 480); B = 1976-01 a 1981-03 (fuera de muestra antes de la publicacion, n = 63); C = 1981-04 a 2025-12 (despues de la publicacion, n = 537). Para cada ventana calcula la media, el SE de Newey-West(6) y su t. Usa kernel de Bartlett, gamma_j = (1/n)\*suma (x_t - xbar)(x_{t-j} - xbar), S = gamma_0 + 2\*suma_{j=1..6}(1 - j/7)\*gamma_j y SE = raiz(S/(n-1)). Luego calcula d = media_C - media_A, SE_d = raiz(SE_A^2 + SE_C^2) (muestras tratadas como independientes), t_d e IC95 = d +/- 1.96\*SE_d. Interpreta: ¿se puede afirmar que la publicacion 'mato' la prima de tamanio? Explica por que SMB no es la variable que midio Banz y que implica eso para la comparacion.

### Clave (descifrada)

A (1936-01 a 1975-12): media 0.1574 %/mes, SE 0.1431, t = 1.10. B (1976-01 a 1981-03): media 1.2232 %/mes, SE 0.2954, t = 4.14. C (1981-04 a 2025-12): media 0.0099 %/mes, SE 0.1195, t = 0.08. d = C - A = -0.1476 %/mes; SE_d = 0.1864; t_d = -0.79; IC95 = [-0.513, +0.218]. Interpretacion: despues de la publicacion la prima SMB es practicamente cero, pero la diferencia contra la muestra de Banz no es significativa, porque la propia SMB en 1936-1975 era debil (t = 1.10). Con esta medida no se puede afirmar que la publicacion la haya eliminado. Lo que hizo famoso al efecto tamanio fue la racha 1976-1981 (aprox. 14.7 % anual x12), justo antes de la publicacion. Eso es coherente con que la atencion academica llega despues de periodos excepcionales, y con el patron de McLean y Pontiff (2016). SMB no es la variable de Banz: SMB es un diferencial ponderado por valor entre mitades definidas por la mediana del NYSE, promediado sobre 3 terciles de B/M. El efecto de Banz se concentraba en las empresas MAS pequenias ('the main effect occurs for very small firms'). Comparar la prima publicada con SMB mezcla dos definiciones del efecto; lo correcto es replicar la definicion del articulo (deciles extremos) o declarar que se prueba otra hipotesis.

**Rúbrica:** 5 puntos. 1 pt: medias y t de A y C (0.157, t 1.10; 0.010, t 0.08). 1 pt: ventana B (1.22, t 4.14). 1 pt: d = -0.148 (+/-0.005), SE_d 0.186 y t -0.79 con la formula indicada. 1 pt: conclusion correcta (no se rechaza la igualdad; no se puede afirmar que la publicacion 'mato' la prima). 1 pt: explicacion de por que SMB difiere de la medida de Banz, y del papel de la racha previa a la publicacion.

**Valor numérico comprometido:** -0.1476 ± 0.005. **Huella SHA256:** `e34f1ee0ee5778e7a18aedf5ab78ded990fdcab351873118fc546ef0c4b23c65` (coincide con el compromiso).

### Fuente

Kenneth R. French Data Library, F-F_Research_Data_Factors_CSV.zip (CRSP 202607), descargado el 2026-09-25. Banz, R. W. (1981), JFE 9(1): 3-18, marzo de 1981 (https://ideas.repec.org/a/eee/jfinec/v9y1981i1p3-18.html); la muestra de 1936 a 1975 se confirmo con WebSearch. McLean, R. D. y Pontiff, J. (2016), JF 71(1): 5-32. Calculo propio en python3, verificado con la forma matricial de Bartlett.

### Respuesta del sustentante (completa)

DATOS: F-F_Research_Data_Factors.csv, SMB mensual. NW(6) con Bartlett y SE = raiz(S/(n-1)). Calculo propio.

A (1936-01 a 1975-12, n = 480): media 0.157 %/mes, SE_NW 0.143, t 1.100.

B (1976-01 a 1981-03, n = 63): media 1.223, SE_NW 0.295, t 4.141.

C (1981-04 a 2025-12, n = 537): media 0.010, SE_NW 0.119, t 0.082.

d = C - A = -0.148; SE_d = raiz(0.143^2 + 0.119^2) = 0.186; t_d = -0.791 (p = 0.43); IC95 = [-0.513, 0.218]. Las cifras de A y B coinciden con laboratorio/replicas/R03-salida.txt (lineas 26-27); alla POST llega a 2026-07 con 0.015 y t 0.13.

Interpretacion: NO se puede afirmar que la publicacion 'mato' la prima, por tres razones. (1) En la muestra de Banz, SMB ni siquiera era significativo (t_NW 1.10): no hay una prima establecida que pueda desaparecer. (2) La diferencia no es significativa y el IC es enorme: incluye desde una caida de 0.51 %/mes hasta un aumento de 0.22. El efecto minimo detectable con 80 % de potencia es \~2.8\*SE_d = 0.52 %/mes, mas de 3 veces la media de A. El 'decaimiento' de 94 % (1 - C/A) es un cociente de numeros ruidosos. (3) El episodio B (1.22 %/mes, t 4.14) y el colapso posterior es compatible con McLean-Pontiff (arbitraje tras la publicacion; resumen en R03), pero tambien con un ciclo de las acciones pequenas. Ademas, el articulo circulo antes de marzo de 1981 (recibido en junio de 1979 segun R03). La fecha de 'publicacion' es difusa.

Por que SMB no es la variable de Banz: Banz midio, con acciones del NYSE, la pendiente gamma_1 sobre el valor de mercado relativo en regresiones de corte transversal con control por beta (gamma_1 = -0.00052, t = -2.92). Su efecto se concentraba en las MUY pequenas: muy pequenas menos muy grandes = 1.52 %/mes (R03, seccion 1, verificado en el PDF por el sistema). SMB (Fama-French 1993) es otra construccion: ponderado por valor, con corte en la mediana del NYSE (la mitad 'small' incluye medianas), promediado entre tres grupos B/M (neutral a value) e incluyendo AMEX y NASDAQ. Diluye el efecto extremo y controla por otra variable. R03 lo advierte: con los articulos distintos de FF2015 solo se comparan signo y significancia, no magnitud. Implicacion: un SMB plano despues de 1981 no prueba nada sobre el efecto de Banz en microcaps, ni en un sentido ni en el otro. Para probarlo habria que replicar su variable (deciles de tamano del NYSE o regresiones con beta), que no esta en S6 [Inferencia].

### Calificación automática

Fuera de tolerancia (esperado -0.1476, obtenido -0.791, tol. 0.005). **Falso negativo del extractor:** tomó t_d. Recálculo del notario: d = C - A = -0.14757 (SE_d = 0.18645). La respuesta dice "d = C - A = -0.148", dentro de la tolerancia. No se aplica ningún tope.

### Calificación

**Calificador A: 5.0/5.** Verificado: A 0.15742, SE 0.14312, t 1.100; B 1.22317, SE 0.29537, t 4.141; C 0.00985, SE 0.11949, t 0.082; d -0.14757, SE_d 0.18645, t_d -0.7915, IC [-0.513, 0.218]. El 'fuera de tolerancia' es un error de extracción: el calificador tomó -0.791, que es t_d. La respuesta reporta d = -0.148, dentro de la tolerancia de la clave, así que no aplico el tope. La conclusión es correcta: no se puede afirmar que la publicación 'mató' la prima, y el argumento de potencia (MDE aprox. 0.52) es correcto. Explica bien por qué SMB no es la variable de Banz. Los datos de Banz (gamma_1 -0.00052 con t -2.92; muy pequeñas menos muy grandes 1.52 %/mes; recibido en junio de 1979) están en R03 (líneas 27 y 348), y la cita a R03-salida.txt, líneas 26-27, existe. Comenta el papel de la racha B.

**Calificador B: 5.0/5.** El 'fuera de tolerancia' es un falso negativo del extractor: tomó t_d = -0.791. La respuesta dice d = -0.148, y python3 da d = -0.14757 y SE_d = 0.18645. La clave es correcta y la respuesta coincide. A: 0.157, t 1.100. B: 1.223, t 4.141. C: 0.010, t 0.082. t_d -0.791 e IC [-0.513, 0.218], todo verificado. Conclusión correcta: no se puede afirmar que la publicación 'mató' la prima; lo refuerza con potencia y MDE. La racha B está bien discutida (arbitraje contra ciclo, y fecha de circulación difusa). La explicación de SMB frente a Banz es completa (gamma_1, deciles extremos 1.52 %/mes, mediana del NYSE, VW, promedio sobre B/M, AMEX/NASDAQ). Las citas a R03 (línea 27: recepción en junio de 1979, gamma_1 -0.00052, t -2.92, 1.52 %) y a R03-salida.txt, líneas 26-27, existen y coinciden.

**Promedio A-B: 5.0/5** (|A − B| = 0; sin arbitraje).

### Defensa oral

No hubo defensa oral para esta pregunta (la defensa cubrió S6-01 a S6-04). Deducción: 0.

### Puntaje final

**5.0/5** = 5.0 (promedio de A y B), sin deducción.

### Hueco

**Ninguno.** Cumple los cinco puntos, con argumento de potencia (efecto mínimo detectable ≈ 0.52 %/mes) que la clave no pedía. La calificación automática marcó "fuera de tolerancia" por un error de extracción.

---

## S6-08 — Impacto de los costos de GBM (0.25 % + 16 % de IVA por lado) sobre una regla de rebalanceo con rotacion calculada (laboratorio)

### Enunciado

Archivos en /home/user/New1/laboratorio/examen-datos/S6/: yahoo_EWW_1d.json (SHA256 a2d69e0f91acb4dbdf7ee4a658a91a606eb9fc6069316f53a819c345d67fa5ff) y yahoo_TLT_1d.json (SHA256 e325d311f8bb7b6a28b0b40d2acbccf45df1a525b65bed746d56f896d60a4189). Fecha = timestamp convertido a America/New_York; precio = indicators.adjclose[0].adjclose. El cierre de mes es la ultima fecha de cada mes con adjclose no nulo de ambos. Rendimientos mensuales de 2003-01 a 2025-12 (base 2002-12-31, n = 276). Portafolio en USD con 60 % EWW y 40 % TLT; valor inicial 1 el 2002-12-31, sin cobrar la compra inicial. Estrategia M: rebalancea a 60/40 al cierre de cada mes de 2003-01 a 2025-11 (275 rebalanceos). Estrategia A: rebalancea solo al cierre de cada diciembre de 2003 a 2024 (22 rebalanceos). Entre rebalanceos los pesos derivan con los rendimientos. Costo de GBM: c = 0.25 % \* 1.16 = 0.29 % por lado sobre el monto operado. En cada rebalanceo, costo = c \* V \* suma_i |w_i^deriva - w_i^objetivo|, que es el monto operado de ambos lados; se descuenta de V y luego se fija 60/40 (convencion simplificada). Calcula para M y para A: CAGR bruto y neto ((V_final)^(12/n) - 1), el arrastre (bruto - neto) en puntos base por anio y la rotacion media anual de un solo sentido = suma(1/2 \* suma_i |dw_i|)/(n/12). Compara ambas estrategias netas, descompon la diferencia en efecto costo y efecto trayectoria, y verifica que el arrastre se aproxima a c por la rotacion de ambos lados.

### Clave (descifrada)

M (mensual): CAGR bruto 8.393 %, neto 8.285 %, arrastre de 10.8 pb por anio. Monto operado acumulado de ambos lados = 7.903 veces el portafolio, lo que da una rotacion de un solo sentido de 17.2 % anual y un costo medio de 0.0997 % anual. A (anual): bruto 8.773 %, neto 8.734 %, arrastre de 3.9 pb; operado acumulado 2.816 veces, rotacion de un solo sentido de 6.1 % anual. Neto A - neto M = +0.449 pp. De eso, 0.380 pp son efecto trayectoria (diferencia bruta) y solo 0.069 pp son efecto costo. Chequeo: c \* rotacion de ambos lados = 0.29 % \* 34.4 % = 0.0997 %, aprox. 10 pb, consistente con el arrastre medido. Referencias: comprar y mantener sin rebalanceo da 8.325 %; EWW 10.06 %; TLT 3.37 %; corr(EWW, TLT) mensual = -0.055. Interpretacion: con la comision de GBM el costo de rebalancear es de segundo orden (unos pb al anio). La diferencia entre frecuencias la domina la trayectoria de los rendimientos relativos (tendencia intra-anual frente a reversion), que es una sola realizacion y no se puede generalizar sin inferencia (bootstrap por bloques, por ejemplo). Faltan diferenciales de compra-venta, el tipo de cambio del SIC, impuestos (ISR sobre ganancias al vender) y comisiones minimas, que en montos pequenios pueden dominar.

**Rúbrica:** 5 puntos. 1 pt: alineacion de cierres, n = 276 y deriva de pesos correcta. 1 pt: rotacion de 17.2 % (M) y 6.1 % (A). 1 pt: arrastre de M de 10.8 pb (+/-0.3) y CAGR bruto y neto. 1 pt: estrategia A y descomposicion de la diferencia neta (trayectoria 0.38 contra costo 0.07). 1 pt: chequeo arrastre aprox. c \* rotacion y advertencias (una sola trayectoria, costos omitidos, impuestos). Si se omite el IVA (c = 0.25 %), el arrastre es de aprox. 9.3 pb: -1 pt.

**Valor numérico comprometido:** 10.8 ± 0.3. **Huella SHA256:** `f2a4f9f256645da3b8b7393729114f16fd21862bc4674ec04927e6287612ff9a` (coincide con el compromiso).

### Fuente

Yahoo Finance chart API v8 (EWW y TLT, interval=1d, includeAdjustedClose=true, User-Agent Mozilla/5.0), descargado el 2026-09-25 hacia las 05:44 UTC. Comisiones de GBM (0.25 % hasta 1 millon de MXN operados en 3 meses, por operacion, mas IVA): https://gbm.com/faqs/que-comisiones-cobran-al-invertir-en-gbm/ y https://www.rankia.mx/blog/casas-de-bolsa-de-mexico/7057487-analisis-gbm-apertura-cuenta-comisiones-opiniones (verificado con WebSearch/WebFetch). Simulacion propia en python3.

### Respuesta del sustentante (completa)

DATOS: yahoo_EWW_1d.json y yahoo_TLT_1d.json (fechas en America/New_York; adjclose; EWW tiene un nulo, el 2026-09-22, fuera de la ventana). Cierre de mes = ultima fecha con ambos adjclose no nulos; coincide con el ultimo dia de negociacion de cada ETF en todos los meses. Son 277 cierres (2002-12-31 a 2025-12-31), n = 276. Pesos que derivan con los rendimientos; costo = c\*V\*suma|w_deriva - w_obj| con c = 0.29 %, descontado antes de fijar 60/40; la compra inicial no se cobra. Calculo propio.

M (275 rebalanceos): V bruto 6.383 y neto 6.238. CAGR bruto 8.393 %, neto 8.285 %. Arrastre 10.797 pb/ano. Rotacion de un sentido 17.181 %/ano.

A (22 rebalanceos, dic-2003 a dic-2024): V bruto 6.917 y neto 6.861. CAGR bruto 8.773 %, neto 8.734 %. Arrastre 3.863 pb/ano. Rotacion 6.122 %/ano.

Comparacion neta: A supera a M por 0.449 pp/ano (M - A = -0.449). Efecto trayectoria (diferencia bruta) = -0.380 pp; efecto costo = -(10.797 - 3.863) pb = -0.069 pp. La suma cuadra con -0.449. El 85 % de la diferencia es trayectoria, no costos. Referencia sin rebalancear nunca: 8.325 %. [Inferencia: en esta muestra, dejar correr la deriva ayudo porque EWW rindio mucho mas (CAGR 10.06 % contra 3.37 % de TLT, correlacion -0.055) y el rendimiento relativo mensual tuvo autocorrelacion +0.12 en el rezago 1. Es un efecto de una sola trayectoria, no una ventaja confiable; el efecto costo si es estructural.]

Verificacion del arrastre: c\*2\*rotacion = 0.29 %\*2\*17.181 % = 9.965 pb en M, y 3.551 pb en A. El arrastre en CAGR es aproximadamente (1+CAGR bruto)\*c\*2\*rotacion: 1.0839\*9.965 = 10.80 pb (observado 10.797) y 1.0877\*3.551 = 3.86 pb (observado 3.863). Dos lados multiplicado por la rotacion de un sentido es igual a suma|dw| operada. El factor (1+g) aparece porque el costo se cobra sobre el nivel de V mientras el CAGR mide crecimiento. El costo por lado de 0.25 % + IVA viene de arena/investigacion/01-gbm-operativa-y-costos.md (linea 17). Ese calculo no incluye spread (0.10-0.60 %, misma fuente), impuestos ni tipo de cambio.

### Calificación automática

Fuera de tolerancia (esperado 10.8, obtenido -0.449, tol. 0.3). **Falso negativo del extractor:** tomó la diferencia neta M - A. Recálculo del notario: arrastre de M = 10.797 pb (rotación 17.181 %). La respuesta dice "Arrastre 10.797 pb/ano", dentro de la tolerancia. No se aplica ningún tope.

### Calificación

**Calificador A: 5.0/5.** Reproduje la simulación: 277 cierres y n=276. M: V bruto 6.3826 y neto 6.2380, CAGR 8.3927/8.2847, arrastre 10.797 pb, operado 7.903, rotación 17.18 %. A: 6.9174/6.8611, 8.7725/8.7339, arrastre 3.863 pb, rotación 6.12 %. Comprar y mantener da 8.325 %. El 'fuera de tolerancia' es un error de extracción: el calificador tomó -0.449, que es la diferencia neta M-A, en lugar del arrastre de M. La respuesta reporta 10.797 pb, que coincide con la clave, así que no aplico el tope. La descomposición trayectoria/costo (0.380/0.069) es correcta. El chequeo del arrastre es incluso más fino que la clave, con el factor (1+g). Las advertencias están completas (una sola trayectoria; spread, impuestos y tipo de cambio omitidos), y las citas a arena/investigacion/01, líneas 17 y 94, existen.

**Calificador B: 5.0/5.** El 'fuera de tolerancia' es un falso negativo del extractor: tomó la diferencia neta -0.449. La respuesta reporta un arrastre de 10.797 pb, y mi simulación en python3 da 10.797 pb. La clave es correcta y la respuesta coincide. n=276, 275 y 22 rebalanceos. M: bruto 8.393 %, neto 8.285 %, rotación 17.181 %. A: 8.773 %, 8.734 %, 3.863 pb, rotación 6.122 %. Todo verificado. La descomposición es correcta: trayectoria -0.380 pp y costo -0.069 pp. El chequeo del arrastre es excelente: c\*2\*rotación = 9.965 pb, y el factor (1+g) lleva a 10.80. Las advertencias cubren la trayectoria única, el spread, los impuestos y el tipo de cambio. Incluye el IVA. La cita de arena/investigacion/01, línea 17, existe.

**Promedio A-B: 5.0/5** (|A − B| = 0; sin arbitraje).

### Defensa oral

No hubo defensa oral para esta pregunta (la defensa cubrió S6-01 a S6-04). Deducción: 0.

### Puntaje final

**5.0/5** = 5.0 (promedio de A y B), sin deducción.

### Hueco

**Ninguno.** Cumple los cinco puntos. Su chequeo del arrastre con el factor (1 + g) (10.80 pb contra 10.797 observado) es más fino que el de la clave (≈ 10 pb). La calificación automática marcó "fuera de tolerancia" por un error de extracción.

---

## S6-09 — Alineacion temporal del tipo de cambio: diagnostico del cierre de Yahoo MXN=X frente a la Fed H.10 (laboratorio)

### Enunciado

Archivos en /home/user/New1/laboratorio/examen-datos/S6/: yahoo_EWW_1d.json (SHA256 a2d69e0f91acb4dbdf7ee4a658a91a606eb9fc6069316f53a819c345d67fa5ff); yahoo_MXN_X_1d.json (SHA256 2805ce83648f149b50f3910ff32ba5c295cda445692f27e46c0df6ce2f6dd829); dbnomics_FED_H10_RXI_N.B.MX.csv (SHA256 9b35dd88d46767f89ad6e384d8934e9586670cc26637dbefff653cd27ab14502; MXN por USD, noon buying rate de NY; 'NA' es faltante). Convierte el timestamp de EWW a fecha en America/New_York y el de MXN=X a fecha en Europe/London (meta.exchangeTimezoneName), NO a fecha UTC. Series: EWW = indicators.adjclose[0].adjclose; MXN=X = indicators.quote[0].close (tambien usa quote.open); H.10 = valor del CSV. Sea D el conjunto de fechas entre 2023-01-01 y 2025-12-31 en que las TRES series tienen dato no nulo. Calcula log-rendimientos entre fechas consecutivas de D: r_t de EWW, f^H_t de H.10 y f^Y_t de MXN=X. Reporta (a) el numero de fechas y de rendimientos; (b) corr(r_t, f_t) (rezago 0) y corr(r_t, f_{t+1}) ('adelanto', pares t = 1..n-1) para cada fuente; (c) la fraccion de fechas de D con |close/open - 1| \< 2e-5 en MXN=X; (d) lo mismo en la ventana de control 2010-01-01 a 2012-12-31. (e) Diagnostica que representa hoy el 'close' diario de MXN=X, formula la regla correcta para convertir a MXN un precio de cierre del NYSE y explica por que un corrimiento fijo en toda la muestra tambien es incorrecto.

### Clave (descifrada)

(a) 2023-2025: 745 fechas comunes y 744 rendimientos. (b) H.10: rezago 0 = -0.630; adelanto = -0.225. Yahoo MXN=X: rezago 0 = -0.0015 (practicamente cero); adelanto = -0.721. (c) 96.2 % de los dias con close aprox. igual a open. (d) Control 2010-2012 (747 fechas): H.10 rezago 0 = -0.628, adelanto = -0.243; Yahoo rezago 0 = -0.833, adelanto = +0.112; close aprox. igual a open en solo 0.4 % de los dias. (e) Diagnostico: en los datos recientes, el 'close' de MXN=X con fecha de Londres D es en realidad una foto al inicio de ese dia de Londres (aprox. 00:00 Londres, 19:00 de NY del dia D-1), por eso es casi igual al open. La variacion de D a D+1 de Yahoo es la que contiene la sesion de NY del dia D, y de ahi la correlacion de -0.72 con el adelanto y de cero con el rezago 0. H.10 (mediodia de NY) si es contemporanea (-0.63); su adelanto de -0.22 refleja el tramo de 12:00 a 16:00 que la tasa del mediodia no ve. Regla correcta: usar una fuente con marca de tiempo documentada (H.10 al mediodia de NY, FIX de Banxico, WM/Reuters a las 16:00 de Londres) y declarar el desfase residual; si se usa Yahoo, tomar para el cierre NYSE del dia D el valor fechado D+1 SOLO en el regimen reciente. El comportamiento cambio en el tiempo (2005-2012 era un cierre tardio correcto; desde aprox. 2022 es una foto de inicio de dia; la fraccion close=open era de 14.6 % en 2019, 79.6 % en 2022 y 98.9 % en 2024). Un corrimiento fijo en toda la muestra desalinearia el periodo antiguo. Consecuencia: correlaciones, betas, drawdowns diarios y rendimientos en MXN al cierre de mes calculados con Yahoo quedan sesgados o con ruido de un dia.

**Rúbrica:** 5 puntos. 1 pt: conversion de zonas horarias correcta y conjunto comun (744 rendimientos). 1 pt: las cuatro correlaciones de 2023-2025 (Yahoo con rezago 0 aprox. 0 +/-0.02 y adelanto aprox. -0.72; H.10 -0.63 y -0.22). 1 pt: ventana de control con el signo invertido del patron. 1 pt: fraccion close=open y diagnostico de la foto de inicio de dia. 1 pt: regla de alineacion correcta y advertencia del cambio de regimen. Usar fecha UTC para MXN=X y no detectarlo: maximo 2 pt.

**Valor numérico comprometido:** -0.0015 ± 0.02. **Huella SHA256:** `afb4da7a17ec448b4cc5a27c9c2df63ba70c80d6dc32559912ad16cfb941fabd` (coincide con el compromiso).

### Fuente

Yahoo Finance chart API v8, https://query1.finance.yahoo.com/v8/finance/chart/MXN=X?period1=0&period2=\<ahora>&interval=1d&includeAdjustedClose=true y .../EWW (User-Agent Mozilla/5.0), descargados el 2026-09-25 hacia las 05:44-05:48 UTC. Federal Reserve H.10 RXI_N.B.MX via DBnomics (https://api.db.nomics.world/v22/series/FED/H10/RXI_N.B.MX?observations=1&format=csv); es la misma serie de FRED DEXMXUS, 'noon buying rates in New York' segun FRED. Calculo propio en python3 con zoneinfo.

### Respuesta del sustentante (completa)

DATOS: EWW (adjclose; America/New_York), MXN=X (quote.close y quote.open; fecha en Europe/London, que es meta.exchangeTimezoneName) y H.10 ('NA' = faltante). Los timestamps de MXN=X son las 00:00 de Londres (23:00 UTC en verano y 00:00 UTC en invierno). Hay un duplicado de fecha (2026-09-25, con barra viva) fuera de la ventana. Log-rendimientos entre fechas consecutivas de D. Calculo propio.

(a) 2023-01-01 a 2025-12-31: 745 fechas y 744 rendimientos.

(b) H.10: corr(r_t, f_t) = -0.630; corr(r_t, f_{t+1}) = -0.225. MXN=X: corr(r_t, f_t) = -0.002; corr(r_t, f_{t+1}) = -0.721.

(c) |close/open - 1| \< 2e-5 en MXN=X: 96.2 % de las fechas de D.

(d) Control 2010-2012: 747 fechas y 746 rendimientos. H.10: lag 0 = -0.628 y adelanto = -0.244. MXN=X: lag 0 = -0.833 y adelanto = +0.112. close\~open en solo 0.40 %.

(e) Diagnostico: hoy, el 'close' diario de MXN=X con fecha d es en esencia una sola cotizacion tomada al abrir la barra (00:00 de Londres, \~19:00-20:00 ET del dia d-1). La barra esta colapsada (close = open en el 96 %). No contiene el movimiento de la sesion de Nueva York de d, sino el de d-1: la correlacion contemporanea con EWW es \~0 y la del adelanto es -0.72. Serie anual (calculo propio adicional): el cambio de regimen ocurre \~2018. Hasta 2017 el lag 0 era de -0.63 a -0.88 y el adelanto \~0. De 2018 a 2026 el lag 0 va de -0.26 a +0.05 y el adelanto de -0.58 a -0.75. En cambio, close = open solo domina en 2022-2025 (79-99.6 %) y baja a 9.5 % en 2026 con el adelanto aun en -0.68. Es un sintoma; el diagnostico robusto es el desfase adelanto/rezago. H.10 (12:00 ET) es estable en ambos periodos: capta la manana, y la tarde de Nueva York cae en el dato del dia siguiente (adelanto de \~-0.23). Por eso se pidio la fecha de Londres: con fecha UTC, las barras de verano quedan en el dia anterior y las de invierno no (657 fechas; lag 0 = -0.50 y adelanto = -0.30 en 2023-25), lo que mezcla dos convenciones dentro del ano. Regla correcta: un precio de cierre del NYSE (16:00 ET de d) se convierte con una cotizacion tomada lo mas cerca posible de las 16:00 ET del mismo d. Se alinea por instante de reloj, no por la etiqueta de fecha, y se verifica empiricamente por subperiodo que el lag 0 domine. Con Yahoo despues de 2018, lo mas cercano es la barra con fecha de Londres d+1 (\~3-4 horas despues). Con H.10 es la misma fecha d (4 horas antes, un desfase residual conocido; el sistema ya usa H.10/DEXMXUS en laboratorio/replicas/V04-benchmarks-en-pesos-y-sma10-senal-mxn/README.md). Por que un corrimiento fijo en toda la muestra tambien esta mal: la convencion del proveedor cambio. Un +1 fijo desalinea 2004-2017, donde el mismo dia era el correcto (en 2010-2012 el adelanto seria +0.11 contra -0.83 del lag 0), y un 0 fijo desalinea 2018-2026. Ademas, el desfase entre medianoche de Londres y 16:00 ET varia con los cambios de horario (Reino Unido y EUA cambian en fechas distintas), y los feriados de Londres y EUA difieren. Hace falta detectar el regimen o usar una fuente con hora documentada [Inferencia sobre la causa del proveedor].

### Calificación automática

Fuera de tolerancia (esperado -0.0015, obtenido -0.721, tol. 0.02). **Falso negativo del extractor:** tomó el adelanto de Yahoo. Recálculo del notario: rezago 0 de Yahoo MXN=X = -0.0015 (adelanto -0.7213). La respuesta dice "MXN=X: corr(r_t, f_t) = -0.002", dentro de la tolerancia. No se aplica ningún tope.

### Calificación

**Calificador A: 5.0/5.** Verificado con fecha de Londres para MXN=X: 745 fechas y 744 rendimientos. H.10 da -0.630/-0.225; Yahoo da -0.0015/-0.7213; close=open en 96.2 %. Control 2010-2012: 747 fechas, H.10 -0.628/-0.243, Yahoo -0.833/+0.112, 0.40 %. El 'fuera de tolerancia' es un error de extracción: el calificador tomó -0.721, que es el adelanto, en lugar del rezago 0. La respuesta reporta el rezago 0 de Yahoo como -0.002, dentro de la tolerancia, así que no aplico el tope. El diagnóstico de la foto al inicio del día es correcto, igual que la regla de alinear por instante de reloj y la advertencia de que un corrimiento fijo desalinea el periodo antiguo. Su fechado del régimen (desfase desde 2018 y close=open solo en 2022-2025, con 9.5 % en 2026) lo verifiqué año por año y es correcto, más preciso que la clave. La variante UTC (657 fechas, -0.50/-0.30) también está verificada. La cita a V04 (DEXMXUS) existe.

**Calificador B: 5.0/5.** El 'fuera de tolerancia' es un falso negativo del extractor: tomó el adelanto -0.721. La respuesta reporta un rezago 0 de -0.002 para MXN=X, que es -0.0015 redondeado a 3 decimales, y mi recálculo con zoneinfo da -0.00153. La clave es correcta y la respuesta coincide. 745 fechas y 744 rendimientos. H.10: -0.630 y -0.225. Yahoo: -0.002 y -0.721. close=open en 96.2 %. Control 2010-2012: -0.628, -0.244, -0.833, +0.112 y 0.40 %. Todo verificado. El diagnóstico (foto al inicio del día de Londres), la regla de alineación por instante de reloj y la advertencia del cambio de régimen son correctos. Además precisa, con verificación, que el desfase adelanto/rezago empieza hacia 2018 aunque close=open solo domina en 2022-2025, lo que mejora la clave. La variante con fecha UTC (657 fechas; -0.50/-0.30) está verificada. La cita de V04 (DEXMXUS) existe.

**Promedio A-B: 5.0/5** (|A − B| = 0; sin arbitraje).

### Defensa oral

No hubo defensa oral para esta pregunta (la defensa cubrió S6-01 a S6-04). Deducción: 0.

### Puntaje final

**5.0/5** = 5.0 (promedio de A y B), sin deducción.

### Hueco

**Ninguno.** Cumple los cinco puntos. La calificación automática marcó "fuera de tolerancia" por un error de extracción.

**Observación sobre la clave (no cambia puntos):** la clave fecha el cambio de régimen de MXN=X "desde aprox. 2022". La respuesta, verificada año por año por A y B, muestra que el desfase adelanto/rezago empieza hacia 2018, aunque close = open solo domina en 2022-2025 (y baja a 9.5 % en 2026). El diagnóstico robusto es el desfase de correlaciones, no la fracción close = open. La clave comprometida no se modifica; la precisión queda registrada aquí.

---

## S6-10 — Drawdown maximo diario con fechas en USD y en MXN (EWW, iShares MSCI Mexico) (laboratorio)

### Enunciado

Archivos en /home/user/New1/laboratorio/examen-datos/S6/: yahoo_EWW_1d.json (SHA256 a2d69e0f91acb4dbdf7ee4a658a91a606eb9fc6069316f53a819c345d67fa5ff; fecha en America/New_York; precio = indicators.adjclose[0].adjclose) y dbnomics_FED_H10_RXI_N.B.MX.csv (SHA256 9b35dd88d46767f89ad6e384d8934e9586670cc26637dbefff653cd27ab14502; MXN por USD; 'NA' es faltante). Sea D el conjunto de fechas de 2008-01-02 a 2025-12-31 con adjclose de EWW y H.10 no faltantes. P_USD = adjclose y P_MXN = adjclose \* H10, en la misma fecha. Para cada serie calcula el drawdown maximo diario, MDD = min_t [P_t / max_{s\<=t} P_s - 1] (el maximo corre desde la primera fecha de D). Reporta la fecha del pico, la del valle y la de recuperacion (primera fecha posterior al valle con P >= P_pico). Indica cuantos dias de negociacion de EWW se excluyen por falta de H.10 y por que, y si eso cambia el MDD en USD. Por ultimo, explica economicamente por que difieren las fechas de pico y valle entre monedas, y que exposicion cambiaria tiene realmente un inversionista mexicano que compra EWW en el SIC.

### Clave (descifrada)

D tiene 4483 fechas. Se excluyen 46 dias de EWW sin H.10 (feriados federales de EUA en que el NYSE opera, como Columbus Day y Veterans Day, y 2010-12-31). Con los 4529 dias de EWW, el MDD en USD es identico. USD: MDD = -64.62 %; pico 2008-05-30; valle 2009-03-09; recuperacion 2010-12-02. MXN: MDD = -49.47 %; pico 2008-04-01; valle 2008-10-27; recuperacion 2009-12-01. Dato adicional (no obligatorio), 2020: -47.68 % en USD contra -29.80 % en MXN, ambos del 2020-01-17 al 2020-03-23. Interpretacion: EWW tiene acciones mexicanas; su valor en MXN es aprox. el de la bolsa mexicana en pesos (con dividendos y menos el costo del fondo). El valle en MXN (octubre de 2008) es el piso de la bolsa local. El valle en USD se retrasa a marzo de 2009 porque el peso siguio depreciandose hasta principios de marzo de 2009, asi que la caida en USD suma la caida de las acciones y la del peso. Para un inversionista mexicano, comprar EWW en USD en el SIC NO agrega diversificacion cambiaria: la exposicion es al peso a traves del subyacente, y el envoltorio en USD no la cambia. El drawdown relevante para el es el de MXN. Desfase residual: tasa H.10 del mediodia contra cierre a las 16:00.

**Rúbrica:** 5 puntos. 1 pt: alineacion (4483 fechas) y explicacion de los 46 dias excluidos. 1 pt: MDD en USD de -64.62 con fechas de pico y valle. 1 pt: MDD en MXN de -49.47 (+/-0.1) con fechas. 1 pt: fechas de recuperacion. 1 pt: interpretacion (EWW en MXN aprox. igual a la bolsa local en pesos, sin diversificacion cambiaria; por que se desfasan los valles).

**Valor numérico comprometido:** -49.47 ± 0.1. **Huella SHA256:** `9067f40c6de384e4c3db53a3b7417e45ac39a04533c212a2fde2a5d0134c7d93` (coincide con el compromiso).

### Fuente

Yahoo Finance chart API v8 (EWW, interval=1d, includeAdjustedClose=true, User-Agent Mozilla/5.0), descargado el 2026-09-25. Federal Reserve H.10 RXI_N.B.MX (la fuente de FRED DEXMXUS) via DBnomics, https://api.db.nomics.world/v22/series/FED/H10/RXI_N.B.MX?observations=1&format=csv, descargado el 2026-09-25. Calculo propio en python3.

### Respuesta del sustentante (completa)

DATOS: yahoo_EWW_1d.json (adjclose, America/New_York) y H.10. D = fechas de 2008-01-02 a 2025-12-31 con ambos datos: 4,483 fechas, de 4,529 dias de EWW. MDD con el maximo corrido desde la primera fecha de D. Calculo propio.

USD: MDD = -64.618 %. Pico 2008-05-30 (EWW 42.07, FX 10.329), valle 2009-03-09 (14.88, FX 15.382), recuperacion 2010-12-02.

MXN (adjclose\*H10): MDD = -49.473 %. Pico 2008-04-01 (FX 10.601), valle 2008-10-27 (FX 13.274), recuperacion 2009-12-01.

Segundo episodio (calculo propio): USD -62.19 % (2013-04-11 a 2020-03-23) contra MXN -34.29 % (2017-07-26 a 2020-03-23).

Exclusiones: 46 dias de negociacion de EWW sin H.10, todos marcados 'NA' en el CSV. Hay 18 de Columbus Day y 18 de Veterans Day: feriados federales/bancarios en los que la Fed no publica la noon rate y el NYSE si abre. Otros 2 son Ano Nuevo observado en viernes (2010-12-31 y 2021-12-31). Los restantes son cierres federales por decreto u otros: 2014-12-26, 2018-12-24, 2020-12-24, las tomas de posesion 2017-01-20 y 2021-01-20, y 2019-01-14, 2019-02-20 y 2020-11-27 [Inferencia: causa de los ultimos no verificada]. No cambia el MDD en USD: con los 4,529 dias da el mismo -64.618 %, con el mismo pico, valle y recuperacion.

Explicacion economica: el precio en USD de EWW es aproximadamente el valor en pesos de las acciones mexicanas dividido entre el tipo de cambio. En las crisis el peso se deprecia justo cuando caen las acciones (correlacion diaria EWW-H10 de -0.63; ver S6-09). En USD se suman ambas caidas, y el valle en USD llega en marzo de 2009 con el peso en su punto mas debil (15.38). En MXN, la depreciacion compensa, asi que la caida es menor y toca fondo antes (oct-2008). El pico en MXN llega antes (abr-2008) porque el peso se aprecio en abr-may 2008. Exposicion real de un mexicano que compra EWW en el SIC: P_MXN = P_USD\*FX, que es aproximadamente el valor en pesos de acciones mexicanas. Su exposicion economica es a renta variable mexicana en pesos. La cotizacion en dolares es solo el envoltorio: no le da exposicion neta al dolar ni lo cubre contra una depreciacion [Inferencia, apoyada en la correlacion negativa]. Le quedan exposiciones residuales: TER del ETF, retenciones fiscales en EUA sobre dividendos (arena/investigacion/01-gbm-operativa-y-costos.md, linea 24) y desfases de horario. Consistente con laboratorio/alertas-de-datos.md, alerta 2 (distinguir caida maxima diaria de cambio entre fechas).

### Calificación automática

Fuera de tolerancia (esperado -49.47, obtenido -64.618, tol. 0.1). **Falso negativo del extractor:** tomó el MDD en USD. Recálculo del notario: MDD en MXN = -49.473 % (USD -64.617 %; 4,483 fechas, 46 excluidas). La respuesta dice "MDD = -49.473 %" (MXN), dentro de la tolerancia. No se aplica ningún tope.

### Calificación

**Calificador A: 5.0/5.** Verificado: D tiene 4483 fechas y se excluyen 46 días, todos NA en H.10. Son 18 de Columbus Day, 18 de Veterans Day, 2010-12-31, 2021-12-31 y 8 días más, con la misma lista que da la respuesta. El MDD en USD, -64.617 %, es idéntico con los 4529 días. USD: pico 2008-05-30, valle 2009-03-09, recuperación 2010-12-02. MXN: -49.473 %, pico 2008-04-01, valle 2008-10-27, recuperación 2009-12-01. El 'fuera de tolerancia' es un error de extracción: el calificador tomó -64.618, que es el MDD en USD. La respuesta reporta el MDD en MXN como -49.473, que coincide con la clave, así que no aplico el tope. La interpretación económica es correcta: EWW en MXN es aproximadamente renta variable mexicana en pesos, sin diversificación cambiaria, y explica bien el desfase de los valles. Las causas no verificadas están marcadas como inferencia, y las citas existen.

**Calificador B: 5.0/5.** El 'fuera de tolerancia' es un falso negativo del extractor: tomó el MDD en USD -64.618. La respuesta reporta un MDD en MXN de -49.473 %, y python3 da -49.4734. La clave es correcta y la respuesta coincide. D = 4,483 fechas, con 46 excluidas (verifiqué el desglose: 18 Columbus, 18 Veterans, 2 Años Nuevos observados y 8 cierres ad hoc, todos NA). USD: pico 2008-05-30, valle 2009-03-09, recuperación 2010-12-02. MXN: 2008-04-01, 2008-10-27, 2009-12-01. El MDD en USD no cambia con los 4,529 días. Todo verificado, y el segundo episodio también (-62.19 % y -34.29 %). La interpretación económica es correcta: el valle en USD se retrasa por el peso y la exposición real es a renta variable mexicana en pesos, sin diversificación cambiaria. Las citas del repo existen.

**Promedio A-B: 5.0/5** (|A − B| = 0; sin arbitraje).

### Defensa oral

No hubo defensa oral para esta pregunta (la defensa cubrió S6-01 a S6-04). Deducción: 0.

### Puntaje final

**5.0/5** = 5.0 (promedio de A y B), sin deducción.

### Hueco

**Ninguno.** Cumple los cinco puntos. La calificación automática marcó "fuera de tolerancia" por un error de extracción.

**Observación sobre la clave (no cambia puntos):** la clave explica los 46 días excluidos con "Columbus Day y Veterans Day, y 2010-12-31", lo que es incompleto. El desglose de la respuesta, verificado por A y B, es 18 + 18 + 2 Años Nuevos observados (2010-12-31 y 2021-12-31) + 8 cierres ad hoc.

---

## S6-11 — Reconstruccion del HML europeo desde sus 6 portafolios: cota de redondeo y prima de valor en grandes frente a pequenias (laboratorio)

### Enunciado

Archivos en /home/user/New1/laboratorio/examen-datos/S6/: (1) Europe_6_Portfolios_ME_BE-ME_CSV.zip, SHA256 4c6e35d00e6e3fc304cf6614d4de5d10674bfd37d388f6f94ddaf46c3527b1e1; CSV Europe_6_Portfolios_ME_BE-ME.csv, seccion 'Average Value Weighted Returns -- Monthly', columnas SMALL LoBM, ME1 BM2, SMALL HiBM, BIG LoBM, ME2 BM2, BIG HiBM (% mensual, en USD). (2) Europe_3_Factors_CSV.zip, SHA256 529b7f1909b91343d02ad48b51f09dd137d38dd542f74d8c577c3872c2b6585a, columnas SMB y HML. (a) Para 1990-07 a 2026-08 (434 meses) reconstruye HML_rec = 1/2(SMALL HiBM + BIG HiBM) - 1/2(SMALL LoBM + BIG LoBM) y SMB_rec = 1/3(las tres pequenias) - 1/3(las tres grandes). Reporta el maximo de |diferencia| contra el factor publicado y el mes en que ocurre. (b) Deriva la cota teorica maxima de la discrepancia atribuible solo al redondeo, sabiendo que ambos archivos muestran 2 decimales, y concluye. (c) Para 1990-07 a 2025-12 (n = 426) calcula la media y el t de Newey-West(6) de HML_rec, de BIG HiBM - BIG LoBM y de SMALL HiBM - SMALL LoBM. Usa kernel de Bartlett, gamma_j = (1/n)\*suma (x_t - xbar)(x_{t-j} - xbar), S = gamma_0 + 2\*suma_{j=1..6}(1 - j/7)\*gamma_j y SE = raiz(S/(n-1)). (d) Calcula la fraccion de la media de HML_rec que aporta la mitad pequenia, [1/2\*media(SMALL HiBM - SMALL LoBM)]/media(HML_rec), en %. (e) Explica que significan 'Big' y 'Small' en los factores regionales de French y por que importa para un inversionista que solo puede comprar ETFs de Europa de gran capitalizacion.

### Clave (descifrada)

(a) max|HML_rec - HML| = 0.015, en 1999-11 (reconstruido -9.035 contra publicado -9.05). max|SMB_rec - SMB| = 0.0133, en 2013-08. Correlaciones de 0.999998. (b) Cota para HML: cuatro insumos con error de +/-0.005 cada uno, ponderados por 1/2, dan 1/2\*4\*0.005 = 0.010; el HML publicado aporta +/-0.005; cota total 0.015. Cota para SMB: 1/3\*6\*0.005 + 0.005 = 0.015. Lo observado alcanza pero no rebasa la cota, asi que la discrepancia es solo redondeo y el factor se reproduce exactamente. (c) HML_rec: media 0.3312 %/mes, t_NW = 1.87 (publicado: 0.3316, t 1.88). Grandes (BIG HiBM - BIG LoBM): 0.2139 %/mes, t_NW = 1.16. Pequenias (SMALL HiBM - SMALL LoBM): 0.4485 %/mes, t_NW = 2.27. (d) Mitad pequenia 0.2243 contra mitad grande 0.1069: la fraccion pequenia es 67.7 %. (e) En los factores regionales de French, 'Big' son las acciones del 90 % superior de la capitalizacion de junio de la region y 'Small' las del 10 % inferior. Los cortes de B/M son los percentiles 30 y 70 de las acciones grandes. Asi, 'Small' es un segmento de micro y pequenia capitalizacion que pesa poco en el mercado. La parte de la prima de valor que se puede capturar con ETFs de valor de gran capitalizacion (la mitad grande) es de aprox. 2.6 % anual x12, no significativa (t 1.16), en USD, antes de costos, y como diferencial largo-corto, no como exceso long-only sobre el mercado. Aun con toda la muestra, el HML europeo no alcanza 1.96.

**Rúbrica:** 5 puntos. 1 pt: reconstruccion y maximos (0.015 en 1999-11; 0.0133). 1 pt: derivacion de la cota de 0.015 y conclusion. 1 pt: medias y t de HML_rec, del diferencial grande y del pequenio. 1 pt: fraccion de 67.7 % (+/-0.5). 1 pt: definicion 90 %/10 % y cortes 30/70 sobre las grandes, con la implicacion practica. Confundir la seccion equiponderada o la de numero de empresas invalida los puntos numericos.

**Valor numérico comprometido:** 67.7 ± 0.5. **Huella SHA256:** `f9e0881cc11842518f8d875442ccf2fb291e2185096305574bb8dd032d905254` (coincide con el compromiso).

### Fuente

Kenneth R. French Data Library: Europe_6_Portfolios_ME_BE-ME_CSV.zip y Europe_3_Factors_CSV.zip (Bloomberg 202608), https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/, descargados el 2026-09-25. Construccion regional (Big = 90 % superior de la capitalizacion de junio, Small = 10 % inferior, cortes B/M en los percentiles 30/70 de las grandes, formulas SMB y HML): https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_3developed.html (verificado con WebFetch). Calculo propio en python3.

### Respuesta del sustentante (completa)

DATOS: Europe_6_Portfolios_ME_BE-ME.csv, seccion 'Average Value Weighted Returns -- Monthly' (lineas 20-455; 199007-202608; 2 decimales verificados). Europe_3_Factors.csv, SMB y HML. Calculo propio con aritmetica Decimal exacta.

(a) En 1990-07 a 2026-08 (434 meses): max|HML_rec - HML| = 0.015, alcanzado en 3 meses empatados. El primero es 1999-11 (-9.035 vs -9.05); los otros, 2003-01 (2.495 vs 2.51) y 2025-03 (5.525 vs 5.54). max|SMB_rec - SMB| = 0.0133 en 7 meses empatados: 1997-11 (el primero), 1997-12, 2010-04, 2013-08, 2014-08, 2015-12 y 2018-03.

(b) Cota teorica: cada portafolio tiene |e_i| \<= 0.005, y las combinaciones tienen suma de |pesos| = 2 (cuatro de 1/2 en HML, seis de 1/3 en SMB), asi que la reconstruccion tiene error \<= 0.010. El factor publicado tiene |e_f| \<= 0.005. Total \<= 0.015 para ambos. Conclusion: ninguna discrepancia excede la cota (HML la toca, SMB queda en 0.0133), asi que en magnitud es compatible con redondeo y economicamente irrelevante: la media publicada es 0.3316 contra 0.3312 reconstruida. Matiz (calculo propio adicional): tocar exactamente 0.015 exige que los cinco errores esten en +/-0.005 a la vez, lo que tiene probabilidad cero con rendimientos continuos. En una simulacion de redondeo puro, |dif| = 0.01 ocurre en 4.2 % de los meses (18 esperados) y aqui ocurre 46 veces (p \~ 1e-8). SMB muestra lo mismo (18 contra 4.6 en 0.01, y 7 contra \~0 en 0.0133). Hay una diferencia adicional minima (sigma \~0.003 pp) entre los insumos del factor y los portafolios publicados; su causa (version de datos o precision intermedia) no se puede verificar [Inferencia]. En EUA (S6-06), con 4 decimales, el ajuste si es redondeo puro.

(c) En 1990-07 a 2025-12 (n = 426): HML_rec media 0.331 %/mes, t_NW 1.875 (SE 0.177). BIG HiBM - BIG LoBM: 0.214, t_NW 1.158. SMALL HiBM - SMALL LoBM: 0.449, t_NW 2.272.

(d) Fraccion pequena = 0.5\*0.4485/0.3312 = 67.712 %.

(e) [De memoria, no documentado en el repo: en los factores regionales de French, 'Big' son las acciones del 90 % superior de la capitalizacion de la region a fin de junio y 'Small' el 10 % inferior. Los cortes de B/M son los percentiles 30 y 70 de las grandes.] 'Small' en Europa son small y microcaps de verdad, una definicion distinta del corte en la mediana del NYSE en EUA. Un ETF europeo de gran capitalizacion es aproximadamente el universo 'Big'. Ahi la prima de value fue de 0.214 %/mes (\~2.6 %/ano) con t 1.16, no significativa, y los dos tercios de HML que vienen de la mitad pequena no son accesibles. Incluso HML completo tiene t_NW 1.875 \< 1.96. El inversionista debe esperar una prima mucho menor e incierta, antes de TER, spread, comisiones (0.29 % por lado en GBM) y retenciones fiscales. Los factores estan en USD, asi que tambien incluyen el tipo de cambio.

### Calificación automática

Dentro de tolerancia (esperado 67.7, obtenido 67.712, tol. 0.5).

### Calificación

**Calificador A: 5.0/5.** Verificado: max|HML_rec-HML| = 0.015, empatado en 1999-11, 2003-01 y 2025-03; max SMB = 0.01333, empatado en 7 meses que incluyen 1997-11 y 2013-08. HML_rec 0.33120 (t 1.875), grandes 0.21387 (t 1.158), pequeñas 0.44852 (t 2.272), fracción 67.712 %. La cota de 0.015 está bien derivada. El matiz adicional es correcto y va más allá de la clave: simulé redondeo puro y |dif|=0.01 ocurre en 4.2 % de los meses en HML (unos 18 esperados contra 46 observados) y en 1.06 % en SMB (4.6 esperados contra 18). Además, llegar exactamente a 0.015 tiene probabilidad cero, así que la afirmación de 'solo redondeo' de la clave es discutible, y la respuesta lo marca bien como inferencia. La definición 90/10 y 30/70 es correcta y está declarada honestamente como de memoria. La implicación práctica está bien.

**Calificador B: 5.0/5.** Verificado con python3 y aritmética Decimal: max|HML| 0.015 con 3 empates (1999-11, 2003-01, 2025-03) y max|SMB| 0.0133 con 7 empates. La clave nombra 2013-08, pero con aritmética exacta es un empate y la respuesta lo trata con más rigor. La cota de 0.015 está bien derivada. Su matiz también se verifica: |dif| = 0.01 aparece 46 veces cuando el redondeo puro implica \~4.1 % (\~18), y 0.015 tiene probabilidad casi nula, así que la respuesta es más precisa que la clave sin contradecir la conclusión práctica. HML_rec 0.3312, t 1.875; diferencial grande 0.2139, t 1.158; diferencial pequeño 0.4485, t 2.272; fracción 67.712 %, todo verificado. (e) La definición 90 %/10 % y 30/70 sobre las grandes es correcta aunque viene marcada como de memoria, y la implicación práctica está bien argumentada. Usa la sección VW.

**Promedio A-B: 5.0/5** (|A − B| = 0; sin arbitraje).

### Defensa oral

No hubo defensa oral para esta pregunta (la defensa cubrió S6-01 a S6-04). Deducción: 0.

### Puntaje final

**5.0/5** = 5.0 (promedio de A y B), sin deducción.

### Hueco

**Ninguno.** Cumple los cinco puntos.

**Observaciones sobre la clave (no cambian puntos):**
- La clave da 2013-08 como el mes del máximo de SMB. Con aritmética exacta hay 7 meses empatados en 0.0133 (el primero es 1997-11). La respuesta lo trata con más rigor.
- La clave concluye "la discrepancia es solo redondeo". A y B verificaron el matiz de la respuesta: bajo redondeo puro, |dif| = 0.01 debería aparecer en ≈ 4.2 % de los meses (≈ 18) y aparece 46 veces, y tocar exactamente la cota de 0.015 tiene probabilidad prácticamente nula. La conclusión práctica (el factor se reproduce y la diferencia es económicamente irrelevante) se sostiene; la afirmación "solo redondeo" es más fuerte de lo que los datos permiten.

**Base:** la definición 90 %/10 % y los cortes 30/70 de los factores regionales se dieron correctamente pero "de memoria"; no están en el repositorio (ver S6-01).

---

## S6-12 — Costos de GBM sobre una regla con rotacion dada: decil de valor long-only contra el mercado (laboratorio)

### Enunciado

Archivos en /home/user/New1/laboratorio/examen-datos/S6/: (1) Portfolios_Formed_on_BE-ME_CSV.zip, SHA256 7ddd8918eb34b125b03e3e6e0bc927aef71dd9e3ff5a2a274d47da3a453c305b; CSV Portfolios_Formed_on_BE-ME.csv, seccion 'Value Weight Returns -- Monthly', columna 'Hi 10' (decil de B/M mas alto, ponderado por valor, % mensual). (2) F-F_Research_Data_Factors_CSV.zip, SHA256 b840dba55d319f4818fc7300e65c52eff5f64870c8d495fa58ff5d4cd749f5eb; mercado R_m = Mkt-RF + RF. Ventana: 2000-01 a 2025-12 (n = 312). Rotacion dada: rotacion anual de un solo sentido tau = 60 %, ejecutada completa al cierre de cada junio (el rebalanceo anual de French), de junio de 2000 a junio de 2025 (26 veces). Costo de GBM: c = 0.25 % \* 1.16 = 0.29 % por lado. En cada rebalanceo se descuenta de la riqueza 2\*tau\*c. El mercado se trata como un indice con rotacion cero y sin costo; se excluyen la compra inicial y la venta final. Calcula: (a) el costo por rebalanceo en %; (b) el CAGR bruto y el neto de Hi 10, el CAGR del mercado ((W_final)^(12/n) - 1) y la diferencia neta contra el mercado en pp; (c) la rotacion de equilibrio tau\* (un solo sentido, anual) con la que el CAGR neto de Hi 10 iguala al del mercado; (d) la media mensual del exceso Hi 10 - R_m y su t de Newey-West(6). Usa kernel de Bartlett, gamma_j = (1/n)\*suma (x_t - xbar)(x_{t-j} - xbar), S = gamma_0 + 2\*suma_{j=1..6}(1 - j/7)\*gamma_j y SE = raiz(S/(n-1)). (e) Concluye si 'los costos de GBM se comen la prima de valor' y enumera los supuestos que hacen optimista este calculo.

### Clave (descifrada)

(a) 2 \* 0.60 \* 0.29 % = 0.348 % por rebalanceo, 26 rebalanceos. (b) CAGR bruto de Hi 10 = 9.062 %; neto = 8.683 %; mercado = 8.271 %. Bruto - mercado = +0.791 pp; neto - mercado = +0.412 pp; arrastre = 0.380 pp por anio. Riquezas finales: 9.540 bruta, 8.713 neta y 7.894 del mercado. (c) tau\* aprox. 125 % anual de un solo sentido, un costo de aprox. 0.725 % por anio. (d) Exceso medio = 0.222 %/mes (2.67 %/anio x12), t_NW = 0.81: no significativo. (e) Con la comision de GBM los costos NO se comen la prima: harian falta rotaciones de mas de 125 % anual. El problema es estadistico, no de costos: el exceso no se distingue de cero (t 0.81), y la diferencia de CAGR la dominan periodos concretos (2000-2006). Supuestos optimistas: (1) Hi 10 es un portafolio de papel de French, sin ETF que lo replique; un ETF de valor real tiene su comision de administracion, otra composicion y error de replica. (2) Se ignoran el diferencial de compra-venta, el impacto de mercado (el decil tiene muchas acciones pequenias ilíquidas), los impuestos y el tipo de cambio del SIC. (3) La rotacion del 60 % es un supuesto, no un dato: la rotacion real del decil extremo puede ser mayor. (4) Hay sesgo de seleccion en la eleccion del decil extremo y de la ventana.

**Rúbrica:** 5 puntos. 1 pt: series correctas (seccion VW, 'Hi 10', mercado = Mkt-RF + RF) y costo de 0.348 % x 26. 1 pt: CAGR bruto 9.06, neto 8.68 y mercado 8.27. 1 pt: neto - mercado = +0.41 pp (+/-0.02). 1 pt: tau\* aprox. 125 % y t_NW 0.81 del exceso. 1 pt: conclusion correcta (el problema es estadistico, no de costos) con al menos tres supuestos optimistas. Si se omite el IVA, neto - mercado aprox. +0.46: -1 pt.

**Valor numérico comprometido:** 0.412 ± 0.02. **Huella SHA256:** `a9c8052ae7c6900c769bba821e737f443a7304eecc6b70c46163a1673b054fb9` (coincide con el compromiso).

### Fuente

Kenneth R. French Data Library: Portfolios_Formed_on_BE-ME_CSV.zip y F-F_Research_Data_Factors_CSV.zip (CRSP 202607), https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/, descargados el 2026-09-25. Comision de GBM de 0.25 % por operacion mas IVA del 16 %: https://gbm.com/faqs/que-comisiones-cobran-al-invertir-en-gbm/ y rankia.mx (verificado con WebSearch/WebFetch). Calculo propio en python3 (tau\* por biseccion).

### Respuesta del sustentante (completa)

DATOS: Portfolios_Formed_on_BE-ME.csv, seccion 'Value Weight Returns -- Monthly' (lineas 23-1225), columna 'Hi 10'. R_m = Mkt-RF + RF de F-F_Research_Data_Factors.csv. Ventana 2000-01 a 2025-12, n = 312, sin faltantes. Rebalanceos al cierre de cada junio, 2000-06 a 2025-06 (26). Riqueza multiplicada por (1 - 2\*tau\*c) en cada uno; sin compra inicial ni venta final. Calculo propio.

(a) Costo por rebalanceo = 2\*0.60\*0.29 % = 0.348 %.

(b) Hi 10 bruto: W = 9.540, CAGR 9.062 %. Neto: W = 8.714, CAGR 8.683 %. Mercado: W = 7.894, CAGR 8.271 %. Diferencia neta contra el mercado = +0.412 pp (bruta +0.791 pp). Arrastre 37.95 pb/ano \~ (1+g)\*26\*0.348 %/26 anos.

(c) tau\*: (1 - 2\*tau\*c)^26 \* W_bruto = W_mercado -> tau\* = [1 - (7.894/9.540)^(1/26)]/(2\*0.0029) = 125.114 % anual de un sentido, verificado numericamente. Habria que rotar mas del 100 % del portafolio al ano para empatar.

(d) Exceso mensual Hi 10 - R_m: media 0.222 %/mes (2.67 % x12), SE_NW 0.273, t_NW 0.815 (t IID 0.92). Error de seguimiento 14.9 % anual; volatilidad de Hi 10 24.8 % contra 15.7 % del mercado.

(e) Conclusion: NO, con solo la comision de GBM y 60 % de rotacion, los costos se comen \~48 % (38 de 79 pb) de la ventaja bruta en CAGR, pero no toda, y el punto de equilibrio exige tau\* = 125 %. La conclusion importante es otra: la prima bruta misma no es distinguible de cero (t_NW 0.81) y depende del inicio de la muestra. Calculo propio: 2003-2025 da Hi 10 9.70 % contra mercado 11.70 % bruto; 2010-2019 da 8.03 % contra 13.60 %. La pregunta no es si los costos se comen la prima, sino si la prima existe. Supuestos que hacen optimista el calculo: (1) solo comision, sin spread (0.10-0.60 % por lado segun arena/investigacion/01-gbm-operativa-y-costos.md), impacto ni conversion cambiaria; (2) rotacion de 60 % dada y ejecutada toda al cierre de junio al precio de cierre, junto con todo el universo value (hacinamiento), cuando la del decil extremo puede ser mayor; (3) Hi 10 es un portafolio de papel sin ETF que lo replique, con cientos de acciones y algunas en dificultades; el SIC no permite fracciones; (4) no hay TER, impuestos (10 % sobre la ganancia, retencion sobre dividendos, que es mas pesada en value por su mayor rendimiento por dividendo; linea 24 de la misma fuente) ni costo del W-8BEN; (5) se excluyen la compra inicial y la venta final (\~0.58 % ida y vuelta); (6) la ventana empieza justo antes del estallido punto-com, el mejor momento relativo del value; (7) se comparan CAGR sin ajustar por el riesgo mayor de Hi 10, y el mercado tratado como gratuito es un sesgo menor en sentido contrario. Regla de costos del sistema: conocimiento/14-analisis-tecnico-que-sobrevive.md (0.29 % por lado, regla de las 3x).

### Calificación automática

Dentro de tolerancia (esperado 0.412, obtenido 0.412, tol. 0.02).

### Calificación

**Calificador A: 5.0/5.** Verificado: sección VW, 'Hi 10', 312 meses, 26 rebalanceos de 0.348 %. W 9.5401/8.7135/7.8944; CAGR 9.062/8.683/8.271; neto contra mercado +0.4119 pp; tau\* 125.11 %; exceso 0.2221 con t_NW 0.8147. Los extras cuadran: 2003-2025 da 9.70 contra 11.70, 2010-2019 da 8.03 contra 13.60, TE 14.85 % y volatilidades 24.8/15.7. La conclusión es correcta: el problema es estadístico, no de costos. Da siete supuestos optimistas bien fundados. Las citas a arena/investigacion/01 (spread, línea 24 sobre dividendos) y a conocimiento/14 (regla 3x, línea 343) existen.

**Calificador B: 5.0/5.** Verificado con python3: costo 0.348 % en 26 rebalanceos. W bruta 9.540, neta 8.713 y mercado 7.894; CAGR 9.062, 8.683 y 8.271; neto menos mercado +0.412 pp. tau\* = 125.11 % y t_NW del exceso 0.815. Todo coincide. La conclusión es correcta: el problema es estadístico y no de costos. Enumera más de tres supuestos optimistas. Subperiodos verificados: 2003-2025 da 9.70 contra 11.70; 2010-2019, 8.03 contra 13.60. Las citas existen: arena/investigacion/01 (spread 0.10-0.60 y línea 24 de impuestos) y conocimiento/14 (0.29 % por lado y regla 3x, línea 343). Incluye el IVA.

**Promedio A-B: 5.0/5** (|A − B| = 0; sin arbitraje).

### Defensa oral

No hubo defensa oral para esta pregunta (la defensa cubrió S6-01 a S6-04). Deducción: 0.

### Puntaje final

**5.0/5** = 5.0 (promedio de A y B), sin deducción.

### Hueco

**Ninguno.** Cumple los cinco puntos, con siete supuestos optimistas (la rúbrica pide tres) y subperiodos que muestran que la ventaja bruta depende del inicio de la muestra.

---

## Resumen de la sección S6

| Pregunta | Tema | Automática | A | B | Promedio | Defensa | Final | Hueco principal |
|---|---|---|---|---|---|---|---|---|
| S6-01 | Media aritmética frente a CAGR (Japón en USD) | fuera (falso negativo) | 4.5 | 4.5 | 4.5 | −0.5 | 4.0 | No dijo que el RF es la T-bill de EUA; frase del "mercado bajista" retirada en la defensa |
| S6-02 | t IID frente a Newey-West(6) (HML 2007-2020) | dentro | 5.0 | 5.0 | 5.0 | −1.0 | 4.0 | "Casi garantiza" y peso de gamma_6 retirados en la defensa |
| S6-03 | MDD de HML con fechas | dentro | 5.0 | 5.0 | 5.0 | — | 5.0 | — |
| S6-04 | Correlación en caídas y benchmark BGL | dentro | 5.0 | 5.0 | 5.0 | −0.5 | 4.5 | Limitación (1) en dirección equivocada (defensa) |
| S6-05 | GLD en MXN con FX alineado | dentro | 5.0 | 5.0 | 5.0 | — | 5.0 | — |
| S6-06 | Reconstrucción de HML/SMB de EUA | fuera (falso negativo) | 5.0 | 5.0 | 5.0 | — | 5.0 | — |
| S6-07 | SMB antes y después de Banz (1981) | fuera (falso negativo) | 5.0 | 5.0 | 5.0 | — | 5.0 | — |
| S6-08 | Costos de GBM y frecuencia de rebalanceo | fuera (falso negativo) | 5.0 | 5.0 | 5.0 | — | 5.0 | — |
| S6-09 | Alineación de Yahoo MXN=X frente a H.10 | fuera (falso negativo) | 5.0 | 5.0 | 5.0 | — | 5.0 | — |
| S6-10 | MDD diario de EWW en USD y MXN | fuera (falso negativo) | 5.0 | 5.0 | 5.0 | — | 5.0 | — |
| S6-11 | Reconstrucción del HML europeo | dentro | 5.0 | 5.0 | 5.0 | — | 5.0 | — |
| S6-12 | Decil de valor contra el mercado con costos | dentro | 5.0 | 5.0 | 5.0 | — | 5.0 | — |
| **Total** | | | **59.5** | **59.5** | **59.5** | **−2.0** | **57.5 / 60** | |

- **Total S6: 57.5 / 60 = 95.83 %.**
- **Verificación de la revelación:** correcta. `clave.enc` del commit `6c526b6` descifra con la contraseña revelada; la huella del archivo en claro y las 12 huellas por pregunta coinciden con `compromiso.json`; la clave y la rúbrica que usaron A y B, y los valores de la calificación automática, son idénticos a los descifrados.
- **Arbitrajes:** ninguno. A y B coincidieron exactamente en las 12 preguntas (59.5 cada uno).
- **Defensa oral:** −2.0 en total (S6-01 −0.5, S6-02 −1.0, S6-04 −0.5; S6-03 sin deducción).
- **Frente al umbral** (`PROTOCOLO.md` §1): 95.83 % supera el mínimo de 85 % por sección. El dictamen global depende de las demás secciones.
- **Etiqueta:** con compromiso público previo (clave cifrada y huellas en GitHub antes de las respuestas; revelación verificable en este commit).
- **Lectura sin maquillaje:**
  - Se perdieron 2.5 puntos, ninguno por cálculo. Los 12 resultados numéricos coinciden con la clave, y los calificadores los reprodujeron con los datos congelados.
  - La pérdida viene de afirmaciones cualitativas que iban más allá de lo que el sustentante había calculado: 0.5 por omitir un dato que la rúbrica pedía (RF = T-bill de EUA, S6-01) y 2.0 por tres afirmaciones que la defensa oral tumbó (S6-01, S6-02 y S6-04).
  - A y B dieron 5/5 en S6-02 y S6-04 sin detectar esos errores. Los dos verifican muy bien los números y menos bien el razonamiento cualitativo. Sin la defensa oral, la sección habría quedado en 59.5.
  - La defensa oral solo cubrió 4 de las 12 preguntas, así que las otras 8 no pasaron por el mismo escrutinio. Es probable que el 95.8 % sea una cota superior.
  - El extractor automático falló en 6 de 12 preguntas, siempre del lado de "fuera de tolerancia" (falsos negativos). No sirve como calificador único mientras la respuesta no declare su número principal en una línea fija.
  - En cuatro preguntas (S6-08, S6-09, S6-10 y S6-11) la respuesta fue más precisa que la clave. La clave comprometida no se modifica, y las diferencias quedan registradas como observaciones.
- **Acciones:**
  1. Documentar en `laboratorio/` la construcción de los factores regionales de French (USD, RF = T-bill de EUA, 90/10, cortes 30/70), con fuente.
  2. En el formato de respuesta, exigir una línea `RESPUESTA NUMÉRICA: <valor>` con el número que pide la clave, para que el extractor no tome otro.
  3. Pedir a los calificadores que revisen explícitamente cada afirmación cualitativa (dirección de un sesgo, "casi garantiza", "agrava"), no solo las cifras, y extender la defensa oral a todas las preguntas o a una muestra aleatoria.
  4. Registrar para una futura versión del banco las precisiones a la clave de S6-09 (régimen desde ~2018), S6-10 (desglose de los 46 días) y S6-11 (empates y "solo redondeo").
