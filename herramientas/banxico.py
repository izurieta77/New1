"""Series oficiales de Banxico (SIE API) para el marcador y los briefs.

Token: variable de entorno BANXICO_TOKEN (nunca en git). Sin token, las funciones lanzan SinToken y
quien llama debe usar el proxy documentado en competencia/marcador.md.

Uso: python3 herramientas/banxico.py            -> últimas observaciones de las series de abajo
     python3 herramientas/banxico.py SF43936 2026-01-01 2026-09-30   -> rango de una serie (fechas AAAA-MM-DD)
"""
from __future__ import annotations
import json, os, sys, urllib.request
from datetime import date, datetime

BASE = "https://www.banxico.org.mx/SieAPIRest/service/v1/series"
SERIES = {
    "SF43936": "CETES 28 días, tasa de rendimiento en subasta (% anual)",
    "SF61745": "Tasa objetivo de Banxico (% anual)",
    "SF43718": "Tipo de cambio FIX, pesos por dólar",
    "SP30578": "INPC, variación anual (%)",
}


class SinToken(RuntimeError):
    pass


def token() -> str:
    t = os.environ.get("BANXICO_TOKEN", "").strip()
    if not t:
        raise SinToken("Falta BANXICO_TOKEN en el entorno; usa el proxy de CETES documentado en competencia/marcador.md")
    return t


def _fetch(url: str) -> dict:
    req = urllib.request.Request(url, headers={"Bmx-Token": token(), "Accept": "application/json",
                                               "User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def _parsear(payload: dict) -> dict[str, list[tuple[date, float]]]:
    """{id_serie: [(fecha, valor), ...]} ordenado por fecha; omite 'N/E'."""
    salida = {}
    for s in payload.get("bmx", {}).get("series", []):
        filas = []
        for d in s.get("datos", []) or []:
            v = str(d.get("dato", "")).replace(",", "")
            if v in ("", "N/E"):
                continue
            filas.append((datetime.strptime(d["fecha"], "%d/%m/%Y").date(), float(v)))
        salida[s["idSerie"]] = sorted(filas)
    return salida


def oportuno(ids=tuple(SERIES)) -> dict[str, tuple[date, float]]:
    """Última observación de cada serie: {id: (fecha, valor)}."""
    datos = _parsear(_fetch(f"{BASE}/{','.join(ids)}/datos/oportuno"))
    return {k: v[-1] for k, v in datos.items() if v}


def rango(id_serie: str, desde: str, hasta: str) -> list[tuple[date, float]]:
    return _parsear(_fetch(f"{BASE}/{id_serie}/datos/{desde}/{hasta}")).get(id_serie, [])


def cetes28_anual() -> tuple[date, float]:
    """(fecha de subasta, tasa % anual) del CETE a 28 días, la más reciente."""
    return oportuno(("SF43936",))["SF43936"]


def main(argv: list[str]) -> int:
    try:
        if len(argv) == 4:
            for f, v in rango(argv[1], argv[2], argv[3]):
                print(f"{f}\t{v}")
        else:
            for k, (f, v) in oportuno().items():
                print(f"{k}\t{SERIES.get(k, '')}\t{v}\t({f})")
    except SinToken as e:
        print(e, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
