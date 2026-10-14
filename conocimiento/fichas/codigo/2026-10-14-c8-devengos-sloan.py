#!/usr/bin/env python3
"""Ficha 14-oct-2026 (Doctorado contabilidad C8): devengos de Sloan (1996).

1) Devengos por el método de balance (Sloan 1996, definición de la tabla 1).
2) Pronóstico de la utilidad siguiente con persistencias distintas (Sloan, tabla 3, panel A pooled:
   gamma1 = 0.765 devengos, gamma2 = 0.855 flujo) contra la "fijación" (persistencia común 0.8).
3) Contraejemplo: una adquisición infla el método de balance (Hribar-Collins 2002) aunque el
   devengo operativo sea cero.
Corre con python3 -I; las aserciones son la comprobación.
"""

def devengos_balance(d_ac, d_caja, d_pc, d_deuda_cp, d_isr_por_pagar, dep, activos_prom):
    """Accruals = (dCA - dCash) - (dCL - dSTD - dTP) - Dep, entre activos totales promedio."""
    return ((d_ac - d_caja) - (d_pc - d_deuda_cp - d_isr_por_pagar) - dep) / activos_prom

# --- 1) Empresa A: crece en cuentas por cobrar e inventario (devengos altos)
acc_a = devengos_balance(d_ac=180, d_caja=20, d_pc=60, d_deuda_cp=10, d_isr_por_pagar=5, dep=40, activos_prom=1000)
# (180-20) - (60-10-5) - 40 = 160 - 45 - 40 = 75 -> 7.5%
assert abs(acc_a - 0.075) < 1e-12

# --- 2) Dos empresas con la misma utilidad (ROA 10%) y distinta composición
G_ACC, G_CF, G_FIJ = 0.765, 0.855, 0.80  # sin intercepto, para aislar el efecto de composición
def pronostico(roa, acc, persistencia_separada=True):
    cf = roa - acc
    return G_ACC * acc + G_CF * cf if persistencia_separada else G_FIJ * roa

alta = pronostico(0.10, 0.075)          # devengos 7.5%, flujo 2.5%
baja = pronostico(0.10, -0.025)         # devengos -2.5%, flujo 12.5%
fij = pronostico(0.10, 0.0, False)
print(f"ROA siguiente: devengos altos {alta:.4%}, devengos bajos {baja:.4%}, fijación {fij:.4%}")
assert abs(alta - (0.765*0.075 + 0.855*0.025)) < 1e-12   # 7.875%
assert abs(baja - (0.765*-0.025 + 0.855*0.125)) < 1e-12  # 8.775%
assert abs((baja - alta) - 0.009) < 1e-12  # 0.9 pp = (0.855-0.765) x 10 pp de diferencia en devengos
# La fijación sobreestima a la de devengos altos y subestima a la de devengos bajos:
assert fij > alta and fij < baja

# --- 3) Contraejemplo: adquisición pagada con caja, sin actividad operativa nueva
# Compra una empresa con 100 de cuentas por cobrar y 30 de proveedores: el balance consolidado
# sube dCA en 100 y dCL en 30, aunque los devengos operativos del año sean cero.
acc_fusion = devengos_balance(d_ac=100, d_caja=0, d_pc=30, d_deuda_cp=0, d_isr_por_pagar=0, dep=0, activos_prom=1000)
assert abs(acc_fusion - 0.07) < 1e-12
print(f"Devengos por balance tras la adquisición: {acc_fusion:.2%} (operativos verdaderos: 0.00%)")

# --- 4) Segunda comprobación con los datos de French (salida de laboratorio/replicas/R13.py)
pre, post = 0.4139, 0.1632   # %/mes VW Lo10-Hi10, 1963-07..1996-06 y 1996-07..2026-08
assert abs((1 - post/pre) - 0.606) < 0.002
print("Comprobaciones OK")
