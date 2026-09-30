from analisis import *
per = [(date(2006,2,24), date(2007,12,10)), (date(2014,6,6), date(2016,2,16)), (date(2026,3,27), date(2026,9,30))]
for a, b in per:
    xs = []
    for t in fk:
        if a <= t <= b and add_m(t, 12) <= ULT:
            r = fwd(t); xs.append((r["c12"], r["maxdep12"], r["c1"], r["c3"], r["c6"]))
    print(a, b, resumen(xs, 0, "c12"), "|", resumen(xs, 1, "maxdep12"))
# 2006-07: ventanas que incluyen oct-2008 vs no
a, b = per[0]
x1 = [fwd(t) for t in fk if a <= t <= b and add_m(t, 12) < date(2008,9,15)]
x2 = [fwd(t) for t in fk if a <= t <= b and add_m(t, 12) >= date(2008,9,15)]
print("2006-07 ventana 12m termina antes de Lehman:", resumen([(r['c12'], r['maxdep12'],0,0,0) for r in x1],0,'c12'), resumen([(r['c12'], r['maxdep12'],0,0,0) for r in x1],1,'maxdep'))
print("2006-07 ventana 12m incluye Lehman:", resumen([(r['c12'], r['maxdep12'],0,0,0) for r in x2],0,'c12'), resumen([(r['c12'], r['maxdep12'],0,0,0) for r in x2],1,'maxdep'))
# FIX nivel en cada periodo
for a, b in per:
    w = [(t, v) for t, v in fixl if a <= t <= b]
    print(a, b, "FIX ini", w[0], "fin", w[-1], "max", max(w, key=lambda z: z[1]), "min", min(w, key=lambda z: z[1]), f"cambio periodo {100*(w[-1][1]/w[0][1]-1):.1f}%")
# 1,3,6 meses en el estado <=3 (mensual) vs base
M = mensual()
lo = [fwd(v[1]) for k, v in M.items() if v[0] <= 3.0 and date(2006,1,1) <= v[1]]
for h in ("c1","c3","c6"):
    vv=[r[h] for r in lo if r[h] is not None]; print(h, "<=3 fin de mes n", len(vv), "mediana", st.median(vv))
# ultimo mes (sep 2026) y rango desde minimo
print("FIX 2026-09-04 -> 2026-09-29:", round(100*(18.071/16.8748-1),2), "% ; a 28-sep:", round(100*(17.8413/16.8748-1),2))
# dif > 6: ultimos dias
print("ultimo dia dif>6:", max(s[0] for s in serie if s[3] > 6), " ultimo dia dif>=6:", max(s[0] for s in serie if s[3] >= 6))
# variante Fed limite inferior hoy
print("hoy con limite inferior (4.00-0.25):", 6.5 - 3.75)
