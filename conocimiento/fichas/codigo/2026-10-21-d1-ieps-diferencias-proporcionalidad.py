"""D1 · Proporcionalidad (CPEUM art. 31 fr. IV; P./J. 10/2003) aplicada al IEPS por diferencias de litros (LIF 2027, iniciativa;
fuente secundaria grado C). Ejercicio con aserciones. CIFRAS ILUSTRATIVAS: la cuota (6.00 MXN/l) y el margen (1.40 MXN/l) son
supuestos, no datos verificados. Reproduce: python3 conocimiento/fichas/codigo/2026-10-21-d1-ieps-diferencias-proporcionalidad.py"""

CUOTA = 6.00     # MXN por litro, supuesto (la cuota real 2027 debe leerse en la LIEPS/RMF vigentes)
MARGEN = 1.40    # MXN por litro de margen bruto de la estación, supuesto


def ieps_diferencias(comprados, vendidos, cuota=CUOTA):
    """Base según la iniciativa (reportada): diferencia POSITIVA mensual vendidos − adquiridos, sin acreditamiento."""
    return max(0.0, vendidos - comprados) * cuota


# Caso 1: estación sin ninguna irregularidad, con desfase de calendario.
# Mes 1 compra 520 mil l y vende 480 mil (sube inventario 40 mil); mes 2 compra 460 mil y vende 500 mil (baja inventario 40 mil).
m1 = ieps_diferencias(520_000, 480_000)
m2 = ieps_diferencias(460_000, 500_000)
margen_m2 = 500_000 * MARGEN
assert m1 == 0 and m2 == 240_000
assert abs(m2 / margen_m2 - 0.342857) < 1e-5           # 34.3% del margen bruto del mes, sin litros irregulares
# Bimestre completo: compras = ventas = 980 mil l. No hubo litro sin origen, y aun así hay impuesto.
assert 520_000 + 460_000 == 480_000 + 500_000

# Caso 2: misma estación, pero con inventario conciliado (si la autoridad o la ley reconocen el inventario inicial).
def ieps_con_inventario(comprados, vendidos, inv_ini, inv_fin, cuota=CUOTA):
    faltante = vendidos - (comprados + inv_ini - inv_fin)   # litros vendidos que no se explican con compras ± inventario
    return max(0.0, faltante) * cuota
assert ieps_con_inventario(460_000, 500_000, 40_000, 0) == 0

# Caso 3: venta real de 2,500 l sin origen (huachicol). Ese es el objetivo declarado de la medida.
c3 = ieps_con_inventario(500_000, 502_500, 0, 0)
assert c3 == 15_000 and abs(c3 / (502_500 * MARGEN) - 0.02132) < 1e-4

print(f"Caso 1 (solo calendario): mes 2 paga {m2:,.0f} MXN = {m2 / margen_m2:.1%} del margen bruto del mes, sin litros irregulares")
print("Caso 2 (inventario reconocido): 0 MXN")
print(f"Caso 3 (2,500 l sin origen): {c3:,.0f} MXN = {c3 / (502_500 * MARGEN):.1%} del margen")
print("Todas las aserciones pasaron.")
