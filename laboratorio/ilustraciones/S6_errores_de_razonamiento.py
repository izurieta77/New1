"""Errores de razonamiento del examen S6 (2026-09-25): ejercicio numerico y comprobacion.

Ficha: conocimiento/fichas/2026-09-25-examen-S6-errores-de-razonamiento.md
Datos congelados: laboratorio/examen-datos/S6/ (verificar antes con sha256sum -c SHA256SUMS.txt).

  E1  RF de los factores regionales de French = T-bill de EUA a 1 mes (S6-01).
  E2  Peso de Bartlett de gamma_6 con L=6 y su efecto en el SE Newey-West (S6-02).
  E3  Probabilidad de una t negativa "significativa" en el minimo de ventanas moviles
      bajo una prima positiva constante (S6-02, "casi garantiza").
  E4  Direccion del sesgo del SE al tratar el benchmark BGL como fijo (S6-04).

Uso: python3 laboratorio/ilustraciones/S6_errores_de_razonamiento.py
Salida guardada en laboratorio/ilustraciones/S6_errores_de_razonamiento-salida.txt
"""
import csv
import io
import math
import os
import sys
import zipfile

import numpy as np

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, RAIZ)
from herramientas import estadistica  # noqa: E402

D = os.path.join(RAIZ, "laboratorio", "examen-datos", "S6")
Z = 1.959963984540054


def mensual(zipname):
    """Primer bloque mensual (yyyymm) de un CSV de French: {yyyymm: {columna: valor}}."""
    z = zipfile.ZipFile(os.path.join(D, zipname))
    txt = z.read(z.namelist()[0]).decode("latin-1")
    out, cols = {}, None
    for fila in csv.reader(io.StringIO(txt)):
        if not fila:
            continue
        c0 = fila[0].strip()
        if cols is None and len(fila) > 1 and c0 == "" and fila[1].strip():
            cols = [c.strip() for c in fila[1:]]
            continue
        if cols is not None:
            if len(c0) == 6 and c0.isdigit():
                out[int(c0)] = {k: float(v) for k, v in zip(cols, fila[1:])}
            elif out:
                break
    return out


def meses(d, ini, fin):
    return [m for m in sorted(d) if ini <= m <= fin]


def phi(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


us = mensual("F-F_Research_Data_Factors_CSV.zip")
jp = mensual("Japan_3_Factors_CSV.zip")
eu = mensual("Europe_3_Factors_CSV.zip")

# ---------------------------------------------------------------- E1
print("== E1. RF de los factores regionales de French")
for nom, reg in (("Japon", jp), ("Europa", eu)):
    comunes = sorted(set(reg) & set(us))
    dif = [(m, reg[m]["RF"], us[m]["RF"]) for m in comunes if abs(reg[m]["RF"] - us[m]["RF"]) > 1e-9]
    print(f"  {nom}: {len(comunes)} meses comunes ({comunes[0]}-{comunes[-1]}); RF identico en "
          f"{len(comunes) - len(dif)}; distintos: {dif}")
v = meses(jp, 199101, 202512)
rf = np.array([jp[m]["RF"] for m in v]) / 100
ex = np.array([jp[m]["Mkt-RF"] for m in v]) / 100
R = ex + rf
n = len(v)
cagr = np.prod(1 + R) ** (12 / n) - 1
cagr_rf = np.prod(1 + rf) ** (12 / n) - 1
print(f"  Japon USD 1991-01..2025-12: n={n}; media RF={100 * rf.mean():.4f} %/mes "
      f"(x12 {1200 * rf.mean():.3f} %); CAGR de R=Mkt-RF+RF {100 * cagr:.3f} %; CAGR del RF {100 * cagr_rf:.3f} %")
print(f"  media x12 de Mkt-RF (exceso sobre T-bill de EUA) = {1200 * ex.mean():.3f} %; de R = {1200 * R.mean():.3f} %")
FRED_JP = os.path.join(RAIZ, "laboratorio", "ilustraciones", "datos", "fred_IRSTCI01JPM156N.csv")
if os.path.exists(FRED_JP):  # tasa call de Japon (OECD MEI via FRED), % anual; solo contraste
    with open(FRED_JP) as f:
        filas = list(csv.reader(f))[1:]
    jpc = [float(r[1]) for r in filas if "1991-01-01" <= r[0] <= "2025-12-01" and r[1] not in ("", ".")]
    print(f"  contraste: tasa call de Japon (FRED IRSTCI01JPM156N) 1991-01..2025-12, n={len(jpc)}, "
          f"media {sum(jpc) / len(jpc):.3f} % anual  vs  RF de French x12 {1200 * rf.mean():.3f} %")

# ---------------------------------------------------------------- E2
print("\n== E2. Peso de gamma_6 en Newey-West(6), HML de EUA 2007-01..2020-12")
v = meses(us, 200701, 202012)
x = [us[m]["HML"] for m in v]
n = len(x)
b = estadistica.contribuciones_nw(x, 6, "bartlett")
u = estadistica.contribuciones_nw(x, 6, "uniforme")
nw = estadistica.newey_west(x, 6)
print(f"  n={n}  media={np.mean(x):.4f}  t_IID={nw['t_iid']:.3f}  t_NW(6)={nw['t']:.4f}  SE_NW={nw['se']:.5f}")
print("  j  gamma_j   rho_j   w_j(Bart)  2*w_j*gamma_j  | w_j(unif) 2*gamma_j")
for j in range(7):
    print(f"  {j}  {b['gammas'][j]:7.3f}  {b['gammas'][j] / b['gammas'][0]:6.3f}   {b['pesos'][j]:.4f}    "
          f"{b['contribuciones'][j]:8.3f}       |   {u['pesos'][j]:.0f}    {u['contribuciones'][j]:8.3f}")
print(f"  S_Bartlett={b['S']:.3f}  t={b['t']:.3f}   |   S_uniforme={u['S']:.3f}  t={u['t']:.3f}")
c = b["contribuciones"]
print(f"  lag 6 / lag 1 (Bartlett) = {c[6]:.3f} / {c[1]:.3f} = {c[6] / c[1]:.3f};  "
      f"(uniforme) = {u['contribuciones'][6]:.3f} / {u['contribuciones'][1]:.3f} = "
      f"{u['contribuciones'][6] / u['contribuciones'][1]:.3f}")
print(f"  rezagos 4-6 suman {sum(c[4:7]):.3f}; rezagos 1-3 suman {sum(c[1:4]):.3f}")
S_sin6 = b["S"] - c[6]
se_sin6 = math.sqrt(S_sin6 / (n - 1))
print(f"  Sin el rezago 6 (gamma_6 := 0): S={S_sin6:.3f}, SE={se_sin6:.5f}, t={np.mean(x) / se_sin6:.3f} "
      f"(cambio de SE {100 * (nw['se'] / se_sin6 - 1):+.2f} %; de t {nw['t'] - np.mean(x) / se_sin6:+.3f})")
dse = (1 / 7) / (2 * b["S"])  # d ln SE / d gamma_6 = (dS/dgamma_6)/(2S) = (2/7)/(2S)
print(f"  d ln(SE)/d gamma_6 = (2/7)/(2S) = {dse:.5f} por unidad de gamma_6")
P = np.array([[b["gammas"][abs(i - j)] for j in range(7)] for i in range(7)])
print(f"  Teorema 1 NW: e'Pe/(L+1) = {P.sum() / 7:.6f}  vs S = {b['S']:.6f}; "
      f"eigenvalor minimo de P = {np.linalg.eigvalsh(P).min():.4f}")
print("  Pesos de Bartlett: L, w_L=1/(L+1), participacion de w_L en suma w_1..w_L = 2/(L(L+1))")
for L in (1, 3, 4, 6, 12, 24):
    w = estadistica.pesos_bartlett(L)
    print(f"    L={L:2d}  w_L={w[L]:.4f}  participacion={w[L] / sum(w[1:]):.4f}")

# ---------------------------------------------------------------- E3
print("\n== E3. Minimo de t sobre ventanas moviles de 168 meses bajo prima positiva")
v = meses(us, 192607, 202607)
h = np.array([us[m]["HML"] for m in v])
N, W = len(h), 168
K = N - W + 1
nwf = estadistica.newey_west(list(h), 6)
print(f"  HML 1926-07..2026-07: N={N}, media={h.mean():.4f}, sd={h.std(ddof=1):.4f}, "
      f"t_IID={nwf['t_iid']:.2f}, t_NW(6)={nwf['t']:.2f}; ventanas={K}")


def t_ventanas(M):
    """t IID de todas las ventanas de largo W; M con forma (B, N)."""
    c1 = np.concatenate([np.zeros((M.shape[0], 1)), np.cumsum(M, axis=1)], axis=1)
    c2 = np.concatenate([np.zeros((M.shape[0], 1)), np.cumsum(M * M, axis=1)], axis=1)
    s1 = c1[:, W:] - c1[:, :-W]
    s2 = c2[:, W:] - c2[:, :-W]
    med = s1 / W
    var = (s2 - W * med * med) / (W - 1)
    return med / np.sqrt(var / W)


def t_ventanas_nw(M, L=6):
    """t Newey-West(L) (Bartlett, n/(n-1)) de todas las ventanas de largo W; M con forma (B, N)."""
    z0 = np.zeros((M.shape[0], 1))
    c1 = np.concatenate([z0, np.cumsum(M, axis=1)], axis=1)
    s1 = c1[:, W:] - c1[:, :-W]
    med = s1 / W
    S = None
    for j in range(L + 1):
        cp = np.concatenate([z0, np.cumsum(M[:, j:] * M[:, :M.shape[1] - j], axis=1)], axis=1)
        # ventana que empieza en s: pares t = s+j..s+W-1 -> indices de cp s..s+W-j
        sp = cp[:, W - j:W - j + K] - cp[:, :K]
        a = c1[:, W:W + K] - c1[:, j:j + K]  # suma de x_t, t = s+j..s+W-1
        bb = c1[:, W - j:W - j + K] - c1[:, :K]  # suma de x_{t-j}, t-j = s..s+W-1-j
        g = (sp - med * (a + bb) + (W - j) * med * med) / W
        S = g if j == 0 else S + 2 * (1 - j / (L + 1)) * g
    return med / np.sqrt(S / (W - 1))


tv = t_ventanas(h[None, :])[0]
tvnw = t_ventanas_nw(h[None, :])[0]
i_min = int(tv.argmin())
i_obs = v.index(200701)
print(f"  observado: t_IID de 2007-01..2020-12 = {tv[i_obs]:.3f}; minimo = {tv[i_min]:.3f} "
      f"({v[i_min]}..{v[i_min + W - 1]}); rango de t en ventanas [{tv.min():.2f}, {tv.max():.2f}]")
chk = estadistica.newey_west(list(h[i_obs:i_obs + W]), 6)["t"]
j_min = int(tvnw.argmin())
print(f"  t_NW(6) por ventanas (cumsum) en 2007-01 = {tvnw[i_obs]:.4f} vs herramientas.newey_west = {chk:.4f}; "
      f"minimo t_NW = {tvnw[j_min]:.3f} ({v[j_min]}..{v[j_min + W - 1]})")
Et = h.mean() * math.sqrt(W) / h.std(ddof=1)
p1 = phi(-Z - Et)
k_disj = N // W
print(f"  analitico (normal): E[t] por ventana = {Et:.3f}; p1 = P(t < -1.96) = Phi({-Z - Et:.3f}) = {p1:.5f}")
print(f"    {k_disj} ventanas disjuntas: 1-(1-p1)^{k_disj} = {1 - (1 - p1) ** k_disj:.4f}; "
      f"cota de Bonferroni {K}*p1 = {K * p1:.3f}")

rng = np.random.default_rng(20260925)
B = 4000


def sim_iid(mu, B=B):
    base = h - h.mean() + mu
    return base[rng.integers(0, N, size=(B, N))]


def sim_bloques(mu, bloque, B=B):
    base = h - h.mean() + mu
    nb = -(-N // bloque)
    ini = rng.integers(0, N, size=(B, nb))
    idx = (ini[:, :, None] + np.arange(bloque)[None, None, :]) % N  # circular
    return base[idx.reshape(B, -1)[:, :N]]


def resumen(nombre, tt, t_obs_min):
    mn = tt.min(axis=1)
    pm = (mn < -Z).mean()
    pmarg = (tt < -Z).mean()
    meff = math.log(1 - pm) / math.log(1 - pmarg) if 0 < pmarg < pm < 1 else float("nan")
    se_pm = math.sqrt(pm * (1 - pm) / tt.shape[0])
    print(f"  {nombre}: P(min t < -1.96) = {pm:.4f} (+/- {1.96 * se_pm:.4f}); mediana del minimo = "
          f"{np.median(mn):.3f}; P(t < -1.96) por ventana = {pmarg:.5f}; pruebas independientes "
          f"equivalentes = {meff:.0f}; P(min <= {t_obs_min:.2f}) = {(mn <= t_obs_min).mean():.3f}")


for nombre, M in (("iid", sim_iid(h.mean())), ("bloques circulares de 24", sim_bloques(h.mean(), 24))):
    resumen(f"bootstrap {nombre} (B={B}, prima {h.mean():.3f}), t IID", t_ventanas(M), tv[i_min])
    resumen(f"bootstrap {nombre} (B={B}, prima {h.mean():.3f}), t NW(6)", t_ventanas_nw(M), tvnw[j_min])
for mu in (0.0, 0.10, 0.20):
    mn = t_ventanas(sim_iid(mu, 2000)).min(axis=1)
    print(f"  bootstrap iid con prima {mu:.2f} (B=2000), t IID: P(min t < -1.96) = {(mn < -Z).mean():.3f}")

# ---------------------------------------------------------------- E4
print("\n== E4. Prueba de Fisher con benchmark BGL fijo (EUA vs Europa, 1990-07..2025-12)")
v = meses(us, 199007, 202512)
X = np.array([us[m]["Mkt-RF"] for m in v])
Y = np.array([eu[m]["Mkt-RF"] for m in v])


def estad(X, Y):
    rho = np.corrcoef(X, Y)[0, 1]
    a = X < 0
    rd = np.corrcoef(X[a], Y[a])[0, 1]
    q = X.var(ddof=1) / X[a].var(ddof=1)
    bgl = rho / math.sqrt(rho ** 2 + (1 - rho ** 2) * q)
    return rho, rd, bgl, int(a.sum())


rho, rd, bgl, nd = estad(X, Y)
zf = (math.atanh(rd) - math.atanh(bgl)) * math.sqrt(nd - 3)
se_f = (1 - rd ** 2) / math.sqrt(nd - 3)
print(f"  n={len(X)} rho={rho:.4f} n_down={nd} rho_down={rd:.4f} BGL={bgl:.4f} exceso={rd - bgl:.4f}")
print(f"  Fisher con benchmark fijo: z={zf:.3f}, p bilateral={2 * (1 - phi(abs(zf))):.3f}; "
      f"SE implicito en escala rho=(1-rho_down^2)/raiz(n_down-3)={se_f:.4f}")
nB = 5000
rb = np.random.default_rng(7)
res = np.array([estad(X[i], Y[i]) for i in rb.integers(0, len(X), size=(nB, len(X)))])
sd_r, sd_b = res[:, 1].std(ddof=1), res[:, 2].std(ddof=1)
cor = np.corrcoef(res[:, 1], res[:, 2])[0, 1]
sd_d = (res[:, 1] - res[:, 2]).std(ddof=1)
print(f"  bootstrap iid de pares (B={nB}): sd(rho_down)={sd_r:.4f}  sd(BGL)={sd_b:.4f}  corr={cor:.3f}  "
      f"sd(exceso)={sd_d:.4f}")
print(f"    formula: raiz(sd_r^2+sd_b^2-2 corr sd_r sd_b) = {estadistica.se_diferencia(sd_r, sd_b, cor):.4f}; "
      f"umbral corr* = sd_b/(2 sd_r) = {sd_b / (2 * sd_r):.3f}")
lo, hi = np.percentile(res[:, 1] - res[:, 2], [2.5, 97.5])
print(f"    IC95 percentil del exceso = [{lo:.4f}, {hi:.4f}]; P(exceso <= 0) = {(res[:, 1] - res[:, 2] <= 0).mean():.4f}")
print(f"    corr(rho_down, rho total) = {np.corrcoef(res[:, 1], res[:, 0])[0, 1]:.3f}")
print(f"    z con sd bootstrap del exceso = {(rd - bgl) / sd_d:.3f}  vs  z de Fisher = {zf:.3f}")
nT = len(X)
for bloque in (12, 24):  # bootstrap circular por bloques (preserva agrupamiento de volatilidad)
    nb = -(-nT // bloque)
    ini = rb.integers(0, nT, size=(2000, nb))
    idx = ((ini[:, :, None] + np.arange(bloque)[None, None, :]) % nT).reshape(2000, -1)[:, :nT]
    rbk = np.array([estad(X[i], Y[i]) for i in idx])
    a_, b_ = rbk[:, 1].std(ddof=1), rbk[:, 2].std(ddof=1)
    c_ = np.corrcoef(rbk[:, 1], rbk[:, 2])[0, 1]
    d_ = rbk[:, 1] - rbk[:, 2]
    print(f"  bootstrap bloques circulares de {bloque} (B=2000): sd(rho_down)={a_:.4f} sd(BGL)={b_:.4f} "
          f"corr={c_:.3f} sd(exceso)={d_.std(ddof=1):.4f}; IC95 [{np.percentile(d_, 2.5):.4f}, "
          f"{np.percentile(d_, 97.5):.4f}]; umbral corr*={b_ / (2 * a_):.3f}")

# Comprobacion bajo H0: normal bivariada con correlacion constante (BGL exacto), con la
# media de X fijada para que P(X < 0) = 154/426, como en la muestra.
R_MC = 20000
mc = np.random.default_rng(11)
sx, sy = X.std(ddof=1), Y.std(ddof=1)
q = nd / len(X)
lo_, hi_ = -10.0, 10.0
for _ in range(200):  # inversa de phi por biseccion: phi(-k) = q
    mid = (lo_ + hi_) / 2
    lo_, hi_ = (mid, hi_) if phi(-mid) > q else (lo_, mid)
k_media = (lo_ + hi_) / 2
rej, zs, ds, rs, bs, ns = 0, [], [], [], [], []
for _ in range(R_MC):
    x0 = mc.standard_normal(len(X))
    y0 = rho * x0 + math.sqrt(1 - rho ** 2) * mc.standard_normal(len(X))
    r0, d0, b0, n0 = estad(sx * (x0 + k_media), sy * y0)
    z0 = (math.atanh(d0) - math.atanh(b0)) * math.sqrt(n0 - 3)
    rej += abs(z0) > Z
    zs.append(z0)
    ds.append(d0 - b0)
    rs.append(d0)
    bs.append(b0)
    ns.append(n0)
rs, bs, ds, zs = np.array(rs), np.array(bs), np.array(ds), np.array(zs)
print(f"  Monte Carlo H0 normal (rho={rho:.3f}, n={len(X)}, media de X = {k_media:.3f} sd, "
      f"n_down medio={np.mean(ns):.1f}, R={R_MC}):")
print(f"    tamano real de Fisher al 5 % = {rej / R_MC:.4f} (+/- {1.96 * math.sqrt(0.05 * 0.95 / R_MC):.4f}); "
      f"sd(z de Fisher) = {zs.std(ddof=1):.3f} (1 si el SE fuera correcto)")
print(f"    sd(rho_down)={rs.std(ddof=1):.4f} sd(BGL)={bs.std(ddof=1):.4f} corr={np.corrcoef(rs, bs)[0, 1]:.3f} "
      f"sd(exceso)={ds.std(ddof=1):.4f}; media del exceso={ds.mean():+.4f}; "
      f"umbral corr* = {bs.std(ddof=1) / (2 * rs.std(ddof=1)):.3f}")
print(f"    media rho_down={rs.mean():.4f} media BGL={bs.mean():.4f}; SE de Fisher implicito en escala rho = "
      f"(1-{rs.mean():.3f}^2)/raiz({np.mean(ns):.0f}-3) = {(1 - rs.mean() ** 2) / math.sqrt(np.mean(ns) - 3):.4f}")
