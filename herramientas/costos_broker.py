"""Costo total por broker para una cuenta chica (arena): comisiones, IVA, cuotas de terceros,
tipo de cambio, fondeo y retiro, cuotas fijas, efectivo ocioso, liquidacion y arrastre fiscal.

Solo biblioteca estandar. Montos en MXN salvo sufijo _usd. Tasas como fraccion (0.0025 = 0.25%).

Unidad de actividad: una "operacion" es UNA ejecucion (una compra o una venta), que es lo que
cobra el broker. Una ida y vuelta son 2 operaciones. La mitad de las operaciones son ventas.

Dos totales, porque el torneo y el bolsillo del dueno no miden lo mismo:

- ``torneo``: lo que sale de la cuenta y mueve el TWR en MXN. Comision + IVA + cuotas de
  terceros y regulatorias + desviacion cambiaria implicita del SIC (ruta "sic") + conversion de
  entrada (ruta "extranjero") + fondeo + cuotas fijas + W-8BEN + retenciones de dividendos dentro
  de la cuenta + arrastre por esperar liquidacion - rendimiento del efectivo ocioso.
- ``dueno``: ``torneo`` + salida (conversion final, retiro y cobro del banco receptor) + impuesto
  de dividendos pagado por fuera + ISR diferencial sobre ganancias realizadas (tasa del broker
  menos la tasa de referencia de 10% del art. 129 LISR) + costo de cumplimiento (contador).

Formulas (n = operaciones_anuales * meses / 12; v = orden_promedio_mxn; TC = tipo_cambio):

- Acciones por orden: a = v / TC / precio_accion_usd.
- Comision por operacion en activos USD: c = max(pct*v + usd_por_accion*a*TC, min_mxn, min_usd*TC),
  topada en max_pct*v. IVA = c * iva. Terceros = (terceros_usd_por_accion*a + terceros_frac*c/TC)*TC.
  Regulatorias por venta = (sec_frac*v/TC + min(taf*a, taf_max))*TC.
- Operaciones en BMV (fraccion 1 - fraccion_usd): c_local = max(pct_local*v, min_local), con su IVA.
- Promocion: comision e IVA se multiplican por max(0, 1 - meses_sin_comision/meses).
- Ruta "sic": desviacion = n*fraccion_usd*v*desviacion_sic_por_lado (el tipo de cambio va en el precio).
- Ruta "extranjero": conversion por flujo = max(pct*monto, min_usd*TC) + fijo, con
  monto = capital/flujos*fraccion_usd. Entrada en cada deposito; salida en cada retiro.
- Fijos: cuota_mensual*meses*(1+iva) + custodia_anual*capital*meses/12*(1+iva) + mantenimiento.
  El mantenimiento no se cobra si la rotacion mensual (volumen de un lado o de ambos / capital)
  supera el umbral.
- Efectivo (ingreso, resta al costo): rend_efectivo*fraccion_efectivo*capital*meses/12.
- Liquidacion: (n/2)*v*dias_espera/252*rendimiento_esperado_anual.
- Dividendos: d = rend_div*capital*(1-fraccion_efectivo)*fraccion_usd*meses/12;
  dentro = d*retencion_div_en_cuenta; fuera = d*impuesto_div_fuera.
- Fiscal diferencial: (tasa_isr_ganancias - tasa_isr_referencia)*ganancia_realizada_anual_pct*capital*meses/12.

Las tarifas de ``catalogo()`` vienen de arena/investigacion/brokers/B1-B4 y de las paginas oficiales
releidas el 2026-09-25; cada preset trae su fuente y lo que no esta verificado. Ver
arena/investigacion/05-comparativa-brokers.md.

CLI: python3 herramientas/costos_broker.py [--tc 17.70] [--desviacion 0.0017] [--recepcion-ibkr 0]
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, replace
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

DIAS_HABILES = 252
IVA_MX = 0.16
# MXN por USD. Tasa media de la API publica de Wise, 25-sep-2026 06:15 UTC (B4 [36]).
TC_REFERENCIA = 17.70


@dataclass(frozen=True)
class Broker:
    clave: str
    nombre: str
    ruta: str  # "sic": casa de bolsa mexicana (activos USD en pesos via SIC); "extranjero": cuenta en USD
    # Comision por operacion en activos USD (SIC o NYSE/Nasdaq)
    comision_pct: float = 0.0
    comision_usd_por_accion: float = 0.0
    comision_min_mxn: float = 0.0
    comision_min_usd: float = 0.0
    comision_max_pct: float | None = None
    iva_comision: float = 0.0
    terceros_usd_por_accion: float = 0.0
    terceros_frac_comision: float = 0.0
    sec_frac_venta: float = 0.0
    taf_usd_por_accion_venta: float = 0.0
    taf_max_usd: float = 0.0
    # Operaciones en la BMV (emisoras mexicanas)
    bmv_disponible: bool = True
    comision_local_pct: float | None = None  # None: igual que comision_pct
    comision_local_min_mxn: float = 0.0
    iva_local: float | None = None  # None: igual que iva_comision
    # Conversion MXN<->USD (solo ruta "extranjero")
    conv_entrada_pct: float = 0.0
    conv_entrada_min_usd: float = 0.0
    conv_entrada_fijo_mxn: float = 0.0
    conv_salida_pct: float = 0.0
    conv_salida_min_usd: float = 0.0
    conv_salida_fijo_mxn: float = 0.0
    # Flujos
    costo_deposito_mxn: float = 0.0
    depositos_gratis_mes: int = 0
    costo_retiro_mxn: float = 0.0
    retiros_gratis_mes: int = 0
    costo_recepcion_retiro_mxn: float = 0.0
    # Cuotas fijas
    cuota_mensual_mxn: float = 0.0
    iva_cuota: float = 0.0
    custodia_anual_pct: float = 0.0
    iva_custodia: float = 0.0
    mantenimiento_anual_pct: float = 0.0
    iva_mantenimiento: float = 0.0
    mantenimiento_exento_si_rotacion_mayor_a: float | None = None
    rotacion_un_lado: bool = True
    meses_sin_comision: float = 0.0
    # Efectivo y liquidacion
    rendimiento_efectivo_anual: float = 0.0
    dias_espera_por_venta: float = 0.0
    # Dividendos, impuestos y cumplimiento
    retencion_div_en_cuenta: float = 0.0
    impuesto_div_fuera: float = 0.0
    costo_w8ben_mxn: float = 0.0
    tasa_isr_ganancias: float = 0.10
    costo_cumplimiento_anual_mxn: float = 0.0
    fuente: str = ""

    def __post_init__(self):
        if self.ruta not in ("sic", "extranjero"):
            raise ValueError(f"ruta desconocida: {self.ruta!r}")


@dataclass(frozen=True)
class Uso:
    capital_mxn: float = 20_000.0
    operaciones_anuales: float = 12
    orden_promedio_mxn: float = 5_000.0
    meses: float = 12
    fraccion_usd: float = 1.0
    depositos: int = 1
    retiros: int = 1
    tipo_cambio: float = TC_REFERENCIA
    precio_accion_usd: float = 50.0
    desviacion_sic_por_lado: float = 0.0017
    fraccion_efectivo: float = 0.0
    rendimiento_esperado_anual: float = 0.10
    rendimiento_dividendo_anual: float = 0.0
    ganancia_realizada_anual_pct: float = 0.0
    tasa_isr_referencia: float = 0.10

    def __post_init__(self):
        if self.capital_mxn <= 0 or self.orden_promedio_mxn <= 0 or self.tipo_cambio <= 0:
            raise ValueError("capital, orden y tipo de cambio deben ser positivos")
        if self.meses <= 0 or self.operaciones_anuales < 0:
            raise ValueError("meses > 0 y operaciones >= 0")
        if not 0.0 <= self.fraccion_usd <= 1.0 or not 0.0 <= self.fraccion_efectivo <= 1.0:
            raise ValueError("las fracciones van de 0 a 1")


# ------------------------------------------------------------------ por operacion

def acciones_por_orden(uso: Uso) -> float:
    return uso.orden_promedio_mxn / uso.tipo_cambio / uso.precio_accion_usd


def comision_usd_mxn(b: Broker, uso: Uso) -> float:
    """Comision (sin IVA ni terceros) de una operacion en activo USD, en MXN."""
    v, tc = uso.orden_promedio_mxn, uso.tipo_cambio
    c = b.comision_pct * v + b.comision_usd_por_accion * acciones_por_orden(uso) * tc
    c = max(c, b.comision_min_mxn, b.comision_min_usd * tc)
    if b.comision_max_pct is not None:
        c = min(c, b.comision_max_pct * v)
    return c


def comision_local_mxn(b: Broker, uso: Uso) -> float:
    """Comision (sin IVA) de una operacion en la BMV."""
    pct = b.comision_pct if b.comision_local_pct is None else b.comision_local_pct
    return max(pct * uso.orden_promedio_mxn, b.comision_local_min_mxn)


def terceros_mxn(b: Broker, uso: Uso) -> float:
    """Cuotas de bolsa, compensacion y traspaso por operacion en activo USD (ambos lados)."""
    tc = uso.tipo_cambio
    c_usd = comision_usd_mxn(b, uso) / tc
    return (b.terceros_usd_por_accion * acciones_por_orden(uso) + b.terceros_frac_comision * c_usd) * tc


def regulatorias_venta_mxn(b: Broker, uso: Uso) -> float:
    """SEC + FINRA TAF de una venta en activo USD."""
    tc = uso.tipo_cambio
    taf = b.taf_usd_por_accion_venta * acciones_por_orden(uso)
    if b.taf_max_usd:
        taf = min(taf, b.taf_max_usd)
    return (b.sec_frac_venta * uso.orden_promedio_mxn / tc + taf) * tc


def costo_por_lado(b: Broker, uso: Uso) -> dict:
    """Costo medio de una operacion en activo USD (compra y venta promediadas), sin promociones."""
    c = comision_usd_mxn(b, uso)
    total = c * (1 + b.iva_comision) + terceros_mxn(b, uso) + regulatorias_venta_mxn(b, uso) / 2
    if b.ruta == "sic":
        total += uso.desviacion_sic_por_lado * uso.orden_promedio_mxn
    return {"mxn": total, "pct_orden": total / uso.orden_promedio_mxn}


# ------------------------------------------------------------------ total

def _conversion(pct: float, min_usd: float, fijo: float, monto_mxn: float, tc: float) -> float:
    if monto_mxn <= 0:
        return 0.0
    return max(pct * monto_mxn, min_usd * tc) + fijo


def costo_total(b: Broker, uso: Uso) -> dict:
    """Desglose del costo en el horizonte ``uso.meses``; ver formulas en el docstring del modulo."""
    tc, v, cap, meses = uso.tipo_cambio, uso.orden_promedio_mxn, uso.capital_mxn, uso.meses
    n = uso.operaciones_anuales * meses / 12.0
    n_usd = n * uso.fraccion_usd
    n_loc = n - n_usd
    if n_loc > 1e-12 and not b.bmv_disponible:
        raise ValueError(f"{b.nombre} no da acceso a la BMV; use fraccion_usd = 1")

    promo = max(0.0, 1.0 - b.meses_sin_comision / meses)
    iva_loc = b.iva_comision if b.iva_local is None else b.iva_local

    comision = promo * (n_usd * comision_usd_mxn(b, uso) + n_loc * comision_local_mxn(b, uso))
    iva = promo * (n_usd * comision_usd_mxn(b, uso) * b.iva_comision
                   + n_loc * comision_local_mxn(b, uso) * iva_loc)
    terceros = n_usd * terceros_mxn(b, uso)
    regulatorias = (n_usd / 2.0) * regulatorias_venta_mxn(b, uso)
    desviacion_sic = n_usd * v * uso.desviacion_sic_por_lado if b.ruta == "sic" else 0.0

    conv_entrada = conv_salida = 0.0
    if b.ruta == "extranjero" and uso.fraccion_usd > 0:
        if uso.depositos:
            monto = cap / uso.depositos * uso.fraccion_usd
            conv_entrada = uso.depositos * _conversion(b.conv_entrada_pct, b.conv_entrada_min_usd,
                                                       b.conv_entrada_fijo_mxn, monto, tc)
        if uso.retiros:
            monto = cap / uso.retiros * uso.fraccion_usd
            conv_salida = uso.retiros * _conversion(b.conv_salida_pct, b.conv_salida_min_usd,
                                                    b.conv_salida_fijo_mxn, monto, tc)

    depositos_cobrados = max(0.0, uso.depositos - b.depositos_gratis_mes * meses)
    retiros_cobrados = max(0.0, uso.retiros - b.retiros_gratis_mes * meses)
    fondeo = depositos_cobrados * b.costo_deposito_mxn
    retiro = retiros_cobrados * b.costo_retiro_mxn
    recepcion = uso.retiros * b.costo_recepcion_retiro_mxn

    rotacion_mensual = (uso.operaciones_anuales / 12.0 * v * (0.5 if b.rotacion_un_lado else 1.0)) / cap
    exento = (b.mantenimiento_exento_si_rotacion_mayor_a is not None
              and rotacion_mensual > b.mantenimiento_exento_si_rotacion_mayor_a)
    mantenimiento = 0.0 if exento else (b.mantenimiento_anual_pct * cap * meses / 12.0
                                        * (1 + b.iva_mantenimiento))
    fijos = (b.cuota_mensual_mxn * meses * (1 + b.iva_cuota)
             + b.custodia_anual_pct * cap * meses / 12.0 * (1 + b.iva_custodia)
             + mantenimiento)

    efectivo = b.rendimiento_efectivo_anual * uso.fraccion_efectivo * cap * meses / 12.0
    liquidacion = (n / 2.0) * v * b.dias_espera_por_venta / DIAS_HABILES * uso.rendimiento_esperado_anual

    dividendos = (uso.rendimiento_dividendo_anual * cap * (1 - uso.fraccion_efectivo)
                  * uso.fraccion_usd * meses / 12.0)
    div_en_cuenta = dividendos * b.retencion_div_en_cuenta
    div_fuera = dividendos * b.impuesto_div_fuera
    fiscal = ((b.tasa_isr_ganancias - uso.tasa_isr_referencia)
              * uso.ganancia_realizada_anual_pct * cap * meses / 12.0)
    cumplimiento = b.costo_cumplimiento_anual_mxn * meses / 12.0

    torneo = (comision + iva + terceros + regulatorias + desviacion_sic + conv_entrada + fondeo
              + fijos + b.costo_w8ben_mxn + div_en_cuenta + liquidacion - efectivo)
    salida = conv_salida + retiro + recepcion
    dueno = torneo + salida + div_fuera + fiscal + cumplimiento
    return {
        "broker": b.clave,
        "nombre": b.nombre,
        "meses": meses,
        "operaciones": n,
        "comision": comision,
        "iva": iva,
        "terceros": terceros,
        "regulatorias": regulatorias,
        "desviacion_sic": desviacion_sic,
        "conversion_entrada": conv_entrada,
        "fondeo": fondeo,
        "fijos": fijos,
        "mantenimiento": mantenimiento,
        "w8ben": b.costo_w8ben_mxn,
        "dividendos_en_cuenta": div_en_cuenta,
        "liquidacion": liquidacion,
        "efectivo": efectivo,
        "conversion_salida": conv_salida,
        "retiro": retiro,
        "recepcion": recepcion,
        "salida": salida,
        "dividendos_fuera": div_fuera,
        "fiscal_diferencial": fiscal,
        "cumplimiento": cumplimiento,
        "torneo": torneo,
        "dueno": dueno,
        "torneo_pct": torneo / cap,
        "dueno_pct": dueno / cap,
    }


def comparar(brokers, uso: Uso, total: str = "dueno") -> list[dict]:
    """Costos de varios brokers ordenados de menor a mayor por ``total`` ("torneo" o "dueno")."""
    filas = []
    for b in brokers:
        try:
            filas.append(costo_total(b, uso))
        except ValueError:
            continue
    return sorted(filas, key=lambda f: f[total])


def equilibrio_operaciones(a: Broker, b: Broker, uso: Uso, total: str = "dueno",
                           max_ops: int = 2000) -> int | None:
    """Menor numero entero de operaciones al ano con el que ``a`` cuesta <= ``b``; None si nunca."""
    for ops in range(0, max_ops + 1):
        u = replace(uso, operaciones_anuales=ops)
        if costo_total(a, u)[total] <= costo_total(b, u)[total] + 1e-9:
            return ops
    return None


def holgura_cumplimiento_anual(candidato: Broker, referencia: Broker, uso: Uso) -> float:
    """Costo anual maximo de contador/cumplimiento con el que ``candidato`` sigue igual o mejor
    que ``referencia`` para el dueno (en MXN por ano)."""
    ahorro = costo_total(referencia, uso)["dueno"] - costo_total(candidato, uso)["dueno"]
    return ahorro * 12.0 / uso.meses


# ------------------------------------------------------------------ catalogo

def catalogo(tipo_cambio: float = TC_REFERENCIA, recepcion_retiro_ibkr_mxn: float = 0.0,
             tasa_marginal_etf: float = 0.30) -> dict[str, Broker]:
    """Presets con tarifas de fuente oficial (2026-09-25). Lo no verificado va en ``fuente``.

    recepcion_retiro_ibkr_mxn: lo que cobre el banco mexicano por recibir el SWIFT en MXN de IBKR
    (no verificado; peor caso del tarifario BBVA: 30 USD + IVA).
    tasa_marginal_etf: tasa hipotetica si un ETF vendido fuera de Mexico cae fuera del art. 129.
    """
    tc = tipo_cambio
    gbm = Broker(
        clave="gbm_sic", nombre="GBM Trading MX/SIC (linea base)", ruta="sic",
        comision_pct=0.0025, iva_comision=IVA_MX,
        rendimiento_efectivo_anual=0.031, retencion_div_en_cuenta=0.37,
        fuente=("Guia de Servicios GBM jul-2026: 0.25% + IVA, sin minimo ni custodia (B1). Smart Cash "
                "4.00% (<300k) menos retencion 0.90% (LIF 2026 art. 24) = 3.1% [I]. Sin W-8BEN: "
                "dividendos 30% EUA + 10% MX sobre el neto = 37% (B1, B4)."),
    )
    actinver = Broker(
        clave="actinver_trade", nombre="Actinver Trade (con mes gratis)", ruta="sic",
        comision_pct=0.0025, iva_comision=IVA_MX, meses_sin_comision=1.0,
        retencion_div_en_cuenta=0.19,
        fuente=("Guia Actinver 26.1.3 (vigente 22-jul-2026): 0.25% + IVA, custodia y administracion $0; "
                "30 dias sin comisiones con primer deposito >= 10,000 MXN (terminos 2024; los de 2026 no "
                "verificados). W-8BEN gratis (original en CDMX): 10% EUA + 9% MX. Rendimiento del fondo "
                "ACTIREN no verificado: 0."),
    )
    actinver_sin = replace(actinver, clave="actinver_trade_sin_promo",
                           nombre="Actinver Trade (sin promocion)", meses_sin_comision=0.0)
    kuspit_opt = Broker(
        clave="kuspit_optimista", nombre="Kuspit (0.20% sin IVA, sin mantenimiento)", ruta="sic",
        comision_pct=0.0020, iva_comision=0.0, retencion_div_en_cuenta=0.37,
        fuente=("kuspit.com JSON oficial: 0.20% por operacion, sin custodia ni administracion. IVA no "
                "indicado (no verificado). Mantenimiento '0%' segun Kuspit en X (mar-2024)."),
    )
    kuspit_pru = replace(
        kuspit_opt, clave="kuspit_prudente", nombre="Kuspit (0.20% + IVA, mantenimiento 0.99%)",
        iva_comision=IVA_MX, mantenimiento_anual_pct=0.0099, iva_mantenimiento=IVA_MX,
        mantenimiento_exento_si_rotacion_mayor_a=1.0, rotacion_un_lado=True,
        fuente=("Peor caso de B2: IVA probable por LIVA; mantenimiento 0.99% anual (Kuspit en X 2018, "
                "Rankia 2026), exento el mes con rotacion > portafolio; se supone rotacion de un lado. "
                "Guia G_Serv_Inv_Kuspit.pdf inaccesible (2026-09-25)."),
    )
    finamex = Broker(
        clave="finamex", nombre="Finamex Trading", ruta="sic",
        comision_pct=0.0006, iva_comision=IVA_MX, cuota_mensual_mxn=86.0, iva_cuota=IVA_MX,
        custodia_anual_pct=0.02, iva_custodia=IVA_MX,
        fuente=("FAQ oficial Finamex Trading: 0.06%, 86 MXN + IVA al mes, administracion 2% anual en "
                "contratos < 1 MDP. IVA sobre 0.06% y 2%: no verificado (se supone)."),
    )
    ibkr = Broker(
        clave="ibkr_tiered", nombre="Interactive Brokers Pro Tiered", ruta="extranjero",
        comision_usd_por_accion=0.0035, comision_min_usd=0.35, comision_max_pct=0.01,
        terceros_usd_por_accion=0.0030 + 0.0002 + 0.000003, terceros_frac_comision=0.000175 + 0.00056,
        sec_frac_venta=0.0000206, taf_usd_por_accion_venta=0.000195, taf_max_usd=9.79,
        comision_local_pct=0.001, comision_local_min_mxn=60.0, iva_local=0.0,
        conv_entrada_pct=0.00002, conv_entrada_min_usd=2.0,
        conv_salida_pct=0.00002, conv_salida_min_usd=2.0,
        costo_deposito_mxn=100.0, depositos_gratis_mes=1,
        costo_retiro_mxn=100.0, retiros_gratis_mes=2,
        costo_recepcion_retiro_mxn=recepcion_retiro_ibkr_mxn,
        rendimiento_efectivo_anual=0.0, dias_espera_por_venta=1.0,
        retencion_div_en_cuenta=0.10, impuesto_div_fuera=0.09, tasa_isr_ganancias=0.10,
        fuente=("interactivebrokers.com (commissions-stocks, other-fees, spot-currencies y FAQ MXN, "
                "releidas 2026-09-25): 0.0035 USD/accion min 0.35; bolsa NYSE 0.0030 + NSCC 0.0002 + "
                "CAT 0.000003 por accion; traspasos 0.000735 x comision; SEC 0.0000206 y TAF 0.000195 "
                "en ventas; BMV 0.1% min 60 MXN; FX 0.20 pb min 2 USD; SPEI: 1er deposito del mes "
                "gratis, luego 100 MXN; retiro SWIFT: 2 gratis al mes, luego 100 MXN; efectivo 0% "
                "(<10k USD). Sin IVA mexicano [I]. Cuenta de efectivo: 1 dia de espera por venta "
                "(tope; margen lo elimina). Acciones listadas en el SIC: 10% (criterio 37/ISR/N)."),
    )
    ibkr_etf = replace(
        ibkr, clave="ibkr_tiered_etf_peor_caso",
        nombre=f"IBKR Tiered, ETF fuera del art. 129 (tasa {tasa_marginal_etf:.0%})",
        tasa_isr_ganancias=tasa_marginal_etf,
        fuente=("Mismo costo que ibkr_tiered. Peor caso fiscal [I]: ETF vendido fuera de Mexico en "
                "regimen general (tarifa hasta 35%); sin el pago provisional del art. 126."),
    )
    ibkr_fixed = replace(
        ibkr, clave="ibkr_fixed", nombre="Interactive Brokers Pro Fixed",
        comision_usd_por_accion=0.005, comision_min_usd=1.0, terceros_usd_por_accion=0.0,
        terceros_frac_comision=0.0,
        fuente="Fixed: 0.005 USD/accion, min 1 USD, max 1%; SEC y TAF se trasladan (B3).",
    )
    firstrade = Broker(
        clave="firstrade", nombre="Firstrade (o Schwab International en acciones)", ruta="extranjero",
        sec_frac_venta=0.0000206, taf_usd_por_accion_venta=0.000195, taf_max_usd=9.79,
        bmv_disponible=False,
        conv_entrada_pct=170.33 / 20_000.0, conv_entrada_fijo_mxn=23.51,
        conv_salida_pct=12.57 / 1_100.0,
        costo_retiro_mxn=25.0 * tc,
        rendimiento_efectivo_anual=0.0, dias_espera_por_venta=1.0,
        retencion_div_en_cuenta=0.10, impuesto_div_fuera=0.09, tasa_isr_ganancias=0.10,
        fuente=("Firstrade: US$0 acciones/ETFs/opciones, sin minimo, wire de salida US$25 (Schwab "
                "International igual en acciones). Entrada con Wise 193.84 MXN por 20k (0.97%) y salida "
                "Wise 1.14%: que el broker acepte fondos de Wise y que Wise reciba el wire, no "
                "verificado. SEC/TAF trasladados: supuesto. Sin BMV."),
    )
    return {b.clave: b for b in (gbm, actinver, actinver_sin, kuspit_opt, kuspit_pru, finamex,
                                 ibkr, ibkr_etf, ibkr_fixed, firstrade)}


ESCENARIOS = {"a) baja": 12, "b) media": 48, "c) alta": 96}


def tabla_escenarios(brokers: dict[str, Broker], base: Uso, total: str) -> str:
    """Tabla markdown: filas = brokers; columnas = escenario x horizonte (MXN y % del capital)."""
    cols = [(nombre, ops, meses) for nombre, ops in ESCENARIOS.items() for meses in (6, 12)]
    enc = "| Broker | " + " | ".join(f"{n} {o} op/ano, {m} m" for n, o, m in cols) + " |"
    sep = "|---|" + "---|" * len(cols)
    filas = [enc, sep]
    for b in brokers.values():
        celdas = []
        for _, ops, meses in cols:
            u = replace(base, operaciones_anuales=ops, meses=meses)
            try:
                r = costo_total(b, u)
                celdas.append(f"{r[total]:,.0f} ({r[total + '_pct']:.2%})")
            except ValueError:
                celdas.append("n/d")
        filas.append(f"| {b.nombre} | " + " | ".join(celdas) + " |")
    return "\n".join(filas)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Costo total por broker (arena, 20k MXN)")
    ap.add_argument("--tc", type=float, default=TC_REFERENCIA)
    ap.add_argument("--desviacion", type=float, default=0.0017,
                    help="desviacion implicita del SIC por lado (fraccion)")
    ap.add_argument("--recepcion-ibkr", type=float, default=0.0,
                    help="cobro del banco mexicano por recibir el retiro SWIFT de IBKR (MXN)")
    ap.add_argument("--efectivo", type=float, default=0.0, help="fraccion promedio en efectivo")
    ap.add_argument("--fraccion-usd", type=float, default=1.0)
    ap.add_argument("--ganancia", type=float, default=0.0,
                    help="ganancia realizada anual como fraccion del capital (para el ISR diferencial)")
    args = ap.parse_args(argv)
    base = Uso(tipo_cambio=args.tc, desviacion_sic_por_lado=args.desviacion,
               fraccion_efectivo=args.efectivo, fraccion_usd=args.fraccion_usd,
               ganancia_realizada_anual_pct=args.ganancia)
    cat = catalogo(args.tc, recepcion_retiro_ibkr_mxn=args.recepcion_ibkr)
    print(f"# Costos por broker (capital {base.capital_mxn:,.0f} MXN, orden {base.orden_promedio_mxn:,.0f}, "
          f"TC {args.tc}, desviacion SIC {args.desviacion:.2%}/lado)\n")
    print("## Costo por lado de una orden en activo USD (sin promociones)\n")
    print("| Broker | MXN | % de la orden |\n|---|---|---|")
    for b in cat.values():
        r = costo_por_lado(b, base)
        print(f"| {b.nombre} | {r['mxn']:.2f} | {r['pct_orden']:.3%} |")
    for total, titulo in (("torneo", "Costo dentro de la cuenta (mueve el TWR)"),
                          ("dueno", "Costo para el dueno (incluye salida y diferencias fiscales)")):
        print(f"\n## {titulo}\n")
        print(tabla_escenarios(cat, base, total))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
