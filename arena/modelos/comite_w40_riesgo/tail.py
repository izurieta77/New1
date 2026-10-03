import pickle,datetime as dt,bisect
h=pickle.load(open('hist.pkl','rb')); dx=dict(pickle.load(open('dexmxus.pkl','rb')))
G=h['^GSPC'];N=h['^NDX'];U=h['UPRO'];M=h['MXN=X']
def r(S,a,b): return S[b]/S[a]-1
fk=sorted(dx)
def fx(d): return dx[fk[bisect.bisect_right(fk,d)-1]]
D=dt.date
for nm,a,b in [('16-mar-2020',D(2020,3,13),D(2020,3,16)),('abr-2025 sem',D(2025,4,2),D(2025,4,8))]:
    s,n,u=r(G,a,b),r(N,a,b),r(U,a,b); f=fx(b)/fx(a)-1
    print(nm,'SP %.1f NDX %.1f UPRO %.1f FX %.1f'%(s*100,n*100,u*100,f*100))
    for k,w in {'papel':(0.402,0.274,0.268,0.055),'real Q+U':(0,0.56,0.274,0.166),'real S+U':(0.493,0,0.274,0.233)}.items():
        mx=w[0]*((1+s)*(1+f)-1)+w[1]*((1+n)*(1+f)-1)+w[2]*((1+u)*(1+f)-1)
        us=w[0]*s+w[1]*n+w[2]*u
        print('  ',k,'MXN %.1f%%  USD %.1f%%'%(mx*100,us*100))
