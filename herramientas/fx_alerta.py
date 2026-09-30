"""Regla FX-1: alerta cambiaria USD/MXN en las dos direcciones (30-sep-2026).

No ordena comprar ni vender: informa y pide revision. Nace de que el dolar paso de 16.87 (4-sep) a
18.07 (FIX del 29-sep) sin que ninguna regla lo convirtiera en alerta.

Fuentes, en orden de preferencia:
- spot: Yahoo MXN=X (chart v8, intervalo 1m, User-Agent de navegador); si falla, Binance USDT/MXN.
- referencia diaria: FIX de Banxico (SF43718, herramientas/banxico.py) si hay BANXICO_TOKEN; sin token,
  cierres diarios de Yahoo MXN=X (range=3mo, interval=1d); si Yahoo falla, cierres diarios de Binance
  USDT/MXN (base de 0.1-0.25% frente al USD/MXN). Nunca maximos ni minimos diarios. La fuente usada
  queda escrita en la salida, y si la referencia mas reciente no es la del dia habil anterior, una nota.
"Hoy" es la fecha de la Ciudad de Mexico (el decisor y el vigia corren de noche, ya en otro dia UTC).

Calculo (la referencia es una serie de dias habiles; "anteriores" = fechas estrictamente antes de hoy):
    sd  = desviacion estandar muestral de los ultimos 20 rendimientos logaritmicos de la referencia
    D1  = spot / referencia del dia habil anterior - 1
    D10 = spot / referencia de hace 10 dias habiles - 1
    episodio = (referencia de hoy, o spot) / minimo (y / maximo) de las 15 referencias anteriores - 1
Niveles:
    AVISO  si |D1| >= max(1.0%, 2 sd)  o  |D10| >= max(3.0%, 2 sd raiz(10))
    ALERTA si |D10| >= max(4.5%, 3 sd raiz(10))  o  episodio >= +6%  o  <= -6%
Supresion: una alerta de la misma direccion y del mismo nivel (o de uno mayor) no se repite durante
10 dias habiles, salvo que el USD/MXN se aleje otro sd raiz(10) (log, sd de hoy) del nivel en que se
aviso. El estado vive en bitacora/supervision/estado-fx.json; solo lo escribe la supervision (rutina 9)
o `--registrar`. Un estado ilegible o con forma invalida se ignora con una nota (no tumba la supervision).

Dos desviaciones deliberadas de la especificacion literal ("mismo nivel y misma direccion"; "salvo que el
movimiento se amplie 1 sd raiz(10) mas"):
  1. una ALERTA vigente tambien calla los AVISOS de su misma direccion (un AVISO nunca calla una ALERTA);
     con la regla literal, el dia despues de una ALERTA saldria un AVISO de lo mismo;
  2. la ampliacion se mide sobre el nivel del USD/MXN en que se aviso, con el sd de hoy (D10 es una
     ventana movil: su "movimiento" cambia de base cada dia).
Calibracion con datos reales (corrida del 30-sep-2026; en la historia el spot de cada dia es la referencia
de ese dia):
  - septiembre de 2026, FIX: AVISO el 23-sep (D1 +1.16%, D10 +3.44%), suprimidas el 24 y el 25, ALERTA el
    28-sep (D10 +5.13%), suprimidas el 29 y el 30. Con cierres de Yahoo: AVISO el 23 (D10 +3.85%) y ALERTA
    el 28 (D10 +4.97%).
  - 5 anios (oct-2021 a sep-2026), FIX: 56 AVISOS y 11 ALERTAS (35 y 10 al alza); con la supresion
    literal, 60 y 11. Con cierres de Yahoo: 68 y 10. La especificacion esperaba ~36 y ~8, que no sale con
    ninguna variante (lo mas cercano: 35 AVISOS al alza con el FIX).
  - la frase para el dueno usa el efecto real (lotes_usd / efecto_cambiario): lo que se compro con el dolar
    ya movido no cuenta el movimiento de toda la ventana. Sin lotes, solo dice la exposicion de hoy.

Uso:
    python3 herramientas/fx_alerta.py              # estado FX-1 de este momento (solo lectura)
    python3 herramientas/fx_alerta.py --brief      # linea "Tipo de cambio" del brief: efecto de precio y
                                                   # efecto cambiario por cuenta (solo lectura)
    python3 herramientas/fx_alerta.py --registrar  # como el primero, pero si dispara guarda el estado de
                                                   # supresion al final (solo si tu rutina avisa esa alerta)
"""
from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
import urllib.parse
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Callable

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from herramientas import banxico, datos
from herramientas.parametros import DIR_BITACORA

try:
    from zoneinfo import ZoneInfo
    ZONA_LOCAL = ZoneInfo("America/Mexico_City")
except Exception:  # noqa: BLE001 - sin base tzdata: Mexico no tiene horario de verano desde 2022
    ZONA_LOCAL = timezone(timedelta(hours=-6))

OK, AVISO, ALERTA = 0, 1, 2          # mismos codigos que herramientas/supervision.py
NOMBRE = {OK: "OK", AVISO: "AVISO", ALERTA: "ALERTA"}

TICKER = "MXN=X"
SERIE_FIX = "SF43718"
PAR_BINANCE = "USDTMXN"
URL_BINANCE = "https://data-api.binance.vision/api/v3/"
NOTA_BINANCE = "USDT/MXN trae una base de 0.1-0.25% frente al USD/MXN"

N_SIGMA = 20                 # rendimientos para sd
N_D10 = 10                   # dias habiles de D10
N_EPISODIO = 15              # referencias anteriores del episodio
AVISO_D1, AVISO_D10, ALERTA_D10, EPISODIO = 0.010, 0.030, 0.045, 0.060
K_AVISO, K_ALERTA = 2.0, 3.0
DIAS_SUPRESION = 10          # dias habiles
RUTA_ESTADO = DIR_BITACORA / "supervision" / "estado-fx.json"
LIBROS_DUENO = ("real", "real-binance")   # "tu dinero" en la frase para el dueno
MESES = ("ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic")

Serie = list[tuple[date, float]]


class ErrorFX(Exception):
    """Sin datos suficientes para evaluar FX-1."""


# ---------------------------------------------------------------- calendario y formato

def fecha_local(ahora: datetime) -> date:
    """Fecha en la Ciudad de Mexico: a las 19:27 CDMX (01:27 UTC del dia siguiente) sigue siendo hoy."""
    return ahora.astimezone(ZONA_LOCAL).date()


def es_habil(d: date) -> bool:
    return d.weekday() < 5


def dia_habil_anterior(d: date) -> date:
    d -= timedelta(days=1)
    while not es_habil(d):
        d -= timedelta(days=1)
    return d


def dias_habiles(desde: date, hasta: date) -> int:
    """Dias habiles (lunes a viernes) en (desde, hasta]."""
    n, d = 0, desde
    while d < hasta:
        d += timedelta(days=1)
        n += es_habil(d)
    return n


def sumar_habiles(d: date, n: int) -> date:
    while n > 0:
        d += timedelta(days=1)
        n -= es_habil(d)
    return d


def fecha_corta(d: date) -> str:
    return f"{d.day}-{MESES[d.month - 1]}"


def proximo_viernes(d: date) -> date:
    return d + timedelta(days=(4 - d.weekday()) % 7)


def _pct(x: float, dec: int = 2) -> str:
    return f"{x * 100:+.{dec}f}%".replace("-", "−")


def _mxn(x: float) -> str:
    return f"{x:,.0f}"


def _valor_en(referencia: Serie, fecha: date, respaldo: float) -> float:
    """Referencia en la fecha o la anterior mas cercana; 'respaldo' si no hay ninguna."""
    p = datos.valor_en_o_antes(referencia, fecha)
    return p[1] if p else respaldo


# ---------------------------------------------------------------- regla (funciones puras)

def _direccion(x: float) -> str:
    return "sube" if x > 0 else "baja"


def evaluar(referencia: Serie, spot: float, hoy: date) -> dict:
    """Mide D1, D10, sd y el episodio, y lista los candidatos a AVISO/ALERTA (antes de la supresion).

    referencia: [(fecha, valor)] ordenada, un punto por dia habil; se usan las fechas < hoy
    (y la de hoy, si existe, solo para el episodio). spot: USD/MXN de este momento.
    Cada candidato trae 'base' = (fecha, valor) desde donde se mide su movimiento.
    """
    previa = [(f, v) for f, v in referencia if f < hoy]
    if len(previa) < N_SIGMA + 1:
        raise ErrorFX(f"referencia insuficiente: {len(previa)} observaciones antes de {hoy} "
                      f"(se necesitan {N_SIGMA + 1})")
    valores = [v for _, v in previa]
    rend = [math.log(b / a) for a, b in zip(valores[-N_SIGMA - 1:-1], valores[-N_SIGMA:])]
    sigma = statistics.stdev(rend)
    s10 = sigma * math.sqrt(N_D10)
    d1 = spot / valores[-1] - 1
    d10 = spot / valores[-N_D10] - 1
    ref_hoy = next((v for f, v in referencia if f == hoy), None)
    x = ref_hoy if ref_hoy is not None else spot
    ventana = previa[-N_EPISODIO:]
    i_min = min(range(len(ventana)), key=lambda i: ventana[i][1])
    i_max = max(range(len(ventana)), key=lambda i: ventana[i][1])
    ep_sube, ep_baja = x / ventana[i_min][1] - 1, x / ventana[i_max][1] - 1
    umbral = {"aviso_d1": max(AVISO_D1, K_AVISO * sigma), "aviso_d10": max(AVISO_D10, K_AVISO * s10),
              "alerta_d10": max(ALERTA_D10, K_ALERTA * s10), "episodio": EPISODIO}
    cand = []  # en orden de prioridad: el primero de cada (nivel, direccion) es el motivo que se reporta

    def agrega(nivel, cambio, motivo, u, dias, base):
        cand.append({"nivel": nivel, "direccion": _direccion(cambio), "motivo": motivo, "cambio": cambio,
                     "umbral": u, "dias": dias, "base": base})
    if abs(d10) >= umbral["alerta_d10"]:
        agrega(ALERTA, d10, "Δ10", umbral["alerta_d10"], N_D10, previa[-N_D10])
    episodios = [(ep, len(ventana) - i, ventana[i]) for ep, i, ok in ((ep_sube, i_min, ep_sube >= EPISODIO),
                                                                      (ep_baja, i_max, ep_baja <= -EPISODIO)) if ok]
    for ep, dias, base in sorted(episodios, key=lambda p: -abs(p[0])):  # ambos solo en un vaivén de >12%
        agrega(ALERTA, ep, "episodio", EPISODIO, dias, base)
    if abs(d10) >= umbral["aviso_d10"]:
        agrega(AVISO, d10, "Δ10", umbral["aviso_d10"], N_D10, previa[-N_D10])
    if abs(d1) >= umbral["aviso_d1"]:
        agrega(AVISO, d1, "Δ1", umbral["aviso_d1"], 1, previa[-1])
    return {"hoy": hoy, "spot": spot, "x_episodio": x, "ref_hoy": ref_hoy, "d1": d1, "d10": d10,
            "sigma": sigma, "sigma10": s10, "ref1": previa[-1], "ref10": previa[-N_D10],
            "ep_sube": ep_sube, "ep_baja": ep_baja, "min15": ventana[i_min], "max15": ventana[i_max],
            "umbral": umbral, "candidatos": cand}


def registros_vigentes(estado: dict, hoy: date) -> dict:
    """Registros de alertas emitidas hace menos de 10 dias habiles (estado ya validado)."""
    return {k: r for k, r in (estado.get("registros") or {}).items()
            if dias_habiles(date.fromisoformat(r["fecha"]), hoy) < DIAS_SUPRESION}


def _bloqueo(cand: dict, vigentes: dict, spot: float, sigma10: float) -> dict | None:
    """Registro que suprime al candidato: misma direccion, nivel igual o mayor, y el USD/MXN no se ha
    alejado otro sd raiz(10) (sd de hoy, log) desde el nivel en que se aviso."""
    signo = 1 if cand["direccion"] == "sube" else -1
    for r in vigentes.values():
        if r["direccion"] == cand["direccion"] and r["nivel"] >= cand["nivel"] \
                and signo * math.log(spot / r["usdmxn"]) < sigma10:
            return r
    return None


def decidir(ev: dict, estado: dict) -> dict:
    """Aplica la supresion. Devuelve {'disparo': candidato | None, 'suprimidos': [(cand, registro)],
    'estado': estado nuevo (con el disparo registrado)}."""
    hoy = ev["hoy"]
    vigentes = registros_vigentes(estado, hoy)
    suprimidos, disparo = [], None
    for c in ev["candidatos"]:  # ya vienen de ALERTA a AVISO
        r = _bloqueo(c, vigentes, ev["spot"], ev["sigma10"])
        if r is None:
            disparo = c
            break
        if not any(s[0]["nivel"] == c["nivel"] and s[0]["direccion"] == c["direccion"] for s in suprimidos):
            suprimidos.append((c, r))
    nuevo = {"regla": "FX-1", "registros": dict(vigentes)}
    if disparo is not None:
        nuevo["registros"][f"{NOMBRE[disparo['nivel']]}:{disparo['direccion']}"] = {
            "fecha": hoy.isoformat(), "nivel": disparo["nivel"], "direccion": disparo["direccion"],
            "usdmxn": round(ev["spot"], 6), "sigma10": round(ev["sigma10"], 6),
            "motivo": f"{disparo['motivo']} {_pct(disparo['cambio'])}"}
    return {"disparo": disparo, "suprimidos": suprimidos, "estado": nuevo}


def validar_estado(crudo, nombre: str = "estado-fx.json") -> tuple[dict, list[str]]:
    """(estado limpio, notas). Descarta lo que no tenga la forma que escribe decidir()."""
    if not isinstance(crudo, dict) or not isinstance(crudo.get("registros", {}), dict):
        return {}, [f"{nombre} con forma inválida ({type(crudo).__name__}): se ignora y la supresión "
                    f"arranca de cero"]
    registros, malos = {}, []
    for k, r in (crudo.get("registros") or {}).items():
        try:
            limpio = {**r, "fecha": date.fromisoformat(r["fecha"]).isoformat(), "nivel": int(r["nivel"]),
                      "direccion": str(r["direccion"]), "usdmxn": float(r["usdmxn"])}
            valido = limpio["nivel"] in (AVISO, ALERTA) and limpio["direccion"] in ("sube", "baja") \
                and limpio["usdmxn"] > 0
        except (KeyError, TypeError, ValueError):
            valido = False
        if valido:
            registros[str(k)] = limpio
        else:
            malos.append(str(k))
    notas = [f"{nombre}: registro(s) inválido(s) descartado(s): {', '.join(malos)}"] if malos else []
    return {"regla": "FX-1", "registros": registros}, notas


def leer_estado(ruta: Path | None) -> tuple[dict, list[str]]:
    """(estado, notas). Nunca lanza: un archivo ilegible o mal formado se ignora con una nota."""
    if ruta is None or not ruta.exists():
        return {}, []
    try:
        crudo = json.loads(ruta.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        return {}, [f"{ruta.name} ilegible ({type(e).__name__}): se ignora y la supresión arranca de cero"]
    return validar_estado(crudo, ruta.name)


def guardar_estado(ruta: Path, estado: dict) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(estado, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- efecto en pesos

def parte_usd(filas: list[dict]) -> float:
    """Valor en MXN de las posiciones que cotizan en USD (filas de portafolio.valuar_libro)."""
    return sum(f["valor_mxn"] for f in filas if f.get("moneda") == "USD")


def lotes_usd(operaciones: list[dict], filas: list[dict]) -> list[dict]:
    """Lotes vigentes (PEPS) de lo que cotiza en USD: [{'ticker','fecha','cantidad','precio','fx_compra'}].

    operaciones: portafolio.leer_operaciones (en orden). filas: [{'ticker','moneda','precio'}] con el
    precio de hoy en USD (filas de valuar_libro); sin precio, la posicion no entra. fx_compra: el
    tipo_cambio de la operacion si es en USD y lo trae; si no (p. ej. BTC comprado en MXN), None.
    """
    cotiza = {f["ticker"]: f["precio"] for f in filas if f.get("moneda") == "USD" and f.get("precio") is not None}
    abiertos: dict[str, list[dict]] = {}
    for op in operaciones:
        t = op.get("ticker")
        if op["lado"] == "compra":
            fx_op = op.get("tipo_cambio") if op.get("moneda") == "USD" else None
            abiertos.setdefault(t, []).append({"ticker": t, "fecha": op["fecha"], "cantidad": op["cantidad"],
                                               "fx_compra": fx_op or None})
        elif op["lado"] == "venta":
            q = op["cantidad"]
            for lote in abiertos.get(t, []):
                usar = min(q, lote["cantidad"])
                lote["cantidad"] -= usar
                q -= usar
                if q <= 1e-12:
                    break
            abiertos[t] = [x for x in abiertos.get(t, []) if x["cantidad"] > 1e-12]
    return [{**x, "precio": cotiza[t]} for t, ls in sorted(abiertos.items()) if t in cotiza for x in ls]


def efecto_cambiario(lotes: list[dict], referencia: Serie, base: tuple[date, float], spot: float,
                     hoy: date) -> float:
    """MXN que el movimiento del USD/MXN desde 'base' = (fecha, valor) le sumo a lo que de verdad se
    tenia en dolares: suma de q p_hoy (spot - fx_ini), con fx_ini = el valor de la base si el lote ya
    estaba, o el tipo de cambio de la compra si entro despues (el de la operacion; si no lo trae, la
    referencia de su fecha; si se compro hoy sin referencia de hoy, el spot, o sea efecto cero)."""
    fb, vb = base
    ref_hoy = next((v for f, v in referencia if f == hoy), None)
    total = 0.0
    for x in lotes:
        if x["fecha"] <= fb:
            fx_ini = vb
        elif x.get("fx_compra"):
            fx_ini = x["fx_compra"]
        elif x["fecha"] >= hoy:
            fx_ini = ref_hoy if ref_hoy is not None else spot
        else:
            fx_ini = _valor_en(referencia, x["fecha"], vb)
        total += x["cantidad"] * x["precio"] * (spot - fx_ini)
    return total


def efecto_movimiento(parte_usd_mxn: float, cambio: float) -> float:
    """MXN que un cambio ya ocurrido le habria sumado a una parte en USD que se tuvo toda la ventana."""
    return parte_usd_mxn * cambio / (1 + cambio)


def descomponer(posiciones: list[dict], fx0: float, fx1: float) -> dict:
    """Separa el cambio de valor en MXN en efecto de precio y efecto cambiario.

    posiciones: [{'cantidad', 'p0', 'p1', 'moneda'[, 'fx0']}]; 'fx0' de la posicion (el USD/MXN de la
    fecha de p0) manda sobre el argumento, para que precio y cambio cubran la misma ventana.
    precio = q (p1 - p0) fx0; cambio = q p1 (fx1 - fx0) para lo que cotiza en USD; su suma es el
    cambio total exacto de (p0, fx0) a (p1, fx1).
    """
    precio = cambio = 0.0
    for p in posiciones:
        fx_a, fx_b = (p.get("fx0", fx0), fx1) if p["moneda"] == "USD" else (1.0, 1.0)
        precio += p["cantidad"] * (p["p1"] - p["p0"]) * fx_a
        cambio += p["cantidad"] * p["p1"] * (fx_b - fx_a)
    return {"precio": precio, "cambio": cambio, "total": precio + cambio}


def texto_por_uno(expos: dict[str, float | None]) -> str:
    """'papel ±102 MXN; real sin libro valuado; ...' por cada 1% del USD/MXN."""
    partes = [f"{n} ±{_mxn(v * 0.01)} MXN" if v is not None else f"{n} sin libro valuado"
              for n, v in expos.items()]
    total = sum(v for v in expos.values() if v is not None)
    return "; ".join(partes + [f"total ±{_mxn(total * 0.01)} MXN"]) if partes else "sin libros valuados"


def efecto_dueno(cand: dict, lotes: dict[str, list | None] | None, expos: dict[str, float | None],
                 referencia: Serie, spot: float, hoy: date) -> float | None:
    """Efecto cambiario real en los libros del dueno desde la base del candidato; None si falta algun
    libro real valuado sin sus lotes."""
    if lotes is None:
        return None
    total = 0.0
    for n in LIBROS_DUENO:
        if expos.get(n) is None:
            continue
        if lotes.get(n) is None:
            return None
        total += efecto_cambiario(lotes[n], referencia, cand["base"], spot, hoy)
    return total


def frase_dueno(cand: dict, expos: dict[str, float | None], hoy: date, efecto: float | None = None) -> str:
    """Frase para el dueno. 'efecto': MXN que el movimiento le sumo de verdad (efecto_dueno); sin el,
    solo la exposicion de hoy (nunca la parte en USD de hoy por el movimiento de toda la ventana, que
    sobreestima cuando se compro con el dolar ya movido)."""
    verbo = "subió" if cand["direccion"] == "sube" else "bajó"
    plazo = "desde ayer" if cand["dias"] == 1 else f"en {cand['dias']} días"
    reales = [expos[n] for n in LIBROS_DUENO if expos.get(n) is not None]
    if not reales:
        dinero = "no pude calcular el efecto en tu dinero (sin libros reales valuados)"
    elif sum(reales) < 0.5:
        dinero = "tu dinero real no tiene parte en dólares, así que no le cambia"
    else:
        usd = sum(reales)
        expo = f"hoy tienes unos {_mxn(usd)} MXN en dólares: cada 1% del dólar les mueve unos {_mxn(usd * 0.01)} MXN"
        if efecto is None:
            dinero = expo
        else:
            verbo_ef, r = ("suma" if efecto >= 0 else "resta"), round(abs(efecto))
            parte = ("a tu dinero casi no le cambió (menos de 1 MXN)" if r == 0
                     else f"a tu dinero le {verbo_ef} 1 MXN" if r == 1
                     else f"a tu dinero le {verbo_ef} unos {_mxn(abs(efecto))} MXN")
            if abs(efecto) < 0.5 * abs(efecto_movimiento(usd, cand["cambio"])):
                parte += (", porque casi todo lo que tienes en dólares lo compraste con el dólar ya "
                          + ("arriba" if cand["direccion"] == "sube" else "abajo"))
            dinero = f"{parte}; {expo}"
    vie = proximo_viernes(hoy)
    comite = (f"lo revisa el comité de hoy, viernes {fecha_corta(vie)}" if vie == hoy
              else f"lo revisa el comité del viernes {fecha_corta(vie)}")
    return (f"el dólar {verbo} {abs(cand['cambio']) * 100:.1f}% {plazo}; {dinero}; "
            f"no hay que hacer nada hoy, {comite}")


def lineas(ev: dict, dec: dict, fuente: dict, expos: dict[str, float | None],
           lotes: dict[str, list | None] | None = None) -> list[tuple[int, str]]:
    """Salida para la supervision: [(nivel, texto)]. 'lotes' (lotes_usd por libro) da el efecto real
    en la frase para el dueno; sin ellos la frase solo dice la exposicion."""
    hora = fuente.get("hora")
    hora_txt = f"{hora:%Y-%m-%d %H:%M} UTC" if hora else "hora desconocida"
    medida = (f"USD/MXN {ev['spot']:.4f} ({fuente.get('fuente_spot', 'spot')}, {hora_txt}) · "
              f"Δ1 {_pct(ev['d1'])} vs {ev['ref1'][1]:.4f} del {fecha_corta(ev['ref1'][0])} · "
              f"Δ10 {_pct(ev['d10'])} vs {ev['ref10'][1]:.4f} del {fecha_corta(ev['ref10'][0])} · "
              f"σd {ev['sigma'] * 100:.2f}% · referencia {fuente.get('fuente_ref', '?')}")
    notas = f" · notas: {'; '.join(fuente['notas'])}" if fuente.get("notas") else ""
    efecto = f" · efecto por cada 1% del USD/MXN: {texto_por_uno(expos)}"
    c = dec["disparo"]
    if c is None:
        sup = ""
        if dec["suprimidos"]:  # se reporta el de mayor nivel
            cs, r = dec["suprimidos"][0]
            f0 = date.fromisoformat(r["fecha"])
            signo = 1 if r["direccion"] == "sube" else -1
            umbral = r["usdmxn"] * math.exp(signo * ev["sigma10"])
            sup = (f" · {NOMBRE[cs['nivel']]} {cs['direccion']} ({cs['motivo']} {_pct(cs['cambio'])}) suprimida: "
                   f"ya se avisó con la {NOMBRE[r['nivel']]} del {fecha_corta(f0)}; no se repite hasta el "
                   f"{fecha_corta(sumar_habiles(f0, DIAS_SUPRESION))} salvo que el USD/MXN "
                   f"{'pase de' if signo > 0 else 'baje de'} {umbral:.4f}")
        return [(OK, f"FX-1 OK · sin disparo nuevo · {medida}{sup}{efecto}{notas}")]
    txt = (f"FX-1 {NOMBRE[c['nivel']]} · el dólar {c['direccion']}: {c['motivo']} {_pct(c['cambio'])} "
           f"(umbral {c['umbral'] * 100:.2f}%"
           + (f", {c['dias']} días hábiles" if c["motivo"] == "episodio" else "") + ") · "
           f"{medida}{efecto}{notas} · no es orden de compra ni de venta: pide revisión")
    if c["nivel"] == ALERTA:
        ef = efecto_dueno(c, lotes, expos, fuente.get("referencia") or [], ev["spot"], ev["hoy"])
        txt += f' · para el dueño: "{frase_dueno(c, expos, ev["hoy"], ef)}"'
    return [(c["nivel"], txt)]


def revisar(datos_fx: dict, expos: dict[str, float | None], hoy: date, ruta_estado: Path | None,
            registrar: bool = True, lotes: dict[str, list | None] | None = None) -> list[tuple[int, str]]:
    """Evalua FX-1 y aplica la supresion; si hay disparo y registrar=True, guarda el estado despues de
    armar la salida (si algo falla antes, la alerta no queda suprimida sin haberse dicho)."""
    ev = evaluar(datos_fx["referencia"], datos_fx["spot"], hoy)
    estado, notas_estado = leer_estado(ruta_estado)
    dec = decidir(ev, estado)
    fuente = {**datos_fx, "notas": list(datos_fx.get("notas") or []) + notas_estado}
    salida = lineas(ev, dec, fuente, expos, lotes)
    if registrar and dec["disparo"] is not None and ruta_estado is not None:
        try:
            guardar_estado(ruta_estado, dec["estado"])
        except OSError as e:
            salida.append((AVISO, f"FX-1: no se pudo guardar {ruta_estado.name} ({e}); la misma alerta saldrá "
                                  f"otra vez en la próxima corrida"))
    return salida


# ---------------------------------------------------------------- fuentes (red)

def parsear_spot_yahoo(texto: str) -> dict:
    """Ultimo minuto con precio de chart v8 (1m): {'precio', 'hora' (UTC), 'cierre_previo', 'gmtoffset'}."""
    try:
        r = json.loads(texto)["chart"]["result"][0]
        cierres = r["indicators"]["quote"][0]["close"]
        pares = [(ts, c) for ts, c in zip(r.get("timestamp") or [], cierres) if c is not None]
        ts, precio = pares[-1]
    except (KeyError, IndexError, TypeError, ValueError) as e:
        raise datos.ErrorDatos(f"Yahoo {TICKER} 1m sin precio: {e!r}") from e
    meta = r.get("meta", {})
    return {"precio": float(precio), "hora": datetime.fromtimestamp(ts, tz=timezone.utc),
            "cierre_previo": meta.get("previousClose"), "gmtoffset": int(meta.get("gmtoffset", 0))}


def spot_yahoo() -> dict:
    url = datos.URL_YAHOO + urllib.parse.quote(TICKER, safe="") + "?range=1d&interval=1m"
    return parsear_spot_yahoo(datos.descargar(url, datos.UA_NAVEGADOR))


def parsear_diario_yahoo(texto: str) -> dict:
    """Barras diarias de chart v8: {'cierres': [(fecha de Londres, cierre)], 'aperturas': {fecha: apertura},
    'gmtoffset'}. Solo apertura y cierre, nunca maximo ni minimo. Si un dia trae dos puntos (la barra en
    curso y el precio en vivo), gana el ultimo cierre y la primera apertura."""
    try:
        r = json.loads(texto)["chart"]["result"][0]
        q = r["indicators"]["quote"][0]
        tiempos = r.get("timestamp") or []
        aperturas_l, cierres_l = q.get("open") or [], q.get("close") or []
        off = int(r.get("meta", {}).get("gmtoffset", 0))
    except (KeyError, IndexError, TypeError, ValueError) as e:
        raise datos.ErrorDatos(f"Yahoo {TICKER} 1d inesperado: {e!r}") from e
    cierres: dict[date, float] = {}
    aperturas: dict[date, float] = {}
    for i, ts in enumerate(tiempos):
        f = datetime.fromtimestamp(ts + off, tz=timezone.utc).date()
        o = aperturas_l[i] if i < len(aperturas_l) else None
        c = cierres_l[i] if i < len(cierres_l) else None
        if o is not None and f not in aperturas:
            aperturas[f] = float(o)
        if c is not None:
            cierres[f] = float(c)
    if not cierres:
        raise datos.ErrorDatos(f"Yahoo {TICKER} 1d sin cierres")
    return {"cierres": sorted(cierres.items()), "aperturas": aperturas, "gmtoffset": off}


def referencia_yahoo(cierres: Serie, fecha_londres: date, cierre_previo: float | None,
                     apertura_en_curso: float | None = None) -> Serie:
    """Cierres diarios de Yahoo MXN=X reetiquetados al dia habil que cierran.

    Yahoo fecha cada barra diaria de divisas a las 00:00 de Londres y su "cierre" es practicamente la
    cotizacion de ese momento (apertura ≈ cierre en las barras completas: mediana |o/c - 1| de 0.01%,
    maximo 0.17%, 3 meses al 30-sep-2026): la barra del dia D es el cierre del dia habil anterior a D.
    La barra en curso (fecha de Londres de hoy) trae el precio en vivo y se descarta; en su lugar va el
    cierre anterior: el previousClose de la consulta 1m o, si esa fallo, la apertura de la barra en
    curso (es la misma cotizacion de las 00:00 de Londres).
    """
    salida: dict[date, float] = {}
    for f, v in cierres:
        if f < fecha_londres:
            salida[dia_habil_anterior(f)] = v
    previo = cierre_previo or apertura_en_curso
    if previo:
        salida[dia_habil_anterior(fecha_londres)] = float(previo)
    return sorted(salida.items())


def diario_yahoo() -> dict:
    url = datos.URL_YAHOO + urllib.parse.quote(TICKER, safe="") + "?range=3mo&interval=1d"
    return parsear_diario_yahoo(datos.descargar(url, datos.UA_NAVEGADOR))


def spot_binance() -> float:
    try:
        return float(json.loads(datos.descargar(URL_BINANCE + "ticker/price?symbol=" + PAR_BINANCE))["price"])
    except (KeyError, TypeError, ValueError) as e:
        raise datos.ErrorDatos(f"Binance {PAR_BINANCE} sin precio: {e!r}") from e


def parsear_klines_binance(texto: str, hoy: date) -> Serie:
    """Cierres diarios (indice 4) de dias habiles completos; nunca maximo ni minimo."""
    try:
        velas = json.loads(texto)
        serie = [(datetime.fromtimestamp(k[0] / 1000, tz=timezone.utc).date(), float(k[4])) for k in velas]
    except (TypeError, ValueError, IndexError) as e:
        raise datos.ErrorDatos(f"Binance {PAR_BINANCE} velas invalidas: {e!r}") from e
    return [(f, v) for f, v in serie if f < hoy and es_habil(f)]


def diario_binance(hoy: date) -> Serie:
    url = URL_BINANCE + "klines?" + urllib.parse.urlencode({"symbol": PAR_BINANCE, "interval": "1d", "limit": 120})
    return parsear_klines_binance(datos.descargar(url), hoy)


FUENTES_RED = {"spot_yahoo": spot_yahoo, "diario_yahoo": diario_yahoo, "fix": banxico.rango,
               "spot_binance": spot_binance, "diario_binance": diario_binance}


def nota_hueco(referencia: Serie, hoy: date) -> str | None:
    """Nota si la referencia mas reciente antes de hoy no es la del dia habil anterior (feriado, fuente
    atrasada o un cierre que falto): entonces D1 y D10 miden dias habiles de mas."""
    previas = [f for f, _ in referencia if f < hoy]
    esperado = dia_habil_anterior(hoy)
    if not previas or previas[-1] >= esperado:
        return None
    n = dias_habiles(previas[-1], hoy)
    return (f"la referencia más reciente es del {fecha_corta(previas[-1])}, no del {fecha_corta(esperado)}: "
            f"Δ1 mide {n} días hábiles, no 1, y Δ10 mide {n - 1} de más")


def obtener(ahora: datetime, fuentes: dict[str, Callable] | None = None) -> dict:
    """Spot y referencia con sus respaldos: {'spot', 'hora', 'fuente_spot', 'referencia', 'fuente_ref',
    'notas'}. Sin BANXICO_TOKEN (contenedores de rutinas) usa los cierres diarios de Yahoo."""
    f = {**FUENTES_RED, **(fuentes or {})}
    hoy, notas = fecha_local(ahora), []
    cierre_previo, fecha_londres = None, None
    try:
        s = f["spot_yahoo"]()
        spot, hora, cierre_previo = s["precio"], s["hora"], s.get("cierre_previo")
        fecha_londres = (ahora + timedelta(seconds=s.get("gmtoffset", 0))).date()
        fuente_spot = "spot Yahoo MXN=X 1m"
    except datos.ErrorDatos as e:
        notas.append(f"spot de Yahoo no disponible ({e})")
        try:
            spot, hora, fuente_spot = f["spot_binance"](), ahora, "spot Binance USDT/MXN"
            notas.append(NOTA_BINANCE)
        except datos.ErrorDatos as e2:
            raise ErrorFX(f"sin spot de USD/MXN: Yahoo ({e}); Binance ({e2})") from e2
    referencia, fuente_ref = None, None
    try:
        referencia = f["fix"](SERIE_FIX, (hoy - timedelta(days=120)).isoformat(), hoy.isoformat())
        fuente_ref = f"FIX Banxico {SERIE_FIX}"
    except banxico.SinToken:
        notas.append("sin BANXICO_TOKEN: cierres diarios de Yahoo en lugar del FIX")
    except Exception as e:  # noqa: BLE001 - cualquier falla del SIE cae al respaldo
        notas.append(f"FIX no disponible ({type(e).__name__}): cierres diarios de Yahoo en su lugar")
    if referencia and sum(1 for d, _ in referencia if d < hoy) < N_SIGMA + 1:
        notas.append(f"FIX con solo {len(referencia)} datos: cierres diarios de Yahoo en su lugar")
        referencia = None
    if not referencia:
        try:
            d = f["diario_yahoo"]()
            if fecha_londres is None:
                fecha_londres = (ahora + timedelta(seconds=d.get("gmtoffset", 0))).date()
            referencia = referencia_yahoo(d["cierres"], fecha_londres, cierre_previo,
                                          d.get("aperturas", {}).get(fecha_londres))
            fuente_ref = "cierres diarios Yahoo MXN=X (3mo, 1d) como sustituto del FIX"
        except datos.ErrorDatos as e:
            notas.append(f"cierres de Yahoo no disponibles ({e})")
            try:
                referencia = f["diario_binance"](hoy)
                fuente_ref = "cierres diarios Binance USDT/MXN como sustituto del FIX"
                if NOTA_BINANCE not in notas:
                    notas.append(NOTA_BINANCE)
            except datos.ErrorDatos as e2:
                raise ErrorFX(f"sin referencia diaria: Yahoo ({e}); Binance ({e2})") from e2
    hueco = nota_hueco(referencia, hoy)
    if hueco:
        notas.append(hueco)
    return {"spot": spot, "hora": hora, "fuente_spot": fuente_spot, "referencia": referencia,
            "fuente_ref": fuente_ref, "notas": notas}


# ---------------------------------------------------------------- CLI (solo lectura)

def _posiciones_con_cierres(libro, grafica: Callable | None = None) -> tuple[list[dict], list[str]]:
    """([{'ticker','cantidad','p0','f0','p1','f1','moneda'}], tickers omitidos) con los dos ultimos
    cierres diarios de Yahoo. Los omitidos (sin datos) se devuelven para anotarlos, no se callan."""
    grafica = grafica or datos.yahoo_grafica
    salida, omitidos = [], []
    for t, p in sorted(libro.posiciones.items()):
        try:
            g = grafica(t, "5d", "1d")
        except datos.ErrorDatos:
            omitidos.append(t)
            continue
        serie = g["serie"]
        if len(serie) < 2:
            omitidos.append(t)
            continue
        moneda = str(g["meta"].get("currency", "")).upper() or p["moneda"]
        salida.append({"ticker": t, "cantidad": p["cantidad"], "p0": serie[-2][1], "f0": serie[-2][0],
                       "p1": serie[-1][1], "f1": serie[-1][0], "moneda": moneda})
    return salida, omitidos


def cuentas_vacias() -> dict:
    return {"expos": {}, "efectos": {}, "lotes": {}, "previos": {}, "notas": []}


def por_cuenta(bitacora: Path, referencia: Serie, spot: float) -> dict:
    """Por libro (red: Yahoo): {'expos': parte en USD al spot (MXN), 'efectos': descomposicion precio/
    cambio del cierre previo de cada posicion a este momento (fx0 = referencia de la fecha del previo),
    'lotes': lotes_usd, 'previos': (fecha minima, maxima) de los previos, 'notas'}."""
    from herramientas import portafolio, supervision  # import diferido: supervision importa este modulo
    from herramientas.parametros import parametros_efectivos
    c = cuentas_vacias()
    fx_def = referencia[-1][1] if referencia else spot
    for nombre, ops, _eq, _prm in supervision.libros(bitacora, parametros_efectivos("arena_agresivo"),
                                                     parametros_efectivos("cripto_binance")):
        try:
            operaciones = portafolio.leer_operaciones(ops) if ops.exists() else []
            if not operaciones:
                c["expos"][nombre] = c["efectos"][nombre] = c["lotes"][nombre] = c["previos"][nombre] = None
                continue
            fx_hist = portafolio.proveedor_fx_yahoo(min(o["fecha"] for o in operaciones)) \
                if any(o["moneda"] == "USD" for o in operaciones) else None
            pos, omitidos = _posiciones_con_cierres(portafolio.construir_libro(operaciones, fx_hist))
        except Exception as e:  # noqa: BLE001 - un libro que no se puede valuar no tumba la linea
            c["expos"][nombre] = c["efectos"][nombre] = c["lotes"][nombre] = c["previos"][nombre] = None
            c["notas"].append(f"{nombre}: no se pudo valuar ({type(e).__name__}: {e})")
            continue
        if omitidos:
            c["notas"].append(f"{nombre}: sin cierres de Yahoo para {', '.join(omitidos)}; no entran en el "
                              f"efecto de precio ni en la parte en USD (subestimadas)")
        for p in pos:
            p["fx0"] = _valor_en(referencia, p["f0"], fx_def)
        c["efectos"][nombre] = descomponer(pos, fx_def, spot)
        c["expos"][nombre] = sum(p["cantidad"] * p["p1"] * spot for p in pos if p["moneda"] == "USD")
        c["lotes"][nombre] = lotes_usd(operaciones, [{"ticker": p["ticker"], "moneda": p["moneda"],
                                                      "precio": p["p1"]} for p in pos])
        c["previos"][nombre] = (min(p["f0"] for p in pos), max(p["f0"] for p in pos)) if pos else None
    return c


def linea_brief(d: dict, ev: dict, dec: dict, cuentas: dict) -> str:
    """Linea 'Tipo de cambio' del brief: efecto de precio separado del efecto cambiario por cuenta, los
    dos sobre la misma ventana (del cierre previo de cada posicion a este momento)."""
    c = dec["disparo"]
    estado = (f"{NOMBRE[c['nivel']]} {c['direccion']} ({c['motivo']} {_pct(c['cambio'])})" if c
              else "OK" + (" (alerta vigente ya avisada, suprimida)" if dec["suprimidos"] else ""))
    partes = []
    for n, e in cuentas["efectos"].items():
        if e is None:
            partes.append(f"{n}: sin libro")
            continue
        prev = cuentas["previos"].get(n)
        desde = ("" if prev is None else f" (desde el cierre del {fecha_corta(prev[0])})" if prev[0] == prev[1]
                 else f" (desde los cierres del {fecha_corta(prev[0])} al {fecha_corta(prev[1])})")
        partes.append(f"{n}{desde}: precio {e['precio']:+,.0f} MXN, cambio {e['cambio']:+,.0f} MXN")
    notas = list(d.get("notas") or []) + list(cuentas.get("notas") or [])
    return (f"**Tipo de cambio:** USD/MXN {d['spot']:.4f} ({d['fuente_spot']}, {d['hora']:%H:%M} UTC); "
            f"Δ1 {_pct(ev['d1'])}, Δ10 {_pct(ev['d10'])}, σd {ev['sigma'] * 100:.2f}%; FX-1 {estado}; "
            f"referencia {d['fuente_ref']}. Del cierre previo de cada posición a este momento (precio: último "
            f"precio contra el cierre previo, al USD/MXN de la fecha de ese cierre; cambio: ese USD/MXN → "
            f"{d['spot']:.4f}) — " + ("; ".join(partes) or "sin libros")
            + f". Por cada 1% del USD/MXN: {texto_por_uno(cuentas['expos'])}."
            + (f" Notas: {'; '.join(notas)}." if notas else ""))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Regla FX-1 (alerta cambiaria USD/MXN)")
    ap.add_argument("--brief", action="store_true", help="línea 'Tipo de cambio' del brief, por cuenta")
    ap.add_argument("--registrar", action="store_true",
                    help="si dispara, guarda el estado de supresión (úsalo solo si tu rutina avisa la alerta)")
    args = ap.parse_args(argv)
    ahora = datetime.now(timezone.utc)
    hoy = fecha_local(ahora)
    try:
        d = obtener(ahora)
        ev = evaluar(d["referencia"], d["spot"], hoy)
    except ErrorFX as e:
        print(f"AVISO · FX-1 sin datos: {e}")
        return AVISO
    estado, notas_estado = leer_estado(RUTA_ESTADO)
    d["notas"] = list(d["notas"]) + notas_estado
    dec = decidir(ev, estado)  # el estado lo escribe la supervision (o --registrar, al final)
    try:
        cuentas = por_cuenta(DIR_BITACORA, d["referencia"], d["spot"])
    except Exception as e:  # noqa: BLE001 - sin libros la regla se dice igual
        cuentas = cuentas_vacias()
        cuentas["notas"].append(f"sin libros valuados ({type(e).__name__}: {e})")
    if args.brief:
        print(linea_brief(d, ev, dec, cuentas))
        nivel = OK
    else:
        nivel, texto = lineas(ev, dec, {**d, "notas": d["notas"] + cuentas["notas"]},
                              cuentas["expos"], cuentas["lotes"])[0]
        print(f"{NOMBRE[nivel]} · {texto}")
    if args.registrar and dec["disparo"] is not None:
        try:
            guardar_estado(RUTA_ESTADO, dec["estado"])
            print(f"FX-1 {NOMBRE[dec['disparo']['nivel']]} {dec['disparo']['direccion']} registrada en "
                  f"bitacora/supervision/{RUTA_ESTADO.name} (supresión de {DIAS_SUPRESION} días hábiles)")
        except OSError as e:
            print(f"AVISO · FX-1: no se pudo guardar {RUTA_ESTADO.name} ({e}); la alerta no quedó suprimida")
            return max(nivel, AVISO)
    return nivel


if __name__ == "__main__":
    sys.exit(main())
