"""C9 · Gobierno corporativo de la sociedad anónima bursátil (LMV arts. 24-26, 42-43). Verificador con aserciones.
Texto: LMV vigente, última reforma DOF 14-11-2025 (diputados.gob.mx). Casos ilustrativos (supuestos propios).
Reproduce: python3 conocimiento/fichas/codigo/2026-10-19-c9-gobierno-lmv.py"""


def consejo_ok(total, independientes):
    """Art. 24: máximo 21 consejeros y al menos 25% independientes."""
    return total <= 21 and independientes / total >= 0.25


def comite_ok(miembros_indep, miembros_total, tipo, control_50=False, revelado=False):
    """Art. 25: comités de prácticas societarias y de auditoría solo con independientes y mínimo 3.
    Excepción: si un grupo controla >= 50% del capital, el de prácticas societarias basta con mayoría de independientes, revelándolo."""
    if miembros_total < 3:
        return False
    if tipo == "practicas" and control_50 and revelado:
        return miembros_indep / miembros_total > 0.5
    return miembros_indep == miembros_total


def proveedor_importante(ventas_de_la_sociedad_al_tercero, ventas_totales_del_tercero):
    """Art. 26 fr. IV: importante si las ventas de la sociedad representan > 10% de las ventas totales del cliente, prestador o proveedor (12 meses)."""
    return ventas_de_la_sociedad_al_tercero / ventas_totales_del_tercero > 0.10


def deudor_acreedor_importante(credito, activos_sociedad, activos_contraparte):
    """Art. 26 fr. IV: importante si el crédito es > 15% de los activos de la sociedad o de su contraparte."""
    return credito / activos_sociedad > 0.15 or credito / activos_contraparte > 0.15


def puede_ser_consejero(meses_desde_que_fue_auditor_externo):
    """Art. 24 párr. 2: no puede serlo quien fue auditor externo de la sociedad o de su grupo en los 12 meses anteriores."""
    return meses_desde_que_fue_auditor_externo is None or meses_desde_que_fue_auditor_externo > 12


# Consejo: 15 miembros. Con 4 independientes, 26.7% (cumple); con 3, 20% (no cumple). Mínimo con 15: ceil(3.75) = 4.
assert consejo_ok(15, 4) and not consejo_ok(15, 3)
assert consejo_ok(21, 6) and not consejo_ok(22, 10)          # 6/21 = 28.6%; 22 excede el máximo
minimo = {n: -(-n // 4) for n in (8, 12, 15, 21)}            # ceil(n * 0.25)
assert minimo == {8: 2, 12: 3, 15: 4, 21: 6}

# Comités: auditoría con 3 independientes cumple; con 2 independientes y 1 patrimonial no.
assert comite_ok(3, 3, "auditoria") and not comite_ok(2, 3, "auditoria")
# Emisora controlada (grupo con >= 50%): prácticas societarias con 2 de 3 independientes cumple solo si se revela.
assert comite_ok(2, 3, "practicas", control_50=True, revelado=True)
assert not comite_ok(2, 3, "practicas", control_50=True, revelado=False)
assert not comite_ok(2, 3, "auditoria", control_50=True, revelado=True)   # la excepción no alcanza al comité de auditoría

# Independencia, fr. IV: un consejero que es socio de un proveedor que vende 60 a la sociedad.
# Lo que cuenta es lo que la SOCIEDAD representa en las ventas del proveedor: 60 / 500 = 12% > 10%, importante; 60 / 800 = 7.5%, no.
assert proveedor_importante(60, 500) and not proveedor_importante(60, 800)
# Acreedor: crédito de 200; activos de la sociedad 1,500 (13.3%) y de la contraparte 1,200 (16.7%): importante por la contraparte.
assert deudor_acreedor_importante(200, 1500, 1200) and not deudor_acreedor_importante(200, 1500, 2000)
# Exauditor externo: a los 10 meses no puede ser consejero; a los 13, sí.
assert not puede_ser_consejero(10) and puede_ser_consejero(13)

print("Mínimo de independientes por tamaño del consejo:", minimo)
print("Proveedor que vende 60 con ventas totales de 500: importante (12% > 10%); con 800: no (7.5%).")
print("Acreedor de 200: 13.3% de los activos de la sociedad y 16.7% de los de la contraparte: importante.")
print("Emisora controlada: prácticas societarias puede ir con mayoría de independientes si se revela; auditoría, siempre 100%.")
print("Todas las aserciones pasaron.")
