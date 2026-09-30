#!/usr/bin/env python3
"""AC-09: segunda ejecucion independiente (ciega) de R01, timing SMA de 10 meses (Faber).

Escrito desde el pre-registro de R01 (secciones 1 a 9), sin leer R01.py ni sus salidas.
Biblioteca estandar de Python 3.11. De herramientas/ solo usa parsear_yahoo_json y
parsear_fred_csv (lectores genericos). La senal, la alineacion de fechas, los costos y las
metricas estan escritos aqui.

Fuentes (distintas de A, que usa French/CRSP):
  - Shiller, ie_data.xls (shillerdata.com, guardado 2026-09-02): dividendos D mensuales
    (y precio promedio mensual P para la sensibilidad "Shiller puro").
  - Yahoo ^GSPC diario (cierres de fin de mes, precio) desde 1927-12.
  - Yahoo ^SP500TR diario (rendimiento total) desde 1988-01; tambien la descarga range=30y.
  - FRED TB3MS (T-bill 3 meses, desde 1934) y M1329AUSM193NNBR (NBER, 1920-1933).
  - FRED DEXMXUS e INTGSTMXM193N (moneda MXN).

Uso: python3 laboratorio/auditorias/AC-09-sma10-faber/AC09.py   (sin red; lee datos/)
"""
from __future__ import annotations

import hashlib
import json
import math
import random
import statistics
import struct
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ))
from herramientas.datos import parsear_fred_csv, parsear_yahoo_json  # noqa: E402

AQUI = Path(__file__).resolve().parent
DATOS = AQUI / "datos"
SALIDA: list[str] = []
RES: dict = {}

COSTO_DEF = 0.0029 + 0.0005          # comision GBM + spread, por lado
ULTIMO_MES = (2026, 8)                # ultimo mes completo (2026-09 es intradia)


def p(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    SALIDA.append(s)


# ------------------------------------------------------------ lector OLE2 + BIFF8 propio
def ole_flujo(b: bytes, nombre: str) -> bytes:
    if b[:8] != bytes.fromhex("D0CF11E0A1B11AE1"):
        raise ValueError("no es OLE2")
    ssz = 1 << struct.unpack_from("<H", b, 0x1E)[0]
    n_fat, dir_ini = struct.unpack_from("<II", b, 0x2C)
    dif_ini, n_dif = struct.unpack_from("<II", b, 0x44)
    dif = list(struct.unpack_from("<109I", b, 0x4C))
    s = dif_ini
    for _ in range(n_dif):
        off = (s + 1) * ssz
        vals = struct.unpack_from(f"<{ssz // 4}I", b, off)
        dif.extend(vals[:-1])
        s = vals[-1]
    fat: list[int] = []
    for sec in dif[:n_fat]:
        fat.extend(struct.unpack_from(f"<{ssz // 4}I", b, (sec + 1) * ssz))

    def cadena(ini):
        out, s, vistos = [], ini, 0
        while s < 0xFFFFFFFA and vistos < len(fat):
            out.append(b[(s + 1) * ssz:(s + 2) * ssz])
            s = fat[s]
            vistos += 1
        return b"".join(out)

    d = cadena(dir_ini)
    for i in range(0, len(d), 128):
        e = d[i:i + 128]
        ln = struct.unpack_from("<H", e, 0x40)[0]
        nm = e[:max(ln - 2, 0)].decode("utf-16-le", "ignore")
        if nm == nombre:
            ini, tam = struct.unpack_from("<II", e, 0x74)
            if tam < 4096:
                raise ValueError("flujo en mini-stream (no soportado)")
            return cadena(ini)[:tam]
    raise ValueError(f"flujo {nombre} no encontrado")


def rk(v: int) -> float:
    if v & 2:
        x = float(v >> 2 if v < 2**31 else (v >> 2) - (1 << 30))
    else:
        x = struct.unpack("<d", struct.pack("<Q", (v & 0xFFFFFFFC) << 32))[0]
    return x / 100 if v & 1 else x


def biff_hoja(libro: bytes, hoja: str) -> dict[tuple[int, int], float]:
    pos, hojas = 0, {}
    while pos + 4 <= len(libro):
        rid, ln = struct.unpack_from("<HH", libro, pos)
        dat = libro[pos + 4:pos + 4 + ln]
        if rid == 0x0085:
            bof = struct.unpack_from("<I", dat, 0)[0]
            cch, fl = dat[6], dat[7]
            nm = dat[8:8 + cch * 2].decode("utf-16-le") if fl & 1 else dat[8:8 + cch].decode("latin-1")
            hojas[nm] = bof
        if rid == 0x000A:
            break
        pos += 4 + ln
    pos, celdas = hojas[hoja], {}
    while pos + 4 <= len(libro):
        rid, ln = struct.unpack_from("<HH", libro, pos)
        dat = libro[pos + 4:pos + 4 + ln]
        if rid == 0x0203:
            r, c = struct.unpack_from("<HH", dat, 0)
            celdas[(r, c)] = struct.unpack_from("<d", dat, 6)[0]
        elif rid == 0x027E:
            r, c = struct.unpack_from("<HH", dat, 0)
            celdas[(r, c)] = rk(struct.unpack_from("<I", dat, 6)[0])
        elif rid == 0x00BD:
            r, c0 = struct.unpack_from("<HH", dat, 0)
            n = (ln - 6) // 6
            for k in range(n):
                celdas[(r, c0 + k)] = rk(struct.unpack_from("<I", dat, 4 + 6 * k + 2)[0])
        elif rid == 0x0006:
            r, c = struct.unpack_from("<HH", dat, 0)
            if dat[12:14] != b"\xff\xff":
                celdas[(r, c)] = struct.unpack_from("<d", dat, 6)[0]
        elif rid == 0x000A:
            break
        pos += 4 + ln
    return celdas


# ------------------------------------------------------------ carga de datos
def mes_de(d) -> tuple[int, int]:
    return (d.year, d.month)


def sig(m):
    return (m[0] + (m[1] == 12), m[1] % 12 + 1)


def ant(m):
    return (m[0] - (m[1] == 1), (m[1] - 2) % 12 + 1)


def rango(a, b):
    out, m = [], a
    while m <= b:
        out.append(m)
        m = sig(m)
    return out


def ftxt(m):
    return f"{m[0]}-{m[1]:02d}"


def cargar_shiller():
    celdas = biff_hoja(ole_flujo((DATOS / "shiller_ie_data.xls").read_bytes(), "Workbook"), "Data")
    filas = sorted({r for r, _ in celdas})
    P, D = {}, {}
    for r in filas:
        a = celdas.get((r, 0))
        if a is None or not (1870 < a < 2100):
            continue
        y = int(a)
        mo = int(round((a - y) * 100))
        if not 1 <= mo <= 12:
            continue
        if (r, 1) in celdas:
            P[(y, mo)] = celdas[(r, 1)]
        if (r, 2) in celdas and celdas[(r, 2)] > 0:
            D[(y, mo)] = celdas[(r, 2)]
    return P, D


def fin_de_mes_yahoo(nombre):
    ser = parsear_yahoo_json((DATOS / nombre).read_text())["serie"]
    out = {}
    for d, v in ser:
        out[mes_de(d)] = (d, v)
    return {m: v for m, (d, v) in out.items() if m <= ULTIMO_MES}, ser


def fred_mensual(nombre):
    return {mes_de(d): v for d, v in parsear_fred_csv((DATOS / nombre).read_text())}


def fred_fin_de_mes_diario(nombre, max_dias=10):
    ser = parsear_fred_csv((DATOS / nombre).read_text())
    out = {}
    for d, v in ser:
        out[mes_de(d)] = (d, v)
    res = {}
    for m, (d, v) in out.items():
        fin = date(m[0] + (m[1] == 12), m[1] % 12 + 1, 1)
        if (fin - d).days - 1 <= max_dias:
            res[m] = v
    return res


# ------------------------------------------------------------ metricas
def nivel(rend: dict, meses):
    I, v = {}, 1.0
    I[ant(meses[0])] = v
    for m in meses:
        v *= 1 + rend[m]
        I[m] = v
    return I


def pesos(I: dict, meses, regla: str, n=10, rezago=0):
    """w[m] decidido al cierre del mes m-1 (o m-1-rezago) con niveles hasta ese mes."""
    w = {}
    for m in meses:
        u = ant(m)
        for _ in range(rezago):
            u = ant(u)
        if regla == "bh":
            w[m] = 1.0
        elif regla == "efectivo":
            w[m] = 0.0
        elif regla == "sma":
            ven, x = [], u
            for _ in range(n):
                ven.append(I[x])
                x = ant(x)
            w[m] = 1.0 if I[u] > sum(ven) / n else 0.0
        elif regla == "mom":
            x = u
            for _ in range(n):
                x = ant(x)
            w[m] = 1.0 if I[u] > I[x] else 0.0
        else:
            raise ValueError(regla)
    return w


def correr(r: dict, rf: dict, w: dict, meses, costo=COSTO_DEF, rf_efectivo=None):
    caja = rf_efectivo or rf
    out, prev = {}, 0.0
    for m in meses:
        out[m] = w[m] * r[m] + (1 - w[m]) * caja[m] - abs(w[m] - prev) * costo
        prev = w[m]
    return out


def metricas(serie: dict, rf: dict, w: dict | None, a, b):
    ms = [m for m in rango(a, b) if m in serie]
    x = [serie[m] for m in ms]
    ex = [serie[m] - rf[m] for m in ms]
    n = len(x)
    v, pico, mdd = 1.0, 1.0, 0.0
    for q in x:
        v *= 1 + q
        pico = max(pico, v)
        mdd = min(mdd, v / pico - 1)
    sd = statistics.stdev(x)
    sde = statistics.stdev(ex)
    d = {"desde": ftxt(ms[0]), "hasta": ftxt(ms[-1]), "n": n,
         "cagr": v ** (12 / n) - 1, "vol": sd * math.sqrt(12),
         "sharpe": (statistics.fmean(ex) / sde * math.sqrt(12)) if sde > 0 else 0.0,
         "mdd": mdd}
    if w is not None:
        ws = [w[m] for m in ms]
        salidas = sum(1 for i in range(1, n) if ws[i - 1] == 1 and ws[i] == 0)
        d["invertido"] = statistics.fmean(ws)
        d["salidas_por_anio"] = salidas / (n / 12)
        d["cambios"] = sum(1 for i in range(1, n) if ws[i] != ws[i - 1])
    return d


def fmt(d):
    extra = ""
    if "invertido" in d:
        extra = f" | inv {d['invertido']*100:5.1f}% | salidas/año {d['salidas_por_anio']:.2f}"
    return (f"CAGR {d['cagr']*100:6.2f}% | vol {d['vol']*100:5.2f}% | Sharpe {d['sharpe']:.3f} | "
            f"MDD {d['mdd']*100:7.2f}%{extra} | n {d['n']}")


def newey_west_t(x, L=6):
    n = len(x)
    mu = statistics.fmean(x)
    e = [q - mu for q in x]
    g0 = sum(q * q for q in e) / n
    s = g0
    for l in range(1, L + 1):
        g = sum(e[i] * e[i - l] for i in range(l, n)) / n
        s += 2 * (1 - l / (L + 1)) * g
    se = math.sqrt(s / n)
    return mu, se, mu / se


def norm_cdf(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def norm_ppf(p_):
    lo, hi = -10.0, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if norm_cdf(mid) < p_:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def dsr(ex: list[float], sr_ensayos: list[float], N: int):
    """Deflated Sharpe (Bailey y Lopez de Prado 2014), Sharpe mensual sin anualizar."""
    T = len(ex)
    mu, sd = statistics.fmean(ex), statistics.pstdev(ex)
    sr = mu / sd
    sk = sum(((q - mu) / sd) ** 3 for q in ex) / T
    ku = sum(((q - mu) / sd) ** 4 for q in ex) / T
    V = statistics.variance(sr_ensayos)
    g = 0.5772156649
    sr0 = math.sqrt(V) * ((1 - g) * norm_ppf(1 - 1 / N) + g * norm_ppf(1 - 1 / (N * math.e)))
    z = (sr - sr0) * math.sqrt(T - 1) / math.sqrt(1 - sk * sr + (ku - 1) / 4 * sr * sr)
    return {"sr_mensual": sr, "sr0": sr0, "V": V, "N": N, "dsr": norm_cdf(z), "psr0": norm_cdf(
        sr * math.sqrt(T - 1) / math.sqrt(1 - sk * sr + (ku - 1) / 4 * sr * sr))}


def boot_dsharpe(a: list[float], b: list[float], rfl: list[float], bloque=12, reps=5000, semilla=9):
    n = len(a)
    rnd = random.Random(semilla)

    def sh(x, r):
        e = [p_ - q for p_, q in zip(x, r)]
        s = statistics.stdev(e)
        return statistics.fmean(e) / s * math.sqrt(12)

    obs = sh(a, rfl) - sh(b, rfl)
    difs = []
    for _ in range(reps):
        idx = []
        while len(idx) < n:
            i0 = rnd.randrange(n)
            idx.extend((i0 + k) % n for k in range(bloque))
        idx = idx[:n]
        difs.append(sh([a[i] for i in idx], [rfl[i] for i in idx]) - sh([b[i] for i in idx], [rfl[i] for i in idx]))
    difs.sort()
    return obs, difs[int(0.025 * reps)], difs[int(0.975 * reps) - 1]


# ------------------------------------------------------------ principal
def main():
    # huellas
    lineas = []
    for f in sorted(DATOS.iterdir()):
        if f.name == "SHA256SUMS.txt":
            continue
        lineas.append(f"{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.name}")
    (DATOS / "SHA256SUMS.txt").write_text("\n".join(lineas) + "\n")
    p("AC-09 | auditoria ciega de R01 (SMA 10 meses, Faber) | fuentes: Shiller + Yahoo ^GSPC/^SP500TR + FRED")
    for l_ in lineas:
        p("  sha256", l_)
    RES["sha256"] = dict(reversed(l_.split("  ")) for l_ in lineas)

    P_sh, D_sh = cargar_shiller()
    gspc, _ = fin_de_mes_yahoo("yahoo_GSPC_1d.json")
    sptr, _ = fin_de_mes_yahoo("yahoo_SP500TR_1d.json")
    sptr30, _ = fin_de_mes_yahoo("yahoo_SP500TR_1d_30y.json")
    sptr_mo = {mes_de(d): v for d, v in parsear_yahoo_json(
        (DATOS / "yahoo_SP500TR_1mo_30y.json").read_text(), "1mo")["serie"]}
    tb3 = fred_mensual("fred_TB3MS.csv")
    nber = fred_mensual("fred_M1329AUSM193NNBR.csv")
    fx = fred_fin_de_mes_diario("fred_DEXMXUS.csv")
    cetes = fred_mensual("fred_INTGSTMXM193N.csv")
    fin_D = max(D_sh)
    p(f"Shiller P: {ftxt(min(P_sh))} a {ftxt(max(P_sh))}; D: {ftxt(min(D_sh))} a {ftxt(fin_D)}")
    p(f"^GSPC fin de mes: {ftxt(min(gspc))} a {ftxt(max(gspc))}; ^SP500TR: {ftxt(min(sptr))} a {ftxt(max(sptr))}")
    p(f"TB3MS hasta {ftxt(max(tb3))}; DEXMXUS fin de mes hasta {ftxt(max(fx))}; Cetes FMI hasta {ftxt(max(cetes))}")
    # control range=30y diario contra period1 diario, y barras 1mo
    com = [m for m in sptr30 if m in sptr]
    dmax = max(abs(sptr30[m] / sptr[m] - 1) for m in com)
    p(f"Control ^SP500TR range=30y vs period1 (fin de mes, {len(com)} meses): dif. relativa max {dmax:.2e}")
    RES["control_sp500tr_30y_vs_period1"] = dmax

    # tasa libre de riesgo: tasa del mismo mes / 1200 (NBER 1920-1933, TB3MS desde 1934)
    rf = {}
    for m in rango((1920, 1), ULTIMO_MES):
        tasa = tb3.get(m) if m >= (1934, 1) else nber.get(m)
        if tasa is None:
            raise SystemExit(f"falta rf en {ftxt(m)}")
        rf[m] = tasa / 1200

    # --- serie principal B1: ^GSPC fin de mes + D Shiller/12 hasta 1988-01; ^SP500TR desde 1988-02
    r_b1, r_b2, r_pr = {}, {}, {}
    for m in rango((1928, 1), ULTIMO_MES):
        a_ = ant(m)
        pr = gspc[m] / gspc[a_] - 1
        r_pr[m] = pr
        if m in D_sh:
            r_b2[m] = pr + D_sh[m] / 12 / gspc[a_]
        if m <= (1988, 1):
            r_b1[m] = r_b2[m]
        else:
            r_b1[m] = sptr[m] / sptr[a_] - 1
    # --- sensibilidad B3: Shiller puro (precio promedio mensual + D/12), desde 1920
    r_b3 = {}
    for m in rango((1920, 1), min(max(P_sh), ULTIMO_MES)):
        if m in D_sh and ant(m) in P_sh:
            r_b3[m] = (P_sh[m] + D_sh[m] / 12) / P_sh[ant(m)] - 1

    # empalme: control de dividendos Shiller contra ^SP500TR en el traslape
    tras = [m for m in rango((1988, 2), fin_D) if m in r_b2]
    c_b2 = math.prod(1 + r_b2[m] for m in tras) ** (12 / len(tras)) - 1
    c_tr = math.prod(1 + (sptr[m] / sptr[ant(m)] - 1) for m in tras) ** (12 / len(tras)) - 1
    p(f"Traslape {ftxt(tras[0])}-{ftxt(tras[-1])}: CAGR ^GSPC+D Shiller {c_b2*100:.2f}% vs ^SP500TR {c_tr*100:.2f}%")
    RES["traslape_divs"] = {"desde": ftxt(tras[0]), "hasta": ftxt(tras[-1]), "gspc_mas_D": c_b2, "sp500tr": c_tr}

    INI_B1 = (1929, 1)   # 12 rendimientos (1928-01..1928-12) antes de la primera decision
    FIN_A = (2026, 7)
    SEG = {
        "dentro": (INI_B1, (2006, 12)),
        "fuera_A": ((2007, 1), FIN_A),
        "fuera_ext": ((2007, 1), ULTIMO_MES),
        "articulo_2005": (INI_B1, (2005, 12)),
        "articulo_2012": (INI_B1, (2012, 12)),
        "toda": (INI_B1, FIN_A),
    }

    def bloque(r, meses, ini_sig, variantes, segs, rfl=rf, etiqueta=""):
        I = nivel(r, [m for m in rango(ini_sig, meses[-1])])
        out = {}
        for nombre, (regla, n, rez, costo, Isig) in variantes.items():
            w = pesos(Isig or I, meses, regla, n, rez)
            s = correr(r, rfl, w, meses, costo)
            out[nombre] = {"serie": s, "w": w,
                           "seg": {k: metricas(s, rfl, w, a, b) for k, (a, b) in segs.items()}}
        return out

    # indice de precio para la senal sobre ^GSPC
    I_pr = nivel(r_pr, rango((1928, 1), ULTIMO_MES))
    meses_b1 = rango(INI_B1, ULTIMO_MES)
    V = {
        "comprar_y_mantener": ("bh", 0, 0, COSTO_DEF, None),
        "efectivo": ("efectivo", 0, 0, COSTO_DEF, None),
        "sma6": ("sma", 6, 0, COSTO_DEF, None),
        "sma8": ("sma", 8, 0, COSTO_DEF, None),
        "sma10": ("sma", 10, 0, COSTO_DEF, None),
        "sma12": ("sma", 12, 0, COSTO_DEF, None),
        "mom12": ("mom", 12, 0, COSTO_DEF, None),
        "sma10_rezago1m": ("sma", 10, 1, COSTO_DEF, None),
        "sma10_senal_precio_GSPC": ("sma", 10, 0, COSTO_DEF, I_pr),
        "sma10_sin_costos": ("sma", 10, 0, 0.0, None),
        "bh_sin_costos": ("bh", 0, 0, 0.0, None),
        "sma10_c044": ("sma", 10, 0, 0.0029 + 0.0015, None),
        "sma10_c059": ("sma", 10, 0, 0.0029 + 0.0030, None),
        "sma10_c068": ("sma", 10, 0, 0.0058 + 0.0010, None),
    }
    B1 = bloque(r_b1, meses_b1, (1928, 1), V, SEG)

    p("")
    p("=" * 110)
    p("B1 (principal): ^GSPC fin de mes + dividendos Shiller hasta 1988-01; ^SP500TR desde 1988-02; rf NBER/TB3MS")
    p("Senal: I_{t-1} > media(I_{t-10..t-1}) -> w_t = 1; costo |dw| x 0.34%; exposicion inicial 0")
    p("=" * 110)
    orden_seg = ["dentro", "fuera_A", "fuera_ext", "articulo_2005", "articulo_2012", "toda"]
    for seg in orden_seg:
        a, b = SEG[seg]
        p(f"\n-- {seg}: {ftxt(a)} a {ftxt(b)}")
        for nm, d in B1.items():
            if seg.startswith("articulo") and nm not in ("sma10_sin_costos", "bh_sin_costos", "sma10", "comprar_y_mantener"):
                continue
            p(f"  {nm:26s} {fmt(d['seg'][seg])}")
    RES["B1"] = {nm: d["seg"] for nm, d in B1.items()}

    # criterios del pre-registro
    def criterios(B, seg_art, seg_in, seg_out, etiqueta):
        s0, b0 = B["sma10_sin_costos"]["seg"][seg_art], B["bh_sin_costos"]["seg"][seg_art]
        red = 1 - s0["mdd"] / b0["mdd"]
        c = {"C1_reduccion_mdd": red, "C1": 0.30 <= red <= 0.60,
             "C2_dif_cagr_pp": (s0["cagr"] - b0["cagr"]) * 100, "C2": 0 < s0["cagr"] - b0["cagr"] <= 0.0191,
             "C3_invertido": s0["invertido"], "C3": 0.60 <= s0["invertido"] <= 0.80,
             "C4_salidas": s0["salidas_por_anio"], "C4": 0.40 <= s0["salidas_por_anio"] <= 1.00}
        si, bi = B["sma10"]["seg"][seg_in], B["comprar_y_mantener"]["seg"][seg_in]
        c["ref_a_red_mdd_neto"] = 1 - si["mdd"] / bi["mdd"]
        c["ref_b_sharpe"] = (si["sharpe"], bi["sharpe"])
        c["refutado"] = c["ref_a_red_mdd_neto"] < 0.20 or si["sharpe"] <= bi["sharpe"]
        so, bo = B["sma10"]["seg"][seg_out], B["comprar_y_mantener"]["seg"][seg_out]
        ro = 1 - so["mdd"] / bo["mdd"]
        c["fuera_red_mdd"] = ro
        c["fuera_sharpe"] = (so["sharpe"], bo["sharpe"])
        c["veredicto_fuera"] = ("No se sostiene" if ro < 0.20 else
                                "Se sostiene" if so["sharpe"] >= bo["sharpe"] else "Solo protección")
        if c["refutado"]:
            est = "No replicado"
        elif all(c[k] for k in ("C1", "C2", "C3", "C4")):
            est = "Replicado"
        else:
            est = "Replicado con diferencias"
        c["estado"] = est
        p(f"\n  Criterios [{etiqueta}] tramo articulo {seg_art}, sin costos:")
        p(f"    C1 reduccion relativa MDD {red:.3f} ({'cumple' if c['C1'] else 'NO cumple'}; rango 0.30-0.60)")
        p(f"    C2 dif. CAGR {c['C2_dif_cagr_pp']:+.2f} pp ({'cumple' if c['C2'] else 'NO cumple'}; (0, +1.91])")
        p(f"    C3 tiempo invertido {c['C3_invertido']:.3f} ({'cumple' if c['C3'] else 'NO cumple'}; 0.60-0.80)")
        p(f"    C4 salidas/año {c['C4_salidas']:.2f} ({'cumple' if c['C4'] else 'NO cumple'}; 0.40-1.00)")
        p(f"    Refutacion (dentro, neto): red. MDD {c['ref_a_red_mdd_neto']:.3f}; Sharpe sma10 {si['sharpe']:.3f} vs B&H {bi['sharpe']:.3f} -> {'REFUTADO' if c['refutado'] else 'no refutado'}")
        p(f"    Fuera de muestra ({seg_out}, neto): red. MDD {ro:.3f}; Sharpe {so['sharpe']:.3f} vs {bo['sharpe']:.3f} -> {c['veredicto_fuera']}")
        p(f"    Estado segun reglas del pre-registro: {est}")
        return c

    RES["criterios_B1"] = criterios(B1, "articulo_2005", "dentro", "fuera_A", "B1")
    RES["criterios_B1_fuera_ext"] = criterios(B1, "articulo_2005", "dentro", "fuera_ext", "B1, fuera hasta 2026-08")

    # significancia
    p("\n-- Significancia (B1)")
    sig_res = {}
    for seg in ("dentro", "fuera_A", "toda"):
        a, b = SEG[seg]
        ms = rango(a, b)
        dif = [B1["sma10"]["serie"][m] - B1["comprar_y_mantener"]["serie"][m] for m in ms]
        mu, se, t = newey_west_t(dif, 6)
        obs, lo, hi = boot_dsharpe([B1["sma10"]["serie"][m] for m in ms],
                                   [B1["comprar_y_mantener"]["serie"][m] for m in ms], [rf[m] for m in ms])
        sig_res[seg] = {"dif_media_mensual": mu, "se_nw6": se, "t_nw6": t,
                        "dsharpe": obs, "ic95_dsharpe_bootstrap_bloques12": [lo, hi]}
        p(f"  {seg:9s} sma10 - B&H neto: media {mu*100:+.3f}%/mes (×12 {mu*1200:+.2f}%), t NW6 {t:+.2f}; "
          f"ΔSharpe {obs:+.3f} IC95 bootstrap bloques [{lo:+.3f}, {hi:+.3f}]")
    a, b = SEG["dentro"]
    ms = rango(a, b)
    srs = []
    for nm in ("sma6", "sma8", "sma10", "sma12", "mom12"):
        e = [B1[nm]["serie"][m] - rf[m] for m in ms]
        srs.append(statistics.fmean(e) / statistics.pstdev(e))
    ex10 = [B1["sma10"]["serie"][m] - rf[m] for m in ms]
    for N in (5, 20):
        d_ = dsr(ex10, srs, N)
        sig_res[f"dsr_N{N}"] = d_
        p(f"  DSR sma10 dentro, N={N}: {d_['dsr']:.3f} (SR mensual {d_['sr_mensual']:.4f}, SR0 {d_['sr0']:.4f}, "
          f"V[SR] de 5 ensayos {d_['V']:.2e}); PSR(0) {d_['psr0']:.3f}")
    RES["significancia_B1"] = sig_res

    # --- sensibilidad B2: ^GSPC + D Shiller en todo el periodo hasta fin de D
    SEG2 = {"dentro": (INI_B1, (2006, 12)), "articulo_2005": (INI_B1, (2005, 12)),
            "fuera_hasta_finD": ((2007, 1), min(fin_D, FIN_A))}
    V2 = {k: V[k] for k in ("comprar_y_mantener", "sma10", "sma10_sin_costos", "bh_sin_costos")}
    meses_b2 = rango(INI_B1, min(fin_D, ULTIMO_MES))
    B2 = bloque(r_b2, meses_b2, (1928, 1), V2, SEG2)
    p("\n" + "=" * 110)
    p(f"B2 (sensibilidad): ^GSPC fin de mes + dividendos Shiller en todo el periodo (hasta {ftxt(fin_D)})")
    for seg in SEG2:
        p(f"-- {seg}: {ftxt(SEG2[seg][0])} a {ftxt(SEG2[seg][1])}")
        for nm, d in B2.items():
            p(f"  {nm:26s} {fmt(d['seg'][seg])}")
    RES["B2"] = {nm: d["seg"] for nm, d in B2.items()}

    # --- sensibilidad B3: Shiller puro (precio promedio), ventana exacta desde 1927-07
    fin3 = max(r_b3)
    SEG3 = {"dentro": ((1927, 7), (2006, 12)), "articulo_2005": ((1927, 7), (2005, 12)),
            "fuera_hasta_fin": ((2007, 1), min(fin3, FIN_A))}
    meses_b3 = rango((1927, 7), min(fin3, ULTIMO_MES))
    B3 = bloque(r_b3, meses_b3, (1920, 1), V2 | {"sma10_rezago1m": V["sma10_rezago1m"]}, SEG3)
    p("\n" + "=" * 110)
    p(f"B3 (sensibilidad): Shiller puro, (P_t + D_t/12)/P_(t-1) con P = promedio mensual; desde 1927-07 (hasta {ftxt(fin3)})")
    p("   Advertencia: el promedio mensual suaviza y autocorrelaciona los rendimientos; favorece al timing.")
    for seg in SEG3:
        p(f"-- {seg}: {ftxt(SEG3[seg][0])} a {ftxt(SEG3[seg][1])}")
        for nm, d in B3.items():
            p(f"  {nm:26s} {fmt(d['seg'][seg])}")
    RES["B3"] = {nm: d["seg"] for nm, d in B3.items()}
    RES["criterios_B3"] = criterios(B3, "articulo_2005", "dentro", "fuera_hasta_fin", "B3 Shiller puro")

    # --- MXN (bloque G): senal en USD (B1), rendimientos en MXN desde 1994-01
    p("\n" + "=" * 110)
    p("MXN (bloque G): senal sma10 en USD sobre B1; r_MXN = (1+r_USD)·FX_t/FX_(t-1) − 1; FX = DEXMXUS fin de mes")
    p("   Sharpe en MXN: exceso sobre Cetes (FMI INTGSTMXM193N/1200 del mismo mes)")
    mm = rango((1994, 1), FIN_A)
    fxr = {m: fx[m] / fx[ant(m)] for m in mm}
    r_mx = {m: (1 + r_b1[m]) * fxr[m] - 1 for m in mm}
    rf_usd_mx = {m: (1 + rf[m]) * fxr[m] - 1 for m in mm}
    ce = {m: cetes[m] / 1200 for m in mm}
    w10 = B1["sma10"]["w"]
    # la exposicion previa a 1994-01 viene de la corrida continua en USD
    w_prev = w10[ant(mm[0])]
    mx_res = {}
    for nm, w, caja in (("comprar_y_mantener", {m: 1.0 for m in mm}, rf_usd_mx),
                        ("sma10_caja_TbillUSD", w10, rf_usd_mx),
                        ("sma10_caja_Cetes", w10, ce),
                        ("efectivo_TbillUSD", {m: 0.0 for m in mm}, rf_usd_mx),
                        ("efectivo_Cetes", {m: 0.0 for m in mm}, ce)):
        s, prev = {}, (w_prev if nm.startswith("sma10") else (1.0 if nm == "comprar_y_mantener" else 0.0))
        for m in mm:
            s[m] = w[m] * r_mx[m] + (1 - w[m]) * caja[m] - abs(w[m] - prev) * COSTO_DEF
            prev = w[m]
        mx_res[nm] = {}
        for seg, (a, b) in {"1994-2006": ((1994, 1), (2006, 12)), "fuera_A": ((2007, 1), FIN_A),
                            "1994-2026": ((1994, 1), FIN_A)}.items():
            mx_res[nm][seg] = metricas(s, ce, None, a, b)
    for seg in ("1994-2006", "fuera_A", "1994-2026"):
        p(f"-- {seg}")
        for nm in mx_res:
            p(f"  {nm:26s} {fmt(mx_res[nm][seg])}")
    RES["MXN"] = mx_res

    conciliacion(B1, r_b1, rf, SEG)

    (AQUI / "salida.txt").write_text("\n".join(SALIDA) + "\n")
    (AQUI / "resultados.json").write_text(json.dumps(RES, indent=1, ensure_ascii=False, default=str))


# ------------------------------------------------------------ conciliacion (post-hoc)
def dd_fechas(serie: dict, a, b):
    v, pico, mp, peor = 1.0, 1.0, ant(a), (0.0, None, None)
    for m in rango(a, b):
        v *= 1 + serie[m]
        if v > pico:
            pico, mp = v, m
        dd = v / pico - 1
        if dd < peor[0]:
            peor = (dd, mp, m)
    return peor


def french():
    import io
    import zipfile
    z = zipfile.ZipFile(DATOS / "french_F-F_Research_Data_Factors_CSV_202607.zip")
    txt = z.read(z.namelist()[0]).decode("latin-1").splitlines()
    r, rf = {}, {}
    for l_ in txt[5:]:
        if not l_.strip():
            break
        c = [x.strip() for x in l_.split(",")]
        m = (int(c[0][:4]), int(c[0][4:]))
        r[m] = (float(c[1]) + float(c[4])) / 100
        rf[m] = float(c[4]) / 100
    return r, rf


def conciliacion(B1, r_b1, rf_b, SEG):
    """Agregado DESPUES de leer los resultados de A. No cambia ninguna cifra anterior."""
    p("\n" + "=" * 110)
    p("CONCILIACION CON A (post-hoc, agregada despues de leer R01 §10-§16; no cambia las cifras de arriba)")
    p("=" * 110)
    C = {}
    # 1) fechas de los MDD de B1
    for nm in ("sma10", "comprar_y_mantener"):
        for seg in ("dentro", "fuera_A"):
            dd, pk, vl = dd_fechas(B1[nm]["serie"], *SEG[seg])
            p(f"  MDD B1 {nm:20s} {seg:8s} {dd*100:7.2f}%  pico {ftxt(pk)}  valle {ftxt(vl)}")
            C[f"mdd_fechas_B1_{nm}_{seg}"] = [dd, ftxt(pk), ftxt(vl)]
    # 2) control C: el codigo de B sobre French 202607 (datos de A), con la ventana de A
    rF, rfF = french()
    VF = {"comprar_y_mantener": ("bh", 0, 0, COSTO_DEF), "sma10": ("sma", 10, 0, COSTO_DEF),
          "sma10_sin_costos": ("sma", 10, 0, 0.0), "bh_sin_costos": ("bh", 0, 0, 0.0),
          "sma10_rezago1m": ("sma", 10, 1, COSTO_DEF), "mom12": ("mom", 12, 0, COSTO_DEF),
          "sma12": ("sma", 12, 0, COSTO_DEF), "sma8": ("sma", 8, 0, COSTO_DEF), "sma6": ("sma", 6, 0, COSTO_DEF)}
    mF = rango((1927, 7), (2026, 7))
    IF = nivel(rF, rango((1926, 7), (2026, 7)))
    segF = {"dentro_A": ((1927, 7), (2006, 12)), "fuera_A": ((2007, 1), (2026, 7)),
            "articulo_A": ((1927, 7), (2005, 12)), "dentro_desde1929": ((1929, 1), (2006, 12))}
    CF = {}
    p("\n  Control C: codigo B sobre French 202607 (Mkt-RF + RF; rf = RF de French), decisiones desde 1927-07")
    for nm, (regla, n, rez, costo) in VF.items():
        w = pesos(IF, mF, regla, n, rez)
        s = correr(rF, rfF, w, mF, costo)
        CF[nm] = {"w": w, "serie": s, "seg": {k: metricas(s, rfF, w, a, b) for k, (a, b) in segF.items()}}
    for seg in segF:
        p(f"  -- {seg}: {ftxt(segF[seg][0])} a {ftxt(segF[seg][1])}")
        for nm in CF:
            p(f"     {nm:22s} {fmt(CF[nm]['seg'][seg])}")
    s0, b0 = CF["sma10_sin_costos"]["seg"]["articulo_A"], CF["bh_sin_costos"]["seg"]["articulo_A"]
    p(f"  Control C, C1 reduccion MDD tramo articulo sin costos: {1 - s0['mdd']/b0['mdd']:.4f}; C2 {(s0['cagr']-b0['cagr'])*100:+.3f} pp")
    C["control_C_french"] = {nm: d["seg"] for nm, d in CF.items()}
    # 3) desacuerdo de senal B1 (S&P) contra French, y descomposicion senal/rendimiento
    wB, wF = B1["sma10"]["w"], CF["sma10"]["w"]
    for seg in ("dentro", "fuera_A"):
        a, b = SEG[seg]
        ms = rango(a, b)
        dif = [m for m in ms if wB[m] != wF[m]]
        p(f"\n  Senal sma10 S&P (B1) vs French, {seg}: {len(dif)} de {len(ms)} meses distintos")
        p("    " + ", ".join(f"{ftxt(m)}(B{int(wB[m])}/F{int(wF[m])})" for m in dif))
        C[f"meses_senal_distinta_{seg}"] = [ftxt(m) for m in dif]
    # descomposicion: cruzar senales y rendimientos en fuera_A y dentro_desde1929
    p("\n  Descomposicion (neto, 0.34%/lado): senal x rendimientos")
    for seg, (a, b) in (("fuera_A", SEG["fuera_A"]), ("dentro_desde1929", ((1929, 1), (2006, 12)))):
        ms = rango((1929, 1), b)
        for et, w, r_, rfx in (("senal S&P  + rend S&P   (B1)", wB, r_b1, rf_b),
                               ("senal French + rend S&P", wF, r_b1, rf_b),
                               ("senal S&P  + rend French", wB, rF, rfF),
                               ("senal French + rend French", wF, rF, rfF)):
            s = correr(r_, rfx, w, ms)
            d = metricas(s, rfx, w, a, b)
            bh = metricas(correr(r_, rfx, {m: 1.0 for m in ms}, ms), rfx, None, a, b)
            p(f"    {seg:17s} {et:28s} {fmt(d)} || B&H Sharpe {bh['sharpe']:.3f}")
            C[f"descomp_{seg}_{et}"] = {"sma10": d, "bh": bh}
    RES["conciliacion"] = C


if __name__ == "__main__":
    main()
