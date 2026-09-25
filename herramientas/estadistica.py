"""Inferencia robusta para series de rendimientos (solo biblioteca estandar).

- newey_west: media, error estandar HAC (kernel de Bartlett, correccion n/(n-1)),
  estadistico t e intervalo de confianza al 95%.
- ic_bootstrap_bloques: intervalo de la media por bootstrap de bloques moviles.
- veredicto: "apoyo" / "contraria" / "inconcluso" segun el intervalo.
"""
import math
import random
import statistics

Z95 = 1.959963984540054


def newey_west(x, rezagos=6):
    """Media y error estandar Newey-West de una serie (misma unidad que x)."""
    n = len(x)
    if n < 3:
        raise ValueError("serie demasiado corta")
    m = sum(x) / n
    u = [v - m for v in x]
    omega = sum(a * a for a in u) / n
    for j in range(1, rezagos + 1):
        peso = 1 - j / (rezagos + 1)
        omega += 2 * peso * sum(u[i] * u[i - j] for i in range(j, n)) / n
    se = math.sqrt(omega / n * n / (n - 1))
    return {
        "n": n,
        "media": m,
        "se": se,
        "t": m / se if se > 0 else float("nan"),
        "t_iid": m / (statistics.stdev(x) / math.sqrt(n)),
        "ic95": (m - Z95 * se, m + Z95 * se),
        "rezagos": rezagos,
    }


def ic_bootstrap_bloques(x, bloque=12, repeticiones=5000, semilla=7, nivel=0.95):
    """Intervalo de la media por bootstrap de bloques moviles (respeta autocorrelacion)."""
    n = len(x)
    rng = random.Random(semilla)
    medias = []
    for _ in range(repeticiones):
        muestra = []
        while len(muestra) < n:
            i = rng.randrange(0, n - bloque + 1)
            muestra.extend(x[i:i + bloque])
        medias.append(sum(muestra[:n]) / n)
    medias.sort()
    a = (1 - nivel) / 2
    return medias[int(a * repeticiones)], medias[int((1 - a) * repeticiones) - 1]


def veredicto(ic):
    """Regla pre-registrable: apoyo si el limite inferior > 0, contraria si el superior < 0."""
    lo, hi = ic
    if lo > 0:
        return "apoyo"
    if hi < 0:
        return "contraria"
    return "inconcluso"
