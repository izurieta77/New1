# Examen diagnóstico — Sección S7: Frontera: machine learning, microestructura y derivados

- **Sección:** S7, Frontera: machine learning, microestructura y derivados. 12 preguntas de 5 puntos (60 puntos).
- **Fecha:** 2026-09-25.
- **Acta redactada por:** árbitro, secretario y notario de revelación del examen (subagente del flujo de trabajo).
- **Resultado:** **58.75 / 60 = 97.92%**, con compromiso público previo verificado.

## Protocolo con que se aplicó

1. **Compromiso público antes de responder.** Se cifró la clave de las 12 preguntas: texto de la clave, valor numérico principal, tolerancia y rúbrica. El cifrado es AES-256-CBC con PBKDF2-SHA256 de 200,000 iteraciones y sal aleatoria. El archivo cifrado se publicó junto con tres huellas SHA256: la del archivo cifrado, la del archivo en claro y la de cada pregunta. Quedó en el commit `2a50ca2c7f5cd6cf6e6f4ce9f6da535ee02acb86` (fecha de commit 2026-09-25 06:03:15 UTC; `fecha_compromiso_utc` 06:03:05Z). Según el registro local de la rama remota, el commit llegó a `origin` a las 06:03:22 UTC. El primer registro de la sesión del sustentante es de las 06:03:46 UTC, 24 segundos después. La contraseña no estaba en el repositorio y se revela en esta acta (`contrasena.txt`). Verifiqué además que las instrucciones del sustentante, tanto las del examen escrito como las de la defensa oral, no contienen ninguna clave.
2. **Libro cerrado.** El sustentante no tuvo herramientas web ni red desde Bash, y tenía prohibido leer `conocimiento/examenes/`. Contestó con la base del repositorio y su memoria, y marcó "de memoria" o "sin verificar" lo que no sale de la base. El resumen de la auditoría del registro está abajo (`PROTOCOLO.md` §3).
3. **Calificación automática.** El resultado numérico principal se compara con el valor `numerica` ± `tolerancia` de la clave. Aplica a 11 preguntas; S7-04 es un caso sin resultado numérico.
4. **Dos calificadores independientes (A y B).** Cada uno calificó las 12 preguntas con la clave y la rúbrica, sin ver la nota del otro.
5. **Arbitraje.** Si |A − B| ≤ 1, el puntaje es el promedio de A y B. Si difieren en más de 1 punto, arbitra el secretario y justifica. **En esta sección no hubo arbitraje:** la diferencia máxima fue 0.5 (S7-02).
6. **Defensa oral.** Un examinador formuló dos repreguntas sobre cada una de S7-01 a S7-04. El sustentante contestó en las mismas condiciones de libro cerrado y sin clave. Un juez, con la clave, fijó la deducción de cada pregunta. Puntaje final = promedio de A y B − deducción (mínimo 0). **Deducciones: 0 en las cuatro preguntas defendidas.**
7. **Umbral** (`PROTOCOLO.md` §1): 85% o más en cada sección y 90% o más global.
8. **Cronología de la sesión (UTC):**
   - examinador: 05:42–06:00;
   - notario del compromiso: 06:00–06:03 (commit a las 06:03:15);
   - sustentante: 06:03:46–06:15:13;
   - calificadores A y B: 06:15–06:18;
   - examinador de la defensa: 06:18–06:19;
   - defensa oral: 06:19:36–06:33:34;
   - juez de la defensa: 06:33–06:35;
   - esta acta: desde 06:35.

## Revelación y verificación de la clave

| Comprobación | Resultado |
|---|---|
| SHA256 de `clave.enc` en el commit `2a50ca2` | `0355bd38fe70692a541aa87d9c399a94922319563534692d4a9f133ec9a1df6e`: **coincide** con `compromiso.json` (34,768 bytes). Idéntico al del árbol de trabajo |
| `compromiso.json` actual frente al del commit `2a50ca2` | **Idéntico**, sin cambios posteriores |
| Descifrado con la contraseña revelada (OpenSSL 3.0.13) | Correcto. El comando sin `-md` usa SHA256 por defecto en OpenSSL 3, igual que el comando del compromiso |
| SHA256 de `clave.json` descifrado | `4aa2121251ef21966ccbfead7780ccdb117eaa3cc92de40eb3e4b8ff1078cd11`: **coincide**. Volver a serializar con `json.dumps(..., sort_keys=True, ensure_ascii=False, indent=2) + "\n"` reproduce los mismos bytes |
| Huellas por pregunta | **12/12 coinciden** (tabla siguiente) |
| Clave usada por los calificadores A y B | El texto de la clave y el de la rúbrica que recibió cada calificador son **idénticos byte a byte** al descifrado, en las 12 preguntas |
| Clave usada por la calificación automática | `numerica` y `tolerancia` **coinciden** en las 11 preguntas numéricas; S7-04 tiene `null`/`null` en los dos lados |
| Clave usada por el juez de la defensa | El texto de la clave de S7-01 a S7-04 que recibió el juez es idéntico al descifrado |
| Clave en las instrucciones del sustentante (examen y defensa) | **Ausente** en las 12 preguntas |

| Pregunta | SHA256 publicado en `2a50ca2` | SHA256 recalculado | ¿Coincide? |
|---|---|---|---|
| S7-01 | `44445a97c5183b572cfee539e89136e58e2a413e88f56335d0b68810c8fc10bb` | `44445a97c5183b572cfee539e89136e58e2a413e88f56335d0b68810c8fc10bb` | sí |
| S7-02 | `9ab75cd1a81019d405a9b9c1a313a03678a624d19d6eb9a97c2a4c84d0a7782d` | `9ab75cd1a81019d405a9b9c1a313a03678a624d19d6eb9a97c2a4c84d0a7782d` | sí |
| S7-03 | `17e18b310e8fa44e51ec9bfc774f153d70c392bb1e001ccb86c00bcfa8715c0e` | `17e18b310e8fa44e51ec9bfc774f153d70c392bb1e001ccb86c00bcfa8715c0e` | sí |
| S7-04 | `08395115da83078f7b0c94a8c3593040524d93eb7de79f05f4d1a5e43fcb8d89` | `08395115da83078f7b0c94a8c3593040524d93eb7de79f05f4d1a5e43fcb8d89` | sí |
| S7-05 | `552f3c067eb7256319494ea6d4173712b41834c5e43973cfe30812ffd546e359` | `552f3c067eb7256319494ea6d4173712b41834c5e43973cfe30812ffd546e359` | sí |
| S7-06 | `7c2d9dca5f816ae32096163c725b7824db1994aeadd334a16f8a79c70f7f5b5f` | `7c2d9dca5f816ae32096163c725b7824db1994aeadd334a16f8a79c70f7f5b5f` | sí |
| S7-07 | `5a79d0743368403d7b312940f10052d2e1bec93d131c40b76ff0ef0827e2b837` | `5a79d0743368403d7b312940f10052d2e1bec93d131c40b76ff0ef0827e2b837` | sí |
| S7-08 | `c3e023761f5ce7e7797b5927e867ab2ceeab6a5bcd75169a41ecbf223717012d` | `c3e023761f5ce7e7797b5927e867ab2ceeab6a5bcd75169a41ecbf223717012d` | sí |
| S7-09 | `963fac22f03816e9d8710a8b723c826720ddfee27f658c28e2d9bcfbdd192c7e` | `963fac22f03816e9d8710a8b723c826720ddfee27f658c28e2d9bcfbdd192c7e` | sí |
| S7-10 | `215249d539c60009dabf05c00f5e9c3043be65abc93c2315d84b40e23578cc36` | `215249d539c60009dabf05c00f5e9c3043be65abc93c2315d84b40e23578cc36` | sí |
| S7-11 | `a330fe9fd82645d26e75d58ce2a0d6f6697e79678872a38bbe342a3a28d64a8f` | `a330fe9fd82645d26e75d58ce2a0d6f6697e79678872a38bbe342a3a28d64a8f` | sí |
| S7-12 | `813f04b8cf27e91994bff73906fc8dfaadc25d5e563c44494dfcf1f01173526b` | `813f04b8cf27e91994bff73906fc8dfaadc25d5e563c44494dfcf1f01173526b` | sí |

**Cómo verificarlo usted mismo** (desde la raíz del repositorio):

```
git show 2a50ca2c7f5cd6cf6e6f4ce9f6da535ee02acb86:conocimiento/examenes/2026-09-25-diagnostico/S7/clave.enc > /tmp/S7.enc
sha256sum /tmp/S7.enc   # 0355bd38fe70692a541aa87d9c399a94922319563534692d4a9f133ec9a1df6e
openssl enc -d -aes-256-cbc -md sha256 -pbkdf2 -iter 200000 -in /tmp/S7.enc -out /tmp/S7-clave.json \
  -pass file:conocimiento/examenes/2026-09-25-diagnostico/S7/contrasena.txt
sha256sum /tmp/S7-clave.json   # 4aa2121251ef21966ccbfead7780ccdb117eaa3cc92de40eb3e4b8ff1078cd11
cmp /tmp/S7-clave.json conocimiento/examenes/2026-09-25-diagnostico/S7/clave.json && echo identico
python3 -c "import json,hashlib; [print(d['id'], hashlib.sha256(json.dumps({k:d[k] for k in ('id','clave','numerica','tolerancia','rubrica')}, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()) for d in json.load(open('/tmp/S7-clave.json', encoding='utf-8'))]"
git log --format="%H %cI" -- conocimiento/examenes/2026-09-25-diagnostico/S7/compromiso.json
```

**Alcance del compromiso.** Las huellas cubren la clave, el valor numérico, la tolerancia y la rúbrica. **No** cubren el enunciado ni la fuente. Estos se transcriben del registro del flujo; comprobé que el enunciado que recibió el sustentante es idéntico al de esta acta, pero un tercero no puede verificarlo solo con el commit.

## Auditoría de libro cerrado (resumen)

- **Sustentante:** registro `agent-aecb982e36d078093.jsonl` (flujo `wf_eefffca4-9f5`), de 06:03:46 a 06:15:13 UTC.
  - Herramientas: Bash 16 veces, Read 1 y StructuredOutput 1.
  - **0 usos** de WebSearch, WebFetch, curl, wget o URLs.
  - Los `find` excluyeron `conocimiento/examenes`. Los `grep` se limitaron a archivos del primer nivel (`conocimiento/*.md`, `laboratorio/*.md`, etc.) o filtraron esa carpeta (ver la observación de abajo).
  - El único archivo leído fuera del repositorio fue la salida de su propio `grep`, que el harness guardó (`tool-results/bref7mrv1.txt`). Lo declaró en la respuesta, y esa salida no contiene ninguna línea de `examenes/`.
  - Escribió y ejecutó sus propios scripts de python3 en el scratchpad (`s7_calc.py`, `s7_calc2.py`, `s7_nagel.py`).
- **Observación de protocolo:** uno de sus `grep -rn … .` recorrió todo el árbol, incluido `conocimiento/examenes/`, en archivos `.md`, `.json`, `.txt`, `.csv` y `.py`. Filtró esas líneas con `grep -v "conocimiento/examenes"` antes de mostrarlas, así que el sustentante no vio nada de esa carpeta. `clave.enc` no entra en esos patrones y, en todo caso, está cifrado; `compromiso.json` solo tiene huellas. Para rondas futuras conviene `--exclude-dir=examenes` en lugar del filtro posterior.
- **Defensa oral:** registro `agent-ae975c274e2544251.jsonl`, de 06:19:36 a 06:33:34 UTC.
  - Herramientas: Bash 5 veces y StructuredOutput 1.
  - **0 usos** de herramientas web o red.
  - Solo listó el nivel superior del repositorio y ejecutó sus propios scripts (`s7.py`, `s7b.py`, `s7c.py`) en el scratchpad.
- **Veredicto:** sin violaciones, con una observación de protocolo (el `grep` recursivo filtrado).
- **Límite de independencia:** el examinador, el sustentante, los calificadores y el juez son instancias del mismo modelo dentro del mismo flujo. La independencia es de procedimiento (contextos separados, clave comprometida antes), no institucional. El calificador A verificó dos datos con búsqueda web; eso está permitido a los calificadores, no al sustentante.

---

## S7-01 — Machine learning en asset pricing: regularización ridge/lasso/elastic net y resultados de Gu-Kelly-Xiu (2020) (derivacion)

### Enunciado
Considere la regresión penalizada de Gu, Kelly y Xiu (2020, RFS) con pérdida cuadrática L(θ) = (1/2NT) Σ_{i,t} (r_{i,t+1} − z_{i,t}'θ)² + φ(θ; λ, ρ), donde φ(θ; λ, ρ) = λ(1−ρ) Σ_j |θ_j| + (1/2) λρ Σ_j θ_j². Suponga un diseño ortonormal estandarizado (Z'Z/NT = I_P), de modo que el estimador MCO es b = Z'r/NT.

(a) Derive la solución cerrada, coordenada por coordenada, del elastic net (incluya la condición de subgradiente que produce ceros exactos) y muestre los casos especiales ρ = 1 (ridge) y ρ = 0 (lasso).

(b) Con b = (0.50, −0.12, 0.03, 0.20) y λ = 0.10, calcule θ̂ para ρ = 0.5, ρ = 1 y ρ = 0. RESULTADO NUMÉRICO PRINCIPAL: θ̂_1 con ρ = 0.5 (4 decimales).

(c) Con ρ = 0.5, ¿cuál es el menor λ que anula los cuatro coeficientes? ¿Puede ridge producir ceros exactos?

(d) En GKX (2020), ENet+H obtiene un R²oos mensual (panel de acciones) inferior al de árboles y redes. Dé las magnitudes aproximadas de OLS (todas las variables), OLS-3+H, ENet+H, RF, GBRT+H y NN3; explique qué implica sobre la forma funcional del premio por riesgo; describa cómo eligen hiperparámetros (esquema de entrenamiento/validación/prueba y por qué no usan validación cruzada k-fold) y el papel de la pérdida de Huber.

### Clave (texto descifrado, idéntico al de `clave.json`)
(a) Con Z'Z/NT = I: (1/2NT)||r − Zθ||² = const − θ'b + ½||θ||² = ½||θ − b||² + const. El problema se separa por coordenada: min ½(θ_j − b_j)² + λ(1−ρ)|θ_j| + ½λρθ_j². Si θ_j ≠ 0: θ_j − b_j + λ(1−ρ)sign(θ_j) + λρθ_j = 0 ⇒ θ_j = (b_j − λ(1−ρ)sign θ_j)/(1+λρ). Subgradiente en 0: 0 ∈ −b_j + λ(1−ρ)[−1,1] ⇔ |b_j| ≤ λ(1−ρ) ⇒ θ_j = 0. Solución: θ̂_j = S(b_j, λ(1−ρ))/(1+λρ), con S(x,γ) = sign(x)(|x|−γ)_+ (umbral suave seguido de contracción proporcional). ρ = 1 (ridge): θ̂ = b/(1+λ). ρ = 0 (lasso): θ̂ = S(b, λ).

(b) ρ = 0.5: umbral 0.05, divisor 1.05 ⇒ θ̂ = (0.45/1.05, −0.07/1.05, 0, 0.15/1.05) = (0.4286, −0.0667, 0, 0.1429). ρ = 1: b/1.1 = (0.4545, −0.1091, 0.0273, 0.1818). ρ = 0: S(b, 0.10) = (0.40, −0.02, 0, 0.10). Principal: θ̂_1 = 0.428571 (verificado numéricamente con optimización directa).

(c) Todos cero si λ(1−ρ) ≥ max|b_j| = 0.50 ⇒ λ ≥ 1.0. Ridge nunca produce ceros exactos (salvo b_j = 0): contrae proporcionalmente; lasso sesga todos los coeficientes grandes por una constante λ; EN combina selección (ℓ1) y estabilidad ante predictores correlacionados (efecto de agrupamiento, ℓ2).

(d) GKX Tabla 1 (R²oos mensual, %): OLS −3.46; OLS-3+H 0.16; PLS 0.27; PCR 0.26; ENet+H 0.11; GLM+H 0.19; RF 0.33; GBRT+H 0.34; NN1 0.33; NN2 0.39; NN3 0.40; NN4 0.39; NN5 0.36. Interpretación: la ganancia proviene de no linealidades e interacciones entre características (que un modelo lineal penalizado no captura); los predictores dominantes son tendencias de precio (momentum, reversión de corto plazo, momentum industrial), liquidez y volatilidad. Beneficio económico: long-short de deciles con NN4 Sharpe ≈ 1.35 (VW) y 2.45 (EW); timing del S&P 500 0.77 vs 0.51 buy-and-hold. Esquema: 1957–1974 entrenamiento, 1975–1986 validación (12 años), 1987–2016 prueba; reestiman una vez al año ampliando el entrenamiento y rodando la validación; hiperparámetros (λ, ρ, etc.) se eligen en la muestra de validación; no usan CV para preservar el orden temporal (evitar fuga). Huber: pérdida cuadrática para errores pequeños y absoluta para grandes, robusta a colas pesadas de retornos; mejora OLS, ENet, GLM, GBRT. R²oos se mide contra pronóstico cero (denominador sin desmediar).

**Valor numérico principal comprometido:** 0.428571 ± 0.001.

**Rúbrica:** 5 puntos. (a) 1.5 pts: reducción a problema separable (0.5), FOC y condición de subgradiente |b_j| ≤ λ(1−ρ) (0.5), casos ridge y lasso correctos (0.5). (b) 1.5 pts: 0.5 por cada vector correcto; θ̂_1(ρ=0.5) = 0.4286 obligatorio para el crédito de ese inciso (tolerancia ±0.001). (c) 0.5 pts: λ = 1.0 y ridge sin ceros exactos con justificación. (d) 1.5 pts: magnitudes de R²oos al menos para OLS, ENet+H y NN3 con orden correcto (0.5); explicación no linealidad/interacciones y predictores dominantes (0.5); esquema train/validación/prueba sin CV por orden temporal y papel de Huber (0.5). Cero en (d) si se afirma que GKX usan k-fold aleatorio.

### Fuente
Gu, S., Kelly, B., Xiu, D. (2020), 'Empirical Asset Pricing via Machine Learning', Review of Financial Studies 33(5): 2223–2273 (Tabla 1; sección 1.3 y 3); Zou, H., Hastie, T. (2005), 'Regularization and variable selection via the elastic net', JRSS-B 67(2); Hastie, Tibshirani, Friedman, The Elements of Statistical Learning, cap. 3. Cálculo verificado con python3.

### Respuesta del sustentante (completa)
Nota de procedimiento: todos los cálculos del examen los hice con mis propios scripts de python3, escritos en el scratchpad de la sesión (s7_calc.py y s7_calc2.py). No usé internet. La única ruta fuera del repo que leí fue la salida guardada por el harness de mi propio grep sobre archivos del repo.

(a) Derivación. Con Z'Z/NT = I, la parte cuadrática es (1/2NT)||r − Zθ||² = cte + ½θ'θ − θ'b, con b = Z'r/NT. El problema se separa por coordenada:

min_θj ½θj² − θj·bj + λ(1−ρ)|θj| + ½λρθj².

Condición de subgradiente (KKT): 0 ∈ (1+λρ)θj − bj + λ(1−ρ)·sj, donde sj = sign(θj) si θj ≠ 0 y sj ∈ [−1, 1] si θj = 0.

- θj = 0 es óptimo si y solo si |bj| ≤ λ(1−ρ). Así aparecen los ceros exactos.
- Si no, θ̂j = sign(bj)·(|bj| − λ(1−ρ))₊ /(1+λρ). Es decir, primero se aplica umbral suave (soft threshold) y después se encoge de forma proporcional.

Casos especiales:

- ρ = 1 (ridge): θ̂ = b/(1+λ). Encoge de forma proporcional y nunca produce ceros.
- ρ = 0 (lasso): θ̂ = sign(b)(|b| − λ)₊. Es umbral suave puro.

(b) Con λ = 0.10:

- ρ = 0.5: umbral 0.05, divisor 1.05. θ̂ = (0.4286, −0.0667, 0, 0.1429).
- ρ = 1: θ̂ = b/1.1 = (0.4545, −0.1091, 0.0273, 0.1818).
- ρ = 0: θ̂ = (0.40, −0.02, 0, 0.10).

RESULTADO PRINCIPAL: θ̂1 (ρ = 0.5) = 0.45/1.05 = 0.4286.

(c) Con ρ = 0.5, todos los coeficientes son cero si λ(1−ρ) ≥ max|bj| = 0.50, o sea λ ≥ 1.0. Ridge no produce ceros exactos: θ̂j = bj/(1+λ) ≠ 0 siempre que bj ≠ 0, porque la penalización cuadrática tiene derivada 0 en el origen y no crea una región de subgradiente.

(d) Evidencia de GKX (2020). El repo solo verifica lo cualitativo: árboles y redes a veces duplican el desempeño de las regresiones, y todos los métodos coinciden en que las señales dominantes son momentum, liquidez y volatilidad (02:160; 06:126). Las magnitudes que siguen vienen de mi memoria de la Tabla 1 de GKX. No están en el repo.

- R²oos mensual, panel completo, prueba 1987-2016: OLS+H con las ~920 variables ≈ −3.46%; OLS-3+H ≈ 0.16%; ENet+H ≈ 0.11%; RF ≈ 0.33%; GBRT+H ≈ 0.34%; NN3 ≈ 0.40%, el mejor. PLS y PCR ≈ 0.26-0.27%.
- Qué implica: un modelo lineal penalizado con cientos de predictores no le gana a un OLS de 3 variables (tamaño, B/M y momentum). La ganancia de árboles y redes viene de no linealidades, sobre todo interacciones entre características y entre características y estado macro. Las redes poco profundas ganan a las profundas porque la razón señal-ruido es baja.
- Inferencia: el premio por riesgo no es una función lineal y aditiva de las características. Aun así, el R² es de décimas de punto porcentual.
- Hiperparámetros: la muestra es 1957-2016. El entrenamiento inicial es de 18 años (1957-74), la validación de 12 (1975-86) y la prueba de 30 (1987-2016). Se reestima una vez al año: la ventana de entrenamiento crece un año y la de validación, de 12 años, avanza. λ y ρ del ENet, y la profundidad, los árboles, la tasa de aprendizaje, etc., se eligen con una malla que maximiza el ajuste en validación.
- Por qué no usan k-fold: la validación debe ser posterior al entrenamiento y la prueba posterior a ambas. Así se conserva el orden temporal y se evita la fuga por dependencia serial y no estacionariedad. También reduce el costo computacional.
- Huber (+H): H(x) = x² si |x| ≤ ξ y 2ξ|x| − ξ² si |x| > ξ, con ξ adaptativo (un cuantil alto de los residuos; detalle de memoria). Los rendimientos individuales tienen colas pesadas. Con 920 regresores, el MCO se sobreajusta a los outliers. Huber hace la pérdida robusta y mejora a OLS, ENet, GLM y GBRT.

### Calificación automática
**Dentro de tolerancia:** esperado 0.428571, obtenido 0.4286, tolerancia ±0.001 (|diferencia| = 2.9e-05).

### Calificación
**Calificador A: 5.0/5.** (a) Completo: el problema se separa por coordenada, da la condición de subgradiente |b_j| ≤ λ(1−ρ) para los ceros exactos y la solución S(b_j, λ(1−ρ))/(1+λρ), con los casos ridge y lasso correctos. (b) Los tres vectores coinciden con la clave; θ̂_1 = 0.4286. (c) λ ≥ 1.0, y ridge no produce ceros porque su derivada en el origen es 0. (d) Las magnitudes de la Tabla 1 coinciden (OLS+H −3.46, OLS-3+H 0.16, ENet+H 0.11, RF 0.33, GBRT+H 0.34, NN3 0.40). Explica no linealidades e interacciones y nombra los predictores dominantes. El esquema 1957-74 / 1975-86 / 1987-2016 es correcto, igual que el argumento contra k-fold (orden temporal) y la fórmula y el papel de Huber. Marca con honestidad lo que cita de memoria. No encontré errores.

**Calificador B: 5.0/5.** (a) 1.5/1.5. Separa el problema por coordenada, escribe la condición KKT con subgradiente |b_j| ≤ λ(1−ρ) y da bien ridge b/(1+λ) y lasso S(b,λ). (b) 1.5/1.5. Los tres vectores coinciden con la clave; θ̂1 = 0.4286. (c) 0.5/0.5. λ ≥ 1.0 y ridge sin ceros exactos, justificado con la derivada nula de la penalización ℓ2 en el origen. (d) 1.5/1.5. Da −3.46 (OLS+H, que es la etiqueta de la Tabla 1 de GKX), 0.16, 0.11, 0.33, 0.34 y 0.40, en el orden correcto. Atribuye la ganancia a no linealidades e interacciones y nombra los predictores dominantes (momentum, liquidez, volatilidad). Describe bien el esquema 18/12/30 años con reestimación anual, la razón temporal para no usar k-fold y la fórmula de Huber con ξ adaptativo. No encontré citas inventadas.

|A − B| = 0 ≤ 1: promedio 5.0, sin arbitraje.

### Defensa oral
**Repregunta 1.** Su solución cerrada depende de que Z'Z/NT = I. En GKX las características se rankean en [-1, 1] y varias están muy correlacionadas, como tamaño, volumen en dólares y bid-ask, o momentum de 12 y de 6 meses. Suponga dos predictores con correlación 0.95 y el mismo efecto verdadero. ¿Qué hace el lasso (ρ = 0) con ese par y qué cambia con ρ = 0.5? Cuando el diseño no es ortonormal, ¿sigue siendo |b_j| ≤ λ(1−ρ) la condición para un cero exacto? Si no lo es, ¿qué la reemplaza? Piense en el residuo parcial del coordinate descent. Por último, si cambia la pérdida cuadrática por Huber (ENet+H), ¿se conserva la fórmula de umbral suave dividido entre (1+λρ)? ¿Qué papel juegan las observaciones con residuo mayor que ξ?

**Repregunta 2.** El ENet puede reproducir OLS-3+H como caso particular: basta con anular todo salvo tamaño, B/M y momentum. ¿Por qué, entonces, ENet+H con λ y ρ elegidos en validación puede quedar fuera de muestra por debajo de OLS-3+H? En su respuesta discuta tres cosas: el sesgo de encogimiento sobre los coeficientes que sobreviven, el ruido al elegir λ cuando el R² es de décimas de punto porcentual y el conocimiento previo que OLS-3 trae 'gratis' desde la literatura. Si la brecha de 0.11% contra 0.40% frente a NN3 no fuera estadísticamente significativa según la prueba que usan GKX, ¿qué quedaría de su conclusión de que el premio por riesgo no es lineal y aditivo? ¿Qué modelo lineal con interacciones entre características y variables macro podría cerrar esa brecha sin que haya una no linealidad 'genuina'?

**Respuesta del sustentante (completa):**

Notación: pérdida ½(1/NT)‖r−Zθ‖² + λ(1−ρ)‖θ‖₁ + ½λρ‖θ‖²; a_j = z_j'r/NT; G = Z'Z/NT.

PREGUNTA 1

(a) Par con c = 0.95 y el mismo β, lasso (ρ = 0).

- Con los dos coeficientes activos: θ1+θ2 = (a1+a2−2λ)/(1+c) y θ1−θ2 = (a1−a2)/(1−c).
- En la dirección de la diferencia la curvatura es 1−c = 0.05, así que el ruido de a1−a2 se amplifica 20 veces.
- θ2 se hace cero exacto en cuanto a1−a2 ≥ [(1−c)/(1+c)]·(a1+a2−2λ). Basta una ventaja muestral de 2.6% de la señal conjunta neta.
- En la población la solución es simétrica (θ = β − λ/(1+c) para cada uno). En la muestra, el lasso se queda con UNO de los dos, elegido al azar, y le carga el efecto de ambos (≈ β(1+c) − λ).
- Simulación con coordinate descent (n = 3000, β = 0.03, σ = 1, λ = 0.02): en 76% de las muestras anula exactamente uno, y cuál anula cambia de una muestra a otra.
- En GKX, que reestiman cada año, 'tamaño' puede entrar un año como mve y al siguiente como dolvol o baspread. El pronóstico se parece; la interpretación y la importancia de las variables no son estables.

Con ρ = 0.5.

- La parte ridge suma λρ a la curvatura en todas las direcciones: θ1−θ2 = (a1−a2)/(1−c+λρ) y θ1+θ2 = (a1+a2−2λ(1−ρ))/(1+c+λρ).
- Es el agrupamiento de Zou-Hastie: los coeficientes de predictores casi colineales se atraen y se reparten el efecto.
- Lo que decide no es ρ sino el tamaño de λρ frente a 1−c.
  - Con el mismo umbral (λ = 0.04, ρ = 0.5), λρ = 0.02 < 0.05 y todavía se anula uno en 67% de las muestras.
  - Hace falta λρ ≫ 1−c: con λ = 0.5 y ρ = 0.96 baja a 8%.
- Con ρ = 0.5 fijo, como en GKX, λρ = λ(1−ρ) es el propio umbral, que está al nivel del ruido de a_j. El agrupamiento es parcial, no está garantizado.

(b) Diseño no ortonormal. |b_j| ≤ λ(1−ρ) YA NO es la condición. La reemplaza la condición KKT sobre el residuo parcial:
  θ̂_j = 0 ⇔ |(1/NT)·z_j'(r − Z_{−j}θ̂_{−j})| ≤ λ(1−ρ)

El paso de coordinate descent es θ_j ← S((1/NT)z_j'r^(j), λ(1−ρ)) / (d_j + λρ), con d_j = z_j'z_j/NT. Tres consecuencias:

- (i) La condición es conjunta. En el par, a2 es grande, pero una vez que entra x1 el residuo parcial de x2 vale a2 − c·θ1 y cae bajo el umbral. Al revés, una variable con b_j marginal chico puede entrar por supresión.
- (ii) Aunque las características no estén correlacionadas, un rango uniforme en [−1, 1] tiene d_j = 1/3, no 1. El umbral en unidades de coeficiente es λ(1−ρ)/d_j y el divisor es d_j + λρ; la fórmula cerrada hay que reescalarla.
- (iii) Por bloques: θ_A = (G_AA + λρI)⁻¹(a_A − λ(1−ρ)s_A), junto con ‖Z_{Aᶜ}'(r − Z_Aθ_A)/NT‖_∞ ≤ λ(1−ρ).

(c) Huber (ENet+H). NO se conserva la fórmula cerrada.

- La condición de primer orden es (1/NT)·Σ_i z_ij·ψ_ξ(e_i) = λ(1−ρ)s_j + λρθ_j, con ψ_ξ = clip(e, −ξ, ξ) (hay un factor 2 según cómo normalice GKX).
- Separando dentro de ξ (I) y fuera de ξ (O):
  θ = (Z_I'Z_I/NT + λρI)⁻¹·[Z_I'r_I/NT + ξ·Z_O'sign(e_O)/NT − λ(1−ρ)s]
- Dado O, es un umbral suave sobre un 'b huberizado' dividido entre (d_j^I + λρ). Aunque Z'Z/NT = I, Z_I'Z_I/NT no es I.
- Pero O depende de θ: es un punto fijo que se resuelve por IRLS/MM con la seudo-respuesta Zθ + ψ(e).
- La fórmula original solo se recupera si en la solución ningún residuo supera ξ.

Papel de las observaciones con |e| > ξ:

- Aportan al score un voto acotado ±ξ·z_ij: cuenta su signo, no su magnitud.
- No aportan curvatura.
- Una característica cuyo b_j viene de pocos rendimientos extremos (microcaps con +300%) pierde ese empuje y cae más fácilmente bajo el umbral. Huber cambia QUÉ variables sobreviven, no solo cuánto se encogen.

PREGUNTA 2

Punto de partida: que la clase de modelos contenga a OLS-3 no significa que el estimador lo alcance. La trayectoria {θ(λ, 0.5)} en general no pasa por OLS-3. Para reproducirlo harían falta penalizaciones distintas por coeficiente (penalty factors, lasso adaptativo o relajado), y el ENet de GKX no las tiene.

1) Sesgo de encogimiento sobre los sobrevivientes.
- Para anular unos 917 de 920 regresores (94 características × (8 macro + constante) + 74 industrias), λ(1−ρ) tiene que estar por encima del ruido de los a_j.
- Ese mismo λ resta λ(1−ρ) a los tres verdaderos y los divide entre (d + λρ). Con señales débiles, del tamaño del umbral, se come casi todo el efecto.
- El pronóstico queda tímido. Además elige representantes erráticos de cada grupo colineal, y los productos z⊗x son casi colineales con z porque x es persistente.

2) Ruido al elegir λ.
- El criterio de validación (12 años) es un R² de décimas de punto. La curva frente a λ es plana.
- Su error muestral, dominado por choques comunes de mercado que castigan a todos los activos cuando el benchmark es cero, es del orden de las diferencias entre λ vecinos.
- El argmax tiene maldición del ganador: elige el λ con ruido favorable en validación, así que fuera de muestra rinde menos.
- Como se reelige cada año, λ salta:
  - los años con λ chico meten ruido, y la varianza del pronóstico entra 1 a 1 en el ECM;
  - los años con λ grande dan el pronóstico cero.
- OLS-3 no tiene nada que afinar.

3) Conocimiento previo 'gratis'.
- Tamaño, B/M y momentum salen de décadas de búsqueda de la profesión, en parte con datos que se traslapan con la prueba de GKX (1987-2016): FF 1992, JT 1993.
- Es un prior muy informativo, con algo de look-ahead, que OLS-3 no paga en grados de libertad. El ENet debe descubrir el soporte entre 920 candidatos y paga un umbral de ~σ√(2 ln p / n).
- Una comparación justa sería un ENet sin penalización sobre esas 3 variables, o un OLS-3 cuya selección use solo datos previos a cada ventana.

Si la brecha 0.11% vs 0.40% no fuera significativa con el Diebold-Mariano de GKX (diferencia de pérdidas promediada en la sección cruzada cada mes, ~360 meses, EE Newey-West):

- 'El premio no es lineal-aditivo' deja de ser una conclusión y pasa a ser una hipótesis ni rechazada ni demostrada. No significativo con baja potencia no es evidencia de linealidad.
- Quedaría lo siguiente:
  - (i) El patrón de que árboles y redes superan a los lineales. No son pruebas independientes: mismos datos y mismos predictores.
  - (ii) La evidencia de portafolio (Sharpe long-short), que necesita su propia prueba (Jobson-Korkie-Memmel o bootstrap), aunque ahí puede haber más potencia porque se agregan miles de acciones.
  - (iii) El punto más importante: la comparación relevante es contra el MEJOR lineal. PCR/PLS dan 0.26-0.27, así que la prima atribuible a la no linealidad es ~0.13 pp, no 0.29. Casi todo lo que pierde el ENet se debe a imponer esparsidad sobre señales densas y colineales, no a la linealidad.

Modelo lineal que podría cerrar la brecha:
  E_t[r_{i,t+1}] = z_{i,t}'·B·x_t, con B = ΓΛ' de rango reducido K
- Son precios de riesgo por característica que varían con el estado macro a través de pocos factores, al estilo IPCA de Kelly-Pruitt-Su con λ_t = Λx_t.
- Se estima con encogimiento denso (ridge/PLS), no con lasso.
- Se amplían las variables de estado: volatilidad realizada, rendimiento pasado del mercado (crashes de momentum), liquidez agregada.
- Opcionalmente se añaden productos característica×característica de bajo orden (tamaño×reversión, tamaño×iliquidez) y splines por característica.
- Todo es lineal en parámetros. Si cierra la brecha, la conclusión correcta es 'coeficientes que dependen del estado / interacciones de bajo orden', no 'no linealidad genuina'.
- Prueba: DM de NN3 contra este modelo, y medir qué parte de la ventaja de la red explica su aproximación de segundo orden (H de Friedman).

Nota de procedimiento (vale para toda la sección): no usé internet ni herramientas web, y no leí conocimiento/examenes/. Lo único que vi del repo fue el listado de su nivel superior. Las cifras simuladas y numéricas de S7-01 a S7-04 salen de scripts de python3 (numpy/scipy) que escribí y ejecuté en el scratchpad de la sesión, que está fuera del repo; no leí ahí ningún otro archivo.

**Dictamen del juez: deducción 0.0.** Motivo textual del juez (lo emitió en inglés):

> The defense holds up. The algebra for the correlated pair is correct: (1+c) and (1-c) curvature, a zero condition of 2.6% of the net signal, a symmetric population solution, and the dropped coefficient's effect loaded onto the other at about beta(1+c)-lambda. The ENet case is right: lambda*rho is added to 1-c, and the defense correctly states that grouping depends on lambda*rho relative to 1-c, not on rho alone. For a non-orthonormal design it gives the right KKT condition on the partial residual, the coordinate descent step S(.)/(d_j+lambda*rho), and the rescaling d_j=1/3 for a uniform rank. It shows that Huber breaks the closed form: the score uses psi clipped at xi, observations outside xi give a bounded vote and add no curvature, and the fixed point is solved by IRLS. On Q2 it correctly rejects the premise that the ENet path passes through OLS-3, which would need per-coefficient penalty factors. It covers shrinkage bias, winner's curse and noise in choosing lambda, and the literature prior with look-ahead. It reads correctly what is left if the result is not significant (the right comparison is against PCR/PLS at 0.26-0.27) and proposes a reasonable linear model: reduced rank z'Bx with dense shrinkage and low-order interactions. The count of 920 regressors and the DM test with about 360 months are consistent with GKX.

**Puntaje final: 5.0/5** (A 5.0, B 5.0; promedio 5.0; deducción de la defensa 0.0).

### Hueco
Ninguno en la respuesta. Las magnitudes de la Tabla 1 de GKX salieron de memoria y el sustentante lo declaró: la base solo guarda lo cualitativo (caps. 02 y 06). En la defensa oral no hubo deducción. Resolvió el diseño no ortonormal (condición KKT sobre el residuo parcial y reescalamiento por d_j), mostró que con Huber se pierde la fórmula cerrada y comparó contra el mejor modelo lineal (PCR/PLS 0.26-0.27), no contra el ENet.

**Acción para la base:** guardar la Tabla 1 de GKX (R²oos por método) y el esquema 1957-74 / 1975-86 / 1987-2016 en el cap. 02 o en el 06.

---

## S7-02 — R² fuera de muestra, benchmark y la 'virtud de la complejidad' (Kelly-Malamud-Zhou 2024) y sus críticas (concepto-evidencia)

### Enunciado
(a) Un modelo pronostica excesos de retorno mensuales de acciones individuales. En la muestra de prueba: Σ r² = 1,000; Σ (r − r̄_hist)² = 1,030 (r̄_hist = media histórica recursiva de cada acción); Σ (r − r̂)² = 998. Calcule el R²oos con benchmark de pronóstico cero (GKX 2020) y con benchmark de media histórica (Campbell-Thompson 2008). ¿Cuál es apropiado para acciones individuales y por qué?

(b) Suponga E[r] = E[r̂] = 0, Var(r) = σ², r̂ = k·σ·f con f estandarizado y corr(f, r) = ρ. Derive R²oos = 2ρk − k². Con ρ = 0.08 y k = 0.25 calcule R²oos. RESULTADO NUMÉRICO PRINCIPAL: este R²oos en decimal (no en %). Muestre además que la estrategia de timing con posición w_t = r̂_t tiene rendimiento esperado positivo y, bajo normalidad conjunta, Sharpe por periodo ρ/√(1+ρ²) independiente de k. ¿Qué k maximiza R² y cuál es ese máximo?

(c) Relacione (b) con el argumento de Kelly, Malamud y Zhou (2024, JF) sobre la 'virtud de la complejidad': defina c = P/T, qué predice su teoría para R² y para el Sharpe de timing cuando c crece (incluso c > 1), y su diseño y resultado empíricos principales.

(d) Exponga al menos dos críticas publicadas en 2025, con su mecanismo y evidencia cuantitativa, y dé un veredicto razonado sobre qué parte del argumento sobrevive.

### Clave (texto descifrado, idéntico al de `clave.json`)
(a) GKX: R² = 1 − 998/1000 = 0.20%. Media histórica: R² = 1 − 998/1030 = 3.11%. Para acciones individuales el benchmark correcto es cero: la media histórica por acción es tan ruidosa que pronostica peor que cero (1,030 > 1,000) y 'baja la vara'; GKX reportan que usar la media histórica infla el R² ≈ 3 puntos porcentuales (p. ej., OLS-3 pasaría a 3.74% mensual). Para el índice agregado la media histórica sí es benchmark razonable (Campbell-Thompson; Goyal-Welch).

(b) E[(r − r̂)²] = σ² − 2kρσ² + k²σ² ⇒ R² = 1 − (1 − 2ρk + k²) = 2ρk − k². Con ρ = 0.08, k = 0.25: 0.04 − 0.0625 = −0.0225 (−2.25%). R² < 0 siempre que k > 2ρ = 0.16, aunque la correlación sea positiva. Timing: E[r̂ r] = kρσ² > 0 (= 0.02σ²). Con normalidad conjunta, Var(r̂ r) = k²σ⁴(1+ρ²) ⇒ SR = ρ/√(1+ρ²) = 0.0797 por periodo (≈0.276 anual si mensual i.i.d.), invariante a k. k* = ρ = 0.08 ⇒ R²max = ρ² = 0.0064. Lección: R² penaliza el error de escala (varianza del pronóstico); el Sharpe de timing es invariante a escala, así que R² negativo no implica ausencia de valor económico (el mapeo de Campbell-Thompson R²→Sharpe supone pronóstico bien escalado).

(c) KMZ (JF 79(1), 2024): complejidad c = P/T (parámetros/observaciones). Con modelos mal especificados y regresión ridge(less), prueban que el Sharpe fuera de muestra del timing crece con c, incluso más allá del umbral de interpolación c = 1; el R² puede ser muy negativo (máxima varianza cerca de c ≈ 1 sin contracción, 'doble descenso'). Empírico: 15 predictores de Goyal-Welch transformados en hasta P = 12,000 random Fourier features, ventanas rodantes T = 12 (también 60, 120) meses, CRSP 1926–2020: mejora de Sharpe vs buy-and-hold ≈ 0.47 anual con t ≈ 3, pese a R² negativo en la mayoría de modelos; las posiciones se parecen a una estrategia larga que reduce exposición antes de recesiones.

(d) Nagel (2025, NBER WP 34104, 'Seemingly Virtuous Complexity in Return Prediction'): con P ≫ T el pronóstico RFF es un promedio ponderado de los T retornos de entrenamiento con pesos por similitud (kernel); con T = 12 la similitud refleja proximidad temporal ⇒ promedio ponderado por recencia = momentum de serie de tiempo con timing de volatilidad; en datos artificiales con reversión el método construye el mismo momentum y pierde ⇒ el desempeño viene de que ese momentum funcionó históricamente, no de 'aprender'. Buncic (2025, SSRN 5239006, 'Simplified…'): los resultados dependen de restringir el intercepto a cero y de un esquema de agregación poco convencional que penalizan a los modelos simples; una regresión lineal de ventana expansiva con contracción leve logra Sharpe 0.699 vs 0.485 del modelo más complejo de KMZ; incluso la media histórica los supera. Elmore y Strauss (2025, Economics Letters, 'Is complexity virtuous?'): el promedio móvil de 12 meses de retornos tiene correlación 97.5% con los pronósticos RFF de alta penalización; sin ganancias en Sharpe, alfa ni utilidad. Veredicto: sobrevive el punto teórico (R² no es suficiente para evaluar valor económico; modelos sobreparametrizados con ridge pueden generalizar), no sobrevive la afirmación empírica de que la complejidad per se extrae predictibilidad adicional de los predictores macro; exigir benchmarks simples (momentum/vol-timing, promedio móvil, modelo con intercepto) y evaluar con la misma agregación.

**Valor numérico principal comprometido:** -0.0225 ± 0.0005.

**Rúbrica:** 5 puntos. (a) 1 pt: ambos R² correctos (0.20% y 3.11%) (0.5) y justificación del benchmark cero para acciones con referencia a la inflación ≈3 pp de GKX (0.5). (b) 1.5 pts: derivación de 2ρk − k² (0.5); R² = −0.0225 (0.25, tolerancia ±0.0005); E[r̂ r] > 0 y Sharpe invariante a k (0.5); k* = ρ y R²max = 0.0064 (0.25). (c) 1 pt: definición de c y predicciones sobre Sharpe y R² (0.5); diseño empírico (RFF, Goyal-Welch, T = 12, P hasta 12,000) y resultado ≈0.47 de mejora de Sharpe con R² negativo (0.5). (d) 1.5 pts: 0.5 por cada crítica correcta con mecanismo y dato (máx. 1.0) y 0.5 por veredicto que separe resultado teórico de afirmación empírica. Penalizar −0.5 si se atribuyen cifras inventadas.

### Fuente
Gu, Kelly, Xiu (2020, RFS 33(5)) sección 2 y nota 34; Campbell, J., Thompson, S. (2008), RFS 21(4): 1509–1531; Kelly, B., Malamud, S., Zhou, K. (2024), 'The Virtue of Complexity in Return Prediction', Journal of Finance 79(1): 459–503; Nagel, S. (2025), NBER WP 34104; Buncic, D. (2025), SSRN 5239006; Elmore, R., Strauss, J. (2025), 'Is complexity virtuous?', Economics Letters. Álgebra verificada por simulación en python3.

### Respuesta del sustentante (completa)
(a) R²oos con benchmark cero (GKX) = 1 − 998/1000 = 0.0020 (0.20%). Con benchmark de media histórica (Campbell-Thompson, 20:§2.11) = 1 − 998/1030 = 0.0311 (3.11%).

Para acciones individuales conviene el benchmark cero. La media histórica de cada acción se estima con muchísimo ruido: aquí pronostica peor que cero (1030 > 1000). Usarla infla el R² con un rival débil, y el mismo modelo pasa de 0.2% a 3.1%. Campbell-Thompson lo pensaron para el índice, donde la media histórica es un rival serio.

(b) Derivación. Con E[r] = E[r̂] = 0, Var(r) = σ², r̂ = kσf, Var(f) = 1 y Cov(f, r) = ρσ:

- E[r r̂] = kρσ².
- E(r − r̂)² = σ² − 2kρσ² + k²σ².
- R²oos = 1 − E(r − r̂)²/E r² = 2ρk − k².

Con ρ = 0.08 y k = 0.25: 0.04 − 0.0625 = −0.0225. RESULTADO PRINCIPAL: −0.0225. Una simulación Monte Carlo propia da ≈ −0.022.

Timing con w = r̂: E[w r] = kρσ² > 0 si ρ > 0.

Sharpe por periodo: con normalidad conjunta y medias cero, Isserlis da Var(XY) = VarX·VarY + Cov². Entonces Var(r̂ r) = k²σ⁴(1 + ρ²) y SR = kρσ²/(kσ²√(1+ρ²)) = ρ/√(1+ρ²). La k se cancela.

- SR por periodo = 0.0797, y ≈ 0.276 anual si los periodos son meses.
- R² se maximiza en k = ρ, donde R²max = ρ² = 0.0064.

Moraleja: con la escala mal puesta, el R² es negativo aunque la señal tenga valor económico. El R² castiga la escala y el Sharpe no la ve.

(c) Kelly-Malamud-Zhou (JF 79(1), 2024; repo 02:180, 20:§2.11) definen la complejidad c = P/T: parámetros entre observaciones de entrenamiento.

Teoría (regresión ridge/ridgeless sobre random Fourier features, modelo mal especificado):

- Cerca de c = 1 la varianza explota (double descent) y el R²oos puede ser muy negativo.
- Con c > 1, el ridgeless de norma mínima regulariza de forma implícita: el pronóstico se encoge (k → 0) y el R² sube hacia ~0 por abajo.
- El Sharpe del timing, que es invariante a la escala como en (b), crece con c. Con ridge óptimo, R² y Sharpe crecen ambos con c.
- Conexión con (b): la complejidad eleva la correlación ρ mientras la escala k queda mal calibrada.

Diseño empírico (de memoria, no verificado en el repo): rendimiento mensual del mercado de EUA con los ~15 predictores de Welch-Goyal, expandidos con hasta P ≈ 12,000 RFF, ventanas móviles de T = 12 meses (c de hasta ~1000) y una malla de shrinkage.

Resultado: el R²oos es negativo o cercano a cero, pero el Sharpe y el alfa del timing crecen con c. Recuerdo un Sharpe del orden de 0.4-0.5 anual, sin verificar, y posiciones que se reducen antes de recesiones.

(d) Críticas de 2025:

1) Nagel (2025, NBER w34104, 'Seemingly Virtuous Complexity'; repo 06:282, 20:191). Con P ≫ T y T = 12, el pronóstico RFF es un promedio de los 12 rendimientos de entrenamiento, ponderados por similitud. Como los predictores son persistentes, la similitud equivale a cercanía en el tiempo, y el pronóstico se vuelve momentum cronometrado por volatilidad. Con datos artificiales de reversión construye la misma estrategia y le va mal.
   Evidencia cuantitativa propia (ilustración con datos sintéticos, no réplica): con 15 predictores AR(1) φ = 0.98, P = 12,000, T = 12 y ridgeless, el peso medio sobre r_{t−1} es 0.905, 0.701 o 0.284 (γ = 0.5, 1, 2), y los otros 11 rezagos pesan casi 0.
2) Buncic (2025, SSRN 5239006, 'Simplified…'). El repo solo verifica el título (20:192). De memoria, sin verificar: el resultado depende de decisiones de diseño (sin intercepto, estandarización) y de un posicionamiento casi siempre largo, y especificaciones simples lo reproducen.

Complemento de 2026 (repo 02:180): Guo-Huang-Li-Yu documentan el double descent, pero ni ridge ni ridgeless superan a la media histórica.

Veredicto (grado C, repo 20:277):

- Sobrevive el punto estadístico: un R² negativo no implica cero valor económico, el shrinkage implícito existe y un modelo sobreparametrizado no necesariamente está sobreajustado.
- No sobrevive, o no está probado, que la complejidad descubra predictibilidad no lineal oculta del mercado. Con T = 12 el modelo es un suavizador kernel de rendimientos recientes.
- Regla (repo 06:428): todo ML de timing debe ganar, neto, a la media histórica, al momentum ajustado por volatilidad y a comprar y mantener.

### Calificación automática
**Dentro de tolerancia:** esperado -0.0225, obtenido -0.0225, tolerancia ±0.0005 (|diferencia| = 0).

### Calificación
**Calificador A: 4.0/5.** (a) Los dos R² son correctos (0.20% y 3.11%) y la justificación del benchmark cero es buena, pero no cita el hallazgo de GKX de que la media histórica infla el R² unos 3 pp (−0.25). (b) Completo: deriva 2ρk−k², obtiene −0.0225, prueba E[r̂r]>0 y el Sharpe ρ/√(1+ρ²) invariante a k vía Isserlis, y da k*=ρ con R²max=0.0064. (c) Define bien c y lo que predice la teoría; el diseño es correcto (15 predictores de Welch-Goyal, P≈12,000 RFF, T=12). El resultado queda vago y sin verificar ('Sharpe del orden de 0.4-0.5'), sin la mejora ≈0.47 ni su t (−0.15). (d) El mecanismo de Nagel es correcto, pero su 'dato' es una simulación propia, no evidencia publicada. De Buncic acierta la restricción de intercepto cero, pero no da la cifra clave (Sharpe 0.699 vs 0.485) y añade elementos dudosos ('estandarización', 'casi siempre largo'). Faltó Elmore-Strauss. El veredicto separa bien teoría y empírica. Suma ≈4.2.

**Calificador B: 4.5/5.** (a) 0.75/1. Los dos R² son correctos (0.20% y 3.11%) y justifica bien el benchmark cero. No cita el hallazgo de GKX de que la media histórica infla el R² unos 3 pp, que la rúbrica pide de forma explícita; solo lo muestra con su ejemplo. (b) 1.5/1.5. Deriva 2ρk − k², obtiene −0.0225, usa Isserlis para el Sharpe ρ/√(1+ρ²) invariante a k, y da k* = ρ y R²max = 0.0064. (c) ≈0.85/1. Define c = P/T y predice bien el doble descenso, el R² negativo y el Sharpe creciente con c. El diseño empírico es correcto (15 predictores de Welch-Goyal, RFF hasta 12,000, T = 12). El resultado queda vago y marcado como 'sin verificar' ('Sharpe del orden de 0.4-0.5'), sin la mejora frente a comprar y mantener ni el estadístico t. (d) ≈1.25/1.5. Nagel está correcto, con mecanismo de kernel/recencia y el experimento con reversión (0.5). Buncic solo tiene un mecanismo parcial (sin intercepto) y ningún dato cuantitativo (Sharpe 0.699 frente a 0.485), así que recibe 0.25. El veredicto separa bien teoría de afirmación empírica (0.5). Guo-Huang-Li-Yu (arXiv 2608.23761) sí está en el repo (02:180), así que no es cita inventada. Total ≈4.35, redondeado a 4.5.

|A − B| = 0.5 ≤ 1: promedio 4.25, sin arbitraje.

### Defensa oral
**Repregunta 1.** En (b) usted supone E[r] = 0. Suponga ahora una prima positiva, E[r] = μ > 0, y un pronóstico r̂ = kσf que sigue teniendo media cero. ¿Cómo cambian la expresión de R²oos con benchmark cero y el Sharpe de la estrategia w_t = r̂_t? ¿Sigue siendo el Sharpe independiente de k? Si la independencia respecto de k solo refleja que escalar una posición no altera el Sharpe, ¿qué contenido económico le queda al resultado? ¿Sigue siendo irrelevante k cuando hay límites de apalancamiento o costos de transacción proporcionales a |w_t|? ¿Qué pasa si k < 0?

**Repregunta 2.** Usted dice que la complejidad 'eleva ρ mientras k queda mal calibrada'. Sin embargo, las random Fourier features son funciones deterministas de los mismos ~15 predictores de Welch-Goyal. ¿De dónde sale la información nueva que subiría ρ? Diseñe el experimento decisivo: sustituya esos predictores por ruido AR(1) persistente, independiente de r, y mantenga T = 12 y c ≫ 1. Si el Sharpe del timing se mantiene, ¿qué afirmación de KMZ queda refutada y cuál de sus resultados teóricos sigue intacta? En el caso contrario, ¿cómo afectaría eso a la crítica de Nagel?

**Respuesta del sustentante (completa):**

PREGUNTA 1

Planteamiento: r = μ + σu; f estandarizada; corr(f, u) = ρ; normalidad conjunta; r̂ = kσf; S = μ/σ (Sharpe por periodo del mercado).

R²oos con benchmark cero:
  R²oos = 1 − [σ²+μ² − 2kρσ² + k²σ²] / (σ²+μ²) = (2kρ − k²) / (1 + S²)
- La prima no entra en el numerador, porque E[r·r̂] = kσ²ρ cuando el pronóstico tiene media cero. Sí infla el denominador.
- El máximo sigue en k = ρ (vale ρ²/(1+S²)) y R² > 0 sigue exigiendo 0 < k < 2ρ.
- Con S mensual ≈ 0.12 el factor es 0.986: cuantitativamente no importa.

Sharpe de w_t = r̂_t:

- E[wr] = kσ²ρ.
- Var(wr) = k²σ²[μ² + σ²(1+ρ²)], porque Cov(f, fu) = E[f²u] = 0.
- SR = sign(k)·ρ / √(1 + ρ² + S²).
- Sigue sin depender de |k|, y es algo menor: la posición de media cero tiene una exposición μf a la deriva que añade varianza sin añadir rendimiento.
- Simulación con ρ = 0.1 y S = 0.133:
  - SR = 0.0986 para k = 0.05, 0.1, 0.5 y 2;
  - en esos mismos casos R² = 0.74%, 0.98%, −14.7% y −354%.
- Si el pronóstico tuviera media m ≠ 0 (r̂ = m + kσf), sería en parte beta estático. Entonces el Sharpe depende de m/k, k deja de ser irrelevante y la estrategia se juzga por su alfa contra el mercado.

Contenido económico. La invariancia es trivial (homogeneidad de grado 1), pero deja tres cosas:

- (i) El Sharpe mide discriminación (ρ); el R² mide discriminación y calibración (k). Un R² < 0 no implica valor nulo para quien puede reapalancar.
- (ii) Ese valor solo se cobra si la escala se fija sin mirar el futuro, por ejemplo con vol-targeting sobre la volatilidad pasada de la estrategia.
  - Un inversionista media-varianza que toma r̂ al pie de la letra tiene CE(k) = [kρ − ½k²(1+ρ²+S²)]/γ.
  - Ese CE es negativo si k > 2ρ/(1+ρ²+S²). Es la misma lógica del R².
- (iii) Con varios activos o señales, la escala relativa sí importa: k's mal calibradas y distintas entre activos distorsionan los pesos cruzados y bajan el Sharpe del portafolio. La invariancia es solo de un activo.

Límites de apalancamiento: k ya NO es irrelevante.

- Con |w| ≤ L, la regla es clip(kσf). Con k grande se satura hacia L·sign(f), cuyo Sharpe es ρ√(2/π)/√(1+S²−2ρ²/π): unos 20% menos.
- Simulación: 0.0987 → 0.094 (32% del tiempo en el tope) → 0.083 (84% en el tope).
- Con k chico se conserva el Sharpe, pero L limita la volatilidad y el rendimiento alcanzables.
- Con long-only, k pesa todavía más.

Costos proporcionales a |w_t|:

- El neto w·r − c|w| sigue siendo homogéneo de grado 1 en k, así que el Sharpe neto NO depende de k. Simulación: 0.090 para k = 0.1, 1 y 5.
- El Sharpe neto es menor que el bruto y su signo es sign(ρσ − c√(2/π)). k no rescata una señal cuyo margen por unidad de posición no cubre el costo.
- Lo que sí rompe la invariancia:
  - costos convexos (impacto ∝ w²);
  - costos fijos;
  - un spread de financiamiento por apalancamiento > 1, que mete un quiebre en el costo;
  - requisitos de margen.
- Con costos proporcionales a la rotación |Δw|, la invariancia se mantiene dentro de las reglas lineales, pero la regla lineal deja de ser óptima (aparece una banda de no-operación).

k < 0:

- R² = 2kρ − k² < 0 para cualquier k < 0 si ρ > 0, y SR = −ρ/√(1+ρ²+S²). En la simulación, con k = −0.1: SR = −0.0986 y R² = −2.9%.
- La invariancia es respecto de |k|, no del signo: lo que importa es sign(kρ). Escalar no corrige un signo equivocado, y voltear ex post una estrategia con Sharpe negativo es minería de datos.

PREGUNTA 2

¿De dónde sale la información? Nada nuevo respecto de x_t.

- Las RFF son funciones medibles de x_t con pesos aleatorios independientes de r: σ(RFF_t) ⊆ σ(x_t).
- La cota es la correlación máxima ρ* = corr(r_{t+1}, E[r_{t+1}|x_t]) ≥ ρ_lineal. La complejidad solo acerca el ρ del ajuste a ρ* si E[r|x] es no lineal y hay datos para aprenderla. Con T = 12 y 15 dimensiones no los hay.

El hecho algebraico clave (teorema del representante): la predicción ridge o ridgeless es un suavizador lineal de las etiquetas de entrenamiento.
  r̂_{t+1} = Σ_{s=t−11}^{t} ω_s·r_s, con ω = k(x_t)'(K + zI)⁻¹ y K el kernel (≈ gaussiano cuando c → ∞)
- El pronóstico vive en el espacio de los últimos 12 rendimientos; los predictores solo fijan los pesos.
- Con predictores persistentes, K(x_t, x_s) cae con |t−s|. El resultado es un promedio de rendimientos recientes ponderado por recencia: momentum de serie de tiempo del mercado, más un sesgo largo por la prima.
- Si ρ 'sube', la información nueva son los rendimientos pasados, no el contenido económico de Welch-Goyal. Esa es la crítica de Nagel.

Experimento decisivo:

- Placebo: 15 series AR(1) independientes de r, con φ_j igual a la persistencia estimada de cada predictor WG (≈ 0.9-0.99). Misma estandarización, mismo ancho de banda de las RFF, mismo P (c ≫ 1, p. ej. P = 12,000), mismo z, T = 12, mismas fechas.
- 500-1000 réplicas, para obtener la distribución placebo del Sharpe, del alfa frente al mercado y de la curva Sharpe-vs-c.
- Controles:
  - (a) ruido iid (φ = 0), para aislar el papel de la persistencia;
  - (b) etiquetas permutadas dentro de la ventana;
  - (c) benchmarks explícitos: promedio de 12 meses y promedio exponencial con el mismo perfil de pesos, más una regresión de cobertura de KMZ sobre mercado + TSMOM.
- p-valor = fracción de placebos con Sharpe ≥ el real.

Si el Sharpe se mantiene:

- Queda refutada la afirmación EMPÍRICA de KMZ: que la ganancia de timing viene de extraer la relación (no lineal) entre los predictores y la prima, es decir, que la 'virtud de la complejidad' observada es evidencia de previsibilidad desde los predictores.
- Sigue intacto el resultado TEÓRICO: en su marco (estacionariedad, T, P → ∞ con P/T → c, señal repartida en muchas características, z → 0), el Sharpe esperado fuera de muestra crece con c y puede haber R² < 0 con Sharpe > 0. Son teoremas bajo supuestos. El placebo solo muestra que no explican su evidencia con T = 12, donde la asintótica no aplica.

Caso contrario (el Sharpe real queda sobre el percentil 95 del placebo y tiene alfa significativo sobre TSMOM):

- El mecanismo de 'suavizador por recencia', que el placebo reproduce con la misma persistencia, no basta.
- Los pesos de los predictores reales contendrían información de estado: qué meses pasados se parecen económicamente al presente (pronóstico por análogos). La versión fuerte de la crítica de Nagel, un artefacto mecánico independiente de los predictores, se debilita.
- No desaparece del todo:
  - (1) d/p, e/p, b/m, svar y ntis son funciones de precios y codifican rendimientos o volatilidad pasados. Hay que repetir la prueba solo con tbl, lty, tms, dfy e infl, u ortogonalizar los predictores contra rendimientos y volatilidad pasados.
  - (2) Sigue en pie que con T = 12 la asintótica no sirve de justificación, y queda el riesgo de minería sobre (γ, z, P, T).

**Dictamen del juez: deducción 0.0.** Motivo textual del juez (lo emitió en inglés):

> The derivations check out. R2 = (2k*rho - k^2)/(1+S^2). Var(wr) = k^2 sigma^2 [mu^2 + sigma^2 (1+rho^2)], so SR = sign(k) rho/sqrt(1+rho^2+S^2), which is still invariant to |k|. The saturated leverage case gives rho*sqrt(2/pi)/sqrt(1+S^2-2rho^2/pi), and it follows that k matters under a leverage limit. The defense correctly shows that proportional costs keep degree-1 homogeneity in k, and it names which costs do break the invariance (convex, fixed, financing spread). On k<0 it notes that the invariance holds only for |k|, not the sign. On economic content it separates discrimination from calibration, gives the certainty equivalent for a mean-variance investor, and explains relative scale across several assets. On Q2 it states correctly that the RFF features are measurable in x_t and so carry no new information. It gives the representer theorem (a linear smoother of the last 12 returns, which yields recency-weighted momentum). The placebo design is rigorous, with persistent AR(1) series, iid noise, permuted labels and explicit benchmarks. It correctly separates the refuted empirical claim from the theoretical result that survives, and gives a nuanced reading of the opposite case: some predictors are functions of prices, so orthogonalize them.

**Puntaje final: 4.25/5** (A 4.0, B 4.5; promedio 4.25; deducción de la defensa 0.0).

### Hueco
**Faltó (−0.75 en el promedio de A y B):**

- (a) No citó el hallazgo de GKX de que la media histórica infla el R² de acciones individuales unos 3 pp; solo lo mostró con el ejemplo numérico.
- (c) El resultado empírico de KMZ quedó vago y marcado como "sin verificar" ("Sharpe del orden de 0.4-0.5"). Faltan la mejora de ≈0.47 frente a comprar y mantener, con t ≈ 3, y la muestra CRSP 1926-2020.
- (d) Buncic aparece sin la cifra clave (Sharpe 0.699 de la regresión simple frente a 0.485 del modelo más complejo de KMZ) y con dos elementos sin respaldo ("estandarización", "casi siempre largo"), aunque rotulados como de memoria. No citó a Elmore y Strauss (correlación de 97.5% entre el pronóstico RFF y el promedio móvil de 12 meses). La "evidencia cuantitativa" que da para Nagel es una simulación propia, rotulada como tal, no la cifra publicada.

No se aplicó la penalización por cifras inventadas: no presentó ningún dato como publicado sin marcarlo.

**Defensa oral:** sin deducción. Extendió el resultado a E[r] = μ > 0, a límites de apalancamiento, a costos proporcionales y a k < 0, y diseñó el placebo AR(1) que decidiría entre KMZ y Nagel.

**Base:** el repositorio solo verifica el título de Buncic (20:192) y no guarda las cifras de KMZ ni las de las críticas de 2025.

**Acción:** una ficha de KMZ (diseño y cifras) y otra de Nagel, Buncic y Elmore-Strauss con sus números, en el cap. 02 o en el 20.

---

## S7-03 — Validación cruzada purgada con embargo y CPCV (López de Prado) (calculo)

### Enunciado
Tiene T = 1,000 observaciones diarias indexadas i = 0, …, 999. La etiqueta de la observación i (método de triple barrera) usa precios en el intervalo [i, i+20] (horizonte h = 20). Usa k-fold purgado con 5 bloques contiguos de 200 observaciones y analiza el bloque de prueba i = 400, …, 599. Reglas: (1) Purga: eliminar del entrenamiento toda observación cuyo intervalo de etiqueta [i, i+20] intersecte la unión de los intervalos de etiqueta del bloque de prueba. (2) Embargo: además, eliminar las E = 0.01T observaciones inmediatamente posteriores a la última observación purgada a la derecha del bloque de prueba (convención del código PurgedKFold de López de Prado, que reinicia el entrenamiento después del máximo t1 del bloque de prueba más el embargo).

(a) ¿Cuántas observaciones se purgan antes y después del bloque de prueba, cuántas se embargan y cuál es el tamaño final del conjunto de entrenamiento? RESULTADO NUMÉRICO PRINCIPAL: tamaño final del entrenamiento.

(b) Si el embargo se definiera en cambio como las 10 observaciones inmediatamente posteriores al final del bloque de prueba (600–609), ¿cuál sería el tamaño del entrenamiento? ¿Por qué?

(c) Explique qué fuga evita la purga y cuál el embargo; por qué k-fold estándar con barajado sobreestima el desempeño en finanzas; y por qué Gu-Kelly-Xiu (2020) evitaron la validación cruzada.

(d) En validación cruzada combinatoria purgada (CPCV) con N = 10 grupos y k = 2 grupos de prueba por partición, ¿cuántas particiones y cuántas trayectorias de backtest se generan? Derive la fórmula de trayectorias.

### Clave (texto descifrado, idéntico al de `clave.json`)
(a) Unión de intervalos de etiqueta de prueba: [400, 619]. Antes: se purga i si i + 20 ≥ 400 ⇒ i = 380…399: 20 observaciones. Después: se purga i si i ≤ 619 ⇒ i = 600…619: 20 observaciones. Embargo: i = 620…629: 10 observaciones. Entrenamiento = 1000 − 200 (prueba) − 20 − 20 − 10 = 750 (izquierda 0–379: 380; derecha 630–999: 370). K-fold ingenuo usaría 800.

(b) 760: las observaciones 600–609 ya fueron eliminadas por la purga (600–619), así que un embargo contado desde el fin del bloque de prueba queda subsumido cuando E ≤ h; 1000 − 200 − 40 = 760.

(c) Purga: elimina observaciones de entrenamiento cuyas etiquetas se forman con información que se traslapa temporalmente con las etiquetas de prueba (etiquetas traslapadas ⇒ el modelo 've' parte del resultado de prueba). Embargo: protege contra correlación serial de características/efectos rezagados después del bloque de prueba (p. ej., características tipo ARMA o reacción tardía), solo es necesario después del bloque de prueba. K-fold con barajado: observaciones adyacentes casi idénticas (etiquetas traslapadas, no i.i.d.) quedan en entrenamiento y prueba ⇒ memorización y R²/Sharpe inflados; además la selección repetida de hiperparámetros sobreajusta el backtest. GKX usan una muestra de validación posterior al entrenamiento y prueba posterior a ambas, 'para mantener el orden temporal de los datos'.

(d) Particiones = C(10,2) = 45. Cada grupo aparece como prueba en C(N−1, k−1) particiones, por lo que el número de trayectorias completas es φ[N,k] = (k/N)·C(N,k) = C(N−1,k−1) = 9. (Ej. clásico: N = 6, k = 2 ⇒ 15 particiones y 5 trayectorias.) CPCV da una distribución de Sharpe por trayectoria, útil para probabilidad de sobreajuste de backtest y Sharpe deflactado.

**Valor numérico principal comprometido:** 750 ± 0.5.

**Rúbrica:** 5 puntos. (a) 2 pts: purga 20 antes y 20 después (1.0); embargo 10 y total 750 (1.0; tolerancia ±0.5 en el conteo final). (b) 0.5 pts: 760 con explicación de subsunción. (c) 1.5 pts: purga (0.5), embargo (0.5), falla de k-fold barajado y razón de GKX (0.5). (d) 1 pt: 45 particiones (0.25), 9 trayectorias (0.25), derivación φ = (k/N)C(N,k) = C(N−1,k−1) (0.5).

### Fuente
López de Prado, M. (2018), Advances in Financial Machine Learning, Wiley, cap. 7 (purged k-fold, embargo, snippet PurgedKFold) y cap. 12 (CPCV, φ[N,k] = (k/N)·C(N,k)); Gu, Kelly, Xiu (2020, RFS) nota 32; documentación skfolio CombinatorialPurgedCV. Conteos verificados con python3.

### Respuesta del sustentante (completa)
(a) Cálculo en código propio sobre los índices 0..999:

- Las etiquetas del bloque de prueba (400-599) cubren [400, 619].
- Se purga toda i fuera de prueba con i+20 ≥ 400 e i ≤ 619:
  - antes del bloque: i = 380..399, 20 observaciones;
  - después del bloque: i = 600..619, 20 observaciones.
- Embargo: E = 0.01·1000 = 10 observaciones después de la última purgada, i = 620..629.
- Entrenamiento = 1000 − 200 − 20 − 20 − 10 = 750, formado por i = 0..379 y 630..999. RESULTADO PRINCIPAL: 750.

Inferencia sobre el código: aplicado de forma literal, el snippet PurgedKFold de AFML (conserva t1 ≤ t0 a la izquierda y reanuda en maxT1Idx + embargo) da 752. Conserva i = 380 (su etiqueta toca 400 solo en un punto) y reanuda en 629. Con la regla de intersección cerrada del enunciado, el tamaño es 750.

(b) Si el embargo es 600-609, esas observaciones ya estaban purgadas (600-619). El embargo no quita nada nuevo y el entrenamiento queda en 1000 − 200 − 40 = 760. Como h = 20 > E = 10, la purga ya cubre esa franja. Un embargo medido desde el fin del bloque no protege de la dependencia serial más allá del traslape de etiquetas. Por eso López de Prado lo mide desde el máximo t1.

(c) Qué fuga evita cada regla:

- Purga: la etiqueta de una observación de entrenamiento no debe usar precios del periodo de prueba. Si lo hace, el modelo aprende el resultado de la prueba. Aquí la etiqueta de i = 395 usa precios de 395 a 415.
- Embargo: después de la prueba, las features (ventanas de rezagos, volatilidad, memoria larga) siguen correlacionadas con las etiquetas de prueba. Eliminar un colchón corta esa fuga, que es más difícil de ver.

Por qué el k-fold barajado sobreestima: las observaciones no son IID. Con h = 20, las etiquetas de i e i+1 comparten 19 de 20 días. Al barajar, casi todo punto de prueba tiene un 'gemelo' en entrenamiento y los modelos flexibles (RF, GBRT) lo memorizan. A eso se suman la selección entre muchas variantes y la no estacionariedad (repo 19:190; DSR y PBO en laboratorio/README.md).

GKX (2020) evitaron la validación cruzada por esas razones. Conservaron el orden temporal con entrenamiento, luego validación y luego prueba, reestimando año con año (ver S7-01d).

(d) CPCV con N = 10 y k = 2:

- Particiones = C(10, 2) = 45.
- Trayectorias φ = (k/N)·C(N, k) = C(N−1, k−1) = 9.

Derivación: las 45 particiones suman k·C(N, k) = 90 bloques de prueba. Cada trayectoria necesita los N = 10 grupos una vez cada uno, así que φ = 90/10 = 9. De otro modo: cada grupo aparece en C(N−1, k−1) = 9 particiones. Cada partición entrena con N − k = 8 grupos, menos la purga y el embargo.

### Calificación automática
**Dentro de tolerancia:** esperado 750, obtenido 750, tolerancia ±0.5 (|diferencia| = 0).

### Calificación
**Calificador A: 5.0/5.** (a) Correcto: purga 20 antes (380-399) y 20 después (600-619), embargo 10 (620-629) y entrenamiento de 750. Añade una observación correcta y valiosa: el snippet literal de PurgedKFold (t1 ≤ t0 a la izquierda, reanuda en maxT1Idx+embargo) da 752; lo verifiqué contra el código de AFML. (b) 760, con la explicación de subsunción (h=20 > E=10). (c) Explica purga, embargo, la falla del k-fold barajado (etiquetas que comparten 19 de 20 días) y la razón de GKX. (d) 45 particiones y 9 trayectorias, con una derivación correcta por conteo de bloques de prueba. Todo completo.

**Calificador B: 5.0/5.** (a) 2/2. Purga 20 antes (380-399) y 20 después (600-619), embargo 620-629 y entrenamiento de 750. La observación de que el snippet literal de AFML da 752 es correcta: conserva i = 380 porque t1 ≤ t0, y reanuda en maxT1Idx + 10 = 629. (b) 0.5/0.5. Llega a 760 y explica bien por qué la purga ya cubre esa franja. (c) 1.5/1.5. Distingue purga de embargo, explica la falla del k-fold barajado (etiquetas que comparten 19 de 20 días, memorización) y da la razón temporal de GKX. (d) 1/1. 45 particiones y 9 trayectorias, con una derivación por conteo de bloques (90/10) y por C(N−1,k−1).

|A − B| = 0 ≤ 1: promedio 5.0, sin arbitraje.

### Defensa oral
**Repregunta 1.** ¿Por qué el embargo se aplica solo a la derecha del bloque de prueba y no a la izquierda? ¿Qué distingue a la fuga que queda del lado izquierdo, que ya cubre la purga, de la que queda del lado derecho? Rehaga el conteo del entrenamiento para el primer bloque (0-199) y para el último (800-999). Ahora suponga que las etiquetas de triple barrera terminan al tocar una barrera, de modo que t1_i ≤ i+20 y varía por observación. ¿Su 750 pasa a ser una cota inferior, una cota superior o sigue siendo exacto? ¿Qué dato necesitaría para purgar bien en ese caso?

**Repregunta 2.** En CPCV con N = 10 y k = 2 obtiene 9 trayectorias. ¿Son estadísticamente independientes? Tome en cuenta que comparten datos de entrenamiento y que cada grupo de prueba aparece en varias particiones. ¿Qué implica esa dependencia si usted usa la dispersión de los Sharpe entre trayectorias como medida de incertidumbre o como insumo para el PBO? Si subiera k a 5 con N = 10, ¿cuántas particiones y trayectorias habría y cuánto entrenamiento efectivo le quedaría a cada modelo después de la purga y el embargo? ¿Qué intercambio entre sesgo y varianza está haciendo con esa elección?

**Respuesta del sustentante (completa):**

Supuestos: T = 1000; 5 bloques de 200; t1_i = i + 20; embargo de 10 observaciones (1% de T). El 750 sale de 800 − 20 (purga izquierda) − 20 (purga derecha) − 10 (embargo).

PREGUNTA 1

¿Por qué solo a la derecha? Por la flecha del tiempo.

Lado izquierdo:

- Después de la purga, todo lo que queda a la izquierda (rasgos y etiquetas) está fechado antes de s, el inicio de la prueba. Es exactamente la información que tendría un pronosticador en tiempo real en s.
- Que los rasgos de prueba compartan ventanas de rezago con etiquetas previas no es fuga: es pasado compartido, disponible en s.
- La fuga de la izquierda es de un solo tipo: la etiqueta de entrenamiento contiene rendimientos del periodo de prueba. La purga, que quita las i con [i, t1_i] traslapado con la prueba, la elimina por completo.

Lado derecho:

- Aunque se purgue el traslape de etiquetas (i ≥ e + 21), los rasgos de esas observaciones se calculan con ventanas de rezago que cubren el bloque de prueba. Por ejemplo, la volatilidad de 60 días en e + 30 contiene 30 días de prueba.
- Por la correlación serial de rasgos y etiquetas, esas observaciones son parientes cercanas del régimen de prueba. Entrenar con ellas es usar información POSTERIOR a las predicciones: look-ahead.
- La purga, que solo mira etiquetas, no lo detecta. Por eso se necesita el embargo, de tamaño ≈ máx(rezago de los rasgos, horizonte de dependencia serial).
- Por la misma razón walk-forward, que no tiene lado derecho, necesita purga pero no embargo.
- Matiz: si en producción los datos llegan con d días de retraso, también hace falta un hueco de d días a la izquierda. Eso es realismo operativo, no fuga.

Conteo (verificado con un script):

- Bloque 0-199: no hay lado izquierdo. Bruto 200-999 = 800; purga 200-219 (i ≤ t1_199 = 219): −20; embargo 220-229: −10. Total: 770.
- Bloques interiores: 750.
- Bloque 800-999: bruto 0-799 = 800; purga 780-799: −20; no hay embargo porque no hay entrenamiento a la derecha. Total: 780.
- Promedio de los cinco bloques: 760.
- Ojo: las etiquetas de 980-999 necesitan precios hasta 1019. Si la muestra termina en 999, esas etiquetas se truncan o se excluyen.

Triple barrera (t1_i ≤ i + 20, variable): 750 pasa a ser una COTA INFERIOR, siempre que se purgue con t1 exacto.

- Izquierda: solo se purgan las i ∈ [s−20, s−1] con t1_i ≥ s, que son un subconjunto.
- Derecha: solo las i ≤ máx_{j∈prueba} t1_j ≤ e + 20.
- Embargo: 10 observaciones después de ese máximo.
- Hay igualdad solo si todas las observaciones afectadas terminan en la barrera vertical.
- Simulación con duraciones uniformes de 1 a 20: 760-767 en los bloques interiores, 773 en el primero y 790 en el último.
- Si se sigue purgando con el horizonte máximo, el conteo queda en 750: es válido pero conservador y desperdicia datos.
- Dato necesario: el vector t1 (fecha del primer toque de barrera) de cada evento, tanto de entrenamiento como de prueba (el t1 de López de Prado). Para el embargo, además, el rezago máximo de los rasgos.

PREGUNTA 2

CPCV con N = 10 y k = 2: C(10,2) = 45 particiones; cada grupo aparece en prueba C(9,1) = 9 veces; φ = (k/N)·C(N,k) = 9 trayectorias. NO son independientes, por tres razones:

- (1) Mismos datos de prueba. Cada trayectoria recorre los 10 grupos, es decir, los mismos 1000 rendimientos realizados; solo cambia el modelo que predice.
  - La dispersión entre trayectorias mide la varianza del MODELO condicional a una sola historia. Omite la varianza de muestreo de la historia, que es la relevante para inferencia.
  - Caso extremo: una regla determinista (siempre largo) da 9 Sharpes idénticos, con dispersión cero, aunque su EE real sea ≈ 1/√años.
- (2) Entrenamientos traslapados. Dos particiones cualesquiera comparten al menos 6 de 8 grupos (7 de 8 si comparten un grupo de prueba). Los modelos son casi iguales y sus predicciones están muy correlacionadas.
- (3) Asignación arbitraria. Cuál de las 9 predicciones de un grupo va a cuál trayectoria es una convención; otra asignación cambia la dispersión sin añadir información.

Implicaciones:

- Usar sd/√9 como EE subestima dos veces: la sd es chica por construcción y √9 supone independencia.
- La corrección de Nadeau-Bengio, Var ≈ (1/J + n_test/n_train)σ², da 0.361 frente a 0.111, es decir, EE ×1.8. Aun así no captura la varianza de la historia.
- En el PBO, la fracción de combinaciones con logit ≤ 0 no es una proporción binomial de ensayos independientes. Es un diagnóstico de robustez frente a perturbaciones del entrenamiento, no una probabilidad con EE conocido.
- Si se usa la dispersión entre trayectorias como V[SR] en el Deflated Sharpe, V queda subestimada, SR0 queda bajo y el DSR sale inflado.
- Remedios:
  - bootstrap estacionario por bloques de la historia, reejecutando la CPCV;
  - EE HAC del Sharpe agregado;
  - reportar la dispersión entre trayectorias solo como medida de estabilidad.

Con k = 5 y N = 10 (grupos de 100):

- C(10,5) = 252 particiones; φ = (5/10)·252 = C(9,4) = 126 trayectorias.
- Entrenamiento bruto: 500 (50%). Después de purgar 20 a la izquierda de cada racha de prueba y purgar más embargar 30 a su derecha:
  - mínimo 270, con prueba {1,3,5,7,9} (cinco rachas);
  - máximo 480, con prueba {5,…,9};
  - media 375, es decir, 37.5% de la muestra.
- Con k = 2 los valores son 700 / 720 / 780 (media 72%). Purga y embargo se comen 25% del bruto con k = 5 y 10% con k = 2, porque hay más fronteras.

Intercambio entre sesgo y varianza:

- Lo que gana k grande:
  - más trayectorias;
  - modelos más diversos: dos particiones comparten en promedio 2.5 de 5 grupos;
  - menor varianza del promedio frente a perturbaciones del entrenamiento;
  - una distribución más completa para el PBO.
- Lo que cuesta:
  - SESGO pesimista por la curva de aprendizaje: se evalúa un modelo entrenado con 37.5% de los datos, no el que se desplegará con 100%. El sesgo es mayor en modelos complejos, así que la selección se inclina artificialmente hacia modelos simples;
  - más dispersión porque los modelos son peores y más inestables, lo que se leería como más incertidumbre o más PBO;
  - entrenamientos fragmentados que pueden dejar fuera regímenes enteros.
- Lo que no mejora: 126 trayectorias correlacionadas no son 126 historias; la incertidumbre de tener una sola muestra de 1000 observaciones sigue igual.
- k = 2 da menos sesgo y más varianza. Con series cortas prefiero k pequeño, complementado con bootstrap por bloques.

**Dictamen del juez: deducción 0.0.** Motivo textual del juez (lo emitió en inglés):

> It explains the asymmetry correctly. On the left, after purging, everything is information available at time s. On the right, features with lookback windows and serial correlation bring in test-period information that the label-based purge does not catch, which is why walk-forward needs purging but not an embargo. The counts are right: 770 (first block), 750 (interior blocks), 780 (last block), average 760. With a variable triple barrier, it correctly identifies 750 as a lower bound when purging with the exact t1, and names the vector t1 as the data needed. On CPCV it gives three sound reasons for dependence: the same test history, training sets that share 6-7 of 8 groups, and arbitrary assignment. It draws the implications for the standard error (Nadeau-Bengio 0.361 vs 0.111, correct), for the PBO and for the DSR. For k=5: 252 partitions and 126 paths are correct, and min 270 / max 480 / mean 375 are correct (the expected number of boundaries is 2.5). There is a small inconsistency in how the groups are indexed ({1,3,5,7,9} is 1-based, {5,...,9} is 0-based), but the figures are right. The bias-variance tradeoff via the learning curve is well argued.

**Puntaje final: 5.0/5** (A 5.0, B 5.0; promedio 5.0; deducción de la defensa 0.0).

### Hueco
Ninguno. Además hizo una observación que la clave no tenía: el snippet literal de PurgedKFold de AFML da 752, porque conserva i = 380 (t1 ≤ t0) y reanuda en 629. Los dos calificadores la verificaron.

**Defensa oral:** sin deducción. Explicó por qué el embargo solo va a la derecha, dio los conteos por bloque (770/750/780, promedio 760) y la cota inferior con triple barrera, y mostró la dependencia entre trayectorias de CPCV (EE de Nadeau-Bengio).

**Detalle sin costo:** en el caso k = 5 mezcla la indexación base 1 ({1,3,5,7,9}) con la base 0 ({5,…,9}). Las cifras son correctas.

---

## S7-04 — Fuga de información, sesgo de anticipación y memorización en LLMs usados para predecir retornos (caso)

### Enunciado
Un equipo cuantitativo usa un LLM de frontera (corte de conocimiento declarado: diciembre de 2024) para puntuar titulares de noticias por empresa y formar un portafolio long-short diario. Backtest 2016–2024: Sharpe anual 4.1. Periodo enero 2025–junio 2026: Sharpe 0.8. Para 'corregir' el sesgo, el equipo propone (i) añadir al prompt 'actúa como si hoy fuera la fecha del titular y no uses información posterior' y (ii) reemplazar el nombre de la empresa por 'Empresa X'.

(a) Identifique al menos cuatro canales distintos de fuga o memorización y cómo inflarían el Sharpe previo al corte.

(b) Evalúe con evidencia publicada si las dos correcciones propuestas funcionan.

(c) Diseñe un protocolo de evaluación que permita una conclusión creíble (mínimo cinco elementos concretos, incluyendo al menos una prueba estadística específica).

(d) ¿La caída de 4.1 a 0.8 prueba memorización? Discuta la identificación, la incertidumbre muestral del Sharpe post-corte y qué evidencia adicional distinguiría memorización de cambio de régimen o decaimiento de la señal.

### Clave (texto descifrado, idéntico al de `clave.json`)
(a) Canales: 1) Sesgo de anticipación por preentrenamiento: el corpus contiene texto posterior al titular (reacción del mercado, desenlace del evento), el modelo 'sabe' qué pasó. 2) Memorización literal de datos numéricos: los LLMs recuerdan valores exactos de variables económicas, retornos e índices anteriores a su corte (Lopez-Lira, Tang y Zhu 2025). 3) Conocimiento de la entidad/sobrevivencia: sabe qué empresas ganaron o quebraron; efecto 'distracción' del conocimiento general sobre la empresa (Glasserman y Lin 2023). 4) Corte difuso: entrenamiento continuado, fine-tuning/RLHF o actualizaciones de versión de API con datos posteriores; herramientas de búsqueda/retrieval. 5) Fuga clásica del backtest: selección de prompts/hiperparámetros con toda la muestra (snooping), sellos de tiempo de titulares revisados en vez de primera publicación, universo no point-in-time. Todos elevan la precisión dentro de muestra sin capacidad predictiva real.

(b) (i) Instrucciones de respetar la fecha: Lopez-Lira, Tang y Zhu (2025) muestran que no impiden precisión de nivel 'recuerdo'; Sarkar y Vafa (2024; ICML 2025) documentan sesgo de anticipación con pruebas directas y señalan los límites de las soluciones por prompt, recomendando modelos preentrenados solo con texto previo al periodo. (ii) Anonimizar: Lopez-Lira, Tang y Zhu hallan que el enmascaramiento falla porque el LLM reconstruye entidad y fecha con poco contexto; Glasserman y Lin (2023) encuentran que los titulares anonimizados rinden más dentro de muestra (el efecto distracción pesa más que el sesgo de anticipación), útil para depurar pero no garantiza eliminar la fuga. Conclusión: ninguna corrección es suficiente.

(c) Protocolo: 1) evaluación verdaderamente fuera de muestra solo después del corte y de cualquier fine-tuning, con versión de modelo y prompt congelados (hash) y pre-registro; 2) modelos cronológicamente consistentes (ChronoBERT/ChronoGPT, He, Lv, Manela y Wu 2025) o reentrenados point-in-time para el periodo previo (ellos hallan sesgo modesto en su aplicación de noticias → la magnitud es empírica); 3) prueba de 'Lookahead Propensity' (Gao, Jiang y Yan 2025): regresión de precisión sobre pronóstico × LAP; interacción positiva indica contaminación; LAP colapsa tras el corte; 4) sondas de memorización: pedir retornos/fechas dada solo empresa+fecha; placebo con eventos impredecibles (Sarkar-Vafa); 5) sellos de primera publicación, ejecución en la siguiente apertura, costos, universo point-in-time; 6) cualquier ajuste con validación purgada/embargada; 7) estadística: prueba de diferencia de Sharpe (Jobson-Korkie/Memmel o bootstrap por bloques) pre vs post, Sharpe deflactado por el número de prompts probados, comparación con benchmarks de sentimiento entrenados antes del periodo (diccionario/FinBERT); 8) heterogeneidad: desempeño más alto en empresas grandes/muy cubiertas es síntoma de fuga.

(d) No lo prueba por sí sola. El Sharpe post-corte tiene error estándar ≈ √((1 + SR²/2)/años) = √((1+0.32)/1.5) ≈ 0.94, así que 0.8 es poco preciso (aunque 4.1 queda muy lejos). La caída también es compatible con cambio de régimen, saturación de la señal o decaimiento post-publicación (McLean-Pontiff). Identificación: diferencias en diferencias alrededor del corte comparando el LLM con un modelo cronológicamente consistente en los mismos periodos (si el modelo crono es estable y el LLM cae, hay fuga); interacción con LAP en la muestra previa y su desaparición posterior; sondas de memorización positivas antes del corte y nulas después.

**Valor numérico principal comprometido:** no aplica.

**Rúbrica:** 5 puntos. (a) 1.5 pts: ≥4 canales distintos bien explicados (0.375 c/u). (b) 1 pt: evaluación de instrucción temporal (0.5) y anonimización (0.5) con evidencia correcta (Lopez-Lira-Tang-Zhu; Glasserman-Lin; Sarkar-Vafa). (c) 1.5 pts: ≥5 elementos concretos (1.0) incluyendo una prueba estadística específica y un modelo o prueba de consistencia cronológica/LAP (0.5). (d) 1 pt: reconoce que no identifica por sí sola (0.25), cuantifica la incertidumbre del Sharpe (0.25), propone diseño de identificación tipo diferencias en diferencias/LAP (0.5).

### Fuente
Lopez-Lira, A., Tang, Y., Zhu, M. (2025), 'The Memorization Problem: Can We Trust LLMs' Economic Forecasts?', arXiv 2504.14765 / SSRN 5217505; Glasserman, P., Lin, C. (2023), 'Assessing Look-Ahead Bias in Stock Return Predictions Generated by GPT Sentiment Analysis', arXiv 2309.17322; Sarkar, S., Vafa, K. (2024), 'Lookahead Bias in Pretrained Language Models', SSRN 4754678 (ICML 2025); He, S., Lv, L., Manela, A., Wu, J. (2025), 'Chronologically Consistent Large Language Models', arXiv 2502.21206; Gao, Z., Jiang, W., Yan, Y. (2025), 'Detecting Lookahead Bias in LLM Forecasts', arXiv 2512.23847; Lopez-Lira, A., Tang, Y. (2023), 'Can ChatGPT Forecast Stock Price Movements?', arXiv 2304.07619.

### Respuesta del sustentante (completa)
(a) Canales de fuga o memorización que inflan el Sharpe de 2016-2024:

1) Memoria del desenlace: el LLM 'sabe' cómo reaccionó el precio o qué pasó después (fusión, resultados, quiebra). Su puntaje se correlaciona con el rendimiento realizado, no con el texto.
2) Retrospectiva por empresa: sabe qué firmas ganaron o perdieron en la década (p. ej., NVDA frente a SVB) y sesga el sentimiento hacia los futuros ganadores.
3) Retrospectiva macro o de régimen: conoce el crash y rebote de COVID y el ciclo de tasas de 2022. Eso inclina las exposiciones sectoriales o netas.
4) Contaminación del corpus: artículos que traen el titular junto con la reacción ('las acciones cayeron 12% tras…'), titulares reescritos después y marcas de tiempo del proveedor revisadas.
5) Look-ahead del investigador: elegir prompt, modelo, universo y umbral sobre 2016-2024 (pruebas múltiples); además, el corte 'declarado' puede ser impreciso y las versiones de la API cambian.
6) Look-ahead de ejecución: operar al cierre del día del titular o antes de su hora real, y un universo con sesgo de supervivencia.

(b) Las dos correcciones no funcionan:

- (i) 'Actúa como si fuera la fecha…': Lopez-Lira, Tang y Zhu (2025, arXiv 2504.14765) muestran que pedirle al modelo que no use el futuro no lo evita, porque el modelo no puede 'desaprender' (03:258; 25:104).
- (ii) 'Empresa X': los mismos autores muestran que enmascarar no basta. El modelo reconstruye la entidad y la fecha con muy poco contexto (productos, montos, directivos). Además, el anonimato no toca los canales 3-6.
- Gao, Jiang y Yan (2025, arXiv 2512.23847; repo 26:140): la 'propensión de anticipación' colapsa a cero después del corte, y con ella la ventaja de precisión.
- De memoria, no está en el repo: Glasserman y Lin (2023) encuentran que anonimizar cambia el desempeño dentro de muestra por un 'efecto distracción', pero no identifica el efecto fuera de muestra. La alternativa seria son LLM cronológicamente consistentes, entrenados solo hasta cada fecha (p. ej., He-Lv-Manela-Wu 2025, también de memoria).
- Regla del sistema: ningún backtest de LLM previo a su corte cuenta como evidencia (03:366, 424).

(c) Protocolo:

1) Prerregistro con hash del prompt, ID y versión congelada del modelo, universo, regla de portafolio y modelo de costos, antes de ver datos posteriores al corte.
2) Prueba verdaderamente fuera de muestra: solo titulares posteriores a la fecha de lanzamiento del modelo (no solo al corte declarado), más forward-testing en papel con marcas de tiempo.
3) Diseño de cortes escalonados: varios modelos de pesos abiertos con cortes conocidos, cada uno evaluado solo después de su corte. Se busca una discontinuidad del desempeño justo en cada corte.
4) Sondas de memorización: pedir el rendimiento del día siguiente, la fecha y la empresa para titulares enmascarados. Después, un DiD de P&L entre titulares con recuerdo alto y bajo.
5) Placebos: fechas o empresas barajadas y titulares contrafactuales con el sentimiento invertido. El puntaje debe responder al texto, no al desenlace.
6) Bases de comparación sin memoria: diccionario Loughran-McDonald o FinBERT entrenado antes de 2016, más una regresión sobre FF5 + momentum + reversión de corto plazo con errores HAC.
7) Pruebas estadísticas: Ledoit-Wolf (2008) con bootstrap HAC para la diferencia de Sharpe antes y después y contra la base; Chow o Andrews (quiebre) en la fecha de corte; Deflated Sharpe con N = número de prompts y variantes (repo 19:334); Diebold-Mariano sobre las pérdidas de pronóstico.
8) Ejecución realista: siguiente precio disponible después de la marca de tiempo, spreads de acciones pequeñas y capacidad.

(d) La caída no prueba memorización. Cálculo propio con la fórmula de Lo (2002), suponiendo rendimientos iid y normales:

- Post-corte: SR = 0.8 en 1.5 años (≈378 días), EE ≈ 0.82, IC95 ≈ [−0.80, 2.40], t ≈ 0.98. No se rechaza SR = 0 ni SR = 2.4. Para t = 1.96 con SR 0.8 harían falta ≈6 años.
- Pre-corte: SR = 4.1 en 9 años, EE ≈ 0.34. La diferencia da z ≈ 3.7, pero ignora colas, autocorrelación y, sobre todo, que el 4.1 fue seleccionado dentro de muestra.

Explicaciones rivales:

- Decaimiento por adopción: los rendimientos de señales LLM de titulares caen al subir la adopción (Lopez-Lira-Tang, v6 oct-2025; 26:138).
- Recorte normal fuera de muestra: sobrevive ~50% según Chen-Lopez-Lira-Zimmermann (02:182), y hay −26% fuera de muestra según McLean-Pontiff (19:46).
- Cambio de régimen y sobreajuste del prompt.

Evidencia que distinguiría memorización: (i) una caída discreta justo en el corte, que se repite con modelos de cortes distintos (el decaimiento sería gradual y por calendario, no por modelo); (ii) un P&L previo concentrado en titulares de alto recuerdo; (iii) bases sin LLM que no caen en 2025-26, lo que descarta el régimen; (iv) placebos que 'predicen' antes del corte.

### Calificación automática
**No aplica:** es una pregunta de caso, sin resultado numérico.

### Calificación
**Calificador A: 5.0/5.** (a) Seis canales distintos y bien explicados: desenlace, retrospectiva por empresa, régimen macro, contaminación del corpus y marcas de tiempo, snooping del investigador con corte difuso, y look-ahead de ejecución o supervivencia. (b) Evalúa la instrucción temporal y la anonimización con Lopez-Lira-Tang-Zhu (correcto) y añade Gao-Jiang-Yan (LAP) y Glasserman-Lin (señalado como de memoria, correcto pero vago). Sarkar-Vafa no aparece, pero no es obligatorio. (c) Ocho elementos concretos: prerregistro con hash, prueba verdaderamente fuera de muestra, cortes escalonados (consistencia cronológica), sondas de memorización, placebos, benchmarks sin memoria y pruebas estadísticas (Ledoit-Wolf, Chow/Andrews, DSR, Diebold-Mariano), además de ejecución realista. (d) Reconoce que la caída no identifica memorización. Cuantifica el EE con Lo a frecuencia diaria (0.82); es válido y difiere del 0.94 de la clave solo por la frecuencia de cálculo. Propone identificar con discontinuidad en cortes de varios modelos, contrastes de alto frente a bajo recuerdo, bases sin LLM (tipo DiD) y placebos. Cita correctamente a McLean-Pontiff (−26%).

**Calificador B: 5.0/5.** (a) 1.5/1.5. Da seis canales distintos y bien explicados: desenlace, retrospectiva por empresa, régimen macro, contaminación del corpus y timestamps, snooping con corte difuso y look-ahead de ejecución con supervivencia. (b) 1/1. Evalúa la instrucción temporal y el enmascaramiento con Lopez-Lira-Tang-Zhu 2025 (correcto) y Glasserman-Lin (efecto distracción, correcto), y añade LAP de Gao-Jiang-Yan. (c) 1.5/1.5. Ocho elementos concretos: prerregistro con hash, cortes escalonados (prueba de consistencia cronológica), sondas, placebos, líneas base anteriores al periodo, y pruebas específicas (Ledoit-Wolf HAC, Chow/Andrews, DSR, Diebold-Mariano). (d) 1/1. Dice que la caída no identifica memorización por sí sola. Cuantifica bien la incertidumbre con Lo 2002: EE ≈ 0.82, IC [−0.8, 2.4], z ≈ 3.7; lo verifiqué. Propone una identificación tipo DiD con discontinuidad en cortes de varios modelos, P&L según nivel de recuerdo y líneas base sin LLM. Las referencias de apoyo (McLean-Pontiff −26%, Chen-Lopez-Lira-Zimmermann) son reales.

|A − B| = 0 ≤ 1: promedio 5.0, sin arbitraje.

### Defensa oral
**Repregunta 1.** Su argumento de identificación se apoya en una discontinuidad del desempeño en la fecha de corte de cada modelo. Suponga que los modelos disponibles tienen cortes entre 2023 y 2025, y que en esos mismos años se acelera la adopción de señales LLM, lo que produce un decaimiento por calendario. ¿Cómo separa el efecto del corte del efecto del calendario? Explique qué variación le da identificación: por ejemplo, el mismo titular, en la misma fecha, puntuado por modelos con cortes distintos. Diga también qué supuesto de exclusión necesita, dado que modelos de distinta generación también difieren en capacidad y no solo en corte.

**Repregunta 2.** Usted calcula un EE ≈ 0.82 para el Sharpe posterior al corte con la fórmula de Lo bajo iid y normalidad. Suponga que los rendimientos diarios del long-short tienen autocorrelación positiva y curtosis cercana a 10. ¿El EE sube o baja? ¿Cambia su conclusión de que no se rechaza ni SR = 0 ni SR = 2.4? Su z ≈ 3.7 compara contra un 4.1 elegido dentro de muestra. ¿Cómo aplicaría el Deflated Sharpe si el equipo no documentó cuántos prompts, modelos y umbrales probó? ¿Qué haría con el número de ensayos N y con la correlación entre esas variantes?

**Respuesta del sustentante (completa):**

PREGUNTA 1: separar el efecto del corte del efecto del calendario

Variación que identifica: un panel titular h (con fecha t_h) × modelo m (con corte c_m). El resultado y_{h,m} es el score estandarizado por fecha × el rendimiento siguiente, o el long-short por fecha y modelo.
  y_{h,m} = α_h + γ_m + β·1[t_h ≤ c_m] + ε
- α_h (efecto fijo de titular o de fecha) absorbe todo lo que es común a los modelos ese día: decaimiento por calendario, adopción de señales LLM, régimen de mercado y dificultad del titular.
- γ_m absorbe la capacidad constante de cada modelo.
- β se identifica SOLO con titulares fechados entre cortes: el mismo titular, el mismo día, está dentro del entrenamiento del modelo con corte posterior y fuera del de corte anterior.

En forma DiD, con c_A < c_B, se sigue la brecha B − A en tres tramos: antes de c_A (ambos dentro), entre c_A y c_B (solo B dentro) y después de c_B (ambos fuera).

- La memorización predice que la brecha se abre en [c_A, c_B] y vuelve a su nivel base después de c_B.
- El calendario se cancela en la diferencia.

Con tres o más cortes escalonados:

- event-study en tiempo relativo al corte, con efectos fijos de titular;
- estimadores Sun-Abraham, Callaway-Sant'Anna o DiD apilado, porque TWFE está sesgado con adopción escalonada y efectos heterogéneos;
- placebos con cortes falsos.

El corte efectivo es difuso: la densidad de datos cae antes del corte y hay datos de post-entrenamiento. Conviene estimarlo con pruebas de recuerdo mes a mes y usar un RD 'donut'.

Complementos:

- un benchmark sin corte (Loughran-McDonald, o un modelo congelado anterior a 2019) para medir el decaimiento puro por calendario, con un DiD LLM − benchmark alrededor del corte;
- anonimizar empresa y fecha: la memorización se cae con la máscara antes del corte, no después.

Supuesto de exclusión: condicional a α_h y γ_m, estar dentro del entrenamiento afecta el poder predictivo SOLO por look-ahead, y la brecha de capacidad entre generaciones es constante en el calendario (tendencias paralelas de la brecha). Amenazas:

- (i) Obsolescencia. El modelo viejo desconoce entidades y conceptos nuevos, así que rinde menos después de su corte por falta de conocimiento legítimo, no porque pierda el look-ahead. Los dos mecanismos producen una caída en c_m.
  - El look-ahead es un escalón en el corte y es sensible a la anonimización.
  - La obsolescencia crece con la distancia al corte y se concentra en titulares con entidades nuevas.
- (ii) Hacinamiento heterogéneo. Si el modelo más usado, que suele ser el más nuevo, es el más arbitrado, hay una interacción modelo×calendario correlacionada con el corte. Mitigación: usar el componente ortogonal entre scores.
- (iii) Calibración distinta entre generaciones. Mitigación: rangos dentro de cada modelo y fecha.
- (iv) Recuperación o búsqueda web: debe estar apagada.

La exclusión más limpia se logra variando SOLO el corte: la misma arquitectura preentrenada con datos truncados cronológicamente, o el continued pretraining de un modelo abierto hasta fechas distintas. Así la capacidad es constante por construcción.

PREGUNTA 2

EE ≈ 0.82 implica n ≈ 252/0.82² ≈ 375 días (EE ≈ 1/√años).

Autocorrelación positiva: el EE SUBE.

- La varianza de la media se multiplica por f = 1 + 2Σρ_k. Con AR(1):
  - ρ = 0.05: f = 1.11, EE 0.86;
  - ρ = 0.10: f = 1.22, EE 0.91;
  - ρ = 0.20: f = 1.50, EE 1.00.
- Además (Lo 2002), anualizar con √252 sobrestima el Sharpe en √f, así que la estimación puntual también baja.

Curtosis 10: el EE también SUBE, pero casi nada a frecuencia diaria.

- Var(SR̂) = [1 − γ3·SR + (γ4−1)/4·SR²]/n, donde SR es el diario: 1.2/√252 ≈ 0.076 o 2.4/√252 ≈ 0.15.
- Pasar de γ4 = 3 a γ4 = 10 lleva el factor de 1.003 a 1.013 (SR 1.2), o de 1.011 a 1.051 (SR 2.4): el EE pasa de 0.82 a 0.825-0.84.
- Un sesgo negativo pesa más: con γ3 = −1, EE 0.855-0.90.
- La curtosis importa en frecuencias bajas o en muestras chicas, no aquí.

¿Cambia la conclusión? No; se refuerza.

- Para no rechazar ni 0 ni 2.4 con EE 0.82, el SR posterior tiene que estar en (~0.8, ~1.6). Con un intervalo más ancho sigue sin rechazarse ninguno. Ejemplo con SR ≈ 1.1 y EE 0.91: z(0) = 1.2 y z(2.4) = 1.4.
- La prueba no tiene potencia. Para distinguir 1.2 de 0 con 80% de potencia hacen falta ≈ ((1.96 + 0.84)/1.2)² ≈ 5.4 años con datos iid, y unos 6.6 con f = 1.22. La respuesta honesta es 'no sabemos'.

El z ≈ 3.7 contra 4.1. Lo leo como (4.1 − SR_post)/0.82: trata 4.1 como una constante conocida. Tiene dos errores:

- Ignora el EE del propio 4.1; el denominador debería ser √(EE_pre² + EE_post²).
- 4.1 es el máximo de muchas variantes, así que está sesgado al alza (maldición del ganador). Parte de la caída es regresión a la media, no look-ahead. Selección y look-ahead quedan confundidos en esa caída.
- Además, el DSR corrige la selección, no el look-ahead.

Deflated Sharpe sin documentación del número de ensayos:

1) Reconstruir N con artefactos: historial de git y notebooks, logs y facturación de la API (llamadas por modelo y por hash de prompt) y el tracker de experimentos. Enumerar la rejilla: prompts × modelos × umbrales × horizontes × universos × ponderaciones × filtros. Lo que no esté documentado se trata con la cota alta plausible.
2) Correlación entre variantes:
   - reejecutar la rejilla para obtener la matriz T×N de rendimientos;
   - agruparla (ONC o clustering jerárquico) y tomar N_eff = número de clusters, o (Σλ_i)²/Σλ_i², o ρ̄ + (1−ρ̄)N;
   - V[SR] = varianza de los Sharpes entre los representantes de cada cluster, no entre variantes casi idénticas ni entre trayectorias.
3) SR0 = √V·[(1−γ)Φ⁻¹(1 − 1/N_eff) + γΦ⁻¹(1 − 1/(e·N_eff))] y DSR = Φ[(SR̂ − SR0)√(n−1) / √(1 − γ3·SR̂ + (γ4−1)/4·SR̂²)], en frecuencia diaria y con un n efectivo ajustado por autocorrelación.
4) Sensibilidad y punto de quiebre. Reportar el DSR como función de N y el N* que lo lleva a 0.95.
   - En unidades del EE de cada ensayo, el máximo esperado de N ensayos nulos independientes es 1.57 (N = 10), 2.53 (100), 3.26 (1,000) y 3.69 (5,000).
   - Un z ≈ 3.7 se explica con N_eff ≈ 5,200; un z de 2.9, con unos 300.
   - Una rejilla de 5 prompts × 4 modelos × 10 umbrales × 5 horizontes × 3 universos ya son 3,000 variantes brutas: la selección por sí sola puede explicar buena parte.
   - La correlación reduce N_eff y V al mismo tiempo. Hay que estimar ambos juntos, no corregir uno solo.
5) Sin N documentado, la evidencia limpia es una retención congelada:
   - fijar hoy (con hash) el prompt, el modelo y el umbral;
   - preregistrar;
   - medir con datos posteriores a la congelación.
   Si el periodo posterior al corte se usó para elegir la variante, también SR_post necesita deflación.

**Dictamen del juez: deducción 0.0.** Motivo textual del juez (lo emitió en inglés):

> The identification is solid: a headline x model panel with headline/date fixed effects that absorb calendar decay, model fixed effects for capability, and beta identified only from headlines dated between cutoffs. It mentions staggered DiD with correct estimators (Sun-Abraham, Callaway-Sant'Anna) and cutoff placebos. The exclusion restriction (parallel trends in the capability gap) is stated explicitly, the threats are relevant (obsolescence vs look-ahead, told apart as a step vs a slope and by anonymization), and so is the cleanest remedy (same architecture with truncated pretraining). On Q2 it correctly states that positive autocorrelation raises the standard error by the factor f and that sqrt(252) annualization overstates the Sharpe. The kurtosis calculation shows, correctly, that the effect is negligible at daily frequency. The conclusion of low power (about 5.4 years) is sound. It self-critiques the original z honestly: the SE of the 4.1 is ignored and the winner's curse confounds selection with look-ahead, which strengthens rather than overturns the original conclusion. The Deflated Sharpe procedure (reconstructing N from artifacts, N_eff by clustering or rho + (1-rho)N, sensitivity and break-even N*, frozen holdout) is correct and complete.

**Puntaje final: 5.0/5** (A 5.0, B 5.0; promedio 5.0; deducción de la defensa 0.0).

### Hueco
Ninguno con costo. Sarkar-Vafa (2024) no aparece; la rúbrica lo lista como evidencia posible, no obligatoria. Glasserman-Lin y He-Lv-Manela-Wu se citaron de memoria y bien. El EE posterior al corte (0.82) se calculó con la fórmula de Lo a frecuencia diaria; la clave da 0.94 con la aproximación anual. Las dos son válidas.

**Observación del secretario sobre la defensa oral.** En la segunda repregunta, el sustentante describió su propio z ≈ 3.7 como "(4.1 − SR_post)/0.82", es decir, como si hubiera tratado 4.1 como una constante conocida, y se corrigió pidiendo √(EE_pre² + EE_post²). No es exacto: en la respuesta escrita ya había usado EE_pre ≈ 0.34, y (4.1 − 0.8)/√(0.82² + 0.34²) = 3.72. Con 4.1 como constante habría salido ≈ 4.0. Es un error al releer su propio cálculo, en dirección autocrítica, y el punto de fondo es correcto: la maldición del ganador sesga el 4.1 y confunde selección con look-ahead. El juez no dedujo nada y esta acta no modifica la deducción, pero deja el error asentado.

---

## S7-05 — Microestructura: modelo de Kyle (1985) y lambda; competencia entre insiders (derivacion)

### Enunciado
Modelo de Kyle (1985) de un periodo: el valor v ~ N(p0, Σ0); los noise traders envían u ~ N(0, σu²), independiente de v; un insider neutral al riesgo observa v y envía x; un creador de mercado competitivo observa y = x + u y fija p = E[v | y].

(a) Conjeture x = β(v − p0) y p = p0 + λy. Derive β, λ, el beneficio esperado del insider y Var(v | y).

(b) Con √Σ0 = $1.50 y σu = 30,000 acciones, calcule: λ en $ por acción (RESULTADO NUMÉRICO PRINCIPAL), β, el impacto en precio de un flujo neto de 40,000 acciones, el beneficio esperado del insider, la varianza posterior y la pérdida esperada de los noise traders.

(c) Extienda a N insiders idénticos con la misma señal que compiten à la Cournot. Derive λ_N = √(NΣ0)/((N+1)σu), la intensidad individual β_i, el beneficio total esperado y Var(v | y). Evalúe con N = 4.

(d) Interprete: ¿por qué el insider monopolista no revela toda su información? ¿Qué ocurre en la versión continua de Kyle y con varios insiders en múltiples periodos (Holden-Subrahmanyam 1992)? ¿Cómo se estima λ empíricamente?

### Clave (texto descifrado, idéntico al de `clave.json`)
(a) Insider: max_x E[(v − p0 − λ(x + u))x | v] ⇒ x = (v − p0)/(2λ) ⇒ β = 1/(2λ). Creador de mercado: λ = Cov(v, y)/Var(y) = βΣ0/(β²Σ0 + σu²). Sustituyendo: λ = √Σ0/(2σu), β = σu/√Σ0. Beneficio esperado: E[(v−p0)²]/(4λ) = Σ0/(4λ) = ½√Σ0·σu. Var(v|y) = Σ0 − λβΣ0 = Σ0/2.

(b) λ = 1.5/(2·30,000) = 2.5×10⁻⁵ $/acción (= $0.25 por cada 10,000 acciones); β = 30,000/1.5 = 20,000 acciones por $; impacto de 40,000 = $1.00; beneficio esperado = ½·1.5·30,000 = $22,500; Var posterior = 1.125 (desv. $1.06); los noise traders pierden en esperanza $22,500 (el creador de mercado tiene beneficio esperado cero).

(c) FOC del insider i: (v−p0) − λ(2x_i + (N−1)β(v−p0)) = 0 ⇒ en simetría λβ(N+1) = 1 ⇒ β = 1/((N+1)λ). Creador de mercado: λ = NβΣ0/(N²β²Σ0 + σu²) ⇒ λ² = NΣ0/((N+1)²σu²) ⇒ λ_N = √(NΣ0)/((N+1)σu). Beneficio total = √(NΣ0)·σu/(N+1); Var(v|y) = Σ0/(N+1). Con N = 4: λ = 3/150,000 = 2.0×10⁻⁵; β_i = 10,000 (total 40,000); beneficio total $18,000 ($4,500 c/u); Var posterior 0.45. La competencia hace más agresivo el trading, precios más informativos, mercado más profundo y menores pérdidas de los noise traders.

(d) El insider internaliza su propio impacto: operar más mueve el precio en su contra; el ruido le da camuflaje, y en equilibrio el flujo revela la mitad de la varianza. En tiempo continuo, λ es constante, el insider opera gradualmente, la información se incorpora linealmente y el precio iguala v al final (Σ_T = 0). Con varios insiders en múltiples periodos (Holden-Subrahmanyam 1992) compiten agresivamente y la información se revela muy rápido; en el límite de subastas continuas la profundidad es infinita. Estimación: regresión de cambios de precio sobre flujo de órdenes firmado (Lee-Ready), Glosten-Harris (1988), VAR de Hasbrouck (1991); proxy de baja frecuencia: ILLIQ de Amihud (2002).

**Valor numérico principal comprometido:** 2.5e-05 ± 5e-07.

**Rúbrica:** 5 puntos. (a) 1.5 pts: FOC del insider (0.5), condición de eficiencia del creador de mercado y solución de λ, β (0.5), beneficio y Var posterior (0.5). (b) 1 pt: λ = 2.5×10⁻⁵ (0.5, tolerancia ±5×10⁻⁷), resto de cantidades (0.5). (c) 1.5 pts: derivación de λ_N y β_i (0.75), valores con N = 4 (λ = 2×10⁻⁵, beneficio 18,000, Var 0.45) (0.75). (d) 1 pt: intuición de revelación parcial (0.25), versión continua y competencia multiperiodo (0.5), métodos de estimación (0.25).

### Fuente
Kyle, A. S. (1985), 'Continuous Auctions and Insider Trading', Econometrica 53(6): 1315–1335; Holden, C., Subrahmanyam, A. (1992), 'Long-Lived Private Information and Imperfect Competition', Journal of Finance 47(1): 247–270; Hasbrouck, J. (1991), JF 46(1); Amihud, Y. (2002), JFM 5(1); O'Hara, Market Microstructure Theory (1995). Equilibrio verificado con python3.

### Respuesta del sustentante (completa)
El repo no cubre Kyle (1985). La derivación es propia y los números los calculé en python3.

(a) Con x = β(v − p0) e y = x + u:

- El creador de mercado fija λ = Cov(v, y)/Var(y) = βΣ0/(β²Σ0 + σu²).
- El insider maximiza E[x(v − p)|v] = x(v − p0 − λx), así que x = (v − p0)/(2λ) y β = 1/(2λ).
- Sustituyendo: λσu² = Σ0/(4λ), de donde λ = √Σ0/(2σu) y β = σu/√Σ0.
- Beneficio esperado: E[(v − p0)²]/(4λ) = σu√Σ0/2.
- Var(v|y) = Σ0(1 − λβ) = Σ0/2.

(b) Con √Σ0 = 1.50 y σu = 30,000:

- λ = 1.5/60,000 = 2.5×10⁻⁵ $/acción (RESULTADO PRINCIPAL).
- β = 20,000 acciones por $.
- Impacto de 40,000 acciones: 2.5×10⁻⁵ × 40,000 = $1.00.
- Beneficio esperado del insider: 30,000 × 1.5/2 = $22,500.
- Var(v|y) = 2.25/2 = 1.125 $² (DE ≈ $1.06).
- Pérdida esperada de los noise traders: $22,500, porque el creador de mercado competitivo tiene beneficio esperado cero.

(c) N insiders à la Cournot, con x_i = β_i(v − p0):

- La CPO de i es v − p0 − λΣ_{j≠i}x_j − 2λx_i = 0. En equilibrio simétrico, β_i = 1/(λ(N+1)) y β = Nβ_i.
- Sustituyendo en λ = βΣ0/(β²Σ0 + σu²): λ²σu² = NΣ0/(N+1)², o sea λ_N = √(NΣ0)/((N+1)σu).
- β_i = σu/√(NΣ0); β total = √N·σu/√Σ0; λβ = N/(N+1).
- Var(v|y) = Σ0/(N+1).
- Beneficio total = βΣ0/(N+1) = √N·σu√Σ0/(N+1).

Con N = 4:

- λ = 3/150,000 = 2.0×10⁻⁵ (un flujo de 40,000 acciones mueve el precio $0.80).
- β_i = 10,000 y β total = 40,000.
- Beneficio total = $18,000, es decir $4,500 por insider (antes $22,500).
- Var(v|y) = 0.45.

La competencia vuelve el precio más informativo y el mercado más profundo, y disipa las rentas. Cuando N → ∞, λ, Var(v|y) y el beneficio tienden a 0.

(d) Interpretación:

- El monopolista no revela todo porque cada acción extra mueve el precio en su contra (λx). Iguala el margen marginal con el impacto y opera la mitad de lo que 'vale' su información. El precio incorpora justo la mitad de ella (Var se reduce a la mitad), y los noise traders le sirven de camuflaje.
- Kyle continuo: el insider opera de forma gradual. λ es constante (√Σ0/σu con T = 1), el flujo agregado se ve como ruido browniano y la información entra linealmente hasta revelarse por completo en T. El beneficio es σu√Σ0, el doble que en una subasta (de memoria).
- Holden-Subrahmanyam (1992): con varios insiders idénticos y muchas subastas compiten ('rat race'). La información se revela casi de inmediato, la profundidad se vuelve muy grande y los beneficios tienden a cero en el límite continuo. Con señales heterogéneas (Foster-Viswanathan 1996) hay un 'waiting game' y la revelación es más lenta.
- Estimación empírica de λ: regresión de Δp intradía (5-30 min) sobre el flujo firmado (volumen comprador menos vendedor, con la clasificación de Lee-Ready); Glosten-Harris (1988); VAR de Hasbrouck (1991) para el impacto permanente. En frecuencia baja se usa Amihud (2001) |r|/volumen en $ como proxy, validado contra λ de alta frecuencia (Goyenko-Holden-Trzcinka 2009). Estas referencias son de memoria y no están en el repo.

### Calificación automática
**Dentro de tolerancia:** esperado 2.5e-05, obtenido 2.5e-05, tolerancia ±5e-07 (|diferencia| = 0).

### Calificación
**Calificador A: 5.0/5.** (a) CPO del insider, eficiencia del creador de mercado, λ=√Σ0/(2σu), β=σu/√Σ0, beneficio ½σu√Σ0 y Var=Σ0/2: todo correcto. (b) λ=2.5e-5, β=20,000, impacto $1.00, beneficio $22,500, Var 1.125 y pérdida de los noise traders $22,500: correctos. (c) Deriva λ_N y β_i y da Var=Σ0/(N+1) y el beneficio total. Con N=4: λ=2e-5, β_i=10,000, $18,000 y 0.45, todos correctos. (d) La intuición de revelación parcial es correcta. En Kyle continuo, λ constante y el beneficio σu√Σ0 son correctos; Holden-Subrahmanyam está bien descrito y añade Foster-Viswanathan. Los métodos de estimación son correctos. Solo un detalle menor: fecha Amihud 2001 en vez de 2002.

**Calificador B: 5.0/5.** (a) 1.5/1.5. La condición de primer orden del insider, la eficiencia del creador de mercado, λ = √Σ0/(2σu), β, el beneficio ½σu√Σ0 y Var = Σ0/2 son correctos. (b) 1/1. λ = 2.5e-5, β = 20,000, impacto $1.00, beneficio $22,500, Var 1.125 y pérdida de los noise traders $22,500. (c) 1.5/1.5. Deriva λ_N y β_i = σu/√(NΣ0). Con N = 4: λ = 2e-5, β_i = 10,000, beneficio $18,000 y Var 0.45, todo correcto. (d) 1/1. Explica bien la revelación parcial. Kyle continuo con λ constante, revelación completa y beneficio σu√Σ0; Holden-Subrahmanyam como rat race y Foster-Viswanathan como waiting game, todo correcto. En los métodos de estimación, Amihud aparece como 2001 en vez de 2002 (JFM), un error menor de año que no justifica descuento.

|A − B| = 0 ≤ 1: promedio 5.0, sin arbitraje.

### Defensa oral
No hubo repreguntas sobre esta pregunta; la defensa oral cubrió S7-01 a S7-04. Deducción: 0.

**Puntaje final: 5.0/5** (A 5.0, B 5.0; promedio 5.0; deducción de la defensa 0.0).

### Hueco
Ninguno. Kyle no está en la base; la derivación es propia y correcta en todo.

**Detalle sin costo:** fecha de Amihud (2001 en vez de 2002, JFM).

**Acción:** agregar a la base, que hoy no lo cubre, Kyle (1985) en sus versiones de un periodo, con N insiders y continua, y Holden-Subrahmanyam (1992).

---

## S7-06 — Microestructura: Glosten-Milgrom, componente de selección adversa del spread y PFOF (calculo)

### Enunciado
Modelo de Glosten-Milgrom (1985): V ∈ {98, 102}, con prior P(V = 102) = 0.5. En cada instante llega un trader: con probabilidad μ = 0.3 es informado (compra si V = 102, vende si V = 98); con probabilidad 1 − μ es no informado y compra o vende con probabilidad 1/2. El creador de mercado es competitivo y neutral al riesgo, sin costos de inventario ni de procesamiento.

(a) Derive el ask y el bid iniciales y el spread; muestre que en este caso simétrico spread = μ(V_H − V_L).

(b) La primera operación es una compra. Actualice la creencia y calcule el nuevo ask (RESULTADO NUMÉRICO PRINCIPAL, 4 decimales) y el nuevo bid. ¿Qué ocurre con el spread y por qué?

(c) PFOF: un mayorista compra el flujo minorista segregado, cuya fracción informada es μ_r = 0.05, y lo ejecuta contra las cotizaciones de la bolsa del inciso (a), dando al cliente una mejora de precio de $0.10 por acción. ¿Cuál es el pago máximo por acción que puede ofrecer al bróker sin pérdida esperada? Conecte con el 'cream-skimming' (Easley, Kiefer y O'Hara 1996) y con la externalidad sobre el spread de la bolsa.

(d) Resuma el estado regulatorio del PFOF en EE.UU. y en la Unión Europea a septiembre de 2026.

### Clave (texto descifrado, idéntico al de `clave.json`)
(a) P(compra|H) = μ + (1−μ)/2 = 0.65; P(compra|L) = 0.35; P(compra) = 0.5 ⇒ P(H|compra) = 0.65 ⇒ ask = 98 + 4·0.65 = 100.60. Análogamente P(H|venta) = 0.35 ⇒ bid = 99.40. Spread = 1.20 = 0.3·4 = μ(V_H − V_L): todo el spread es selección adversa (el creador de mercado gana a los no informados lo que pierde con los informados).

(b) π = 0.65. P(compra) = 0.65·0.65 + 0.35·0.35 = 0.545; P(H|compra) = 0.4225/0.545 = 0.77523 ⇒ ask₂ = 98 + 4·0.77523 = 101.1009. P(venta) = 0.455; P(H|venta) = 0.65·0.35/0.455 = 0.50 ⇒ bid₂ = 100.00. Spread₂ = 1.1009 < 1.20: menor incertidumbre (π(1−π) cae de 0.25 a 0.2275), menor selección adversa esperada; los precios de transacción son martingala respecto a la información pública y convergen a V.

(c) E[V | compra minorista] = 100 + 0.05·2 = 100.10 (análogamente 99.90 para ventas). El mayorista vende a 100.60 − 0.10 = 100.50 ⇒ beneficio esperado 0.40 por acción; compra a 99.50 frente a 99.90 ⇒ 0.40. Pago máximo por flujo ≈ $0.40/acción (antes de costos operativos). Es 'cream-skimming': se extrae el flujo no informado; EKO (1996) encuentran que las órdenes compradas y ejecutadas en Cincinnati contenían significativamente menos información que las del NYSE. Externalidad: el flujo que queda en la bolsa es más tóxico (μ_lit sube) ⇒ se amplía el spread público (spread = μ_lit·4), lo que también aumenta la referencia NBBO contra la que se mide la 'mejora de precio'.

(d) EE.UU.: la SEC retiró formalmente el 12 de junio de 2025 catorce propuestas, incluida la Order Competition Rule (Regla 615 propuesta, subastas obligatorias antes de internalizar); el PFOF sigue siendo legal con obligaciones de mejor ejecución y divulgación. UE: el art. 39a de MiFIR (en vigor desde el 28 de marzo de 2024) prohíbe el PFOF; la exención temporal (solo Alemania la usó) expiró el 30 de junio de 2026, así que la prohibición es plena en toda la UE.

**Valor numérico principal comprometido:** 101.1009 ± 0.005.

**Rúbrica:** 5 puntos. (a) 1 pt: ask 100.60, bid 99.40 y spread = μ(V_H − V_L) con derivación bayesiana. (b) 1.5 pts: posterior 0.65 (0.25), ask₂ = 101.1009 (0.75, tolerancia ±0.005), bid₂ = 100.00 y explicación del estrechamiento (0.5). (c) 1.5 pts: E[V|minorista] (0.5), PFOF máximo $0.40 (0.5), cream-skimming con evidencia EKO y externalidad sobre el spread público (0.5). (d) 1 pt: EE.UU. retiro de la Regla 615 en junio de 2025 (0.5); UE prohibición del art. 39a con fin de exención el 30-jun-2026 (0.5).

### Fuente
Glosten, L., Milgrom, P. (1985), Journal of Financial Economics 14(1): 71–100; Easley, D., Kiefer, N., O'Hara, M. (1996), 'Cream-Skimming or Profit-Sharing? The Curious Role of Purchased Order Flow', Journal of Finance 51(3): 811–833; SEC, Withdrawal of Proposed Regulatory Actions (Federal Register, 17-jun-2025; Release 33-11377); Reglamento (UE) 2024/791 (MiFIR art. 39a) y lista de ESMA de Estados miembros con exención temporal de PFOF. Cálculos verificados con python3.

### Respuesta del sustentante (completa)
(a) Probabilidad de compra según el valor:

- P(compra|VH) = μ + (1−μ)/2 = 0.65.
- P(compra|VL) = 0.35.

Ask = E[V|compra] = 98 + 4·P(H|compra), con P(H|compra) = 0.5·0.65/0.5 = 0.65. Ask = 100.60.

Bid = 98 + 4·0.35 = 99.40.

Spread = 1.20. En el caso simétrico (π = 0.5): 4[(1+μ)/2 − (1−μ)/2] = μ(VH − VL) = 0.3·4 = 1.2.

(b) Después de una compra, π1 = 0.65.

- Nuevo ask: P(H|compra) = 0.65·0.65/(0.65·0.65 + 0.35·0.35) = 0.4225/0.545 = 0.77523. Ask = 98 + 4·0.77523 = 101.1009 (RESULTADO PRINCIPAL).
- Nuevo bid: P(H|venta) = 0.65·0.35/(0.65·0.35 + 0.35·0.65) = 0.5. Bid = 100.00.
- Spread = 1.1009, menor que 1.20. El punto medio sube a 100.55 y E[V|historia] = 100.60, el ask anterior, como corresponde a una martingala.

El spread se estrecha porque la creencia ya está más concentrada: hay menos incertidumbre sobre V y la selección adversa de la siguiente operación pesa menos. En GM el spread tiende a 0 conforme el precio revela V.

(c) PFOF con μ_r = 0.05:

- P(H|compra minorista) = 0.05 + 0.475 = 0.525, así que E[V|compra] = 100.10.
- El mayorista le vende al cliente a 100.60 − 0.10 = 100.50 y gana 0.40 esperados.
- Del lado de las ventas: E[V|venta] = 99.90, compra a 99.40 + 0.10 = 99.50 y gana 0.40.
- Pago máximo sin pérdida esperada: $0.40 por acción, que equivale al medio spread de la bolsa (0.60) menos la selección adversa minorista (4·0.05/2 = 0.10) menos la mejora de precio (0.10).

Cream-skimming: Easley, Kiefer y O'Hara (1996, JF), de memoria, encuentran que el flujo comprado (Cincinnati/Madoff) estaba menos informado que el flujo del NYSE. Es consistente con el descreme y no con el reparto de beneficios.

Externalidad: la bolsa se queda con el flujo tóxico, su μ sube y el spread se amplía. Ejemplo hipotético propio: si 40 de cada 100 órdenes son minoristas con 5% de informados, en la bolsa queda μ = 28/60 = 0.467 y el spread pasa de 1.20 a 1.87. Pierden quienes no pueden segmentarse, y la 'mejora de precio' se mide contra un NBBO peor.

(d) Estado regulatorio a septiembre de 2026. Lo que no está en el repo es de memoria, no verificado.

EE.UU.:

- El PFOF es legal en acciones y opciones. Lo rigen la divulgación de la Regla 606, la mejor ejecución (FINRA 5310) y las estadísticas de la Regla 605, reformada en 2024.
- Del paquete de dic-2022, la Order Competition Rule (subastas para órdenes minoristas) y la Regulation Best Execution fueron retiradas por la SEC en jun-2025. Tampoco hubo prohibición.
- Sí se adoptó el tick de $0.005 y el tope de access fee de 10 mils (18-sep-2024). La Corte del Circuito de D.C. confirmó la regla el 14-oct-2025, y el cumplimiento se prorrogó al primer día hábil de noviembre de 2026 (repo 01:113, 228).
- Evidencia: el costo real de ida y vuelta va de 0.07% a 0.46% según el bróker, sin relación con el PFOF (Schwarz et al., JF 2025; 01:112).

Unión Europea:

- La revisión de MiFIR (Reglamento (UE) 2024/791, art. 39a) prohíbe recibir PFOF por órdenes de clientes minoristas.
- Había una exención transitoria opcional de los Estados miembros (sobre todo Alemania) hasta el 30-jun-2026. A septiembre de 2026 la prohibición aplica en toda la UE.
- El Reino Unido lo prohíbe desde 2012 (FCA).

### Calificación automática
**Dentro de tolerancia:** esperado 101.1009, obtenido 101.1009, tolerancia ±0.005 (|diferencia| = 0).

### Calificación
**Calificador A: 5.0/5.** (a) Ask 100.60, bid 99.40 y spread = μ(VH−VL) = 1.20, con derivación bayesiana. (b) Posterior 0.65, ask₂ = 101.1009 y bid₂ = 100.00. Explica el estrechamiento del spread y añade la propiedad martingala. (c) E[V|compra minorista] = 100.10 y PFOF máximo $0.40, con una descomposición clara. Cita bien a EKO (Cincinnati/Madoff) y cuantifica la externalidad con un ejemplo aritméticamente correcto (μ=0.467, spread 1.87). (d) EE.UU.: retiro de la Order Competition Rule en junio de 2025. Verifiqué con búsqueda web la confirmación del D.C. Circuit del 14-oct-2025 sobre la regla de tick y access fee. UE: prohibición del art. 39a y fin de la exención el 30-jun-2026. Completo.

**Calificador B: 5.0/5.** (a) 1/1. Ask 100.60, bid 99.40 y spread = μ(VH − VL), con derivación bayesiana. (b) 1.5/1.5. π = 0.65, ask₂ = 101.1009 y bid₂ = 100.00. Explica bien el estrechamiento y además comprueba la martingala (E[V] = 100.60). (c) 1.5/1.5. E[V|compra minorista] = 100.10 y PFOF máximo de $0.40, con la descomposición en medio spread menos selección adversa menos mejora de precio. Cita correctamente a EKO 1996 (Cincinnati/Madoff) y da un ejemplo numérico correcto de la externalidad (μ = 0.467, spread 1.87). (d) 1/1. EE.UU.: retiro de la Order Competition Rule en junio de 2025, correcto. Verifiqué que el D.C. Circuit confirmó la regla de tick y access fee el 14-oct-2025. UE: art. 39a MiFIR con la exención hasta el 30-jun-2026, correcto.

|A − B| = 0 ≤ 1: promedio 5.0, sin arbitraje.

### Defensa oral
No hubo repreguntas sobre esta pregunta; la defensa oral cubrió S7-01 a S7-04. Deducción: 0.

**Puntaje final: 5.0/5** (A 5.0, B 5.0; promedio 5.0; deducción de la defensa 0.0).

### Hueco
Ninguno. EKO (1996) y parte del estado regulatorio de EE.UU. salieron de memoria y están marcados. La regla de tick y access fee, y su confirmación judicial, sí están en la base (01:113, 228). El ejemplo de externalidad (μ = 0.467, spread 1.87) es propio e hipotético, y así lo rotula.

---

## S7-07 — Microestructura: medida de Roll del spread efectivo a partir de datos de transacciones (laboratorio)

### Enunciado
Datos crudos: precios de 16 transacciones consecutivas de una acción en la misma sesión (USD):

24.96, 24.94, 24.99, 24.94, 25.02, 25.02, 25.01, 24.94, 25.01, 25.04, 25.04, 24.96, 24.95, 25.03, 24.97, 24.95.

Sea Δp_t, t = 1, …, 15, el cambio de precio, d̄ su media, γ̂0 = (1/14) Σ_{t=1}^{15} (Δp_t − d̄)² y γ̂1 = (1/14) Σ_{t=2}^{15} (Δp_t − d̄)(Δp_{t−1} − d̄).

(a) Calcule los Δp_t (en centavos), d̄, γ̂0, γ̂1 y la autocorrelación de primer orden.

(b) Con el modelo de Roll (1984), p_t = m_t + c·Q_t, Q_t = ±1 i.i.d. equiprobable, m_t paseo aleatorio con innovaciones u_t independientes de Q: estime el medio spread c y el spread efectivo s = 2c en centavos (RESULTADO NUMÉRICO PRINCIPAL, 2 decimales) y en puntos base del precio medio.

(c) Usando Var(Δp) = 2c² + σu², estime σu² y la fracción de la varianza de los cambios de precio atribuible al rebote bid-ask.

(d) Suponga ahora que los signos de las operaciones siguen una cadena de Markov con corr(Q_t, Q_{t−k}) = ρ_Q^k (u sigue independiente). Derive Cov(Δp_t, Δp_{t−1}) = −c²(1 − ρ_Q)² y recalcule el spread implícito con ρ_Q = 0.25 usando el mismo γ̂1. ¿En qué dirección sesga el estimador de Roll ignorar la persistencia?

(e) Mencione dos limitaciones del estimador de Roll y dos alternativas publicadas para datos diarios.

### Clave (texto descifrado, idéntico al de `clave.json`)
(a) Δp (centavos): −2, +5, −5, +8, 0, −1, −7, +7, +3, 0, −8, −1, +8, −6, −2; d̄ = −0.0667¢. γ̂0 = 28.21 ¢² (0.0028210 $²); Σ productos = −131.80 ¢² ⇒ γ̂1 = −9.4146 ¢² (−0.00094146 $²); ρ̂1 = −0.334.

(b) c = √(−γ̂1) = 3.068¢; s = 2c = 6.14¢ (6.137). Precio medio 24.986 ⇒ s ≈ 24.6 pb.

(c) σu² = γ̂0 − 2c² = 28.21 − 18.83 = 9.38 ¢² (0.000938 $²); fracción por rebote = 2c²/γ̂0 = 66.7%.

(d) Cov(ΔQ_t, ΔQ_{t−1}) = Cov(Q_t,Q_{t−1}) − Cov(Q_t,Q_{t−2}) − Var(Q_{t−1}) + Cov(Q_{t−1},Q_{t−2}) = ρ − ρ² − 1 + ρ = −(1−ρ)² ⇒ Cov(Δp_t, Δp_{t−1}) = −c²(1−ρ_Q)². Entonces c = √(−γ̂1)/(1 − ρ_Q) = 3.068/0.75 = 4.09¢ ⇒ s = 8.18¢. Ignorar la persistencia de signos subestima el spread (sesgo hacia abajo en un factor 1 − ρ_Q). (También Var(ΔQ) = 2(1−ρ_Q).)

(e) Limitaciones: la autocovarianza muestral puede ser positiva (estimador indefinido), fuerte ruido en muestras pequeñas, supone Q i.i.d. y ausencia de componente informativo/inventario (con impacto informativo la autocovarianza se atenúa), sensible a la discreción del tick. Alternativas: estimador bayesiano con muestreo de Gibbs (Hasbrouck 2009), estimador alto-bajo de Corwin-Schultz (2012), estimador cierre-alto-bajo de Abdi-Ranaldo (2017); con datos TAQ, spread efectivo 2|p − m| y descomposición en spread realizado + impacto de precio.

**Valor numérico principal comprometido:** 6.14 ± 0.1.

**Rúbrica:** 5 puntos. (a) 1.5 pts: Δp correctos (0.5), γ̂0 y γ̂1 con el estimador especificado (0.75), ρ̂1 (0.25). (b) 1 pt: s = 6.14¢ (tolerancia ±0.1¢) y ≈24.6 pb. (c) 0.5 pts: σu² ≈ 9.38 ¢² y 66.7%. (d) 1.5 pts: derivación de −(1−ρ)² (1.0), s = 8.18¢ y dirección del sesgo (0.5). (e) 0.5 pts: dos limitaciones y dos alternativas correctas.

### Fuente
Roll, R. (1984), 'A Simple Implicit Measure of the Effective Bid-Ask Spread in an Efficient Market', Journal of Finance 39(4): 1127–1139; Hasbrouck, J. (2009), Journal of Finance 64(3); Corwin, S., Schultz, P. (2012), Journal of Finance 67(2); Abdi, F., Ranaldo, A. (2017), Review of Financial Studies 30(12); Hasbrouck, Empirical Market Microstructure (2007), cap. 5. Serie y estimaciones verificadas con python3.

### Respuesta del sustentante (completa)
Todo se calculó con código propio a partir de los 16 precios crudos.

(a) Δp en centavos: −2, +5, −5, +8, 0, −1, −7, +7, +3, 0, −8, −1, +8, −6, −2.

- d̄ = −1/15 = −0.0667 c.
- γ̂0 = (1/14)Σ(Δp − d̄)² = 28.2095 c².
- γ̂1 = −9.4146 c².
- Autocorrelación de primer orden = −0.3337. Es negativa, cercana al −0.5 del rebote puro.

(b) Roll: Cov(Δp_t, Δp_{t−1}) = −c², así que c = √(−γ̂1) = √9.4146 = 3.068 c.

- Spread efectivo s = 2c = 6.14 centavos (RESULTADO PRINCIPAL).
- Precio medio de las 16 operaciones = 24.9856. s = 0.0614/24.9856 = 24.56 pb, y c = 12.28 pb.

(c) Var(Δp) = 2c² + σu², de donde σu² = 28.2095 − 18.8292 = 9.380 c² (σu ≈ 3.06 c). La fracción de la varianza atribuible al rebote bid-ask es 2c²/γ̂0 = 66.7%.

(d) Signos en cadena de Markov: Δp_t = u_t + c(Q_t − Q_{t−1}). Entonces Cov(Δp_t, Δp_{t−1}) = c²·Cov(Q_t − Q_{t−1}, Q_{t−1} − Q_{t−2}) = c²(ρ − ρ² − 1 + ρ) = −c²(1−ρQ)².

- Con ρQ = 0.25: c = √9.4146/0.75 = 4.091 c, así que s = 8.18 c (32.75 pb).
- Además Var(Δp) = 2c²(1−ρQ) + σu², con lo que σu² ≈ 3.10 c².

Ignorar la persistencia sesga el estimador de Roll hacia abajo: da c(1−ρQ) en vez de c, aquí 6.14 frente a 8.18.

(e) Limitaciones del estimador de Roll:

(1) Si la autocovarianza muestral es positiva, el spread no está definido (raíz imaginaria). Pasa con frecuencia en datos diarios.

(2) Supone flujo iid y sin información (u independiente de Q). Con selección adversa o persistencia solo capta el componente transitorio y subestima el spread.

(3) Es muy ruidoso en muestras chicas (15 cambios aquí) y supone un spread constante, sin operaciones en el punto medio ni discreción de tick.

Alternativas publicadas para datos diarios (de memoria, no están en el repo):

- Corwin y Schultz (2012, JF), con máximos y mínimos.
- Abdi y Ranaldo (2017, RFS), CHL con cierre, máximo y mínimo.
- Hasbrouck (2009, JF), Roll bayesiano con muestreo de Gibbs.
- Otras: Lesmond-Ogden-Trzcinka (1999, días con rendimiento cero) y Ardia-Guidotti-Kroencke (2024, JFE, EDGE con OHLC).

### Calificación automática
**Dentro de tolerancia:** esperado 6.14, obtenido 6.14, tolerancia ±0.1 (|diferencia| = 0).

### Calificación
**Calificador A: 5.0/5.** (a) Los Δp, d̄, γ̂0 = 28.21, γ̂1 = −9.4146 y ρ̂1 = −0.334 coinciden con la clave. (b) c = 3.068¢, s = 6.14¢ y 24.56 pb. (c) σu² = 9.38 ¢² y 66.7%. (d) La derivación −c²(1−ρ)² es correcta, s = 8.18¢ y el sesgo es a la baja. Añade correctamente Var(Δp) = 2c²(1−ρ)+σu² y recalcula σu². (e) Limitaciones válidas y alternativas bien citadas: Corwin-Schultz 2012, Abdi-Ranaldo 2017, Hasbrouck 2009, Ardia-Guidotti-Kroencke 2024. Completo.

**Calificador B: 5.0/5.** (a) 1.5/1.5. Los Δp son correctos, d̄ = −0.0667, γ̂0 = 28.21, γ̂1 = −9.4146 y ρ̂1 = −0.334. (b) 1/1. s = 6.14¢ y 24.56 pb. (c) 0.5/0.5. σu² = 9.38 ¢² y 66.7%. (d) 1.5/1.5. Deriva bien −c²(1−ρQ)², obtiene s = 8.18¢ y da la dirección del sesgo (a la baja). Además recalcula bien σu² = 3.10 con Var(ΔQ) = 2(1−ρ). (e) 0.5/0.5. Las limitaciones son válidas. Las alternativas (Corwin-Schultz 2012, Abdi-Ranaldo 2017, Hasbrouck 2009, Lesmond et al. 1999, Ardia-Guidotti-Kroencke 2024 JFE) son todas referencias reales.

|A − B| = 0 ≤ 1: promedio 5.0, sin arbitraje.

### Defensa oral
No hubo repreguntas sobre esta pregunta; la defensa oral cubrió S7-01 a S7-04. Deducción: 0.

**Puntaje final: 5.0/5** (A 5.0, B 5.0; promedio 5.0; deducción de la defensa 0.0).

### Hueco
Ninguno. En (d) recalculó además σu² con Var(ΔQ) = 2(1−ρ_Q) (3.10 ¢²), que la clave solo menciona de pasada. Las alternativas (Corwin-Schultz, Abdi-Ranaldo, Hasbrouck, Lesmond et al., Ardia-Guidotti-Kroencke) salieron de memoria, están marcadas y son correctas.

---

## S7-08 — Microestructura: ley de impacto de raíz cuadrada e implementation shortfall (calculo)

### Enunciado
Un gestor decide comprar Q = 400,000 acciones cuando el precio es $40.00 (precio de decisión). Volumen diario promedio V = 8,000,000 acciones; volatilidad diaria σ = 1.8%. Use la ley de raíz cuadrada para el impacto pico al terminar la metaorden: I(Q) = Y·σ·√(Q/V), con Y = 0.7.

(a) Calcule el impacto pico esperado en puntos base.

(b) Bajo la condición de 'fair pricing' de Farmer, Gerig, Lillo y Waelbroeck (2013), el precio promedio de ejecución iguala el precio tras la relajación, que es ≈ 2/3 del impacto pico. Calcule el costo de ejecución esperado en pb y en dólares para la orden completa.

(c) Ejecución real: la orden llega a la mesa cuando el precio es $40.05 (precio de llegada); se compran 300,000 acciones a un promedio de $40.25; comisión $0.01 por acción; las 100,000 restantes se cancelan cuando el precio es $40.60, que se usa para valuar el costo de oportunidad. Descomponga el implementation shortfall (Perold 1988) en costo de retraso, costo de ejecución, costo de oportunidad y comisiones; dé el total en dólares y en pb del portafolio en papel (Q × precio de decisión). RESULTADO NUMÉRICO PRINCIPAL: IS total en pb.

(d) Compare el costo de ejecución realizado (pb frente al precio de llegada) con la predicción del modelo para 300,000 acciones e interprete la diferencia.

(e) Si se duplica Q, ¿cómo cambian el impacto por acción y el costo total en dólares? ¿Qué evidencia respalda el exponente 1/2 y cuál propone otro?

### Clave (texto descifrado, idéntico al de `clave.json`)
(a) I = 0.7 × 0.018 × √0.05 = 0.0028174 ⇒ 28.17 pb.

(b) 2/3 × 28.17 = 18.78 pb; en dólares 0.0018783 × 400,000 × 40 = $30,053.

(c) Retraso = 300,000 × (40.05 − 40.00) = $15,000; ejecución = 300,000 × (40.25 − 40.05) = $60,000; oportunidad = 100,000 × (40.60 − 40.00) = $60,000; comisiones = $3,000. Total = $138,000 (= ganancia en papel 400,000×0.60 = $240,000 menos ganancia real 300,000×0.35 − 3,000 = $102,000). En pb: 138,000/16,000,000 = 86.25 pb.

(d) Realizado: 0.20/40.05 = 49.9 pb. Modelo para 300,000 (Q/V = 0.0375): pico 24.4 pb, promedio ≈ 16.3 pb. El exceso sugiere deriva adversa (información/alfa del gestor filtrándose, momentum, metaórdenes correlacionadas de otros), o simple ruido: la ley es un promedio condicional con enorme dispersión por orden. El costo de oportunidad elevado (el precio siguió subiendo) indica decaimiento del alfa: se debe equilibrar impacto y riesgo de retraso (Almgren-Chriss).

(e) Impacto por acción × √2 ≈ 1.414; costo total ∝ Q·√Q ⇒ × 2^{1.5} ≈ 2.83. Evidencia: Tóth et al. (2011, PRX), Bouchaud et al. (2018) y Sato y Kanazawa (2025, PRL 135: 257401) con datos por cuenta de toda la Bolsa de Tokio 2012–2019 muestran δ ≈ 1/2 de forma universal entre acciones; Almgren, Thum, Hauptmann y Li (2005, Risk), con ~700,000 órdenes de Citigroup, rechazan la raíz cuadrada para el impacto temporal en favor de un exponente 3/5 (0.6) y no rechazan impacto permanente lineal. El impacto es transitorio y decae tras terminar la metaorden (≈2/3 del pico según fair pricing).

**Valor numérico principal comprometido:** 86.25 ± 0.5.

**Rúbrica:** 5 puntos. (a) 0.5 pts: 28.17 pb. (b) 1 pt: 18.78 pb y ≈$30,053. (c) 2 pts: 0.4 por cada uno de los cuatro componentes y 0.4 por total $138,000 = 86.25 pb (tolerancia ±0.5 pb); si usa el precio de llegada como referencia para la oportunidad o un denominador distinto sin justificarlo, máximo 1 pt. (d) 0.75 pts: 49.9 pb frente a ~16–24 pb con interpretación económica. (e) 0.75 pts: factores √2 y 2.83 (0.35); evidencia a favor y en contra con cita correcta (0.4).

### Fuente
Perold, A. (1988), 'The Implementation Shortfall: Paper versus Reality', Journal of Portfolio Management 14(3): 4–9; Farmer, J. D., Gerig, A., Lillo, F., Waelbroeck, H. (2013), 'How Efficiency Shapes Market Impact', Quantitative Finance 13(11): 1743–1758; Almgren, R., Thum, C., Hauptmann, E., Li, H. (2005), 'Direct Estimation of Equity Market Impact', Risk; Tóth, B. et al. (2011), Physical Review X 1: 021006; Sato, Y., Kanazawa, K. (2025), Physical Review Letters 135: 257401; Almgren, R., Chriss, N. (2000), Journal of Risk 3(2). Cálculos verificados con python3.

### Respuesta del sustentante (completa)
El repo solo recoge el principio de medir el implementation shortfall contra el precio de decisión (01:333). El modelo y las cifras son cálculo propio.

(a) I = 0.7 × 0.018 × √(400,000/8,000,000) = 0.0126 × 0.2236 = 0.002817, o sea 28.17 pb de impacto pico.

(b) Fair pricing (Farmer-Gerig-Lillo-Waelbroeck 2013): costo = 2/3 × 28.17 = 18.78 pb. En dólares: 0.0018783 × 400,000 × $40 = $30,053.

(c) Descomposición de Perold. El portafolio en papel vale 400,000 × 40 = $16,000,000.

- Retraso: (40.05 − 40.00) × 300,000 = $15,000 (9.375 pb).
- Ejecución: (40.25 − 40.05) × 300,000 = $60,000 (37.5 pb).
- Oportunidad: (40.60 − 40.00) × 100,000 = $60,000 (37.5 pb).
- Comisiones: 0.01 × 300,000 = $3,000 (1.875 pb).
- Total: $138,000, que son 86.25 pb (RESULTADO PRINCIPAL).

Verificación: el papel gana (40.60 − 40.00) × 400,000 = $240,000 y el real gana (40.60 − 40.25) × 300,000 − 3,000 = $102,000. La diferencia es $138,000.

Otra convención: cargar el retraso a las 400,000 acciones ($20,000) y medir la oportunidad desde el precio de llegada ($55,000). El total es el mismo.

(d) Costo realizado frente al precio de llegada: (40.25 − 40.05)/40.05 = 49.9 pb, o 52.4 pb con comisión. El modelo para 300,000 acciones da un pico de 0.0126 × √0.0375 = 24.40 pb y un costo de 2/3 de eso, 16.27 pb. Lo realizado es ≈3.1 veces lo predicho.

Interpretación (inferencia):

- El precio venía subiendo (40.00 → 40.05 → 40.60, +137 pb frente a la llegada). Buena parte del 'costo' es deriva del mercado, sea momentum, otros compradores con la misma información o fuga, y no impacto propio.
- El modelo da un valor esperado, y la dispersión de una sola orden es enorme: σ diaria = 180 pb, mucho más que la diferencia de 34 pb.
- La cancelación está correlacionada con el movimiento adverso, lo que sesga lo que se observa.
- Para evaluar hace falta un benchmark ajustado por mercado (VWAP del intervalo o beta) y muchas órdenes.

(e) Si se duplica Q:

- El impacto por acción escala con √2: el pico pasa de 28.17 a 39.84 pb y el costo de 18.78 a 26.56 pb.
- El costo total en dólares escala con 2^{3/2} = 2.83: pasa de $30,053 a $85,002.

Evidencia sobre el exponente (de memoria, no está en el repo):

- A favor de δ ≈ 1/2: Torre (BARRA, 1997), Tóth et al. (2011, PRX) con metaórdenes de CFM, Bershova-Rakhlin (2013), Frazzini-Israel-Moskowitz (AQR, 'Trading Costs', 2018), Bucci et al. (2019) y Sato-Kanazawa (2024) con la Bolsa de Tokio completa.
- Alternativas: Almgren, Thum, Hauptmann y Li (2005, Risk) estiman un impacto temporal con exponente ≈ 3/5 (0.6); Zarinelli et al. (2015) ajustan mejor con forma logarítmica; Kyle-Obizhaeva (2016) derivan el escalamiento de la invariancia microestructural.

### Calificación automática
**Dentro de tolerancia:** esperado 86.25, obtenido 86.25, tolerancia ±0.5 (|diferencia| = 0).

### Calificación
**Calificador A: 5.0/5.** (a) 28.17 pb. (b) 18.78 pb y $30,053. (c) Los cuatro componentes son correctos ($15,000, $60,000, $60,000 y $3,000), con total de $138,000 = 86.25 pb sobre el portafolio en papel, más una verificación papel frente a real. (d) 49.9 pb frente a 24.4/16.3 del modelo, con interpretación económica sólida (deriva adversa, dispersión, sesgo por la cancelación, necesidad de benchmark). (e) Factores √2 y 2.83 correctos. La evidencia a favor (Tóth 2011, Bucci 2019, Sato-Kanazawa) y en contra (Almgren et al. 2005 con 3/5, Zarinelli 2015) está bien citada.

**Calificador B: 5.0/5.** (a) 0.5/0.5. 28.17 pb. (b) 1/1. 18.78 pb y $30,053. (c) 2/2. Retraso $15,000, ejecución $60,000, oportunidad $60,000 (medida contra el precio de decisión, que es lo correcto), comisiones $3,000, total $138,000 = 86.25 pb, con la verificación papel menos real. La convención alternativa que menciona da el mismo total. (d) 0.75/0.75. 49.9 pb frente a 24.4 y 16.3 pb, con una interpretación económica sólida: deriva, ruido y selección por la cancelación. (e) 0.75/0.75. Da los factores √2 y 2.83 con cifras correctas. Almgren et al. 2005 con exponente 3/5, Tóth 2011, Bucci 2019, Zarinelli 2015 y Kyle-Obizhaeva 2016 son citas reales. Pone Sato-Kanazawa en 2024 en vez de 2025: el preprint de arXiv es de 2024, así que es aceptable.

|A − B| = 0 ≤ 1: promedio 5.0, sin arbitraje.

### Defensa oral
No hubo repreguntas sobre esta pregunta; la defensa oral cubrió S7-01 a S7-04. Deducción: 0.

**Puntaje final: 5.0/5** (A 5.0, B 5.0; promedio 5.0; deducción de la defensa 0.0).

### Hueco
Ninguno. En la base solo está el principio de medir el IS contra el precio de decisión (01:333); el modelo y las cifras son cálculo propio.

**Detalle sin costo:** fecha Sato-Kanazawa 2024 (preprint), frente a 2025 (PRL 135: 257401) en la clave. La lista de evidencia a favor del exponente 1/2 salió de memoria y está marcada.

---

## S7-09 — Derivados: P&L de la cobertura delta, gamma-theta y prima de riesgo de volatilidad (calculo)

### Enunciado
Un trader compra 500 contratos (multiplicador 100, es decir 50,000 opciones) de calls europeas ATM con S = K = 100, T = 0.25 años, r = q = 0, volatilidad implícita σ_i = 20%, y cubre en delta usando la volatilidad implícita.

(a) Calcule precio Black-Scholes, delta y gamma por opción.

(b) Usando Itô y la EDP de Black-Scholes, derive que el P&L instantáneo de la posición cubierta es ½ΓS²(σ_r² − σ_i²)dt, identificando el theta. Calcule el movimiento diario de equilibrio (dt = 1/252) en dólares y en %.

(c) En un día el subyacente sube a 101.80 sin cambio en la volatilidad implícita. Calcule el P&L aproximado gamma-theta de la posición total (RESULTADO NUMÉRICO PRINCIPAL, en USD) y, como verificación, el P&L exacto por revaluación Black-Scholes. ¿A qué volatilidad realizada anualizada equivale ese movimiento?

(d) Si durante el resto de la vida la volatilidad realizada fuera 16% constante y el trader cubriera con la volatilidad realizada en vez de la implícita, ¿cuál sería el P&L total y por qué es determinista? ¿Por qué el P&L depende de la trayectoria cuando se cubre con σ_i?

(e) Relacione con la prima de riesgo de volatilidad y su evidencia empírica.

### Clave (texto descifrado, idéntico al de `clave.json`)
(a) d1 = (0 + ½·0.04·0.25)/(0.2·0.5) = 0.05; C = 3.9878; Δ = N(0.05) = 0.5199; Γ = φ(0.05)/(S σ √T) = 0.39844/10 = 0.039844.

(b) Cartera Π = C − ΔS. dC = Θdt + ΔdS + ½Γ(dS)², con (dS)² = σ_r²S²dt ⇒ dΠ = (Θ + ½ΓS²σ_r²)dt. La EDP con r = 0 da Θ = −½ΓS²σ_i² ⇒ dΠ = ½ΓS²(σ_r² − σ_i²)dt. Equilibrio: |ΔS| = σ_i S √dt = 0.20×100/√252 = $1.26 (1.26%).

(c) Por opción: gamma ½Γ(1.8)² = 0.064548; theta ½ΓS²σ_i²dt = 0.031623; neto 0.032925 × 50,000 = $1,646. Revaluación exacta (S = 101.8, T − 1/252): $1,614 (diferencia por términos de orden superior y cambio de gamma/theta). Volatilidad realizada equivalente: 1.8% × √252 = 28.6%.

(d) Cubriendo con σ_r (supuesta conocida y constante), el P&L es determinista: C(σ_r) − C(σ_i) = 3.1907 − 3.9878 = −0.7971 por opción ⇒ ≈ −$39,854 (se pagó una vol de 20% por una de 16%). Cubriendo con σ_i, el P&L = ∫½Γ_i S_t²(σ_r² − σ_i²)dt depende de la trayectoria: los movimientos cuentan ponderados por la gamma en dólares, grande cerca del strike y del vencimiento; mismo signo esperado pero magnitud aleatoria.

(e) En promedio la vol implícita supera a la realizada: Bakshi y Kapadia (2003) documentan ganancias de cobertura delta negativas en opciones del índice (prima de riesgo de volatilidad negativa); Carr y Wu (2009) sintetizan tasas de variance swap y hallan primas de riesgo de varianza fuertemente negativas para el S&P 500. Ser largo en gamma cubierta pierde en promedio y gana en crisis (cobertura contra caídas/saltos); el día del ejemplo es un resultado favorable, no una expectativa.

**Valor numérico principal comprometido:** 1646.27 ± 40.

**Rúbrica:** 5 puntos. (a) 0.75 pts: C, Δ, Γ correctos. (b) 1.25 pts: derivación con theta de la EDP (0.75), equilibrio $1.26 / 1.26% (0.5). (c) 1.5 pts: P&L ≈ $1,646 (1.0; tolerancia ±$40, se acepta $1,614 por revaluación exacta), verificación y vol equivalente 28.6% (0.5). (d) 1 pt: ≈ −$39,854 con argumento de determinismo (0.5), dependencia de trayectoria por ponderación de gamma en dólares (0.5). (e) 0.5 pts: signo de la prima de riesgo de volatilidad con al menos una referencia correcta.

### Fuente
Black, F., Scholes, M. (1973), JPE; Carr, P., Madan, D. (1998), 'Towards a Theory of Volatility Trading'; Ahmad, R., Wilmott, P. (2005), 'Which Free Lunch Would You Like Today, Sir?', Wilmott Magazine; Bakshi, G., Kapadia, N. (2003), 'Delta-Hedged Gains and the Negative Market Volatility Risk Premium', Review of Financial Studies 16(2): 527–566; Carr, P., Wu, L. (2009), 'Variance Risk Premiums', Review of Financial Studies 22(3): 1311–1341. Cálculos verificados con python3 (scipy).

### Respuesta del sustentante (completa)
(a) d1 = (0 + ½·0.04·0.25)/(0.2·0.5) = 0.05 y d2 = −0.05.

- C = 100[N(0.05) − N(−0.05)] = 3.9878.
- Δ = N(0.05) = 0.51994.
- Γ = φ(0.05)/(S σ √T) = 0.398444/10 = 0.039844.

La cobertura es ≈25,997 acciones cortas para 50,000 opciones.

(b) Derivación. Por Itô, dV = θdt + ΔdS + ½Γ(dS)², con (dS)² = σr²S²dt. La cartera cubierta V − ΔS gana dΠ = θdt + ½ΓS²σr²dt. La EDP de BS con r = 0 es θ + ½σi²S²Γ = 0, así que θ = −½σi²S²Γ, y por tanto dΠ = ½ΓS²(σr² − σi²)dt (repo 05:§2.3).

- θ = −7.969 por año por opción, o −0.03162 por día. Para la posición: −$1,581.13 al día.
- Movimiento de equilibrio: |ΔS|/S = σi√dt = 0.2/√252 = 1.260%, o sea $1.26 por día.

(c) Con ΔS = 1.80:

- Por opción: ½Γ(1.8²) − ½ΓS²σi²/252 = 0.019922 × (3.24 − 1.5873) = 0.032925.
- Posición: gamma +$3,227.40 y theta −$1,581.13, total ≈ +$1,646.27 (RESULTADO PRINCIPAL).
- Revaluación exacta con BS: C(101.80, T − 1/252) = 4.95593. El P&L es 4.95593 − 3.98776 − 0.51994 × 1.8 = 0.032280 por opción, o sea +$1,614.01. La diferencia de −$32 viene de términos de orden superior (speed, charm).
- Volatilidad realizada equivalente: 1.8% × √252 = 28.57% (con log, 28.32%).

(d) Si σr = 16% constante y la cobertura usa Δ(16%), la cartera replica exactamente el pago con costo C(16%) = 3.19069. El P&L total es (3.19069 − 3.98776) × 50,000 = −$39,854, igual a vega × (−4 pts) ≈ −$39,844.

Es determinista porque la réplica con la volatilidad verdadera elimina todo riesgo: solo cambia el P&L intermedio a mercado.

Si se cubre con σi, el P&L = ∫½Γ_i S²(σr² − σi²)dt depende del dollar gamma a lo largo de la trayectoria. Pesa mucho cuando S está cerca de K y el vencimiento se acerca. Con σr < σi siempre, el P&L es negativo en toda trayectoria, pero su magnitud depende del camino.

(e) Prima de riesgo de volatilidad. Quien compra gamma paga, en promedio, implícita > realizada:

- Bakshi-Kapadia (2003): las ganancias cubiertas en delta son negativas.
- Coval-Shumway (2001): los straddles ATM pierden ≈3% por semana.
- Carr-Wu (2009): VRP medida con swaps sintéticos.
- Cálculo propio del repo: VIX − RV futura = +4.10 pts en promedio y VIX > RV en el 85.9% de los días de 1990-2026 (05:§2.5).

La prima se comprimió: los alfas son ≈0 en los últimos 15 años (Dew-Becker y Giglio 2025). Tiene sesgo negativo, con pérdidas raras pero enormes (feb-2018, feb-2020; 05:§5.5). Este trader largo en gamma gana en días como el de (c) y paga theta en los tranquilos.

### Calificación automática
**Dentro de tolerancia:** esperado 1646.27, obtenido 1646.27, tolerancia ±40 (|diferencia| = 0).

### Calificación
**Calificador A: 5.0/5.** (a) C = 3.9878, Δ = 0.51994 y Γ = 0.039844. (b) La derivación con el theta de la EDP es correcta; equilibrio $1.26 (1.26%). (c) P&L gamma-theta de $1,646.27 y revaluación exacta de $1,614.01, con la diferencia explicada; volatilidad equivalente 28.57%. (d) −$39,854, con el argumento de réplica determinista y la dependencia de trayectoria por el dollar gamma. (e) Signo de la VRP con Bakshi-Kapadia, Coval-Shumway y Carr-Wu, todos correctos. Todo coincide con la clave.

**Calificador B: 5.0/5.** (a) 0.75/0.75. C = 3.9878, Δ = 0.51994, Γ = 0.039844. (b) 1.25/1.25. Derivación por Itô con θ tomado de la EDP y equilibrio de $1.26 / 1.26%. (c) 1.5/1.5. P&L gamma-theta de $1,646.27, revaluación exacta de $1,614.01 atribuyendo la diferencia a términos de orden superior, y volatilidad equivalente de 28.57%. (d) 1/1. −$39,854 con el argumento correcto de determinismo (réplica con la volatilidad verdadera) y chequeo por vega. Explica bien la dependencia de trayectoria a través del dollar gamma. (e) 0.5/0.5. Signo correcto de la VRP con Bakshi-Kapadia, Coval-Shumway (≈3% semanal) y Carr-Wu. Dew-Becker y Giglio 2025 está en el repo y es real.

|A − B| = 0 ≤ 1: promedio 5.0, sin arbitraje.

### Defensa oral
No hubo repreguntas sobre esta pregunta; la defensa oral cubrió S7-01 a S7-04. Deducción: 0.

**Puntaje final: 5.0/5** (A 5.0, B 5.0; promedio 5.0; deducción de la defensa 0.0).

### Hueco
Ninguno. Todo coincide con la clave. Agrega el chequeo por vega (−$39,844) y la compresión reciente de la prima de riesgo de volatilidad (Dew-Becker y Giglio 2025, en la base).

---

## S7-10 — Derivados: variance swaps, replicación estática, efecto del skew y convexidad (derivacion)

### Enunciado
(a) En un modelo de difusión continua sin saltos con r = 0, derive que la varianza realizada integrada satisface ∫_0^T σ_t² dt = 2[∫_0^T dS_t/S_t − ln(S_T/S_0)] y que el strike justo de un variance swap es K_var = (2/T)[∫_0^F P(K)/K² dK + ∫_F^∞ C(K)/K² dK], con F el forward. Explique el papel de la ponderación 1/K².

(b) Suponga un skew lineal en el strike Σ(K) = Σ0 − b(K − F)/F con Σ0 = 20%, b = 0.30 y T = 0.25. Use la aproximación de Demeterfi, Derman, Kamal y Zou (1999) para K_var y exprese el strike en puntos de volatilidad.

(c) Un inversionista es largo en un variance swap con vega notional de $100,000 y strike 21 (puntos de volatilidad); la volatilidad realizada resulta 16. Calcule el nocional de varianza y el P&L (RESULTADO NUMÉRICO PRINCIPAL, en USD). Compárelo con un volatility swap con el mismo vega notional y strike, y explique la convexidad y su implicación para el strike justo del volatility swap.

(d) ¿Qué falla en la replicación con saltos y con monitoreo discreto o caps? ¿Qué implica esto para medir la prima de riesgo de varianza?

### Clave (texto descifrado, idéntico al de `clave.json`)
(a) Itô: d ln S = dS/S − ½σ²dt ⇒ ∫σ²dt = 2∫dS/S − 2ln(S_T/S_0). El primer término se replica con una posición dinámica de 1/S_t unidades del subyacente (valor esperado Q nulo con r = 0). El contrato log se replica estáticamente (Carr-Madan): para f(S) = −ln(S/F), f(S_T) = −(S_T − F)/F + ∫_0^F (K − S_T)^+/K² dK + ∫_F^∞ (S_T − K)^+/K² dK. Tomando E^Q con S_0 = F: K_var = (2/T)E^Q[−ln(S_T/F)] = (2/T)[∫_0^F P/K² dK + ∫_F^∞ C/K² dK]. Con pesos 1/K² la gamma en dólares del portafolio (½S²·∂²V/∂S²) es constante, así que la exposición a varianza no depende del nivel de S; las puts de strikes bajos pesan más, por eso el skew eleva K_var.

(b) K_var ≈ Σ0²(1 + 3Tb²) = 0.04 × (1 + 3·0.25·0.09) = 0.04 × 1.0675 = 0.0427 ⇒ √ = 20.66 puntos de vol (la integración numérica exacta con ese skew da ≈ 20.67). El ajuste crece con T y con el cuadrado de la pendiente.

(c) Nocional de varianza = 100,000/(2×21) = 2,380.95 USD por punto de varianza. P&L = 2,380.95 × (16² − 21²) = 2,380.95 × (−185) = −$440,476. Volatility swap: 100,000 × (16 − 21) = −$500,000. P&L_var = N_vega(σ − K)(σ + K)/(2K): con σ < K pierde menos y con σ > K gana más que el volatility swap ⇒ el largo en varianza es largo en convexidad (volatilidad de la volatilidad), por lo que el strike justo del volatility swap es menor que √K_var (ajuste por convexidad ≈ Var(σ)/(8·σ̄³) en términos de varianza).

(d) Con saltos: −ln(S_T/S_0) = −∫dS/S + ½∫σ²dt + Σ(e^J − 1 − J), mientras que la variación cuadrática es QV = ∫σ²dt + ΣJ². Entonces (2/T)E^Q[−ln] − E^Q[QV]/T = (2/T)E^Q[Σ(e^J − 1 − J − J²/2)] ≈ E[ΣJ³]/(3T): con saltos negativos la tasa replicada con opciones queda por debajo del valor esperado de la varianza realizada y la cobertura falla en crisis (error de tercer orden, Carr-Wu 2009). El monitoreo discreto añade sesgo y error de cobertura (Broadie-Jain 2008); los caps (típicamente 2.5× el strike en acciones individuales) truncan la cola y el swap con cap vale menos. Prima de riesgo de varianza = RV − SW (Carr-Wu 2009): fuertemente negativa para el S&P 500; vender varianza cobra esa prima pero asume riesgo de salto y crisis (2008, feb-2018, mar-2020).

**Valor numérico principal comprometido:** -440476.19 ± 500.

**Rúbrica:** 5 puntos. (a) 1.5 pts: Itô y descomposición (0.5), replicación del contrato log con fórmula de K_var (0.75), interpretación de 1/K² (gamma en dólares constante, peso del ala de puts) (0.25). (b) 1 pt: fórmula de DDKZ (0.5) y 20.66 puntos de vol (0.5; tolerancia ±0.05). (c) 1.5 pts: nocional de varianza 2,380.95 (0.5), P&L −$440,476 (0.5; tolerancia ±$500), comparación con −$500,000 y argumento de convexidad (0.5). (d) 1 pt: sesgo por saltos con signo correcto (0.5), monitoreo discreto/caps e implicación para la prima de riesgo de varianza (0.5).

### Fuente
Demeterfi, K., Derman, E., Kamal, M., Zou, J. (1999), 'More Than You Ever Wanted to Know About Volatility Swaps', Goldman Sachs Quantitative Strategies Research Notes (ec. 30–31; Journal of Derivatives 6(4)); Carr, P., Madan, D. (1998); Carr, P., Wu, L. (2009), Review of Financial Studies 22(3); Broadie, M., Jain, A. (2008), 'The Effect of Jumps and Discrete Sampling on Volatility and Variance Swaps', IJTAF. Aproximación verificada contra integración numérica en python3.

### Respuesta del sustentante (completa)
(a) Derivación. Por Itô, d ln S = dS/S − ½σ²dt, así que ∫σ²dt = 2[∫dS/S − ln(ST/S0)].

Con r = 0, bajo Q el término ∫dS/S es martingala de media 0. Por tanto K_var = (1/T)E^Q[∫σ²dt] = (2/T)E^Q[−ln(ST/F)], con F = S0.

Carr-Madan: para f dos veces diferenciable,

f(ST) = f(F) + f'(F)(ST − F) + ∫_0^F f''(K)(K − ST)⁺dK + ∫_F^∞ f''(K)(ST − K)⁺dK.

Con f = −ln se tiene f'' = 1/K². Tomando esperanzas, E[ST − F] = 0, y queda K_var = (2/T)[∫_0^F P(K)/K² dK + ∫_F^∞ C(K)/K² dK] (Demeterfi-Derman-Kamal-Zou 1999 y Britten-Jones-Neuberger 2000; repo 05:83-84).

Papel de 1/K²: con esos pesos, el dollar gamma de la franja (Σ w_K Γ_K S²) es constante e independiente de S. La cartera expone solo a la varianza, sin importar dónde esté el spot. También hace que los puts de strike bajo pesen más, así que el skew eleva K_var.

(b) Aproximación DDKZ para un skew lineal: K_var ≈ Σ0²(1 + 3Tb²) = 0.04 × (1 + 3·0.25·0.09) = 0.04 × 1.0675 = 0.0427, o sea √ = 20.66 puntos de volatilidad.

Verificación propia: integré numéricamente la franja con esa sonrisa y obtuve 0.042738, es decir 20.67. Con b = 0 recupero 0.0400.

(c) Variance swap:

- Nocional de varianza = vega notional/(2K) = 100,000/42 = 2,380.95 $ por punto de varianza.
- P&L = 2,380.95 × (16² − 21²) = 2,380.95 × (−185) = −$440,476.19 (RESULTADO PRINCIPAL).

Volatility swap con el mismo vega notional: 100,000 × (16 − 21) = −$500,000.

Convexidad: P&L_var = N_vega(σ − K) + N_vega(σ − K)²/(2K). La varianza pierde menos a la baja (−440k frente a −500k) y gana más al alza: con 26 serían +559.5k frente a +500k.

Implicación: por Jensen, E[σ] ≤ √E[σ²], así que el strike justo del vol swap es menor que √K_var. El ajuste de convexidad es ≈ Var(σ²)/(8K_var^{3/2}). El vol swap no se replica de forma estática y requiere un modelo de volatilidad de la volatilidad.

(d) Qué falla en la réplica:

- Saltos: 2[∫dS/S − ln(ST/S0)] = ∫σ²dt + Σ 2(J − ln(1+J)). Con x = ln(1+J), 2(eˣ − 1 − x) = x² + x³/3 + …, así que el contrato log se aleja de la varianza realizada en log-rendimientos en un término de tercer orden. Con saltos negativos, la franja subestima el strike del swap. Carr-Wu (2009) argumentan que el error es pequeño.
- Monitoreo discreto: la suma de rendimientos diarios al cuadrado no es la integral. Hay sesgo de convexidad y el tratamiento de la media es distinto.
- Caps (p. ej., 2.5× el strike): el swap con cap equivale a un swap largo más un call corto sobre la varianza realizada, así que el strike justo baja.
- Además, la franja truncada y los strikes discretos sesgan K_var hacia abajo.

Implicación para medir la VRP: VIX² − RV mezcla prima difusiva, prima de salto y errores de truncación y discretización, y depende de definiciones (21 días, 252 frente a 365). Conviene usar definiciones consistentes o cotizaciones reales de swaps (Dew-Becker et al. 2017, 05:87). La brecha del repo (+4.10 pts) es una cota bruta y no un P&L implementable (05:§2.5).

### Calificación automática
**Dentro de tolerancia:** esperado -440476.19, obtenido -440476.19, tolerancia ±500 (|diferencia| = 0).

### Calificación
**Calificador A: 5.0/5.** (a) Itô, la replicación Carr-Madan del contrato log, la fórmula de K_var y la interpretación de 1/K² (dollar gamma constante, más peso en puts) son correctas. (b) La fórmula DDKZ da 20.66 y la integración numérica 20.67. (c) Nocional de 2,380.95, P&L de −$440,476.19 y vol swap de −$500,000; la descomposición de la convexidad y el ajuste Var(V)/(8K^{3/2}) son correctos (la forma estándar). (d) Término de salto de tercer orden con el signo correcto (los saltos negativos hacen que la franja subestime), más monitoreo discreto, caps, truncamiento y su implicación para medir la VRP. Completo.

**Calificador B: 5.0/5.** (a) 1.5/1.5. Itô, replicación de Carr-Madan con f'' = 1/K² y la fórmula de K_var. Interpreta bien 1/K² como dollar gamma constante y mayor peso de las puts. (b) 1/1. Fórmula DDKZ y 20.66, verificado contra la integración numérica (20.67). (c) 1.5/1.5. Nocional 2,380.95, P&L −$440,476.19 frente a −$500,000. Descompone la convexidad en un término cuadrático, da el ejemplo con 26 y aplica Jensen para el strike del vol swap con el ajuste Var(σ²)/(8K^{3/2}) estándar de DDKZ. (d) 1/1. El término de tercer orden por saltos tiene el signo correcto (con saltos negativos la franja subestima el strike). Trata monitoreo discreto, caps como call corto sobre la varianza y truncación, y la implicación para medir la VRP.

|A − B| = 0 ≤ 1: promedio 5.0, sin arbitraje.

### Defensa oral
No hubo repreguntas sobre esta pregunta; la defensa oral cubrió S7-01 a S7-04. Deducción: 0.

**Puntaje final: 5.0/5** (A 5.0, B 5.0; promedio 5.0; deducción de la defensa 0.0).

### Hueco
Ninguno.

**Nota sobre la clave.** La clave escribe el ajuste de convexidad del volatility swap como "≈ Var(σ)/(8·σ̄³) en términos de varianza". La forma estándar de DDKZ es Var(V)/(8·E[V]^{3/2}) con V = σ², que es la que dio el sustentante y la que aceptaron los dos calificadores. La clave no se corrige porque está comprometida, pero su notación es ambigua en ese punto (Var(σ) debería leerse como la varianza de la varianza).

---

## S7-11 — Derivados: cálculo tipo VIX a partir de una tira de opciones y estructura temporal del VIX (laboratorio)

### Enunciado
Datos crudos (índice estilizado): opciones europeas con vencimiento exactamente a 30 días (T = 30/365), tasa r = 0 (e^{rT} = 1). Cotizaciones medias (todas con bid > 0 salvo lo indicado):

Strike: 80 | 85 | 90 | 95 | 100 | 105 | 110 | 115 | 120

Put (mid): 0.01 | 0.03 | 0.10 | 0.39 | 1.48 | 4.32 | 8.82 | 13.80 | 18.80

Call (mid): 21.21 | 16.23 | 11.30 | 6.59 | 2.68 | 0.52 | 0.02 | bid 0.00/ask 0.05 | bid 0.00/ask 0.05

(a) Determine el forward F con la regla de Cboe (strike con mínima |C − P|) y el strike K0.

(b) Seleccione las opciones que entran al cálculo según la metodología de Cboe (incluida la regla de bids en cero) y defina Q(K_i) y ΔK_i.

(c) Calcule σ² = (2/T) Σ_i (ΔK_i/K_i²) e^{rT} Q(K_i) − (1/T)(F/K0 − 1)² y el índice = 100·√σ². RESULTADO NUMÉRICO PRINCIPAL: el índice con 2 decimales.

(d) Cuantifique dos errores comunes: omitir el término de corrección (F/K0 − 1)² e incluir las calls con bid cero a su precio medio (0.025).

(e) Explique en qué difiere el VIX real (vencimientos usados, precisión temporal, interpolación), por qué VIX² no es exactamente la tasa del variance swap a 30 días, y qué dicen la estructura temporal (contango/backwardation) y la evidencia sobre los retornos de futuros del VIX.

### Clave (texto descifrado, idéntico al de `clave.json`)
(a) La mínima |C − P| está en K = 100: |2.68 − 1.48| = 1.20 (en 105 es 3.80). F = K + e^{rT}(C − P) = 100 + 1.20 = 101.20. K0 = primer strike ≤ F = 100.

(b) Puts OTM con K < K0: 80, 85, 90, 95; en K0: Q = (1.48 + 2.68)/2 = 2.08; calls OTM con K > K0: 105 y 110. Las calls de 115 y 120 tienen bid cero en strikes consecutivos ⇒ se detiene la selección y se excluyen. ΔK_i = (K_{i+1} − K_{i−1})/2 = 5 en el interior; en los extremos, la diferencia con el strike adyacente = 5.

(c) Contribuciones ΔK·Q/K²: 80: 7.81e-6; 85: 2.076e-5; 90: 6.173e-5; 95: 2.1607e-4; 100: 1.040e-3; 105: 2.3583e-4; 110: 8.26e-6. Suma = 0.00159046. (2/T) = 24.3333 ⇒ 0.0387012. Corrección: (1/T)(0.012)² = 12.1667 × 0.000144 = 0.001752. σ² = 0.0369492 ⇒ índice = 100√0.0369492 = 19.22.

(d) Sin corrección: 100√0.0387012 = 19.67 (sesgo +0.45 puntos). Incluyendo las calls con bid cero a 0.025: 19.34 (+0.11).

(e) El VIX real usa opciones SPX estándar y semanales de dos vencimientos (cercano y siguiente) con más de 23 y menos de 37 días, mide el tiempo en minutos (año de 525,600 minutos) e interpola linealmente en varianza total para obtener 30 días constantes. VIX² aproxima la tasa del variance swap a 30 días, pero difiere por discretización y truncamiento de strikes (sesgo a la baja por colas no observadas) y por saltos (el contrato log no replica la variación cuadrática con saltos; error de tercer orden, Carr-Wu 2009). Estructura temporal: en calma suele haber contango (VIX3M > VIX; futuros por encima del spot) por la prima de riesgo de varianza y la reversión a la media; en crisis se invierte (backwardation), señal de estrés de corto plazo. Los futuros convergen al VIX en el vencimiento (liquidación por SOQ), pero no son E^P[VIX futuro]: incorporan prima de riesgo. Evidencia: una cartera de futuros VIX a 1 mes de vencimiento constante pierde ≈30% anual en 2006–2013 (Eraker y Wu 2017, JFE); ser largo en volatilidad es cobertura cara.

**Valor numérico principal comprometido:** 19.22 ± 0.05.

**Rúbrica:** 5 puntos. (a) 0.75 pts: F = 101.20 y K0 = 100. (b) 0.75 pts: selección correcta, Q(K0) = 2.08, exclusión de calls con bid cero y ΔK. (c) 2 pts: suma correcta (0.75), término de corrección (0.5), índice 19.22 (0.75; tolerancia ±0.05). (d) 0.5 pts: 19.67 y 19.34. (e) 1 pt: metodología real (23–37 días, minutos, interpolación) (0.35), diferencias VIX² vs variance swap (0.3), estructura temporal y evidencia de retornos de futuros VIX (0.35).

### Fuente
Cboe Global Markets, 'Volatility Index Methodology: Cboe Volatility Index' y VIX White Paper; Carr, P., Wu, L. (2009), Review of Financial Studies 22(3); Jiang, G., Tian, Y. (2007), 'Extracting Model-Free Volatility from Option Prices: An Examination of the VIX Index', Journal of Derivatives 14(3); Eraker, B., Wu, Y. (2017), 'Explaining the Negative Returns to Volatility Claims: An Equilibrium Approach', Journal of Financial Economics 125(1): 72–98. Cálculo verificado con python3.

### Respuesta del sustentante (completa)
Todo se calculó con código propio a partir de las cotizaciones del enunciado.

(a) C − P por strike: 21.20, 16.20, 11.20, 6.20, 1.20, −3.80, −8.80, −13.775, −18.775. El mínimo de |C − P| está en 100. F = 100 + e^{rT}(1.20) = 101.20, y K0 = el strike inmediatamente debajo de F = 100.

(b) Selección de Cboe:

- Puts OTM con K < K0, bajando desde 95: 95, 90, 85 y 80, todos con bid > 0.
- Calls OTM con K > K0: 105 y 110. En 115 y 120 hay dos bids en cero consecutivos, así que se detiene y se excluyen ambos.
- En K0: Q = (1.48 + 2.68)/2 = 2.08.
- Q(K_i) es el mid de la opción OTM. ΔK_i = (K_{i+1} − K_{i−1})/2 = 5 en los strikes interiores. En los extremos (80 y 110) es la diferencia con el strike adyacente, también 5.

(c) T = 30/365 = 0.082192. Aportes (2/T)·ΔK/K²·Q:

- 80: 0.00019
- 85: 0.00051
- 90: 0.00150
- 95: 0.00526
- 100: 0.02531 (65% del total)
- 105: 0.00574
- 110: 0.00020

Suma = 0.038701. Corrección: (1/T)(1.012 − 1)² = 0.001752. σ² = 0.036949. Índice = 100√σ² = 19.22 (RESULTADO PRINCIPAL).

(d) Dos errores comunes:

- Omitir la corrección: √0.038701 = 19.67, +0.45 pts.
- Incluir los calls de 115 y 120 a 0.025: σ² = 0.037390, índice 19.34, +0.11 pts.

(e) Diferencias con el VIX real (de memoria salvo lo citado):

- Usa opciones SPX estándar y semanales de dos vencimientos, cercano y siguiente, con más de 23 y menos de 37 días.
- Mide T en minutos hasta la liquidación (AM o PM).
- Toma r de la curva de Treasuries CMT con spline.
- Calcula σ1² y σ2² por separado e interpola linealmente la varianza total a 30 días (43,200 minutos): VIX = 100√{[T1σ1²(N_T2 − N30)/(N_T2 − N_T1) + T2σ2²(N30 − N_T1)/(N_T2 − N_T1)]·N365/N30}.

VIX² no es exactamente la tasa del variance swap a 30 días (repo 05:84: 'en esencia'):

- truncación del rango y strikes discretos, ambos hacia abajo;
- saltos: término de tercer orden (ver S7-10d);
- quotes a mid y la aproximación de K0;
- el swap liquida sobre log-rendimientos diarios al cuadrado, a veces con caps.

Para los futuros, E[√V] < √E[V], así que el futuro de VIX es menor que la raíz de la varianza forward.

Estructura temporal y futuros (repo 05:§2.6):

- Lo normal es contango: VIX3M > VIX en 87.7% de los cierres mensuales de 2006-08 a 2026-09. La curva invertida (≈12%) marca estrés (05:R6).
- Los futuros pierden en promedio: Eraker-Wu (2017) ≈ −30% anual en 2006-13; Whaley (2013) ≈ US$4 mil millones perdidos por los ETPs; VXX −99% de 2018 a 2026 (cálculo del repo).
- Simon-Campasano (2014): la base predice el rendimiento del futuro, no el VIX. Es la prima de riesgo que se cosecha.

### Calificación automática
**Dentro de tolerancia:** esperado 19.22, obtenido 19.22, tolerancia ±0.05 (|diferencia| = 0).

### Calificación
**Calificador A: 5.0/5.** (a) F = 101.20 y K0 = 100. (b) La selección es correcta: excluye 115 y 120 por los dos bids en cero consecutivos, Q(K0) = 2.08 y ΔK = 5. (c) Suma 0.038701 (después del factor 2/T), corrección 0.001752 e índice 19.22. (d) 19.67 y 19.34. (e) Metodología real: 23-37 días, minutos, CMT con spline y la fórmula de interpolación. VIX² frente a variance swap: truncamiento, saltos y discretización. Estructura temporal en contango y retornos de futuros (Eraker-Wu ≈ −30%, Whaley, Simon-Campasano). Completo.

**Calificador B: 5.0/5.** (a) 0.75/0.75. F = 101.20 y K0 = 100. (b) 0.75/0.75. Selección correcta, Q(K0) = 2.08, exclusión por dos bids en cero consecutivos y ΔK. (c) 2/2. Suma equivalente (0.038701 ya multiplicada por 2/T), corrección de 0.001752 e índice 19.22. (d) 0.5/0.5. 19.67 (+0.45) y 19.34 (+0.11). (e) 1/1. Metodología real correcta: dos vencimientos de 23 a 37 días, minutos, CMT con spline y la fórmula de interpolación. Da las diferencias de VIX² frente al variance swap (truncación, saltos, discretización) y la desigualdad de Jensen para los futuros. Sobre la estructura temporal: contango normal, Eraker-Wu −30%, Whaley 2013 y Simon-Campasano 2014, todas referencias reales.

|A − B| = 0 ≤ 1: promedio 5.0, sin arbitraje.

### Defensa oral
No hubo repreguntas sobre esta pregunta; la defensa oral cubrió S7-01 a S7-04. Deducción: 0.

**Puntaje final: 5.0/5** (A 5.0, B 5.0; promedio 5.0; deducción de la defensa 0.0).

### Hueco
Ninguno. Todo el cálculo coincide con la clave. En (e) agrega datos propios de la base (contango en 87.7% de los cierres mensuales de 2006-2026; VXX −99% de 2018 a 2026) y la metodología real (CMT y minutos), marcada como de memoria.

---

## S7-12 — Derivados: gamma de dealers, opciones 0DTE y flujos de re-cobertura (caso)

### Enunciado
Un índice cotiza en 6,000. A las 14:00 quedan 2 de las 6.5 horas de la sesión (use T = 2/(6.5×252) años). Los creadores de mercado de opciones (OMM) están netamente cortos en 20,000 contratos de calls 0DTE con strike 6,000 (multiplicador 100), cubiertos en delta. Volatilidad implícita 15%, r = q = 0; use Black-Scholes.

(a) Calcule delta y gamma por opción y la 'exposición gamma' en dólares por un movimiento de 1% (Γ·n·m·S²·0.01), con su signo para los OMM.

(b) Ocurre un salto instantáneo de +1% (S = 6,060) sin cambio en volatilidad ni en tiempo. Calcule el flujo de re-cobertura requerido con el delta exacto: unidades del índice y nocional en miles de millones de USD valuado a 6,060 (RESULTADO NUMÉRICO PRINCIPAL). Compárelo con la aproximación lineal en gamma y explique la diferencia.

(c) ¿En qué dirección va el flujo y por qué es desestabilizador? ¿Cuánto es un movimiento de una desviación estándar en las 2 horas restantes?

(d) Resuma la evidencia empírica publicada entre 2021 y 2025 sobre si la gamma de los OMM (incluidas las 0DTE) amplifica o atenúa la volatilidad del índice (al menos tres estudios con cifras) y la participación de las 0DTE en el volumen de opciones SPX en 2025.

(e) Critique las métricas públicas de 'GEX' construidas con interés abierto.

### Clave (texto descifrado, idéntico al de `clave.json`)
(a) σ√T = 0.15 × √0.0012210 = 0.0052414; d1 = ½σ√T = 0.00262 ⇒ Δ = 0.5010; Γ = φ(d1)/(Sσ√T) = 0.39894/31.45 = 0.012686 por punto por opción. Exposición: 0.012686 × 2,000,000 × 6,000² × 0.01 = $9.13 mil millones por 1%; los OMM están cortos ⇒ −$9.13 mil millones (gamma negativa).

(b) A S = 6,060: d1 = ln(1.01)/0.0052414 + 0.00262 = 1.901 ⇒ Δ = 0.97135; cambio exacto 0.4703 por opción × 2,000,000 = 940,610 unidades del índice ⇒ nocional ≈ 940,610 × 6,060 = $5.70 mil millones (compra). Lineal: Γ × 60 = 0.761 por opción (imposible: desde 0.50 el delta de una call no puede subir más de 0.50) ⇒ 1.52 millones de unidades ≈ $9.1–9.2 mil millones, una sobreestimación de ~60%. Con horas al vencimiento la gamma es muy local y colapsa al quedar la opción dentro del dinero: se requiere revaluación completa o perfil de gamma sobre una rejilla de S.

(c) Los OMM cortos en calls (gamma negativa) deben comprar cuando el índice sube y vender cuando baja: retroalimentación positiva (procíclica). Movimiento de 1 desviación estándar en 2 horas: 6,000 × 0.0052414 = 31.4 puntos (0.52%); el 1% equivale a ≈1.9 desviaciones estándar.

(d) Ni, Pearson, Poteshman y White (2021, RFS): la volatilidad de las acciones se relaciona negativamente con las posiciones netas compradas de inversionistas que cubren (gamma positiva de los cubridores ⇒ menor volatilidad). Baltussen, Da, Lammers y Martens (2021, JFE): la demanda de cobertura de posiciones con gamma negativa genera momentum intradía al cierre. Adams, Fontaine y Ornthanalai (2024): la volatilidad del índice baja 60–90 pb anualizados en días con trading 0DTE (identificación: introducción de vencimientos SPXW de martes y jueves en abril/mayo de 2022); los OMM cubren la mayor parte del flujo 0DTE y la cobertura de posiciones de largo plazo que se vuelven 0DTE atenúa la volatilidad. Dim, Eraker y Vilkov (2024): no hallan que la gamma del interés abierto 0DTE aumente incondicionalmente la volatilidad; las 0DTE tienen la mayor prima de riesgo de volatilidad. Amaya, Garcia-Ares, Pearson y Vasquez (2025), con datos firmados de Cboe jul-2020 a jun-2023: la gamma agregada de los OMM suele ser positiva pero con frecuencia negativa; efecto medio −0.2 pp de volatilidad; efecto máximo +3.3 pp en la volatilidad diaria anualizada y +6.4 pp en la de 30 minutos. Brogaard, Han y Won (2024): la volatilidad se correlaciona con la participación de 0DTE. Participación: 0DTE ≈ 59% del volumen SPX en 2025 (ADV récord ≈2.3 millones de contratos), con récord mensual de 62.4% en agosto de 2025.

(e) El GEX público supone que los dealers están cortos en lo que compran los clientes (el signo real es desconocido sin datos firmados de apertura/cierre); el interés abierto del inicio del día no captura las 0DTE abiertas y cerradas intradía; ignora coberturas con futuros u otras opciones, vanna y charm (cambios de delta por vol y tiempo, dominantes cerca del vencimiento) y la no linealidad mostrada en (b); además supone que todos los OMM cubren mecánica y continuamente.

**Valor numérico principal comprometido:** 5.7 ± 0.1.

**Rúbrica:** 5 puntos. (a) 1 pt: Δ ≈ 0.501, Γ ≈ 0.01269 (0.5); exposición −$9.13 mil millones con signo (0.5). (b) 1.5 pts: delta exacto 0.9714 y cambio 0.4703 (0.5); nocional $5.70 mil millones (0.5; tolerancia ±0.1); comparación con la lineal y explicación de su falla (0.5). (c) 0.5 pts: dirección procíclica y 31.4 puntos. (d) 1.5 pts: tres estudios con hallazgo y cifra correctos (0.4 c/u = 1.2), participación 0DTE ≈59% en 2025 (0.3); penalizar −0.5 si se afirma sin matices que las 0DTE aumentan sistemáticamente la volatilidad. (e) 0.5 pts: al menos dos críticas válidas.

### Fuente
Ni, S., Pearson, N., Poteshman, A., White, J. (2021), 'Does Option Trading Have a Pervasive Impact on Underlying Stock Prices?', Review of Financial Studies 34(4): 1952–1986; Baltussen, G., Da, Z., Lammers, S., Martens, M. (2021), 'Hedging Demand and Market Intraday Momentum', Journal of Financial Economics 142(1); Adams, G., Fontaine, J.-S., Ornthanalai, C. (2024), 'The Market for 0DTE: The Role of Liquidity Providers in Volatility Attenuation', SSRN 4881008; Dim, C., Eraker, B., Vilkov, G. (2024), '0DTEs: Trading, Gamma Risk and Volatility Propagation', SSRN 4692190; Amaya, D., Garcia-Ares, P., Pearson, N., Vasquez, A. (2025), '0DTE Index Options and Market Volatility: How Large is Their Impact?' (Cboe research); Cboe Global Markets, reportes de volumen 2025 (0DTE 59% del volumen SPX; 62.4% en agosto de 2025). Cálculos verificados con python3 (scipy).

### Respuesta del sustentante (completa)
Cálculo propio con Black-Scholes.

(a) T = 2/1638 = 0.0012210 años; σ√T = 0.0052414; d1 = ½σ√T = 0.00262.

- Δ = 0.50105.
- Γ = φ(d1)/(Sσ√T) = 0.398941/31.449 = 0.012686 por punto del índice.
- Exposición gamma = Γ·n·m·S²·0.01 = 0.012686 × 20,000 × 100 × 6000² × 0.01 = $9.13 mil millones por movimiento de 1%.

Para los OMM, que están cortos en calls y por tanto cortos en gamma, el signo es negativo (−$9.13 mil millones). Por cada +1% su delta cae en ese monto y deben comprar.

(b) Con S = 6060: d1 = [ln(1.01) + ½σ²T]/σ√T = 1.9010, así que Δ = 0.97135 y ΔΔ = 0.47030.

- Re-cobertura: 0.47030 × 20,000 × 100 = 940,610 unidades del índice.
- Nocional: 940,610 × 6060 = $5.70 mil millones (RESULTADO PRINCIPAL), a compra.
- Aproximación lineal en gamma: 0.012686 × 60 × 2,000,000 = 1,522,261 unidades, o sea $9.22 mil millones a 6060 ($9.13 a 6000). Sobreestima 62%.

La diferencia se explica porque a 2 horas del vencimiento el delta es una curva en S muy empinada, de ancho ≈ σ√T·S = 31 puntos. Un movimiento de 60 puntos (1.9 DE) cruza casi toda la curva. El delta está acotado en 1, así que ΔΔ ≤ 0.499, y la gamma cae a 16% de su valor inicial (0.00206). La aproximación lineal ignora ese 'speed' negativo.

(c) El flujo va en la dirección del movimiento: los OMM compran cuando sube y venden cuando baja. Es desestabilizador porque es retroalimentación positiva, como en el momentum intradía, y más fuerte cerca del strike y del cierre, cuando la gamma 0DTE se concentra.

Una DE en las 2 horas restantes es σ√T·S = 0.524%, unos 31.4 puntos. El salto de 1% equivale a 1.91 DE.

(d) Evidencia de 2021-2025 (repo 05:§2.7 y §4):

- Amplifican:
  - Baltussen, Da, Lammers y Martens (2021, JFE): momentum intradía en más de 60 futuros, 1974-2020, ligado a la cobertura de gamma.
  - Brogaard, Han y Won (2023, WP): los 0DTE pasaron de 0.08 millones de contratos al mes (ene-2011) a 34.4 millones (ago-2023), 48% del volumen de opciones de índice. Una DE más de 0DTE eleva la volatilidad 9.10% sobre su media.
  - Barbon-Buraschi (2020, WP): la gamma negativa interactúa con la iliquidez.
- Atenúan:
  - Dim, Eraker y Vilkov (2024, WP): la gamma neta de los MM en 0DTE es positiva en promedio y se relaciona negativamente con la volatilidad intradía futura.
  - Adams, Dim, Eraker, Fontaine, Ornthanalai y Vilkov (2025, WP): los 0DTE amortiguan la volatilidad del mercado.
- De memoria, no está en el repo: Ni, Pearson, Poteshman y White (2021, RFS) encuentran menor |r| cuando los OMM están largos en gamma y mayor cuando están cortos.
- 2026 (repo): Elms no encuentra pinning; los días con más interés abierto ATM tienen rangos 16% más amplios.
- Balance del repo: grado C. La evidencia más reciente no apoya que los 0DTE desestabilicen en promedio.

Participación en 2025 (Cboe): los 0DTE fueron 2.3 de los 3.9 millones de contratos diarios del SPX (59%), con un récord de 62.4% en agosto de 2025. Además, más de 75% de las operaciones minoristas en SPX son 0DTE (Beckmeyer et al.).

(e) Críticas al GEX público construido con interés abierto:

1) Supone el signo de la posición del dealer (clientes largos en puts y cortos en calls). Sin datos de contraparte (Cboe Open-Close) el signo es desconocido. Con datos firmados, Dim-Eraker-Vilkov encuentran gamma positiva, lo contrario del supuesto habitual.
2) El interés abierto se publica una vez al día. No ve los 0DTE que se abren y cierran en la misma sesión, que son la mayoría.
3) Ignora spreads y estrategias de varias patas, y trata todo el OI como inventario del dealer.
4) Ignora que los dealers cubren gamma con otras opciones y futuros, y usan umbrales de rebalanceo.
5) Usa gamma BS con una sola volatilidad y omite vanna y charm, que dominan cerca del vencimiento.
6) Mezcla vencimientos y subyacentes (SPX, SPY, ES).
7) Tiene poca validación fuera de muestra. El repo no lo usa como señal: la evidencia es intradía, de grado B/C, y los datos no son públicos (05:R12).

### Calificación automática
**Dentro de tolerancia:** esperado 5.7, obtenido 5.7, tolerancia ±0.1 (|diferencia| = 0).

### Calificación
**Calificador A: 4.5/5.** (a) Δ = 0.50105, Γ = 0.012686 y −$9.13 mil millones con signo. (b) Δ exacto 0.97135, cambio 0.4703, nocional $5.70 mil millones; la comparación lineal (sobreestima 62%) está bien explicada por el delta acotado y el colapso de gamma. (c) Procíclico, 31.4 puntos y 1.91 DE. (d) Verifiqué con búsqueda web que Brogaard-Han-Won (9.10%, 48%) es correcto. Baltussen et al. y Dim-Eraker-Vilkov son correctos pero sin cifra de efecto. Ni et al. tiene la dirección correcta, sin cifra. Faltan Amaya et al. (2025) y la cifra de 60-90 pb de Adams-Fontaine-Ornthanalai. La participación de 59% y el récord de 62.4% son correctos, y el balance tiene matices adecuados. (e) Más de dos críticas válidas al GEX. Descuento por las cifras incompletas en (d).

**Calificador B: 4.5/5.** (a) 1/1. Δ = 0.50105, Γ = 0.012686 y −$9.13 mil millones con signo. (b) 1.5/1.5. Δ = 0.97135, ΔΔ = 0.4703 y $5.70 mil millones. La lineal de $9.22 mil millones es un 62% más alta, y explica bien que el delta está acotado y que la gamma cae al 16% (lo verifiqué: 0.00206). (c) 0.5/0.5. Flujo procíclico y 31.4 puntos (1.91 DE). (d) ≈1.2/1.5. Verifiqué que Brogaard-Han-Won (9.10% por DE, 34.4 millones de contratos en ago-2023) es correcto. Baltussen et al. 2021 tiene hallazgo correcto, pero la cifra es solo de muestra. Dim-Eraker-Vilkov, Ni et al. 2021 y Adams et al. 2025 (en el repo) tienen el hallazgo en la dirección correcta, pero sin cifras de efecto. Faltan Adams-Fontaine-Ornthanalai (60-90 pb) y Amaya et al. 2025 (+3.3/+6.4 pp), que dan las cifras clave. La participación de 59% y el récord de 62.4% son correctos. No aplica penalización, porque matiza que la evidencia reciente no apoya una desestabilización en promedio. (e) 0.5/0.5. Siete críticas válidas al GEX. Total ≈4.7, redondeado a 4.5.

|A − B| = 0 ≤ 1: promedio 4.5, sin arbitraje.

### Defensa oral
No hubo repreguntas sobre esta pregunta; la defensa oral cubrió S7-01 a S7-04. Deducción: 0.

**Puntaje final: 4.5/5** (A 4.5, B 4.5; promedio 4.5; deducción de la defensa 0.0).

### Hueco
**Faltó (−0.5):** en (d), las cifras de efecto de los estudios clave.

- Solo Brogaard-Han-Won trae una cifra de efecto (9.10% de la volatilidad por DE de participación 0DTE).
- Baltussen et al. trae solo cifras de la muestra.
- Dim-Eraker-Vilkov, Ni et al. y Adams et al. (2025) tienen la dirección correcta, sin magnitud.
- No citó a Adams-Fontaine-Ornthanalai: en días con 0DTE la volatilidad del índice es 60-90 pb anualizados menor, con identificación por la introducción de vencimientos de martes y jueves en 2022.
- No citó a Amaya-Garcia-Ares-Pearson-Vasquez (2025): efecto medio de −0.2 pp y efecto máximo de +3.3 pp diario y +6.4 pp a 30 minutos.

No hubo penalización por afirmar sin matices que las 0DTE desestabilizan: el balance es explícitamente matizado.

**Base:** el cap. 05 (§2.7 y §4) no guarda esas magnitudes.

**Acción:** agregarlas al cap. 05.

---

## Resumen de la sección S7

| Pregunta | Tema | Automática | A | B | \|A − B\| | Deducción (defensa) | Final | Hueco principal |
|---|---|---|---|---|---|---|---|---|
| S7-01 | Elastic net y resultados de GKX (2020) | dentro de tolerancia | 5.0 | 5.0 | 0 | 0.0 | 5.0 | — (magnitudes de GKX de memoria; no están en la base) |
| S7-02 | R²oos, benchmark y virtud de la complejidad | dentro de tolerancia | 4.0 | 4.5 | 0.5 | 0.0 | 4.25 | Sin la inflación de ≈3 pp de GKX; KMZ sin 0.47 ni t ≈ 3; Buncic sin cifra; sin Elmore-Strauss |
| S7-03 | CV purgada con embargo y CPCV | dentro de tolerancia | 5.0 | 5.0 | 0 | 0.0 | 5.0 | — |
| S7-04 | Fuga y memorización en LLMs | no aplica | 5.0 | 5.0 | 0 | 0.0 | 5.0 | — (Sarkar-Vafa no citado, no obligatorio) |
| S7-05 | Kyle (1985) e insiders en competencia | dentro de tolerancia | 5.0 | 5.0 | 0 | — | 5.0 | — (Amihud fechado 2001 por 2002, sin costo) |
| S7-06 | Glosten-Milgrom y PFOF | dentro de tolerancia | 5.0 | 5.0 | 0 | — | 5.0 | — |
| S7-07 | Estimador de Roll | dentro de tolerancia | 5.0 | 5.0 | 0 | — | 5.0 | — |
| S7-08 | Impacto de raíz cuadrada e IS | dentro de tolerancia | 5.0 | 5.0 | 0 | — | 5.0 | — (Sato-Kanazawa fechado 2024 por 2025, sin costo) |
| S7-09 | Cobertura delta y gamma-theta | dentro de tolerancia | 5.0 | 5.0 | 0 | — | 5.0 | — |
| S7-10 | Variance swaps y convexidad | dentro de tolerancia | 5.0 | 5.0 | 0 | — | 5.0 | — |
| S7-11 | Cálculo tipo VIX | dentro de tolerancia | 5.0 | 5.0 | 0 | — | 5.0 | — |
| S7-12 | Gamma de dealers y 0DTE | dentro de tolerancia | 4.5 | 4.5 | 0 | — | 4.5 | Sin cifras de Adams-Fontaine-Ornthanalai (60–90 pb) ni de Amaya et al. (+3.3/+6.4 pp) |
| **Total** | | 11/11 | **58.5** | **59.0** | | **0** | **58.75 / 60** | |

- **Total S7: 58.75 / 60 = 97.92%.**
- **Integridad de la clave:** verificada. La clave descifrada del commit `2a50ca2` reproduce las 13 huellas publicadas (la del archivo y las 12 por pregunta), y es exactamente la que usaron los calificadores, la calificación automática y el juez. Etiqueta: **con compromiso público previo, verificado**.
- **Arbitrajes:** ninguno. |A − B| = 0 en 10 preguntas y 0.5 en S7-02. En S7-02, A sumó ≈4.2 y lo dejó en 4; B sumó ≈4.35 y lo redondeó a 4.5. Los dos descuentan por los mismos faltantes.
- **Defensa oral:** 4 preguntas y 8 repreguntas, con deducción total de 0. La única imprecisión (S7-04: relectura errónea de su propio z ≈ 3.7, en dirección autocrítica) queda asentada y no cambia la nota.
- **Frente al umbral** (`PROTOCOLO.md` §1): 97.92% supera el mínimo de 85% por sección. El dictamen global depende de las demás secciones.
- **Lectura sin maquillaje:**
  - Se perdieron 1.25 puntos, todos en incisos de evidencia empírica reciente (2024-2025): 0.75 en S7-02 (KMZ y sus críticas de 2025) y 0.5 en S7-12 (magnitudes de los estudios de 0DTE).
  - En los dos casos la pérdida es por cifras ausentes o vagas, no por cifras erróneas. El sustentante marcó como "de memoria" o "sin verificar" lo que no estaba en la base, y no inventó datos.
  - La causa de fondo es la base: no guarda esas cifras.
  - En las 11 preguntas con resultado numérico, los 11 resultados quedaron dentro de tolerancia. En las preguntas de cálculo, derivación y laboratorio (S7-01, S7-03 y S7-05 a S7-11) no perdió nada.
  - La defensa oral confirmó que el dominio de S7-01 a S7-04 no era memorizado: respondió bien a extensiones que la clave no contemplaba.
  - Límites de esta calificación: calificadores y sustentante son el mismo modelo; el enunciado no tiene huella; y la defensa oral solo cubrió 4 de las 12 preguntas.
- **Acciones para la base:**
  1. Tabla 1 de GKX y su esquema de entrenamiento, validación y prueba (cap. 02 o 06).
  2. Cifras de KMZ (≈0.47 de mejora del Sharpe, t ≈ 3) y de las críticas de 2025: Nagel; Buncic (0.699 frente a 0.485); Elmore-Strauss (97.5%). También el hallazgo de GKX de que la media histórica infla el R² en ≈3 pp (cap. 02 o 20).
  3. Una nota de microestructura con Kyle, Glosten-Milgrom, Roll y la ley de raíz cuadrada, que hoy no están en la base.
  4. Magnitudes de la evidencia de 0DTE y gamma de los OMM: Adams-Fontaine-Ornthanalai 60-90 pb; Amaya et al. −0.2/+3.3/+6.4 pp; Ni et al.; Dim-Eraker-Vilkov (cap. 05 §2.7).
