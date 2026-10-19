"""C4 · Consolidación y combinaciones de negocios (IFRS 3 e IFRS 10). Ejercicio con aserciones.
Cifras ilustrativas (supuestos propios), en millones. Reproduce: python3 conocimiento/fichas/codigo/2026-10-19-c4-consolidacion-ifrs3-ifrs10.py"""


def credito_mercantil(contraprestacion, nci, previa_vr, activos_netos_vr):
    """IFRS 3 §32: (contraprestación + NCI + participación previa a valor razonable) − activos netos identificables."""
    return contraprestacion + nci + previa_vr - activos_netos_vr


# 1) Compra de 60% por 600; activos netos identificables a valor razonable 700.
AN = 700.0
nci_parcial = 0.40 * AN                    # IFRS 3 §19(b): parte proporcional de los activos netos
nci_completo = 380.0                       # §19(a): valor razonable del 40% (sin prima de control: 0.40/0.60*600 = 400 > 380)
gm_parcial = credito_mercantil(600, nci_parcial, 0, AN)
gm_completo = credito_mercantil(600, nci_completo, 0, AN)
assert abs(gm_parcial - 180) < 1e-9 and abs(gm_completo - 280) < 1e-9
assert abs((gm_completo - gm_parcial) - (nci_completo - nci_parcial)) < 1e-9   # la diferencia es el crédito mercantil del minoritario

# 2) Adquisición por etapas (IFRS 3 §42): ya tenía 20% (valor en libros por participación 150; valor razonable 200);
#    compra otro 40% por 440 y obtiene control con 60%.
libros_previa, vr_previa = 150.0, 200.0
ganancia_remedicion = vr_previa - libros_previa            # va a resultados: utilidad contable, no hay efectivo
gm_etapas = credito_mercantil(440, 0.40 * AN, vr_previa, AN)
assert ganancia_remedicion == 50 and abs(gm_etapas - 220) < 1e-9

# 3) Después compra 20% adicional de los minoritarios por 250 (de 60% a 80%), sin cambio de control.
#    IFRS 10 §23: transacción de capital. El crédito mercantil NO cambia y no hay resultado.
nci_antes = nci_parcial                                      # 280 por el 40% (supuesto: sin cambios desde la compra)
nci_transferido = nci_antes * (20 / 40)                      # 140
cargo_capital_controladora = 250 - nci_transferido          # 110 contra el capital de la controladora
assert nci_transferido == 140 and cargo_capital_controladora == 110

# 4) Lectura del analista: utilidad atribuible y valor empresa.
#    Grupo: matriz con EBITDA 700 propio + subsidiaria 60% con EBITDA 300 y utilidad 100. Utilidad consolidada 400.
ebitda_consolidado = 700 + 300                               # IFRS 10: se consolida el 100% de la subsidiaria
utilidad_consolidada = 400.0
utilidad_minoritario = 0.40 * 100                            # B94: se atribuye a la participación no controladora
utilidad_controladora = utilidad_consolidada - utilidad_minoritario
assert ebitda_consolidado == 1000 and utilidad_controladora == 360
#    Valor empresa: si se omite el minoritario (a mercado), el múltiplo EV/EBITDA consolidado queda subestimado.
cap_mercado, deuda_neta, nci_mercado = 6000.0, 2000.0, 600.0
ev_bien = cap_mercado + deuda_neta + nci_mercado
ev_mal = cap_mercado + deuda_neta
mult_bien, mult_mal = ev_bien / ebitda_consolidado, ev_mal / ebitda_consolidado
assert abs(mult_bien - 8.6) < 1e-9 and abs(mult_mal - 8.0) < 1e-9
#    P/U: la capitalización de la controladora va contra la utilidad de la controladora, no contra la consolidada.
pu_bien, pu_mal = cap_mercado / utilidad_controladora, cap_mercado / utilidad_consolidada
assert abs(pu_bien - 16.6667) < 1e-3 and abs(pu_mal - 15.0) < 1e-9

print(f"1) Crédito mercantil: parcial {gm_parcial:.0f}, completo {gm_completo:.0f} (diferencia = minoritario a VR − parte proporcional = {nci_completo - nci_parcial:.0f})")
print(f"2) Por etapas: ganancia por remedición {ganancia_remedicion:.0f} a resultados; crédito mercantil {gm_etapas:.0f}")
print(f"3) Compra de 20% de minoritarios por 250: baja de NCI {nci_transferido:.0f}; cargo al capital de la controladora {cargo_capital_controladora:.0f}; crédito mercantil sin cambio")
print(f"4) EV/EBITDA {mult_bien:.2f}x (con minoritario) contra {mult_mal:.2f}x (sin él); P/U {pu_bien:.2f}x (utilidad controladora) contra {pu_mal:.2f}x (consolidada)")
print("Todas las aserciones pasaron.")
