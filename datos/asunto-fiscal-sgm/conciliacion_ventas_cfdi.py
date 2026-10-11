#!/usr/bin/env python3
"""Conciliación de ventas de combustible: CFDI emitidos contra entregas de controles volumétricos.

Uso:
  python3 conciliacion_ventas_cfdi.py --xml CARPETA_XML --volumetricos entregas.csv \
      [--metadata metadata_sat.txt] [--salida reporte.md]

Entradas:
  --xml           carpeta (se recorre completa) con los XML de CFDI 4.0 EMITIDOS por la estación
                  (descarga masiva del SAT).
  --volumetricos  CSV con columnas: mes (AAAA-MM), producto (diesel|regular|premium), litros_entregados
                  Se capturan del reporte mensual de controles volumétricos (Anexo 30/31) de cada mes.
  --metadata      opcional: archivo de metadatos de la descarga masiva (separador "~") con columnas
                  Uuid y Estatus; los CFDI con Estatus 0 (cancelado) se excluyen.

Qué revisa (por mes y producto):
  1. Litros facturados (CFDI de ingreso vigentes menos CFDI de egreso) contra litros entregados.
     Diferencia > +1.5%: se facturó más de lo que salió del dispensario (riesgo de operación inexistente).
     Diferencia < -1.5%: salió más combustible del que se facturó (presunción del art. 111 Bis inciso b CFF).
  2. CFDI nominativos con forma de pago 01 (efectivo) o 99 (por definir): el cliente no puede deducir
     combustible pagado en efectivo (LISR 27 fr. III) y es una señal de revisión.
  3. Litros a público en general (RFC XAXX010101000) contra nominativos, para detectar refacturación
     de tickets sin cancelar el CFDI original.
  4. UUID repetidos.

No modifica ningún archivo de entrada. Es una herramienta de revisión, no un dictamen.
"""
import argparse
import csv
import os
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict

NS = {"cfdi": "http://www.sat.gob.mx/cfd/4", "tfd": "http://www.sat.gob.mx/TimbreFiscalDigital"}

# Claves del catálogo c_ClaveProdServ del SAT. Ajustar si la estación usa otras.
CLAVES = {
    "15101505": "diesel",
    "15101514": "regular",
    "15101515": "premium",
}
GENERICO = "XAXX010101000"
UMBRAL = 0.015


def leer_metadata(ruta):
    cancelados = set()
    if not ruta:
        return cancelados
    with open(ruta, encoding="utf-8", errors="replace") as f:
        filas = csv.reader(f, delimiter="~")
        enc = [c.strip().lower() for c in next(filas)]
        iu, ie = enc.index("uuid"), enc.index("estatus")
        for r in filas:
            if len(r) > max(iu, ie) and r[ie].strip() == "0":
                cancelados.add(r[iu].strip().upper())
    return cancelados


def leer_cfdi(ruta):
    raiz = ET.parse(ruta).getroot()
    tfd = raiz.find(".//tfd:TimbreFiscalDigital", NS)
    uuid = tfd.get("UUID").upper() if tfd is not None else None
    receptor = raiz.find("cfdi:Receptor", NS)
    conceptos = []
    for c in raiz.findall("cfdi:Conceptos/cfdi:Concepto", NS):
        prod = CLAVES.get(c.get("ClaveProdServ"))
        if prod:
            conceptos.append((prod, float(c.get("Cantidad"))))
    return {
        "archivo": os.path.basename(ruta),
        "uuid": uuid,
        "fecha": raiz.get("Fecha", "")[:7],
        "tipo": raiz.get("TipoDeComprobante"),
        "forma_pago": raiz.get("FormaPago", ""),
        "metodo_pago": raiz.get("MetodoPago", ""),
        "rfc_receptor": receptor.get("Rfc") if receptor is not None else "",
        "conceptos": conceptos,
    }


def conciliar(carpeta, ruta_vol, ruta_meta=None):
    cancelados = leer_metadata(ruta_meta)
    facturado = defaultdict(float)
    publico = defaultdict(float)
    nominativo = defaultdict(float)
    efectivo, vistos, repetidos, errores = [], set(), [], []
    for base, _, archivos in os.walk(carpeta):
        for a in sorted(archivos):
            if not a.lower().endswith(".xml"):
                continue
            try:
                d = leer_cfdi(os.path.join(base, a))
            except Exception as e:  # XML dañado o que no es CFDI 4.0
                errores.append((a, str(e)))
                continue
            if d["uuid"] in vistos:
                repetidos.append(d["uuid"])
                continue
            vistos.add(d["uuid"])
            if d["uuid"] in cancelados or d["tipo"] not in ("I", "E"):
                continue
            signo = 1 if d["tipo"] == "I" else -1
            for prod, litros in d["conceptos"]:
                k = (d["fecha"], prod)
                facturado[k] += signo * litros
                (publico if d["rfc_receptor"] == GENERICO else nominativo)[k] += signo * litros
            if (d["tipo"] == "I" and d["rfc_receptor"] != GENERICO and d["conceptos"]
                    and d["forma_pago"] in ("01", "99") and d["metodo_pago"] == "PUE"):
                efectivo.append(d)
    entregas = {}
    with open(ruta_vol, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            entregas[(r["mes"].strip(), r["producto"].strip().lower())] = float(r["litros_entregados"])
    filas = []
    for k in sorted(set(facturado) | set(entregas)):
        fac, ent = facturado.get(k, 0.0), entregas.get(k)
        dif = None if not ent else (fac - ent) / ent
        if dif is None:
            alerta = "SIN DATO VOLUMÉTRICO"
        elif dif > UMBRAL:
            alerta = "FACTURADO > ENTREGADO"
        elif dif < -UMBRAL:
            alerta = "ENTREGADO > FACTURADO (111 Bis b)"
        else:
            alerta = "OK"
        filas.append((k[0], k[1], fac, publico.get(k, 0.0), nominativo.get(k, 0.0), ent, dif, alerta))
    return filas, efectivo, repetidos, errores


def reporte(filas, efectivo, repetidos, errores):
    out = ["# Conciliación de ventas: CFDI emitidos contra entregas volumétricas", "",
           "| Mes | Producto | Litros CFDI | Público general | Nominativos | Entregas volumétricas | Diferencia | Alerta |",
           "|---|---|---:|---:|---:|---:|---:|---|"]
    for m, p, fac, pub, nom, ent, dif, al in filas:
        out.append(f"| {m} | {p} | {fac:,.2f} | {pub:,.2f} | {nom:,.2f} | "
                   f"{'' if ent is None else f'{ent:,.2f}'} | {'' if dif is None else f'{dif:+.2%}'} | {al} |")
    out += ["", f"## CFDI nominativos de combustible pagados en efectivo o 'por definir' (PUE): {len(efectivo)}", ""]
    for d in efectivo[:200]:
        out.append(f"- {d['fecha']} · {d['rfc_receptor']} · forma {d['forma_pago']} · {d['uuid']} · {d['archivo']}")
    out += ["", f"## UUID repetidos en la carpeta: {len(repetidos)}"] + [f"- {u}" for u in repetidos]
    out += ["", f"## Archivos que no se pudieron leer: {len(errores)}"] + [f"- {a}: {e}" for a, e in errores]
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--xml", required=True)
    ap.add_argument("--volumetricos", required=True)
    ap.add_argument("--metadata")
    ap.add_argument("--salida")
    a = ap.parse_args()
    texto = reporte(*conciliar(a.xml, a.volumetricos, a.metadata))
    if a.salida:
        open(a.salida, "w", encoding="utf-8").write(texto)
    sys.stdout.write(texto)


if __name__ == "__main__":
    main()
