# FRED rechaza UA de navegador (ver herramientas/datos.py); se usa el UA por defecto de urllib (genérico).
import urllib.request, os, time
D = os.path.dirname(os.path.abspath(__file__))
for s in ["DTB3", "DFEDTARU", "DFEDTAR", "DFF"]:
    for i in range(3):
        try:
            txt = urllib.request.urlopen(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={s}", timeout=90).read().decode()
            break
        except Exception as e:
            print(s, "retry", repr(e)); time.sleep(3)
    open(f"{D}/{s}.csv", "w").write(txt)
    L = txt.strip().splitlines()
    print(s, len(L), L[0], L[1], L[-1])
