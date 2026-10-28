"""Ficha 2026-10-28 · C7 · Valuación por ingreso residual (Ohlson 1995; Feltham-Ohlson 1995).
1) Identidad: con excedente limpio (B_t = B_{t-1} + X_t - D_t), el valor presente de dividendos = B_0 + VP(ingreso residual).
   Comprobación numérica con un plan sintético (sin y con recompras tratadas como distribución).
2) Contraejemplo: excedente sucio (ORI que no pasa por la utilidad) rompe la igualdad por exactamente VP del ORI.
3) Caso Visa (SEC companyfacts, XBRL 10-K): cuánto cumple el excedente limpio por año y qué ROE perpetuo
   descuenta el precio. Uso: python3 -I este.py  (data.sec.gov con el User-Agent por defecto del repo, sin correo)."""
import json, urllib.request
R = 0.09  # costo de capital supuesto para el ejemplo y para Visa (supuesto declarado)

def vp(fl, r=R):
    return sum(c / (1 + r) ** (t + 1) for t, c in enumerate(fl))

# 1) Plan sintético de 30 años + valor terminal con crecimiento g; ROE y pago cambiantes
B0, g = 100.0, 0.03
roe = [0.18 - 0.003 * t for t in range(30)]          # ROE que se desvanece de 18% a ~9%
pago = [0.5 + 0.01 * t for t in range(30)]            # pago creciente (dividendos + recompras)
B, X, D = [B0], [], []
for t in range(30):
    x = roe[t] * B[-1]; d = pago[t] * x
    X.append(x); D.append(d); B.append(B[-1] + x - d)   # excedente limpio
RI = [x - R * b for x, b in zip(X, B[:-1])]
# terminal: a partir del año 31, ROE fijo = roe[-1], crece g: dividendos y RI en perpetuidad de Gordon
x31 = roe[-1] * B[-1]; d31 = x31 * (1 - g / roe[-1]); ri31 = x31 - R * B[-1]
v_ddm = vp(D) + d31 / (R - g) / (1 + R) ** 30
v_riv = B0 + vp(RI) + ri31 / (R - g) / (1 + R) ** 30
print(f"1) DDM {v_ddm:.6f} | RIV {v_riv:.6f} | diferencia {v_ddm - v_riv:.2e}")

# 2) Excedente sucio: un ORI negativo de -2 por año reduce el libro sin pasar por la utilidad
B2, X2 = [B0], []
for t in range(30):
    x = roe[t] * B2[-1]; d = pago[t] * x
    X2.append(x); B2.append(B2[-1] + x - d - 2.0)
D2 = [p * x for p, x in zip(pago, X2)]
RI2 = [x - R * b for x, b in zip(X2, B2[:-1])]
x31 = roe[-1] * B2[-1]; d31 = x31 * (1 - g / roe[-1]); ri31 = x31 - R * B2[-1]
v_ddm2 = vp(D2) + d31 / (R - g) / (1 + R) ** 30
v_riv2 = B0 + vp(RI2) + ri31 / (R - g) / (1 + R) ** 30
print(f"2) excedente sucio: DDM {v_ddm2:.4f} | RIV {v_riv2:.4f} | RIV−DDM {v_riv2 - v_ddm2:.4f} | VP del ORI (30 años) {vp([2.0]*30):.4f}")

# 3) Visa (CIK 1403161), valores anuales de 10-K
req = urllib.request.Request("https://data.sec.gov/api/xbrl/companyfacts/CIK0001403161.json",
                             headers={"User-Agent": "SistemaInversionNew1/1.0 investigacion", "Accept-Encoding": "identity"})
f = json.load(urllib.request.urlopen(req, timeout=60))["facts"]["us-gaap"]
def anual(tag, inst=False):
    """Valores de 10-K: instantes al cierre fiscal (30-sep) o duraciones de ~1 año; el último presentado gana."""
    import datetime as dt
    out = {}
    for u in sorted(f.get(tag, {}).get("units", {}).get("USD", []), key=lambda z: z.get("filed", "")):
        if u.get("form") != "10-K" or u["end"][5:7] != "09": continue
        if not inst:
            if not u.get("start"): continue
            dias = (dt.date.fromisoformat(u["end"]) - dt.date.fromisoformat(u["start"])).days
            if not 350 <= dias <= 380: continue
        out[u["end"]] = u["val"]
    return out
eq = {**anual("StockholdersEquity", inst=True), **anual("StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest", inst=True)}
ni = anual("NetIncomeLoss")
dv = anual("PaymentsOfDividends") or anual("PaymentsOfDividendsCommonStock")
rp = anual("PaymentsForRepurchaseOfCommonStock")
oci = anual("OtherComprehensiveIncomeLossNetOfTax")
fechas = sorted(d for d in eq if d[5:7] == "09")
print("3) Visa: año | B | X | D+recompra | ORI | ΔB − (X − D) | residuo sin ORI | ROE")
for a, b in zip(fechas, fechas[1:]):
    if b in ni and b in dv and b in rp:
        dB = eq[b] - eq[a]; clean = ni[b] - dv[b] - rp[b]; o = oci.get(b, 0)
        print(f"   {b[:4]} | {eq[b]/1e9:6.1f} | {ni[b]/1e9:5.1f} | {(dv[b]+rp[b])/1e9:5.1f} | {o/1e9:5.2f} | {(dB-clean)/1e9:6.2f} | {(dB-clean-o)/1e9:6.2f} | {ni[b]/eq[a]:.1%}")
ult = fechas[-1]
print(f"   último patrimonio 10-K {ult}: {eq[ult]/1e9:.1f} mil M USD")

# 4) Qué descuenta el precio (RIV con ROE y crecimiento constantes; supuesto: B y ROE del FY25, r = 9%)
P, N = 401.86, 1.882e9           # cierre del 27-oct (Yahoo) y acciones clase A diluidas del 4T FY26 (8-K del 27-oct)
B, roe = eq["2025-09-30"], ni["2025-09-30"] / eq["2024-09-30"]
mc = P * N
g_impl = R - (roe - R) * B / (mc - B)
print(f"4) cap. de mercado {mc/1e9:.0f} mil M; B {B/1e9:.1f}; ROE {roe:.1%}; g perpetuo del RI implícito = {g_impl:.2%}")
# segunda comprobación: Gordon sobre distribuciones con pago = 1 − g/ROE debe dar el mismo valor
x1 = roe * B; d1 = x1 * (1 - g_impl / roe)
print(f"   Gordon: D1 {d1/1e9:.1f} mil M / (r − g) = {d1/(R - g_impl)/1e9:.0f} mil M (debe igualar {mc/1e9:.0f})")
for r_alt in (0.08, 0.10):
    print(f"   sensibilidad r = {r_alt:.0%}: g implícito = {r_alt - (roe - r_alt) * B / (mc - B):.2%}")
