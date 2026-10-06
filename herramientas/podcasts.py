"""Lector de feeds de podcasts: episodios nuevos, transcripciones del feed y palabras clave.

Solo biblioteca estandar. No resume ni interpreta: lista los episodios recientes de
`datos/podcasts-feeds.csv`, baja la transcripcion cuando el feed la publica (etiqueta
`podcast:transcript`) a `datos/cache/podcasts/` (fuera de git) y cuenta palabras clave.
El resumen y la verificacion los hace el agente de inteligencia (rutinas/inteligencia.md).

Uso:
    python3 herramientas/podcasts.py --dias 3
    python3 herramientas/podcasts.py --dias 3 --salida bitacora/inteligencia/podcasts-AAAA-MM-DD.md
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from herramientas import datos
from herramientas.parametros import DIR_CACHE

RAIZ = Path(__file__).resolve().parent.parent
RUTA_FEEDS = RAIZ / "datos" / "podcasts-feeds.csv"
NS_PODCAST = "https://podcastindex.org/namespace/1.0"
PALABRAS_CLAVE = [
    "Fed", "Treasury", "yield", "inflation", "tariff", "Iran", "Hormuz", "oil", "natural gas", "LNG",
    "data center", "Nvidia", "bitcoin", "ether", "ETF", "peso", "Banxico", "SAT", "recession",
    "default", "debt", "earnings", "dilution", "buyback", "credit", "volatility",
]
SENSIBLES_A_MAYUSCULAS = {"Fed", "SAT", "ETF", "LNG"}  # "fed" y "sat" existen como palabras comunes
PREFERENCIA_FORMATO = ("text/plain", "application/srt", "text/vtt", "text/html")


def _texto(el) -> str:
    return (el.text or "").strip() if el is not None else ""


def limpiar_html(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", html.unescape(s or ""))
    return re.sub(r"\s+", " ", s).strip()


def parsear_feed(xml_texto: str) -> list[dict]:
    """Lista de episodios [{titulo, fecha (UTC), descripcion, enlace, transcripciones {tipo: url}}]."""
    raiz = ET.fromstring(xml_texto)
    episodios = []
    for it in raiz.iter("item"):
        fecha_txt = _texto(it.find("pubDate"))
        try:
            fecha = parsedate_to_datetime(fecha_txt)
            fecha = fecha.astimezone(timezone.utc) if fecha.tzinfo else fecha.replace(tzinfo=timezone.utc)
        except (TypeError, ValueError):
            continue
        trans = {}
        for t in it.findall(f"{{{NS_PODCAST}}}transcript"):
            url, tipo = t.get("url"), (t.get("type") or "").lower()
            if url and tipo and tipo not in trans:
                trans[tipo] = html.unescape(url)
        episodios.append({
            "titulo": limpiar_html(_texto(it.find("title"))),
            "fecha": fecha,
            "descripcion": limpiar_html(_texto(it.find("description"))),
            "enlace": _texto(it.find("link")),
            "transcripciones": trans,
        })
    episodios.sort(key=lambda e: e["fecha"], reverse=True)
    return episodios


def texto_de_transcripcion(crudo: str) -> str:
    """Quita marcas de tiempo, numeracion SRT/VTT y encabezados; deja solo el texto."""
    lineas = []
    for l in crudo.splitlines():
        l = l.strip()
        if not l or l == "WEBVTT" or re.fullmatch(r"\d+", l):
            continue
        if re.fullmatch(r"[\d:.,]+(\s*-->\s*[\d:.,]+.*)?", l):
            continue
        lineas.append(l)
    return " ".join(lineas)


def contar_palabras_clave(texto: str, palabras=PALABRAS_CLAVE) -> dict[str, int]:
    bajo = texto.lower()
    out = {}
    for p in palabras:
        if p in SENSIBLES_A_MAYUSCULAS:
            n = len(re.findall(r"(?<![A-Za-z])" + re.escape(p) + r"(?![A-Za-z])", texto))
        else:
            n = len(re.findall(r"(?<![a-z])" + re.escape(p.lower()) + r"(?![a-z])", bajo))
        if n:
            out[p] = n
    return dict(sorted(out.items(), key=lambda kv: -kv[1]))


def elegir_transcripcion(trans: dict) -> tuple[str, str] | None:
    for tipo in PREFERENCIA_FORMATO:
        if tipo in trans:
            return tipo, trans[tipo]
    return next(iter(trans.items())) if trans else None


def cargar_feeds(ruta: Path = RUTA_FEEDS) -> list[dict]:
    with open(ruta, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def slug(nombre: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", nombre.lower()).strip("-")


def procesar(dias: int, bajar: bool = True, ahora: datetime | None = None) -> list[dict]:
    ahora = ahora or datetime.now(timezone.utc)
    corte = ahora - timedelta(days=dias)
    filas = []
    for fd in cargar_feeds():
        try:
            eps = parsear_feed(datos.descargar(fd["feed_url"], datos.UA_NAVEGADOR, cache_horas=0.5))
        except Exception as e:  # feed caido: se reporta y se sigue
            filas.append({"programa": fd["nombre"], "error": str(e)[:120]})
            continue
        for ep in eps:
            if ep["fecha"] < corte:
                break
            fila = {"programa": fd["nombre"], "idioma": fd["idioma"], "titulo": ep["titulo"], "fecha": ep["fecha"],
                    "enlace": ep["enlace"], "descripcion": ep["descripcion"][:280], "transcripcion": "no",
                    "caracteres": 0, "palabras_clave": {}, "archivo": ""}
            elegido = elegir_transcripcion(ep["transcripciones"])
            if elegido and bajar:
                tipo, url = elegido
                try:
                    texto = texto_de_transcripcion(datos.descargar(url, datos.UA_NAVEGADOR, timeout=60, cache_horas=24))
                    carpeta = DIR_CACHE / "podcasts" / slug(fd["nombre"])
                    carpeta.mkdir(parents=True, exist_ok=True)
                    ruta = carpeta / f"{ep['fecha']:%Y-%m-%d}-{hashlib.sha1(ep['titulo'].encode()).hexdigest()[:8]}.txt"
                    ruta.write_text(texto, encoding="utf-8")
                    fila.update(transcripcion=f"si ({tipo})", caracteres=len(texto),
                                palabras_clave=contar_palabras_clave(texto), archivo=str(ruta.relative_to(RAIZ)))
                except Exception as e:
                    fila["transcripcion"] = f"fallo ({str(e)[:60]})"
            elif elegido:
                fila["transcripcion"] = f"disponible ({elegido[0]})"
            filas.append(fila)
    return filas


def a_markdown(filas: list[dict], dias: int) -> str:
    sal = [f"# Podcasts: episodios de los últimos {dias} días", "",
           "> Generado por `herramientas/podcasts.py`. Metadatos y palabras clave; el resumen y la verificación los hace el agente de inteligencia. Las transcripciones quedan en `datos/cache/podcasts/` (fuera de git).", ""]
    ok = [f for f in filas if "error" not in f]
    err = [f for f in filas if "error" in f]
    sal += ["| Programa | Episodio | Fecha (UTC) | Transcripción | Caracteres | Palabras clave (veces) |", "|---|---|---|---|---|---|"]
    for f in ok:
        kw = ", ".join(f"{k} {v}" for k, v in list(f["palabras_clave"].items())[:8])
        sal.append(f"| {f['programa']} | {f['titulo'][:90].replace('|', '/')} | {f['fecha']:%Y-%m-%d %H:%M} | {f['transcripcion']} | {f['caracteres']:,} | {kw} |")
    if not ok:
        sal.append("| (sin episodios nuevos) | | | | | |")
    for f in err:
        sal.append(f"\nFeed con error: {f['programa']}: {f['error']}")
    return "\n".join(sal) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dias", type=int, default=3)
    ap.add_argument("--sin-transcripciones", action="store_true", help="solo lista los episodios")
    ap.add_argument("--salida", help="escribe el resumen en este archivo markdown")
    a = ap.parse_args(argv)
    filas = procesar(a.dias, bajar=not a.sin_transcripciones)
    md = a_markdown(filas, a.dias)
    if a.salida:
        Path(a.salida).write_text(md, encoding="utf-8")
        print(f"Escrito {a.salida}")
    print(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
