# Réplica R15: ¿qué hace el USD/MXN después de un episodio de depreciación de 6% en 15 días (regla FX-1)?

> Fase 0: formación. No recomienda inversiones. Las secciones 1 a 9 son el pre-registro, escrito el 2026-10-16 antes de calcular cualquier rendimiento posterior a un episodio. La hora real es la del commit que agrega este archivo.

| Campo | Valor |
|---|---|
| ID | `R15` (script `laboratorio/replicas/R15.py`; salida `R15-salida.txt`) |
| Hallazgo que se prueba | La regla FX-1 del sistema (`herramientas/fx_alerta.py`): emite una ALERTA cuando el USD/MXN sube ≥ 6% sobre el mínimo de los 15 días hábiles previos (y su espejo, a la baja). La regla solo informa, no ordena. Pregunta: ¿qué sigue después de un episodio así? ¿Continuación o reversión? |
| Pre-registro escrito el | 2026-10-16, antes de cualquier corrida |
| Responsable | A: orquestador. B: `auditor-de-replicas`, código desde cero y otra fuente |
| Estado | en curso |

**Conocimiento previo declarado:**
- Sé que el peso tuvo episodios grandes en 1994-95, 2008, 2016 (elección en EUA), 2020 y 2024, y que el 28-sep-2026 la regla disparó. No he calculado nada con estos datos.
- Mi intuición es que hay reversión parcial: la "sobrerreacción" del tipo de cambio de Dornbusch y la prima de carry del peso.

## PRE-REGISTRO (secciones 1 a 9; no se editan después de la primera corrida)

### 1. Hipótesis previa y mecanismo
- **Evento:** un día t en que USD/MXN(t) ≥ 1.06 × min(USD/MXN de t−15 a t−1), que es la definición de episodio al alza de FX-1. Los eventos de un mismo episodio (a menos de 20 días hábiles del anterior) se agrupan; cuenta el **primer día** de cada episodio.
- **H1 (reversión):** el cambio del USD/MXN en los 20 días hábiles siguientes al primer día del episodio es, en promedio, **negativo** (el peso recupera), con una media menor que la incondicional de 20 días y **t ≤ −1.0** sobre los episodios.
- **H2 (no continuación):** la frecuencia de que el USD/MXN siga subiendo otro 3% o más en esos 20 días es **menor a 30%**.
- **Mecanismo:** sobrerreacción a choques de riesgo y regreso del carry. El mecanismo alternativo, continuación por salida de capitales, es la refutación.

### 2. Criterio de refutación
- **H1 refutada** si la media del cambio de 20 días posterior al episodio es ≥ la media incondicional, o si su t por episodio es > −1.0.
- **H2 refutada** si la frecuencia de "+3% adicional o más" es ≥ 30%.
- Ambas sostenidas: "Replicado". Solo una: "Replicado con diferencias". Ninguna: "No replicado".

### 3. Datos
- **A:** FRED `DEXMXUS` (mediodía de Nueva York), diario desde 1993-11-08.
- **B:** la elige el auditor. Puede ser el FIX de Banxico (SF43718; sin token, otra vía pública) o Yahoo `MXN=X`.

### 4. Universo
Un solo par: USD/MXN.

### 5. Fecha de disponibilidad
El evento se conoce con el dato del día t; la ventana empieza en t. Sin información futura.

### 6. Periodo
Toda la serie disponible hasta el 15-oct-2026. **Variante de robustez obligatoria:** desde 1996-01-01, para excluir la crisis de 1994-95, cuando México tenía otro régimen cambiario.

### 7. Limpieza
Días sin dato se descartan y se reportan.

### 8. Variantes (N = 4)
Horizonte de 10 y 20 días; serie completa y desde 1996. La principal es 20 días desde 1996. También se reporta el espejo a la baja (peso apreciándose 6%), solo como información.

### 9. Costos y comparación
Sin costos: es una pregunta de pronóstico, no una estrategia. Comparación: el cambio incondicional de 20 días y la frecuencia incondicional de "+3% o más en 20 días".

---

## RESULTADOS (se llenan después de correr)
