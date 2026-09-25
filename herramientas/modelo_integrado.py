"""Motor generico de modelo integrado de 3 estados (resultados, balance y flujo) con controles.

FASE 0 (formacion). El motor proyecta ESCENARIOS con supuestos explicitos. Los escenarios NO son
pronosticos, ni guia del emisor, ni consenso. Nada de lo que produce es recomendacion de compra o
venta. Solo usa la biblioteca estandar de Python 3.11.

Tres naturalezas de cifra, siempre separadas en la salida:
  - "hecho (filing)": cifras historicas transcritas de un documento (cada periodo exige 'fuente').
  - "calculo sobre hechos": drivers implicitos y partidas conciliatorias derivadas del historico.
  - "supuesto de escenario": entradas de proyeccion elegidas por el analista.
Las inferencias se escriben en notas-y-modelo.md con el prefijo "Inferencia:".

USO COMO LIBRERIA (p. ej. desde empresas/<TICKER>/modelo/modelo.py)
    import sys
    from pathlib import Path
    AQUI = Path(__file__).resolve().parent
    sys.path.insert(0, str(AQUI.parents[2]))          # raiz del repo
    from herramientas import modelo_integrado as mi
    base = mi.cargar_json(AQUI / "base.json")
    res = mi.construir_modelo(base)                   # supuestos en base["supuestos"] o 2o argumento
    mi.guardar_json(res, AQUI / "resultados.json")
    mi.escribir_sha256sums([AQUI / "base.json", AQUI / "modelo.py", AQUI / "resultados.json"],
                           AQUI / "SHA256SUMS.txt")
    print(mi.resumen_markdown(res))
    raise SystemExit(0 if res["resumen_controles"]["todos_ok"] else 1)

CLI
    python3 herramientas/modelo_integrado.py correr --base B.json [--supuestos S.json] --salida R.json \
        [--sha256 SHA256SUMS.txt] [--markdown resumen.md]            # codigo 1 si algun control FALLA
    python3 herramientas/modelo_integrado.py dcf-inverso --precio P --acciones N --deuda-neta D \
        --wacc 0.09 --g-terminal 0.03 --margen-fcf 0.25 --anos 10 --ingresos-base I [--tasa-libre-riesgo 0.042]

BASE HISTORICA (JSON). Montos en las unidades declaradas (p. ej. millones), >= 2 ejercicios en orden:
{
  "empresa": "Acme Corp", "ticker": "ACME", "moneda": "USD", "unidades": "millones",
  "fecha_corte": "2026-09-25",
  "fuentes": {"F1": {"documento": "10-K FY2025", "url": "https://www.sec.gov/Archives/...", "fecha": "2025-07-30"}},
  "tolerancias": {...opcional, ver TOLERANCIAS_DEFECTO...},
  "historico": [
    {"periodo": "FY2025", "anio": 2025, "fin": "2025-06-30",
     "fuente": "F1: estados financieros p. 50-54",                    # OBLIGATORIO
     "fuentes_campos": {"flujo.capex": "F1 p. 54"},                   # opcional, por cifra
     "resultados": {ingresos, costo_ventas, utilidad_operativa, gasto_intereses,
                    utilidad_antes_impuestos, impuestos, utilidad_neta            (obligatorios)
                    utilidad_bruta, gastos_operativos, ingreso_intereses, otros_ingresos,
                    otros_despues_impuestos, utilidad_neta_controladora}           (opcionales)
     "balance":    {caja, cuentas_por_cobrar, inventarios, ppe_neto, activo_total, proveedores,
                    deuda, pasivo_total, capital_contable                          (obligatorios)
                    inversiones_cp, otros_activos_circulantes, otros_activos_lp,
                    otros_pasivos_circulantes, otros_pasivos_lp, arrendamientos_financieros,
                    revolvente, utilidades_retenidas}                              (opcionales)
     "flujo":      {depreciacion_amortizacion, sbc, cfo, capex, cfi, cff          (obligatorios)
                    dividendos, recompras, emision_deuda, amortizacion_deuda,
                    principal_arrendamientos_financieros, emision_acciones,
                    efecto_cambiario                                    (opcionales; 0 si faltan)
                    cambio_capital_trabajo, otros_operativos, otros_inversion,
                    otros_financiamiento                     (numero o {concepto: monto}; opcionales)
                    caja_inicial, caja_final, utilidad_neta, fcf_reportado}         (opcionales)
     "movimientos_capital": {dividendos_declarados, recompras (obligatorios en el bloque),
                    capital_inicial, utilidades_retenidas_iniciales, utilidad_neta, sbc,
                    emision_acciones, ori, otros, recompras_contra_utilidades_retenidas,
                    otros_utilidades_retenidas},
     "movimientos_ppe": {adiciones, depreciacion (obligatorios en el bloque), ppe_inicial, otros},
     "movimientos_deuda": {emisiones, amortizaciones, otros, deuda_inicial},
     "movimientos_arrendamientos": {nuevos (obligatorio en el bloque), principal, otros, inicial},
     "ajustado": [{"base": "utilidad_neta", "ajustes": {"concepto": -4963},
                   "valor_ajustado": 128786, "fuente": "F1 conciliacion no GAAP p. 38"}],
     "memo": {...cifras informativas que el motor no usa (compromisos, arrendamientos operativos)...},
     "notas": "texto libre"}
  ],
  "supuestos": {...opcional, ver abajo...}
}
Convenciones de la base:
  - Signos del flujo: capex, dividendos, recompras, emision_deuda, amortizacion_deuda,
    principal_arrendamientos_financieros y emision_acciones van en valor ABSOLUTO (>= 0), como en XBRL
    (PaymentsTo...). cfo, cfi, cff, efecto_cambiario, cambio_capital_trabajo y otros_* llevan el
    signo con que afectan la caja (salida negativa). Un pago negativo es error de validacion.
  - caja: la misma definicion de efectivo que el estado de flujo (si el flujo incluye efectivo
    restringido, incluyalo aqui y quitelo de otros activos).
  - deuda: deuda financiera total (corto + largo plazo), incluye revolventes dispuestos.
  - utilidad_neta: consolidada (incluye participacion no controladora), la que abre el flujo.
    capital_contable: total, incluye participacion no controladora.
  - Si faltan otros_activos_* u otros_pasivos_*, se derivan como residuo contra los totales y se
    anota en "derivados". Si faltan inversiones_cp, arrendamientos_financieros o revolvente, valen 0.
  - Bancos y aseguradoras quedan fuera de alcance (el FCF no aplica; ver conocimiento/03 s2.6).

SUPUESTOS DE ESCENARIO (JSON; en base["supuestos"] o archivo aparte)
{
  "anos": 5, "caja_minima": 20000,
  "nota": "Supuestos de escenario; no son pronosticos ni consenso",
  "escenarios": {
    "tension": {"descripcion": "...", "fuente_supuestos": "notas-y-modelo.md s4",
                "crecimiento_ingresos": 0.08 | [0.08, 0.06, ...],   # escalar o lista de 'anos'
                ...}
  }
}
Obligatorios: crecimiento_ingresos, margen_bruto, margen_operativo, tasa_impuestos, da_ventas,
  capex_ventas, sbc_ventas, dias_cxc, dias_inventario, dias_proveedores, tasa_interes, descripcion,
  y caja_minima (global o por escenario; puede ser 0).
Opcionales (defecto): dividendos (0, monto) | dividendos_payout (fraccion de utilidad positiva),
  recompras (0), emision_acciones (0), emision_deuda (0), amortizacion_deuda (0),
  principal_arrendamientos_financieros (0), nuevos_arrendamientos_financieros (0, no monetario:
  sube PPE y pasivo), tasa_arrendamientos_financieros (0), tasa_revolvente (= tasa_interes),
  tasa_rendimiento_caja (0), otros_ingresos (0), amortizacion_intangibles (0; parte de D&A que
  reduce otros_activos_lp en vez de PPE), recompras_contra_utilidades_retenidas (1.0),
  ajuste_utilidad_neta (None; activa C14 en proyeccion), fuente_supuestos, notas.

MECANICA DE PROYECCION (por ano; formulas en _periodo)
  ingresos = ingresos previos x (1+g); utilidad bruta = ingresos x margen_bruto; utilidad operativa =
  ingresos x margen_operativo (D&A y SBC estan DENTRO de costos y gastos, como en US GAAP).
  cxc = dias_cxc x ingresos / 365; inventario y proveedores = dias x costo de ventas / 365 (saldos
  finales). Intereses = tasa x promedio(inicial, final) de deuda, arrendamientos y revolvente;
  ingreso financiero = tasa_rendimiento_caja x promedio de (caja + inversiones_cp). La circularidad
  (intereses <-> revolvente <-> caja) se resuelve por iteracion de punto fijo.
  Impuestos = tasa x UAI (lineal: con UAI negativa hay beneficio fiscal; es un supuesto).
  Otros activos y pasivos e inversiones_cp constantes (simplificacion declarada).
  CAJA ES LA VARIABLE DE CIERRE: caja_pre = caja inicial + CFO + CFI + CFF (sin revolvente).
  Si caja_pre < caja_minima se dispone revolvente = caja_minima - caja_pre y se reporta como
  "financiamiento requerido" explicito; si hay excedente sobre el minimo, primero se paga el
  revolvente (barrido). No existe ningun plug de balance: el balance cuadra por construccion y los
  controles lo recalculan desde los estados publicados.

CONTROLES (16 tipos; cada registro trae esperado, obtenido, diferencia, tolerancia y estado)
  Estados: OK, FALLA, INFO (el dato es implicito/tautologico en el historico: se reporta el valor),
  NO_APLICA (falta el dato para probarlo; se dice cual). todos_ok = ningun FALLA.
  Ver CONTROLES abajo. Tolerancia = max(abs, rel x |ingresos del periodo|), con abs/rel por tipo
  (historico: redondeo de cifras publicadas; proyeccion: error de punto flotante).

DCF INVERSO
  dcf_inverso(precio, acciones, deuda_neta, wacc, g_terminal, margen_fcf, anos, ingresos_base=...)
  despeja por biseccion el crecimiento anual constante de ingresos que iguala el VP de FCFF
  (= ingresos x margen_fcf) mas un valor terminal de Gordon al valor de empresa implicito en el
  precio (precio x acciones + deuda_neta). Supuestos en el resultado. Ver conocimiento/03 s2.7.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import sys
from pathlib import Path

VERSION = "1.0"
DIAS_ANO = 365.0
MAX_ITER_CIRCULAR = 500
TOL_CIRCULAR = 1e-12            # relativo a ingresos del periodo
MAX_PASADAS_REPLAY = 30

AVISO = ("FASE 0 (formacion). Escenarios con supuestos explicitos: no son pronosticos, guia del emisor "
         "ni consenso, y no constituyen recomendacion de compra o venta.")

TOLERANCIAS_DEFECTO = {
    "historico_abs": 2.0,          # unidades de la base: redondeo de cifras publicadas
    "historico_rel": 1e-5,         # fraccion de ingresos del periodo
    "proyeccion_abs": 1e-6,        # punto flotante
    "proyeccion_rel": 1e-9,
    "materialidad_conciliatoria": 0.02,   # partida conciliatoria > 2% de ingresos = ALERTA
}

CONTROLES = {
    "C01": "Balance: activo = pasivo + capital (y totales = suma de componentes)",
    "C02": "Caja: inicial + CFO + CFI + CFF + efecto cambiario = final (y sumas de CFI y CFF)",
    "C03": "Capital: inicial + utilidad + SBC - dividendos - recompras + emisiones + ORI + otros = final",
    "C04": "Utilidades retenidas: inicial + utilidad - dividendos - recompras imputadas + otros = final",
    "C05": "PPE: inicial + capex + nuevos arrendamientos - depreciacion + otros = final",
    "C06": "Deuda: inicial + emisiones - amortizaciones (+ otros) = final (deuda, arrendamientos, revolvente)",
    "C07": "Puente utilidad -> CFO: utilidad + D&A + SBC + capital de trabajo + otros = CFO",
    "C08": "Cuentas por cobrar = dias_cxc x ingresos / 365",
    "C09": "Inventario y proveedores = dias x costo de ventas / 365",
    "C10": "Intereses = tasa x deuda promedio; ingreso financiero = tasa x caja promedio",
    "C11": "Impuestos = tasa x utilidad antes de impuestos",
    "C12": "FCF = CFO - capex; FCF despues de principal de arrendamientos financieros = FCF - principal",
    "C13": "Reconciliacion del historico: el motor reproduce los estados cargados con drivers implicitos",
    "C14": "Conciliacion GAAP vs ajustado: cifra GAAP + ajustes = cifra ajustada",
    "C15": "Aritmetica del estado de resultados (ingresos, bruta, operativa, UAI, neta)",
    "C16": "Caja minima y revolvente: caja >= minimo; financiamiento requerido explicito, sin plug",
}

ACTIVOS = ("caja", "inversiones_cp", "cuentas_por_cobrar", "inventarios", "otros_activos_circulantes",
           "ppe_neto", "otros_activos_lp")
PASIVOS = ("proveedores", "otros_pasivos_circulantes", "deuda", "arrendamientos_financieros", "revolvente",
           "otros_pasivos_lp")

RES_REQ = ("ingresos", "costo_ventas", "utilidad_operativa", "gasto_intereses", "utilidad_antes_impuestos",
           "impuestos", "utilidad_neta")
RES_OPC = ("utilidad_bruta", "gastos_operativos", "ingreso_intereses", "otros_ingresos",
           "otros_despues_impuestos", "utilidad_neta_controladora")
BAL_REQ = ("caja", "cuentas_por_cobrar", "inventarios", "ppe_neto", "activo_total", "proveedores", "deuda",
           "pasivo_total", "capital_contable")
BAL_CERO = ("inversiones_cp", "arrendamientos_financieros", "revolvente")
BAL_RESIDUO_ACT = ("otros_activos_circulantes", "otros_activos_lp")
BAL_RESIDUO_PAS = ("otros_pasivos_circulantes", "otros_pasivos_lp")
BAL_OPC = BAL_CERO + BAL_RESIDUO_ACT + BAL_RESIDUO_PAS + ("utilidades_retenidas",)
FLUJO_REQ = ("depreciacion_amortizacion", "sbc", "cfo", "capex", "cfi", "cff")
FLUJO_CERO = ("dividendos", "recompras", "emision_deuda", "amortizacion_deuda",
              "principal_arrendamientos_financieros", "emision_acciones", "efecto_cambiario")
FLUJO_DETALLE = ("cambio_capital_trabajo", "otros_operativos", "otros_inversion", "otros_financiamiento")
FLUJO_OPC = ("caja_inicial", "caja_final", "utilidad_neta", "fcf_reportado")
PAGOS_NO_NEGATIVOS = ("capex", "dividendos", "recompras", "emision_deuda", "amortizacion_deuda",
                      "principal_arrendamientos_financieros", "emision_acciones")

MOV_CAPITAL = {"requeridos": ("dividendos_declarados", "recompras"),
               "opcionales": ("capital_inicial", "utilidades_retenidas_iniciales", "utilidad_neta", "sbc",
                              "emision_acciones", "ori", "otros", "recompras_contra_utilidades_retenidas",
                              "otros_utilidades_retenidas")}
MOV_PPE = {"requeridos": ("adiciones", "depreciacion"), "opcionales": ("ppe_inicial", "otros")}
MOV_DEUDA = {"requeridos": (), "opcionales": ("deuda_inicial", "emisiones", "amortizaciones", "otros")}
MOV_ARR = {"requeridos": ("nuevos",), "opcionales": ("inicial", "principal", "otros")}
BLOQUES_MOV = {"movimientos_capital": MOV_CAPITAL, "movimientos_ppe": MOV_PPE,
               "movimientos_deuda": MOV_DEUDA, "movimientos_arrendamientos": MOV_ARR}
CLAVES_PERIODO = {"periodo", "anio", "fin", "fuente", "fuentes_campos", "resultados", "balance", "flujo",
                  "ajustado", "memo", "notas"} | set(BLOQUES_MOV)

SUPUESTOS_REQ = ("crecimiento_ingresos", "margen_bruto", "margen_operativo", "tasa_impuestos", "da_ventas",
                 "capex_ventas", "sbc_ventas", "dias_cxc", "dias_inventario", "dias_proveedores", "tasa_interes")
SUPUESTOS_OPC = {
    "dividendos": 0.0, "dividendos_payout": None, "recompras": 0.0, "emision_acciones": 0.0,
    "emision_deuda": 0.0, "amortizacion_deuda": 0.0, "principal_arrendamientos_financieros": 0.0,
    "nuevos_arrendamientos_financieros": 0.0, "tasa_arrendamientos_financieros": 0.0, "tasa_revolvente": None,
    "tasa_rendimiento_caja": 0.0, "otros_ingresos": 0.0, "amortizacion_intangibles": 0.0,
    "recompras_contra_utilidades_retenidas": 1.0, "caja_minima": None, "ajuste_utilidad_neta": None,
}
SUPUESTOS_META = ("descripcion", "fuente_supuestos", "notas")
NO_NEGATIVOS = ("da_ventas", "capex_ventas", "sbc_ventas", "dias_cxc", "dias_inventario", "dias_proveedores",
                "tasa_interes", "dividendos", "dividendos_payout", "recompras", "emision_acciones", "emision_deuda",
                "amortizacion_deuda", "principal_arrendamientos_financieros", "nuevos_arrendamientos_financieros",
                "tasa_arrendamientos_financieros", "tasa_revolvente", "tasa_rendimiento_caja",
                "amortizacion_intangibles", "caja_minima")
TASAS = ("tasa_interes", "tasa_arrendamientos_financieros", "tasa_revolvente", "tasa_rendimiento_caja")

CONVENCIONES = {
    "signos_flujo": "capex, dividendos, recompras, emision/amortizacion de deuda, principal de arrendamientos y "
                    "emision de acciones en valor absoluto; cfo/cfi/cff/efecto_cambiario/otros_* con signo de caja",
    "dias": "saldos finales / (ingresos o costo de ventas) x 365",
    "intereses": "tasa x promedio(saldo inicial, saldo final); circularidad resuelta por punto fijo",
    "d_y_a": "dentro de costos y gastos; toda la D&A reduce PPE salvo amortizacion_intangibles (otros_activos_lp)",
    "otros_saldos": "otros activos/pasivos e inversiones_cp constantes en la proyeccion",
    "cierre": "caja es la variable de cierre; faltante bajo caja_minima = revolvente (financiamiento requerido)",
    "fcf": "FCF = CFO - capex; FCF despues de arrendamientos = FCF - principal de arrendamientos financieros",
}


# ------------------------------------------------------------------ utilidades

def cargar_json(ruta) -> dict:
    return json.loads(Path(ruta).read_text(encoding="utf-8"))


def guardar_json(obj, ruta) -> None:
    Path(ruta).parent.mkdir(parents=True, exist_ok=True)
    Path(ruta).write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def sha256_archivo(ruta) -> str:
    h = hashlib.sha256()
    with open(ruta, "rb") as fh:
        for bloque in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def escribir_sha256sums(rutas, destino) -> str:
    """Escribe '<sha256>  <ruta relativa al directorio de destino>' (formato de sha256sum -c)."""
    destino = Path(destino)
    lineas = []
    for r in rutas:
        r = Path(r)
        try:
            nombre = r.resolve().relative_to(destino.resolve().parent).as_posix()
        except ValueError:
            nombre = r.as_posix()
        lineas.append(f"{sha256_archivo(r)}  {nombre}")
    texto = "\n".join(lineas) + "\n"
    destino.write_text(texto, encoding="utf-8")
    return texto


def _es_num(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def _dividir(a, b):
    return a / b if (a is not None and b) else None


def _tol(tolcfg: dict, tipo: str, escala) -> float:
    return max(tolcfg[f"{tipo}_abs"], tolcfg[f"{tipo}_rel"] * abs(escala or 0.0))


def _registro(cid, prueba, ambito, periodo, esperado, obtenido, tol, estado=None, detalle="") -> dict:
    dif = None
    if esperado is not None and obtenido is not None:
        dif = obtenido - esperado
    if estado is None:
        estado = "OK" if dif is not None and abs(dif) <= tol else "FALLA"
    return {"id": cid, "control": CONTROLES[cid], "prueba": prueba, "ambito": ambito, "periodo": periodo,
            "esperado": esperado, "obtenido": obtenido, "diferencia": dif, "tolerancia": tol,
            "estado": estado, "detalle": detalle}


# ------------------------------------------------------------------ validacion de la base

def _leer_num(d: dict, k: str, ruta: str, errores: list, requerido: bool):
    if k not in d or d[k] is None:
        if requerido:
            errores.append(f"{ruta}.{k}: falta (obligatorio)")
        return None
    v = d[k]
    if not _es_num(v):
        errores.append(f"{ruta}.{k}: se esperaba numero finito, se recibio {v!r}")
        return None
    return float(v)


def _leer_monto(d: dict, k: str, ruta: str, errores: list):
    """Numero o {concepto: numero}. Devuelve (total, detalle o None)."""
    if k not in d or d[k] is None:
        return None, None
    v = d[k]
    if isinstance(v, dict):
        if not v:
            errores.append(f"{ruta}.{k}: detalle vacio")
            return None, None
        det = {}
        for c, x in v.items():
            if not _es_num(x):
                errores.append(f"{ruta}.{k}.{c}: se esperaba numero finito, se recibio {x!r}")
                return None, None
            det[str(c)] = float(x)
        return sum(det.values()), det
    if not _es_num(v):
        errores.append(f"{ruta}.{k}: se esperaba numero o {{concepto: monto}}, se recibio {v!r}")
        return None, None
    return float(v), None


def _claves_desconocidas(d: dict, permitidas, ruta: str, errores: list) -> None:
    extra = sorted(set(d) - set(permitidas))
    if extra:
        errores.append(f"{ruta}: claves no reconocidas {extra} (revise ortografia; permitidas: {sorted(permitidas)})")


def _normalizar_bloque_mov(p: dict, nombre: str, ruta: str, errores: list):
    if nombre not in p or p[nombre] is None:
        return None
    blq = p[nombre]
    if not isinstance(blq, dict):
        errores.append(f"{ruta}.{nombre}: debe ser objeto")
        return None
    spec = BLOQUES_MOV[nombre]
    _claves_desconocidas(blq, spec["requeridos"] + spec["opcionales"] + ("fuente",), f"{ruta}.{nombre}", errores)
    out, det = {}, {}
    for k in spec["requeridos"]:
        out[k], d = _leer_monto(blq, k, f"{ruta}.{nombre}", errores)
        if out[k] is None and k not in blq:
            errores.append(f"{ruta}.{nombre}.{k}: falta (obligatorio en el bloque)")
        if d:
            det[k] = d
    for k in spec["opcionales"]:
        out[k], d = _leer_monto(blq, k, f"{ruta}.{nombre}", errores)
        if d:
            det[k] = d
    out["detalle"] = det
    out["fuente"] = blq.get("fuente")
    return out


def _normalizar_ajustado(p: dict, ruta: str, errores: list) -> list:
    if "ajustado" not in p or p["ajustado"] is None:
        return []
    items = p["ajustado"] if isinstance(p["ajustado"], list) else [p["ajustado"]]
    out = []
    for i, a in enumerate(items):
        r = f"{ruta}.ajustado[{i}]"
        if not isinstance(a, dict):
            errores.append(f"{r}: debe ser objeto")
            continue
        _claves_desconocidas(a, ("base", "ajustes", "valor_ajustado", "fuente", "nombre"), r, errores)
        base = a.get("base")
        if base not in RES_REQ + RES_OPC:
            errores.append(f"{r}.base: debe ser un campo de resultados, se recibio {base!r}")
        if not a.get("fuente"):
            errores.append(f"{r}.fuente: falta (cada ajuste necesita documento y pagina)")
        ajustes = a.get("ajustes")
        if not isinstance(ajustes, dict) or not ajustes or not all(_es_num(x) for x in ajustes.values()):
            errores.append(f"{r}.ajustes: debe ser {{concepto: monto}} no vacio")
            ajustes = {}
        va = a.get("valor_ajustado")
        if not _es_num(va):
            errores.append(f"{r}.valor_ajustado: se esperaba numero")
            va = None
        out.append({"nombre": a.get("nombre") or f"{base}_ajustada", "base": base,
                    "ajustes": {str(k): float(v) for k, v in ajustes.items()},
                    "valor_ajustado": None if va is None else float(va), "fuente": a.get("fuente")})
    return out


def _normalizar_periodo(p, i: int, errores: list) -> dict:
    ruta = f"historico[{i}]"
    if not isinstance(p, dict):
        errores.append(f"{ruta}: debe ser objeto")
        return {}
    _claves_desconocidas(p, CLAVES_PERIODO, ruta, errores)
    etiqueta = p.get("periodo")
    if not isinstance(etiqueta, str) or not etiqueta.strip():
        errores.append(f"{ruta}.periodo: falta etiqueta (p. ej. 'FY2025')")
        etiqueta = f"P{i}"
    ruta = f"historico[{i}] ({etiqueta})"
    if not p.get("fuente"):
        errores.append(f"{ruta}.fuente: falta (cero invencion: documento, pagina/nota y fecha)")
    anio = p.get("anio")
    if anio is not None and (not isinstance(anio, int) or isinstance(anio, bool)):
        errores.append(f"{ruta}.anio: debe ser entero")
        anio = None
    secciones = {}
    for sec, permitidas in (("resultados", RES_REQ + RES_OPC), ("balance", BAL_REQ + BAL_OPC),
                            ("flujo", FLUJO_REQ + FLUJO_CERO + FLUJO_DETALLE + FLUJO_OPC)):
        d = p.get(sec)
        if not isinstance(d, dict):
            errores.append(f"{ruta}.{sec}: falta o no es objeto")
            d = {}
        _claves_desconocidas(d, permitidas, f"{ruta}.{sec}", errores)
        secciones[sec] = d
    derivados, ceros = [], []

    r = {k: _leer_num(secciones["resultados"], k, f"{ruta}.resultados", errores, True) for k in RES_REQ}
    r.update({k: _leer_num(secciones["resultados"], k, f"{ruta}.resultados", errores, False) for k in RES_OPC})
    if r["ingresos"] is not None and r["ingresos"] <= 0:
        errores.append(f"{ruta}.resultados.ingresos: debe ser > 0 (motor no aplica a ingresos nulos)")
    if r["costo_ventas"] is not None and r["costo_ventas"] < 0:
        errores.append(f"{ruta}.resultados.costo_ventas: debe ser >= 0 (costo en valor absoluto)")

    b = {k: _leer_num(secciones["balance"], k, f"{ruta}.balance", errores, True) for k in BAL_REQ}
    b.update({k: _leer_num(secciones["balance"], k, f"{ruta}.balance", errores, False) for k in BAL_OPC})
    for k in BAL_CERO:
        if b[k] is None:
            b[k] = 0.0
            ceros.append(f"balance.{k}")
    for grupo, total, lista in ((BAL_RESIDUO_ACT, "activo_total", ACTIVOS), (BAL_RESIDUO_PAS, "pasivo_total", PASIVOS)):
        faltan = [k for k in grupo if b[k] is None]
        if not faltan or b[total] is None or any(b[k] is None for k in lista if k not in grupo):
            continue
        conocido = sum(b[k] for k in lista if b[k] is not None)
        if len(faltan) == 2:
            b[grupo[0]] = 0.0
            b[grupo[1]] = b[total] - conocido
            derivados.append(f"balance.{grupo[1]} = {total} - suma de componentes reportados "
                             f"({b[grupo[1]]:.6g}); balance.{grupo[0]} = 0")
        else:
            b[faltan[0]] = b[total] - conocido
            derivados.append(f"balance.{faltan[0]} = {total} - suma de componentes reportados ({b[faltan[0]]:.6g})")

    f = {k: _leer_num(secciones["flujo"], k, f"{ruta}.flujo", errores, True) for k in FLUJO_REQ}
    for k in FLUJO_CERO:
        f[k] = _leer_num(secciones["flujo"], k, f"{ruta}.flujo", errores, False)
        if f[k] is None:
            f[k] = 0.0
            ceros.append(f"flujo.{k}")
    detalle = {}
    for k in FLUJO_DETALLE:
        f[k], d = _leer_monto(secciones["flujo"], k, f"{ruta}.flujo", errores)
        if d:
            detalle[f"flujo.{k}"] = d
    f.update({k: _leer_num(secciones["flujo"], k, f"{ruta}.flujo", errores, False) for k in FLUJO_OPC})
    for k in PAGOS_NO_NEGATIVOS:
        if f.get(k) is not None and f[k] < 0:
            errores.append(f"{ruta}.flujo.{k}: debe ser >= 0 (pago o cobro en valor absoluto); se recibio {f[k]}")

    fc = p.get("fuentes_campos") or {}
    if not isinstance(fc, dict):
        errores.append(f"{ruta}.fuentes_campos: debe ser objeto")
        fc = {}
    validas = {f"{s}.{k}" for s, ks in (("resultados", RES_REQ + RES_OPC), ("balance", BAL_REQ + BAL_OPC),
                                         ("flujo", FLUJO_REQ + FLUJO_CERO + FLUJO_DETALLE + FLUJO_OPC)) for k in ks}
    malas = sorted(set(fc) - validas - {f"{blq}.{k}" for blq, spec in BLOQUES_MOV.items()
                                        for k in spec["requeridos"] + spec["opcionales"]})
    if malas:
        errores.append(f"{ruta}.fuentes_campos: campos inexistentes {malas}")

    movs = {n: _normalizar_bloque_mov(p, n, ruta, errores) for n in BLOQUES_MOV}
    return {"periodo": etiqueta, "anio": anio, "fin": p.get("fin"), "fuente": p.get("fuente"),
            "fuentes_campos": fc, "naturaleza": "hecho (filing)",
            "resultados": r, "balance": b, "flujo": f, "detalle": detalle, **movs,
            "ajustado": _normalizar_ajustado(p, ruta, errores), "memo": p.get("memo") or {},
            "notas": p.get("notas"), "derivados": derivados, "ceros_por_omision": ceros}


def normalizar_base(base: dict) -> dict:
    """Valida la base historica y devuelve una copia normalizada (floats; None = no reportado).

    Lanza ValueError con TODOS los errores encontrados (claves desconocidas, signos, faltantes)."""
    if not isinstance(base, dict):
        raise ValueError("La base debe ser un objeto JSON")
    errores = []
    for k in ("empresa", "moneda", "unidades"):
        if not base.get(k):
            errores.append(f"falta '{k}'")
    hist = base.get("historico")
    if not isinstance(hist, list) or len(hist) < 2:
        errores.append("'historico' debe ser lista con al menos 2 ejercicios en orden cronologico")
        hist = hist if isinstance(hist, list) else []
    periodos = [_normalizar_periodo(p, i, errores) for i, p in enumerate(hist)]
    etiquetas = [p.get("periodo") for p in periodos]
    if len(set(etiquetas)) != len(etiquetas):
        errores.append(f"etiquetas de periodo repetidas: {etiquetas}")
    fines = [p.get("fin") for p in periodos]
    if fines and all(isinstance(x, str) for x in fines) and (fines != sorted(fines) or len(set(fines)) != len(fines)):
        errores.append(f"'historico' no esta en orden cronologico estricto por 'fin': {fines}")
    anios = [p.get("anio") for p in periodos]
    if anios and all(isinstance(a, int) for a in anios) and any(b <= a for a, b in zip(anios, anios[1:])):
        errores.append(f"'historico' no esta en orden cronologico estricto por 'anio': {anios}")
    tol = dict(TOLERANCIAS_DEFECTO)
    tin = base.get("tolerancias") or {}
    if not isinstance(tin, dict):
        errores.append("'tolerancias' debe ser objeto")
        tin = {}
    for k, v in tin.items():
        if k not in TOLERANCIAS_DEFECTO:
            errores.append(f"tolerancias.{k}: clave no reconocida")
        elif not _es_num(v) or v < 0:
            errores.append(f"tolerancias.{k}: debe ser numero >= 0")
        else:
            tol[k] = float(v)
    if errores:
        raise ValueError("Base invalida:\n- " + "\n- ".join(errores))
    return {"empresa": base["empresa"], "ticker": base.get("ticker"), "moneda": base["moneda"],
            "unidades": base["unidades"], "fecha_corte": base.get("fecha_corte"),
            "fuentes": base.get("fuentes") or {}, "tolerancias": tol, "periodos": periodos}


# ------------------------------------------------------------------ supuestos

def resolver_supuestos(esc: dict, anos: int, caja_minima_global=None, nombre: str = "") -> list[dict]:
    """Expande un escenario a una lista de 'anos' diccionarios (escalar = constante; lista = por ano)."""
    ruta = f"escenario '{nombre}'"
    if not isinstance(esc, dict):
        raise ValueError(f"{ruta}: debe ser objeto")
    errores = []
    permitidas = set(SUPUESTOS_REQ) | set(SUPUESTOS_OPC) | set(SUPUESTOS_META)
    _claves_desconocidas(esc, permitidas, ruta, errores)
    if not esc.get("descripcion"):
        errores.append(f"{ruta}.descripcion: falta (describa el escenario; no es pronostico)")
    for k in SUPUESTOS_REQ:
        if k not in esc:
            errores.append(f"{ruta}.{k}: falta (obligatorio)")
    if esc.get("dividendos") is not None and esc.get("dividendos_payout") is not None:
        errores.append(f"{ruta}: use 'dividendos' (monto) o 'dividendos_payout' (fraccion), no ambos")
    if errores:
        raise ValueError("Supuestos invalidos:\n- " + "\n- ".join(errores))

    def serie(k, defecto):
        v = esc.get(k, defecto)
        if v is None:
            return [None] * anos
        if isinstance(v, list):
            if len(v) != anos:
                errores.append(f"{ruta}.{k}: la lista tiene {len(v)} valores y 'anos' = {anos}")
                return [None] * anos
            vals = v
        else:
            vals = [v] * anos
        for x in vals:
            if not _es_num(x):
                errores.append(f"{ruta}.{k}: se esperaba numero, se recibio {x!r}")
                return [None] * anos
        return [float(x) for x in vals]

    columnas = {k: serie(k, None) for k in SUPUESTOS_REQ}
    columnas.update({k: serie(k, d) for k, d in SUPUESTOS_OPC.items()})
    if columnas["caja_minima"][0] is None:
        if caja_minima_global is None or not _es_num(caja_minima_global):
            errores.append(f"{ruta}.caja_minima: declare caja_minima (global o por escenario; puede ser 0)")
        else:
            columnas["caja_minima"] = [float(caja_minima_global)] * anos
    if columnas["tasa_revolvente"][0] is None:
        columnas["tasa_revolvente"] = list(columnas["tasa_interes"])
    anos_lista = []
    for t in range(anos):
        s = {k: columnas[k][t] for k in columnas}
        et = f"{ruta} ano {t + 1}"
        for k in NO_NEGATIVOS:
            if s.get(k) is not None and s[k] < 0:
                errores.append(f"{et}: {k} debe ser >= 0 (se recibio {s[k]})")
        if s["crecimiento_ingresos"] is not None and s["crecimiento_ingresos"] <= -1:
            errores.append(f"{et}: crecimiento_ingresos debe ser > -1")
        for k in ("margen_bruto", "margen_operativo"):
            if s[k] is not None and s[k] > 1:
                errores.append(f"{et}: {k} debe ser <= 1")
        if s["tasa_impuestos"] is not None and not 0 <= s["tasa_impuestos"] < 1:
            errores.append(f"{et}: tasa_impuestos debe estar en [0, 1)")
        for k in TASAS:
            if s[k] is not None and s[k] >= 1:
                errores.append(f"{et}: {k} debe ser < 1 (fraccion anual)")
        if not 0 <= s["recompras_contra_utilidades_retenidas"] <= 1:
            errores.append(f"{et}: recompras_contra_utilidades_retenidas debe estar en [0, 1]")
        anos_lista.append(s)
    if errores:
        raise ValueError("Supuestos invalidos:\n- " + "\n- ".join(errores))
    return anos_lista


# ------------------------------------------------------------------ motor

def _apertura(bal: dict) -> dict:
    ap = {k: float(bal.get(k) or 0.0) for k in ACTIVOS + PASIVOS}
    ap["capital_contable"] = float(bal["capital_contable"])
    ure = bal.get("utilidades_retenidas")
    ap["utilidades_retenidas"] = None if ure is None else float(ure)
    return ap


def _periodo(ap: dict, ing_prev: float, s: dict, caja_minima, exo: dict | None = None) -> dict:
    """Un ano del modelo integrado. 'ap' = balance de apertura; 's' = supuestos resueltos del ano.

    caja_minima=None desactiva el revolvente (modo reconciliacion del historico). 'exo' solo lo usa
    la reconciliacion del historico (partidas conciliatorias explicitas); en proyeccion es vacio."""
    exo = exo or {}
    nm = exo.get("no_monetario", {})
    oo = exo.get("otros_operativos", 0.0)
    oi = exo.get("otros_inversion", 0.0)
    of = exo.get("otros_financiamiento", 0.0)
    fx = exo.get("efecto_cambiario", 0.0)
    otros_desp = exo.get("otros_despues_impuestos", 0.0)

    ing = ing_prev * (1.0 + s["crecimiento_ingresos"])
    ub = ing * s["margen_bruto"]
    cv = ing - ub
    uo = ing * s["margen_operativo"]
    gop = ub - uo
    da = ing * s["da_ventas"]
    sbc = ing * s["sbc_ventas"]
    capex = ing * s["capex_ventas"]
    amort_int = s["amortizacion_intangibles"]
    dep_ppe = da - amort_int

    cxc = s["dias_cxc"] * ing / DIAS_ANO
    inv = s["dias_inventario"] * cv / DIAS_ANO
    prov = s["dias_proveedores"] * cv / DIAS_ANO

    emi_d, amo_d = s["emision_deuda"], s["amortizacion_deuda"]
    deuda = ap["deuda"] + emi_d - amo_d + nm.get("deuda", 0.0)
    nuevos_arr, princ_arr = s["nuevos_arrendamientos_financieros"], s["principal_arrendamientos_financieros"]
    arr = ap["arrendamientos_financieros"] + nuevos_arr - princ_arr + nm.get("arrendamientos_financieros", 0.0)
    ppe = ap["ppe_neto"] + capex + nuevos_arr - dep_ppe + nm.get("ppe_neto", 0.0)
    inv_cp = ap["inversiones_cp"] + nm.get("inversiones_cp", 0.0)
    oac = ap["otros_activos_circulantes"] + nm.get("otros_activos_circulantes", 0.0)
    oalp = ap["otros_activos_lp"] - amort_int - oi + nm.get("otros_activos_lp", 0.0)
    opc = ap["otros_pasivos_circulantes"] + nm.get("otros_pasivos_circulantes", 0.0)
    oplp = ap["otros_pasivos_lp"] + oo + of + nm.get("otros_pasivos_lp", 0.0)
    rev_ini = ap["revolvente"]
    rev_base = rev_ini + nm.get("revolvente", 0.0)
    caja_ini = ap["caja"]
    rec, emi_a = s["recompras"], s["emision_acciones"]

    d_cxc = -(cxc - ap["cuentas_por_cobrar"])
    d_inv = -(inv - ap["inventarios"])
    d_prov = prov - ap["proveedores"]
    d_ct = d_cxc + d_inv + d_prov

    rev_fin, caja_fin = rev_base, caja_ini
    escala = max(1.0, abs(ing))
    for it in range(1, MAX_ITER_CIRCULAR + 1):
        gi = (s["tasa_interes"] * (ap["deuda"] + deuda) / 2
              + s["tasa_arrendamientos_financieros"] * (ap["arrendamientos_financieros"] + arr) / 2
              + s["tasa_revolvente"] * (rev_ini + rev_fin) / 2)
        ii = s["tasa_rendimiento_caja"] * ((caja_ini + ap["inversiones_cp"]) + (caja_fin + inv_cp)) / 2
        uai = uo - gi + ii + s["otros_ingresos"]
        imp = s["tasa_impuestos"] * uai
        un = uai - imp + otros_desp
        div = s["dividendos_payout"] * max(un, 0.0) if s["dividendos_payout"] is not None else s["dividendos"]
        cfo = un + da + sbc + d_ct + oo
        cfi = -capex + oi
        cff_sin_rev = emi_d - amo_d - princ_arr - div - rec + emi_a + of
        caja_pre = caja_ini + cfo + cfi + cff_sin_rev + fx
        if caja_minima is None:
            disp = pago = 0.0
        else:
            disp = max(0.0, caja_minima - caja_pre)
            pago = min(rev_base, max(0.0, caja_pre - caja_minima))
        nuevo_rev = rev_base + disp - pago
        nueva_caja = caja_pre + disp - pago
        delta = abs(nuevo_rev - rev_fin) + abs(nueva_caja - caja_fin)
        rev_fin, caja_fin = nuevo_rev, nueva_caja
        if delta <= TOL_CIRCULAR * escala:
            break
    else:
        raise RuntimeError("La circularidad intereses-caja-revolvente no convergio; revise tasas")
    # Recalculo final con los saldos convergidos: todas las lineas quedan mutuamente consistentes.
    gi = (s["tasa_interes"] * (ap["deuda"] + deuda) / 2
          + s["tasa_arrendamientos_financieros"] * (ap["arrendamientos_financieros"] + arr) / 2
          + s["tasa_revolvente"] * (rev_ini + rev_fin) / 2)
    ii = s["tasa_rendimiento_caja"] * ((caja_ini + ap["inversiones_cp"]) + (caja_fin + inv_cp)) / 2
    uai = uo - gi + ii + s["otros_ingresos"]
    imp = s["tasa_impuestos"] * uai
    un = uai - imp + otros_desp
    div = s["dividendos_payout"] * max(un, 0.0) if s["dividendos_payout"] is not None else s["dividendos"]
    cfo = un + da + sbc + d_ct + oo
    cff = emi_d - amo_d - princ_arr - div - rec + emi_a + of + disp - pago
    caja_fin = caja_ini + cfo + cfi + cff + fx

    otros_cap = exo.get("otros_capital", 0.0)
    capital = ap["capital_contable"] + un + sbc - div - rec + emi_a + otros_cap
    f_ure = s["recompras_contra_utilidades_retenidas"]
    if ap["utilidades_retenidas"] is None:
        ure = None
    else:
        ure = ap["utilidades_retenidas"] + un - div - rec * f_ure + exo.get("otros_ure", 0.0)

    balance = {"caja": caja_fin, "inversiones_cp": inv_cp, "cuentas_por_cobrar": cxc, "inventarios": inv,
               "otros_activos_circulantes": oac, "ppe_neto": ppe, "otros_activos_lp": oalp,
               "proveedores": prov, "otros_pasivos_circulantes": opc, "deuda": deuda,
               "arrendamientos_financieros": arr, "revolvente": rev_fin, "otros_pasivos_lp": oplp}
    balance["activo_total"] = sum(balance[k] for k in ACTIVOS)
    balance["pasivo_total"] = sum(balance[k] for k in PASIVOS)
    balance["capital_contable"] = capital
    balance["utilidades_retenidas"] = ure
    fcf = cfo - capex
    return {
        "resultados": {"ingresos": ing, "costo_ventas": cv, "utilidad_bruta": ub, "gastos_operativos": gop,
                       "utilidad_operativa": uo, "gasto_intereses": gi, "ingreso_intereses": ii,
                       "otros_ingresos": s["otros_ingresos"], "utilidad_antes_impuestos": uai, "impuestos": imp,
                       "otros_despues_impuestos": otros_desp, "utilidad_neta": un,
                       "depreciacion_amortizacion": da, "sbc": sbc, "ebitda": uo + da},
        "balance": balance,
        "flujo": {"utilidad_neta": un, "depreciacion_amortizacion": da, "sbc": sbc, "cambio_cxc": d_cxc,
                  "cambio_inventarios": d_inv, "cambio_proveedores": d_prov, "cambio_capital_trabajo": d_ct,
                  "otros_operativos": oo, "cfo": cfo, "capex": capex, "otros_inversion": oi, "cfi": cfi,
                  "emision_deuda": emi_d, "amortizacion_deuda": amo_d,
                  "principal_arrendamientos_financieros": princ_arr, "disposicion_revolvente": disp,
                  "pago_revolvente": pago, "dividendos": div, "recompras": rec, "emision_acciones": emi_a,
                  "otros_financiamiento": of, "cff": cff, "efecto_cambiario": fx, "caja_inicial": caja_ini,
                  "caja_final": caja_fin, "fcf": fcf, "fcf_despues_arrendamientos": fcf - princ_arr},
        "movimientos": {
            "capital": {"capital_inicial": ap["capital_contable"], "utilidad_neta": un, "sbc": sbc,
                        "dividendos": div, "recompras": rec, "emision_acciones": emi_a, "otros": otros_cap,
                        "capital_final": capital, "utilidades_retenidas_iniciales": ap["utilidades_retenidas"],
                        "recompras_contra_utilidades_retenidas": rec * f_ure,
                        "otros_utilidades_retenidas": exo.get("otros_ure", 0.0), "utilidades_retenidas_finales": ure},
            "ppe": {"ppe_inicial": ap["ppe_neto"], "capex": capex, "nuevos_arrendamientos_financieros": nuevos_arr,
                    "depreciacion_ppe": dep_ppe, "amortizacion_intangibles": amort_int,
                    "otros": nm.get("ppe_neto", 0.0), "ppe_final": ppe},
            "deuda": {"deuda_inicial": ap["deuda"], "emisiones": emi_d, "amortizaciones": amo_d,
                      "otros": nm.get("deuda", 0.0), "deuda_final": deuda},
            "arrendamientos": {"inicial": ap["arrendamientos_financieros"], "nuevos": nuevos_arr,
                               "principal": princ_arr, "otros": nm.get("arrendamientos_financieros", 0.0),
                               "final": arr},
            "revolvente": {"inicial": rev_ini, "disposiciones": disp, "pagos": pago,
                           "otros": nm.get("revolvente", 0.0), "final": rev_fin},
        },
        "iteraciones_circularidad": it,
    }


def _etiqueta_proyeccion(ultimo: dict, k: int) -> str:
    if isinstance(ultimo.get("anio"), int):
        return f"{ultimo['anio'] + k}E"
    return f"{ultimo['periodo']}+{k}"


def proyectar_escenario(ultimo: dict, nombre: str, esc: dict, anos: int, caja_minima_global=None) -> dict:
    """Proyecta un escenario desde el ultimo periodo historico normalizado."""
    sups = resolver_supuestos(esc, anos, caja_minima_global, nombre)
    ap = _apertura(ultimo["balance"])
    ing_prev = ultimo["resultados"]["ingresos"]
    periodos, alertas = [], []
    for k, s in enumerate(sups, 1):
        etq = _etiqueta_proyeccion(ultimo, k)
        if ap["deuda"] + s["emision_deuda"] - s["amortizacion_deuda"] < -1e-9:
            raise ValueError(f"escenario '{nombre}' {etq}: amortizacion_deuda ({s['amortizacion_deuda']}) excede la "
                             f"deuda disponible ({ap['deuda'] + s['emision_deuda']})")
        if ap["arrendamientos_financieros"] + s["nuevos_arrendamientos_financieros"] - \
                s["principal_arrendamientos_financieros"] < -1e-9:
            raise ValueError(f"escenario '{nombre}' {etq}: principal_arrendamientos_financieros excede el saldo")
        p = _periodo(ap, ing_prev, s, s["caja_minima"])
        p["periodo"] = etq
        p["naturaleza"] = "supuesto de escenario"
        p["supuestos"] = s
        r, b, f = p["resultados"], p["balance"], p["flujo"]
        met = {"crecimiento_ingresos": s["crecimiento_ingresos"], "margen_bruto": _dividir(r["utilidad_bruta"], r["ingresos"]),
               "margen_operativo": _dividir(r["utilidad_operativa"], r["ingresos"]),
               "margen_neto": _dividir(r["utilidad_neta"], r["ingresos"]),
               "fcf_ventas": _dividir(f["fcf"], r["ingresos"]),
               "deuda_neta": b["deuda"] + b["arrendamientos_financieros"] + b["revolvente"] - b["caja"] - b["inversiones_cp"],
               "financiamiento_requerido": f["disposicion_revolvente"]}
        if s["ajuste_utilidad_neta"] is not None:
            met["ajuste_utilidad_neta"] = s["ajuste_utilidad_neta"]
            met["utilidad_neta_ajustada"] = r["utilidad_neta"] + s["ajuste_utilidad_neta"]
        p["metricas"] = met
        if s["margen_operativo"] > s["margen_bruto"]:
            alertas.append(f"{etq}: margen_operativo > margen_bruto (gastos operativos negativos)")
        if b["ppe_neto"] < 0:
            alertas.append(f"{etq}: PPE neto negativo ({b['ppe_neto']:.6g}); revise capex_ventas vs da_ventas")
        if b["otros_activos_lp"] < 0:
            alertas.append(f"{etq}: otros_activos_lp negativo; amortizacion_intangibles excede el saldo")
        if f["disposicion_revolvente"] > 0:
            alertas.append(f"{etq}: FINANCIAMIENTO REQUERIDO {f['disposicion_revolvente']:.6g} (revolvente) para "
                           f"mantener caja_minima {s['caja_minima']:.6g}")
        if r["utilidad_antes_impuestos"] < 0:
            alertas.append(f"{etq}: UAI negativa; el impuesto lineal registra beneficio fiscal (supuesto)")
        if b["capital_contable"] < 0:
            alertas.append(f"{etq}: capital contable negativo")
        periodos.append(p)
        ap = _apertura(b)
        ing_prev = r["ingresos"]
    ing0 = ultimo["resultados"]["ingresos"]
    ingf = periodos[-1]["resultados"]["ingresos"]
    resumen = {
        "anos": anos,
        "ingresos_final": ingf,
        "cagr_ingresos": (ingf / ing0) ** (1 / anos) - 1 if ing0 > 0 and ingf > 0 else None,
        "utilidad_neta_acumulada": sum(p["resultados"]["utilidad_neta"] for p in periodos),
        "fcf_acumulado": sum(p["flujo"]["fcf"] for p in periodos),
        "fcf_despues_arrendamientos_acumulado": sum(p["flujo"]["fcf_despues_arrendamientos"] for p in periodos),
        "dividendos_acumulados": sum(p["flujo"]["dividendos"] for p in periodos),
        "recompras_acumuladas": sum(p["flujo"]["recompras"] for p in periodos),
        "financiamiento_requerido_total": sum(p["flujo"]["disposicion_revolvente"] for p in periodos),
        "revolvente_maximo": max(p["balance"]["revolvente"] for p in periodos),
        "periodos_con_financiamiento": [p["periodo"] for p in periodos if p["flujo"]["disposicion_revolvente"] > 0],
        "caja_final": periodos[-1]["balance"]["caja"],
        "deuda_neta_final": periodos[-1]["metricas"]["deuda_neta"],
    }
    return {"naturaleza": "supuesto de escenario: no es pronostico, guia ni consenso",
            "descripcion": esc.get("descripcion"), "fuente_supuestos": esc.get("fuente_supuestos"),
            "notas": esc.get("notas"), "supuestos_entrada": copy.deepcopy(esc), "periodos": periodos,
            "resumen": resumen, "alertas": alertas}


# ------------------------------------------------------------------ historico: drivers y reconciliacion

def _ub(r: dict) -> float:
    return r["utilidad_bruta"] if r.get("utilidad_bruta") is not None else r["ingresos"] - r["costo_ventas"]


def drivers_implicitos(cur: dict, prev: dict | None = None) -> dict:
    """Drivers implicitos de un periodo historico (calculo sobre hechos, no supuestos)."""
    r, b, f = cur["resultados"], cur["balance"], cur["flujo"]
    ing, cv = r["ingresos"], r["costo_ventas"]
    d = {"naturaleza": "calculo sobre hechos",
         "margen_bruto": _dividir(ing - cv, ing), "margen_operativo": _dividir(r["utilidad_operativa"], ing),
         "margen_neto": _dividir(r["utilidad_neta"], ing),
         "tasa_impuestos": _dividir(r["impuestos"], r["utilidad_antes_impuestos"]),
         "da_ventas": _dividir(f["depreciacion_amortizacion"], ing), "capex_ventas": _dividir(f["capex"], ing),
         "sbc_ventas": _dividir(f["sbc"], ing),
         "dias_cxc": _dividir(b["cuentas_por_cobrar"] * DIAS_ANO, ing),
         "dias_inventario": _dividir(b["inventarios"] * DIAS_ANO, cv),
         "dias_proveedores": _dividir(b["proveedores"] * DIAS_ANO, cv),
         "fcf": f["cfo"] - f["capex"], "fcf_despues_arrendamientos": f["cfo"] - f["capex"] - f["principal_arrendamientos_financieros"],
         "fcf_ventas": _dividir(f["cfo"] - f["capex"], ing),
         "payout_dividendos": _dividir(f["dividendos"], r["utilidad_neta"]) if r["utilidad_neta"] > 0 else None,
         "crecimiento_ingresos": None, "tasa_interes_sobre_deuda": None,
         "tasa_interes_sobre_deuda_y_arrendamientos": None}
    if prev is not None:
        bp = prev["balance"]
        d["crecimiento_ingresos"] = _dividir(ing, prev["resultados"]["ingresos"]) - 1
        prom = (bp["deuda"] + b["deuda"]) / 2
        d["tasa_interes_sobre_deuda"] = _dividir(r["gasto_intereses"], prom)
        prom2 = prom + (bp["arrendamientos_financieros"] + b["arrendamientos_financieros"]
                        + bp["revolvente"] + b["revolvente"]) / 2
        d["tasa_interes_sobre_deuda_y_arrendamientos"] = _dividir(r["gasto_intereses"], prom2)
    return d


LINEAS_FORZADAS = ("inversiones_cp", "otros_activos_circulantes", "otros_activos_lp", "ppe_neto",
                   "otros_pasivos_circulantes", "otros_pasivos_lp", "deuda", "arrendamientos_financieros",
                   "revolvente")
LINEAS_COMPARADAS = (("resultados", "ingresos"), ("resultados", "utilidad_bruta"), ("resultados", "utilidad_operativa"),
                     ("resultados", "gasto_intereses"), ("resultados", "utilidad_antes_impuestos"),
                     ("resultados", "impuestos"), ("resultados", "utilidad_neta"),
                     ("flujo", "cfo"), ("flujo", "cfi"), ("flujo", "cff"),
                     ("balance", "caja"), ("balance", "cuentas_por_cobrar"), ("balance", "inventarios"),
                     ("balance", "proveedores"), ("balance", "ppe_neto"), ("balance", "deuda"),
                     ("balance", "arrendamientos_financieros"), ("balance", "capital_contable"),
                     ("balance", "activo_total"), ("balance", "pasivo_total"))


def reconciliar_periodo(prev: dict, cur: dict, tolcfg: dict) -> dict:
    """C13: corre el MISMO motor (_periodo) desde el balance reportado de 'prev' con los drivers implicitos
    de 'cur' y compara contra lo reportado. Lo que el motor no explica entra como partida conciliatoria
    EXPLICITA (con monto y % de ingresos), nunca como plug oculto."""
    r, b, f = cur["resultados"], cur["balance"], cur["flujo"]
    bp = prev["balance"]
    ap = _apertura(bp)
    ing, ing_p, cv = r["ingresos"], prev["resultados"]["ingresos"], r["costo_ventas"]
    notas = []
    base_int = (bp["deuda"] + b["deuda"] + bp["arrendamientos_financieros"] + b["arrendamientos_financieros"]
                + bp["revolvente"] + b["revolvente"]) / 2
    if base_int > 0:
        tasa = r["gasto_intereses"] / base_int
    else:
        tasa = 0.0
        if r["gasto_intereses"]:
            notas.append("gasto de intereses sin deuda promedio: el motor no puede reproducir esa linea")
    uai = r["utilidad_antes_impuestos"]
    otros_desp = r.get("otros_despues_impuestos") or 0.0
    if uai:
        tasa_imp = r["impuestos"] / uai
    else:
        tasa_imp = 0.0
        if r["impuestos"]:
            notas.append("UAI = 0 con impuestos distintos de 0: no hay tasa implicita")
    nuevos_arr = b["arrendamientos_financieros"] - bp["arrendamientos_financieros"] + f["principal_arrendamientos_financieros"]
    mc = cur.get("movimientos_capital")
    f_ure = 1.0
    if mc and mc.get("recompras_contra_utilidades_retenidas") is not None and f["recompras"]:
        f_ure = mc["recompras_contra_utilidades_retenidas"] / f["recompras"]
    s = {"crecimiento_ingresos": ing / ing_p - 1, "margen_bruto": (ing - cv) / ing,
         "margen_operativo": r["utilidad_operativa"] / ing, "tasa_impuestos": tasa_imp,
         "da_ventas": f["depreciacion_amortizacion"] / ing, "capex_ventas": f["capex"] / ing,
         "sbc_ventas": f["sbc"] / ing, "dias_cxc": b["cuentas_por_cobrar"] * DIAS_ANO / ing,
         "dias_inventario": b["inventarios"] * DIAS_ANO / cv if cv else 0.0,
         "dias_proveedores": b["proveedores"] * DIAS_ANO / cv if cv else 0.0,
         "tasa_interes": tasa, "tasa_arrendamientos_financieros": tasa, "tasa_revolvente": tasa,
         "tasa_rendimiento_caja": 0.0, "otros_ingresos": 0.0,
         "dividendos": f["dividendos"], "dividendos_payout": None, "recompras": f["recompras"],
         "emision_acciones": f["emision_acciones"], "emision_deuda": f["emision_deuda"],
         "amortizacion_deuda": f["amortizacion_deuda"],
         "principal_arrendamientos_financieros": f["principal_arrendamientos_financieros"],
         "nuevos_arrendamientos_financieros": nuevos_arr, "amortizacion_intangibles": 0.0,
         "recompras_contra_utilidades_retenidas": f_ure}
    if not cv and (b["inventarios"] or b["proveedores"]):
        notas.append("costo de ventas = 0 con inventario/proveedores: dias no definidos")
    # Capital: derivado del estado de variaciones si existe (prueba real); si no, partida conciliatoria.
    capital_forzado = mc is None
    otros_capital = 0.0
    if mc is not None:
        un_mov = mc["utilidad_neta"] if mc.get("utilidad_neta") is not None else r["utilidad_neta"]
        sbc_mov = mc["sbc"] if mc.get("sbc") is not None else f["sbc"]
        emi_mov = mc["emision_acciones"] if mc.get("emision_acciones") is not None else f["emision_acciones"]
        otros_capital = ((un_mov - r["utilidad_neta"]) + (sbc_mov - f["sbc"])
                         - ((mc["dividendos_declarados"] or 0.0) - f["dividendos"])
                         - ((mc["recompras"] or 0.0) - f["recompras"]) + (emi_mov - f["emision_acciones"])
                         + (mc.get("ori") or 0.0) + (mc.get("otros") or 0.0))
    exo = {"otros_operativos": 0.0, "otros_inversion": 0.0, "otros_financiamiento": 0.0,
           "efecto_cambiario": f["efecto_cambiario"], "otros_despues_impuestos": otros_desp,
           "otros_capital": otros_capital, "otros_ure": 0.0, "no_monetario": {k: 0.0 for k in LINEAS_FORZADAS}}
    escala = max(1.0, abs(ing))
    for pasada in range(1, MAX_PASADAS_REPLAY + 1):
        out = _periodo(ap, ing_p, s, None, exo)
        ro, bo, fo = out["resultados"], out["balance"], out["flujo"]
        ajustes = []
        # otros_ingresos: cierra UAI reportada dados UO e intereses del motor
        d = (uai - ro["utilidad_antes_impuestos"])
        s["otros_ingresos"] += d
        ajustes.append(d)
        for clave, rep, mod in (("otros_operativos", f["cfo"], fo["cfo"]), ("otros_inversion", f["cfi"], fo["cfi"]),
                                ("otros_financiamiento", f["cff"], fo["cff"])):
            exo[clave] += rep - mod
            ajustes.append(rep - mod)
        for k in LINEAS_FORZADAS:
            dd = (b[k] or 0.0) - bo[k]
            exo["no_monetario"][k] += dd
            ajustes.append(dd)
        if capital_forzado:
            dd = b["capital_contable"] - bo["capital_contable"]
            exo["otros_capital"] += dd
            ajustes.append(dd)
        if b.get("utilidades_retenidas") is not None and bo["utilidades_retenidas"] is not None:
            dd = b["utilidades_retenidas"] - bo["utilidades_retenidas"]
            exo["otros_ure"] += dd
            ajustes.append(dd)
        if max(abs(x) for x in ajustes) <= 1e-10 * escala:
            break
    else:
        notas.append("la reconciliacion no convergio en el numero maximo de pasadas")
    tol = _tol(tolcfg, "historico", ing)
    comparacion, peor = [], 0.0
    for sec, k in LINEAS_COMPARADAS:
        if sec == "resultados" and k == "utilidad_bruta":
            rep = _ub(r)
        else:
            rep = cur[sec][k]
        mod = out[sec][k]
        dif = mod - rep
        peor = max(peor, abs(dif))
        comparacion.append({"linea": f"{sec}.{k}", "reportado": rep, "modelo": mod, "diferencia": dif,
                            "ok": abs(dif) <= tol})
    ident = bo["activo_total"] - bo["pasivo_total"] - bo["capital_contable"]
    comparacion.append({"linea": "balance.activo - pasivo - capital (modelo)", "reportado": 0.0, "modelo": ident,
                        "diferencia": ident, "ok": abs(ident) <= tol})
    peor = max(peor, abs(ident))
    mat = tolcfg["materialidad_conciliatoria"]
    partidas = []

    def partida(nombre, monto, origen, reportado=None):
        pct = monto / ing if ing else None
        partidas.append({"partida": nombre, "monto": monto, "pct_ingresos": pct, "origen": origen,
                         "reportado_en_filing": reportado,
                         "material": pct is not None and abs(pct) > mat})

    partida("otros_ingresos (UAI - UO + intereses; incluye ingreso financiero)", s["otros_ingresos"], "implicito",
            r.get("otros_ingresos"))
    partida("otros_operativos del CFO (incluye diferencia capital de trabajo balance vs flujo)",
            exo["otros_operativos"], "implicito", f.get("otros_operativos"))
    partida("otros_inversion (CFI + capex)", exo["otros_inversion"], "implicito", f.get("otros_inversion"))
    partida("otros_financiamiento (CFF - componentes)", exo["otros_financiamiento"], "implicito",
            f.get("otros_financiamiento"))
    partida("efecto_cambiario", f["efecto_cambiario"], "reportado")
    ma = cur.get("movimientos_arrendamientos")
    partida("nuevos arrendamientos financieros (saldo final - inicial + principal)", nuevos_arr, "implicito",
            ma["nuevos"] if ma else None)
    for k in LINEAS_FORZADAS:
        partida(f"movimiento no monetario / no explicado en {k}", exo["no_monetario"][k], "residuo explicito")
    partida("capital: " + ("ORI + otros + diferencias devengado vs pagado (del estado de variaciones)"
                           if not capital_forzado else "movimientos no identificados (falta movimientos_capital)"),
            exo["otros_capital"], "derivado de movimientos_capital" if not capital_forzado else "residuo explicito")
    if b.get("utilidades_retenidas") is not None:
        partida("utilidades retenidas: movimientos distintos de utilidad, dividendos pagados y recompras",
                exo["otros_ure"], "residuo explicito")
    lineas_mal = [c["linea"] for c in comparacion if not c["ok"]]
    materiales = [f"{p['partida']} = {p['monto']:.6g} ({100 * p['pct_ingresos']:.2f}% ingresos)"
                  for p in partidas if p["material"]]
    return {"periodo": cur["periodo"], "naturaleza": "calculo sobre hechos", "pasadas": pasada,
            "supuestos_implicitos": dict(s), "comparacion": comparacion, "max_diferencia": peor,
            "tolerancia": tol, "lineas_fuera_de_tolerancia": lineas_mal, "partidas_conciliatorias": partidas,
            "alertas_materialidad": materiales, "notas": notas}


# ------------------------------------------------------------------ controles del historico

def _controles_historicos(periodos: list, tolcfg: dict) -> list:
    out = []
    amb = "historico"
    prev = None
    for cur in periodos:
        r, b, f = cur["resultados"], cur["balance"], cur["flujo"]
        per = cur["periodo"]
        T = _tol(tolcfg, "historico", r["ingresos"])

        def add(cid, prueba, esperado, obtenido, estado=None, detalle=""):
            out.append(_registro(cid, prueba, amb, per, esperado, obtenido, T, estado, detalle))

        # C01
        add("C01", "activo_total = pasivo_total + capital_contable", b["pasivo_total"] + b["capital_contable"],
            b["activo_total"])
        der = " ".join(cur.get("derivados") or [])
        for total, lista, grupo in (("activo_total", ACTIVOS, BAL_RESIDUO_ACT), ("pasivo_total", PASIVOS, BAL_RESIDUO_PAS)):
            if any(g in der for g in grupo):
                add("C01", f"{total} = suma de componentes", None, None, "INFO",
                    f"componente derivado como residuo: {der}")
            else:
                add("C01", f"{total} = suma de componentes", sum(b[k] for k in lista), b[total])
        # C02
        caja_fin = f["caja_final"] if f.get("caja_final") is not None else b["caja"]
        if f.get("caja_final") is not None:
            add("C02", "caja final del flujo = caja del balance (misma definicion)", b["caja"], f["caja_final"],
                detalle="si difieren, cargue 'caja' con la definicion del estado de flujo")
        if prev is not None:
            caja_ini = prev["balance"]["caja"]
            if f.get("caja_inicial") is not None:
                add("C02", "caja inicial del flujo = caja del balance previo", caja_ini, f["caja_inicial"])
        else:
            caja_ini = f.get("caja_inicial")
        if caja_ini is None:
            add("C02", "caja inicial + CFO + CFI + CFF + FX = caja final", None, None, "NO_APLICA",
                "primer ejercicio sin flujo.caja_inicial")
        else:
            add("C02", "caja inicial + CFO + CFI + CFF + FX = caja final",
                caja_ini + f["cfo"] + f["cfi"] + f["cff"] + f["efecto_cambiario"], caja_fin)
        if f.get("otros_inversion") is not None:
            add("C02", "CFI = -capex + otros_inversion", -f["capex"] + f["otros_inversion"], f["cfi"])
        else:
            add("C02", "CFI = -capex + otros_inversion", None, None, "INFO",
                f"otros_inversion no reportado; implicito = {f['cfi'] + f['capex']:.6g}")
        comp_cff = (f["emision_deuda"] - f["amortizacion_deuda"] - f["principal_arrendamientos_financieros"]
                    - f["dividendos"] - f["recompras"] + f["emision_acciones"])
        if f.get("otros_financiamiento") is not None:
            add("C02", "CFF = suma de componentes", comp_cff + f["otros_financiamiento"], f["cff"])
        else:
            add("C02", "CFF = suma de componentes", None, None, "INFO",
                f"otros_financiamiento no reportado; implicito = {f['cff'] - comp_cff:.6g}")
        # C03 / C04
        mc = cur.get("movimientos_capital")
        cap_ini = (mc or {}).get("capital_inicial")
        if cap_ini is None and prev is not None:
            cap_ini = prev["balance"]["capital_contable"]
        if mc is None:
            if prev is None:
                add("C03", "capital inicial + movimientos = capital final", None, None, "NO_APLICA",
                    "primer ejercicio sin movimientos_capital")
            else:
                impl = (b["capital_contable"] - cap_ini - r["utilidad_neta"] - f["sbc"] + f["dividendos"]
                        + f["recompras"] - f["emision_acciones"])
                add("C03", "capital inicial + movimientos = capital final", None, None, "INFO",
                    f"sin movimientos_capital: ORI/otros/diferencias implicitos = {impl:.6g}")
        elif cap_ini is None:
            add("C03", "capital inicial + movimientos = capital final", None, None, "NO_APLICA",
                "primer ejercicio sin movimientos_capital.capital_inicial")
        else:
            un_m = mc["utilidad_neta"] if mc.get("utilidad_neta") is not None else r["utilidad_neta"]
            sbc_m = mc["sbc"] if mc.get("sbc") is not None else f["sbc"]
            emi_m = mc["emision_acciones"] if mc.get("emision_acciones") is not None else f["emision_acciones"]
            esperado = (cap_ini + un_m + sbc_m - mc["dividendos_declarados"] - mc["recompras"] + emi_m
                        + (mc.get("ori") or 0.0) + (mc.get("otros") or 0.0))
            add("C03", "capital inicial + utilidad + SBC - dividendos - recompras + emision + ORI + otros = final",
                esperado, b["capital_contable"])
        ure_ini = (mc or {}).get("utilidades_retenidas_iniciales")
        if ure_ini is None and prev is not None:
            ure_ini = prev["balance"].get("utilidades_retenidas")
        if b.get("utilidades_retenidas") is None or ure_ini is None:
            add("C04", "utilidades retenidas roll-forward", None, None, "NO_APLICA",
                "faltan utilidades_retenidas (inicial o final)")
        elif mc is None or mc.get("recompras_contra_utilidades_retenidas") is None:
            impl = b["utilidades_retenidas"] - ure_ini - r["utilidad_neta"] + f["dividendos"]
            add("C04", "utilidades retenidas roll-forward", None, None, "INFO",
                f"sin movimientos_capital.recompras_contra_utilidades_retenidas; recompras y otros implicitos = {impl:.6g}")
        else:
            un_m = mc["utilidad_neta"] if mc.get("utilidad_neta") is not None else r["utilidad_neta"]
            esperado = (ure_ini + un_m - mc["dividendos_declarados"] - mc["recompras_contra_utilidades_retenidas"]
                        + (mc.get("otros_utilidades_retenidas") or 0.0))
            add("C04", "URE inicial + utilidad - dividendos - recompras imputadas + otros = URE final",
                esperado, b["utilidades_retenidas"])
        # C05
        mp = cur.get("movimientos_ppe")
        ppe_ini = (mp or {}).get("ppe_inicial")
        if ppe_ini is None and prev is not None:
            ppe_ini = prev["balance"]["ppe_neto"]
        if mp is not None and ppe_ini is not None:
            add("C05", "PPE inicial + adiciones - depreciacion + otros = PPE final",
                ppe_ini + mp["adiciones"] - mp["depreciacion"] + (mp.get("otros") or 0.0), b["ppe_neto"])
        elif ppe_ini is None:
            add("C05", "PPE roll-forward", None, None, "NO_APLICA", "primer ejercicio sin movimientos_ppe.ppe_inicial")
        else:
            impl = b["ppe_neto"] - ppe_ini - f["capex"] + f["depreciacion_amortizacion"]
            add("C05", "PPE roll-forward", None, None, "INFO",
                f"sin movimientos_ppe: otros implicitos (arrendamientos, adquisiciones, bajas, amortizacion de "
                f"intangibles incluida en D&A, FX) = {impl:.6g}")
        # C06
        md = cur.get("movimientos_deuda")
        d_ini = (md or {}).get("deuda_inicial")
        if d_ini is None and prev is not None:
            d_ini = prev["balance"]["deuda"]
        if d_ini is None:
            add("C06", "deuda inicial + emisiones - amortizaciones + otros = deuda final", None, None, "NO_APLICA",
                "primer ejercicio sin movimientos_deuda.deuda_inicial")
        else:
            emi = md["emisiones"] if md and md.get("emisiones") is not None else f["emision_deuda"]
            amo = md["amortizaciones"] if md and md.get("amortizaciones") is not None else f["amortizacion_deuda"]
            otros = (md or {}).get("otros") or 0.0
            esperado = d_ini + emi - amo + otros
            if md is None and abs(b["deuda"] - esperado) > T:
                add("C06", "deuda inicial + emisiones - amortizaciones + otros = deuda final", esperado, b["deuda"],
                    "INFO", "sin movimientos_deuda: la diferencia es no monetaria no documentada (FX, descuentos, "
                    "adquisiciones, reclasificaciones); agregue movimientos_deuda desde la nota de deuda")
            else:
                add("C06", "deuda inicial + emisiones - amortizaciones + otros = deuda final", esperado, b["deuda"])
        ma = cur.get("movimientos_arrendamientos")
        a_ini = (ma or {}).get("inicial")
        if a_ini is None and prev is not None:
            a_ini = prev["balance"]["arrendamientos_financieros"]
        if ma is not None and a_ini is not None:
            princ = ma["principal"] if ma.get("principal") is not None else f["principal_arrendamientos_financieros"]
            add("C06", "arrendamientos financieros: inicial + nuevos - principal + otros = final",
                a_ini + ma["nuevos"] - princ + (ma.get("otros") or 0.0), b["arrendamientos_financieros"])
        elif a_ini is not None:
            impl = b["arrendamientos_financieros"] - a_ini + f["principal_arrendamientos_financieros"]
            add("C06", "arrendamientos financieros roll-forward", None, None, "INFO",
                f"sin movimientos_arrendamientos: nuevos + otros implicitos = {impl:.6g}")
        # C07
        un_f = f["utilidad_neta"] if f.get("utilidad_neta") is not None else r["utilidad_neta"]
        if f.get("utilidad_neta") is not None:
            add("C07", "utilidad del flujo = utilidad del estado de resultados", r["utilidad_neta"], f["utilidad_neta"])
        if f.get("cambio_capital_trabajo") is not None and f.get("otros_operativos") is not None:
            add("C07", "utilidad + D&A + SBC + capital de trabajo + otros = CFO",
                un_f + f["depreciacion_amortizacion"] + f["sbc"] + f["cambio_capital_trabajo"] + f["otros_operativos"],
                f["cfo"])
        else:
            impl = f["cfo"] - un_f - f["depreciacion_amortizacion"] - f["sbc"]
            add("C07", "utilidad + D&A + SBC + capital de trabajo + otros = CFO", None, None, "NO_APLICA",
                f"faltan cambio_capital_trabajo u otros_operativos; capital de trabajo + otros implicitos = {impl:.6g}")
        # C08-C11: en el historico el driver es implicito (tautologico): se reporta
        dr = drivers_implicitos(cur, prev)
        add("C08", "dias de cuentas por cobrar implicitos", None, None, "INFO", f"dias_cxc = {dr['dias_cxc']}")
        add("C09", "dias de inventario y proveedores implicitos", None, None, "INFO",
            f"dias_inventario = {dr['dias_inventario']}; dias_proveedores = {dr['dias_proveedores']}")
        if prev is None:
            add("C10", "tasa de interes implicita", None, None, "NO_APLICA", "requiere saldo inicial de deuda")
        else:
            det = (f"tasa sobre deuda = {dr['tasa_interes_sobre_deuda']}; sobre deuda + arrendamientos + revolvente = "
                   f"{dr['tasa_interes_sobre_deuda_y_arrendamientos']}")
            if dr["tasa_interes_sobre_deuda_y_arrendamientos"] is None and r["gasto_intereses"]:
                det += "; ALERTA: gasto de intereses sin deuda promedio"
            add("C10", "tasa de interes implicita", None, None, "INFO", det)
        det = f"tasa efectiva = {dr['tasa_impuestos']}"
        if dr["tasa_impuestos"] is not None and not 0 <= dr["tasa_impuestos"] <= 0.5:
            det += "; ALERTA: tasa efectiva fuera de [0, 50%] (revise partidas discretas)"
        add("C11", "tasa de impuestos implicita", None, None, "INFO", det)
        # C12
        fcf = f["cfo"] - f["capex"]
        fcf2 = fcf - f["principal_arrendamientos_financieros"]
        if f.get("fcf_reportado") is not None:
            if abs(f["fcf_reportado"] - fcf2) <= T < abs(f["fcf_reportado"] - fcf):
                add("C12", "FCF reportado = CFO - capex - principal de arrendamientos", fcf2, f["fcf_reportado"],
                    detalle="el emisor define FCF despues de principal de arrendamientos")
            else:
                add("C12", "FCF reportado = CFO - capex", fcf, f["fcf_reportado"])
        else:
            add("C12", "FCF = CFO - capex", None, None, "INFO",
                f"FCF = {fcf:.6g}; FCF despues de principal de arrendamientos = {fcf2:.6g}")
        # C13
        if prev is None:
            add("C13", "el motor reproduce el historico", None, None, "NO_APLICA",
                "primer ejercicio: no hay balance de apertura")
        else:
            rec = reconciliar_periodo(prev, cur, tolcfg)
            det = []
            if rec["lineas_fuera_de_tolerancia"]:
                det.append("fuera de tolerancia: " + ", ".join(rec["lineas_fuera_de_tolerancia"]))
            if rec["alertas_materialidad"]:
                det.append("ALERTA partidas conciliatorias materiales: " + "; ".join(rec["alertas_materialidad"]))
            det.extend(rec["notas"])
            out.append(_registro("C13", "el motor reproduce el historico (max |modelo - reportado|)", amb, per, 0.0,
                                 rec["max_diferencia"], rec["tolerancia"], detalle=" | ".join(det)))
        # C14
        for a in cur.get("ajustado") or []:
            gaap = r.get(a["base"])
            if gaap is None or a["valor_ajustado"] is None:
                add("C14", f"{a['base']} GAAP + ajustes = ajustado", None, None, "NO_APLICA",
                    f"falta {a['base']} o valor_ajustado")
            else:
                add("C14", f"{a['base']} GAAP + ajustes = ajustado", gaap + sum(a["ajustes"].values()),
                    a["valor_ajustado"], detalle=f"fuente: {a['fuente']}")
        # C15
        if r.get("utilidad_bruta") is not None:
            add("C15", "utilidad bruta = ingresos - costo de ventas", r["ingresos"] - r["costo_ventas"], r["utilidad_bruta"])
        if r.get("gastos_operativos") is not None:
            add("C15", "utilidad operativa = utilidad bruta - gastos operativos", _ub(r) - r["gastos_operativos"],
                r["utilidad_operativa"])
        if r.get("otros_ingresos") is not None:
            add("C15", "UAI = UO - intereses + ingreso financiero + otros",
                r["utilidad_operativa"] - r["gasto_intereses"] + (r.get("ingreso_intereses") or 0.0) + r["otros_ingresos"],
                r["utilidad_antes_impuestos"])
        else:
            impl = r["utilidad_antes_impuestos"] - r["utilidad_operativa"] + r["gasto_intereses"]
            add("C15", "UAI = UO - intereses + otros", None, None, "INFO",
                f"otros_ingresos no reportado; implicito (incluye ingreso financiero) = {impl:.6g}")
        add("C15", "utilidad neta = UAI - impuestos + otros despues de impuestos",
            r["utilidad_antes_impuestos"] - r["impuestos"] + (r.get("otros_despues_impuestos") or 0.0),
            r["utilidad_neta"])
        prev = cur
    return out


# ------------------------------------------------------------------ controles de proyeccion

def _controles_escenario(nombre: str, periodos: list, bal0: dict, ing0: float, tolcfg: dict) -> list:
    out = []
    amb = f"escenario:{nombre}"
    prev, ing_prev = bal0, ing0
    for p in periodos:
        r, b, f, s = p["resultados"], p["balance"], p["flujo"], p["supuestos"]
        mv = p["movimientos"]
        per = p["periodo"]
        T = _tol(tolcfg, "proyeccion", r["ingresos"])

        def add(cid, prueba, esperado, obtenido, estado=None, detalle=""):
            out.append(_registro(cid, prueba, amb, per, esperado, obtenido, T, estado, detalle))

        pv = {k: float(prev.get(k) or 0.0) for k in ACTIVOS + PASIVOS}
        # C01
        add("C01", "activo_total = pasivo_total + capital_contable", b["pasivo_total"] + b["capital_contable"],
            b["activo_total"])
        add("C01", "activo_total = suma de activos", sum(b[k] for k in ACTIVOS), b["activo_total"])
        add("C01", "pasivo_total = suma de pasivos", sum(b[k] for k in PASIVOS), b["pasivo_total"])
        # C02
        add("C02", "caja inicial + CFO + CFI + CFF + FX = caja final",
            pv["caja"] + f["cfo"] + f["cfi"] + f["cff"] + f["efecto_cambiario"], b["caja"])
        add("C02", "CFI = -capex + otros_inversion", -f["capex"] + f["otros_inversion"], f["cfi"])
        add("C02", "CFF = suma de componentes (incluye revolvente)",
            f["emision_deuda"] - f["amortizacion_deuda"] - f["principal_arrendamientos_financieros"]
            + f["disposicion_revolvente"] - f["pago_revolvente"] - f["dividendos"] - f["recompras"]
            + f["emision_acciones"] + f["otros_financiamiento"], f["cff"])
        # C03
        add("C03", "capital inicial + utilidad + SBC - dividendos - recompras + emision + otros = final",
            float(prev["capital_contable"]) + r["utilidad_neta"] + r["sbc"] - f["dividendos"] - f["recompras"]
            + f["emision_acciones"] + mv["capital"]["otros"], b["capital_contable"])
        # C04
        if b.get("utilidades_retenidas") is None or prev.get("utilidades_retenidas") is None:
            add("C04", "utilidades retenidas roll-forward", None, None, "NO_APLICA",
                "la base no trae utilidades_retenidas")
        else:
            add("C04", "URE inicial + utilidad - dividendos - recompras imputadas = URE final",
                prev["utilidades_retenidas"] + r["utilidad_neta"] - f["dividendos"]
                - f["recompras"] * s["recompras_contra_utilidades_retenidas"] + mv["capital"]["otros_utilidades_retenidas"],
                b["utilidades_retenidas"])
        # C05
        add("C05", "PPE inicial + capex + nuevos arrendamientos - (D&A - amortizacion intangibles) = PPE final",
            pv["ppe_neto"] + f["capex"] + mv["ppe"]["nuevos_arrendamientos_financieros"]
            - (r["depreciacion_amortizacion"] - s["amortizacion_intangibles"]) + mv["ppe"]["otros"], b["ppe_neto"])
        # C06
        add("C06", "deuda inicial + emisiones - amortizaciones = deuda final",
            pv["deuda"] + f["emision_deuda"] - f["amortizacion_deuda"] + mv["deuda"]["otros"], b["deuda"])
        add("C06", "arrendamientos financieros: inicial + nuevos - principal = final",
            pv["arrendamientos_financieros"] + mv["arrendamientos"]["nuevos"] - f["principal_arrendamientos_financieros"]
            + mv["arrendamientos"]["otros"], b["arrendamientos_financieros"])
        add("C06", "revolvente: inicial + disposiciones - pagos = final",
            pv["revolvente"] + f["disposicion_revolvente"] - f["pago_revolvente"] + mv["revolvente"]["otros"],
            b["revolvente"])
        # C07
        d_ct = (-(b["cuentas_por_cobrar"] - pv["cuentas_por_cobrar"]) - (b["inventarios"] - pv["inventarios"])
                + (b["proveedores"] - pv["proveedores"]))
        add("C07", "utilidad + D&A + SBC + capital de trabajo (saldos del balance) + otros = CFO",
            r["utilidad_neta"] + r["depreciacion_amortizacion"] + r["sbc"] + d_ct + f["otros_operativos"], f["cfo"])
        add("C07", "capital de trabajo del flujo = cambio de saldos del balance", d_ct, f["cambio_capital_trabajo"])
        # C08 / C09
        add("C08", "cxc = dias_cxc x ingresos / 365", s["dias_cxc"] * r["ingresos"] / DIAS_ANO, b["cuentas_por_cobrar"])
        add("C09", "inventario = dias_inventario x costo de ventas / 365",
            s["dias_inventario"] * r["costo_ventas"] / DIAS_ANO, b["inventarios"])
        add("C09", "proveedores = dias_proveedores x costo de ventas / 365",
            s["dias_proveedores"] * r["costo_ventas"] / DIAS_ANO, b["proveedores"])
        # C10
        gi = (s["tasa_interes"] * (pv["deuda"] + b["deuda"]) / 2
              + s["tasa_arrendamientos_financieros"] * (pv["arrendamientos_financieros"] + b["arrendamientos_financieros"]) / 2
              + s["tasa_revolvente"] * (pv["revolvente"] + b["revolvente"]) / 2)
        add("C10", "gasto de intereses = tasas x saldos promedio (deuda, arrendamientos, revolvente)", gi,
            r["gasto_intereses"])
        ii = s["tasa_rendimiento_caja"] * ((pv["caja"] + pv["inversiones_cp"]) + (b["caja"] + b["inversiones_cp"])) / 2
        add("C10", "ingreso financiero = tasa x (caja + inversiones_cp) promedio", ii, r["ingreso_intereses"])
        # C11
        add("C11", "impuestos = tasa x UAI", s["tasa_impuestos"] * r["utilidad_antes_impuestos"], r["impuestos"])
        # C12
        add("C12", "FCF = CFO - capex", f["cfo"] - f["capex"], f["fcf"])
        add("C12", "FCF despues de arrendamientos = FCF - principal de arrendamientos financieros",
            f["fcf"] - f["principal_arrendamientos_financieros"], f["fcf_despues_arrendamientos"])
        # C14
        met = p.get("metricas") or {}
        if s.get("ajuste_utilidad_neta") is not None:
            add("C14", "utilidad neta + ajuste = utilidad neta ajustada", r["utilidad_neta"] + s["ajuste_utilidad_neta"],
                met.get("utilidad_neta_ajustada"), detalle="ajuste = supuesto de escenario")
        # C15
        add("C15", "ingresos = ingresos previos x (1 + crecimiento)", ing_prev * (1 + s["crecimiento_ingresos"]),
            r["ingresos"])
        add("C15", "utilidad bruta = ingresos - costo de ventas = ingresos x margen bruto",
            r["ingresos"] - r["costo_ventas"], r["utilidad_bruta"])
        add("C15", "utilidad operativa = ingresos x margen operativo = bruta - gastos operativos",
            r["ingresos"] * s["margen_operativo"], r["utilidad_bruta"] - r["gastos_operativos"])
        add("C15", "UAI = UO - intereses + ingreso financiero + otros",
            r["utilidad_operativa"] - r["gasto_intereses"] + r["ingreso_intereses"] + r["otros_ingresos"],
            r["utilidad_antes_impuestos"])
        add("C15", "utilidad neta = UAI - impuestos + otros despues de impuestos",
            r["utilidad_antes_impuestos"] - r["impuestos"] + r["otros_despues_impuestos"], r["utilidad_neta"])
        # C16
        cmin = s["caja_minima"]
        add("C16", "caja final >= caja minima", cmin, b["caja"], "OK" if b["caja"] >= cmin - T else "FALLA",
            f"financiamiento requerido en el periodo = {f['disposicion_revolvente']:.6g}")
        add("C16", "revolvente >= 0", 0.0, b["revolvente"], "OK" if b["revolvente"] >= -T else "FALLA")
        # caja antes de revolvente desde los componentes del flujo SIN revolvente (independiente del saldo
        # final de caja, del total del CFF y de la disposicion que se esta verificando)
        cff_sin_rev = (f["emision_deuda"] - f["amortizacion_deuda"] - f["principal_arrendamientos_financieros"]
                       - f["dividendos"] - f["recompras"] + f["emision_acciones"] + f["otros_financiamiento"])
        caja_pre = pv["caja"] + f["cfo"] + f["cfi"] + cff_sin_rev + f["efecto_cambiario"]
        add("C16", "disposicion = max(0, caja minima - caja antes de revolvente)", max(0.0, cmin - caja_pre),
            f["disposicion_revolvente"])
        add("C16", "pago = min(revolvente inicial, excedente sobre caja minima)",
            min(pv["revolvente"], max(0.0, caja_pre - cmin)), f["pago_revolvente"])
        prev, ing_prev = b, r["ingresos"]
    return out


# ------------------------------------------------------------------ ensamblado

def resumir_controles(controles: list) -> dict:
    por_id = {}
    for c in controles:
        d = por_id.setdefault(c["id"], {"control": c["control"], "OK": 0, "FALLA": 0, "INFO": 0, "NO_APLICA": 0})
        d[c["estado"]] += 1
    fallas = [{k: c[k] for k in ("id", "prueba", "ambito", "periodo", "esperado", "obtenido", "diferencia",
                                 "tolerancia", "detalle")} for c in controles if c["estado"] == "FALLA"]
    tot = {e: sum(1 for c in controles if c["estado"] == e) for e in ("OK", "FALLA", "INFO", "NO_APLICA")}
    return {"total": len(controles), **tot, "todos_ok": tot["FALLA"] == 0,
            "tipos_de_control": len(CONTROLES), "ids_evaluados": sorted(por_id), "por_id": dict(sorted(por_id.items())),
            "fallas": fallas}


def verificar(resultado: dict) -> list:
    """Recalcula TODOS los controles desde los estados guardados en 'resultado' (sirve para auditar
    un resultados.json o un resultado alterado). No usa variables internas del motor."""
    tolcfg = resultado["meta"]["tolerancias"]
    hist = resultado["historico"]["periodos"]
    controles = _controles_historicos(hist, tolcfg)
    ultimo = hist[-1]
    for nombre, esc in resultado.get("escenarios", {}).items():
        controles += _controles_escenario(nombre, esc["periodos"], ultimo["balance"], ultimo["resultados"]["ingresos"],
                                          tolcfg)
    return controles


def _resumen_ajustado(periodos: list) -> list:
    filas, previo = [], {}
    for p in periodos:
        for a in p.get("ajustado") or []:
            gaap = p["resultados"].get(a["base"])
            fila = {"periodo": p["periodo"], "base": a["base"], "gaap": gaap, "ajustes": a["ajustes"],
                    "ajustado": a["valor_ajustado"], "fuente": a["fuente"],
                    "crecimiento_gaap": None, "crecimiento_ajustado": None}
            if a["base"] in previo:
                g0, a0 = previo[a["base"]]
                fila["crecimiento_gaap"] = _dividir(gaap, g0) - 1 if gaap is not None and g0 else None
                fila["crecimiento_ajustado"] = (_dividir(a["valor_ajustado"], a0) - 1
                                                if a["valor_ajustado"] is not None and a0 else None)
            previo[a["base"]] = (gaap, a["valor_ajustado"])
            filas.append(fila)
    return filas


def construir_modelo(base: dict, supuestos: dict | None = None) -> dict:
    """Valida la base, reconcilia el historico, proyecta los escenarios y corre los controles.

    No lanza excepcion por controles fallidos: revise resultado["resumen_controles"]["todos_ok"].
    Lanza ValueError si la base o los supuestos son invalidos (faltantes, signos, claves desconocidas)."""
    norm = normalizar_base(base)
    periodos = norm["periodos"]
    tolcfg = norm["tolerancias"]
    sup = supuestos if supuestos is not None else base.get("supuestos")
    drivers = {}
    reconc = {}
    for i, p in enumerate(periodos):
        prev = periodos[i - 1] if i else None
        drivers[p["periodo"]] = drivers_implicitos(p, prev)
        if prev is not None:
            reconc[p["periodo"]] = reconciliar_periodo(prev, p, tolcfg)
    resultado = {
        "meta": {"motor": "herramientas/modelo_integrado.py", "version": VERSION, "empresa": norm["empresa"],
                 "ticker": norm["ticker"], "moneda": norm["moneda"], "unidades": norm["unidades"],
                 "fecha_corte": norm["fecha_corte"], "fuentes": norm["fuentes"], "aviso": AVISO,
                 "tolerancias": tolcfg, "controles_definidos": CONTROLES, "convenciones": CONVENCIONES},
        "historico": {"naturaleza": "hecho (filing): cifras transcritas de los documentos citados en 'fuente'",
                      "periodos": periodos, "drivers_implicitos": drivers, "reconciliacion": reconc,
                      "ajustado": _resumen_ajustado(periodos)},
        "escenarios": {},
    }
    if sup:
        if not isinstance(sup, dict) or not isinstance(sup.get("escenarios"), dict) or not sup["escenarios"]:
            raise ValueError("supuestos: se espera {'anos': N, 'caja_minima': X, 'escenarios': {nombre: {...}}}")
        extra = sorted(set(sup) - {"anos", "caja_minima", "nota", "escenarios", "fuente_supuestos"})
        if extra:
            raise ValueError(f"supuestos: claves no reconocidas {extra}")
        anos = sup.get("anos")
        if not isinstance(anos, int) or isinstance(anos, bool) or anos < 1:
            raise ValueError("supuestos.anos: entero >= 1")
        resultado["supuestos_nota"] = sup.get("nota") or "Supuestos de escenario; no son pronosticos ni consenso"
        for nombre, esc in sup["escenarios"].items():
            resultado["escenarios"][nombre] = proyectar_escenario(periodos[-1], nombre, esc, anos, sup.get("caja_minima"))
    controles = verificar(resultado)
    resultado["controles"] = controles
    resultado["resumen_controles"] = resumir_controles(controles)
    return resultado


def cargar_y_construir(ruta_base, ruta_supuestos=None) -> dict:
    base = cargar_json(ruta_base)
    sup = cargar_json(ruta_supuestos) if ruta_supuestos else None
    return construir_modelo(base, sup)


# ------------------------------------------------------------------ DCF inverso

def valor_empresa_dcf(ingresos_base: float, crecimiento: float, margen_fcf: float, wacc: float,
                      g_terminal: float, anos: int) -> dict:
    """VP de FCFF = ingresos x margen_fcf durante 'anos' (ingresos crecen a 'crecimiento') mas valor
    terminal de Gordon FCF_n x (1 + g_terminal) / (wacc - g_terminal). Descuento a fin de ano."""
    if wacc <= g_terminal:
        raise ValueError("wacc debe ser mayor que g_terminal")
    ing, vp, flujos = ingresos_base, 0.0, []
    fcf = 0.0
    for t in range(1, anos + 1):
        ing *= 1 + crecimiento
        fcf = ing * margen_fcf
        fd = (1 + wacc) ** -t
        vp += fcf * fd
        flujos.append({"ano": t, "ingresos": ing, "fcf": fcf, "factor_descuento": fd, "vp": fcf * fd})
    vt = fcf * (1 + g_terminal) / (wacc - g_terminal)
    vp_vt = vt * (1 + wacc) ** -anos
    total = vp + vp_vt
    return {"valor_empresa": total, "vp_flujos": vp, "valor_terminal": vt, "vp_terminal": vp_vt,
            "peso_terminal": vp_vt / total if total else None,
            "multiplo_terminal_fcf": vt / fcf if fcf else None, "flujos": flujos}


def dcf_inverso(precio: float, acciones: float, deuda_neta: float, wacc: float, g_terminal: float,
                margen_fcf: float, anos: int, *, ingresos_base: float, limites: tuple = (-0.5, 1.0),
                tol: float = 1e-10, max_iter: int = 400, tasa_libre_riesgo: float | None = None) -> dict:
    """Crecimiento anual constante de ingresos implicito en el precio (biseccion).

    Valor de empresa objetivo = precio x acciones + deuda_neta (deuda + arrendamientos - caja - inversiones,
    definida por el usuario en las MISMAS unidades que ingresos_base). FCFF_t = ingresos_t x margen_fcf.
    El valor es creciente en el crecimiento (margen_fcf > 0), asi que la biseccion es valida.
    Devuelve dict con 'crecimiento_implicito' (None si no hay solucion en 'limites') y 'estado':
    OK, PRECIO_BAJO_EL_RANGO (implicito < limite inferior), PRECIO_SOBRE_EL_RANGO o SIN_SOLUCION."""
    for nombre, v in (("precio", precio), ("acciones", acciones), ("ingresos_base", ingresos_base)):
        if not _es_num(v) or v <= 0:
            raise ValueError(f"{nombre} debe ser numero > 0")
    for nombre, v in (("deuda_neta", deuda_neta), ("wacc", wacc), ("g_terminal", g_terminal), ("margen_fcf", margen_fcf)):
        if not _es_num(v):
            raise ValueError(f"{nombre} debe ser numero finito")
    if not isinstance(anos, int) or isinstance(anos, bool) or anos < 1:
        raise ValueError("anos debe ser entero >= 1")
    if wacc <= g_terminal:
        raise ValueError("wacc debe ser mayor que g_terminal (Gordon)")
    if wacc <= -1:
        raise ValueError("wacc debe ser > -1")
    if margen_fcf <= 0:
        raise ValueError("margen_fcf debe ser > 0: con FCF <= 0 ningun crecimiento justifica un valor positivo")
    lo, hi = limites
    if not (-1 < lo < hi):
        raise ValueError("limites debe cumplir -1 < inferior < superior")
    capitalizacion = precio * acciones
    ve = capitalizacion + deuda_neta
    supuestos = {
        "precio": precio, "acciones": acciones, "capitalizacion": capitalizacion, "deuda_neta": deuda_neta,
        "valor_empresa_objetivo": ve, "wacc": wacc, "g_terminal": g_terminal, "margen_fcf": margen_fcf,
        "anos": anos, "ingresos_base": ingresos_base, "limites_busqueda": [lo, hi],
        "definicion_fcf": "FCFF = ingresos x margen_fcf (margen constante; ya neto de impuestos y reinversion)",
        "valor_terminal": "Gordon: FCF_n x (1 + g_terminal) / (wacc - g_terminal), mismo margen",
        "descuento": "fin de ano, tasa constante = wacc",
        "crecimiento": "tasa anual constante de ingresos durante 'anos'",
    }
    alertas = []
    if tasa_libre_riesgo is not None:
        supuestos["tasa_libre_riesgo"] = tasa_libre_riesgo
        if g_terminal > tasa_libre_riesgo:
            alertas.append("g_terminal > tasa libre de riesgo nominal (conocimiento/03 s2.4: crecimiento gratis)")
    base = {"supuestos": supuestos, "alertas": alertas,
            "aviso": "Crecimiento que descuenta el precio bajo estos supuestos; no es pronostico ni recomendacion. "
                     "Comparar contra tasas base (conocimiento/03 s2.7)."}
    if ve <= 0:
        return {**base, "crecimiento_implicito": None, "estado": "SIN_SOLUCION", "iteraciones": 0,
                "detalle": "valor de empresa objetivo <= 0 (caja neta mayor que la capitalizacion)"}

    def f(g):
        return valor_empresa_dcf(ingresos_base, g, margen_fcf, wacc, g_terminal, anos)["valor_empresa"] - ve

    f_lo, f_hi = f(lo), f(hi)
    if f_lo > 0:
        return {**base, "crecimiento_implicito": None, "estado": "PRECIO_BAJO_EL_RANGO", "iteraciones": 0,
                "detalle": f"aun con crecimiento {lo} el valor supera al precio: el implicito es menor que {lo}"}
    if f_hi < 0:
        return {**base, "crecimiento_implicito": None, "estado": "PRECIO_SOBRE_EL_RANGO", "iteraciones": 0,
                "detalle": f"aun con crecimiento {hi} el valor no alcanza el precio: el implicito es mayor que {hi}"}
    it = 0
    for it in range(1, max_iter + 1):
        mid = (lo + hi) / 2
        fm = f(mid)
        if fm > 0:
            hi = mid
        else:
            lo = mid
        if hi - lo <= tol:
            break
    g = (lo + hi) / 2
    sol = valor_empresa_dcf(ingresos_base, g, margen_fcf, wacc, g_terminal, anos)
    if sol["peso_terminal"] is not None and sol["peso_terminal"] > 0.75:
        alertas.append(f"valor terminal = {100 * sol['peso_terminal']:.1f}% del valor (> 75%: la tesis depende del "
                       "largo plazo; conocimiento/03 s2.4)")
    return {**base, "crecimiento_implicito": g, "estado": "OK", "iteraciones": it,
            "residuo": sol["valor_empresa"] - ve,
            "valor_por_accion_en_solucion": (sol["valor_empresa"] - deuda_neta) / acciones,
            "solucion": sol}


def dcf_inverso_sensibilidad(precio: float, acciones: float, deuda_neta: float, waccs, margenes,
                             g_terminal: float, anos: int, *, ingresos_base: float) -> list:
    """Malla de crecimientos implicitos para varias combinaciones wacc x margen_fcf."""
    filas = []
    for w in waccs:
        for m in margenes:
            r = dcf_inverso(precio, acciones, deuda_neta, w, g_terminal, m, anos, ingresos_base=ingresos_base)
            filas.append({"wacc": w, "margen_fcf": m, "crecimiento_implicito": r["crecimiento_implicito"],
                          "estado": r["estado"]})
    return filas


# ------------------------------------------------------------------ reporte

def _fmt(x, dec=1) -> str:
    if x is None:
        return "n.d."
    return f"{x:,.{dec}f}"


def _pct(x) -> str:
    return "n.d." if x is None else f"{100 * x:.1f}%"


def resumen_markdown(resultado: dict) -> str:
    """Tablas markdown: controles, reconciliacion del historico y escenarios."""
    m = resultado["meta"]
    rc = resultado["resumen_controles"]
    L = [f"Motor {m['motor']} v{m['version']} | {m['empresa']} | {m['moneda']} {m['unidades']}", "",
         f"> {m['aviso']}", "",
         f"**Controles:** {rc['total']} registros, OK {rc['OK']}, FALLA {rc['FALLA']}, INFO {rc['INFO']}, "
         f"NO_APLICA {rc['NO_APLICA']}. Todos OK: {'si' if rc['todos_ok'] else 'NO'}.", "",
         "| Id | Control | OK | FALLA | INFO | NO_APLICA |", "|---|---|---|---|---|---|"]
    for cid, d in rc["por_id"].items():
        L.append(f"| {cid} | {d['control']} | {d['OK']} | {d['FALLA']} | {d['INFO']} | {d['NO_APLICA']} |")
    if rc["fallas"]:
        L += ["", "**Fallas:**"]
        for fl in rc["fallas"]:
            L.append(f"- {fl['id']} {fl['ambito']} {fl['periodo']}: {fl['prueba']} (dif {fl['diferencia']}, "
                     f"tol {fl['tolerancia']}) {fl['detalle']}")
    for per, rec in resultado["historico"]["reconciliacion"].items():
        L += ["", f"**Reconciliacion {per}** (calculo sobre hechos; max |dif| = {_fmt(rec['max_diferencia'], 4)}, "
              f"tolerancia {_fmt(rec['tolerancia'], 4)})", "",
              "| Partida conciliatoria | Monto | % ingresos | Origen | Material |", "|---|---|---|---|---|"]
        for p in rec["partidas_conciliatorias"]:
            if abs(p["monto"]) > 1e-9:
                L.append(f"| {p['partida']} | {_fmt(p['monto'])} | {_pct(p['pct_ingresos'])} | {p['origen']} | "
                         f"{'ALERTA' if p['material'] else ''} |")
    for nombre, esc in resultado.get("escenarios", {}).items():
        per = esc["periodos"]
        L += ["", f"**Escenario {nombre}** (supuesto de escenario; no es pronostico): {esc['descripcion']}", "",
              "| Concepto | " + " | ".join(p["periodo"] for p in per) + " |",
              "|---|" + "---|" * len(per)]
        filas = (("Ingresos", lambda p: p["resultados"]["ingresos"]),
                 ("Utilidad operativa", lambda p: p["resultados"]["utilidad_operativa"]),
                 ("Utilidad neta", lambda p: p["resultados"]["utilidad_neta"]),
                 ("CFO", lambda p: p["flujo"]["cfo"]), ("Capex", lambda p: p["flujo"]["capex"]),
                 ("FCF", lambda p: p["flujo"]["fcf"]),
                 ("FCF despues de arrendamientos", lambda p: p["flujo"]["fcf_despues_arrendamientos"]),
                 ("Dividendos + recompras", lambda p: p["flujo"]["dividendos"] + p["flujo"]["recompras"]),
                 ("Financiamiento requerido", lambda p: p["flujo"]["disposicion_revolvente"]),
                 ("Caja final", lambda p: p["balance"]["caja"]), ("Revolvente", lambda p: p["balance"]["revolvente"]),
                 ("Deuda neta", lambda p: p["metricas"]["deuda_neta"]))
        for etq, fn in filas:
            L.append(f"| {etq} | " + " | ".join(_fmt(fn(p)) for p in per) + " |")
        for a in esc["alertas"]:
            L.append(f"- {a}")
    return "\n".join(L) + "\n"


# ------------------------------------------------------------------ CLI

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Modelo integrado de 3 estados con controles (FASE 0: escenarios).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("correr", help="construye el modelo y escribe resultados.json")
    c.add_argument("--base", required=True)
    c.add_argument("--supuestos")
    c.add_argument("--salida", required=True)
    c.add_argument("--sha256", help="escribe SHA256SUMS de base, supuestos y salida")
    c.add_argument("--markdown", help="escribe el resumen markdown en esta ruta")
    d = sub.add_parser("dcf-inverso", help="crecimiento de ingresos implicito en el precio")
    for arg in ("--precio", "--acciones", "--deuda-neta", "--wacc", "--g-terminal", "--margen-fcf", "--ingresos-base"):
        d.add_argument(arg, type=float, required=True)
    d.add_argument("--anos", type=int, required=True)
    d.add_argument("--tasa-libre-riesgo", type=float)
    a = ap.parse_args(argv)
    if a.cmd == "dcf-inverso":
        r = dcf_inverso(a.precio, a.acciones, a.deuda_neta, a.wacc, a.g_terminal, a.margen_fcf, a.anos,
                        ingresos_base=a.ingresos_base, tasa_libre_riesgo=a.tasa_libre_riesgo)
        r.pop("solucion", None)
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0 if r["estado"] == "OK" else 2
    res = cargar_y_construir(a.base, a.supuestos)
    guardar_json(res, a.salida)
    md = resumen_markdown(res)
    if a.markdown:
        Path(a.markdown).write_text(md, encoding="utf-8")
    if a.sha256:
        rutas = [a.base] + ([a.supuestos] if a.supuestos else []) + [a.salida]
        escribir_sha256sums(rutas, a.sha256)
    print(md)
    return 0 if res["resumen_controles"]["todos_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
