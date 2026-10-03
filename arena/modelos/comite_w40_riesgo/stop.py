exec(open('sim.py').read().split("def run(")[0])
def run2(w,H=82,stop=-0.112,start_year=1994):
    ws,wn,wu,wc=w; out=[]; dl=[x[0] for x in R]
    for i in range(1,len(R)-H):
        if dl[i].year<start_year or not state.get(dl[i-1],False): continue
        s,n,u,c=ws,wn,wu,wc; peak=1;mdd=0;pend=None;inu=True;ref=wu;stopped=False;flt=False
        for k in range(i,i+H):
            d,sp,nd,up,fr=R[k]
            s*=(1+sp)*(1+fr); n*=(1+nd)*(1+fr); uu=u*(1+up)
            if inu and not stopped and wu>0:
                # usd price ratio
                ref*=(1+up)
                if ref/wu-1<=stop: stopped=True; c+=u*(1+stop/1)*(1+fr)*(1-0.0029) if False else 0
            u=uu*(1+fr)
            if stopped and inu: c+=u*(1-0.0029); u=0; inu=False
            if pend=='sell' and inu: c+=u*(1-0.0029); u=0; inu=False; flt=True
            pend=None
            if inu and not state[d]: pend='sell'
            tot=s+n+u+c; peak=max(peak,tot); mdd=min(mdd,tot/peak-1)
        out.append((mdd,stopped,tot-1,flt))
    n=len(out); p=lambda L: 100*sum(1 for x in out if x[0]<=L)/n
    q=sorted(x[2] for x in out)
    print(f"n={n} P(stop)={100*sum(x[1] for x in out)/n:.0f}% P(salida filtro)={100*sum(x[3] for x in out)/n:.0f}% DD -12/20/28/35: {p(-.12):.1f}/{p(-.2):.1f}/{p(-.28):.1f}/{p(-.35):.2f} med {q[n//2]*100:.1f}% peor {min(x[0] for x in out)*100:.1f}")
for sy in (1994,2004):
  print(sy); run2((0.402,0.274,0.268,0.055),start_year=sy); run2((0.493,0,0.274,0.233),start_year=sy); run2((0.402,0.274,0.268,0.055),stop=-0.30,start_year=sy)
