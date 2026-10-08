"""D7: ISR incremental de una ganancia de un ETF de EUA (no cedular) para un residente en México.
Usa la tarifa anual 2026 ya verificada en 2026-10-07-principios-tributarios.py (LISR art. 152, Anexo 8 RMF 2026).
Escenarios: (a) ganancia 100,000 con salario S; (b) comparación con 10% cedular del art. 129 (solo bolsas mexicanas)."""
import importlib.util, pathlib
spec = importlib.util.spec_from_file_location("p", pathlib.Path(__file__).with_name("2026-10-07-principios-tributarios.py"))
p = importlib.util.module_from_spec(spec); spec.loader.exec_module(p)
isr = p.isr_tarifa

G = 100_000.0
TASA_129 = 0.10
print("Ganancia G =", G, "| cedular 10% =", round(TASA_129 * G, 2))
for S in [0, 150_000, 300_000, 1_000_000]:
    inc = isr(S + G) - isr(S)
    print(f"salario S={S:>9,}: ISR incremental por G = {inc:12,.2f}  tasa efectiva sobre G = {inc/G:6.2%}  vs 10% = {inc-TASA_129*G:+12,.2f}")
# punto de equilibrio: G tal que ISR incremental = 10% G (con S = 0 y con S = 150,000)
for S in [0, 150_000]:
    lo, hi = 1.0, 5_000_000.0
    f = lambda g: (isr(S + g) - isr(S)) - TASA_129 * g
    if f(lo) * f(hi) < 0:
        for _ in range(200):
            mid = (lo + hi) / 2
            (lo, hi) = (lo, mid) if f(lo) * f(mid) <= 0 else (mid, hi)
        print(f"equilibrio con S={S:,}: G* = {(lo+hi)/2:,.2f} (por debajo, la tarifa general es menor que el 10%)")
    else:
        print(f"S={S:,}: sin cruce en el rango")
