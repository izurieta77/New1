"""Replica A: diferencial de tasas de politica Banxico - Fed (lim. sup.) y FIX despues de cruzar umbrales.
Datos: bmx.json (SF61745, SF43718), fondeo43773.json (SF43773, proxy pre 21-ene-2008), DFEDTAR/DFEDTARU.csv (FRED)."""
import json, bisect, statistics as st, sys
from datetime import date, timedelta
import calendar
import os
D = os.path.dirname(os.path.abspath(__file__))
P = date.fromisoformat
raw = [(P(t), b, br, f, d, s) for t, b, br, f, d, s in json.load(open(f"{D}/diferencial.json"))]
# --- suavizado pre-2008: un nivel de fondeo redondeado que dura <5 dias habiles se ignora (ruido de mercado)
bm = [r[1] for r in raw]
sm = bm[:]
i = 0
cur = bm[0]
out = []
k = 0
while k < len(raw):
    t = raw[k][0]
    if t >= date(2008,1,21):
        out.append(bm[k]); k += 1; continue
    if bm[k] != cur:
        j = k
        while j < len(raw) and bm[j] == bm[k] and raw[j][0] < date(2008,1,21): j += 1
        if j - k >= 5 or raw[min(j,len(raw)-1)][0] >= date(2008,1,21): cur = bm[k]
    out.append(cur); k += 1
serie = [(r[0], out[n], r[3], round(out[n] - r[3], 4)) for n, r in enumerate(raw)]  # (t, bmx, fed, dif)
fixl = [(P(f), v) for f, v in json.load(open(f"{D}/bmx.json"))["SF43718"]]
fk = [t for t, _ in fixl]; fv = [v for _, v in fixl]
def fix_asof(t):
    i = bisect.bisect_right(fk, t) - 1
    return fk[i], fv[i]
ULT = fk[-1]  # ultimo FIX disponible
def add_m(t, m):
    y, mo = t.year + (t.month - 1 + m) // 12, (t.month - 1 + m) % 12 + 1
    return date(y, mo, min(t.day, calendar.monthrange(y, mo)[1]))
def fwd(t):
    _, x0 = fix_asof(t)
    r = {"fix0": x0}
    for m in (1, 3, 6, 12):
        tt = add_m(t, m)
        r[f"c{m}"] = None if tt > ULT else round((fix_asof(tt)[1] / x0 - 1) * 100, 2)
    end = add_m(t, 12)
    i0 = bisect.bisect_right(fk, t); i1 = bisect.bisect_right(fk, min(end, ULT))
    win = fv[i0:i1]
    r["maxdep12"] = round((max(win) / x0 - 1) * 100, 2) if win else None
    r["maxdep12_completo"] = end <= ULT
    if win:
        j = max(range(len(win)), key=lambda q: win[q]); r["fecha_max"] = str(fk[i0 + j])
    return r
dif_k = [s[0] for s in serie]
def dif_asof(t):
    return serie[bisect.bisect_right(dif_k, t) - 1][3]

def episodios_cruce(thr, persist=1, sep_m=12, desde=date(2006,1,1)):
    """(i) cruce hacia abajo: dif[t-1] > thr y dif[t] <= thr; opcional persistencia (dias habiles) ; separacion minima."""
    ev = []
    for n in range(1, len(serie)):
        t, _, _, d = serie[n]
        if t < desde: continue
        if serie[n-1][3] > thr and d <= thr:
            if persist > 1 and not all(serie[q][3] <= thr for q in range(n, min(n + persist, len(serie)))): continue
            if ev and t < add_m(ev[-1], sep_m): continue
            ev.append(t)
    return ev

def mensual(modo="fin"):
    """{(y,m): valor} con fin de mes o promedio mensual del diferencial."""
    g = {}
    for t, _, _, d in serie:
        g.setdefault((t.year, t.month), []).append((t, d))
    return {k: (v[-1][1] if modo == "fin" else sum(x for _, x in v) / len(v), v[-1][0], v) for k, v in sorted(g.items())}

def episodios_mes(thr, modo="fin", meses_arriba=6, sep_m=12, desde=(2006,1)):
    """(ii) primer mes <= thr tras >=6 meses consecutivos > thr. Fecha de inicio: primer dia del mes con dif<=thr."""
    M = mensual(modo); ks = list(M); ev = []
    for n, k in enumerate(ks):
        if k < desde or n < meses_arriba: continue
        if M[k][0] <= thr and all(M[ks[q]][0] > thr for q in range(n - meses_arriba, n)):
            # fecha de inicio = primer dia del mes en que el diario cruza; si promedio, fin de mes
            t0 = next((t for t, d in M[k][2] if d <= thr), M[k][1]) if modo == "fin" else M[k][1]
            if ev and t0 < add_m(ev[-1], sep_m): continue
            ev.append(t0)
    return ev

def base(desde=date(2006,1,1), hasta=None, filtro=None, mensual_fin=False):
    """Distribucion de c12 y maxdep12 para todos los dias (o fines de mes) con 12m completos."""
    hasta = hasta or add_m(ULT, -12)
    xs = []
    if mensual_fin:
        pts = [v[1] for k, v in mensual().items()]
    else:
        pts = fk
    for t in pts:
        if t < desde or t > hasta: continue
        if filtro and not filtro(dif_asof(t)): continue
        r = fwd(t); xs.append((r["c12"], r["maxdep12"], r["c1"], r["c3"], r["c6"]))
    return xs

def resumen(xs, idx, nombre):
    v = sorted(x[idx] for x in xs if x[idx] is not None)
    if not v: return f"{nombre}: n=0"
    q = lambda p: v[min(len(v) - 1, int(p * (len(v) - 1) + 0.5))]
    return (f"{nombre}: n={len(v)} mediana={st.median(v):.2f} p25={q(.25):.2f} p75={q(.75):.2f} "
            f"media={st.mean(v):.2f} P(>=14%)={sum(x >= 14 for x in v)/len(v):.0%} P(>=10%)={sum(x >= 10 for x in v)/len(v):.0%} P(>0)={sum(x > 0 for x in v)/len(v):.0%}")

if __name__ == "__main__":
    print("Hoy:", serie[-1], "| ultimo FIX", ULT, fv[-1])
    # periodos <=3
    print("\nPeriodos con dif <= 3.0 (2006-2026):")
    ini = None
    for n, (t, b, f, d) in enumerate(serie):
        if t < date(2006,1,1): continue
        if d <= 3.0 and ini is None: ini = t
        if d > 3.0 and ini is not None: print(f"  {ini} a {serie[n-1][0]}  (min dif {min(x[3] for x in serie if ini <= x[0] <= serie[n-1][0]):.2f})"); ini = None
    if ini: print(f"  {ini} a hoy {serie[-1][0]} (min {min(x[3] for x in serie if x[0] >= ini):.2f})")
    print("Max dif 2006-2026:", max((s for s in serie if s[0] >= date(2006,1,1)), key=lambda s: s[3]))
    print("Max dif 2022-2024:", max((s for s in serie if date(2022,1,1) <= s[0] <= date(2024,12,31)), key=lambda s: s[3]))
    for thr in (2.5, 3.0, 3.5):
        for persist in (1, 5):
            ev = episodios_cruce(thr, persist)
            print(f"\n== (i) cruce <= {thr} desde arriba, persistencia {persist}d, sep 12m: {[str(e) for e in ev]}")
            for e in ev:
                r = fwd(e); print(f"   {e} dif={dif_asof(e):.2f} FIX0={r['fix0']} c1={r['c1']} c3={r['c3']} c6={r['c6']} c12={r['c12']} maxdep12={r['maxdep12']} ({r['fecha_max']}, completo={r['maxdep12_completo']})")
        for modo in ("fin", "prom"):
            ev = episodios_mes(thr, modo)
            print(f"== (ii) primer mes <= {thr} ({modo}) tras >=6m arriba: {[str(e) for e in ev]}")
            for e in ev:
                r = fwd(e); print(f"   {e} dif={dif_asof(e):.2f} FIX0={r['fix0']} c1={r['c1']} c3={r['c3']} c6={r['c6']} c12={r['c12']} maxdep12={r['maxdep12']} ({r['fecha_max']}, completo={r['maxdep12_completo']})")
    print("\n== Tasa base (diaria, 2006-01-02 .. ultimo con 12m completos)")
    allx = base(); print(" ", resumen(allx, 0, "c12 todos")); print(" ", resumen(allx, 1, "maxdep12 todos"))
    for thr in (2.5, 3.0, 3.5):
        lo = base(filtro=lambda d: d <= thr); hi = base(filtro=lambda d: d > thr)
        print(f"  thr {thr}:"); print("   ", resumen(lo, 0, f"c12 dif<={thr}")); print("   ", resumen(lo, 1, f"maxdep12 dif<={thr}"))
        print("   ", resumen(hi, 0, f"c12 dif>{thr}")); print("   ", resumen(hi, 1, f"maxdep12 dif>{thr}"))
    print("\n== Tasa base mensual (fin de mes)")
    allm = base(mensual_fin=True); print(" ", resumen(allm, 0, "c12")); print(" ", resumen(allm, 1, "maxdep12"))
    for m_idx, nm in ((2, "c1"), (3, "c3"), (4, "c6")): print(" ", resumen(allm, m_idx, nm))
    lo = base(mensual_fin=True, filtro=lambda d: d <= 3.0); hi = base(mensual_fin=True, filtro=lambda d: d > 3.0)
    print(" ", resumen(lo, 0, "c12 dif<=3")); print(" ", resumen(lo, 1, "maxdep12 dif<=3")); print(" ", resumen(hi, 0, "c12 dif>3")); print(" ", resumen(hi, 1, "maxdep12 dif>3"))
    # excluyendo crisis 2008 y covid
    ex = lambda t: not (date(2007,10,1) <= t <= date(2009,3,31)) and not (date(2019,3,1) <= t <= date(2020,5,31))
    xs = [ (fwd(v[1])['c12'], fwd(v[1])['maxdep12']) for k, v in mensual().items() if date(2006,1,1) <= v[1] <= add_m(ULT,-12) and ex(v[1]) and dif_asof(v[1])>3]
    print("  c12 dif>3 sin ventanas 2008/covid:", resumen([(a,b,None,None,None) for a,b in xs],0,"c12"), "|", resumen([(a,b,None,None,None) for a,b in xs],1,"maxdep12"))
