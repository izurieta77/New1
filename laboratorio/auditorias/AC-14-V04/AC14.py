#!/usr/bin/env python3
"""AC-14: doble ejecucion independiente de V04 (benchmarks en pesos y SMA10 con senal en MXN).

Escrito desde cero (solo biblioteca estandar). No importa reproducir.py, independiente.py ni herramientas/.
Lectores de datos, cierres de mes, indice de CETES, senal, ejecucion T0/T1, costos, metricas y Newey-West
son propios. Sin red: lee datos/ (descarga 2026-10-07) y, para la corrida de control con los datos de A,
los archivos congelados de V04.

Uso (desde la raiz del repo):
    python3 -I laboratorio/auditorias/AC-14-V04/AC14.py > laboratorio/auditorias/AC-14-V04/salida.txt
Escribe ademas resultados.json junto a este archivo.
"""
import csv
import hashlib
import io
import json
import math
import os
import zipfile
from datetime import date, datetime, timezone

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, "..", "..", ".."))
DB = os.path.join(AQUI, "datos")
DA = os.path.join(RAIZ, "laboratorio", "replicas", "V04-benchmarks-en-pesos-y-sma10-senal-mxn", "datos")

COSTO_LADO = 0.0029 + 0.0005  # comision 0.25% + IVA (0.29%) + spread supuesto 0.05%, por lado (prerregistro 7)
NW_LAGS = 6
SALIDA = []
RES = {}


def p(*a):
    SALIDA.append(" ".join(str(x) for x in a))


# ----------------------------------------------------------------------------- lectores

def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def lee_yahoo(path, campo="adjclose"):
    with open(path, "rb") as f:
        r = json.load(f)["chart"]["result"][0]
    ts = r["timestamp"]
    if campo == "adjclose":
        vals = r["indicators"]["adjclose"][0]["adjclose"]
    else:
        vals = r["indicators"]["quote"][0][campo]
    out = {}
    for t, v in zip(ts, vals):
        if v is None:
            continue
        d = datetime.fromtimestamp(t, tz=timezone.utc).date()  # apertura 9:30 NY / 8:30 CDMX => misma fecha UTC
        out[d] = float(v)
    divs = {}
    for ev in (r.get("events") or {}).get("dividends", {}).values():
        d = datetime.fromtimestamp(ev["date"], tz=timezone.utc).date()
        divs[d] = float(ev["amount"])
    return out, divs


def lee_fred(path):
    out = {}
    with open(path, newline="") as f:
        rd = csv.reader(f)
        next(rd)
        for fila in rd:
            if len(fila) < 2 or fila[1].strip() in ("", "."):
                continue
            out[date.fromisoformat(fila[0])] = float(fila[1])
    return out


def lee_banxico(path, serie):
    """Bloque cuyo encabezado es "Fecha","<serie>"...; fechas dd/mm/aaaa; ignora N/E."""
    with open(path, "rb") as f:
        texto = f.read().decode("latin-1")
    out, col, dentro = {}, None, False
    for fila in csv.reader(io.StringIO(texto)):
        if not fila:
            dentro = False
            continue
        if fila[0] == "Fecha":
            dentro = serie in fila
            col = fila.index(serie) if dentro else None
            continue
        if dentro and len(fila) > col:
            v = fila[col].strip()
            if v in ("", "N/E"):
                continue
            dd, mm, aa = fila[0].split("/")
            out[date(int(aa), int(mm), int(dd))] = float(v)
    return out


def lee_french_diario(path):
    """Indice de rendimiento total del mercado CRSP VW (Mkt-RF + RF), USD, base 1 antes del primer dia."""
    with zipfile.ZipFile(path) as z:
        texto = z.read(z.namelist()[0]).decode("latin-1")
    nivel, out = 1.0, {}
    for linea in texto.splitlines():
        partes = [x.strip() for x in linea.split(",")]
        if len(partes) == 5 and len(partes[0]) == 8 and partes[0].isdigit():
            d = date(int(partes[0][:4]), int(partes[0][4:6]), int(partes[0][6:]))
            nivel *= 1.0 + (float(partes[1]) + float(partes[4])) / 100.0
            out[d] = nivel
    return out


# ----------------------------------------------------------------------------- indices de efectivo

class CetesSubasta:
    """Prerregistro 4: interes simple entre colocaciones semanales; capitaliza en cada colocacion."""

    def __init__(self, tasas):
        self.f = sorted(tasas)
        self.y = [tasas[d] for d in self.f]
        self.I = [1.0]
        for k in range(1, len(self.f)):
            dias = (self.f[k] - self.f[k - 1]).days
            self.I.append(self.I[-1] * (1 + self.y[k - 1] / 100 * dias / 360))

    def __call__(self, d):
        lo, hi = 0, len(self.f) - 1
        if d < self.f[0]:
            raise ValueError(d)
        while lo < hi:  # ultimo k con f[k] <= d
            mid = (lo + hi + 1) // 2
            if self.f[mid] <= d:
                lo = mid
            else:
                hi = mid - 1
        return self.I[lo] * (1 + self.y[lo] / 100 * (d - self.f[lo]).days / 360)


class CetesMensual:
    """Tasa mensual (fechada el dia 1): interes simple dentro del mes, capitaliza el dia 1 de cada mes.
    Si falta un mes al final se arrastra la ultima tasa (se reporta)."""

    def __init__(self, tasas):
        self.t = {(d.year, d.month): v for d, v in tasas.items()}
        self.ult = max(self.t)
        self.cache = {}
        self.arrastre = set()

    def tasa(self, y, m):
        if (y, m) in self.t:
            return self.t[(y, m)]
        if (y, m) > self.ult:
            self.arrastre.add((y, m))
            return self.t[self.ult]
        raise KeyError((y, m))

    def inicio_mes(self, y, m):
        k = (y, m)
        if k in self.cache:
            return self.cache[k]
        y0, m0 = min(self.t)
        I, yy, mm = 1.0, y0, m0
        while (yy, mm) < k:
            ny, nm = (yy + 1, 1) if mm == 12 else (yy, mm + 1)
            I *= 1 + self.tasa(yy, mm) / 100 * (date(ny, nm, 1) - date(yy, mm, 1)).days / 360
            yy, mm = ny, nm
            self.cache[(yy, mm)] = I
        self.cache[k] = I
        return I

    def __call__(self, d):
        return self.inicio_mes(d.year, d.month) * (1 + self.tasa(d.year, d.month) / 100 * (d.day - 1) / 360)


# ----------------------------------------------------------------------------- utilidades

def anios(d0, d1):
    return (d1 - d0).days / 365.25


def cagr(v0, v1, d0, d1):
    return (v1 / v0) ** (1 / anios(d0, d1)) - 1


def ultimo_le(serie_fechas, d):
    lo, hi, r = 0, len(serie_fechas) - 1, None
    while lo <= hi:
        mid = (lo + hi) // 2
        if serie_fechas[mid] <= d:
            r = serie_fechas[mid]
            lo = mid + 1
        else:
            hi = mid - 1
    return r


def media(x):
    return sum(x) / len(x)


def desv(x):
    m = media(x)
    return math.sqrt(sum((v - m) ** 2 for v in x) / (len(x) - 1))


def nw_t(x, L=NW_LAGS):
    T = len(x)
    m = media(x)
    e = [v - m for v in x]
    S = sum(v * v for v in e) / T
    for l in range(1, L + 1):
        g = sum(e[t] * e[t - l] for t in range(l, T)) / T
        S += 2 * (1 - l / (L + 1)) * g
    ee = math.sqrt(S / T)
    return m, m / ee, (m - 1.96 * ee, m + 1.96 * ee)


def veredicto(ic):
    return "apoyo" if ic[0] > 0 else ("contraria" if ic[1] < 0 else "inconcluso")


def mdd(vals):
    pico, peor = vals[0], 0.0
    for v in vals:
        pico = max(pico, v)
        peor = min(peor, v / pico - 1)
    return peor


# ----------------------------------------------------------------------------- universo de una configuracion

class Universo:
    def __init__(self, nombre, activo_usd, fx, cetes):
        self.nombre = nombre
        self.usd = activo_usd
        self.fx = fx
        self.cetes = cetes
        self.fechas = sorted(set(activo_usd) & set(fx))  # alerta #3: precio y FX en la misma fecha
        self.mxn = {d: activo_usd[d] * fx[d] for d in self.fechas}
        porm = {}
        for d in self.fechas:
            porm.setdefault((d.year, d.month), []).append(d)
        self.meses = sorted(porm)
        self.E = {k: max(v) for k, v in porm.items()}
        self.F = {k: min(v) for k, v in porm.items()}

    def nivel(self, d, moneda):
        return self.mxn[d] if moneda == "MXN" else self.usd[d]

    def sim(self, n, senal, ejec, ini=(1995, 1), fin=(2026, 8), costo=COSTO_LADO, bh=False):
        """Lista de meses con (mes, d0, d1, w, r_activo, r_cetes, r_neto). Arranca desde efectivo antes de ini."""
        filas, w_prev = [], 0.0
        i0 = self.meses.index(ini)
        i1 = self.meses.index(fin)
        for i in range(i0, i1 + 1):
            m = self.meses[i]
            if bh:
                w = 1.0
            else:
                hist = [self.nivel(self.E[self.meses[j]], senal) for j in range(i - n, i)]
                assert i - n >= 0
                w = 1.0 if hist[-1] > sum(hist) / n else 0.0
            if ejec == "T0":
                d0, d1 = self.E[self.meses[i - 1]], self.E[m]
            else:
                d0 = self.F[m]
                d1 = self.F[self.meses[i + 1]] if i + 1 < len(self.meses) else self.fechas[-1]
            ra = self.mxn[d1] / self.mxn[d0] - 1
            rc = self.cetes(d1) / self.cetes(d0) - 1
            bruto = w * ra + (1 - w) * rc
            neto = (1 - costo * abs(w - w_prev)) * (1 + bruto) - 1
            filas.append((m, d0, d1, w, ra, rc, neto))
            w_prev = w
        return filas


def metricas(filas, a=None, b=None):
    sel = [f for f in filas if (a is None or f[0] >= a) and (b is None or f[0] <= b)]
    v = [1.0]
    for f in sel:
        v.append(v[-1] * (1 + f[6]))
    exc = [f[6] - f[5] for f in sel]
    cambios = sum(1 for k in range(1, len(sel)) if sel[k][3] != sel[k - 1][3])
    return {
        "desde": sel[0][1].isoformat(), "hasta": sel[-1][2].isoformat(), "meses": len(sel),
        "cagr": cagr(1.0, v[-1], sel[0][1], sel[-1][2]),
        "vol": desv([f[6] for f in sel]) * math.sqrt(12),
        "mdd": mdd(v),
        "sharpe": media(exc) / desv(exc) * math.sqrt(12),
        "invertido": media([f[3] for f in sel]),
        "cambios": cambios,
    }


def dif_nw(fa, fb, a, b):
    x = [ra[6] - rb[6] for ra, rb in zip(fa, fb) if a <= ra[0] <= b]
    m, t, ic = nw_t(x)
    return {"anual_pp": m * 12 * 100, "t": t, "veredicto": veredicto(ic), "n": len(x)}


SEG = {"2008-2026": ((2008, 1), (2026, 8)), "1995-2007": ((1995, 1), (2007, 12)), "1995-2026": ((1995, 1), (2026, 8))}


def bench(u, d0, d1):
    a = ultimo_le(u.fechas, d0)
    b = ultimo_le(u.fechas, d1)
    return {"desde": a.isoformat(), "hasta": b.isoformat(),
            "sp_mxn": cagr(u.mxn[a], u.mxn[b], a, b), "sp_usd": cagr(u.usd[a], u.usd[b], a, b),
            "cetes": cagr(u.cetes(a), u.cetes(b), a, b)}


def correr(u):
    p("")
    p("=" * 100)
    p("CONFIGURACION:", u.nombre)
    p(f"  fechas comunes activo y FX: {len(u.fechas)} ({u.fechas[0]} a {u.fechas[-1]})")
    r = {"fechas": [u.fechas[0].isoformat(), u.fechas[-1].isoformat(), len(u.fechas)]}
    # benchmarks
    vent = {"W1": (date(2007, 12, 31), date(2026, 8, 31)), "W2": (date(2008, 1, 31), date(2026, 8, 31)),
            "W3": (date(2008, 1, 2), date(2026, 9, 18)), "W4": (date(2007, 12, 31), date(2025, 12, 31))}
    r["bench"] = {}
    p("  Benchmarks (CAGR, sin costos):  ventana | desde..hasta | S&P TR MXN | S&P TR USD | CETES")
    for k, (d0, d1) in vent.items():
        if u.fechas[-1] < d1:
            p(f"    {k}: sin datos hasta {d1} (ultimo dato comun {u.fechas[-1]})")
            continue
        b = bench(u, d0, d1)
        r["bench"][k] = b
        p(f"    {k}: {b['desde']}..{b['hasta']} | {b['sp_mxn']*100:6.2f}% | {b['sp_usd']*100:6.2f}% | {b['cetes']*100:5.2f}%")
    # sensibilidad de inicio 2007-01..2009-12
    cs = []
    for y in (2007, 2008, 2009):
        for m in range(1, 13):
            d0 = u.E[(y, m)]
            d1 = ultimo_le(u.fechas, date(2026, 8, 31))
            cs.append(cagr(u.mxn[d0], u.mxn[d1], d0, d1))
    r["inicio_min_max"] = [min(cs), max(cs)]
    p(f"  Sensibilidad de inicio (cierres 2007-01..2009-12 a 2026-08): S&P MXN de {min(cs)*100:.2f}% a {max(cs)*100:.2f}%")
    # 2008 calendario
    a, b = ultimo_le(u.fechas, date(2007, 12, 31)), ultimo_le(u.fechas, date(2008, 12, 31))
    r["anio2008"] = {"usd": u.usd[b] / u.usd[a] - 1, "mxn": u.mxn[b] / u.mxn[a] - 1}
    p(f"  Ano 2008 entre fechas fijas: USD {r['anio2008']['usd']*100:.1f}%  MXN {r['anio2008']['mxn']*100:.1f}%")
    # S&P MXN - CETES (T0 comprar y mantener, W1)
    bh0 = u.sim(10, "MXN", "T0", bh=True, costo=0.0)
    x = [f[4] - f[5] for f in bh0 if (2008, 1) <= f[0] <= (2026, 8)]
    m_, t_, ic = nw_t(x)
    r["sp_menos_cetes_2008"] = {"anual_pp": m_ * 1200, "t": t_, "veredicto": veredicto(ic)}
    p(f"  S&P MXN - CETES 2008-2026: media x12 {m_*1200:+.2f} pp, t NW6 {t_:.2f} ({veredicto(ic)})")
    # SMA10 principal y comprar y mantener
    corr = {}
    for ej in ("T0", "T1"):
        corr[("BH", ej)] = u.sim(10, "MXN", ej, bh=True)
        for s in ("MXN", "USD"):
            for n in (6, 8, 10, 12):
                corr[(n, s, ej)] = u.sim(n, s, ej)
    r["sma"] = {}
    p("  SMA y comprar y mantener (costos GBM 0.34% por lado)")
    p("    corrida             segmento   | CAGR    | vol    | MDD     | Sharpe | invert. | cambios")
    for clave in [(10, "MXN", "T1"), ("BH", "T1"), (10, "MXN", "T0"), ("BH", "T0"), (10, "USD", "T1"), (10, "USD", "T0")]:
        nom = "BH-" + clave[1] if clave[0] == "BH" else f"SMA{clave[0]}-{clave[1]}-{clave[2]}"
        for sn, (a_, b_) in SEG.items():
            mt = metricas(corr[clave], a_, b_)
            r["sma"][f"{nom}|{sn}"] = mt
            p(f"    {nom:18s}  {sn} | {mt['cagr']*100:6.2f}% | {mt['vol']*100:5.2f}% | {mt['mdd']*100:6.1f}% | "
              f"{mt['sharpe']:6.3f} | {mt['invertido']*100:5.1f}% | {mt['cambios']}")
    p("  Diferencia mensual neta SMA10 - comprar y mantener (misma ejecucion), NW(6)")
    r["dif"] = {}
    for s in ("MXN", "USD"):
        for ej in ("T1", "T0"):
            for sn, (a_, b_) in SEG.items():
                d = dif_nw(corr[(10, s, ej)], corr[("BH", ej)], a_, b_)
                r["dif"][f"SMA10-{s}-{ej}|{sn}"] = d
                p(f"    SMA10-{s}-{ej} {sn}: {d['anual_pp']:+.3f} pp/ano, t {d['t']:.3f} ({d['veredicto']}, n={d['n']})")
    # Parejas senal MXN contra USD (mismo n y ejecucion)
    r["parejas"] = {}
    for sn in ("2008-2026", "1995-2007"):
        a_, b_ = SEG[sn]
        mxn_mas_cagr = usd_menos_caida = 0
        for n in (6, 8, 10, 12):
            for ej in ("T0", "T1"):
                mm, mu = metricas(corr[(n, "MXN", ej)], a_, b_), metricas(corr[(n, "USD", ej)], a_, b_)
                mxn_mas_cagr += mm["cagr"] > mu["cagr"]
                usd_menos_caida += mu["mdd"] > mm["mdd"]
        r["parejas"][sn] = {"mxn_mas_cagr": mxn_mas_cagr, "usd_menos_caida": usd_menos_caida}
        p(f"  Parejas (8) {sn}: senal MXN con mas CAGR que USD en {mxn_mas_cagr}; senal USD con menor caida en {usd_menos_caida}")
    p("  16 variantes: rango de MDD (y si todas quedan arriba de comprar y mantener)")
    r["variantes"] = {}
    for sn in ("2008-2026", "1995-2007"):
        a_, b_ = SEG[sn]
        md = [metricas(corr[(n, s, ej)], a_, b_)["mdd"] for n in (6, 8, 10, 12) for s in ("MXN", "USD") for ej in ("T0", "T1")]
        bh = [metricas(corr[("BH", ej)], a_, b_)["mdd"] for ej in ("T0", "T1")]
        todas = all(x > max(bh) for x in md)
        r["variantes"][sn] = {"mdd_min": min(md), "mdd_max": max(md), "bh": bh, "todas_menor_caida": todas}
        p(f"    {sn}: MDD variantes {min(md)*100:.1f}% a {max(md)*100:.1f}%; comprar y mantener T0 {bh[0]*100:.1f}% / T1 {bh[1]*100:.1f}%;"
          f" todas con menor caida: {'si' if todas else 'NO'}")
    return r


def ipc(nombre, path, fin=date(2026, 8, 31)):
    adj, divs = lee_yahoo(path)
    f = sorted(d for d in adj if d <= fin)
    d0, d1 = f[0], f[-1]
    c = cagr(adj[d0], adj[d1], d0, d1)
    jun = ultimo_le(f, date(2026, 6, 30))
    cj = cagr(adj[d0], adj[jun], d0, jun)
    anios_div = sorted({d.year for d in divs})
    falt = [y for y in range(2008, 2026) if y not in anios_div]
    p(f"  {nombre}: {d0}..{d1} CAGR {c*100:.2f}% (a {jun}: {cj*100:.2f}%); anos sin dividendo 2008-2025: {falt}")
    return {"desde": d0.isoformat(), "hasta": d1.isoformat(), "cagr": c, "cagr_jun2026": cj, "anios_sin_div": falt}


def main():
    p("AC-14: doble ejecucion independiente de V04. Fase 0, formacion; no es recomendacion.")
    p("Huellas sha256 de los datos leidos:")
    archivos_b = sorted(os.listdir(DB))
    for fn in archivos_b:
        if fn.endswith((".csv", ".zip", ".json")):
            p(f"  B {fn} {sha(os.path.join(DB, fn))[:16]}")
    archivos_a = ["yahoo_SPY_1d.json", "fred_DEXMXUS.csv", "banxico_CF107_cetes28_SF43936.csv",
                  "banxico_CF102_fix_SF43718.csv", "yahoo_NAFTRAC.MX_1d.json", "yahoo_SP500TR_1d.json",
                  "yahoo_GSPC_1d.json", "fred_INTGSTMXM193N.csv"]
    for fn in archivos_a:
        p(f"  A {fn} {sha(os.path.join(DA, fn))[:16]}")

    # --- datos A (congelados de V04)
    spy_a, _ = lee_yahoo(os.path.join(DA, "yahoo_SPY_1d.json"))
    dex_a = lee_fred(os.path.join(DA, "fred_DEXMXUS.csv"))
    cet_a = CetesSubasta(lee_banxico(os.path.join(DA, "banxico_CF107_cetes28_SF43936.csv"), "SF43936"))
    # --- datos B (descarga 2026-10-07)
    french = lee_french_diario(os.path.join(DB, "french_daily_descarga.zip"))
    fix_b = lee_banxico(os.path.join(DB, "banxico_FIX_SF43718.csv"), "SF43718")
    dex_b = lee_fred(os.path.join(DB, "alfred_DEXMXUS.csv"))
    cet_sub_b = CetesSubasta(lee_banxico(os.path.join(DB, "banxico_CETES_SF43936_SF282.csv"), "SF43936"))
    cet_men_b = CetesMensual(lee_banxico(os.path.join(DB, "banxico_CETES_SF43936_SF282.csv"), "SF282"))
    cet_fmi = CetesMensual(lee_fred(os.path.join(DB, "alfred_INTGSTMXM193N.csv")))

    # Comparacion de tipos de cambio en fechas comunes
    comunes = sorted(set(fix_b) & set(dex_a))
    difs = sorted(abs(fix_b[d] / dex_a[d] - 1) for d in comunes if d >= date(1993, 11, 8))
    p("")
    p(f"FIX Banxico (B) contra DEXMXUS (A): {len(difs)} fechas comunes; mediana |dif| {difs[len(difs)//2]*100:.3f}%, "
      f"p90 {difs[int(len(difs)*0.9)]*100:.3f}%, max {difs[-1]*100:.2f}%")
    vint = [d for d in set(dex_a) & set(dex_b) if d <= date(2026, 9, 18) and dex_a[d] != dex_b[d]]
    p(f"DEXMXUS vintage 2026-10-07 (ALFRED) contra la de A: {len(vint)} fechas con valor distinto; "
      f"fechas solo en A: {len(set(d for d in dex_a if d<=date(2026,9,18)) - set(dex_b))}, solo en B (<=2026-09-18): "
      f"{len(set(d for d in dex_b if d<=date(2026,9,18)) - set(dex_a))}")
    # SPY (A) contra French en USD, CAGR W1
    a0, a1 = date(2007, 12, 31), date(2026, 8, 31)
    p(f"USD W1: SPY adjclose (A) {cagr(spy_a[a0], spy_a[a1], a0, a1)*100:.2f}%  |  French CRSP VW (B) "
      f"{cagr(french[a0], french[a1], a0, a1)*100:.2f}%")
    # FRED SP500 (precio) contra Yahoo ^GSPC (A), cierres comunes
    gspc_a, _ = lee_yahoo(os.path.join(DA, "yahoo_GSPC_1d.json"), "close")
    sp_fred = lee_fred(os.path.join(DB, "fred_SP500_de_AC13.csv"))
    cc = sorted(set(gspc_a) & set(sp_fred))
    dd = [abs(sp_fred[d] / gspc_a[d] - 1) for d in cc]
    p(f"FRED SP500 (precio, via AC-13) contra Yahoo ^GSPC (A): {len(cc)} fechas comunes {cc[0]}..{cc[-1]}, "
      f"{sum(1 for x in dd if x > 1e-4)} con |dif| > 0.01%, max {max(dd)*100:.3f}%")
    b0, b1 = date(2016, 10, 31), date(2026, 8, 31)
    fb = sorted(set(sp_fred) & set(fix_b))
    x0, x1 = ultimo_le(fb, b0), ultimo_le(fb, b1)
    ga = sorted(set(gspc_a) & set(dex_a))
    y0, y1 = ultimo_le(ga, b0), ultimo_le(ga, b1)
    c_fred = cagr(sp_fred[x0] * fix_b[x0], sp_fred[x1] * fix_b[x1], x0, x1)
    c_yah = cagr(gspc_a[y0] * dex_a[y0], gspc_a[y1] * dex_a[y1], y0, y1)
    p(f"S&P precio en MXN {b0}..{b1}: FRED SP500 x FIX {c_fred*100:.2f}%  |  Yahoo ^GSPC x DEXMXUS {c_yah*100:.2f}%")
    RES["controles"] = {"fix_vs_dex_mediana": difs[len(difs) // 2], "dex_vintage_difs": len(vint),
                        "sp500_fred_vs_gspc_max": max(dd), "sp_precio_mxn_2016_fred_fix": c_fred,
                        "sp_precio_mxn_2016_yahoo_dex": c_yah}

    configs = [
        Universo("A-datos: SPY adjclose (Yahoo) x DEXMXUS (FRED, V04) ; CETES subasta SF43936 (V04) [control de codigo]",
                 spy_a, dex_a, cet_a),
        Universo("B1 (segunda fuente principal): French CRSP VW TR x FIX Banxico ; CETES SF282 promedio mensual Banxico",
                 french, fix_b, cet_men_b),
        Universo("B2: French CRSP VW TR x DEXMXUS (ALFRED 2026-10-07) ; CETES FMI INTGSTMXM193N (ALFRED)",
                 french, dex_b, cet_fmi),
        Universo("B3 (aisla FX): SPY adjclose (A) x FIX Banxico ; CETES subasta SF43936 (descarga nueva)",
                 spy_a, fix_b, cet_sub_b),
        Universo("B4 (aisla activo): French CRSP VW TR x DEXMXUS (A) ; CETES subasta SF43936 (A)",
                 french, dex_a, cet_a),
    ]
    RES["config"] = {}
    for u in configs:
        RES["config"][u.nombre.split(":")[0]] = correr(u)
    # Diagnostico: meses en que la senal SMA10-MXN difiere entre A-datos y cada configuracion B
    p("")
    p("=" * 100)
    p("Meses con senal SMA10-MXN distinta de A-datos (w de A -> w de B); misma regla, mismo codigo")
    base = {f[0]: f[3] for f in configs[0].sim(10, "MXN", "T1")}
    RES["meses_senal_distinta"] = {}
    for u in configs[1:]:
        otra = {f[0]: f[3] for f in u.sim(10, "MXN", "T1")}
        dif = [f"{y}-{m:02d}:{int(base[(y, m)])}->{int(otra[(y, m)])}" for (y, m) in sorted(base) if base[(y, m)] != otra[(y, m)]]
        RES["meses_senal_distinta"][u.nombre.split(":")[0]] = dif
        p(f"  {u.nombre.split(':')[0]}: {len(dif)} meses: {' '.join(dif)}")
    # Margen de la senal (precio/SMA - 1) en esos meses, A contra B1
    p("  Margen de la senal MXN (P/SMA10 - 1) en A y en B1 para los meses distintos de B1:")
    for et in RES["meses_senal_distinta"]["B1 (segunda fuente principal)"]:
        y, m = int(et[:4]), int(et[5:7])
        fila = []
        for u in (configs[0], configs[1]):
            i = u.meses.index((y, m))
            h = [u.mxn[u.E[u.meses[j]]] for j in range(i - 10, i)]
            fila.append(h[-1] / (sum(h) / 10) - 1)
        p(f"    {et}: A {fila[0]*100:+.2f}%  B1 {fila[1]*100:+.2f}%")
    # Caida maxima de SMA10-MXN-T1 1995-2007: pico y valle
    for u in (configs[0], configs[1]):
        fl = [f for f in u.sim(10, "MXN", "T1") if (1995, 1) <= f[0] <= (2007, 12)]
        v, pico, ip, peor, rango_ = 1.0, 1.0, fl[0][1], 0.0, None
        for f in fl:
            v *= 1 + f[6]
            if v > pico:
                pico, ip = v, f[2]
            if v / pico - 1 < peor:
                peor, rango_ = v / pico - 1, (ip, f[2])
        p(f"  MDD SMA10-MXN-T1 1995-2007 {u.nombre.split(':')[0]}: {peor*100:.1f}% de {rango_[0]} a {rango_[1]}")
    # Efecto de terminar T1 el 2026-08-31 (French no tiene 2026-09-01): datos A recortados
    ua = Universo("A recortado a 2026-08-31", {d: v for d, v in spy_a.items() if d <= date(2026, 8, 31)}, dex_a, cet_a)
    p("")
    p("Datos A recortados a 2026-08-31 (como B1/B2/B4, sin el 2026-09-01 que cierra el ultimo periodo T1):")
    for clave, nom in (((10, "MXN", "T1"), "SMA10-MXN-T1"), (None, "BH-T1")):
        f = ua.sim(10, "MXN", "T1", bh=(clave is None))
        mt = metricas(f, (2008, 1), (2026, 8))
        p(f"  {nom} 2008-2026: CAGR {mt['cagr']*100:.2f}%  MDD {mt['mdd']*100:.1f}%  hasta {mt['hasta']}")
    d = dif_nw(ua.sim(10, "MXN", "T1"), ua.sim(10, "MXN", "T1", bh=True), (2008, 1), (2026, 8))
    p(f"  dif SMA10-MXN-T1 - BH-T1 2008-2026: {d['anual_pp']:+.3f} pp/ano, t {d['t']:.3f}")
    RES["A_recortado_0831"] = d
    if cet_men_b.arrastre or cet_fmi.arrastre:
        p("")
        p(f"Meses de CETES con tasa arrastrada (falta el dato): SF282 {sorted(cet_men_b.arrastre)}; FMI {sorted(cet_fmi.arrastre)}")

    p("")
    p("=" * 100)
    p("IPC (A2): NAFTRAC adjclose Yahoo (piso: sin dividendos en varios anos) y OECD precio (promedio mensual)")
    RES["ipc"] = {"naftrac_A": ipc("NAFTRAC A (V04, 2026-09-25)", os.path.join(DA, "yahoo_NAFTRAC.MX_1d.json")),
                  "naftrac_B": ipc("NAFTRAC B (descarga 2026-10-07)", os.path.join(DB, "yahoo_NAFTRAC.MX_1d.json"))}
    oecd = lee_fred(os.path.join(DB, "alfred_SPASTT01MXM661N.csv"))
    o0, o1 = date(2007, 12, 1), date(2026, 8, 1)
    c_o = (oecd[o1] / oecd[o0]) ** (1 / (18 + 8 / 12)) - 1
    RES["ipc"]["oecd_precio"] = c_o
    p(f"  OECD SPASTT01MXM661N (precio, promedio mensual) dic-2007..ago-2026: {c_o*100:.2f}% (sin dividendos)")
    mxx, _ = lee_yahoo(os.path.join(DA, "yahoo_MXX_1d.json"), "close")
    f = sorted(d for d in mxx if d <= date(2026, 8, 31))
    m0, m1 = ultimo_le(f, date(2007, 12, 31)), f[-1]
    c_m = cagr(mxx[m0], mxx[m1], m0, m1)
    RES["ipc"]["mxx_precio_A"] = c_m
    p(f"  ^MXX precio (A) {m0}..{m1}: {c_m*100:.2f}% (referencia del precio con la serie de A)")

    with open(os.path.join(AQUI, "resultados.json"), "w") as fh:
        json.dump(RES, fh, indent=1, ensure_ascii=False, sort_keys=True, default=str)
    print("\n".join(SALIDA))


if __name__ == "__main__":
    main()
