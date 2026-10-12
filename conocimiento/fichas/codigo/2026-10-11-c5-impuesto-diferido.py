"""C5 · Impuesto diferido (NIC 12 / IAS 12) con reglas fiscales mexicanas (LISR 9, 34 fr. VII, 36 fr. II).

Supuestos simplificados (declarados en la ficha): años completos, sin actualización por inflación
de la deducción (LISR 31), sin valor residual, tasa 30% constante (LISR 9).
"""
TASA = 0.30


def calendario_equipo(costo=90_000, vida_contable=5, tasa_fiscal=0.30, anios=5):
    """Equipo de cómputo: contable en línea recta a 5 años; fiscal al 30% anual (LISR 34 fr. VII)."""
    filas, libros, base = [], costo, costo
    for a in range(1, anios + 1):
        libros -= costo / vida_contable
        base -= min(costo * tasa_fiscal, base)
        dif = libros - base                     # diferencia temporaria imponible si > 0
        filas.append((a, round(libros, 2), round(base, 2), round(dif, 2), round(dif * TASA, 2)))
    return filas


def provision_vacaciones(monto=50_000):
    """Pasivo contable que solo se deduce al pagarse: base fiscal del pasivo = 0 -> diferencia deducible."""
    return {"anio_1_activo_diferido": monto * TASA, "anio_2_reversa": -monto * TASA}


def automovil(costo=300_000, tope=175_000):
    """Parte no deducible por el tope del LISR 36 fr. II: nunca se deducirá."""
    return {"deducible": min(costo, tope), "no_deducible": max(costo - tope, 0)}


if __name__ == "__main__":
    print("Año | Libros | Base fiscal | Diferencia | Pasivo diferido (30%)")
    for f in calendario_equipo():
        print(" | ".join(str(x) for x in f))
    print(provision_vacaciones())
    print(automovil())
    cal = calendario_equipo()
    assert [f[4] for f in cal] == [2700.0, 5400.0, 8100.0, 5400.0, 0.0]
    assert provision_vacaciones()["anio_1_activo_diferido"] == 15000.0
    assert automovil() == {"deducible": 175000, "no_deducible": 125000}
    # Movimiento del pasivo diferido en resultados: gasto (+) o beneficio (-) por año
    movs = [cal[0][4]] + [round(cal[i][4] - cal[i - 1][4], 2) for i in range(1, len(cal))]
    assert movs == [2700.0, 2700.0, 2700.0, -2700.0, -5400.0] and round(sum(movs), 2) == 0
    print("movimientos del diferido:", movs, "suma", sum(movs))
