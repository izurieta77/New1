"""Extraccion de texto de los PDF congelados (NO es stdlib: requiere pypdf; se uso pypdf 6.19.0).
Genera los .txt que lee reproducir.py. Se corre una sola vez, desde la raiz del repo:
  python3 laboratorio/replicas/V05-spiva-y-fiscalidad-sic/datos/extraer_texto.py
reproducir.py verifica, si pypdf esta instalado, que la re-extraccion coincide byte a byte con el .txt congelado."""
import glob
import os

AQUI = os.path.dirname(os.path.abspath(__file__))


def extraer(ruta_pdf):
    import pypdf
    r = pypdf.PdfReader(ruta_pdf)
    return "".join(f"\n===== PAGINA {i} =====\n" + (p.extract_text() or "") for i, p in enumerate(r.pages, 1))


if __name__ == "__main__":
    for pdf in sorted(glob.glob(os.path.join(AQUI, "spiva", "*.pdf"))):
        with open(pdf[:-4] + ".txt", "w", encoding="utf-8") as f:
            f.write(extraer(pdf))
        print(pdf)
