#!/usr/bin/env python3
"""AC-11: segunda ejecucion independiente (ciega) de R07, curva 10a-3m y recesion (Estrella-Mishkin).

Escrito desde el pre-registro de R07 (secciones 1 a 9), sin leer R07.py, R07_verificacion.py,
R07-salida.txt, R07-resultados.json ni R07-variantes.csv.
Python 3.11 + numpy. De herramientas/ solo usa parsear_fred_csv y parsear_yahoo_json (lectores
genericos); del codigo de AC-09 solo el lector OLE2/BIFF8 del xls de Shiller (copiado abajo).
Probit (Newton-Raphson), Newey-West, pseudo R2 de Estrella, etiquetas en tiempo real, motor,
costos, metricas y DSR estan escritos aqui.

Fuentes (distintas de A, que usa FRED GS10/TB3MS mensuales, USREC/USRECQ y French):
  - FRED DGS10 (10a CMT diario, desde 1962-01-02) -> promedio mensual de dias habiles.
  - FRED IRLTLT01USM156N (OECD, rendimiento largo de EUA, mensual) solo 1953-04 a 1961-12.
  - FRED DTB3 (T-bill 3m diario, base descuento, desde 1954-01-04): BEY dia a dia y promedio.
  - FRED T10Y3M (diario, desde 1982) y DGS3MO: control y episodio 2022-2024.
  - NBER: business_cycle_dates.json (picos y valles mensuales), tabla de picos/valles
    trimestrales (pagina "US Business Cycle Expansions and Contractions") y pagina de anuncios.
  - Acciones: Yahoo ^GSPC (cierre de fin de mes) + dividendos de Shiller D/12 hasta 1996-10;
    Yahoo ^SP500TR desde 1996-11. Efectivo: DTB3 promedio mensual / 1200.
  - FRED DEXMXUS (MXN por USD) para la sensibilidad en pesos.

Uso: python3 laboratorio/auditorias/AC-11-curva-recesion/AC11.py   (sin red; lee datos/)
"""
from __future__ import annotations

import hashlib
import html
import json
import math
import re
import struct
import sys
from datetime import date
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ))
from herramientas.datos import parsear_fred_csv, parsear_yahoo_json  # noqa: E402

AQUI = Path(__file__).resolve().parent
DATOS = AQUI / "datos"
SALIDA: list[str] = []
RES: dict = {}

C_DEF = 0.0029 + 0.0005
C_MED = 0.0015
MES_REC_FIN = (2026, 8)       # ultimo mes de recesion evaluado (como el USREC de A)
MES_STOCK_FIN = (2026, 7)     # ultimo mes del motor (como French 202607 de A)


def p(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    SALIDA.append(s)


# ------------------------------------------------------------ calendario
def sig(m, k=1):
    y, mo = m
    t = y * 12 + (mo - 1) + k
    return (t // 12, t % 12 + 1)


def mi(m):
    return m[0] * 12 + m[1] - 1


def rango(a, b):
    out, m = [], a
    while m <= b:
        out.append(m)
        m = sig(m)
    return out


def ft(m):
    return f"{m[0]}-{m[1]:02d}"


def qsig(q, k=1):
    t = q[0] * 4 + q[1] - 1 + k
    return (t // 4, t % 4 + 1)


def qrango(a, b):
    out, q = [], a
    while q <= b:
        out.append(q)
        q = qsig(q)
    return out


def fq(q):
    return f"{q[0]}T{q[1]}"


# ------------------------------------------------------------ lector OLE2 + BIFF8 (de AC-09)
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
            return cadena(ini)[:tam]
    raise ValueError(f"flujo {nombre} no encontrado")


def rk(v: int) -> float:
    if v & 2:
        x = float(v >> 2 if v < 2**31 else (v >> 2) - (1 << 30))
    else:
        x = struct.unpack("<d", struct.pack("<Q", (v & 0xFFFFFFFC) << 32))[0]
    return x / 100 if v & 1 else x


def biff_hoja(libro: bytes, hoja: str):
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
            for k in range((ln - 6) // 6):
                celdas[(r, c0 + k)] = rk(struct.unpack_from("<I", dat, 4 + 6 * k + 2)[0])
        elif rid == 0x0006:
            r, c = struct.unpack_from("<HH", dat, 0)
            if dat[12:14] != b"\xff\xff":
                celdas[(r, c)] = struct.unpack_from("<d", dat, 6)[0]
        elif rid == 0x000A:
            break
        pos += 4 + ln
    return celdas


# ------------------------------------------------------------ normal
_erfc = np.vectorize(math.erfc)


def Phi(z):
    return 0.5 * _erfc(-np.asarray(z, float) / math.sqrt(2.0))


def phi(z):
    z = np.asarray(z, float)
    return np.exp(-0.5 * z * z) / math.sqrt(2 * math.pi)


def norm_cdf(z):
    return 0.5 * math.erfc(-z / math.sqrt(2))


def norm_ppf(q):
    lo, hi = -40.0, 40.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if norm_cdf(mid) < q:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def logPhi(z):
    """log Phi(z) estable en la cola izquierda."""
    z = np.asarray(z, float)
    out = np.empty_like(z)
    a = z > -30
    out[a] = np.log(np.maximum(Phi(z[a]), 1e-300))
    b = ~a
    zb = z[b]
    out[b] = -0.5 * zb * zb - np.log(-zb) - 0.5 * math.log(2 * math.pi)
    return out


# ------------------------------------------------------------ probit
def probit(x, y, tol=1e-10, itmax=100):
    """MV por Newton-Raphson con gradiente y hessiano analiticos. x: (n,), y: 0/1.
    Devuelve dict(b, conv, it) o None si no hay unos/ceros."""
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    if y.sum() == 0 or y.sum() == len(y):
        return None
    X = np.column_stack([np.ones_like(x), x])
    b = np.array([norm_ppf(y.mean()), 0.0])
    for it in range(1, itmax + 1):
        z = X @ b
        lp1, lp0 = logPhi(z), logPhi(-z)
        lam1 = np.exp(np.log(phi(z) + 1e-320) - lp1)      # phi/Phi
        lam0 = np.exp(np.log(phi(z) + 1e-320) - lp0)      # phi/(1-Phi)
        g_i = np.where(y == 1, lam1, -lam0)               # d logL / d z
        grad = X.T @ g_i
        # d2 logL / dz2
        h_i = np.where(y == 1, -lam1 * (z + lam1), -lam0 * (lam0 - z))
        H = (X * h_i[:, None]).T @ X
        try:
            paso = np.linalg.solve(H, grad)
        except np.linalg.LinAlgError:
            return {"b": b, "conv": False, "it": it}
        b = b - paso
        if np.max(np.abs(paso)) < tol:
            return {"b": b, "conv": True, "it": it}
    return {"b": b, "conv": False, "it": itmax}


def probit_inferencia(x, y, b, lags):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    X = np.column_stack([np.ones_like(x), x])
    z = X @ b
    lp1, lp0 = logPhi(z), logPhi(-z)
    lam1 = np.exp(np.log(phi(z) + 1e-320) - lp1)
    lam0 = np.exp(np.log(phi(z) + 1e-320) - lp0)
    g_i = np.where(y == 1, lam1, -lam0)
    h_i = np.where(y == 1, -lam1 * (z + lam1), -lam0 * (lam0 - z))
    H = (X * h_i[:, None]).T @ X
    Hi = np.linalg.inv(-H)
    se_mv = np.sqrt(np.diag(Hi))
    G = X * g_i[:, None]
    S = G.T @ G
    for l in range(1, lags + 1):
        w = 1 - l / (lags + 1)
        Gl = G[l:].T @ G[:-l]
        S += w * (Gl + Gl.T)
    V = Hi @ S @ Hi
    se_nw = np.sqrt(np.diag(V))
    return {"t_mv": b / se_mv, "t_nw": b / se_nw}


def loglik(pr, y):
    pr = np.clip(np.asarray(pr, float), 1e-12, 1 - 1e-12)
    y = np.asarray(y, float)
    return float(np.sum(y * np.log(pr) + (1 - y) * np.log(1 - pr)))


def pseudo_r2(lu, lc, n):
    return 1 - (lu / lc) ** (-(2.0 / n) * lc)


def auc(pr, y):
    pr = np.asarray(pr, float)
    y = np.asarray(y, int)
    pos, neg = pr[y == 1], pr[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    tot = 0.0
    for v in pos:
        tot += np.sum(neg < v) + 0.5 * np.sum(neg == v)
    return tot / (len(pos) * len(neg))


# ------------------------------------------------------------ datos
def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fred(nombre):
    return parsear_fred_csv((DATOS / f"fred_{nombre}.csv").read_text())


def promedio_mensual(serie, f=lambda v: v):
    acc: dict = {}
    for d, v in serie:
        acc.setdefault((d.year, d.month), []).append(f(v))
    return {m: sum(v) / len(v) for m, v in acc.items()}, {m: len(v) for m, v in acc.items()}


def bey(desc):
    d = desc / 100.0
    return 100.0 * 365 * d / (360 - 91 * d)


def cargar_tasas():
    dgs10, n10 = promedio_mensual(fred("DGS10"))
    dtb3_bey, nb = promedio_mensual(fred("DTB3"), bey)
    dtb3_desc, _ = promedio_mensual(fred("DTB3"))
    oecd = {(d.year, d.month): v for d, v in fred("IRLTLT01USM156N")}
    ultimo = (2026, 9)
    # mes completo: se exige el mes calendario terminado (2026-09 termina el 30)
    l10 = {}
    for m in rango((1953, 4), ultimo):
        if m >= (1962, 1):
            if m in dgs10:
                l10[m] = (dgs10[m], "DGS10")
        elif m in oecd:
            l10[m] = (oecd[m], "OECD")
    S, Sdesc, B10, B3 = {}, {}, {}, {}
    for m in rango((1954, 1), ultimo):
        if m in l10 and m in dtb3_bey:
            S[m] = l10[m][0] - dtb3_bey[m]
            Sdesc[m] = l10[m][0] - dtb3_desc[m]
            B10[m] = l10[m][0]
            B3[m] = dtb3_bey[m]
    faltan = [ft(m) for m in rango((1954, 1), ultimo) if m not in S]
    if faltan:
        raise SystemExit(f"faltan meses de tasas: {faltan[:5]}")
    t10y3m, _ = promedio_mensual(fred("T10Y3M"))
    return S, Sdesc, B10, B3, dtb3_desc, t10y3m, n10, nb


def cargar_nber():
    js = json.loads((DATOS / "nber_business_cycle_dates.json").read_text())
    picos, valles = [], []
    for e in js:
        if e["peak"]:
            d = date.fromisoformat(e["peak"])
            picos.append((d.year, d.month))
        if e["trough"]:
            d = date.fromisoformat(e["trough"])
            valles.append((d.year, d.month))
    t = (DATOS / "nber_expansions_contractions.html").read_text()
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    t = re.sub(r"\s+", " ", t)
    pares = re.findall(r"([A-Z][a-z]+) (\d{4}) \((\d{4})Q(\d)\)", t)
    meses = {n: i + 1 for i, n in enumerate(["January", "February", "March", "April", "May", "June", "July",
                                              "August", "September", "October", "November", "December"])}
    turn_q = {}
    for nm, y, qy, qq in pares:
        turn_q[(int(y), meses[nm])] = (int(qy), int(qq))
    # anuncios
    a = (DATOS / "nber_bcdc_announcements.html").read_text()
    a = re.sub(r"<[^>]+>", " ", a)
    a = html.unescape(a)
    a = re.sub(r"\s+", " ", a)
    anun = {}
    for m in re.finditer(r"([A-Z][a-z]+) (\d{1,2}), (\d{4}) (?:Announcement|Determination) of (?:the )?"
                         r"([A-Z][a-z]+) (\d{4}) (?:business cycle )?(peak|trough|Peak|Trough)", a):
        d = date(int(m.group(3)), meses[m.group(1)], int(m.group(2)))
        giro = (int(m.group(5)), meses[m.group(4)])
        anun[(giro, m.group(6).lower())] = d
    return picos, valles, turn_q, anun


def rec_mensual(picos, valles, hasta):
    R = {}
    for m in rango((1854, 12), hasta):
        R[m] = 0
    for pk in picos:
        vs = [v for v in valles if v > pk]
        v = vs[0] if vs else hasta
        for m in rango(sig(pk), min(v, hasta)):
            R[m] = 1
    return R


def rec_trimestral(picos, valles, turn_q, hasta_q):
    R = {q: 0 for q in qrango((1854, 4), hasta_q)}
    for pk in picos:
        vs = [v for v in valles if v > pk]
        if not vs:
            continue
        qp, qv = turn_q[pk], turn_q[vs[0]]
        for q in qrango(qsig(qp), qv):
            if q in R:
                R[q] = 1
    return R


def etiquetas_tiempo_real(picos, valles, anun, origen):
    """Etiquetas mensuales conocidas al cierre del mes `origen`. dict mes->0/1 para meses <= origen."""
    def conocido(giro, tipo):
        if giro < (1979, 1):
            return origen >= sig(giro, 12)
        d = anun.get((giro, tipo))
        if d is None:
            raise SystemExit(f"sin anuncio para {tipo} {ft(giro)}")
        return (d.year, d.month) <= origen
    R = {}
    for m in rango((1954, 1), origen):
        R[m] = 0
    for pk in picos:
        if pk < (1953, 1) or not conocido(pk, "peak"):
            continue
        vs = [v for v in valles if v > pk]
        if vs and conocido(vs[0], "trough"):
            fin = vs[0]
        else:
            fin = origen
        for m in rango(sig(pk), min(fin, origen)):
            if m in R:
                R[m] = 1
    return R


def cargar_acciones():
    def fin_mes(nombre):
        ser = parsear_yahoo_json((DATOS / nombre).read_text())["serie"]
        out = {}
        for d, v in ser:
            out[(d.year, d.month)] = (d, v)
        return out
    g = fin_mes("yahoo_GSPC_1d.json")
    tr = fin_mes("yahoo_SP500TR_1d_30y.json")
    celdas = biff_hoja(ole_flujo((DATOS / "shiller_ie_data.xls").read_bytes(), "Workbook"), "Data")
    D = {}
    for r in sorted({r for r, _ in celdas}):
        a = celdas.get((r, 0))
        if a is None or not (1870 < a < 2100):
            continue
        y = int(a)
        mo = int(round((a - y) * 100))
        if 1 <= mo <= 12 and (r, 2) in celdas and celdas[(r, 2)] > 0:
            D[(y, mo)] = celdas[(r, 2)]
    r = {}
    for m in rango((1928, 1), (2026, 9)):
        pm = sig(m, -1)
        if m <= (1996, 10):
            r[m] = g[m][1] / g[pm][1] - 1 + (D[m] / 12) / g[pm][1]
        else:
            r[m] = tr[m][1] / tr[pm][1] - 1
    return r


# ------------------------------------------------------------ motor
def correr(w: dict, r: dict, rf: dict, meses, c):
    W_pre, out, ntr = 0.0, {}, 0
    for m in meses:
        W = w[m]
        giro = abs(W - W_pre)
        if giro > 1e-12:
            ntr += 1
        rb = W * r[m] + (1 - W) * rf[m]
        out[m] = (1 - giro * c) * (1 + rb) - 1
        W_pre = W * (1 + r[m]) / (1 + rb) if (1 + rb) != 0 else W
    return out, ntr


def metricas(serie: dict, rf: dict, a, b, w=None):
    ms = [m for m in rango(a, b)]
    x = np.array([serie[m] for m in ms])
    ex = np.array([serie[m] - rf[m] for m in ms])
    n = len(x)
    niv = np.concatenate([[1.0], np.cumprod(1 + x)])
    cagr = niv[-1] ** (12 / n) - 1
    vol = x.std(ddof=1) * math.sqrt(12)
    sh = ex.mean() / ex.std(ddof=1) * math.sqrt(12)
    mdd = float(np.min(niv / np.maximum.accumulate(niv) - 1))
    out = {"cagr": cagr, "vol": vol, "sharpe": sh, "mdd": mdd, "n": n,
           "sr_m": ex.mean() / ex.std(ddof=1),
           "skew": float(np.mean((ex - ex.mean()) ** 3) / ex.std() ** 3),
           "kurt": float(np.mean((ex - ex.mean()) ** 4) / ex.std() ** 4)}
    if w is not None:
        out["trades"] = sum(1 for m in ms if abs(w[m] - w[sig(m, -1)]) > 1e-12)
        out["exp"] = float(np.mean([w[m] for m in ms]))
    return out


def dsr(sr, T, skew, kurt, sr_ens, N):
    V = float(np.var(sr_ens, ddof=1))
    g = 0.5772156649
    sr0 = math.sqrt(V) * ((1 - g) * norm_ppf(1 - 1 / N) + g * norm_ppf(1 - 1 / (N * math.e)))
    den = math.sqrt(max(1 - skew * sr + (kurt - 1) / 4 * sr * sr, 1e-12))
    return norm_cdf((sr - sr0) * math.sqrt(T - 1) / den)


# ------------------------------------------------------------ principal
def main():
    p("AC-11: doble ejecucion independiente de R07 (curva 10a-3m y recesion). Fase 0, no es recomendacion.")
    p("Archivos de datos (sha256):")
    sums = []
    for f in sorted(DATOS.iterdir()):
        if f.name == "SHA256SUMS.txt":
            continue
        h = sha(f)
        sums.append(f"{h}  {f.name}")
        p(f"  {h[:12]}...  {f.name}")
    (DATOS / "SHA256SUMS.txt").write_text("\n".join(sums) + "\n")
    RES["sha256"] = {s.split("  ")[1]: s.split("  ")[0] for s in sums}

    S, Sdesc, B10, B3, T3desc, t10y3m, n10, nb = cargar_tasas()
    picos, valles, turn_q, anun = cargar_nber()
    p(f"\n[datos] Spread mensual B (10a: OECD 1953-04..1961-12, DGS10 promedio diario desde 1962-01; "
      f"3m: DTB3 -> BEY diario y promedio): {ft(min(S))} a {ft(max(S))}, n={len(S)}")
    p(f"  anuncios NBER leidos: {len(anun)}; ultimo pico NBER: {ft(picos[-1])}; ultimo valle: {ft(valles[-1])}")
    post = [pk for pk in picos if pk > (2020, 2)]
    p(f"  picos NBER posteriores a 2020-02: {len(post)}")
    # control contra T10Y3M
    dif = [S[m] - t10y3m[m] for m in rango((1982, 2), (2026, 9))]
    p(f"  control: S_B - promedio mensual T10Y3M, 1982-02..2026-09: media {np.mean(dif):+.4f} pp, "
      f"|max| {np.max(np.abs(dif)):.4f} pp")
    RES["control_t10y3m"] = {"media": float(np.mean(dif)), "absmax": float(np.max(np.abs(dif)))}

    Rm = rec_mensual(picos, valles, MES_REC_FIN)
    Rq = rec_trimestral(picos, valles, turn_q, (2026, 2))
    # control: trimestral desde mensual (algun mes en recesion en el trimestre)
    dif_q = []
    for q in qrango((1959, 1), (1995, 1)):
        ms = [(q[0], 3 * (q[1] - 1) + i) for i in (1, 2, 3)]
        alt = 1 if sum(Rm[m] for m in ms) >= 2 else 0
        if alt != Rq[q]:
            dif_q.append(fq(q))
    p(f"  trimestres 1959T1-1995T1 donde la tabla trimestral NBER difiere de 'mayoria de meses': {dif_q}")

    # ---------------------------------------------------------- trimestral
    Sq, Sqd = {}, {}
    for q in qrango((1954, 1), (2026, 3)):
        ms = [(q[0], 3 * (q[1] - 1) + i) for i in (1, 2, 3)]
        if all(m in S for m in ms):
            Sq[q] = np.mean([B10[m] for m in ms]) - np.mean([B3[m] for m in ms])
            Sqd[q] = np.mean([B10[m] for m in ms]) - np.mean([T3desc[m] for m in ms])

    def ajuste_trimestral(k, q0, q1, spread=Sq, lags=None, por_objetivo=False):
        if por_objetivo:
            orgs = [qsig(t, -k) for t in qrango(q0, q1)]
        else:
            orgs = qrango(q0, qsig(q1, -k))
        x = np.array([spread[q] for q in orgs])
        y = np.array([Rq[qsig(q, k)] for q in orgs])
        f = probit(x, y)
        inf = probit_inferencia(x, y, f["b"], (k - 1) if lags is None else lags)
        pr = Phi(f["b"][0] + f["b"][1] * x)
        lu = loglik(pr, y)
        lc = loglik(np.full(len(y), y.mean()), y)
        return {"k": k, "n": len(y), "a": float(f["b"][0]), "b": float(f["b"][1]),
                "t_mv": float(inf["t_mv"][1]), "t_nw": float(inf["t_nw"][1]),
                "r2": float(pseudo_r2(lu, lc, len(y))), "conv": f["conv"]}

    p("\n[A1/H1] Probit trimestral dentro de muestra, origenes 1959T1..1995T1-k (articulo: R2 k=4 0.296, t -4.57)")
    p("   k     n   alfa     beta    t MV   t NW(k-1)  pseudoR2 | articulo R2   t")
    art_r2 = [0.071, 0.211, 0.271, 0.296, 0.256, 0.149, 0.078, 0.031]
    art_t = [-2.71, -4.21, -4.71, -4.57, -3.87, -4.13, -3.02, -1.63]
    A1 = []
    for k in range(1, 9):
        o = ajuste_trimestral(k, (1959, 1), (1995, 1))
        A1.append(o)
        p(f"  {k:2d} {o['n']:5d} {o['a']:7.4f} {o['b']:8.4f} {o['t_mv']:7.2f} {o['t_nw']:8.2f}   {o['r2']:7.3f}  |"
          f"   {art_r2[k-1]:.3f}  {art_t[k-1]:6.2f}")
    RES["A1"] = A1
    o4 = A1[3]
    s50 = -o4["a"] / o4["b"]
    p(f"  k=4: spread con P=50% = {s50:.3f} pp (Current Issues: -0.82 +- 0.25); P(2.74)={norm_cdf(o4['a']+o4['b']*2.74):.4f}; "
      f"P(-2.18)={norm_cdf(o4['a']+o4['b']*-2.18):.4f}")
    RES["A1_s50"] = s50
    k_max = max(A1, key=lambda d: d["r2"])["k"]
    h1 = ("Replicado" if (o4["b"] < 0 and abs(o4["t_nw"]) >= 2 and 0.246 <= o4["r2"] <= 0.346) else
          "Replicado con diferencias" if (o4["b"] < 0 and abs(o4["t_nw"]) >= 2) else "No replicado")
    p(f"  H1: {h1}; k con R2 maximo = {k_max}; R2 k=1 {A1[0]['r2']:.3f}, k=8 {A1[7]['r2']:.3f} (<0.10?)")
    RES["H1"] = h1
    p("  Sensibilidades k=4: ")
    for nom, kw in [("t NW con k rezagos", dict(lags=4)),
                    ("objetivos 1959T1..1995T1", dict(por_objetivo=True)),
                    ("spread base descuento", dict(spread=Sqd)),
                    ("solo fuentes diarias, origenes 1962T1..", dict()),
                    ]:
        q0 = (1962, 1) if nom.startswith("solo") else (1959, 1)
        o = ajuste_trimestral(4, q0, (1995, 1), **kw)
        p(f"    {nom:40s} n={o['n']} beta {o['b']:.4f} t NW {o['t_nw']:.2f} R2 {o['r2']:.3f}")
        RES.setdefault("A1_sens", {})[nom] = o

    # ---------------------------------------------------------- A2 fuera de muestra trimestral
    p("\n[A2/H2] Fuera de muestra trimestral, objetivos 1971T1..1995T1, estimacion s>=1959T1, s+k<=q, cronologia final")
    p("   k    n   R2 fuera (Lc ventana)  R2 (Lc recursiva)  Brier  Brier clim | articulo")
    art_oos = [0.072, 0.236, 0.328, 0.295, 0.155, 0.141, None, None]
    A2 = []
    for k in range(1, 9):
        prs, ys, clim, fallos = [], [], [], 0
        for tau in qrango((1971, 1), (1995, 1)):
            q = qsig(tau, -k)
            est = [s for s in qrango((1959, 1), q) if qsig(s, k) <= q]
            x = np.array([Sq[s] for s in est])
            y = np.array([Rq[qsig(s, k)] for s in est])
            f = probit(x, y)
            if f is None or not f["conv"]:
                fallos += 1
                pr = y.mean()
            else:
                pr = float(Phi(f["b"][0] + f["b"][1] * Sq[q]))
            prs.append(pr)
            ys.append(Rq[tau])
            clim.append(y.mean())
        ys = np.array(ys)
        lu = loglik(prs, ys)
        lc = loglik(np.full(len(ys), ys.mean()), ys)
        lcr = loglik(clim, ys)
        r2 = pseudo_r2(lu, lc, len(ys))
        r2r = 1 - (lu / lcr) ** (-(2.0 / len(ys)) * lcr)
        brier = float(np.mean((np.array(prs) - ys) ** 2))
        bc = float(np.mean((np.array(clim) - ys) ** 2))
        A2.append({"k": k, "n": len(ys), "r2": float(r2), "r2_rec": float(r2r), "brier": brier,
                   "brier_clim": bc, "fallos": fallos})
        a = f"{art_oos[k-1]:.3f}" if art_oos[k-1] is not None else "negativo"
        p(f"  {k:2d} {len(ys):4d}   {r2:8.3f}             {r2r:8.3f}        {brier:.4f} {bc:.4f}  | {a}  fallos={fallos}")
    RES["A2"] = A2
    r2o = A2[3]["r2"]
    h2 = "Replicado" if 0.245 <= r2o <= 0.345 else ("Replicado con diferencias" if r2o > 0 else "No replicado")
    p(f"  H2: {h2} (k=4 R2 fuera {r2o:.3f})")
    RES["H2"] = h2

    # ---------------------------------------------------------- A3 mensual
    H = 12

    def ajuste_mensual(o0, o1, lags=11, spread=S):
        orgs = rango(o0, o1)
        x = np.array([spread[m] for m in orgs])
        y = np.array([Rm[sig(m, H)] for m in orgs])
        f = probit(x, y)
        inf = probit_inferencia(x, y, f["b"], lags)
        pr = Phi(f["b"][0] + f["b"][1] * x)
        lu = loglik(pr, y)
        lc = loglik(np.full(len(y), y.mean()), y)
        return {"n": len(y), "a": float(f["b"][0]), "b": float(f["b"][1]), "t_mv": float(inf["t_mv"][1]),
                "t_nw": float(inf["t_nw"][1]), "r2": float(pseudo_r2(lu, lc, len(y))),
                "auc": float(auc(pr, y))}

    p("\n[A3] Probit mensual, 12 meses adelante, dentro de muestra")
    for nom, (a, b) in [("1959-01..1994-03", ((1959, 1), (1994, 3))),
                        ("1959-01..2025-08 (completa)", ((1959, 1), (2025, 8)))]:
        o = ajuste_mensual(a, b)
        o12 = ajuste_mensual(a, b, lags=12)
        RES.setdefault("A3_in", {})[nom] = o
        p(f"  {nom:28s} n={o['n']} alfa {o['a']:.4f} beta {o['b']:.4f} t MV {o['t_mv']:.2f} t NW11 {o['t_nw']:.2f} "
          f"(NW12 {o12['t_nw']:.2f}) R2 {o['r2']:.3f} AUC {o['auc']:.3f}; P=50% en {-o['a']/o['b']:.3f} pp")
    fijo = RES["A3_in"]["1959-01..1994-03"]

    cache_rt: dict = {}

    def etq_rt(origen):
        if origen not in cache_rt:
            cache_rt[origen] = etiquetas_tiempo_real(picos, valles, anun, origen)
        return cache_rt[origen]

    def prob_origen(m, tiempo_real, spread=S):
        """Probabilidad de recesion en m+12 con info al cierre de m. Devuelve (p, clim, fallo, coef)."""
        est = rango((1959, 1), sig(m, -H))
        if tiempo_real:
            E = etq_rt(m)
            y = np.array([E[sig(s, H)] for s in est])
        else:
            y = np.array([Rm[sig(s, H)] for s in est])
        x = np.array([spread[s] for s in est])
        f = probit(x, y)
        if f is None or not f["conv"]:
            return float(y.mean()), float(y.mean()), True, None
        return float(Phi(f["b"][0] + f["b"][1] * spread[m])), float(y.mean()), False, f["b"]

    def evaluar(o0, o1, tiempo_real, coef_fijos=None):
        prs, ys, cl, fallos = [], [], [], 0
        for m in rango(o0, o1):
            if coef_fijos is not None:
                pr = float(Phi(coef_fijos[0] + coef_fijos[1] * S[m]))
                _, c, _, _ = prob_origen(m, tiempo_real)
            else:
                pr, c, fl, _ = prob_origen(m, tiempo_real)
                fallos += fl
            prs.append(pr)
            cl.append(c)
            ys.append(Rm[sig(m, H)])
        prs, ys, cl = np.array(prs), np.array(ys), np.array(cl)
        n = len(ys)
        lu = loglik(prs, ys)
        lc = loglik(np.full(n, ys.mean()), ys)
        lcr = loglik(cl, ys)
        out = {"n": n, "unos": int(ys.sum()), "r2": float(pseudo_r2(lu, lc, n)),
               "r2_rec": float(1 - (lu / lcr) ** (-(2.0 / n) * lcr)),
               "brier": float(np.mean((prs - ys) ** 2)), "brier_clim": float(np.mean((cl - ys) ** 2)),
               "auc": float(auc(prs, ys)), "fallos": fallos,
               "acierto30": float(np.mean((prs > 0.3) == (ys == 1))),
               "acierto50": float(np.mean((prs > 0.5) == (ys == 1))),
               "senales50": int(np.sum(prs > 0.5)), "senales30": int(np.sum(prs > 0.3)),
               "p_max": float(prs.max())}
        return out

    p("\n[A3] Fuera de muestra mensual recursivo (estimacion s>=1959-01, s+12<=m; evaluacion con cronologia final)")
    p("  tramo / etiquetas                       n  unos  R2(Lc ven)  R2(Lc rec)  Brier   B.clim   AUC   ac.30 ac.50 n>0.5 fallos")
    A3 = {}
    for nom, a, b, rt, cf in [
        ("1970-01..1998-02 final", (1970, 1), (1998, 2), False, None),
        ("1970-01..1998-02 tiempo real", (1970, 1), (1998, 2), True, None),
        ("1998-03..2025-08 final", (1998, 3), (2025, 8), False, None),
        ("1998-03..2025-08 tiempo real (H3)", (1998, 3), (2025, 8), True, None),
        ("1998-03..2024-02 tiempo real (sens.)", (1998, 3), (2024, 2), True, None),
        ("1998-03..2025-08 coef fijos 59-94", (1998, 3), (2025, 8), True, (fijo["a"], fijo["b"])),
    ]:
        o = evaluar(a, b, rt, cf)
        A3[nom] = o
        p(f"  {nom:36s} {o['n']:4d} {o['unos']:4d}   {o['r2']:8.3f}   {o['r2_rec']:8.3f}   {o['brier']:.4f}  "
          f"{o['brier_clim']:.4f}  {o['auc']:.3f}  {o['acierto30']:.3f} {o['acierto50']:.3f} {o['senales50']:4d} {o['fallos']}")
    RES["A3"] = A3
    h3o = A3["1998-03..2025-08 tiempo real (H3)"]
    if h3o["r2"] > 0 and h3o["brier"] < h3o["brier_clim"]:
        h3 = "sigue prediciendo"
    elif h3o["r2"] <= 0 and h3o["brier"] >= h3o["brier_clim"]:
        h3 = "refutada"
    else:
        h3 = "mixto"
    p(f"  H3: {h3} (R2 {h3o['r2']:.3f}, Brier {h3o['brier']:.4f} contra clim {h3o['brier_clim']:.4f}, AUC {h3o['auc']:.3f})")
    RES["H3"] = h3

    # ---------------------------------------------------------- A4 episodio 2022-2024
    p("\n[A4/H4] Episodio 2022-2024")
    inv = [m for m in rango((2022, 1), (2025, 8)) if S[m] < 0]
    inv_t = [m for m in rango((2022, 1), (2025, 8)) if t10y3m[m] < 0]
    p(f"  meses con S_B<0: {len(inv)} ({ft(inv[0])}..{ft(inv[-1])}); con T10Y3M mensual<0: {len(inv_t)} "
      f"({ft(inv_t[0])}..{ft(inv_t[-1])}); min S_B {min(S[m] for m in inv):.3f} en "
      f"{ft(min(inv, key=lambda m: S[m]))}")
    dd = parsear_fred_csv((DATOS / "fred_T10Y3M.csv").read_text())
    best, cur = (0, None, None), (0, None)
    for d, v in dd:
        if v < 0:
            cur = (cur[0] + 1, cur[1] or d)
            if cur[0] > best[0]:
                best = (cur[0], cur[1], d)
        else:
            cur = (0, None)
    seg = [(d, v) for d, v in dd if best[1] <= d <= best[2]]
    mn = min(seg, key=lambda t: t[1])
    p(f"  racha mas larga de sesiones T10Y3M<0: {best[0]} ({best[1]} a {best[2]}), minimo {mn[1]:.2f} el {mn[0]}")
    ventana = rango(sig(inv[0]), min(sig(inv[-1], 12), MES_REC_FIN))
    rec_v = sum(Rm[m] for m in ventana)
    p(f"  meses en recesion (calendario NBER) de {ft(ventana[0])} a {ft(ventana[-1])}: {rec_v}; "
      f"picos NBER posteriores a 2020-02: {len(post)} -> {'falso positivo' if rec_v == 0 and not post else 'no'}")
    rt = [(m, prob_origen(m, True)[0]) for m in rango((2022, 1), (2025, 8))]
    altos = [m for m, v in rt if v > 0.5]
    mx = max(rt, key=lambda t: t[1])
    p(f"  probit en tiempo real 2022-01..2025-08: meses con P>0.5: {len(altos)}"
      f"{' (' + ft(altos[0]) + '..' + ft(altos[-1]) + ')' if altos else ''}; max {mx[1]:.3f} en {ft(mx[0])}")
    RES["A4"] = {"meses_inv": len(inv), "primero": ft(inv[0]), "ultimo": ft(inv[-1]), "meses_inv_t10y3m": len(inv_t),
                 "racha": best[0], "racha_ini": str(best[1]), "racha_fin": str(best[2]), "min_diario": mn[1],
                 "min_fecha": str(mn[0]), "rec_ventana": rec_v, "meses_p50": len(altos), "p_max": mx[1],
                 "p_max_mes": ft(mx[0])}
    # probabilidad actual
    full = probit(np.array([S[m] for m in rango((1959, 1), (2025, 8))]),
                  np.array([Rm[sig(m, H)] for m in rango((1959, 1), (2025, 8))]))["b"]
    for ult in [(2026, 8), (2026, 9)]:
        p_full = norm_cdf(full[0] + full[1] * S[ult])
        p_rt = prob_origen(ult, True)[0] if ult <= (2026, 8) else None
        p(f"  probabilidad actual con S_B de {ft(ult)} = {S[ult]:.3f} pp: modelo completo (origenes 1959-01..2025-08) "
          f"{p_full:.4f}" + (f"; tiempo real en el origen {p_rt:.4f}" if p_rt is not None else ""))
        RES.setdefault("prob_actual", {})[ft(ult)] = {"S": S[ult], "p_full": p_full, "p_rt": p_rt}
    p_ci = norm_cdf(-0.6651 - 0.8111 * dd[-1][1])
    p_ful_d = norm_cdf(full[0] + full[1] * dd[-1][1])
    p(f"  ultimo diario T10Y3M {dd[-1][0]} = {dd[-1][1]:.2f}: modelo completo {p_ful_d:.4f}; coef. implicitos de Current Issues {p_ci:.4f}")
    RES["prob_actual"]["diario"] = {"fecha": str(dd[-1][0]), "S": dd[-1][1], "p_full": p_ful_d, "p_CI": p_ci}

    # ---------------------------------------------------------- A5
    p("\n[A5/H5] Mercado de EUA (S&P 500 TR: ^GSPC + D/12 Shiller hasta 1996-10, ^SP500TR despues) tras el inicio de inversiones")
    r = cargar_acciones()
    rf = {}
    for m in rango((1954, 1), (2026, 9)):
        rf[m] = T3desc[m] / 1200
    inicios = []
    for m in rango((1955, 1), (2026, 8)):
        if S[m] < 0 and all(S[sig(m, -j)] >= 0 for j in range(1, 13)):
            inicios.append(m)
    p(f"  inicios: {[ft(m) for m in inicios]}")

    def comp(m, n, ex=False):
        ms = rango(sig(m), sig(m, n))
        v = np.prod([1 + r[x] for x in ms]) - 1
        if ex:
            v -= np.prod([1 + rf[x] for x in ms]) - 1
        return v

    ultimo_r = (2026, 8)
    filas = []
    for m in inicios:
        d = {"inicio": ft(m)}
        for n in (6, 12, 18, 24):
            d[f"r{n}"] = comp(m, n) if sig(m, n) <= ultimo_r else None
        d["ex12"] = comp(m, 12, True) if sig(m, 12) <= ultimo_r else None
        ms = [x for x in rango(sig(m), sig(m, 24)) if x <= ultimo_r]
        niv = np.concatenate([[1.0], np.cumprod([1 + r[x] for x in ms])])
        d["mdd24"] = float(np.min(niv / np.maximum.accumulate(niv) - 1))
        d["mes_max24"] = int(np.argmax(niv))
        pk = [x for x in picos if x > m]
        d["meses_a_pico"] = mi(pk[0]) - mi(m) if pk else None
        filas.append(d)
        f = lambda v: f"{100*v:7.2f}%" if v is not None else "   n.d. "
        p(f"  {d['inicio']}: 6m {f(d['r6'])} 12m {f(d['r12'])} 18m {f(d['r18'])} 24m {f(d['r24'])} "
          f"ex12 {f(d['ex12'])} MDD24 {100*d['mdd24']:.1f}% mes max {d['mes_max24']} meses a pico NBER {d['meses_a_pico']}")
    unc = [comp(m, 12) for m in rango((1954, 1), sig(ultimo_r, -12))]
    ev = [d["r12"] for d in filas if d["r12"] is not None]
    t5 = (np.mean(ev) - np.mean(unc)) / (np.std(unc, ddof=1) / math.sqrt(len(ev)))
    p(f"  media 12m eventos {100*np.mean(ev):.2f}% (n={len(ev)}) contra incondicional {100*np.mean(unc):.2f}% "
      f"(n={len(unc)}, sd {100*np.std(unc, ddof=1):.2f}%): t aprox {t5:.2f} -> "
      f"{'H5 expectativa refutada' if t5 <= -2 else 'H5 se sostiene (no es menor)'}")
    RES["A5"] = {"eventos": filas, "media12": float(np.mean(ev)), "incond12": float(np.mean(unc)), "t": float(t5)}

    # ---------------------------------------------------------- B motor H6
    p("\n[B/H6] Motor mensual: S&P 500 TR contra efectivo (DTB3/1200). Decisiones 1971-01..2026-07; "
      "dentro 1971-01..1998-02, fuera 1998-03..2026-07")
    meses = rango((1971, 1), MES_STOCK_FIN)
    Pm = {}
    for m in rango((1969, 12), sig(MES_STOCK_FIN, -1)):
        Pm[m] = prob_origen(m, True)[0]
    Iv, lvl = {}, 1.0
    for m in rango((1928, 1), MES_STOCK_FIN):
        lvl *= 1 + r[m]
        Iv[m] = lvl

    def reglas(Sx, Pmx=None):
        Pu = Pm if Pmx is None else Pmx
        W = {}
        for t in [sig(meses[0], -1)] + meses:
            s1 = Sx[sig(t, -1)]
            neg3 = all(Sx[sig(t, -j)] < 0 for j in (1, 2, 3))
            pp = Pu.get(sig(t, -1))
            ultimos = [Sx[sig(t, -j)] for j in range(1, 13)]
            des = any(Sx[sig(t, -j)] >= 0 and all(Sx[sig(t, -j - i)] < 0 for i in (1, 2, 3)) for j in range(1, 13))
            W.setdefault("inv1", {})[t] = 0.0 if s1 < 0 else 1.0
            W.setdefault("inv3", {})[t] = 0.0 if neg3 else 1.0
            W.setdefault("inv3_medio", {})[t] = 0.5 if neg3 else 1.0
            if pp is not None:
                W.setdefault("probit50", {})[t] = 0.0 if pp > 0.5 else 1.0
                W.setdefault("probit30", {})[t] = 0.0 if pp > 0.3 else 1.0
                W.setdefault("probit_cont", {})[t] = 1.0 - pp
            W.setdefault("inv_fuera12", {})[t] = 0.0 if min(ultimos) < 0 else 1.0
            W.setdefault("desinv12", {})[t] = 0.0 if des else 1.0
        return W

    W = reglas(S)
    t0 = sig(meses[0], -1)
    W["comprar_mantener"] = {t: 1.0 for t in [t0] + meses}
    W["efectivo"] = {t: 0.0 for t in [t0] + meses}
    W["sma10"] = {t: (1.0 if Iv[sig(t, -1)] > np.mean([Iv[sig(t, -j)] for j in range(1, 11)]) else 0.0)
                  for t in [t0] + meses}
    PRUEBA = ["inv1", "inv3", "inv3_medio", "probit50", "probit30", "probit_cont", "inv_fuera12", "desinv12"]
    SEG = {"dentro": ((1971, 1), (1998, 2)), "fuera": ((1998, 3), MES_STOCK_FIN)}
    tabla = {}
    for costo_nom, c in [("def", C_DEF), ("medio", C_MED), ("bruto", 0.0)]:
        for v in PRUEBA + ["comprar_mantener", "efectivo", "sma10"]:
            ser, _ = correr(W[v], r, rf, meses, c)
            for sg, (a, b) in SEG.items():
                tabla[(costo_nom, v, sg)] = metricas(ser, rf, a, b, W[v])
    p("  costo 0.34%/lado          | dentro: CAGR    vol   Sharpe   MDD   oper | fuera: CAGR    vol   Sharpe   MDD   oper  exp")
    for v in PRUEBA + ["comprar_mantener", "efectivo", "sma10"]:
        a_, b_ = tabla[("def", v, "dentro")], tabla[("def", v, "fuera")]
        p(f"  {v:24s} | {100*a_['cagr']:6.2f}% {100*a_['vol']:5.1f}% {a_['sharpe']:6.3f} {100*a_['mdd']:6.1f}% {a_['trades']:4d} |"
          f" {100*b_['cagr']:6.2f}% {100*b_['vol']:5.1f}% {b_['sharpe']:6.3f} {100*b_['mdd']:6.1f}% {b_['trades']:4d} {b_['exp']:.2f}")
    elegido = max(PRUEBA, key=lambda v: tabla[("def", v, "dentro")]["sharpe"])
    e, bh, sm = tabla[("def", elegido, "fuera")], tabla[("def", "comprar_mantener", "fuera")], tabla[("def", "sma10", "fuera")]
    ei, bhi = tabla[("def", elegido, "dentro")], tabla[("def", "comprar_mantener", "dentro")]
    p(f"  elegida por Sharpe dentro: {elegido} ({ei['sharpe']:.3f})")
    agrega_bh = e["sharpe"] > bh["sharpe"] and abs(e["mdd"]) < abs(bh["mdd"])
    agrega_sma = agrega_bh and e["sharpe"] > sm["sharpe"] and abs(e["mdd"]) < abs(sm["mdd"])
    sr_ens = [tabla[("def", v, "fuera")]["sr_m"] for v in PRUEBA]
    d8 = dsr(e["sr_m"], e["n"], e["skew"], e["kurt"], sr_ens, 8)
    d16 = dsr(e["sr_m"], e["n"], e["skew"], e["kurt"], sr_ens, 16)
    h6 = "refutada (Sharpe fuera <= comprar y mantener)" if e["sharpe"] <= bh["sharpe"] else "no refutada"
    freno = "refutado" if not (abs(e["mdd"]) < abs(bh["mdd"]) and abs(ei["mdd"]) < abs(bhi["mdd"])) else "no refutado"
    p(f"  fuera: {elegido} Sharpe {e['sharpe']:.3f} MDD {100*e['mdd']:.1f}% | comprar y mantener {bh['sharpe']:.3f} "
      f"{100*bh['mdd']:.1f}% | SMA10 {sm['sharpe']:.3f} {100*sm['mdd']:.1f}%")
    p(f"  agrega valor frente a comprar y mantener: {agrega_bh}; frente a SMA10: {agrega_sma}; DSR N=8 {d8:.3f}, N=16 {d16:.3f}")
    p(f"  H6: {h6}; uso como freno: {freno}")
    mejor_fuera = max(PRUEBA, key=lambda v: tabla[("def", v, "fuera")]["sharpe"])
    p(f"  (informativo) mejor variante fuera: {mejor_fuera} {tabla[('def', mejor_fuera, 'fuera')]['sharpe']:.3f}")
    p("  Sharpe fuera por costo (def / medio / bruto):")
    for v in PRUEBA + ["comprar_mantener", "sma10"]:
        p(f"    {v:20s} {tabla[('def', v, 'fuera')]['sharpe']:.3f} / {tabla[('medio', v, 'fuera')]['sharpe']:.3f} / "
          f"{tabla[('bruto', v, 'fuera')]['sharpe']:.3f}")
    # spread en base descuento
    Wd = reglas(Sdesc)
    for v in ("inv1", "inv3", "inv3_medio"):
        ser, _ = correr(Wd[v], r, rf, meses, C_DEF)
        mm = metricas(ser, rf, *SEG["fuera"], Wd[v])
        md = metricas(ser, rf, *SEG["dentro"], Wd[v])
        p(f"  sens. spread descuento {v:12s} Sharpe dentro {md['sharpe']:.3f} fuera {mm['sharpe']:.3f} MDD fuera {100*mm['mdd']:.1f}%")
    # MXN
    fx = {}
    for d, v in parsear_fred_csv((DATOS / "fred_DEXMXUS.csv").read_text()):
        fx[(d.year, d.month)] = v
    m0 = min(m for m in fx if m >= (1994, 1) and sig(m, -1) in fx)
    p(f"  MXN (DEXMXUS ultimo dato del mes), {ft(m0)}..{ft(MES_STOCK_FIN)}:")
    for v in (elegido, "comprar_mantener", "sma10"):
        ser, _ = correr(W[v], r, rf, meses, C_DEF)
        x = [(1 + ser[m]) * fx[m] / fx[sig(m, -1)] - 1 for m in rango(m0, MES_STOCK_FIN)]
        niv = np.concatenate([[1.0], np.cumprod(1 + np.array(x))])
        p(f"    {v:18s} CAGR {100*(niv[-1]**(12/len(x))-1):.2f}% MDD {100*np.min(niv/np.maximum.accumulate(niv)-1):.1f}%")
    RES["H6"] = {"elegida": elegido, "tabla": {f"{k[0]}|{k[1]}|{k[2]}": v for k, v in tabla.items()},
                 "agrega_bh": agrega_bh, "agrega_sma": agrega_sma, "dsr8": d8, "dsr16": d16, "veredicto": h6,
                 "freno": freno}

    # ---------------------------------------------------------- CONCILIACION (agregada despues de leer A)
    p("\n[CONCILIACION] Agregada despues de fijar las cifras ciegas y leer R07 secciones 10-17. "
      "Control C: FRED GS10/TB3MS (spread de A) y French 202607 (rendimientos de A).")
    gs10 = {(d.year, d.month): v for d, v in parsear_fred_csv((DATOS / "control_fred_GS10.csv").read_text())}
    tb3 = {(d.year, d.month): v for d, v in parsear_fred_csv((DATOS / "control_fred_TB3MS.csv").read_text())}
    SA = {m: gs10[m] - bey(tb3[m]) for m in rango((1954, 1), (2026, 8)) if m in gs10 and m in tb3}
    dA = [S[m] - SA[m] for m in rango((1954, 1), (2026, 8))]
    signo = [ft(m) for m in rango((1954, 1), (2026, 8)) if (S[m] < 0) != (SA[m] < 0)]
    p(f"  S_B - S_A 1954-01..2026-08: media {np.mean(dA):+.4f} pp, |max| {np.max(np.abs(dA)):.4f} pp; "
      f"1962-01..2026-08 |max| {max(abs(S[m]-SA[m]) for m in rango((1962, 1), (2026, 8))):.4f} pp")
    p(f"  meses con signo distinto (S<0): {signo}")
    import zipfile
    with zipfile.ZipFile(DATOS / "control_french_F-F_Research_Data_Factors_CSV_202607.zip") as z:
        txt = z.read(z.namelist()[0]).decode("latin-1")
    rF, rfF = {}, {}
    for ln in txt.splitlines():
        c = [x.strip() for x in ln.split(",")]
        if len(c) == 5 and len(c[0]) == 6 and c[0].isdigit():
            m = (int(c[0][:4]), int(c[0][4:]))
            if m in rF:
                break
            rF[m] = (float(c[1]) + float(c[4])) / 100
            rfF[m] = float(c[4]) / 100
    PmA = {m: prob_origen(m, True, spread=SA)[0] for m in rango((1969, 12), sig(MES_STOCK_FIN, -1))}
    dif_p50 = [ft(m) for m in PmA if (PmA[m] > 0.5) != (Pm[m] > 0.5)]
    p(f"  meses con P>0.5 distinto (S_B contra S_A, tiempo real): {dif_p50}")

    def corrida(Sx, Pmx, rx, rfx):
        Wx = reglas(Sx, Pmx)
        Ivx, lv = {}, 1.0
        for m in rango((1928, 1), MES_STOCK_FIN):
            lv *= 1 + rx[m]
            Ivx[m] = lv
        Wx["comprar_mantener"] = {t: 1.0 for t in [t0] + meses}
        Wx["sma10"] = {t: (1.0 if Ivx[sig(t, -1)] > np.mean([Ivx[sig(t, -j)] for j in range(1, 11)]) else 0.0)
                       for t in [t0] + meses}
        out = {}
        for v in PRUEBA + ["comprar_mantener", "sma10"]:
            ser, _ = correr(Wx[v], rx, rfx, meses, C_DEF)
            out[v] = {sg: metricas(ser, rfx, a, b, Wx[v]) for sg, (a, b) in SEG.items()}
        return out, Wx

    combos = [("B: S_B + S&P TR + DTB3", S, Pm, r, rf), ("S_B + French", S, Pm, rF, rfF),
              ("S_A + S&P TR + DTB3", SA, PmA, r, rf), ("C: S_A + French (= A)", SA, PmA, rF, rfF)]
    RES["conciliacion"] = {}
    for nom, Sx, Pmx, rx, rfx in combos:
        o, Wx = corrida(Sx, Pmx, rx, rfx)
        el = max(PRUEBA, key=lambda v: o[v]["dentro"]["sharpe"])
        p(f"  {nom}: elegida {el}")
        for v in PRUEBA + ["comprar_mantener", "sma10"]:
            a_, b_ = o[v]["dentro"], o[v]["fuera"]
            p(f"    {v:18s} dentro {a_['sharpe']:.4f} {100*a_['mdd']:6.2f}% CAGR {100*a_['cagr']:5.2f}% | "
              f"fuera {b_['sharpe']:.4f} {100*b_['mdd']:6.2f}% CAGR {100*b_['cagr']:5.2f}%")
        RES["conciliacion"][nom] = {v: {"dentro": o[v]["dentro"]["sharpe"], "fuera": o[v]["fuera"]["sharpe"],
                                        "mdd_fuera": o[v]["fuera"]["mdd"]} for v in o}
    # H5 con French y con S_A
    for nom, Sx, rx in [("S_B + French", S, rF), ("S_A + French (= A)", SA, rF), ("S_A + S&P TR", SA, r)]:
        ini = [m for m in rango((1955, 1), (2026, 8))
               if Sx[m] < 0 and all(Sx[sig(m, -j)] >= 0 for j in range(1, 13))]
        evx = [np.prod([1 + rx[x] for x in rango(sig(m), sig(m, 12))]) - 1 for m in ini if sig(m, 12) <= (2026, 7)]
        ux = [np.prod([1 + rx[x] for x in rango(sig(m), sig(m, 12))]) - 1 for m in rango((1954, 1), sig((2026, 7), -12))]
        tx = (np.mean(evx) - np.mean(ux)) / (np.std(ux, ddof=1) / math.sqrt(len(evx)))
        p(f"  H5 {nom}: inicios {[ft(m) for m in ini]}; media 12m {100*np.mean(evx):.2f}% contra {100*np.mean(ux):.2f}% "
          f"(n={len(ux)}, sd {100*np.std(ux, ddof=1):.2f}%), t {tx:.2f}")
    # MXN en el tramo fuera (como A)
    p("  MXN fuera 1998-03..2026-07 (B):")
    for v in (elegido, "comprar_mantener", "sma10"):
        ser, _ = correr(W[v], r, rf, meses, C_DEF)
        x = [(1 + ser[m]) * fx[m] / fx[sig(m, -1)] - 1 for m in rango((1998, 3), MES_STOCK_FIN)]
        niv = np.concatenate([[1.0], np.cumprod(1 + np.array(x))])
        p(f"    {v:18s} CAGR {100*(niv[-1]**(12/len(x))-1):.2f}% MDD {100*np.min(niv/np.maximum.accumulate(niv)-1):.1f}%")
    p(f"  P(recesion 12m) con coef. fijos 1959-01..1994-03 y S_B 2026-08: {norm_cdf(fijo['a'] + fijo['b'] * S[(2026, 8)]):.4f}")
    p(f"  probit en tiempo real con S_A: max 2022-2025 {max(PmA[m] for m in rango((2022, 1), (2025, 8))):.4f}")

    (AQUI / "salida.txt").write_text("\n".join(SALIDA) + "\n")
    (AQUI / "resultados.json").write_text(json.dumps(RES, indent=1, default=lambda o: float(o) if isinstance(o, np.floating) else str(o)))


if __name__ == "__main__":
    main()
