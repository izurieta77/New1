"""Ficha 2026-10-06: costos relevantes, utilidad contable contra efectivo y sobreendeudamiento.

Cinco ejercicios numericos con cifras inventadas (didacticas), verificados con calculo directo:
1. Linea de producto "con perdida" tras repartir gastos fijos: quitarla ¿sube o baja la utilidad total?
2. Costo hundido: terminar o abandonar un proyecto a medias.
3. Costo de oportunidad de la capacidad: pedido especial con capacidad limitada.
4. Utilidad contable contra efectivo: conversion de efectivo y razon de devengos (Sloan, 1996).
5. Sobreendeudamiento (Myers, 1977): un proyecto con VPN positivo que los accionistas rechazan.
Solo stdlib. Uso: python3 conocimiento/fichas/codigo/2026-10-06-costos-relevantes-y-deuda.py
"""


def ej1():
    print("== 1. Linea de producto con perdida tras repartir gastos fijos ==")
    prod = {"A": (500, 300), "B": (300, 180), "C": (200, 175)}  # ingreso, costo variable
    fijos = 150
    ing_total = sum(i for i, _ in prod.values())
    util = {}
    for k, (i, v) in prod.items():
        asignado = fijos * i / ing_total
        util[k] = i - v - asignado
        print(f"{k}: ingreso {i}, variable {v}, margen de contribucion {i-v}, gasto fijo repartido {asignado:.0f}, utilidad {util[k]:+.0f}")
    total = sum(util.values())
    sin_c = sum(i - v for k, (i, v) in prod.items() if k != "C") - fijos
    print(f"utilidad total con C: {total:+.0f}; sin C (los {fijos} de gasto fijo siguen): {sin_c:+.0f}; cambio {sin_c-total:+.0f} = margen de contribucion de C ({prod['C'][0]-prod['C'][1]})")
    assert abs(total - 195) < 1e-9 and abs(sin_c - 170) < 1e-9


def ej2():
    print("\n== 2. Costo hundido ==")
    gastado, falta = 60, 40
    for valor_terminado, rescate in ((70, 10), (30, 10)):
        terminar = valor_terminado - falta
        decision = "terminar" if terminar > rescate else "abandonar"
        print(f"ya gastado {gastado} (irrelevante); terminar: {valor_terminado}-{falta} = {terminar:+} contra abandonar: {rescate:+} -> {decision}")


def ej3():
    print("\n== 3. Costo de oportunidad de la capacidad ==")
    precio, variable, alterno = 12, 8, 6
    margen_pedido = precio - variable
    print(f"pedido especial: margen {margen_pedido}/unidad contra {alterno}/unidad que se deja de ganar al ocupar la capacidad -> "
          f"{'aceptar' if margen_pedido > alterno else 'rechazar'}; con capacidad ociosa el costo de oportunidad es 0 y se acepta")


def ej4():
    print("\n== 4. Utilidad contable contra efectivo ==")
    ni, cfo, activos_ini, activos_fin = 100, 20, 1000, 1200
    conv = cfo / ni
    devengos = ni - cfo
    razon = devengos / ((activos_ini + activos_fin) / 2)
    print(f"utilidad neta {ni}, flujo operativo {cfo}: conversion de efectivo CFO/NI = {conv:.2f}; devengos {devengos}; razon de devengos = {razon:.1%} de los activos medios")
    print("lectura: utilidad sin efectivo (cuentas por cobrar o inventarios que crecen); en Sloan (1996) las empresas con devengos altos rinden menos despues")


def ej5():
    print("\n== 5. Sobreendeudamiento (Myers, 1977) ==")
    deuda, costo, pago_proy = 90, 10, 14
    estados = ((0.5, 100), (0.5, 40))  # (prob, valor de los activos actuales)

    def valores(extra):
        cap = sum(p * max(v + extra - deuda, 0) for p, v in estados)
        acr = sum(p * min(v + extra, deuda) for p, v in estados)
        return cap, acr

    cap0, acr0 = valores(0)
    cap1, acr1 = valores(pago_proy)
    print(f"sin proyecto: capital {cap0:.0f}, deuda {acr0:.0f}, total {cap0+acr0:.0f}")
    print(f"con proyecto (cuesta {costo}, paga {pago_proy} seguro): capital {cap1:.0f}, deuda {acr1:.0f}, total {cap1+acr1:.0f}")
    print(f"VPN del proyecto = {pago_proy-costo:+}; ganancia neta de los accionistas = {cap1-costo-cap0:+.0f}; de los acreedores = {acr1-acr0:+.0f}")
    print("-> los accionistas rechazan un proyecto con VPN positivo porque el beneficio va a los acreedores")
    assert abs((cap1 - costo - cap0) - (-3)) < 1e-9 and abs((acr1 - acr0) - 7) < 1e-9


if __name__ == "__main__":
    for f in (ej1, ej2, ej3, ej4, ej5):
        f()
