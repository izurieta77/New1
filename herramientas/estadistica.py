"""Inferencia robusta para series de rendimientos (solo biblioteca estandar).

- newey_west: media, error estandar HAC (kernel de Bartlett, correccion n/(n-1)),
  estadistico t e intervalo de confianza al 95%.
- ic_bootstrap_bloques: intervalo de la media por bootstrap de bloques moviles.
- veredicto: "apoyo" / "contraria" / "inconcluso" segun el intervalo.
- pesos_bartlett: pesos w_j = 1 - j/(L+1) del kernel de Bartlett (Newey-West 1987).
- contribuciones_nw: descompone S = gamma_0 + 2*suma w_j*gamma_j por rezago
  (Bartlett o uniforme truncado) para ver cuanto pesa cada autocovarianza.
- se_diferencia: error estandar de a - b con covarianza; dice si tratar b como
  fijo subestima o sobrestima el error estandar.

Notas de razonamiento (examen S6 del 2026-09-25, ver
conocimiento/fichas/2026-09-25-examen-S6-errores-de-razonamiento.md):
- Con Bartlett y L rezagos, el ultimo rezago pesa 1/(L+1): con L=6, gamma_6 entra
  con 2*(1/7)*gamma_6. No "compensa" a gamma_1, que entra con 2*(6/7)*gamma_1.
- Bartlett garantiza S >= 0 (NW 1987, Teorema 1: S = e'Pe/(L+1)); el kernel
  uniforme truncado no.
- Var(a - b) = Var(a) + Var(b) - 2 Cov(a, b). Tratar b como fijo subestima el
  error estandar solo si corr(a, b) < se_b / (2 se_a); si la correlacion es
  mayor (benchmark estimado con la misma muestra), la prueba es conservadora.
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


def pesos_bartlett(rezagos):
    """Pesos del kernel de Bartlett, w_j = 1 - j/(L+1) para j = 0..L.

    Newey y West (1986, NBER TWP 55, ec. 5; Econometrica 1987): w(j, m) = 1 - j/(m+1).
    El ultimo rezago pesa 1/(L+1) (1/7 con L=6) y la suma de w_1..w_L es L/2.
    """
    L = int(rezagos)
    if L < 0:
        raise ValueError("rezagos debe ser >= 0")
    return [1 - j / (L + 1) for j in range(L + 1)]


def autocovarianzas(x, rezagos):
    """gamma_j = (1/n) * suma_{t=j+1..n} (x_t - xbar)(x_{t-j} - xbar), j = 0..L."""
    n = len(x)
    if rezagos >= n:
        raise ValueError("rezagos debe ser menor que n")
    m = sum(x) / n
    u = [v - m for v in x]
    return [sum(u[i] * u[i - j] for i in range(j, n)) / n for j in range(rezagos + 1)]


def contribuciones_nw(x, rezagos=6, kernel="bartlett"):
    """Descompone la varianza de largo plazo S = gamma_0 + 2*suma_j w_j*gamma_j por rezago.

    kernel="bartlett": w_j = 1 - j/(L+1) (mismo S que newey_west; siempre >= 0).
    kernel="uniforme": w_j = 1 (truncado; S puede salir negativo).
    Devuelve gammas, pesos, contribuciones (c_0 = gamma_0, c_j = 2*w_j*gamma_j),
    S, se = raiz(S/(n-1)) (nan si S <= 0) y t.
    """
    n = len(x)
    if n < 3:
        raise ValueError("serie demasiado corta")
    if kernel == "bartlett":
        w = pesos_bartlett(rezagos)
    elif kernel == "uniforme":
        w = [1.0] * (rezagos + 1)
    else:
        raise ValueError("kernel debe ser 'bartlett' o 'uniforme'")
    g = autocovarianzas(x, rezagos)
    c = [g[0]] + [2 * w[j] * g[j] for j in range(1, rezagos + 1)]
    s = sum(c)
    m = sum(x) / n
    se = math.sqrt(s / (n - 1)) if s > 0 else float("nan")
    return {
        "n": n,
        "kernel": kernel,
        "rezagos": rezagos,
        "gammas": g,
        "pesos": w,
        "contribuciones": c,
        "S": s,
        "se": se,
        "t": m / se if s > 0 else float("nan"),
    }


def se_diferencia(se_a, se_b, corr):
    """Error estandar de a - b: raiz(se_a^2 + se_b^2 - 2*corr*se_a*se_b).

    Tratar b como fijo (usar solo se_a) subestima el error estandar si
    corr < se_b/(2*se_a) y lo sobrestima (prueba conservadora) si corr > ese umbral.
    """
    if not -1 <= corr <= 1:
        raise ValueError("corr debe estar en [-1, 1]")
    v = se_a ** 2 + se_b ** 2 - 2 * corr * se_a * se_b
    return math.sqrt(max(v, 0.0))
