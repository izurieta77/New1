# S7: verificación externa del compromiso público

La hizo el coordinador el 25-sep-2026, fuera del flujo de trabajo del examen.

| Comprobación | Resultado |
|---|---|
| Commit de compromiso | `2a50ca2c7f5cd6cf6e6f4ce9f6da535ee02acb86`, 2026-09-25 06:03:15 UTC (fecha puesta por GitHub) |
| SHA256 de `clave.enc` extraído de ese commit (`git show 2a50ca2:...`) | `0355bd38fe70692a541aa87d9c399a94922319563534692d4a9f133ec9a1df6e`, idéntico al registrado en `compromiso.json` **del mismo commit** |
| Descifrado con la contraseña revelada (`openssl enc -d -aes-256-cbc -pbkdf2 -iter 200000`) | SHA256 `4aa2121251ef21966ccbfead7780ccdb117eaa3cc92de40eb3e4b8ff1078cd11`, idéntico al de `compromiso.json` |
| `clave.json` publicada en la revelación (commit `3a0bebe`, 06:43:27 UTC) | Byte a byte igual a la descifrada del commit previo (`cmp` sin diferencias) |
| Cronología | Compromiso a las 06:03:15 → llegó a GitHub a las 06:03:22 → primer registro del sustentante a las 06:03:46 |

**Conclusión:** la clave de S7 no cambió entre el compromiso y la calificación. Cualquiera puede repetir estos pasos con `git show`, `sha256sum` y `openssl`.
