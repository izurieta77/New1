#!/usr/bin/env python3
"""Ficha 15-oct-2026: tres crisis medidas (Nasdaq 2000-02, S&P 500 2007-09, Nasdaq 2021-22).

Para cada caso: pico, valle, caída máxima, días al valle y a recuperar el pico, y qué parte de la
caída habría evitado la salida del filtro vigente (cierre < SMA200 x 0.97, ejecutada al cierre
siguiente) en el índice 1x. Usa los JSON de Yahoo que descarga laboratorio/replicas/R14.py.
Corre: python3 -I conocimiento/fichas/codigo/2026-10-15-crisis-tres-casos.py <ruta de R14-datos>
"""
import json, sys
from datetime import datetime, timezone, date
from pathlib import Path

base = Path(sys.argv[1])
def serie(nombre):
    r = json.loads((base / f"{nombre}.json").read_text())["chart"]["result"][0]
    out = []
    for t, c in zip(r["timestamp"], r["indicators"]["quote"][0]["close"]):
        if c is not None:
            out.append((datetime.fromtimestamp(t, tz=timezone.utc).date(), c))
    return out

CASOS = [("IXIC", date(1999, 6, 1), date(2016, 1, 1), "Nasdaq, burbuja punto com"),
         ("GSPC", date(2007, 1, 1), date(2014, 1, 1), "S&P 500, crisis financiera"),
         ("IXIC", date(2021, 6, 1), date(2025, 1, 1), "Nasdaq, alza de tasas 2022")]
res = []
for nom, ini, fin, etiqueta in CASOS:
    s = serie(nom)
    idx = {d: i for i, (d, _) in enumerate(s)}
    i0 = next(i for i, (d, _) in enumerate(s) if d >= ini)
    i1 = max(i for i, (d, _) in enumerate(s) if d <= fin)
    # pico = máximo antes del valle; valle = mínimo de la ventana
    iv = min(range(i0, i1 + 1), key=lambda i: s[i][1])
    ip = max(range(i0, iv + 1), key=lambda i: s[i][1])
    pico, valle = s[ip][1], s[iv][1]
    mdd = valle / pico - 1
    ir = next((i for i in range(iv, len(s)) if s[i][1] >= pico), None)
    # primera señal de salida del filtro después del pico (SMA200 x 0.97), ejecutada al cierre siguiente
    salida = None
    for i in range(max(ip, 200), iv + 1):
        sma = sum(c for _, c in s[i - 200:i]) / 200 if False else sum(c for _, c in s[i - 199:i + 1]) / 200
        if s[i][1] < sma * 0.97:
            salida = i + 1
            break
    px_salida = s[salida][1]
    evitado = (px_salida - valle) / (pico - valle)  # fracción de la caída (pico->valle) que no se sufrió
    dd_en_salida = px_salida / pico - 1
    r = dict(caso=etiqueta, pico=(str(s[ip][0]), round(pico, 2)), valle=(str(s[iv][0]), round(valle, 2)),
             mdd=round(mdd, 4), dias_al_valle=iv - ip, dias_recuperar=(ir - ip) if ir else None,
             salida=(str(s[salida][0]), round(px_salida, 2)), caida_al_salir=round(dd_en_salida, 4),
             fraccion_evitada=round(evitado, 3))
    res.append(r)
    print(r)

# Aserciones de coherencia (segunda comprobación por construcción)
for r in res:
    assert -1 < r["mdd"] < -0.3, r
    assert r["caida_al_salir"] > r["mdd"]
    assert 0 < r["fraccion_evitada"] < 1
print("Comprobaciones OK")
