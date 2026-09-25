# S6: verificación externa del compromiso público

Hecha por el coordinador el 25-sep-2026, fuera del flujo de trabajo del examen.

| Comprobación | Resultado |
|---|---|
| Commit de compromiso | `6c526b6`, 2026-09-25 06:02:26 UTC (compromiso.json). `clave.enc` entró antes, en `5909c87` (06:02:03 UTC), mediante un commit de sincronización |
| SHA256 de `clave.enc` extraído de `6c526b6` | `ed5f8e0990380279db86b266a4ffdb400507ba3107dae38fd46f4163f33aa2ab`, presente en `compromiso.json` del mismo commit |
| Descifrado (`openssl enc -d -aes-256-cbc -pbkdf2 -iter 200000 -pass file:contrasena.txt`) | SHA256 `8119ceecf65833cbc4f1c2ab16510c767073c64fdd2b1231b72cbfeee55549a8`, igual al comprometido |
| `clave.json` publicada (revelación, commit `9ef8c60`, 06:50:55 UTC) | Idéntica, byte por byte, a la descifrada del commit previo |
| Auditoría de libro cerrado (3 registros del sustentante y la defensa) | 0 usos de web o red; la única escritura fue un script auxiliar de cálculo (`scratchpad/s6/common.py`) |
