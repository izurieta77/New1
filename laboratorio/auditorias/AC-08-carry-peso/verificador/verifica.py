"""Verificador adversarial: recalculo propio (descarga propia via fetch.py; series en base.py).
Reproduce episodios de A y B, tasa base, condicional <=3, prueba de desplazamiento circular, pares FX 2014-15, momentum y probabilidades de 18.50/19.50."""
import csv
exec(open("base.py").read())
def fila(t):
    f=lambda v: 'n/d' if v is None else f'{v:+.2f}'
    return f"{t} FIX0={fix_asof(t):.4f} 1m={f(fwd(t,1))} 3m={f(fwd(t,3))} 6m={f(fwd(t,6))} 12m={f(fwd(t,12))} max12={f(maxdep(t))} (parcial {maxdep(t,parcial=True):+.2f})"
print("Episodios A:"); [print(" ",fila(P(t))) for t in ["2006-02-24","2014-06-06","2026-03-27","2026-09-17"]]
print("Episodios B:"); [print(" ",fila(P(t))) for t in ["2006-02-23","2014-06-12","2015-10-08","2026-04-09"]]
def stats(ts, nombre):
    c=[x for x in (fwd(t,12) for t in ts) if x is not None]; m=[x for x in (maxdep(t) for t in ts) if x is not None]
    print(f"{nombre}: n={len(c)} 12m med {st.median(c):+.2f} P>=14 {sum(x>=14 for x in c)/len(c):.0%} | max12 med {st.median(m):+.2f} P>=14 {sum(x>=14 for x in m)/len(m):.0%}")
FKs=set(FK); fin=date(2025,9,29)
Dd=[(t,d) for t,d in POL if date(2006,1,2)<=t<=fin and t in FKs]
stats([t for t,_ in Dd],"POL diario todos"); stats([t for t,d in Dd if d<=3],"POL diario <=3")
W=[(t,d) for t,d in MKT if date(2006,1,1)<=t and addm(t,12)<=LAST]
stats([t for t,_ in W],"MKT semanal todos"); stats([t for t,d in W if d<=3],"MKT semanal <=3")
ind=[d<=3 for _,d in W]; c12=[fwd(t,12) for t,_ in W]; mx=[maxdep(t) for t,_ in W]
def stat(ind):
    a=[c for c,i in zip(c12,ind) if i]; b=[c for c,i in zip(c12,ind) if not i]
    am=[c for c,i in zip(mx,ind) if i]; bm=[c for c,i in zip(mx,ind) if not i]
    return st.median(a)-st.median(b), sum(x>=14 for x in am)/len(am)-sum(x>=14 for x in bm)/len(bm)
obs=stat(ind); res=[stat(ind[k:]+ind[:k]) for k in range(52,len(ind)-52)]
print("desplazamiento circular semanal: obs", obs, "p", sum(r[0]>=obs[0] for r in res)/len(res), sum(r[1]>=obs[1] for r in res)/len(res))
