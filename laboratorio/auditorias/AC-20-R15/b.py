"""AC-20-R15, ejecución B independiente: USD/MXN después de un episodio FX-1 (+6% sobre el mínimo de 15 días).

Solo biblioteca estándar. Uso: python3 -I b.py  (lee ./datos relativo a este archivo).
Fuente: FIX de Banxico (serie SF43718, columna "Determinación"), descargado de la consulta
pública sin token https://www.banxico.org.mx/tipcamb/tipCamIHAction.do (POST idioma=sp,
fechaInicial=01/11/1991, fechaFinal=15/10/2026, salida=HTML). Guardado comprimido con gzip.
"""
import datetime as dt
import gzip
import math
import os
import re
import statistics as st

AQUI = os.path.dirname(os.path.abspath(__file__))
ARCHIVO = os.path.join(AQUI, "datos", "banxico_fix_19911112_20261015.html.gz")
CORTE = dt.date(2026, 10, 15)
DESDE_ROBUSTEZ = dt.date(1996, 1, 1)
VENTANA_MIN = 15
UMBRAL = 0.06
SEP_EPISODIO = 20
HORIZONTES = (10, 20)
EXTRA = 0.03


def leer_banxico():
    """Devuelve [(fecha, fix)] ascendente y el conteo de días hábiles (lun-vie) sin dato."""
    with gzip.open(ARCHIVO, "rt", encoding="latin-1") as f:
        t = f.read()
    celdas = [c.strip() for c in re.findall(r"<td[^>]*>\s*([^<]*?)\s*</td>", t, re.S)]
    # Las celdas útiles son fechas dd/mm/aaaa, números o N/E. La tabla trae 4 columnas apiladas
    # (Fecha, Determinación, Publicación DOF, Para solventar), cada una con el mismo número de filas.
    utiles = [c for c in celdas if re.fullmatch(r"\d\d/\d\d/\d{4}|\d+\.\d+|N/E", c)]
    fechas = [c for c in utiles if "/" in c and c != "N/E"]
    n = len(fechas)
    assert utiles[:n] == fechas, "la primera columna no son solo fechas"
    assert len(utiles) == 4 * n, (len(utiles), n)
    determinacion = utiles[n:2 * n]
    serie, sin_dato_habil = [], []
    for fs, v in zip(fechas, determinacion):
        d = dt.datetime.strptime(fs, "%d/%m/%Y").date()
        if d > CORTE:
            continue
        if v == "N/E":
            if d.weekday() < 5:
                sin_dato_habil.append(d)
            continue
        serie.append((d, float(v)))
    serie.sort()
    assert all(serie[i][0] < serie[i + 1][0] for i in range(len(serie) - 1))
    return serie, sorted(sin_dato_habil)


def eventos(x, signo):
    """Índices t con x_t >= 1.06*min(x[t-15..t-1]) (signo=+1) o x_t <= 0.94*max(...) (signo=-1)."""
    out = []
    for t in range(VENTANA_MIN, len(x)):
        previos = x[t - VENTANA_MIN:t]
        if signo > 0 and x[t] >= (1 + UMBRAL) * min(previos):
            out.append(t)
        if signo < 0 and x[t] <= (1 - UMBRAL) * max(previos):
            out.append(t)
    return out


def episodios(ev, modo="encadenado"):
    """Primer día de cada episodio. encadenado: se une si dista < 20 del evento anterior.
    ancla: se une si dista < 20 del primer día del episodio (sensibilidad)."""
    primeros, ultimo, ancla = [], None, None
    for t in ev:
        ref = ultimo if modo == "encadenado" else ancla
        if ref is None or t - ref >= SEP_EPISODIO:
            primeros.append(t)
            ancla = t
        ultimo = t
    return primeros


def tstat(v):
    if len(v) < 2:
        return float("nan")
    s = st.stdev(v)
    return st.mean(v) / (s / math.sqrt(len(v))) if s > 0 else float("nan")


def analiza(serie, desde, h, signo, modo="encadenado"):
    s = [p for p in serie if p[0] >= desde]
    f = [p[0] for p in s]
    x = [p[1] for p in s]
    ev = eventos(x, signo)
    ep = episodios(ev, modo)
    completos = [t for t in ep if t + h < len(x)]
    incompletos = [t for t in ep if t + h >= len(x)]
    cambio = [x[t + h] / x[t] - 1 for t in completos]
    maxv = [max(x[t + 1:t + h + 1]) / x[t] - 1 for t in completos]
    minv = [min(x[t + 1:t + h + 1]) / x[t] - 1 for t in completos]
    inc = [x[t + h] / x[t] - 1 for t in range(len(x) - h)]
    inc_max = [max(x[t + 1:t + h + 1]) / x[t] - 1 for t in range(len(x) - h)]
    inc_min = [min(x[t + 1:t + h + 1]) / x[t] - 1 for t in range(len(x) - h)]
    if signo > 0:
        frec_pp = sum(c >= EXTRA for c in cambio) / len(cambio)
        frec_max = sum(c >= EXTRA for c in maxv) / len(maxv)
        inc_pp = sum(c >= EXTRA for c in inc) / len(inc)
        inc_mx = sum(c >= EXTRA for c in inc_max) / len(inc_max)
    else:  # espejo: "otro -3% o más"
        frec_pp = sum(c <= -EXTRA for c in cambio) / len(cambio)
        frec_max = sum(c <= -EXTRA for c in minv) / len(minv)
        inc_pp = sum(c <= -EXTRA for c in inc) / len(inc)
        inc_mx = sum(c <= -EXTRA for c in inc_min) / len(inc_min)
    return dict(
        f=f, x=x, ev=ev, ep=ep, completos=completos, incompletos=incompletos, cambio=cambio,
        maxv=maxv, minv=minv, media=st.mean(cambio), mediana=st.median(cambio),
        t=tstat(cambio), inc_media=st.mean(inc), frec_pp=frec_pp, frec_max=frec_max,
        inc_pp=inc_pp, inc_mx=inc_mx, n_dias=len(x), positivos=sum(c > 0 for c in cambio),
    )


def pct(v):
    return f"{100 * v:+.2f}%"


def main():
    serie, sin_dato = leer_banxico()
    L = []
    p = L.append
    p("AC-20-R15 ejecución B. Fuente: FIX Banxico (SF43718, columna Determinación).")
    p(f"Serie: {serie[0][0]} a {serie[-1][0]}, {len(serie)} días con dato. Corte {CORTE}.")
    p(f"Días hábiles lun-vie sin dato (N/E, feriados MX) descartados: {len(sin_dato)}.")
    saltos = [(serie[i][0], serie[i][1] / serie[i - 1][1] - 1) for i in range(1, len(serie))
              if abs(serie[i][1] / serie[i - 1][1] - 1) > 0.08]
    p(f"Cambios diarios > 8% en valor absoluto (control de redenominación/errores): {[(str(d), round(100*r,2)) for d, r in saltos]}")
    p("")
    variantes = [("serie completa", serie[0][0]), ("desde 1996-01-01", DESDE_ROBUSTEZ)]
    resultados = {}
    for signo, nombre in ((+1, "AL ALZA (FX-1)"), (-1, "ESPEJO A LA BAJA (informativo)")):
        p("=" * 100)
        p(f"{nombre}")
        p("=" * 100)
        for etiqueta, desde in variantes:
            for h in HORIZONTES:
                r = analiza(serie, desde, h, signo)
                resultados[(signo, etiqueta, h)] = r
                p(f"-- {etiqueta}, h={h}: días={r['n_dias']}, eventos={len(r['ev'])}, episodios={len(r['ep'])}"
                  f" (con ventana completa {len(r['completos'])}; sin ventana completa: "
                  f"{[str(r['f'][t]) for t in r['incompletos']]})")
                p(f"   media posterior {pct(r['media'])} | mediana {pct(r['mediana'])} | t {r['t']:+.2f}"
                  f" | incondicional {pct(r['inc_media'])} | >0: {r['positivos']}/{len(r['cambio'])}")
                extra = "+3% o más" if signo > 0 else "-3% o más"
                p(f"   frecuencia {extra} punto a punto: {100*r['frec_pp']:.1f}% (incondicional {100*r['inc_pp']:.1f}%)"
                  f" | en algún día de la ventana: {100*r['frec_max']:.1f}% (incondicional {100*r['inc_mx']:.1f}%)")
        p("")
    # Detalle de episodios al alza (serie completa, ambos horizontes)
    p("Detalle de episodios al alza (serie completa). Fecha, nivel, alza sobre mín 15d, cambio 10d, 20d, máx 20d")
    r10 = resultados[(+1, "serie completa", 10)]
    r20 = resultados[(+1, "serie completa", 20)]
    x, f = r10["x"], r10["f"]
    for t in r10["ep"]:
        alza = x[t] / min(x[t - VENTANA_MIN:t]) - 1
        c10 = pct(x[t + 10] / x[t] - 1) if t + 10 < len(x) else "n/d"
        c20 = pct(x[t + 20] / x[t] - 1) if t + 20 < len(x) else "n/d"
        m20 = pct(max(x[t + 1:t + 21]) / x[t] - 1) if t + 20 < len(x) else "n/d"
        p(f"  {f[t]}  {x[t]:9.4f}  {pct(alza)}  10d {c10:>8}  20d {c20:>8}  máx20 {m20:>8}")
    p("")
    p("Detalle de episodios a la baja (serie completa): fecha, nivel, cambio 20d")
    rb = resultados[(-1, "serie completa", 20)]
    for t in rb["ep"]:
        c20 = pct(rb["x"][t + 20] / rb["x"][t] - 1) if t + 20 < len(rb["x"]) else "n/d"
        p(f"  {rb['f'][t]}  {rb['x'][t]:9.4f}  20d {c20}")
    p("")
    # Sensibilidad: agrupación anclada al primer día
    p("Sensibilidad de agrupación (unir si < 20 días del PRIMER día del episodio, no del evento anterior):")
    for etiqueta, desde in variantes:
        for h in HORIZONTES:
            r = analiza(serie, desde, h, +1, modo="ancla")
            p(f"  {etiqueta}, h={h}: episodios={len(r['ep'])}, media {pct(r['media'])}, t {r['t']:+.2f},"
              f" frec +3% pp {100*r['frec_pp']:.1f}%")
    # Sensibilidad: desde 1996 filtrando episodios de la serie completa
    p("Sensibilidad 'desde 1996' = episodios de la serie completa con primer día >= 1996-01-01:")
    for h in HORIZONTES:
        r = resultados[(+1, "serie completa", h)]
        sel = [(t, c) for t, c in zip(r["completos"], r["cambio"]) if r["f"][t] >= DESDE_ROBUSTEZ]
        v = [c for _, c in sel]
        p(f"  h={h}: episodios={len(v)}, media {pct(st.mean(v))}, t {tstat(v):+.2f},"
          f" frec +3% pp {100*sum(c >= EXTRA for c in v)/len(v):.1f}%")
    p("")
    # Veredicto sobre la principal
    r = resultados[(+1, "desde 1996-01-01", 20)]
    h1 = r["media"] < r["inc_media"] and r["t"] <= -1.0
    h2 = r["frec_pp"] < 0.30
    p("VEREDICTO (principal: 20 días, desde 1996, frecuencia punto a punto):")
    p(f"  H1 reversión: media {pct(r['media'])} vs incondicional {pct(r['inc_media'])}, t {r['t']:+.2f}"
      f" -> {'SOSTENIDA' if h1 else 'REFUTADA'}")
    p(f"  H2 no continuación: frecuencia +3% {100*r['frec_pp']:.1f}% (umbral 30%) -> {'SOSTENIDA' if h2 else 'REFUTADA'}")
    estado = "Replicado" if (h1 and h2) else ("Replicado con diferencias" if (h1 or h2) else "No replicado")
    p(f"  Estado según §2: {estado}")
    texto = "\n".join(L)
    print(texto)
    with open(os.path.join(AQUI, "salida.txt"), "w", encoding="utf-8") as fo:
        fo.write(texto + "\n")


if __name__ == "__main__":
    main()
