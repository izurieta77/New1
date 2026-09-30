"""Verificador: series propias (descarga propia), sin reutilizar codigo de las replicas."""
import json, csv, bisect, statistics as st
from datetime import date, timedelta
P = date.fromisoformat
B = json.load(open("bmx.json"))
def fred(s):
    return sorted((P(r["observation_date"]), float(r[s])) for r in csv.DictReader(open(f"{s}.csv")) if r[s] not in ("","."))
FIX = sorted((P(d), v) for d, v in B["SF43718"])
FK = [d for d,_ in FIX]; FV=[v for _,v in FIX]
def asof_factory(serie):
    ks=[d for d,_ in serie]; vs=[v for _,v in serie]
    def f(t, maxlag=None):
        i=bisect.bisect_right(ks,t)-1
        if i<0: return None
        if maxlag is not None and (t-ks[i]).days>maxlag: return None
        return vs[i]
    return f
fix_asof = asof_factory(FIX)
LAST = FK[-1]
# ---- Politica: Banxico objetivo (2008-01-21+) y proxy pre-2008 = mediana movil 10 dias habiles del fondeo, redondeada a 0.25
fondeo = sorted((P(d), v) for d, v in B["SF43773"])
obj = sorted((P(d), v) for d, v in B["SF61745"])
obj_f = asof_factory(obj)
fk=[d for d,_ in fondeo]; fv=[v for _,v in fondeo]
proxy={}
for i,t in enumerate(fk):
    w=fv[max(0,i-9):i+1]
    proxy[t]=round(st.median(w)*4)/4
proxy_f = asof_factory(sorted(proxy.items()))
fed = [x for x in fred("DFEDTAR") if x[0] < date(2008,12,16)] + fred("DFEDTARU")
fed_f = asof_factory(fed)
fedl = [x for x in fred("DFEDTAR") if x[0] < date(2008,12,16)] + fred("DFEDTARL")
fedl_f = asof_factory(fedl)
def bmx_pol(t): return obj_f(t) if t >= date(2008,1,21) else proxy_f(t)
DIAS = [t for t in FK if t >= date(2005,6,1)]
if DIAS[-1] < date(2026,9,30): DIAS.append(date(2026,9,30))
POL = [(t, bmx_pol(t) - fed_f(t)) for t in DIAS]
# ---- Mercado: CETES28 (fecha Banxico) - DTB3 (ultimo <= fecha, max 7 dias)
C28 = sorted((P(d), v) for d, v in B["SF43936"])
tb3_f = asof_factory(fred("DTB3"))
MKT = [(t, round(c - tb3_f(t, 7), 4)) for t, c in C28 if tb3_f(t, 7) is not None]
def addm(t, m):
    import calendar
    y=t.year+(t.month-1+m)//12; mo=(t.month-1+m)%12+1
    return date(y,mo,min(t.day,calendar.monthrange(y,mo)[1]))
def fwd(t, meses):
    """cambio % del FIX de t (ultimo FIX <= t) a t+meses (ultimo FIX <= esa fecha); None si no hay datos."""
    t1=addm(t,meses)
    if t1 > LAST: return None
    return 100*(fix_asof(t1)/fix_asof(t)-1)
def maxdep(t, meses=12, parcial=False):
    t1=addm(t,meses)
    if t1 > LAST and not parcial: return None
    i0=bisect.bisect_right(FK,t); i1=bisect.bisect_right(FK,min(t1,LAST))
    w=FV[i0:i1]
    return 100*(max(w)/fix_asof(t)-1) if w else None
def cruces(serie, thr, sep_m=12, desde=date(2006,1,1)):
    ev=[]
    for (t0,d0),(t1,d1) in zip(serie, serie[1:]):
        if t1<desde: continue
        if d0>thr and d1<=thr and (not ev or t1>=addm(ev[-1],sep_m)): ev.append(t1)
    return ev
def q(v,p):
    v=sorted(v); k=(len(v)-1)*p; a=int(k); b=min(a+1,len(v)-1); return v[a]+(v[b]-v[a])*(k-a)
