"""D8: ganancia fiscal en el SIC (LISR art. 129, fr. I-III, reglas a) y pérdidas de 10 años) con ejemplos propios.
Supuestos: no se incluye actualización por INPC (regla a: se actualiza el costo promedio hasta el mes anterior a la venta);
se muestra el efecto sin actualizar para aislar comisiones y costo promedio."""

def costo_promedio(compras):
    """compras: lista de (titulos, precio, comision). Regla a): (monto pagado + comisiones) / títulos."""
    t = sum(c[0] for c in compras)
    monto = sum(c[0] * c[1] + c[2] for c in compras)
    return monto / t, t

def ganancia_venta(titulos_v, precio_v, comision_v, costo_prom):
    """Regla a): precio de venta menos comisiones de venta, menos costo promedio por títulos vendidos."""
    ingreso = titulos_v * precio_v - comision_v
    costo = titulos_v * costo_prom
    return ingreso - costo

# Caso 1: dos compras de ACME (emisora de EUA cotizada en la BMV), luego venta parcial
compras = [(10, 100.0, 2.50), (10, 120.0, 2.50)]
cp, t = costo_promedio(compras)
g = ganancia_venta(10, 130.0, 3.25, cp)
print(f"Costo promedio por título = {cp:.4f} (20 títulos, comisiones incluidas)")
print(f"Ganancia de vender 10 a 130 con comisión 3.25 = {g:.2f}")
assert abs(cp - ((10*100+2.5)+(10*120+2.5))/20) < 1e-9
assert abs(g - (10*130 - 3.25 - 10*cp)) < 1e-9

# Caso 2: pérdidas y 10 años de arrastre (fr. I-III, último párrafo): el arrastre solo contra ganancias del mismo régimen
ganancias = {2026: 0.0, 2027: 15000.0}
perdida_2026 = 8000.0
pendiente = perdida_2026
for anio in sorted(ganancias):
    if anio == 2026:
        continue
    aplica = min(pendiente, ganancias[anio])
    pendiente -= aplica
    print(f"{anio}: ganancia {ganancias[anio]:,.2f}, pérdida arrastrada aplicada {aplica:,.2f}, base gravable {ganancias[anio]-aplica:,.2f}")
assert pendiente == 0.0
