#!/usr/bin/env python3
"""Paso de preparación de datos (no es estadística).

Convierte la hoja 'Data' de ie_data.xls (Robert Shiller, descargada de
econ.yale.edu/~shiller/data/ie_data.xls) a un CSV mensual simple.

Este paso necesita xlrd, que NO está en la biblioteca estándar. Es el único
componente fuera de la biblioteca estándar de esta auditoría. Las
estadísticas (ac15_r04_independiente.py) solo leen el CSV generado aquí.

Verificación incluida: el código año.mes de Shiller (p. ej. 1871.10 = octubre)
se contrasta con la columna 'Date Fraction' de la misma hoja.

Uso:
    PYTHONPATH=/ruta/a/pylib python3 convertir_shiller_xls.py
"""
import csv
import os

import xlrd

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, "datos_crudos")
SRC = os.path.join(RAW, "shiller_ie_data.xls")
DST = os.path.join(RAW, "shiller_mensual.csv")


def a_numero(v):
    return float(v) if isinstance(v, float) else None


def main():
    libro = xlrd.open_workbook(SRC)
    hoja = libro.sheet_by_name("Data")
    filas = []
    mismatch = 0
    for r in range(hoja.nrows):
        codigo = a_numero(hoja.cell_value(r, 0))
        if codigo is None:
            continue
        anio = int(codigo + 1e-9)
        mes = int(round((codigo - anio) * 100))
        if not (1 <= mes <= 12):
            raise ValueError(f"fila {r}: mes fuera de rango en {codigo}")
        frac = a_numero(hoja.cell_value(r, 5))
        if frac is not None:
            mes_frac = int((frac - int(frac)) * 12 + 1e-9) + 1
            if mes_frac != mes:
                mismatch += 1
        P = a_numero(hoja.cell_value(r, 1))
        D = a_numero(hoja.cell_value(r, 2))
        GS10 = a_numero(hoja.cell_value(r, 6))
        filas.append((anio, mes, P, D, GS10))

    with open(DST, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["anio", "mes", "P", "D", "GS10"])
        for anio, mes, P, D, GS10 in filas:
            w.writerow([anio, mes,
                        "" if P is None else P,
                        "" if D is None else D,
                        "" if GS10 is None else GS10])
    print(f"filas escritas: {len(filas)}; primera {filas[0][0]}-{filas[0][1]:02d}; "
          f"ultima {filas[-1][0]}-{filas[-1][1]:02d}")
    print(f"discrepancias codigo vs fecha fraccional: {mismatch}")


if __name__ == "__main__":
    main()
