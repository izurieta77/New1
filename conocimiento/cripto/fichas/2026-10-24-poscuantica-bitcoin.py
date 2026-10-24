"""Ficha 2026-10-24: criptografía poscuántica en bitcoin (BIP-360 P2MR, BIP-361, FIPS 204/205).

Ejercicio numérico reproducible (python3 -I este_archivo.py):
  A. Recursos de Shor para ECDLP-256: fórmula de Roetteler et al. (2017) contra Babbush et al. (IACR 2026/625).
  B. Costo en espacio de bloque de firmar con ML-DSA-44 o SLH-DSA-128s dentro de una hoja P2MR,
     frente a una entrada P2TR por la ruta de llave (Schnorr).
  C. Ataque "de exposición corta" (on-spend): probabilidad de que el atacante termine antes del bloque
     que confirma, con bloques Poisson (10 min) y con los intervalos reales de los últimos bloques (mempool.space).
  D. Ataque "de exposición larga": llaves por año que barre una sola máquina según su reloj.
  E. Calendario de BIP-361 (fase A a 160,000 bloques; fase B dos años después).

Supuestos de tamaño (bytes) — fuentes primarias:
  - FIPS 204, tabla 2: ML-DSA-44 llave pública 1312, firma 2420.
  - FIPS 205, tabla 2: SLH-DSA-SHA2-128s llave pública 32, firma 7856.
  - BIP-341/342: firma Schnorr 64 bytes (SIGHASH_DEFAULT); salida P2TR 34 bytes de script.
  - BIP-360 (v0.12.1): salida P2MR = OP_2 + 32 bytes (34 de script); bloque de control 1 + 32*m (sin llave interna).
  El opcode de verificación poscuántica NO existe todavía: el tamaño de la hoja es hipotético (1 byte de opcode).
"""
import json
import math
import statistics
import urllib.request

WU_BLOQUE = 4_000_000
SEG_BLOQUE = 600


def varint(n):
    return 1 if n < 0xFD else (3 if n <= 0xFFFF else 5)


def push(n):
    """Bytes de un push de n bytes dentro de un script (OP_PUSHDATA1/2)."""
    if n <= 75:
        return 1 + n
    if n <= 255:
        return 2 + n
    return 3 + n


# ---------- A. Recursos de Shor ----------
n = 256
q_roet = 9 * n + 2 * math.ceil(math.log2(n)) + 10
t_roet = 448 * n**3 * math.log2(n) + 4090 * n**3
print("A. Roetteler 2017, n=256: qubits lógicos", q_roet, "| Toffoli %.3e" % t_roet)
for q, t in [(1200, 90e6), (1450, 70e6)]:
    print(f"   Babbush 2026: {q} qubits, {t:.0e} Toffoli -> qubits ÷{q_roet/q:.2f}, Toffoli ÷{t_roet/t:,.0f}")
print("   IonQ (sep-2026, empresa, sin arXiv): 1457 lógicos, 39e6 Toffoli, 26 días -> Toffoli ÷%.0f" % (t_roet / 39e6))

# ---------- B. Espacio de bloque ----------
NO_WIT_IN = 36 + 1 + 4          # outpoint + scriptSig vacío + secuencia
SALIDA = 8 + 1 + 34             # P2TR o P2MR
OVERHEAD_NW = 4 + 1 + 1 + 4     # versión, n_in, n_out, locktime
OVERHEAD_W = 2                  # marcador y bandera segwit


def tx_1in2out(witness_in):
    peso = 4 * (OVERHEAD_NW + NO_WIT_IN + 2 * SALIDA) + OVERHEAD_W + witness_in
    return peso, peso / 4


def wit_p2tr_key():
    return 1 + varint(64) + 64


def wit_p2mr_hoja(sig, pk, prof=1):
    script = push(pk) + 1                   # <pk> OP_CHECKSIG_PQ (hipotético)
    control = 1 + 32 * prof
    return 1 + varint(sig) + sig + varint(script) + script + varint(control) + control


casos = {
    "P2TR ruta de llave (Schnorr)": wit_p2tr_key(),
    "P2MR hoja ML-DSA-44": wit_p2mr_hoja(2420, 1312),
    "P2MR hoja SLH-DSA-128s": wit_p2mr_hoja(7856, 32),
}
base_vb = None
print("\nB. Transacción 1 entrada / 2 salidas")
for k, w in casos.items():
    peso, vb = tx_1in2out(w)
    base_vb = base_vb or vb
    txb = WU_BLOQUE / peso
    print(f"   {k:32s} testigo {w:5d} B | {vb:8.2f} vB | ×{vb/base_vb:5.2f} | {txb:6.0f} tx/bloque | {txb/SEG_BLOQUE:5.2f} tx/s | comisión a 2 sat/vB {2*vb:6.0f} sats")

# ---------- C. Exposición corta ----------
print("\nC. P(el atacante termina antes de la 1.ª confirmación), llegada de bloques Poisson λ=1/10 min")
for T in [1, 5, 9, 10, 20, 60]:
    print(f"   T={T:3d} min -> {math.exp(-T/10):.3f}")


def get(u):
    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
    return json.load(urllib.request.urlopen(req, timeout=30))


try:
    req = urllib.request.Request("https://mempool.space/api/blocks/tip/height", headers={"User-Agent": "Mozilla/5.0"})
    tip = int(urllib.request.urlopen(req, timeout=30).read())
    ts = {}
    h = tip
    while len(ts) < 301:
        for b in get(f"https://mempool.space/api/v1/blocks/{h}"):
            ts[b["height"]] = b["timestamp"]
        h = min(ts) - 1
    hs = sorted(ts)[-301:]
    dt = [(ts[hs[i]] - ts[hs[i - 1]]) / 60 for i in range(1, len(hs))]
    print(f"   Real: {len(dt)} intervalos hasta la altura {hs[-1]}; media {statistics.mean(dt):.2f} min, mediana {statistics.median(dt):.2f} (Poisson: 6.93)")
    for T in [1, 5, 9, 10, 20]:
        # Probabilidad de que el siguiente bloque tarde más de T, medido de un instante al azar (paradoja de la inspección):
        # se pondera cada intervalo por su duración: P = Σ max(dt−T,0) / Σ dt
        p_real = sum(max(d - T, 0) for d in dt) / sum(dt)
        print(f"   T={T:3d} min -> empírica (instante al azar) {p_real:.3f}")
except Exception as e:  # sin red: el resto del ejercicio no depende de esto
    print("   (sin datos de mempool.space:", e, ")")

# ---------- D. Exposición larga ----------
print("\nD. Llaves por año que barre UNA máquina (secuencial)")
for nombre, minutos in [("IonQ, reloj lento: 26 días/llave", 26 * 1440), ("reloj rápido: 1 día/llave", 1440),
                        ("reloj rápido: 10 min/llave", 10)]:
    llaves = 365 * 1440 / minutos
    print(f"   {nombre:36s} {llaves:10,.0f} llaves/año | a 50 BTC por salida P2PK: {50*llaves:12,.0f} BTC/año")

# ---------- E. BIP-361 ----------
anos_A = 160_000 * 10 / 60 / 24 / 365.25
print(f"\nE. BIP-361: fase A = 160,000 bloques = {anos_A:.2f} años tras la activación; fase B = +2 años -> {anos_A+2:.2f} años")
for act in [2027, 2028, 2029]:
    print(f"   activación {act}: fase A ~{act+anos_A:.1f}, fase B ~{act+anos_A+2:.1f}")
