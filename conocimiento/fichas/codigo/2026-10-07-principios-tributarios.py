"""Doctorado derecho fiscal D1: progresividad de la tarifa anual 2026 (arts. 97 y 152 LISR,
Anexo 8 RMF 2026, apartado C, fr. II, DOF 28-12-2025) frente a la tasa cedular plana de 10%
sobre la ganancia en bolsa (art. 129 LISR, pago definitivo).

Cifras copiadas del Anexo 8 (PDF del SAT, sha256 inicia 69ebaf8a78a3bde5).
Simplificaciones: base gravable = ingreso ya neto de deducciones; sin deducciones personales
(art. 151), sin subsidio, sin actualización de costo; ganancia 100% en el supuesto del art. 129.
"""

# (límite inferior, límite superior, cuota fija, % sobre excedente del límite inferior)
TARIFA_2026 = [
    (0.01, 10_135.11, 0.00, 1.92),
    (10_135.12, 86_022.11, 194.59, 6.40),
    (86_022.12, 151_176.19, 5_051.37, 10.88),
    (151_176.20, 175_735.66, 12_140.13, 16.00),
    (175_735.67, 210_403.69, 16_069.64, 17.92),
    (210_403.70, 424_353.97, 22_282.14, 21.36),
    (424_353.98, 668_840.14, 67_981.92, 23.52),
    (668_840.15, 1_276_925.98, 125_485.07, 30.00),
    (1_276_925.99, 1_702_567.97, 307_910.81, 32.00),
    (1_702_567.98, 5_107_703.92, 444_116.23, 34.00),
    (5_107_703.93, float("inf"), 1_601_862.46, 35.00),
]
TASA_129 = 0.10

# --- Comprobación 0: consistencia interna de la tabla publicada -------------------------
for k in range(len(TARIFA_2026) - 1):
    li, ls, cf, t = TARIFA_2026[k]
    li2, _, cf2, _ = TARIFA_2026[k + 1]
    assert abs(li2 - ls - 0.01) < 1e-6, f"hueco entre tramos {k}"
    cf_calc = cf + (li2 - li) * t / 100          # cuota del tramo siguiente implícita
    assert abs(cf_calc - cf2) < 0.05, (k, cf_calc, cf2)


def isr_tarifa(base: float) -> float:
    """Método A: cuota fija + % sobre el excedente del límite inferior (como lo aplica el SAT)."""
    if base <= 0:
        return 0.0
    for li, ls, cf, t in TARIFA_2026:
        if li <= base <= ls + 0.0099:
            return cf + (base - li) * t / 100
    raise ValueError(base)


def isr_marginal(base: float) -> float:
    """Método B (segunda comprobación, independiente de la cuota fija): suma tramo por tramo."""
    imp, previo = 0.0, 0.0
    for _, ls, _, t in TARIFA_2026:
        tope = min(base, ls)
        if tope > previo:
            imp += (tope - previo) * t / 100
        previo = ls
        if base <= ls:
            break
    return imp


def marginal(base: float) -> float:
    for li, ls, _, t in TARIFA_2026:
        if li <= base <= ls + 0.0099:
            return t
    return TARIFA_2026[-1][3]


print("1) Progresividad de la tarifa anual 2026 (art. 152): tasa efectiva y marginal")
print(f"{'base gravable':>15} {'ISR (A)':>14} {'ISR (B)':>14} {'efectiva':>9} {'marginal':>9}")
niveles = [50_000, 100_000, 250_000, 500_000, 1_000_000, 2_000_000, 5_000_000, 10_000_000, 50_000_000]
prev_ef = 0.0
for b in niveles:
    a, bb = isr_tarifa(b), isr_marginal(b)
    assert abs(a - bb) < 1.0, (b, a, bb)      # difieren solo por redondeo de cuotas publicadas
    ef = a / b
    assert ef > prev_ef                         # efectiva estrictamente creciente = progresiva
    prev_ef = ef
    print(f"{b:>15,.0f} {a:>14,.2f} {bb:>14,.2f} {ef:>8.2%} {marginal(b):>8.2f}%")
print(f"   La tasa efectiva tiende a 35% sin alcanzarla: a 50 M es {isr_tarifa(50e6)/50e6:.2%}")

print("\n2) Cedular plana (art. 129): misma tasa efectiva para cualquier monto de ganancia")
for g in [50_000, 1_000_000, 50_000_000]:
    print(f"   ganancia {g:>12,.0f} -> ISR {g*TASA_129:>12,.2f} = {TASA_129:.0%}")

print("\n3) ¿Cuánto costaría la misma ganancia de 500,000 si se acumulara a la tarifa? (ISR incremental)")
G = 500_000
print(f"{'otros ingresos':>15} {'ISR increm.':>13} {'tasa increm.':>12} {'cedular 10%':>12} {'diferencia':>12}")
for s in [0, 150_000, 400_000, 1_000_000, 3_000_000]:
    inc = isr_tarifa(s + G) - isr_tarifa(s)
    print(f"{s:>15,.0f} {inc:>13,.2f} {inc/G:>11.2%} {G*TASA_129:>12,.2f} {inc-G*TASA_129:>12,.2f}")

print("\n4) Equidad horizontal: dos personas con el mismo ingreso total de 1,000,000")
sal = isr_tarifa(1_000_000)
print(f"   A: 1,000,000 de salario          -> ISR {sal:,.2f} ({sal/1e6:.2%})")
print(f"   B: 1,000,000 de ganancia en bolsa -> ISR {1e6*TASA_129:,.2f} ({TASA_129:.2%})")
print(f"   B paga {sal - 1e6*TASA_129:,.2f} menos ({sal/(1e6*TASA_129):.2f} veces)")

print("\n5) Contraejemplo: el inversionista pequeño SIN otros ingresos paga MÁS con la cedular")
# punto de equilibrio: isr_tarifa(G)/G = 10% (bisección)
lo, hi = 10_000.0, 1_000_000.0
for _ in range(200):
    mid = (lo + hi) / 2
    if isr_tarifa(mid) / mid < TASA_129:
        lo = mid
    else:
        hi = mid
eq = (lo + hi) / 2
assert abs(isr_tarifa(eq) / eq - TASA_129) < 1e-9
print(f"   Equilibrio: ganancia única de {eq:,.2f} -> tarifa {isr_tarifa(eq):,.2f} = 10%")
for g in [30_000, 100_000, eq]:
    print(f"   ganancia {g:>10,.2f}: tarifa {isr_tarifa(g):>10,.2f} ({isr_tarifa(g)/g:.2%}) vs cedular {g*TASA_129:>10,.2f}")
# un contribuyente cuyo ingreso total queda en tramos con marginal < 10% no puede optar por acumular:
print("   (el pago del art. 129 es definitivo y el art. 152 excluye lo que ya pagó impuesto definitivo)")
