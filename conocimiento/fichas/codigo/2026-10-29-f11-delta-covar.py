"""Ficha 2026-10-29 · F11 · ΔCoVaR incondicional (Adrian y Brunnermeier, NBER w17454, ec. 2-5) con datos públicos.
Rendimientos semanales de precio (Yahoo, cierre ajustado, viernes) 2005-2026. Sistema: XLF (EUA) e ^MXX (México).
ΔCoVaR_i = β_q · (VaR_q,i − VaR_50,i), con β_q de la regresión cuantílica del sistema sobre la institución.
Regresión cuantílica sin numpy: para cada pendiente b la constante óptima es el cuantil q de (y − b x);
la pérdida perfilada es convexa en b → búsqueda ternaria.
Segunda comprobación: (a) calibración: fracción de semanas con el sistema bajo la recta cuantílica ≈ q;
(b) pendiente por rejilla exhaustiva (paso 0.005) contra la búsqueda ternaria.
Uso: python3 -I este.py"""
import json, urllib.request, urllib.parse, datetime as dt, statistics as st

def semanal(t):
    q = urllib.parse.urlencode({"period1": 1104537600, "period2": 1793000000, "interval": "1wk"})
    r = json.load(urllib.request.urlopen(urllib.request.Request(
        f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(t)}?{q}", headers={"User-Agent": "Mozilla/5.0"}), timeout=60))["chart"]["result"][0]
    adj = r["indicators"]["adjclose"][0]["adjclose"]
    s = {dt.datetime.utcfromtimestamp(a).date(): v for a, v in zip(r["timestamp"], adj) if v}
    d = sorted(s); return {b: s[b] / s[a] - 1 for a, b in zip(d, d[1:])}

def cuantil(v, q):
    v = sorted(v); k = (len(v) - 1) * q; f = int(k); c = min(f + 1, len(v) - 1)
    return v[f] + (v[c] - v[f]) * (k - f)

def perdida(y, x, q, b):
    r = [yi - b * xi for yi, xi in zip(y, x)]; a = cuantil(r, q)
    return sum((q - (e - a < 0)) * (e - a) for e in r), a

def qreg(y, x, q):
    lo, hi = -3.0, 3.0
    for _ in range(80):
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if perdida(y, x, q, m1)[0] < perdida(y, x, q, m2)[0]: hi = m2
        else: lo = m1
    b = (lo + hi) / 2; return perdida(y, x, q, b)[1], b

def delta_covar(sis, inst, q):
    f = sorted(set(sis) & set(inst))
    if len(f) < 150: return len(f), None, None, None, None
    y = [sis[d] for d in f]; x = [inst[d] for d in f]
    a, b = qreg(y, x, q)
    var_q, var_50 = cuantil(x, q), cuantil(x, 0.5)
    dcv = b * (var_q - var_50)
    # segunda comprobación: calibración y rejilla
    cal = sum(1 for yy, xx in zip(y, x) if yy < a + b * xx) / len(y)
    rej = min((perdida(y, x, q, k / 200)[0], k / 200) for k in range(-200, 401))[1]
    emp = (cal, rej)
    return len(f), b, var_q, dcv, emp

grupos = {"EUA (sistema XLF)": ("XLF", ["JPM", "BAC", "C", "WFC", "GS", "MS"]),
          "México (sistema ^MXX)": ("^MXX", ["GFNORTEO.MX", "BBAJIOO.MX", "GFINBURO.MX"])}
for g, (s, lst) in grupos.items():
    S = semanal(s); print(f"\n{g} · semanas de rendimiento de precio, 2005-2026")
    print("inst | n | q | β_q | VaR_q inst | ΔCoVaR (pp semanales) | calibración | β por rejilla")
    for i in lst:
        I = semanal(i)
        for q in (0.01, 0.05):
            n, b, vq, dcv, emp = delta_covar(S, I, q)
            if b is None: print(f"{i} | {n} | sin fechas comunes suficientes"); break
            print(f"{i} | {n} | {q:.0%} | {b:.3f} | {vq*100:.2f}% | {dcv*100:.2f} | {emp[0]:.3f} | {emp[1]:.3f}")
