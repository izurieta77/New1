#!/usr/bin/env python3
"""AC-13: doble ejecucion independiente de R09 (efecto cambio de mes).

Solo stdlib. No importa ni copia R09.py ni R09_verificacion.py. Lee los datos
crudos de ./datos (descarga propia del 2026-10-06): French diario 202608 (descarga
nueva) y 202607 (control, copia del repo), Yahoo ^GSPC / ^SP500TR / SPY / ^DJI
(JSON v8 crudo) y FRED SP500 / DJIA (csv).
Uso: python3 AC13.py > salida.txt  (escribe tambien resultados.json)
"""
import csv, json, math, os, random, statistics as st, sys, zipfile
from datetime import date, datetime, timezone

AQUI = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(AQUI, "datos")
CORTE = date(2008, 2, 29)          # dentro: <= CORTE ; fuera: > CORTE
FIN_FR = date(2026, 7, 31)         # ultimo dia de la RF en el pre-registro
FIN_SP = date(2026, 8, 31)         # ultimo mes completo de ^GSPC en el pre-registro
COSTO_LADO = 0.0029 + 0.0005       # 0.34 % por lado (pre-registro, seccion 9)
SEMILLA = 20261006
RES = {}

# ----------------------------------------------------------------- lectores
def leer_french(nombre):
    """-> dict fecha -> (mkt_total, rf) en fraccion; mkt_total = Mkt-RF + RF."""
    z = zipfile.ZipFile(os.path.join(D, nombre))
    txt = z.read(z.namelist()[0]).decode("latin-1")
    out = {}
    for ln in txt.splitlines():
        p = [x.strip() for x in ln.split(",")]
        if len(p) == 5 and len(p[0]) == 8 and p[0].isdigit():
            f = date(int(p[0][:4]), int(p[0][4:6]), int(p[0][6:]))
            mk, rf = float(p[1]), float(p[4])
            if mk <= -99 or rf <= -99:
                continue
            out[f] = ((mk + rf) / 100.0, rf / 100.0)
    return out

def leer_yahoo(nombre, campo):
    j = json.load(open(os.path.join(D, nombre)))["chart"]["result"][0]
    ts = j["timestamp"]
    if campo == "adjclose":
        px = j["indicators"]["adjclose"][0]["adjclose"]
    else:
        px = j["indicators"]["quote"][0]["close"]
    out = []
    for t, p in zip(ts, px):
        if p is None:
            continue
        out.append((datetime.fromtimestamp(t, timezone.utc).date(), float(p)))
    # sin duplicados de fecha
    d = {}
    for f, p in out:
        d[f] = p
    return sorted(d.items())

def leer_fred(nombre):
    out = []
    with open(os.path.join(D, nombre)) as fh:
        r = csv.reader(fh)
        next(r)
        for f, v in r:
            if v in (".", ""):
                continue
            y, m, dd = map(int, f.split("-"))
            out.append((date(y, m, dd), float(v)))
    return out

def rend_de_precios(serie):
    """lista (fecha, precio) -> lista (fecha, rendimiento simple), fecha = dia del rend."""
    return [(serie[i][0], serie[i][1] / serie[i - 1][1] - 1.0) for i in range(1, len(serie))]

# ----------------------------------------------------------------- calendario
def posiciones(fechas):
    """pos_ini (1 = primer dia del mes) y pos_fin (-1 = ultimo) por indice.
    Cada mes se completa solo si la serie lo abarca entero; si no, None."""
    n = len(fechas)
    ini = [None] * n
    fin = [None] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and (fechas[j + 1].year, fechas[j + 1].month) == (fechas[i].year, fechas[i].month):
            j += 1
        k = j - i + 1
        for q in range(i, j + 1):
            ini[q] = q - i + 1
            fin[q] = q - j - 1
        i = j + 1
    return ini, fin

def preparar(fechas, rets, primera_fecha_precio=None):
    """fechas/rets alineadas (dia del rendimiento). Para series de precio, el dia
    base (primera_fecha_precio) forma parte del calendario del mes pero no tiene
    rendimiento. Devuelve dict de listas."""
    cal = ([primera_fecha_precio] if primera_fecha_precio else []) + list(fechas)
    ini, fin = posiciones(cal)
    if primera_fecha_precio:
        ini, fin = ini[1:], fin[1:]
        # el primer mes se abre a mitad si la base no es dia <= 5: pos_ini no es fiable
        base = primera_fecha_precio
        if base.day > 5:
            m0 = (base.year, base.month)
            ini = [None if (f.year, f.month) == m0 else v for f, v in zip(fechas, ini)]
    return {"f": list(fechas), "r": list(rets), "ini": ini, "fin": fin}

def es_tom(i_, f_):
    return f_ == -1 or (i_ is not None and 1 <= i_ <= 3)

def en_otros(i_, f_):
    # -10..-2 o +4..+10 (fuera del TOM)
    if f_ is not None and -10 <= f_ <= -2:
        return True
    if i_ is not None and 4 <= i_ <= 10:
        return True
    return False

# ----------------------------------------------------------------- estadistica
def media(x): return sum(x) / len(x)

def var_m(x):
    m = media(x)
    return sum((v - m) ** 2 for v in x) / (len(x) - 1)

def ols_dummy(y, d, rezagos=10):
    """y = a + b d + e. -> b, t_mco, t_hc1, t_nw (Bartlett, n/(n-k))."""
    n = len(y)
    s1 = sum(d); sy = sum(y); sdy = sum(a * b for a, b in zip(d, y))
    sxx = [[n, s1], [s1, s1]]
    det = n * s1 - s1 * s1
    inv = [[s1 / det, -s1 / det], [-s1 / det, n / det]]
    b0 = inv[0][0] * sy + inv[0][1] * sdy
    b1 = inv[1][0] * sy + inv[1][1] * sdy
    e = [yy - b0 - b1 * dd for yy, dd in zip(y, d)]
    k = 2
    def sand(S):
        # inv * S * inv
        M = [[sum(inv[a][c] * S[c][b] for c in range(2)) for b in range(2)] for a in range(2)]
        V = [[sum(M[a][c] * inv[c][b] for c in range(2)) for b in range(2)] for a in range(2)]
        return V
    # MCO
    s2 = sum(v * v for v in e) / (n - k)
    t_mco = b1 / math.sqrt(s2 * inv[1][1])
    # HC1: S = sum e^2 x x'
    S = [[0.0, 0.0], [0.0, 0.0]]
    for ee, dd in zip(e, d):
        w = ee * ee
        S[0][0] += w; S[0][1] += w * dd; S[1][0] += w * dd; S[1][1] += w * dd * dd
    V = sand(S)
    t_hc1 = b1 / math.sqrt(V[1][1] * n / (n - k))
    # NW: g_t = e_t (1, d_t)
    g0 = [ee for ee in e]
    g1 = [ee * dd for ee, dd in zip(e, d)]
    G = [[0.0, 0.0], [0.0, 0.0]]
    for a_, b_ in ((g0, g0), (g0, g1), (g1, g0), (g1, g1)):
        pass
    def gam(u, v, l):
        return sum(u[t] * v[t - l] for t in range(l, n))
    S = [[gam(g0, g0, 0), gam(g0, g1, 0)], [gam(g1, g0, 0), gam(g1, g1, 0)]]
    for l in range(1, rezagos + 1):
        w = 1 - l / (rezagos + 1)
        a = gam(g0, g0, l); b = gam(g0, g1, l); c = gam(g1, g0, l); dd_ = gam(g1, g1, l)
        S[0][0] += w * 2 * a
        S[0][1] += w * (b + c)
        S[1][0] += w * (b + c)
        S[1][1] += w * 2 * dd_
    V = sand(S)
    t_nw = b1 / math.sqrt(V[1][1] * n / (n - k))
    return b0, b1, t_mco, t_hc1, t_nw

def t_dos_muestras(a, b):
    ma, mb = media(a), media(b)
    na, nb = len(a), len(b)
    va, vb = var_m(a), var_m(b)
    sp = ((na - 1) * va + (nb - 1) * vb) / (na + nb - 2)
    t_p = (ma - mb) / math.sqrt(sp * (1 / na + 1 / nb))
    t_w = (ma - mb) / math.sqrt(va / na + vb / nb)
    return ma - mb, t_p, t_w

def t_iid(x):
    return media(x) / math.sqrt(var_m(x) / len(x))

def boot_ic(x, rep=10000, seed=9):
    rng = random.Random(seed)
    n = len(x)
    ms = sorted(sum(x[rng.randrange(n)] for _ in range(n)) / n for _ in range(rep))
    return ms[int(0.025 * rep)], ms[int(0.975 * rep) - 1]

def binom_cola(k, n):
    """P(X >= k), X~Bin(n,.5)"""
    s = 0
    c = 1
    # sumar en logs para n grande
    tot = 0.0
    for j in range(k, n + 1):
        tot += math.exp(math.lgamma(n + 1) - math.lgamma(j + 1) - math.lgamma(n - j + 1) - n * math.log(2))
    return tot

# ----------------------------------------------------------------- pruebas del efecto
def recorte(S, desde, hasta):
    """indices con desde <= fecha <= hasta"""
    return [q for q, f in enumerate(S["f"]) if (desde is None or f >= desde) and (hasta is None or f <= hasta)]

def efecto(S, desde, hasta, rf=None):
    ix = recorte(S, desde, hasta)
    # regresion diaria: solo dias con posicion conocida (descarta el primer mes parcial)
    ix_ok = [q for q in ix if S["fin"][q] is not None and S["ini"][q] is not None]
    y = [100 * S["r"][q] for q in ix_ok]
    d = [1.0 if es_tom(S["ini"][q], S["fin"][q]) else 0.0 for q in ix_ok]
    b0, b1, tm, th, tn = ols_dummy(y, d)
    # estrecha
    tom = []; otr = []; seq = []; dd2 = []
    for q in ix_ok:
        if es_tom(S["ini"][q], S["fin"][q]):
            tom.append(100 * S["r"][q]); seq.append(100 * S["r"][q]); dd2.append(1.0)
        elif en_otros(S["ini"][q], S["fin"][q]):
            otr.append(100 * S["r"][q]); seq.append(100 * S["r"][q]); dd2.append(0.0)
    dif, tp, tw = t_dos_muestras(tom, otr)
    _, _, _, _, tn2 = ols_dummy(seq, dd2)
    out = dict(n=len(y), nTOM=int(sum(d)), mu=b0, delta=b1, t_mco=tm, t_hc1=th, t_nw=tn,
               tom_mean=media(tom), otros_mean=media(otr), dif_mx=dif, t_mx_mco=tp, t_mx_welch=tw,
               t_mx_nw=tn2, desde=str(S["f"][ix_ok[0]]), hasta=str(S["f"][ix_ok[-1]]))
    # medias por dia -1,+1,+2,+3
    for nombre, cond in (("d-1", lambda i_, f_: f_ == -1), ("d+1", lambda i_, f_: i_ == 1),
                         ("d+2", lambda i_, f_: i_ == 2), ("d+3", lambda i_, f_: i_ == 3)):
        v = [100 * S["r"][q] for q in ix_ok if cond(S["ini"][q], S["fin"][q])]
        out[nombre] = media(v)
    return out

def mensual(S, desde, hasta, rf=None):
    """D_m y E_m. Mes m: TOM = dia -1 de m + dias +1..+3 de m+1; resto = +4..-2 de m."""
    f, r, ini, fin = S["f"], S["r"], S["ini"], S["fin"]
    n = len(f)
    Dm = []; E = []; tom4 = []; mes = []; rest = []
    # indices de dias -1
    for q in range(n - 3):
        if fin[q] != -1:
            continue
        if not (desde is None or f[q] >= desde) or not (hasta is None or f[q] <= hasta):
            continue
        tq = [q, q + 1, q + 2, q + 3]
        if not (ini[q + 1] == 1 and ini[q + 2] == 2 and ini[q + 3] == 3):
            continue
        # resto de m: desde +4 de m hasta -2 de m
        j = q
        while j > 0 and (f[j - 1].year, f[j - 1].month) == (f[q].year, f[q].month):
            j -= 1
        resto = [k for k in range(j, q) if ini[k] is not None and ini[k] >= 4]
        if not resto or ini[j] is None or ini[j] != 1:
            continue
        mtom = media([100 * r[k] for k in tq])
        mres = media([100 * r[k] for k in resto])
        Dm.append((f[q], mtom - mres))
        prod = 1.0
        for k in tq: prod *= 1 + r[k]
        tom4.append(100 * (prod - 1))
        if rf is not None:
            pr = 1.0
            for k in tq: pr *= 1 + rf.get(f[k], 0.0)
            E.append(100 * (prod - pr))
    x = [v for _, v in Dm]
    out = dict(N=len(x), D_media=media(x), D_mediana=st.median(x), D_t=t_iid(x))
    lo, hi = boot_ic(x)
    out["D_ic"] = (lo, hi)
    out["D_pos"] = sum(1 for v in x if v > 0)
    out["D_psigno"] = binom_cola(out["D_pos"], len(x))
    if E:
        out["E_media"] = media(E); out["E_t"] = t_iid(E); out["E_ic"] = boot_ic(E)
        out["E_pos"] = sum(1 for v in E if v > 0) / len(E)
    out["TOM4_medio"] = media(tom4)
    return out

# ----------------------------------------------------------------- estrategia
def metricas(rets_netos, rf_d, fechas):
    ex = [a - b for a, b in zip(rets_netos, rf_d)]
    n = len(ex)
    eq = 1.0; pico = 1.0; mdd = 0.0
    for v in rets_netos:
        eq *= 1 + v
        pico = max(pico, eq)
        mdd = min(mdd, eq / pico - 1)
    anios = (fechas[-1] - fechas[0]).days / 365.25
    cagr = eq ** (1 / anios) - 1 if eq > 0 else -1
    vol = math.sqrt(var_m(rets_netos)) * math.sqrt(252)
    sh = media(ex) / math.sqrt(var_m(ex)) * math.sqrt(252)
    # t NW(10) de la media del exceso
    d = [0.0] * n
    _, b0, _, _, tnw = ols_dummy_const(ex)
    return dict(cagr=cagr, vol=vol, sharpe=sh, mdd=mdd, nw_t=tnw, n=n, exceso_medio_anual=media(ex) * 252)

def ols_dummy_const(y, rezagos=10):
    n = len(y); m = media(y)
    e = [v - m for v in y]
    s = sum(v * v for v in e)
    for l in range(1, rezagos + 1):
        w = 1 - l / (rezagos + 1)
        s += 2 * w * sum(e[t] * e[t - l] for t in range(l, n))
    v = s / n ** 2 * n / (n - 1)
    return None, m, None, None, m / math.sqrt(v)

def estrategia(S, rfd, a, b, desde, hasta, costo=COSTO_LADO, regla="tom", sma=200):
    """Exposicion w_t (conocida al cierre de t-1) -> rend neto del dia t.
    w_t = 1 si fin_t >= a (a<0) o ini_t <= b (ventana [a, b]); 'bh' = 1; 'sma' regla de media movil.
    Costo = costo * |w_t - w_{t-1}| aplicado al rendimiento del dia t (se opera al cierre de t-1).
    Segmento (desde, hasta]: w previo = exposicion del dia anterior (la posicion arranca ya tomada)."""
    f, r, ini, fin = S["f"], S["r"], S["ini"], S["fin"]
    n = len(f)
    w = [0.0] * n
    if regla == "tom":
        for q in range(n):
            ok = (fin[q] is not None and fin[q] >= a) or (ini[q] is not None and ini[q] <= b)
            w[q] = 1.0 if ok else 0.0
    elif regla == "bh":
        w = [1.0] * n
    elif regla == "sma":
        niv = []; x = 1.0
        for v in r:
            x *= 1 + v; niv.append(x)
        for q in range(n):
            if q >= sma:      # nivel de cierre de t-1 vs media de los ultimos sma cierres hasta t-1
                m = sum(niv[q - sma:q]) / sma
                w[q] = 1.0 if niv[q - 1] > m else 0.0
    out = []; fe = []; rr = []
    for q in range(1, n):
        if not (f[q] > desde and (hasta is None or f[q] <= hasta)):
            continue
        rf = rfd.get(f[q], 0.0)
        c = costo * abs(w[q] - w[q - 1]) if f[q - 1] > desde else 0.0
        ret = w[q] * r[q] + (1 - w[q]) * rf
        ret = (1 + ret) * (1 - c) - 1
        out.append(ret); rr.append(rf); fe.append(f[q])
    ops = sum(1 for q in range(1, n) if f[q] > desde and (hasta is None or f[q] <= hasta) and w[q] != w[q - 1])
    m = metricas(out, rr, fe)
    m["ops_anio"] = ops / ((fe[-1] - fe[0]).days / 365.25)
    m["exposicion"] = media([w[q] for q in range(1, n) if f[q] > desde and (hasta is None or f[q] <= hasta)])
    # bruto: exceso bruto de la regla, y costo de equilibrio por lado
    bruto = []
    for q in range(1, n):
        if f[q] > desde and (hasta is None or f[q] <= hasta):
            rf = rfd.get(f[q], 0.0)
            bruto.append(w[q] * r[q] + (1 - w[q]) * rf - rf)
    m["exceso_bruto_anual"] = media(bruto) * 252
    m["costo_eq_lado"] = (m["exceso_bruto_anual"] / m["ops_anio"]) if m["ops_anio"] > 0 else None
    return m

# ----------------------------------------------------------------- salida
def fmt(x, d=4):
    return "NA" if x is None else f"{x:.{d}f}"

def tabla_efecto(titulo, S, ventanas, rf=None):
    print(f"\n### {titulo}")
    print("| ventana | desde | hasta | n | nTOM | delta pp/dia | t MCO | t HC1 | t NW10 | TOM | otros | dif MX | t MX MCO | t MX Welch | t MX NW |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    res = {}
    for nom, (de, ha) in ventanas.items():
        try:
            e = efecto(S, de, ha)
        except Exception as ex:
            print(f"| {nom} | (sin datos: {ex}) |"); continue
        res[nom] = e
        print(f"| {nom} | {e['desde']} | {e['hasta']} | {e['n']} | {e['nTOM']} | {e['delta']:.4f} | {e['t_mco']:.2f} | {e['t_hc1']:.2f} | {e['t_nw']:.2f} | "
              f"{e['tom_mean']:.4f} | {e['otros_mean']:.4f} | {e['dif_mx']:.4f} | {e['t_mx_mco']:.2f} | {e['t_mx_welch']:.2f} | {e['t_mx_nw']:.2f} |")
    return res

def tabla_mensual(titulo, S, ventanas, rf):
    print(f"\n### {titulo} (mensual pareado D_m y E)")
    print("| ventana | meses | D media | D mediana | t | IC95 | D>0 | p signo | TOM 4d % | E medio % | t E | IC95 E | E>0 |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    res = {}
    for nom, (de, ha) in ventanas.items():
        try:
            m = mensual(S, de, ha, rf)
        except Exception as ex:
            print(f"| {nom} | sin datos |"); continue
        res[nom] = m
        ee = f"{m['E_media']:.4f} | {m['E_t']:.2f} | [{m['E_ic'][0]:.4f}, {m['E_ic'][1]:.4f}] | {m['E_pos']:.3f}" if "E_media" in m else "NA | NA | NA | NA"
        print(f"| {nom} | {m['N']} | {m['D_media']:.4f} | {m['D_mediana']:.4f} | {m['D_t']:.2f} | [{m['D_ic'][0]:.4f}, {m['D_ic'][1]:.4f}] | "
              f"{m['D_pos']}/{m['N']} | {m['D_psigno']:.4f} | {m['TOM4_medio']:.4f} | {ee} |")
    return res

VENT = {
    "completo": (None, None),
    "dentro (<=2008-02-29)": (None, CORTE),
    "fuera (>2008-02-29)": (date(2008, 3, 1), None),
    "MX A 1926-1986": (None, date(1986, 12, 31)),
    "MX B 1987-2005": (date(1987, 1, 1), date(2005, 12, 31)),
    "MX C 1926-2005": (None, date(2005, 12, 31)),
    "hueco 2006-01..2008-02": (date(2006, 1, 1), CORTE),
    "fuera mitad 1 (2008-03..2016-12)": (date(2008, 3, 1), date(2016, 12, 31)),
    "fuera mitad 2 (2017-01..)": (date(2017, 1, 1), None),
}

def cortar(S, hasta):
    ix = [q for q, f in enumerate(S["f"]) if f <= hasta]
    return {k: [S[k][q] for q in ix] for k in S}

def main():
    print("# AC-13: doble ejecucion independiente de R09 (efecto cambio de mes)\n")
    print(f"Costo por lado {COSTO_LADO:.4f}; corte {CORTE}; semilla bootstrap iid 9 (como el pre-registro).\n")
    # ---- datos
    fr8 = leer_french("french_daily_202608_descarga.zip")
    fr7 = leer_french("french_daily_202607_repo.zip")
    fechas8 = sorted(fr8); fechas7 = sorted(fr7)
    print(f"French 202608: {len(fechas8)} dias {fechas8[0]}..{fechas8[-1]}; French 202607 (repo): {len(fechas7)} dias {fechas7[0]}..{fechas7[-1]}")
    comunes = [f for f in fechas7 if f in fr8]
    dmax = max(abs(fr7[f][0] - fr8[f][0]) for f in comunes)
    ndif = sum(1 for f in comunes if abs(fr7[f][0] - fr8[f][0]) > 1e-12)
    print(f"Vintages: {len(comunes)} fechas comunes, max |dif| del mercado = {dmax:.6f}, fechas con dif > 1e-12: {ndif}")
    rf8 = {f: v[1] for f, v in fr8.items()}
    rf7 = {f: v[1] for f, v in fr7.items()}
    SFR8 = preparar(fechas8, [fr8[f][0] for f in fechas8])
    SFR7 = preparar(fechas7, [fr7[f][0] for f in fechas7])
    SFR8c = cortar(SFR8, FIN_FR)           # mismo fin que R09 (2026-07-31)

    gs = leer_yahoo("yahoo_GSPC_1d.json", "close")
    print(f"Yahoo ^GSPC: {len(gs)} cierres {gs[0][0]}..{gs[-1][0]}")
    rg = rend_de_precios(gs)
    SGS = cortar(preparar([f for f, _ in rg], [v for _, v in rg], gs[0][0]), FIN_SP)
    tr = leer_yahoo("yahoo_SP500TR_1d.json", "close")
    print(f"Yahoo ^SP500TR: {len(tr)} cierres {tr[0][0]}..{tr[-1][0]}")
    rt = rend_de_precios(tr)
    STR = cortar(preparar([f for f, _ in rt], [v for _, v in rt], tr[0][0]), FIN_SP)
    spy = leer_yahoo("yahoo_SPY_1d.json", "adjclose")
    print(f"Yahoo SPY (adjclose): {len(spy)} cierres {spy[0][0]}..{spy[-1][0]}")
    rs = rend_de_precios(spy)
    SSPY = cortar(preparar([f for f, _ in rs], [v for _, v in rs], spy[0][0]), FIN_SP)
    fs = leer_fred("fred_SP500.csv")
    print(f"FRED SP500: {len(fs)} cierres {fs[0][0]}..{fs[-1][0]}")
    rfr = rend_de_precios(fs)
    SFS = cortar(preparar([f for f, _ in rfr], [v for _, v in rfr], fs[0][0]), FIN_SP)
    fd = leer_fred("fred_DJIA.csv")
    print(f"FRED DJIA: {len(fd)} cierres {fd[0][0]}..{fd[-1][0]}")
    rd = rend_de_precios(fd)
    SDJ = cortar(preparar([f for f, _ in rd], [v for _, v in rd], fd[0][0]), FIN_SP)

    # coherencia: mismas fechas / mismos rendimientos entre ^GSPC y FRED SP500
    dg = {f: v for f, v in rg}; dfr = {f: v for f, v in rfr}
    com = [f for f in dfr if f in dg]
    # los rendimientos pueden diferir si faltan fechas en una; comparar solo si el dia previo es igual
    print(f"^GSPC vs FRED SP500: {len(com)} fechas comunes; max |dif rend diario| = "
          f"{max(abs(dg[f]-dfr[f]) for f in com):.6f}; dias con dif>1e-4: {sum(1 for f in com if abs(dg[f]-dfr[f])>1e-4)}")
    # french vs ^GSPC: calendario en 1928-1952
    set_f = set(fechas8)
    ex_fr = [f for f in fechas8 if gs[0][0] <= f <= gs[-1][0] and f not in {g for g, _ in gs}]
    print(f"Fechas de French dentro del rango de ^GSPC que no estan en Yahoo: {len(ex_fr)} (sabados: {sum(1 for f in ex_fr if f.weekday()==5)}); "
          f"fechas de Yahoo ausentes en French: {sum(1 for g,_ in gs if g not in set_f and g <= FIN_FR)}")
    # TOM por mes: 4 dias
    from collections import Counter
    cnt = Counter()
    for q in range(len(SFR8c['f'])):
        pass
    mes_tom = Counter()
    for f, i_, fi in zip(SFR8c["f"], SFR8c["ini"], SFR8c["fin"]):
        if es_tom(i_, fi):
            mes_tom[(f.year, f.month)] += 1
    print("Dias TOM por mes calendario (French 202608, calculados con posiciones propias): ", dict(Counter(mes_tom.values())),
          "(el dia -1 de un mes y +1..+3 del siguiente cuentan en meses distintos)")

    print("\n## Pruebas del efecto")
    r = {}
    r["FR8"] = tabla_efecto("French 202608 (descarga nueva), Mkt total, USD", SFR8c, VENT)
    r["FR7"] = tabla_efecto("French 202607 (control, copia del repo)", SFR7, VENT)
    r["GSPC"] = tabla_efecto("Yahoo ^GSPC, precio (descarga nueva, parser propio)", SGS, VENT)
    r["SP500TR"] = tabla_efecto("Yahoo ^SP500TR, rendimiento total (1988+), SEGUNDA fuente de total return", STR, VENT)
    r["SPY"] = tabla_efecto("Yahoo SPY adjclose (1993+), ETF invertible con dividendos", SSPY, VENT)
    r["FRED_SP500"] = tabla_efecto("FRED SP500 (2016-10+), precio, proveedor distinto", SFS, {"completo": (None, None), "mitad 2 (2017-01..)": (date(2017, 1, 1), None)})
    r["FRED_DJIA"] = tabla_efecto("FRED DJIA (2016-10+), precio, como L&S", SDJ, {"completo": (None, None)})
    # ^SP500TR, SPY solo ventana fuera; IS parcial reportado arriba

    print("\n## Mensual pareado y exceso por evento E")
    m = {}
    m["FR8"] = tabla_mensual("French 202608", SFR8c, VENT, rf8)
    m["FR7"] = tabla_mensual("French 202607 (control)", SFR7, VENT, rf7)
    m["GSPC"] = tabla_mensual("Yahoo ^GSPC", SGS, VENT, rf8)
    m["SP500TR"] = tabla_mensual("Yahoo ^SP500TR", STR, VENT, rf8)
    m["SPY"] = tabla_mensual("Yahoo SPY", SSPY, VENT, rf8)
    m["FRED_SP500"] = tabla_mensual("FRED SP500", SFS, {"completo": (None, None), "mitad 2": (date(2017, 1, 1), None)}, rf8)

    # ---- comparacion con McConnell-Xu tabla 1 (panel C)
    print("\n## Comparacion con McConnell-Xu (tabla 1, paneles A/B/C, TOM y diferencia)")
    for p in ("MX A 1926-1986", "MX B 1987-2005", "MX C 1926-2005"):
        e = r["FR8"][p]
        print(f"- {p}: TOM {e['tom_mean']:.3f}, otros {e['otros_mean']:.3f}, dif {e['dif_mx']:.4f} (t MCO {e['t_mx_mco']:.2f}); articulo: A 0.16/0.01/0.15 (7.07), B 0.15/-0.00/0.15 (3.78), C 0.16/0.01/0.15 (8.06)")
    # exceso sobre RF, panel C
    ix = recorte(SFR8c, None, date(2005, 12, 31))
    tx = [100 * (SFR8c["r"][q] - rf8[SFR8c["f"][q]]) for q in ix if es_tom(SFR8c["ini"][q], SFR8c["fin"][q])]
    ox = [100 * (SFR8c["r"][q] - rf8[SFR8c["f"][q]]) for q in ix if (not es_tom(SFR8c["ini"][q], SFR8c["fin"][q])) and en_otros(SFR8c["ini"][q], SFR8c["fin"][q])]
    print(f"- Exceso sobre RF, panel C: TOM {media(tx):.4f} (t iid {t_iid(tx):.2f}); otros {media(ox):.4f} (t iid {t_iid(ox):.2f}); articulo tabla 2: 0.15 (8.98) y 0.00 (0.15)")

    # ---- L&S
    print("\n## Estilo L&S (rend acumulado medio, %)")
    def ls(S, desde, hasta):
        f, rr, ini, fin = S["f"], S["r"], S["ini"], S["fin"]
        tomv = []; mesv = []; resv = []
        for q in range(len(f) - 3):
            if fin[q] != -1 or not (f[q] >= desde and f[q] <= hasta):
                continue
            if not (ini[q + 1] == 1 and ini[q + 2] == 2 and ini[q + 3] == 3):
                continue
            j = q
            while j > 0 and (f[j - 1].year, f[j - 1].month) == (f[q].year, f[q].month):
                j -= 1
            if ini[j] != 1:
                continue
            p = 1.0
            for k in range(q, q + 4): p *= 1 + rr[k]
            pm = 1.0
            for k in range(j, q + 1): pm *= 1 + rr[k]
            pr = 1.0
            for k in range(j, q):
                if ini[k] is not None and ini[k] >= 4: pr *= 1 + rr[k]
            tomv.append(100 * (p - 1)); mesv.append(100 * (pm - 1)); resv.append(100 * (pr - 1))
        return len(tomv), media(tomv), media(mesv), media(resv)
    for nom, S, d0 in (("French 202608", SFR8c, date(1926, 1, 1)), ("Yahoo ^GSPC", SGS, date(1928, 1, 1))):
        n_, a, b, c = ls(S, d0, date(1986, 12, 31))
        print(f"- {nom} hasta 1986-12: {n_} meses; TOM 4d {a:.4f}; mes completo {b:.4f}; resto {c:.4f}; TOM/mes {a/b:.2f} (L&S DJIA 1897-1986: 0.473 vs 0.349)")

    # ---- estrategias (OOS)
    print("\n## Estrategias, tramo fuera de muestra (2008-02-29 a fin), costos GBM 0.34% por lado")
    est = {}
    def bloque(nombre, S, rfd, hasta, desde=CORTE):
        print(f"\n### {nombre}  ({desde} a {hasta or S['f'][-1]})")
        print("| variante | CAGR | vol | Sharpe | t NW10 | MDD | exposicion | ops/anio | exceso bruto anual | costo equil. lado |")
        print("|---|---|---|---|---|---|---|---|---|---|")
        o = {}
        for nom, (a, b, rg_, c) in {
            "tom_m1_p3 (articulo) neto": (-1, 3, "tom", COSTO_LADO),
            "tom_m1_p3 bruto": (-1, 3, "tom", 0.0),
            "tom_m1_p3 spread medio 0.44%": (-1, 3, "tom", 0.0029 + 0.0015),
            "tom_m2_p3": (-2, 3, "tom", COSTO_LADO),
            "tom_m3_p3": (-3, 3, "tom", COSTO_LADO),
            "tom_m1_p2": (-1, 2, "tom", COSTO_LADO),
            "tom_m1_p4": (-1, 4, "tom", COSTO_LADO),
            "comprar y mantener": (0, 0, "bh", COSTO_LADO),
            "SMA200": (0, 0, "sma", COSTO_LADO),
        }.items():
            m_ = estrategia(S, rfd, a, b, desde, hasta, costo=c, regla=rg_)
            o[nom] = m_
            print(f"| {nom} | {m_['cagr']*100:.2f}% | {m_['vol']*100:.2f}% | {m_['sharpe']:.3f} | {m_['nw_t']:.2f} | {m_['mdd']*100:.1f}% | {m_['exposicion']:.3f} | {m_['ops_anio']:.2f} | {m_['exceso_bruto_anual']*100:.2f}% | {fmt(m_['costo_eq_lado'],5)} |")
        return o
    est["FR8_oos"] = bloque("French 202608", SFR8c, rf8, None)
    est["FR7_oos"] = bloque("French 202607 (control)", SFR7, rf7, None)
    est["GSPC_oos"] = bloque("Yahoo ^GSPC (precio, RF French; agosto con RF = 0)", SGS, rf8, None)
    est["GSPC_oos_0731"] = bloque("Yahoo ^GSPC recortado a 2026-07-31 (mismo fin que R09)", cortar(SGS, FIN_FR), rf8, None)
    est["SP500TR_oos"] = bloque("Yahoo ^SP500TR (rend. total)", STR, rf8, None)
    est["SPY_oos"] = bloque("Yahoo SPY adjclose", SSPY, rf8, None)
    est["FR8_is"] = bloque("French 202608, dentro de muestra", SFR8c, rf8, CORTE, desde=date(1927, 3, 3))
    est["FR8_full"] = bloque("French 202608, completo (1927-03-03...)", SFR8c, rf8, None, desde=date(1927, 3, 3))
    json.dump({"efecto": r, "mensual": {k: {n: {kk: (list(vv) if isinstance(vv, tuple) else vv) for kk, vv in d.items()} for n, d in v.items()} for k, v in m.items()},
               "estrategias": est}, open(os.path.join(AQUI, "resultados.json"), "w"), indent=1, default=str)

if __name__ == "__main__":
    main()
