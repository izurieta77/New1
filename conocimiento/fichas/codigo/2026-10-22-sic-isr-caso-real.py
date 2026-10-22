"""Ficha 2026-10-22 · ISR (LISR art. 129) sobre ventas en el SIC: caso real del dueño.
Datos: correo de GBM del 7-oct (SPYM) en bitacora/real/operaciones.csv y capturas del dueño del 22-oct
(datos/entrada-dueno/2026-10-22.md). Comisión GBM: 0.25% + IVA 16% (correo de GBM: 12.36 + 1.98 = 14.34).
Solo ilustra la mecánica; no es una declaración ni una recomendación."""

COM = 0.0025 * 1.16          # comisión + IVA por operación
TASA = 0.10                  # art. 129, pago definitivo

def com(monto):
    return round(monto * COM, 2)

# --- Caso 1: SPYM del sublibro de Claude (3 títulos) ---
compra_mxn = 3 * 1648.50                     # 4,945.50 (correo GBM)
com_compra = 14.34                           # correo GBM
assert abs(com(compra_mxn) - com_compra) < 0.02
costo = compra_mxn + com_compra              # costo promedio x 3, sin actualización (ver abajo)
venta_mxn = 5043.00                          # valor SIC del 22-oct 10:45 (captura)
neto_venta = venta_mxn - com(venta_mxn)
gan_spym = round(neto_venta - costo, 2)
print(f"SPYM: venta neta {neto_venta:,.2f} - costo {costo:,.2f} = ganancia fiscal {gan_spym:,.2f}; ISR {TASA*gan_spym:,.2f}")

# Descomposición precio vs. tipo de cambio
fx0, usd0 = 17.985, 1648.50 / 17.985          # 7-oct (operaciones.csv)
fx1 = 18.7468                                 # MXN=X ~13:00 UTC 22-oct (brief)
usd1 = 5043.00 / 3 / fx1
r_usd, r_fx = usd1 / usd0 - 1, fx1 / fx0 - 1
r_mxn = (1 + r_usd) * (1 + r_fx) - 1
print(f"SPYM en USD {r_usd:+.2%}; dólar {r_fx:+.2%}; en MXN {r_mxn:+.2%} (captura: +1.97%)")
assert abs(r_mxn - (5043.00 / compra_mxn - 1)) < 1e-9

# --- Caso 2: todo el SIC de la captura (seis emisoras), suma de ganancias y pérdidas del ejercicio ---
# Ganancia o pérdida contra costo según GBM (sin comisiones); valor de mercado.
pos = {"SPYM": (5043.00, 97.50), "NFLX": (5032.52, 144.12), "NVDA": (3980.00, -286.00),
       "UBER": (3833.58, -120.42), "FSLR": (3175.00, -9.00), "LULU": (1855.00, 45.00)}

def resultado(tickers):
    total = 0.0
    for t in tickers:
        valor, gp = pos[t]
        costo_t = valor - gp
        total += (valor - com(valor)) - (costo_t + com(costo_t))   # comisiones de venta y de compra (supuesto 0.29%)
    return round(total, 2)

todo = resultado(pos)
ganadoras = resultado(["SPYM", "NFLX", "LULU"])
perdedoras = resultado(["NVDA", "UBER", "FSLR"])
print(f"Vender todo: resultado {todo:,.2f} -> ISR {max(0, TASA*todo):,.2f}; constancia de pérdida {max(0,-todo):,.2f}")
print(f"Vender solo ganadoras: {ganadoras:,.2f} -> ISR {TASA*max(0,ganadoras):,.2f}")
print(f"Vender solo perdedoras: {perdedoras:,.2f} -> pérdida compensable 10 años")
assert abs((ganadoras + perdedoras) - todo) < 0.02   # la suma entre emisoras es aditiva (2o párrafo del art. 129)
costo_ida_vuelta = sum(com(v) + com(v - g) for v, g in pos.values())
print(f"Comisiones de ida y vuelta de todo el SIC: {costo_ida_vuelta:,.2f} MXN")

# --- Caso 3: actualización del costo (art. 129 a) + art. 17-A CFF) ---
INPC = {"2025-12": None, "2026-01": 143.588, "2026-03": 145.544, "2026-08": 145.462}  # cap. 29 (INEGI)
def factor(inpc_reciente, inpc_antiguo):
    f = inpc_reciente / inpc_antiguo
    return max(1.0, f)    # art. 17-A: si es menor a 1, el factor es 1
# Compra en feb-2026 (mes anterior: ene), venta en sep-2026 (mes inmediato anterior: ago)
f1 = factor(INPC["2026-08"], INPC["2026-01"])
# Compra en abr-2026 (mes anterior: mar), venta en sep-2026
f2 = factor(INPC["2026-08"], INPC["2026-03"])
print(f"Factor feb->sep: {f1:.6f} (costo 10,000 -> {10000*f1:,.2f}); abr->sep: {f2:.6f}")
# Compra y venta en el mismo mes o el siguiente: sin periodo -> factor 1 (el caso real de oct-2026)

# --- Segunda comprobación, independiente: ISR por la vía de la descomposición USD x FX ---
gan_alt = 3 * usd0 * fx0 * ((1 + r_usd) * (1 + r_fx) - 1) - com(venta_mxn) - com_compra
assert abs(gan_alt - gan_spym) < 0.02, (gan_alt, gan_spym)
print("Segunda comprobación OK:", round(gan_alt, 2))
