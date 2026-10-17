#!/usr/bin/env python3
"""Ejercicio de la ficha 2026-10-17 (incidente Ledger/CryptoBilis).

1) Lee en mempool.space las 3 direcciones BTC que publicó Specter (9-oct-2026):
   recibido, gastado, saldo, primera y última transacción (paginación completa).
2) Comprueba que las direcciones no se traslapan (una no paga a otra).
3) Cronología: minutos entre la primera entrada observada, el aviso de Specter
   y el primer comunicado de Ledger (@Ledger_Support, 9-oct 13:32:12 UTC).
4) Escala: BTC visto vs. cifras de prensa (86, 93.2 M USD) y pérdida media por
   cartera con el dato de Bitquery (315 carteras; grado D, Ledger no lo confirma).
5) Ventana de 90 días de Ledger: fecha de compra más antigua afectada.

Uso: python3 -I 2026-10-17-ledger-cadena-suministro.py <precio_btc_usd>
Solo lectura de API públicas; no usa claves.
"""
import datetime as dt
import json
import sys
import urllib.request

DIRS = [
    "bc1qjqgwejnp8dc0x2938x9n9954hj97t82unx49dl",
    "bc1qqnkwurxs99xkx5t4yffqhq3u6qwy0qpjyujtm9",
    "bc1qgqheemzla77pesl227hdtgf5ykz62d0zvld26n",
]
API = "https://mempool.space/api/address/"
U = dt.timezone.utc


def get(url):
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)


def txs_completas(a):
    out, last = [], None
    while True:
        b = get(API + a + "/txs/chain" + (f"/{last}" if last else ""))
        if not b:
            break
        out += b
        last = b[-1]["txid"]
        if len(b) < 25:
            break
    return out


def main():
    precio = float(sys.argv[1])
    tot_rec = tot_bal = 0.0
    primeras = []
    datos = {}
    for a in DIRS:
        st = get(API + a)["chain_stats"]
        txs = txs_completas(a)
        assert len(txs) == st["tx_count"], (a, len(txs), st["tx_count"])
        ts = [t["status"]["block_time"] for t in txs]
        rec, gas = st["funded_txo_sum"] / 1e8, st["spent_txo_sum"] / 1e8
        datos[a] = txs
        tot_rec += rec
        tot_bal += rec - gas
        primeras.append(min(ts))
        print(f"{a[:14]}… tx={st['tx_count']:4d} recibido={rec:10.4f} gastado={gas:10.4f} "
              f"saldo={rec-gas:10.4f}  1a={dt.datetime.fromtimestamp(min(ts), U):%Y-%m-%d %H:%M} "
              f"ult={dt.datetime.fromtimestamp(max(ts), U):%Y-%m-%d %H:%M}")
    # traslape: ¿alguna dirección paga a otra de la lista?
    cruce = 0.0
    for a, txs in datos.items():
        for t in txs:
            if any(v.get("prevout", {}).get("scriptpubkey_address") == a for v in t["vin"]):
                cruce += sum(o["value"] for o in t["vout"]
                             if o.get("scriptpubkey_address") in DIRS and o.get("scriptpubkey_address") != a) / 1e8
    print(f"BTC que pasa de una dirección listada a otra: {cruce:.8f}")
    print(f"Total recibido (sin doble conteo si cruce=0): {tot_rec:.4f} BTC = {tot_rec*precio/1e6:.2f} M USD a {precio:,.2f}")
    print(f"Saldo inmóvil: {tot_bal:.4f} BTC = {tot_bal*precio/1e6:.2f} M USD")
    for ref in (86.0, 93.2):
        print(f"  BTC visto / {ref} M USD de prensa = {100*tot_rec*precio/1e6/ref:.1f}%")
    print(f"Pérdida media por cartera (93.2 M / 315, Bitquery, grado D): {93.2e6/315:,.0f} USD")
    # cronología
    t0 = dt.datetime.fromtimestamp(min(primeras), U)
    specter = dt.datetime(2026, 10, 9, 12, 24, 31, tzinfo=U)
    ledger1 = dt.datetime(2026, 10, 9, 13, 32, 12, tzinfo=U)
    print(f"Primera entrada observada: {t0:%Y-%m-%d %H:%M:%S} UTC")
    print(f"  → aviso de Specter: {(specter-t0).total_seconds()/3600:.1f} h; → 1er comunicado de Ledger: {(ledger1-t0).total_seconds()/3600:.1f} h")
    print(f"  Specter → Ledger: {(ledger1-specter).total_seconds()/60:.0f} min")
    print(f"Ventana de 90 días de Ledger (desde el 9-oct): compras desde el {(dt.date(2026,10,9)-dt.timedelta(90))}")


if __name__ == "__main__":
    main()
