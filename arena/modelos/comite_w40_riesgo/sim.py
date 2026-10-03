import pickle,bisect,math
h=pickle.load(open('hist.pkl','rb')); dx=dict(pickle.load(open('dexmxus.pkl','rb')))
G=h['^GSPC'];N=h['^NDX'];V=h['^VIX'];I=h['^IRX'];M=h['MXN=X'];U=h['UPRO']
days=sorted(d for d in G if d in N and d in V and d.year>=1993)
# fx: DEXMXUS then MXN=X fill
fxd={**dx}; 
for d,v in M.items():
    if d not in fxd and v: fxd[d]=v
fk=sorted(fxd); 
def fx(d): return fxd[fk[bisect.bisect_right(fk,d)-1]]
ik=sorted(I)
def rf(d): return I[ik[bisect.bisect_right(ik,d)-1]]/100
# SMA200 over full GSPC
gk=sorted(G); gp=[G[d] for d in gk]; idx={d:i for i,d in enumerate(gk)}
def sma(d):
    i=idx[d]; return sum(gp[i-199:i+1])/200
DIV=0.015; ERU=0.0091; DRAG=float(__import__('os').environ.get('DRAG','0.0'))
R=[]  # per day t (from t-1 to t): sp, nd, upro_syn, fxret
for a,b in zip(days,days[1:]):
    sp=G[b]/G[a]-1+DIV/252; nd=N[b]/N[a]-1+0.007/252
    r=rf(a)/252
    up=3*sp-2*r-(ERU+DRAG)/252
    R.append((b,sp,nd,up,fx(b)/fx(a)-1))
# calibrate vs real UPRO
uk=[x for x in R if x[0] in U and x[0].year>=2010]
import statistics
real=1;syn=1;prev=None
for x in R:
    d=x[0]
    if d in U and prev in U and d.year>=2010:
        real*=U[d]/U[prev]; syn*=1+x[3]
    prev=d
yrs=len([x for x in R if x[0].year>=2010])/252
print('calib 2010+: UPRO real CAGR %.2f%% synth %.2f%%'%((real**(1/yrs)-1)*100,(syn**(1/yrs)-1)*100))
# filter state per day (state known at close of day d)
state={};on=True
for d in days:
    if idx[d]<200: state[d]=on; continue
    s=sma(d)
    if on and (G[d]<s*0.97 or V[d]>=25): on=False
    elif (not on) and G[d]>s*1.03 and V[d]<25: on=True
    state[d]=on
def run(w,H=82,start_year=1994,usd=False):
    ws,wn,wu,wc=w
    res=[]
    for i in range(len(R)-H):
        d0=R[i][0]
        if d0.year<start_year: continue
        # require prior day state on (filter on at entry)
        prevd=days[days.index(d0)-1] if False else None
        res.append(i)
    out=[]
    dlist=[x[0] for x in R]
    for i in res:
        d0=dlist[i-1] if i>0 else None
        if d0 is None or not state.get(d0,False): continue
        s,n,u,c=ws,wn,wu,wc; peak=1; mdd=0; pend=None; inu=True; minv=1
        for k in range(i,i+H):
            d,sp,nd,up,fr=R[k]
            f=0 if usd else fr
            s*=(1+sp)*(1+f); n*=(1+nd)*(1+f); u*=(1+up)*(1+f)
            tot=s+n+u+c
            # action executed at close today based on yesterday's signal
            if pend=='sell' and inu: c+=u*(1-0.0029); u=0; inu=False
            elif pend=='buy' and not inu:
                amt=max(0,c-wc*tot); u=amt*(1-0.0029); c-=amt; inu=True
            pend=None
            st=state[d]
            if inu and not st: pend='sell'
            if (not inu) and st: pend='buy'
            tot=s+n+u+c
            peak=max(peak,tot); mdd=min(mdd,tot/peak-1); minv=min(minv,tot)
        out.append((mdd,minv-1,tot-1))
    return out
def rep(name,w,**kw):
    o=run(w,**kw); n=len(o)
    p=lambda L,j: 100*sum(1 for x in o if x[j]<=L)/n
    q=sorted(x[2] for x in o); md=sorted(x[0] for x in o)
    print(f"{name:34s} n={n} DD<=-12/20/28/35: {p(-.12,0):.1f}/{p(-.20,0):.1f}/{p(-.28,0):.1f}/{p(-.35,0):.2f}%  | desde inicio -12/20/28/35: {p(-.12,1):.1f}/{p(-.20,1):.1f}/{p(-.28,1):.1f}/{p(-.35,1):.2f}%  peorDD {md[0]*100:.1f}% med {q[n//2]*100:.1f}% p10 {q[n//10]*100:.1f}%")
import sys
cfgs={'papel 40/27/27/5':(0.402,0.274,0.268,0.055),
 'papel A 56/27/0/16':(0.563,0.274,0,0.163),
 'real QQQM+UPRO 0/56/27/17':(0,0.560,0.274,0.166),
 'real 3SPYM+UPRO 49/0/27/23':(0.493,0,0.274,0.233),
 'alt 35%UPRO 33/27/35/5':(0.33,0.274,0.35,0.046)}
for sy in (1994,2004):
  for usd in (False,True):
    print('--- desde',sy,'USD' if usd else 'MXN')
    for k,w in cfgs.items(): rep(k,w,start_year=sy,usd=usd)
