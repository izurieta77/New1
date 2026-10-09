"""D7: ISR incremental de una ganancia de un ETF de EUA (no cedular) para un residente en México.
Usa la tarifa anual 2026 ya verificada en 2026-10-07-principios-tributarios.py (LISR art. 152, Anexo 8 RMF 2026).
Escenarios: (a) ganancia 100,000 con salario S; (b) comparación con 10% cedular del art. 129 (solo bolsas mexicanas).
Supuesto del bloque 1: tenencia de 1 año, es decir, la ganancia entera se acumula (art. 120 LISR, fr. I con n = 1).
Corrección 9-oct-2026: para n > 1 años el art. 120 LISR reparte la ganancia; ver el bloque 2."""
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

# --- Bloque 2 (corrección 9-oct-2026): art. 120 LISR, ganancia por enajenación de bienes con n años de tenencia ---
# fr. I: la ganancia G se divide entre n años (sin exceder 20); fr. II: G/n se suma a los demás ingresos
# acumulables (tarifa del art. 152); fr. III: el resto (G - G/n) se multiplica por una tasa promedio.
# fr. III a) no dice si la base de la tasa incluye la parte no acumulable: se calculan las dos lecturas.
print("\nBloque 2 · Art. 120 LISR (tenencia de n años). Tasa total sobre G:")
for S in [0, 150_000, 300_000, 1_000_000]:
    for n in [1, 2, 5, 10]:
        acc = G / n
        inc = isr(S + acc) - isr(S)                   # fr. II
        base_a = S + acc                              # lectura A: base = ingresos acumulables
        tot_a = inc + (G - acc) * isr(base_a) / base_a
        base_b = S + G                                # lectura B: base incluye G completa
        tot_b = inc + (G - acc) * isr(base_b) / base_b
        print(f"  S={S:>9,} n={n:>2}: ISR total = {tot_a:12,.2f} (lectura A) {tot_a/G:6.2%} | lectura B {tot_b/G:6.2%}")
