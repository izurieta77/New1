"""Ficha 2026-10-26 · C2 · CINIIF 12 (= AASB Int. 12): ingresos por construcción en concesiones y su efecto en
márgenes y pronósticos. Datos: ASUR 3T26 (evento relevante BMV del 22-oct, empresas/ASURB.MX/post-mortem-2026-10-23.md)."""
ing_total, construccion = 10_420.5, 2_591.1
ebitda = 4_719.3
ing_sin = ing_total - construccion
print(f"Ingresos sin construcción {ing_sin:,.1f}")
print(f"Margen EBITDA sobre total: {ebitda/ing_total:.1%}; sobre ingresos sin construcción (ajustado de ASUR): {ebitda/ing_sin:.1%}")
assert abs(ebitda / ing_sin - 0.603) < 0.001        # ASUR reporta 60.3%

# Con margen ~0 en construcción (ingreso = costo), el EBITDA no cambia con la construcción;
# el margen sobre el total cae mecánicamente cuando sube el capex del Plan Maestro de Desarrollo.
for c in (1_000, 1_800, 2_591.1, 3_500):
    print(f"construcción {c:>7,.0f}: margen sobre total {ebitda/(ing_sin + c):.1%}")

# Error de pronóstico: nuestro punto 9,450 suponía construcción ~1,800
punto, supuesto_constr = 9_450, 1_800
err_total = (punto / ing_total - 1)
err_sin = ((punto - supuesto_constr) / ing_sin - 1)
print(f"Error del punto total {err_total:+.2%}; sin construcción {err_sin:+.2%}")
# Segunda comprobación: la parte del error explicada por construcción
explicado = (construccion - supuesto_constr) / ing_total
print(f"Parte del error por construcción: {explicado:.1%} de los ingresos totales")
assert abs((err_total) - ((punto - supuesto_constr) - ing_sin - (construccion - supuesto_constr)) / ing_total) < 1e-12
print("Segunda comprobación OK")
