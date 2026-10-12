"""D10 · IRC §1091 (venta ficticia) y §1256 (60/40 y marcar a mercado). Ejercicios con aserciones."""


def wash_sale(costo_viejo, venta, recompra):
    """Pérdida no deducible y base de las acciones recompradas (§1091(a) y (d))."""
    perdida = venta - costo_viejo
    if perdida >= 0:
        return 0.0, recompra
    no_deducible = -perdida
    base_nueva = costo_viejo + (recompra - venta)   # §1091(d): base vendida ± diferencia de precios
    return no_deducible, base_nueva


def tasa_1256(tasa_larga, tasa_corta):
    """§1256(a)(3): 60% largo plazo, 40% corto plazo, sin importar el tiempo de tenencia."""
    return 0.6 * tasa_larga + 0.4 * tasa_corta


if __name__ == "__main__":
    nd, base = wash_sale(5000, 4000, 4200)
    print("pérdida no deducible", nd, "base nueva", base)
    assert (nd, base) == (1000, 5200)
    # La pérdida no desaparece: se difiere. Si luego se vende en 4,800, la pérdida reconocida es 400 = 1000 diferidos - 600 de alza
    assert 4800 - base == -400
    # Tasas ilustrativas (parámetros, NO verificadas hoy contra el IRC §1(h) ni la tabla vigente)
    t = tasa_1256(0.20, 0.37)
    print("tasa combinada 60/40 con 20% y 37%:", round(t, 4))
    assert abs(t - 0.268) < 1e-12
