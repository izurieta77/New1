# Radar de oportunidades por niveles: Oro, Platino y Diamante (pre-registro)

> Pedido del dueño, 5-oct-2026: "¿qué me vas a proponer para oportunidades Diamante, platino u oro?" en cripto, en la bolsa mexicana y en la de Estados Unidos. Este texto **se escribe antes de puntuar a ningún candidato**; no se edita después. Los niveles se asignan con el sistema que ya existe: `conocimiento/26-radar-de-oportunidades.md` §6.2 (puertas P1-P6 y puntaje de 0 a 100). Fase 0: esto es un **radar de candidatos a estudio y comité**, no una recomendación de compra. Una orden real solo sale del comité del viernes, con el gestor de riesgo, y el dueño la ejecuta a mano.

## Niveles
| Nivel | Condición (todas) | Qué sigue |
|---|---|---|
| **Diamante** | Pasa las puertas P1-P6, **grado de evidencia B o mayor** y **puntaje ≥ 80** | Dossier y comité prioritarios; tamaño hasta 100% del riesgo por operación del perfil |
| **Platino** | Pasa las puertas, evidencia **C o mayor** y puntaje **70-79** | Dossier y comité; hasta 50% del riesgo máximo |
| **Oro** | Pasa las puertas y puntaje **55-69** | Vigilancia con alerta de entrada (el disparador que lo subiría de nivel) y de salida |
| Sin nivel | Falla una puerta o puntaje < 55 | Descarte registrado con su razón |

## Reglas de calificación
- Cada componente del puntaje se llena con un **dato verificado** (con fecha y fuente) o, si no se pudo verificar, con el **valor más bajo de su escala** y se marca "no verificado". Nunca se redondea a favor.
- **P2 (evidencia):** el grado lo fija la mejor evidencia de que ese tipo de oportunidad funciona (por ejemplo, la tabla maestra del laboratorio: hoy **0 ventajas demostradas** de 26 pruebas). Una narrativa de moda o un precio que sube no es evidencia.
- **P3 (ejecutable):** solo cuenta lo que el dueño puede comprar. Cripto: BTC y ETH, otra moneda con tope de 20% de la cuenta cripto y aprobación del comité (`parametros.json`). Bolsa: lo que GBM ofrezca en el SIC o la BMV; un título debe caber en el tope por posición del perfil.
- **P4 (costos):** se calcula con la comisión de GBM de 0.25% más IVA, el diferencial cambiario y el *spread*; en Binance, la comisión y el *spread* de BTC/MXN.
- **P5 (salida):** cada candidato trae su *stop* de precio, su *stop* de tiempo y el hecho que refuta la tesis, escritos antes de entrar. Las alertas de entrada y salida salen de ahí.
- **Un candidato con puntaje alto pero sin las puertas no tiene nivel.** Si hoy no hay Diamantes, se dice "no hay Diamantes hoy"; no se baja el listón para llenar la lista.
- Los candidatos **Diamante y Platino** entran al dossier de 48 h (skill `ficha-empresa` o ficha de oportunidad) y se registran como pronóstico antes de cualquier operación (`bitacora/pronosticos.csv`).

## Qué se entrega
1. `13-radar-cripto-2026-10-05.md`, `14-radar-eua-2026-10-05.md` y `15-radar-bmv-2026-10-05.md`: tablas con puertas, puntaje por componente, nivel, contraparte, alertas de entrada y de salida y riesgos.
2. `16-radar-niveles-resultado-2026-10-05.md`: la lista consolidada por nivel, con el comparativo contra lo que ya tiene la cartera.
