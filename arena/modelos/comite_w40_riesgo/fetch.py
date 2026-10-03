import sys,json,pickle
sys.path.insert(0,'/home/user/New1')
from herramientas.datos_historicos import yahoo_historia
out={}
for t in ["^GSPC","^NDX","^VIX","MXN=X","^IRX","UPRO","SPY","QQQ"]:
    h=yahoo_historia(t,"1d",cache_horas=1e6)
    out[t]=dict(zip(h["fechas"],h["precios"]))
    print(t,h["fechas"][0],h["fechas"][-1],len(h["fechas"]))
pickle.dump(out,open("hist.pkl","wb"))
