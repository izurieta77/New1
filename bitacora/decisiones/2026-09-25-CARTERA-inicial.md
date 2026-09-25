# Decisión: cartera inicial real de la cuenta arena-claude en GBM (20,000 MXN)

- **Fecha de decisión:** 25-sep-2026, después del cierre. La hora queda sellada por el commit de este archivo, antes de cualquier precio de ejecución.
- **Ejecución:** lunes 28-sep-2026, en real, por el dueño en la app de GBM. Decisión del dueño del 25-sep-2026 (`config/parametros.json` → `prioridad_actual.excepcion_cuenta_arena`).
- **Temporada:** 28-sep-2026 a 28-ene-2027 (4 meses).
- **Perfil:** `arena_agresivo`. Tope absoluto del dueño: 10,000 MXN.
- **Estado de este documento:** decisión del comité tomada; faltan el dimensionamiento final del gestor de riesgo y el informe del verificador, que se agregan abajo en cuanto lleguen.

## Tesis y cómo se refutaría

**Tesis:** en 4 meses, el TWR lo decide sobre todo la exposición y el control de pérdidas, no la selección. Ningún análisis mostró ventaja sobre beta 1:
- el cuantitativo midió 78 temporadas: la ventaja neta de las variantes tácticas y apalancadas no es significativa (t entre −1.17 y −0.31);
- el laboratorio tiene 0 de 13 estrategias con ventaja demostrada.

Por eso la cartera es beta de EUA sin apalancar (S&P 500 más Nasdaq-100), con liquidez en MXN. Tiene la menor probabilidad de salir del juego y deja espacio para subir exposición cuando haya datos de los rivales (modo torneo).

**Se refuta si, al 28-dic-2026:**
- la cuenta toca −12% (el modelo da ~3% de probabilidad), o
- quedamos 3 pp o más atrás de un rival con beta ≤ 1.2 sin que haya un choque de mercado que lo explique.

## Dictámenes (3 líneas cada uno)

- **Macro, confianza 60. Voto: B, variante con SPYM 7 + SPXL 1 + efectivo.**
  - Régimen mixto: tendencia y crédito a favor; bono de 10 años en ~5.18% (máximo desde 2007) y tasa real de 2.76% en contra.
  - Cada +100 pb del bono restó 7.9% al S&P en 2026 (cálculo propio, grado C).
  - El USD amortigua en MXN.
- **Geopolítico, confianza 55. Voto: C, con SPYM 5 + TQQQ 4 + XLE 5.**
  - El eje de riesgo es Ormuz → WTI → Fed → tasa real → NDX; XLE funcionó como cobertura en 2026.
  - Registró P0006-P0010.
  - Advierte un posible hueco a la baja el lunes por el ultimátum iraní del fin de semana.
- **Fundamental, confianza 60. Voto: B moderado, con SPYM 5 + SPXL 1 + QQQM 1.**
  - Ninguna acción le gana al índice con evidencia: NVDA, LRCX, GE, XOM, MRK y GMEXICOB, evaluadas.
  - S&P con P/U adelantado de 19.2, pero CAPE de 41.3; la valuación no sirve para decidir cuándo entrar a 4 meses.
- **Abogado del diablo, confianza 70. Voto: A ejecutable, con SPYM 7 + QQQM 1 + Smart Cash.**
  - B y C no sobreviven: con 50% en 3x, P(−12%) ≈ 39%, con la misma mediana que A.
  - Riesgos operativos: títulos enteros, hueco del lunes, stops poco confiables en SIC.
  - Detectó un error en `portafolio.py` (cortacircuitos estándar en la arena). Ya se corrigió en el commit d66f602.
- **Cuantitativo, confianza 55. Voto: C′, con SPYM 5 + XLE 5 + QQQM 1.**
  - Para A: mediana +5.9%, p10 −4.4%, P(−12%) 3%, P(−20%) 0%.
  - Para B1: mediana +7.0%, P(−12%) 19%.
  - Ninguna candidata tiene ventaja sobre beta 1. Simulación en `arena/modelos/cartera_inicial_simulacion.py`.

## Votos y regla aplicada

La regla del skill `comite-de-inversion` es para una tesis. Aquí se eligió entre candidatas, así que se aplicó **por componente**:

| Componente | Votos | ¿Sobrevive al abogado del diablo? | Resultado |
|---|---|---|---|
| SPYM (S&P 500) | 5 de 5 | Sí | **Entra** |
| QQQM (Nasdaq-100) | 3 de 5 (fundamental, abogado del diablo, cuantitativo) | Sí | **Entra** |
| SPXL (S&P 3x) | 2 de 5 | No: "no sobrevive" y sin 4 votos con confianza ≥ 60 | Fuera |
| TQQQ (Nasdaq 3x) | 1 de 5 | No | Fuera |
| XLE (energía) | 2 de 5 | No: C no sobrevive y tiene 0 votos con confianza ≥ 60 | Fuera |

Confianza media del comité: 60. El umbral es 55.

**Decisión: cartera A**, con SPYM y QQQM en títulos enteros y el resto en liquidez en MXN.

## Disenso (se conserva íntegro)

- **Macro y fundamental** quieren una línea de SPXL: más mediana y 46% de probabilidad de quedar primero contra 28% de A, en el campo F1 del cuantitativo. Queda como la primera opción para subir exposición en modo torneo cuando haya reportes de los rivales.
- **Geopolítico y cuantitativo** quieren XLE como cobertura de Ormuz: correlación de −0.25 con el S&P a 60 días. Se descarta por ahora: un acuerdo en Ormuz la castiga, y la regla del abogado del diablo no se supera.
- **Condición del abogado del diablo:** nada apalancado hasta tener 6 reportes semanales de los rivales y el ETF verificado en la app de GBM.

## Pronósticos del comité

| ID | Autor | Pregunta | p | Resuelve |
|---|---|---|---|---|
| P0006-P0010 | analista geopolítico | Ormuz, ataque de EUA, retiro del T-MEC, calificación de México | ver `pronosticos.csv` | nov-2026 a mar-2027 |
| P0011 | macro | S&P > 7,743.41 al 28-mar-2027 | 0.72 | 28-mar-2027 |
| P0012 | fundamental | ^GSPC > 7,743.41 el 28-ene-2027 | 0.63 | 28-ene-2027 |
| P0013 | abogado del diablo | S&P con caída de 10% o más desde su máximo antes del 28-ene-2027 | 0.25 | 28-ene-2027 |
| P0014 | cuantitativo | La cuenta real no toca −12% | 0.90 | 28-ene-2027 |

## Tamaño, stop, criterio de salida y boletas

*Pendiente del gestor de riesgo, con veto, y del verificador. Se agregan en este mismo archivo.*
