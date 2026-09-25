# Empresas y geopolitica: edgar.py, dossier.py, geopolitica.py

Python 3.11, solo biblioteca estandar. Se corren desde la raiz del repo (`/home/user/New1`). Descargas en
cache en `datos/cache/` (ignorado por git). Si una fuente falla, la herramienta lo reporta y sigue.

Pruebas (sin red): `python3 -m unittest discover -s herramientas/tests -t .`
(`test_edgar.py`, `test_dossier.py`, `test_geopolitica.py`; fixtures en `herramientas/tests/fixtures/`).

## 1. edgar.py: estados financieros y presentaciones desde SEC EDGAR

```
python3 herramientas/edgar.py NVDA --periodo trimestral          # 8 trimestres + TTM + balance + presentaciones
python3 herramientas/edgar.py WMT --periodo anual --n 5
python3 herramientas/edgar.py MSFT --periodo trimestral --json   # todo el resultado en JSON
python3 herramientas/edgar.py NVDA --form4                       # compras/ventas de insiders (requiere correo, ver abajo)
```

Opciones: `--n` periodos (default 5 anual / 8 trimestral), `--presentaciones N` (0 = ninguna),
`--cache-horas H` (default 12; 0 = sin cache).

### User-Agent (comprobado el 2026-09-25)

| Endpoint | Sin correo (default `SistemaInversionNew1/1.0 investigacion`) | Con correo |
|---|---|---|
| data.sec.gov (companyfacts, submissions) | funciona | funciona |
| www.sec.gov/files/company_tickers.json | 403 | funciona |
| www.sec.gov/Archives (XML de Form 4) | 403 | funciona |
| efts.sec.gov (busqueda de entidades) | funciona | funciona |

Sin correo, `cik_de_ticker` resuelve el CIK con la busqueda de entidades de EDGAR, y `--form4` se omite con aviso.
Para todo: `export SEC_USER_AGENT="SistemaInversionNew1 tu_correo@dominio.com"`. Ritmo: maximo ~9 solicitudes/s
(la politica de la SEC permite 10/s).

### Funciones

| Funcion | Que hace |
|---|---|
| `cik_de_ticker(t)` / `info_ticker(t)` | CIK (cache 7 dias en `datos/cache/sec_company_tickers.json`) |
| `hechos_compania(cik_o_ticker)` | JSON companyfacts completo |
| `estados_financieros(t, "anual"\|"trimestral")` | filas normalizadas + TTM + metricas (ver abajo) |
| `extraer_estados(json, periodo)` | lo mismo sin red, a partir de un JSON companyfacts |
| `presentaciones_recientes(t, tipos=("8-K","10-Q","10-K","4"), n=20)` | fecha, forma, items 8-K con descripcion, alerta, URL |
| `transacciones_form4(t, n=20)` | compras (P) y ventas (S) de insiders, ventas bajo plan 10b5-1 |
| `verificar_vigencia(estados, submissions)` | avisa si companyfacts va atrasado frente al ultimo 10-K/10-Q/20-F |

Campos: ingresos, costo de ventas, utilidad bruta, operativa y neta, UPA diluida, flujo operativo, capex, FCF,
SBC, efectivo, inversiones CP, deuda (largo plazo incluida la porcion circulante + corto plazo; sin
arrendamientos), deuda neta, capital contable, acciones diluidas promedio. Metricas: margenes, crecimiento a/a,
SBC/ingresos, dilucion a/a, conversion de caja (FCF/utilidad neta), cambio de margen en pp.

### Metodo y limites (leer antes de confiar en una cifra)

1. Conceptos alternativos por periodo en orden de prioridad (p. ej. NVDA migro de
   `PaymentsToAcquirePropertyPlantAndEquipment` a `PaymentsToAcquireProductiveAssets`; MSFT de `SalesRevenueNet`
   a `RevenueFromContractWithCustomer...`; bancos usan `RevenuesNetOfInterestExpense`). La linea
   "Conceptos XBRL usados" dice cual se uso.
2. Si un periodo aparece en varias presentaciones, gana la mas reciente (incluye reexpresiones).
3. Splits: se detectan cuando el mismo periodo de acciones promedio aparece reexpresado por ~2, 3, 4, 10...
   en una presentacion posterior; acciones y UPA previas se ajustan (NVDA 4:1 en 2021 y 10:1 en 2024, WMT 3:1 en 2024).
4. Calendario fiscal: solo los periodos de ~12 meses de formas anuales (10-K/20-F/40-F) definen anio fiscal; se
   ignoran columnas de "ultimos doce meses" de algunos 10-Q (AMZN). Etiqueta FY = anio en que termina.
5. Q4 = anual - 9M. Flujo de efectivo trimestral = acumulado - acumulado previo (en 10-Q solo viene acumulado).
   UPA derivada es aproximada; acciones Q4 = 4 x anual - (Q1+Q2+Q3). Todo lo derivado queda marcado.
6. Una sola moneda por emisora (la de reporte): evita mezclar pesos con traducciones de conveniencia a USD en 20-F.
7. Cambio de acciones > 5x o < 0.2x sin split detectado = error de escala del XBRL: la dilucion se descarta y se anota.
8. Emisoras 20-F/40-F: la SEC solo recibe el anual en XBRL (algunas mandan 6-K en XBRL). Caso real: AMX presento
   su 20-F FY2025 el 2026-04-28 y companyfacts seguia en FY2024 al 2026-09-25; la herramienta lo avisa.
9. companyfacts no trae datos dimensionales (ingresos por region o segmento): esos van del 10-K.

Validacion en vivo (2026-09-25) contra cifras publicadas: NVDA FY2026 ingresos 215,938 M (comunicado: $215.9B),
UPA 4.90; Q2 FY2027 96,221 M ($96.2B), UPA 2.46. MSFT FY2026 331,839 M ($331.8B), utilidad neta 133,749 M
($133.7B); Q4 90,007 M ($90.0B), UPA 4.81. WMT FY2026 713,163 M ($713.163B); Q2 FY2027 187,937 M, +5.9% ($187.9B, +5.9%).

## 2. dossier.py: dossier de empresa

```
python3 herramientas/dossier.py MSFT                     # escribe empresas/MSFT/dossier-AAAA-MM-DD.md
python3 herramientas/dossier.py WALMEX.MX                # emisora BMV sin EDGAR: plantilla + precio + fuentes
python3 herramientas/dossier.py AMXB.MX                  # BMV con 20-F en la SEC (mapeo automatico a AMX)
python3 herramientas/dossier.py XYZ.MX --edgar-ticker XYZ   # mapeo manual a un ticker de la SEC
python3 herramientas/dossier.py NVDA --stdout --tasas 0.09,0.10 --crecimiento-terminal 0.025
```

Opciones: `--fecha`, `--salida-dir`, `--cache-horas`, `--tasas` (reverse DCF), `--crecimiento-terminal`,
`--form4`, `--stdout`.

Secciones: 0 resumen automatico · 1 precio y momentum (1m/3m/6m/12m, 12-1, SMA50/200, maximo 52s, volatilidad,
drawdown, beta vs ^GSPC o ^MXX) · 2 contexto · 3 estados (8 trimestres, TTM, 5 anios, balance) · 4 valuacion
(capitalizacion, EV, P/U, P/FCF, FCF yield y FCF-SBC yield, EV/ingresos, EV/EBIT, reverse DCF a 10 anios) ·
5 alertas · 6 presentaciones y Form 4 · 7-13 secciones del analista (negocio y moat, gerencia y asignacion de
capital, exposicion geopolitica y regulatoria con ingresos por region y cadena causal, catalizadores con fecha,
escenarios bear/base/bull con valor esperado, pronostico del proximo reporte con ancla ingenua e intervalo empirico
de 80% y comando para el ledger, riesgos y criterio para matar la tesis) · 14 tamano de posicion leido de
`config/parametros.json` · 15 fuentes.

Alertas automaticas (heuristicas de calidad; no son limites de riesgo): dilucion > 3%/anio (TTM y CAGR 3 anios),
conversion de caja < 0.7 (TTM y ultimo anio), SBC > 10% de ingresos, caida de margen operativo o bruto > 2 pp a/a,
utilidad neta TTM negativa, 8-K con items graves (1.03, 1.05, 2.04-2.06, 3.01, 4.01, 4.02, 5.01) o enmiendas en 12 meses.

Emisoras mexicanas (`.MX`): precio y momentum de Yahoo; fuentes BMV Emisnet, informacion XBRL de la BMV, BIVA y
CNBV; plantilla trimestral a capturar; fecha limite del proximo reporte segun la Circular Unica de Emisoras
(20 dias habiles tras Q1-Q3, 40 tras Q4; sin feriados). Con 20-F en la SEC (AMXB, FEMSAUBD, CEMEXCPO, KOFUBL,
ASURB, OMAB, GAPB, VISTAA, SIMECB, TLEVISACPO) agrega el anual de EDGAR en la moneda de reporte.

Uso con el skill `ficha-empresa`: el dossier es la materia prima; la ficha (`empresas/<TICKER>/ficha.md`) es el
juicio del analista. Pronosticos: `python3 herramientas/pronosticos.py agregar ...` y, para el ledger de la
empresa, `python3 herramientas/pronosticos.py --archivo empresas/<TICKER>/pronosticos.csv agregar ...`.

## 3. geopolitica.py: monitor de riesgo geopolitico

```
python3 herramientas/geopolitica.py                                   # imprime el monitor
python3 herramientas/geopolitica.py --salida bitacora/briefs/AAAA-MM-DD-geopolitica.md
python3 herramientas/geopolitica.py --palabras "Fed,Banxico,tariff,Taiwan,Iran,oil" --volumen-min 5000
python3 herramientas/geopolitica.py --sin-ai-gpr --sin-kalshi --json
```

Opciones: `--palabras`, `--paises` (ISO3), `--max-por-palabra` (6), `--volumen-min` (10,000), `--cache-horas` (6),
`--sin-gpr`, `--sin-ai-gpr`, `--sin-polymarket`, `--sin-kalshi`, `--json`, `--salida`. Tarda ~35 s sin cache.

Contenido:

1. GPR de Caldara e Iacoviello (https://www.matteoiacoviello.com/gpr.htm): mensual (total, amenazas, actos,
   percentil desde 1985, por pais) y diario (media 7/30 dias, picos de 90 dias). No hay CSV (404 al 2026-09-25);
   el `.xls` es BIFF8 y no se lee con la biblioteca estandar, asi que se lee el `.dta` de Stata con un lector propio.
2. AI-GPR (https://www.matteoiacoviello.com/ai_gpr.html): version con LLM que si publica CSV: total, amenazas,
   actos, riesgo petrolero, tipo de evento (conflicto militar, sanciones, etc.) y paises (incluye Iran).
3. Polymarket (gamma-api `/public-search`, respaldo `/markets`) y Kalshi (API oficial v2: `/series` por categoria
   -> `/events` abiertos con mercados; respaldo `/v1/search`, no documentado). Por palabra clave: probabilidad
   implicita (punto medio si el diferencial es <= 0.10, si no ultimo precio), compra/venta, volumen y cierre.
   Filtros: sin clima, deportes ni parlays; "Mexico" no coincide con "New Mexico"; maximo 3 mercados por evento;
   se quitan colas < 1% o > 99% en eventos con varios resultados; si nada pasa el volumen minimo se muestran los
   3 mejores marcados "(bajo)".
4. Fuentes primarias para revisar (Banxico, DOF, SHCP, SE, INEGI, Fed, Casa Blanca, Federal Register, USTR, BIS,
   OFAC, EIA, MOFCOM, Defensa de Taiwan, Comision Europea, OPEP, ISW, OIEA, ACLED, FMI).
5. Estado de las fuentes (que fallo y que respaldo se uso).

Limites: Kalshi responde 429 si se le pide rapido (~20 lecturas/s en el nivel basico; sin Retry-After): la
herramienta pausa 0.25 s y reintenta con backoff exponencial. El volumen de Kalshi esta en contratos y el de
Polymarket en USD. Las fechas de cierre de algunos eventos de Polymarket vienen mal en la API; verificar en la pagina.
