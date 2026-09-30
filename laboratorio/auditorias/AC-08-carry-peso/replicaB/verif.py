# Segunda verificación: mínimo histórico del diferencial, regresión en muestras no traslapadas y polyfit.
import csv, bisect
from datetime import date, timedelta
import numpy as np
def leer(n):
    o=[]
    for r in list(csv.reader(open(n+".csv")))[1:]:
        if len(r)>1 and r[1] not in("","."): o.append((date.fromisoformat(r[0]),float(r[1])))
    return o
c=leer("SF43936"); t=leer("DTB3"); fx=leer("SF43718")
td=[x[0] for x in t]; fd=[x[0] for x in fx]; ULT=fd[-1]
def at(ds,s,d):
    i=bisect.bisect_right(ds,d)-1; return s[i][1]
sem=[(d, v-at(td,t,d)) for d,v in c if d>=date(2005,1,1)]
m=min(sem,key=lambda x:x[1]); print("mínimo del diferencial 2005-2026:", m, " segundo:", sorted(sem,key=lambda x:x[1])[1])
print("semanas con dif<2.0:", [(d.isoformat(),round(x,2)) for d,x in sem if x<2.0])
def ch(d,h):
    d1=d+timedelta(days=h)
    if d1>ULT: return None
    return 100*(at(fd,fx,d1)/at(fd,fx,d)-1)
for h,step in ((365,52),(182,26)):
    for off in range(0,step,13):
        s=[x for x in sem if x[0]>=date(2006,1,1)][off::step]
        pr=[(x[1],ch(x[0],h)) for x in s if ch(x[0],h) is not None]
        X=np.array([p[0] for p in pr]); Y=np.array([p[1] for p in pr])
        b,a=np.polyfit(X,Y,1); e=Y-(a+b*X); n=len(X)
        se=np.sqrt(e@e/(n-2)/((X-X.mean())@(X-X.mean())))
        r2=1-(e@e)/((Y-Y.mean())@(Y-Y.mean()))
        print(f"h={h}d no traslapado offset {off:2d}: n={n} b={b:+.2f} t={b/se:+.2f} R2={r2:.3f}")
# polyfit sobre muestra semanal completa para comparar coeficientes con analisis.py
for h in (182,365):
    pr=[(x[1],ch(x[0],h)) for x in sem if x[0]>=date(2006,1,1) and ch(x[0],h) is not None]
    X=np.array([p[0] for p in pr]); Y=np.array([p[1] for p in pr]); b,a=np.polyfit(X,Y,1)
    print(f"polyfit semanal h={h}: a={a:+.2f} b={b:+.2f} n={len(X)}")
