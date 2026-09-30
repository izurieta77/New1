"""Calibracion de la regla FX-1 (herramientas/fx_alerta.py) sobre datos reales.

Corre la regla dia por dia, con la supresion de 10 dias habiles, sobre:
  A. FIX de Banxico (SF43718), si hay BANXICO_TOKEN en el entorno (el token nunca se imprime);
  B. cierres diarios de Yahoo MXN=X (10y, 1d), reetiquetados al dia habil que cierran (ver
     fx_alerta.referencia_yahoo: la barra diaria de Yahoo es la cotizacion de las 00:00 de Londres).
En la historia no hay spot intradia: el "spot" de cada dia es la referencia de ese dia (FIX o cierre),
como en la tabla de calibracion de la especificacion. Hoy se usa el spot de Yahoo 1m en vivo.

Uso (desde la raiz del repo):
    BANXICO_TOKEN=... python3 laboratorio/auditorias/AC-08-carry-peso/calibracion_fx1.py
Sin red no corre. No escribe archivos (la cache de Yahoo va a datos/cache, fuera de git).
"""
from __future__ import annotations

import math
import os
import sys
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

RAIZ = Path("/home/user/New1")
sys.path.insert(0, str(RAIZ))
from herramientas import banxico, datos  # noqa: E402
from herramientas import fx_alerta as fx  # noqa: E402

HOY = date(2026, 9, 30)


def simular(serie: list[tuple[date, float]], desde: date, hoy_spot: float | None = None,
            estricta: bool = False) -> list[dict]:
    """Disparos de FX-1 dia por dia desde 'desde'. estricta=True: la supresion solo cuenta alertas del
    MISMO nivel (texto literal de la especificacion); por defecto tambien suprime un nivel menor en la
    misma direccion mientras siga vigente una ALERTA (diseno implementado)."""
    original = fx._bloqueo
    if estricta:
        def _bloqueo_estricto(cand, vigentes, spot, sigma10):
            signo = 1 if cand["direccion"] == "sube" else -1
            for r in vigentes.values():
                if r["direccion"] == cand["direccion"] and r["nivel"] == cand["nivel"] \
                        and signo * math.log(spot / r["usdmxn"]) < sigma10:
                    return r
            return None
        fx._bloqueo = _bloqueo_estricto
    try:
        estado, disparos = {}, []
        valores = dict(serie)
        fechas = [f for f, _ in serie if f >= desde]
        if hoy_spot is not None and (not fechas or fechas[-1] < HOY):
            fechas.append(HOY)
        for t in fechas:
            spot = valores[t] if t in valores else hoy_spot
            try:
                ev = fx.evaluar(serie, spot, t)
            except fx.ErrorFX:
                continue
            dec = fx.decidir(ev, estado)
            estado = dec["estado"]
            if dec["disparo"]:
                c = dec["disparo"]
                disparos.append({"fecha": t, "nivel": fx.NOMBRE[c["nivel"]], "dir": c["direccion"],
                                 "motivo": c["motivo"], "cambio": c["cambio"], "d1": ev["d1"], "d10": ev["d10"],
                                 "sigma": ev["sigma"], "ep": ev["ep_sube"] if c["direccion"] == "sube" else ev["ep_baja"]})
            elif t >= date(2026, 9, 1):
                disparos.append({"fecha": t, "nivel": "—", "dir": "", "motivo": "suprimida" if dec["suprimidos"] else "",
                                 "cambio": 0.0, "d1": ev["d1"], "d10": ev["d10"], "sigma": ev["sigma"],
                                 "ep": ev["ep_sube"], "sup": [f"{fx.NOMBRE[c['nivel']]} {c['direccion']}"
                                                              for c, _ in dec["suprimidos"]]})
        return disparos
    finally:
        fx._bloqueo = original


def conteo(disparos: list[dict], desde: date) -> Counter:
    return Counter(d["nivel"] for d in disparos if d["fecha"] > desde and d["nivel"] != "—")


def reporte(nombre: str, serie: list[tuple[date, float]], hoy_spot: float | None) -> None:
    print(f"\n=== {nombre}: {len(serie)} observaciones, {serie[0][0]} a {serie[-1][0]} ===")
    inicio = HOY.replace(year=HOY.year - 5) - timedelta(days=60)  # 60 dias de calentamiento para sd
    for etiqueta, estricta in (("diseño (ALERTA vigente suprime AVISO en la misma dirección)", False),
                               ("literal (solo mismo nivel)", True)):
        ds = simular(serie, inicio, hoy_spot, estricta)
        c1, c5 = conteo(ds, HOY - timedelta(days=365)), conteo(ds, HOY.replace(year=HOY.year - 5))
        print(f"-- supresión {etiqueta}")
        print(f"   último año: {c1['AVISO']} AVISO, {c1['ALERTA']} ALERTA | "
              f"5 años: {c5['AVISO']} AVISO, {c5['ALERTA']} ALERTA")
        if estricta:
            continue
        print("   septiembre de 2026 (spot del día = referencia del día; hoy = Yahoo 1m en vivo):")
        for d in ds:
            if d["fecha"] >= date(2026, 9, 1):
                extra = f"  suprimida: {', '.join(d['sup'])}" if d.get("sup") else ""
                print(f"   {d['fecha']}  {d['nivel']:<6} {d['dir']:<4} {d['motivo']:<9} Δ1 {d['d1']*100:+6.2f}%  "
                      f"Δ10 {d['d10']*100:+6.2f}%  σd {d['sigma']*100:.2f}%  ep {d['ep']*100:+5.2f}%{extra}")
        print("   ALERTAS de los 5 años:")
        for d in ds:
            if d["nivel"] == "ALERTA" and d["fecha"] > HOY.replace(year=HOY.year - 5):
                print(f"   {d['fecha']}  {d['dir']:<4} {d['motivo']:<9} {d['cambio']*100:+.2f}%  σd {d['sigma']*100:.2f}%")
        dirs = Counter((d["nivel"], d["dir"]) for d in ds if d["fecha"] > HOY.replace(year=HOY.year - 5)
                       and d["nivel"] != "—")
        print(f"   por dirección (5 años): {dict(sorted(dirs.items()))}")


def main() -> int:
    s = fx.spot_yahoo()
    spot, hora = s["precio"], s["hora"]
    print(f"Spot Yahoo MXN=X 1m: {spot:.4f} a las {hora:%Y-%m-%d %H:%M} UTC; previousClose {s['cierre_previo']}")
    g = datos.yahoo_grafica(fx.TICKER, "10y", "1d", cache_horas=6)
    fecha_londres = (datetime.now(timezone.utc) + timedelta(seconds=s["gmtoffset"])).date()
    yahoo = fx.referencia_yahoo(g["serie"], fecha_londres, s["cierre_previo"])
    fix = None
    if os.environ.get("BANXICO_TOKEN", "").strip():
        fix = banxico.rango(fx.SERIE_FIX, "2021-01-01", HOY.isoformat())
    else:
        print("Sin BANXICO_TOKEN: solo la réplica con Yahoo.")
    if fix:
        # Verificación del reetiquetado: la barra de Yahoo fechada D se parece más al FIX de D-1 que al de D.
        crudo, fixd = dict(g["serie"]), dict(fix)
        reet = dict(yahoo)
        dif = lambda a, b: sorted(abs(math.log(a[f] / b[f])) for f in a if f in b and f.year >= 2021)  # noqa: E731
        m_crudo, m_reet = dif(fixd, crudo), dif(fixd, reet)
        print(f"Mediana |log(FIX/Yahoo)|: barra con su fecha {m_crudo[len(m_crudo)//2]*100:.3f}% "
              f"vs reetiquetada al día hábil anterior {m_reet[len(m_reet)//2]*100:.3f}% "
              f"(n={len(m_crudo)}/{len(m_reet)})")
        reporte("A. FIX Banxico SF43718", fix, spot)
    reporte("B. Yahoo MXN=X diario reetiquetado", yahoo, spot)  # la barra en curso se quitó: hoy = spot
    return 0


if __name__ == "__main__":
    sys.exit(main())
