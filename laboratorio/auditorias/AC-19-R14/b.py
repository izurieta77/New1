"""AC-19-R14, ejecución B independiente: rebote tras desplome de un día.

Solo biblioteca estándar. Uso: python3 -I b.py  (lee ./datos relativo a este archivo).
Fuentes:
  S&P 500   -> Yahoo chart v8 ^GSPC (parser propio); cotejo con FRED SP500 (2016+).
  Nasdaq    -> FRED NASDAQCOM.
  Nikkei    -> FRED NIKKEI225.
  KOSPI     -> Yahoo chart v8 ^KS11 (parser propio); no hubo fuente alterna accesible.
"""
import csv
import datetime as dt
import json
import math
import os
import statistics as st

AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(AQUI, "datos")
CORTE = dt.date(2026, 10, 14)
UMBRALES = (-0.05, -0.07)
HORIZONTES = (11, 22)
SEP_EPISODIO = 11  # desplomes a < 11 días hábiles del anterior = mismo episodio


def leer_fred(nombre):
    serie, vacios = [], 0
    with open(os.path.join(DATOS, nombre), newline="") as f:
        r = csv.reader(f)
        next(r)
        for fila in r:
            if len(fila) < 2 or fila[1].strip() in ("", "."):
                vacios += 1
                continue
            serie.append((dt.date.fromisoformat(fila[0]), float(fila[1])))
    return serie, vacios


def leer_yahoo(nombre):
    with open(os.path.join(DATOS, nombre)) as f:
        j = json.load(f)["chart"]["result"][0]
    off = j["meta"]["gmtoffset"]  # desfase de la bolsa (no ajusta horario de verano, basta para la fecha)
    ts = j["timestamp"]
    cl = j["indicators"]["quote"][0]["close"]
    serie, vacios, vistos = [], 0, set()
    for t, c in zip(ts, cl):
        d = (dt.datetime(1970, 1, 1) + dt.timedelta(seconds=t + off)).date()
        if c is None:
            vacios += 1
            continue
        if d in vistos:  # barra duplicada (día en curso)
            continue
        vistos.add(d)
        serie.append((d, float(c)))
    serie.sort()
    return serie, vacios


def limpiar(serie):
    """Corta al 14-oct-2026 y descarta cierres repetidos exactos (rendimiento cero)."""
    serie = [(d, c) for d, c in serie if d <= CORTE and c > 0]
    out, repetidos = [], []
    for d, c in serie:
        if out and c == out[-1][1]:
            repetidos.append(d)
            continue
        out.append((d, c))
    return out, repetidos


def tstat(xs):
    n = len(xs)
    if n < 2:
        return float("nan")
    s = st.stdev(xs)
    return st.mean(xs) / (s / math.sqrt(n)) if s > 0 else float("nan")


def eventos(serie, umbral, h):
    """Lista de (indice_dia, fecha, r_dia, r_h) para cada desplome con ventana completa."""
    c = [x[1] for x in serie]
    ev, sin_ventana = [], []
    for i in range(1, len(c)):
        r = c[i] / c[i - 1] - 1
        if r <= umbral:
            if i + h < len(c):
                ev.append((i, serie[i][0], r, c[i + h] / c[i] - 1))
            else:
                sin_ventana.append(serie[i][0])
    return ev, sin_ventana


def incondicional(serie, h):
    c = [x[1] for x in serie]
    rs = [c[i + h] / c[i] - 1 for i in range(len(c) - h)]
    return st.mean(rs), sum(1 for x in rs if x > 0) / len(rs)


def episodios(ev):
    """Agrupa eventos (ordenados) en episodios: nuevo episodio si la distancia al
    desplome anterior es >= SEP_EPISODIO días hábiles."""
    grupos = []
    for e in ev:
        if grupos and e[0] - grupos[-1][-1][0] < SEP_EPISODIO:
            grupos[-1].append(e)
        else:
            grupos.append([e])
    return grupos


def main():
    out = []
    p = out.append
    crudos = {
        "S&P 500 (Yahoo ^GSPC)": leer_yahoo("yahoo_GSPC.json"),
        "Nasdaq (FRED NASDAQCOM)": leer_fred("fred_NASDAQCOM.csv"),
        "Nikkei (FRED NIKKEI225)": leer_fred("fred_NIKKEI225.csv"),
        "KOSPI (Yahoo ^KS11)": leer_yahoo("yahoo_KS11.json"),
    }
    series = {}
    p("AC-19-R14 ejecución B  |  corte de datos: 2026-10-14 (15-oct-2026 excluido)")
    p("")
    p("== Limpieza ==")
    for k, (s, vac) in crudos.items():
        limpia, rep = limpiar(s)
        series[k] = limpia
        p(f"{k}: {limpia[0][0]} a {limpia[-1][0]}, {len(limpia)} cierres; "
          f"sin cierre descartados {vac}; cierres repetidos descartados {len(rep)}"
          + (f" (primeros: {', '.join(str(d) for d in rep[:5])})" if rep else ""))
    p("")

    # Cotejo S&P Yahoo vs FRED en el traslape
    fred_sp, _ = leer_fred("fred_SP500.csv")
    fred_sp, _ = limpiar(fred_sp)
    y = dict(series["S&P 500 (Yahoo ^GSPC)"])
    com = [(d, c) for d, c in fred_sp if d in y]
    maxdif = max(abs(c / y[d] - 1) for d, c in com)
    p(f"Cotejo S&P: FRED SP500 vs Yahoo ^GSPC, {len(com)} fechas comunes "
      f"({com[0][0]} a {com[-1][0]}), máx. dif. relativa de cierre {maxdif:.2e}")
    for u in UMBRALES:
        ef, _ = eventos(fred_sp, u, 11)
        ey, _ = eventos([x for x in series["S&P 500 (Yahoo ^GSPC)"] if x[0] >= fred_sp[0][0]], u, 11)
        p(f"  umbral {u:.0%}: desplomes FRED {[str(e[1]) for e in ef]} | Yahoo {[str(e[1]) for e in ey]}")
    p("")

    resumen = {}
    for u in UMBRALES:
        for h in HORIZONTES:
            clave = f"umbral {u:.0%}, h={h}"
            p(f"==================== {clave} ====================")
            todos_exc, todos_pos, ep_medias, primeros_exc, primeros_pos = [], [], [], [], []
            n_ev_tot = n_ep_tot = 0
            for k, s in series.items():
                mu, fpos_inc = incondicional(s, h)
                ev, sv = eventos(s, u, h)
                grupos = episodios(ev)
                exc = [e[3] - mu for e in ev]
                pos = [e[3] > 0 for e in ev]
                epm = [st.mean(e[3] - mu for e in g) for g in grupos]
                pri = [g[0][3] - mu for g in grupos]
                prip = [g[0][3] > 0 for g in grupos]
                todos_exc += exc; todos_pos += pos; ep_medias += epm
                primeros_exc += pri; primeros_pos += prip
                n_ev_tot += len(ev); n_ep_tot += len(grupos)
                p(f"-- {k}")
                p(f"   media incondicional {h}d {mu:+.4%}, frec. positiva incondicional {fpos_inc:.1%}")
                p(f"   eventos {len(ev)}  episodios {len(grupos)}"
                  + (f"  (sin ventana completa, excluidos: {sv})" if sv else ""))
                if ev:
                    p(f"   frec. positiva {sum(pos)/len(pos):.1%}  media {h}d {st.mean(e[3] for e in ev):+.3%}  "
                      f"exceso medio {st.mean(exc):+.3%}  t(episodios) {tstat(epm):.2f}")
                    p(f"   solo primer desplome: frec. {sum(prip)/len(prip):.1%}  exceso medio {st.mean(pri):+.3%}  t {tstat(pri):.2f}")
                if h == 11 and u == -0.05:
                    for g in grupos:
                        p("     ep " + "; ".join(f"{e[1]} {e[2]:+.1%} -> {e[3]:+.1%}" for e in g))
            f = sum(todos_pos) / len(todos_pos)
            mexc = st.mean(todos_exc)
            t_ep = tstat(ep_medias)
            t_ev = tstat(todos_exc)
            fp = sum(primeros_pos) / len(primeros_pos)
            mp = st.mean(primeros_exc)
            tp = tstat(primeros_exc)
            p(f"** AGRUPADO {clave}: eventos {n_ev_tot}, episodios {n_ep_tot}")
            p(f"   frec. positiva {f:.1%} | exceso medio (por evento) {mexc:+.3%} | "
              f"media de medias por episodio {st.mean(ep_medias):+.3%} | t episodios {t_ep:.2f} | t ingenua por evento {t_ev:.2f}")
            p(f"   solo primer desplome: frec. {fp:.1%} | exceso medio {mp:+.3%} | t {tp:.2f}")
            h1 = f > 0.55
            h2 = mexc > 0 and t_ep >= 1.0
            ver = "Replicado" if h1 and h2 else ("Replicado con diferencias" if h1 or h2 else "No replicado")
            p(f"   H1 {'se sostiene' if h1 else 'refutada'}; H2 {'se sostiene' if h2 else 'refutada'} -> {ver}")
            p("")
            resumen[clave] = (n_ev_tot, n_ep_tot, f, mexc, t_ep, fp, mp, tp, ver)

    p("== Resumen ==")
    p("variante | eventos | episodios | frec+ | exceso medio | t episodios | 1er: frec+ | 1er: exceso | 1er: t | veredicto §2")
    for k, v in resumen.items():
        p(f"{k} | {v[0]} | {v[1]} | {v[2]:.1%} | {v[3]:+.2%} | {v[4]:.2f} | {v[5]:.1%} | {v[6]:+.2%} | {v[7]:.2f} | {v[8]}")
    p("Veredicto principal (umbral -5%, h=11): " + resumen["umbral -5%, h=11"][8])
    texto = "\n".join(out)
    print(texto)
    with open(os.path.join(AQUI, "salida.txt"), "w") as fh:
        fh.write(texto + "\n")


if __name__ == "__main__":
    main()
