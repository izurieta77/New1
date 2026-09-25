"""Datos congelados y verificables: manifiesto SHA-256 de los archivos de una replica.

Uso:
  python3 herramientas/huellas.py crear laboratorio/replicas/V01 datos/*.zip ...
  python3 herramientas/huellas.py verificar laboratorio/replicas/V01/SHA256SUMS.txt
El formato es compatible con `sha256sum -c`.
"""
import hashlib
import os
import sys


def sha256(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def crear(directorio, archivos):
    os.makedirs(directorio, exist_ok=True)
    destino = os.path.join(directorio, "SHA256SUMS.txt")
    with open(destino, "w") as f:
        for a in sorted(archivos):
            f.write(f"{sha256(a)}  {os.path.relpath(a, directorio)}\n")
    return destino


def verificar(manifiesto):
    base = os.path.dirname(manifiesto)
    fallas = []
    with open(manifiesto) as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            esperado, ruta = linea.split("  ", 1)
            real = sha256(os.path.join(base, ruta))
            if real != esperado:
                fallas.append(ruta)
    return fallas


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "crear":
        print(crear(sys.argv[2], sys.argv[3:]))
    elif len(sys.argv) == 3 and sys.argv[1] == "verificar":
        f = verificar(sys.argv[2])
        print("OK" if not f else "FALLAN: " + ", ".join(f))
        sys.exit(1 if f else 0)
    else:
        print(__doc__)
        sys.exit(2)
