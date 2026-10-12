#!/usr/bin/env python3
"""Conciliación de ventas de combustible: CFDI emitidos contra entregas de controles volumétricos.

Uso:
  python3 conciliacion_ventas_cfdi.py --xml CARPETA_XML --volumetricos entregas.csv \
      [--metadata metadata_sat.txt] [--salida reporte.md] [--restar-egresos]

Entradas:
  --xml           carpeta (se recorre completa) con los XML de CFDI 3.3 o 4.0 EMITIDOS por la estación
                  (descarga masiva del SAT).
  --volumetricos  CSV con columnas: mes (AAAA-MM), producto (diesel|regular|premium), litros_entregados
                  Se capturan del reporte mensual de controles volumétricos (Anexo 30/31) de cada mes.
  --metadata      opcional: archivo de metadatos de la descarga masiva (separador "~") con columnas
                  Uuid y Estatus; los CFDI con Estatus 0 (cancelado) se excluyen.

Qué revisa (por mes y producto):
  1. Litros facturados (CFDI de ingreso vigentes) contra litros entregados.
     Facturado > entregado (cualquier exceso arriba de 0.5%, o entregas en 0 con litros facturados):
       se facturó más de lo que salió del dispensario (riesgo de operación inexistente, 69-B / 113 Bis).
     Entregado > facturado en más de 0.5%: determinación presuntiva de ventas (CFF 55 fr. VII f) 1).
     Entregado > facturado en más de 1.5%: además, presunción de procedencia ilícita (CFF 111 Bis b).
     Los CFDI de egreso (notas de crédito) NO restan litros por omisión, porque muchas son solo
     descuentos de precio; sus litros se reportan aparte. Con --restar-egresos sí se restan.
  2. CFDI nominativos con forma de pago 01 (efectivo) o 99 (por definir): el cliente no puede deducir
     combustible pagado en efectivo (LISR 27 fr. III) y es una señal de revisión.
  3. Litros a público en general (RFC XAXX010101000) contra nominativos, para detectar refacturación
     de tickets sin cancelar el CFDI original.
  4. UUID repetidos.
  5. Conceptos sin clave de combustible (p. ej., un CFDI global con clave genérica 01010101): se
     cuentan aparte para que no produzcan una falsa alerta de "entregado > facturado".

Acepta CFDI 3.3 (obligatorio hasta el 31-mar-2023) y 4.0. Un XML que no sea CFDI 3.3 ni 4.0 se
reporta como error y no se cuenta.

No modifica ningún archivo de entrada. Es una herramienta de revisión, no un dictamen.
"""
import argparse
import csv
import os
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict

NS_CFDI = {"http://www.sat.gob.mx/cfd/4", "http://www.sat.gob.mx/cfd/3"}
NS_TFD = "{http://www.sat.gob.mx/TimbreFiscalDigital}TimbreFiscalDigital"

# Claves del catálogo c_ClaveProdServ del SAT. Ajustar si la estación usa otras.
CLAVES = {
    "15101505": "diesel",
    "15101514": "regular",
    "15101515": "premium",
}
GENERICO = "XAXX010101000"
UMBRAL_PRESUNTIVA = 0.005  # CFF 55 fr. VII inciso f) num. 1, líquidos
UMBRAL_111BIS = 0.015      # CFF 111 Bis, párrafo de procedencia ilícita, inciso b), líquidos


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
    ns = raiz.tag[1:].split("}")[0] if raiz.tag.startswith("{") else ""
    if ns not in NS_CFDI or not raiz.tag.endswith("Comprobante"):
        raise ValueError("no es CFDI 3.3 ni 4.0")
    # cfd/3 también es el namespace del CFDI 3.2 (atributo "version" en minúscula, sin ClaveProdServ):
    # se rechaza con error visible en vez de contarlo (conciliación 12-oct-2026).
    if raiz.get("Version") not in ("3.3", "4.0"):
        raise ValueError("versión de CFDI no soportada: %r" % (raiz.get("Version") or raiz.get("version")))
    q = lambda t: "{%s}%s" % (ns, t)
    tfd = raiz.find(".//" + NS_TFD)
    uuid = tfd.get("UUID").upper() if tfd is not None else None
    if not uuid:
        raise ValueError("sin timbre fiscal (UUID)")
    receptor = raiz.find(q("Receptor"))
    conceptos, otros = [], 0
    for c in raiz.findall(q("Conceptos") + "/" + q("Concepto")):
        prod = CLAVES.get(c.get("ClaveProdServ"))
        if prod:
            conceptos.append((prod, float(c.get("Cantidad"))))
        else:
            otros += 1
    return {
        "archivo": os.path.basename(ruta),
        "uuid": uuid,
        "version": raiz.get("Version", ""),
        "fecha": raiz.get("Fecha", "")[:7],
        "tipo": raiz.get("TipoDeComprobante"),
        "forma_pago": raiz.get("FormaPago", ""),
        "metodo_pago": raiz.get("MetodoPago", ""),
        "rfc_receptor": receptor.get("Rfc") if receptor is not None else "",
        "conceptos": conceptos,
        "otros": otros,
    }


def clasificar(fac, ent):
    """Devuelve (diferencia relativa o None, alerta)."""
    if ent is None:
        return None, "SIN DATO VOLUMÉTRICO"
    if ent == 0:
        return None, ("FACTURADO > ENTREGADO (entregas en 0)" if fac > 0 else "OK")
    dif = (fac - ent) / ent
    if dif > UMBRAL_PRESUNTIVA:
        return dif, "FACTURADO > ENTREGADO"
    if dif < -UMBRAL_111BIS:
        return dif, "ENTREGADO > FACTURADO > 1.5% (55 VII y 111 Bis b)"
    if dif < -UMBRAL_PRESUNTIVA:
        return dif, "ENTREGADO > FACTURADO > 0.5% (55 VII f)"
    return dif, "OK"


def conciliar(carpeta, ruta_vol, ruta_meta=None, restar_egresos=False):
    cancelados = leer_metadata(ruta_meta)
    facturado = defaultdict(float)
    publico = defaultdict(float)
    nominativo = defaultdict(float)
    egresos = defaultdict(float)
    sin_clave = defaultdict(int)
    efectivo, vistos, repetidos, errores = [], set(), [], []
    for base, _, archivos in os.walk(carpeta):
        for a in sorted(archivos):
            if not a.lower().endswith(".xml"):
                continue
            try:
                d = leer_cfdi(os.path.join(base, a))
            except Exception as e:  # XML dañado, sin timbre o que no es CFDI 3.3/4.0
                errores.append((a, str(e)))
                continue
            if d["uuid"] in vistos:
                repetidos.append(d["uuid"])
                continue
            vistos.add(d["uuid"])
            if d["uuid"] in cancelados or d["tipo"] not in ("I", "E"):
                continue
            if d["otros"]:
                sin_clave[d["fecha"]] += d["otros"]
            for prod, litros in d["conceptos"]:
                k = (d["fecha"], prod)
                if d["tipo"] == "E":
                    egresos[k] += litros
                    if not restar_egresos:
                        continue
                    litros = -litros
                facturado[k] += litros
                (publico if d["rfc_receptor"] == GENERICO else nominativo)[k] += litros
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
        dif, alerta = clasificar(fac, ent)
        filas.append((k[0], k[1], fac, publico.get(k, 0.0), nominativo.get(k, 0.0),
                      egresos.get(k, 0.0), ent, dif, alerta))
    return filas, efectivo, repetidos, errores, dict(sin_clave)


def reporte(filas, efectivo, repetidos, errores, sin_clave):
    out = ["# Conciliación de ventas: CFDI emitidos contra entregas volumétricas", "",
           "Umbrales (líquidos): 0.5% = determinación presuntiva (CFF 55 fr. VII f); "
           "1.5% = presunción de procedencia ilícita (CFF 111 Bis b). Revisión, no dictamen.", "",
           "| Mes | Producto | Litros CFDI | Público general | Nominativos | Litros en egresos | "
           "Entregas volumétricas | Diferencia | Alerta |",
           "|---|---|---:|---:|---:|---:|---:|---:|---|"]
    for m, p, fac, pub, nom, egr, ent, dif, al in filas:
        out.append(f"| {m} | {p} | {fac:,.2f} | {pub:,.2f} | {nom:,.2f} | {egr:,.2f} | "
                   f"{'' if ent is None else f'{ent:,.2f}'} | {'' if dif is None else f'{dif:+.2%}'} | {al} |")
    if sin_clave:
        out += ["", "## Conceptos sin clave de combustible (no se sumaron a los litros; revisar si son "
                "globales con clave genérica)", ""]
        out += [f"- {m}: {n} conceptos" for m, n in sorted(sin_clave.items())]
    out += ["", f"## CFDI nominativos de combustible pagados en efectivo o 'por definir' (PUE): {len(efectivo)}", ""]
    for d in efectivo[:200]:
        out.append(f"- {d['fecha']} · {d['rfc_receptor']} · forma {d['forma_pago']} · {d['uuid']} · {d['archivo']}")
    out += ["", f"## UUID repetidos en la carpeta: {len(repetidos)}"] + [f"- {u}" for u in repetidos]
    out += ["", f"## Archivos que no se pudieron leer o no son CFDI 3.3/4.0: {len(errores)}"]
    out += [f"- {a}: {e}" for a, e in errores]
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--xml", required=True)
    ap.add_argument("--volumetricos", required=True)
    ap.add_argument("--metadata")
    ap.add_argument("--salida")
    ap.add_argument("--restar-egresos", action="store_true",
                    help="restar los litros de CFDI de egreso (solo si son devoluciones de producto)")
    a = ap.parse_args()
    texto = reporte(*conciliar(a.xml, a.volumetricos, a.metadata, a.restar_egresos))
    if a.salida:
        open(a.salida, "w", encoding="utf-8").write(texto)
    sys.stdout.write(texto)


if __name__ == "__main__":
    main()
