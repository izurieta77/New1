"""Arrendamiento de 5 años, pago anual vencido de 100, tasa de descuento 8%.
Compara el efecto en utilidad de operación, EBITDA y deuda entre IFRS 16 (modelo único del arrendatario)
y ASC 842 contrato operativo (un solo costo de arrendamiento lineal). Segunda comprobación: método alterno."""
pago, n, r = 100.0, 5, 0.08
vp = sum(pago / (1 + r) ** t for t in range(1, n + 1))
vp2 = pago * (1 - (1 + r) ** -n) / r
assert abs(vp - vp2) < 1e-9
dep = vp / n
saldo = vp
filas = []
for t in range(1, n + 1):
    interes = saldo * r
    saldo = saldo + interes - pago
    filas.append((t, dep, interes, dep + interes, saldo))
assert abs(saldo) < 1e-9
tot_ifrs = sum(f[3] for f in filas)
print(f"VP del pasivo = {vp:.2f}")
print("año  depreciación  interés  gasto IFRS16  pasivo final")
for t, d, i, g, s in filas:
    print(f"{t}    {d:8.2f}   {i:7.2f}   {g:10.2f}   {s:9.2f}")
print(f"Gasto total IFRS16 = {tot_ifrs:.2f}; pagos totales = {pago*n:.2f}; ASC 842 operativo: costo lineal {pago:.2f} por año")
assert abs(tot_ifrs - pago * n) < 1e-9
print(f"EBITDA año 1: IFRS16 excluye dep+interés (+{pago:.0f} frente a antes); ASC842 operativo lo resta ({-pago:.0f})")
print(f"Gasto año 1 IFRS16 {filas[0][3]:.2f} vs {pago:.2f} lineal: diferencia {filas[0][3]-pago:+.2f}")
print(f"Gasto año 5 IFRS16 {filas[-1][3]:.2f} vs {pago:.2f} lineal: diferencia {filas[-1][3]-pago:+.2f}")
EBITDA_base = 1000.0
print(f"Deuda adicional visible en IFRS16 al inicio: {vp:.2f}; si EBITDA ajustado = {EBITDA_base:.0f}+{pago:.0f}, la razón deuda/EBITDA cambia")
