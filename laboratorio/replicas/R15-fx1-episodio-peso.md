# Réplica R15: ¿qué hace el USD/MXN después de un episodio de depreciación de 6% en 15 días (regla FX-1)?

> Fase 0: formación. No recomienda inversiones. Las secciones 1 a 9 son el pre-registro, escrito el 2026-10-16 antes de calcular cualquier rendimiento posterior a un episodio. La hora real es la del commit que agrega este archivo.

| Campo | Valor |
|---|---|
| ID | `R15` (script `laboratorio/replicas/R15.py`; salida `R15-salida.txt`) |
| Hallazgo que se prueba | La regla FX-1 del sistema (`herramientas/fx_alerta.py`): emite una ALERTA cuando el USD/MXN sube ≥ 6% sobre el mínimo de los 15 días hábiles previos (y su espejo, a la baja). La regla solo informa, no ordena. Pregunta: ¿qué sigue después de un episodio así? ¿Continuación o reversión? |
| Pre-registro escrito el | 2026-10-16, antes de cualquier corrida |
| Responsable | A: orquestador. B: `auditor-de-replicas`, código desde cero y otra fuente |
| Estado | **Replicado con diferencias** (16-oct-2026; A y AC-20 concordantes): no hay reversión (H1 refutada); la continuación de +3% no llega a 30% (H2 sostenida), pero es 1.5-1.7 veces la normal. Etiqueta: descartada como señal operable; útil para calibrar |

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

### Desviaciones del pre-registro
- **Fin de la serie:** A (FRED DEXMXUS) llega al 9-oct-2026 por el rezago de publicación. B (FIX de Banxico, formulario público sin token) llega al 15-oct.
- **Agrupación de episodios:** A y B encadenan los eventos (un evento a menos de 20 días hábiles del anterior pertenece al mismo episodio). B también reporta la agrupación desde el primer día; el veredicto no cambia.
- **Fecha del último episodio:** el FIX marca el episodio de 2026 el 29-sep, no el 28-sep que menciona el encabezado (ese dato era de Yahoo). No tiene ventana completa y no entra.

### 11. Resultados

| Variante | A (FRED): episodios | A: media posterior / incondicional | A: t | A: +3% punto a punto (incondicional) | B (FIX): episodios | B: media / incondicional | B: t | B: +3% (incondicional) |
|---|---:|---|---:|---|---:|---|---:|---|
| Completa, 10 días | 37 | +1.17% / +0.25% | +0.79 | 19% (8%) | 42 | +0.86% / +0.24% | +0.83 | 16.3% (7.9%) |
| Completa, 20 días | 37 | +2.02% / +0.51% | +1.00 | 27% (15%) | 42 | +1.36% / +0.48% | +1.11 | 23.8% (14.1%) |
| Desde 1996, 10 días | 33 | +0.18% / +0.14% | +0.07 | 18% (8%) | 38 | −0.05% / +0.14% | −0.09 | 15.4% (7.7%) |
| **Desde 1996, 20 días (principal)** | **33** | **+0.66% / +0.27%** | **+0.38** | **24% (14%)** | **38** | **+0.16% / +0.28%** | **+0.17** | **21.1% (14.0%)** |

- **B, tocar +3% en algún día de la ventana de 20 días:** 36.8% desde 1996.
- **Espejo a la baja (desde 1996, 20 días; informativo):** en A, 16 episodios con media +0.35% (t +0.06); en B, 10 episodios con media −0.50% (t −0.33).

### 14. Conclusiones permitidas
- Después de una depreciación del peso de 6% en 15 días, **el peso no recupera en promedio** en los 10-20 días siguientes. El t está entre −0.1 y +1.1 en las 8 combinaciones de fuente y variante. La intuición de reversión del pre-registro no se sostiene. [Precisión 16-oct-2026, auditoría semanal: "no recupera" quiere decir que no hay reversión distinguible de cero. En B, desde 1996, la media a 10 días es −0.05% y la de 20 días (+0.16%) queda por debajo de la incondicional (+0.28%); las dos con t ≈ 0. Recalculado con código propio sobre FRED DEXMXUS: las 4 variantes de A y las 33 fechas coinciden. Las ventanas de 20 días no se traslapan (separación mínima de 28 días hábiles) y no hay look-ahead. La mediana es +1.02% y, sin 2008-09-16 (+18.5%), la media queda en +0.10% (t −0.19).]
- **La cola de continuación es mayor de lo normal:** otro +3% punto a punto ocurre en 21-24% de los episodios (contra 14% incondicional), y tocar +3% en algún momento de la ventana, en ~37%.

### 15. Conclusiones que NO se sostienen
- Que una ALERTA de FX-1 sea momento de "esperar a que el peso regrese": no hay evidencia de reversión.
- Que sea señal de continuación operable: la media no es significativa.

### 16. Estado y reproducción
- **Estado: Replicado con diferencias** (H1 refutada y H2 sostenida, en A y en B).
- **Etiqueta: descartada** como regla de operación. **Uso:** en la frase para el dueño de una ALERTA de FX-1, no sugerir reversión; la probabilidad de otro +3% en 20 días es del orden de 1 en 4 o 5.
- **Reproducción:** `python3 laboratorio/replicas/R15.py` (A) y `python3 -I laboratorio/auditorias/AC-20-R15/b.py` (B). Los datos no se versionan; los sha256 están en las salidas.

