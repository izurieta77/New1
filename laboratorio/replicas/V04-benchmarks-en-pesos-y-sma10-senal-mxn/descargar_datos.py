"""V04 - Descarga (con red) de los datos que reproducir.py usa congelados en ./datos.

NO hace falta correrlo para reproducir: los archivos ya estan en datos/ y sus huellas en
SHA256SUMS.txt. Se conserva para documentar de donde salio cada archivo. Si se vuelve a correr,
los archivos cambian (Yahoo, FRED y Banxico actualizan y revisan) y las huellas dejan de coincidir.

Uso (desde la raiz del repo):  python3 laboratorio/replicas/V04-benchmarks-en-pesos-y-sma10-senal-mxn/descargar_datos.py
Solo biblioteca estandar. Descargado originalmente el 2026-09-25.
"""
import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone

AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(AQUI, "datos")
UA = {"User-Agent": "Mozilla/5.0"}
YAHOO = "https://query1.finance.yahoo.com/v8/finance/chart/"
TICKERS = ["SPY", "^SP500TR", "^GSPC", "NAFTRAC.MX", "^MXX", "MXN=X", "SPY.MX", "IVV.MX", "VOO.MX"]
FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv?id="
SERIES_FRED = ["DEXMXUS", "INTGSTMXM193N"]
# Banxico SIE (exportacion CSV publica del cuadro; no requiere token)
BANXICO = "https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?accion=consultarSeries"
SERIES_BANXICO = {  # archivo: (idCuadro, sector, [series])
    "banxico_CF107_cetes28_SF43936.csv": ("CF107", "22", ["SF43936", "SF43935"]),
    "banxico_CF102_fix_SF43718.csv": ("CF102", "6", ["SF43718"]),
}


def bajar(url, datos=None, encabezados=None):
    req = urllib.request.Request(url, data=datos, headers=encabezados or {})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def nombre_yahoo(t):
    return "yahoo_" + t.replace("^", "").replace("=", "_") + "_1d.json"


def main():
    os.makedirs(DATOS, exist_ok=True)
    bitacora = {"descargado_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "archivos": {}}
    for t in TICKERS:
        params = {"period1": -2208988800, "period2": 4102444800, "interval": "1d", "events": "div,split"}
        url = YAHOO + urllib.parse.quote(t, safe="") + "?" + urllib.parse.urlencode(params)
        try:
            contenido = bajar(url, encabezados=UA)
        except Exception as e:  # se registra el fallo; no se inventa el archivo
            bitacora["archivos"][nombre_yahoo(t)] = {"url": url, "error": repr(e)}
            continue
        with open(os.path.join(DATOS, nombre_yahoo(t)), "wb") as f:
            f.write(contenido)
        bitacora["archivos"][nombre_yahoo(t)] = {"url": url}
    for s in SERIES_FRED:
        url = FRED + s
        contenido = bajar(url)
        with open(os.path.join(DATOS, f"fred_{s}.csv"), "wb") as f:
            f.write(contenido)
        bitacora["archivos"][f"fred_{s}.csv"] = {"url": url}
    for archivo, (cuadro, sector, series) in SERIES_BANXICO.items():
        campos = [("idCuadro", cuadro), ("sector", sector), ("version", "3"), ("locale", "es")]
        campos += [("series", s) for s in series]
        campos += [("anoInicial", "1990"), ("anoFinal", "2026"), ("tipoInformacion", "4,1"),
                   ("metadatosWeb", "true"), ("formatoHorizontal", "false"),
                   ("formatoCSV.x", "10"), ("formatoCSV.y", "10")]
        contenido = bajar(BANXICO, urllib.parse.urlencode(campos).encode())
        with open(os.path.join(DATOS, archivo), "wb") as f:
            f.write(contenido)
        bitacora["archivos"][archivo] = {"url": BANXICO, "post": dict((k, v) for k, v in campos if k != "series"),
                                         "series": series}
    with open(os.path.join(DATOS, "bitacora_descarga.json"), "w") as f:
        json.dump(bitacora, f, indent=1, ensure_ascii=False)
    print(json.dumps(bitacora, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
