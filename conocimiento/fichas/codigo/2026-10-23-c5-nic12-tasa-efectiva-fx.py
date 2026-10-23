"""Ficha 2026-10-23 · C5 · NIC 12 §41: tasa efectiva de una emisora con moneda funcional USD y base fiscal en MXN.
Ilustrativo (cifras redondas), con la regla literal del §41 y el §47 (tasa promulgada) de AASB 112 = IAS 12."""
T = 0.30   # LISR art. 9 (tasa de personas morales)

def periodo(fx0, fx1, valor_usd=1000.0, utilidad_usd=200.0, inpc=0.0, reconocer_activo=True):
    """Activo no monetario de valor en libros fijo en USD; base fiscal en MXN (actualizada por INPC).
    Devuelve (impuesto diferido del periodo en USD, tasa efectiva)."""
    base_mxn0 = valor_usd * fx0               # al inicio la base en USD coincide con el valor en libros
    base_mxn1 = base_mxn0 * (1 + inpc)        # actualización fiscal (deducción de inversiones actualizada)
    base_usd1 = base_mxn1 / fx1
    dif_temp = valor_usd - base_usd1          # >0: gravable (pasivo); <0: deducible (activo)
    dif_imp = T * dif_temp
    if dif_imp < 0 and not reconocer_activo:  # §24/§34: el activo solo si es probable recuperarlo
        dif_imp = 0.0
    corriente = T * utilidad_usd              # sin otras partidas permanentes
    return dif_imp, (corriente + dif_imp) / utilidad_usd

casos = [("peso se deprecia 17.00 → 18.70", 17.0, 18.7, 0.0, True),
         ("peso se aprecia 17.00 → 16.00", 17.0, 16.0, 0.0, True),
         ("aprecia, activo no reconocido (§24)", 17.0, 16.0, 0.0, False),
         ("deprecia 10% con INPC +10% en la base", 17.0, 18.7, 0.10, True),
         ("3T26 real del USD/MXN 17.449 → 18.061", 17.449, 18.061, 0.0, True)]
for nombre, a, b, i, r in casos:
    d, etr = periodo(a, b, inpc=i, reconocer_activo=r)
    print(f"{nombre:42s} diferido {d:+7.2f} USD · tasa efectiva {etr:6.1%}")

# Segunda comprobación, por otra vía: el diferido es T × valor × (1 − (1+inpc)·fx0/fx1)
for nombre, a, b, i, r in casos:
    d, _ = periodo(a, b, inpc=i, reconocer_activo=r)
    alt = T * 1000 * (1 - (1 + i) * a / b)
    if r or alt > 0:
        assert abs(d - alt) < 1e-9, nombre
print("Segunda comprobación OK")

# Sensibilidad: puntos de tasa efectiva por cada 1% que se deprecia el peso, con base fiscal = 5× la utilidad
for ratio in (2, 5, 10):
    d, etr = periodo(17.0, 17.0 * 1.01, valor_usd=200.0 * ratio)
    print(f"base/utilidad = {ratio:2d}: +1% del dólar → tasa efectiva {etr:.1%} (+{(etr - T) * 100:.1f} pp)")
