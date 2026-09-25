# 33 · Solana Development Course (Cyfrin Updraft: Anchor y Rust nativo)

- **Estado:** estudiado. **Acceso:** sección. Revisé el temario completo y el texto de las lecciones conceptuales, y leí el código de los 4 retos de "Common Bugs" en el repositorio. No vi videos ni compilé.
- **Grupo:** G4. **Autor de la ficha:** `analista-cripto`, 25-sep-2026.
- **Etiquetas:** [H] hecho con fuente · [I] inferencia · [O] opinión.

## 1. Ficha

| Campo | Valor |
|---|---|
| Año | 2026. Anunciado a mediados de enero de 2026 ([Colosseum, 16-ene-2026](https://blog.colosseum.com/2026-hackathons-updraft-course-offline-signer-cli/)). Último commit del repositorio: 10-feb-2026. |
| Autor | Cyfrin Updraft. **No encontré en la página qué instructor lo imparte.** |
| Tipo | Curso en línea con lecciones escritas, videos y ejercicios en Rust (nativo y Anchor) |
| Nivel | La página dice "Beginner" y el índice del dueño, "Avanzado". [I] Para un inversionista es avanzado: exige Rust. |
| Duración | La página dice "1 h, 48 lecciones, 16 proyectos". [I] La "1 h" parece un error de la página, porque cada sección marca ~1 h y son 9. La nota de Colosseum habla de 31 lecciones y 16 proyectos. |
| Costo | Gratis |
| Idioma | Inglés, con subtítulos en "20+ idiomas" |
| URL | https://updraft.cyfrin.io/courses/solana · repositorio: https://github.com/Cyfrin/solana-course |
| Conflictos de interés | Como en la ficha 22: Cyfrin vende auditorías, también de Solana, y las secciones abren con mensajes de patrocinadores (Curve, Ankr, Rocket Pool, GMX). |

## 2. Acceso real (25-sep-2026)

**Página del curso:**
- temario de **9 secciones**: introducción, conceptos básicos, Hello Program, Oracle, Piggy Bank, Dutch Auction, AMM, CPI/IDL y Common Bugs;
- leí el texto de "Ethereum and Solana", "Accounts", "PDA", "CPI", "Program Limitations" y "Course Intro", además de los enunciados de los 4 retos de fallos comunes.

**Repositorio** `Cyfrin/solana-course`: `git clone --depth 1`, commit `76dc57a` del 10-feb-2026.
- Leí el código de `apps/ctf/{signer,auth,pda,rent}`: los ejercicios y el `diff` contra las soluciones.

**Referencia externa para juzgar la cobertura:** `coral-xyz/sealevel-attacks`, clonado (commit `24555d0`, 16-jul-2022). Trae 11 clases de ataque en Solana.

**No hice:**
- no vi videos;
- no compilé ni ejecuté los retos, porque no está instalada la herramienta de Solana (`cargo build-sbf`).

**Nivel: sección.**

## 3. Lo esencial

1. [H] **Estructura:** cada proyecto se hace **dos veces**, en Rust nativo y en Anchor. El curso enseña primero el nativo "para educar" y luego Anchor "para producir" ("Course Intro").
2. [H] **Modelo de Solana:**
   - **código y datos están separados**; "todos los datos en Solana se guardan en cuentas";
   - una cuenta tiene `lamports`, `data`, `owner` y `executable`;
   - una cuenta está exenta de renta si guarda SOL suficiente para pagar 2 años de almacenamiento ("Accounts").
3. [H] **PDA:** es una dirección **sin llave privada**, derivada del ID del programa, de semillas y de un "bump". Solo el programa que la deriva puede "firmar" por ella ("PDA").
4. [H] **CPI y extensión de privilegios:** si un programa llama a otro, **las cuentas conservan sus permisos** de firmante y de escritura ("CPI").
   - [I] Por eso llamar a un programa no confiable es peligroso.
5. [H] **Límites del programa:** determinismo; nada de `std::fs`, `std::net`, `std::thread` ni procesos ("Program Limitations").
6. [H] **Reto 1, falta verificar al firmante** (`apps/ctf/signer`):
   - `update` compara `oracle.owner == signer.key` pero **nunca revisa `signer.is_signer`**;
   - cualquiera puede pasar la llave pública del dueño sin firmar y cambiar el precio del oráculo.
7. [H] **Reto 2, falta verificar la autorización** (`apps/ctf/auth`):
   - revisa `is_signer` pero **no que el firmante sea el dueño**;
   - cualquier firmante cambia el precio.
8. [H] **Reto 3, falta verificar la PDA** (`apps/ctf/pda`):
   - `unlock` no comprueba que la cuenta recibida sea la PDA derivada del que llama;
   - la solución dice: "el llamador puede vaciar cualquier PDA de este programa".
9. [H] **Reto 4, falta limpiar la renta** (`apps/ctf/rent`):
   - `unlock` devuelve solo `lock_amt` y deja en la PDA los lamports de la renta;
   - `sweep` deja que **cualquier firmante** se lleve el excedente de la PDA de otro ("Any one can call to sweep excess SOL", comentario de la solución).
10. [I] **Hilo común:** en Solana **las cuentas son entradas del usuario**. El programa debe verificar cada una: firma, dueño, derivación, tipo y cierre. Es el equivalente a los fallos de control de acceso en EVM (fichas 22 y 25), y **dos de los cuatro retos atacan un oráculo de precios**.
11. [H] **Cobertura frente a la referencia:** `sealevel-attacks` lista 11 clases:
    - verificación de firmante;
    - coincidencia de datos de cuenta;
    - verificación de dueño;
    - "type cosplay";
    - inicialización;
    - CPI arbitraria;
    - cuentas mutables duplicadas;
    - canonicalización del bump;
    - PDA compartida;
    - cierre de cuentas;
    - dirección de sysvar.
    - [I] **El curso cubre directamente ~4**: firmante; autorización y dueño; derivación de la PDA; renta y cierre.
    - [I] No cubre: type cosplay, CPI arbitraria, cuentas duplicadas, canonicalización del bump, reinicialización ni sysvar. Es mi comparación, a partir de los nombres de carpeta y del código de los retos.
12. [H] **Caso real: Drift** (1-abr-2026, **~US$285 millones, más de 50% de su TVL**), según Chainalysis a partir del post-mortem de Drift, sin verificación independiente a esa fecha ([Chainalysis, 9-abr-2026](https://www.chainalysis.com/blog/lessons-from-the-drift-hack/)):
    - **no hubo fallo de código**;
    - el atacante usó **"durable nonces"** para que miembros del Consejo de Seguridad **prefirmaran**, sin saberlo, la transferencia del control de administrador;
    - la multisig era de **2 de 5 y sin timelock** tras una migración del 26-mar-2026;
    - con el control, aceptó como colateral un token falso (CVT) con precio fabricado en un pool de ~US$500 y retiró activos reales.
13. [H] **Atribución de Drift:** Chainalysis ve indicios compatibles con Corea del Norte, pero "la atribución formal sigue pendiente".
    - El 5-abr-2026, Drift la asignó con confianza "media-alta" al mismo actor del hackeo de Radiant Capital (oct-2024), que Mandiant atribuye a un grupo norcoreano.
    - Esta segunda parte la tomé de la cobertura de TRM Labs y Elliptic (extracto de búsqueda) y **no la verifiqué en la fuente de Drift**.
14. [H] **Solana y las carteras personales:** Solana tuvo el mayor número de incidentes contra carteras personales en 2025 (~26,500 víctimas), pero una **tasa menor por cartera** que Ethereum y Tron (Chainalysis, 18-dic-2025).
15. [H] **Salida de fondos de Drift:** el atacante movió ~US$232 millones en USDC de Solana a Ethereum con el protocolo de transferencia de Circle (CCTP). Los críticos, entre ellos ZachXBT, dijeron que Circle pudo congelar antes; Circle respondió que congela "cuando la ley lo exige" ([CoinDesk, 25-sep-2026](https://www.coindesk.com/markets/2026/09/25/circle-and-tether-step-in-to-freeze-hacker-wallet-after-massive-bitget-crypto-heist)).
16. [O] El curso sostiene que aprender primero "a la mala" (nativo) evita depender del framework ("Course Intro").

## 4. Qué cambia para invertir

### Riesgo de exchange (lección de FTX aplicada a Binance)
- [H] **Binance emite su propio token de staking de Solana (BNSOL)**, que perdió la paridad en su mercado el 10-oct-2025 dentro del evento que Binance compensó con ~US$283 millones (ficha 25).
- [I] **Un derivado líquido propio de un exchange es un pasivo con riesgo de liquidez**, como FTT pero en otra escala.
- [I] **Para la cuenta:** no usar BNSOL, WBETH ni productos Earn.

### Riesgo de stablecoin
- [H] En Drift, los USDC robados cruzaron de cadena por la vía del propio emisor (CCTP).
- [I] **El emisor puede actuar o no, y lo decide él:** un riesgo y una protección que no controla el usuario (ficha 32).

### Hackeos de exchanges y de puentes
- [H] **Drift demuestra que el riesgo dominante de 2026 en Solana también fue operativo:**
  - llaves de administrador;
  - multisig de umbral bajo sin timelock;
  - ingeniería social durante meses.
- [I] **Preguntas de diligencia para cualquier protocolo de Solana:**
  - ¿quién tiene la llave de actualización del programa?;
  - ¿qué umbral y qué timelock tiene la multisig?;
  - ¿de dónde sale el precio del colateral?;
  - ¿cómo se aprueban activos nuevos como colateral?

### Autocustodia
- [H] **Los "durable nonces" permiten firmar hoy y ejecutar semanas después** (Chainalysis). Implicaciones:
  - [I] no firmar transacciones que no se entienden, en particular las "de rutina" que llegan fuera de banda;
  - [I] revocar o invalidar las firmas pendientes si hay duda;
  - [I] la "firma a ciegas" es el mismo patrón que en Bybit (fichas 22 y 25).

### Cómo leer una prueba de reservas
- [I] En Solana, **"propiedad" es un campo `owner` de la cuenta y un saldo en lamports**.
- [I] Una PoR de un exchange en Solana debe mostrar direcciones verificables, no solo totales. Aplica la misma regla de serie de tiempo y composición que en EVM (lista de señales).

## 5. Contrapuntos y límites
- **Cobertura de seguridad corta:** una sección de ~1 h con 4 clases de 11. **No basta** para auditar programas de Solana.
- **Página inconsistente:** dice "1 h" pero son 9 secciones, y dice "Beginner" cuando exige Rust.
- **No compilé ni ejecuté.** Mi lectura de los fallos sale del código y de los comentarios de la solución.
- **Relevancia directa para la cuenta:** baja, porque no tenemos SOL. Sirve para evaluar exposición indirecta (BNSOL en Binance) y protocolos que el comité no aprobaría hoy.
- **El caso Drift** se basa en el relato del propio Drift, "aún no verificado de forma independiente" según Chainalysis a la fecha de su artículo.

## 6. Autoexamen

**1. En el reto "Missing Signer Check", ¿qué verificación falta y qué permite?**
- `update` compara la llave del firmante con el dueño guardado, pero no comprueba `is_signer`.
- Cualquiera puede incluir la llave pública del dueño como cuenta, sin firmar, y cambiar el precio del oráculo.
- Fuente: `Cyfrin/solana-course`, `apps/ctf/signer/exercise/src/instructions/update.rs`.

**2. ¿Por qué "Missing Rent Cleanup" es un robo aunque `unlock` verifique la PDA?**
- `unlock` devuelve solo el monto bloqueado y deja los lamports de la renta en la cuenta.
- `sweep`, que puede llamar cualquier firmante sobre la PDA de cualquier dueño, transfiere el excedente al que llama.
- Cerrar una cuenta exige devolver todo y neutralizarla.
- Fuente: `apps/ctf/rent/exercise/src/instructions/{unlock,sweep}.rs` y el comentario de la solución.

**3. ¿Cómo tomó el atacante el control de Drift sin romper el código?**
- Con ingeniería social durante meses consiguió que miembros del Consejo de Seguridad prefirmaran transacciones con "durable nonces", que transferían el control de administrador.
- La multisig era 2 de 5 y sin timelock.
- El 1-abr-2026 ejecutó las transacciones prefirmadas, listó un token falso como colateral y retiró ~US$285 millones.
- Fuente: Chainalysis (9-abr-2026).

**4. ¿Qué clases de la referencia sealevel-attacks no cubre el curso y por qué importa?**
- Type cosplay, CPI arbitraria, cuentas mutables duplicadas, canonicalización del bump, reinicialización y dirección de sysvar.
- El curso no basta como formación de auditoría en Solana: sirve de introducción.
- Fuentes: `coral-xyz/sealevel-attacks` (carpetas 0-10); temario de Updraft.

## 7. Grado de evidencia: **B** (contenido técnico) / **C** (cobertura y relevancia para invertir)
- **B:** el código es público y la clase de cada reto la comprobé leyéndolo. Los conceptos coinciden con la documentación de Solana enlazada desde el repositorio.
- **C:** cubre ~4 de 11 clases de referencia, la página tiene datos inconsistentes y su relación con decisiones de inversión es inferencia mía.
