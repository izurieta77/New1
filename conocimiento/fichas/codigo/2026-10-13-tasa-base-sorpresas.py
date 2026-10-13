"""Tasa base de sorpresas de resultados (FactSet) y costo en Brier de ignorarla."""
from statistics import NormalDist


def brier_esperado(p, q):
    """Brier esperado de pronosticar p cuando la probabilidad verdadera es q."""
    return q * (1 - p) ** 2 + (1 - q) * p ** 2


if __name__ == "__main__":
    q = 0.70  # ingresos arriba del consenso, promedio de 5 años (FactSet, 31-jul-2026)
    for p in (0.50, 0.57, 0.70):
        print(f"pronóstico {p:.2f} con q={q}: Brier esperado {brier_esperado(p, q):.4f}")
    assert abs(brier_esperado(0.70, 0.70) - 0.21) < 1e-12
    assert abs(brier_esperado(0.50, 0.70) - 0.25) < 1e-12
    # Si la sorpresa (real - consenso)/sigma ~ N(mu, 1) y P(sorpresa > 0) = q, el sesgo implícito del consenso es mu = z(q)
    mu = NormalDist().inv_cdf(q)
    print(f"sesgo implícito del consenso (en desviaciones): {mu:.3f}")
    assert abs(mu - 0.5244) < 1e-3
    # Pronósticos de 'ingresos > consenso' registrados el 25-sep para el 3T26
    nuestros = {"JPM": 0.50, "WFC": 0.57, "GS": 0.58, "BAC": 0.13, "MS": 0.53, "JNJ": 0.72, "UNH": 0.62, "AMX": 0.45}
    media = sum(nuestros.values()) / len(nuestros)
    print(f"media de nuestros pronósticos: {media:.3f} contra tasa base {q}")
    assert round(media, 3) == 0.512
