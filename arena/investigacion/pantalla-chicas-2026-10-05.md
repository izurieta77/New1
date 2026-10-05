# Pantalla de empresas chicas, 2026-10-05 (salida automatica del script)

## Operabilidad (BMV y SIC, datos al 2026-10-05)

```json
{
 "BMV": {
  "total": 110,
  "con_cik": null,
  "con_precio": 106,
  "en_banda": 47,
  "banda_liq": 25,
  "banda_origen_adv_1M_usd": 0,
  "banda_origen_y_titulo": 0,
  "banda_liq_titulo": 25,
  "sin_dato_mcap": 12,
  "mediana_mcap_usd_m": 1962,
  "menores_2b": 47,
  "menores_10b": 77
 },
 "SIC": {
  "total": 449,
  "con_cik": 412,
  "con_precio": 326,
  "en_banda": 53,
  "banda_liq": 2,
  "banda_origen_adv_1M_usd": 52,
  "banda_origen_y_titulo": 52,
  "banda_liq_titulo": 1,
  "sin_dato_mcap": 10,
  "mediana_mcap_usd_m": 33734,
  "menores_2b": 35,
  "menores_10b": 95
 }
}
```

## Embudo

```json
{
 "universo_total": 559,
 "con_precio_y_cik_o_bmv": 432,
 "F1_tamano": 100,
 "F8_liquidez": 27,
 "F9_titulo": 26,
 "fundamentales_F2_a_F7": 0,
 "fundamentales_y_liquidez": 0,
 "TODOS_los_filtros": 0,
 "fallas_por_filtro_en_banda": {
  "F3 ROIC": 86,
  "F4 ND/EBITDA": 72,
  "F6 EV/EBIT": 72,
  "F2 UDM": 57,
  "F7 dilucion": 31,
  "F2 NI(0)": 28,
  "F5 FCF": 59,
  "F2 NI": 50
 },
 "casi_pasan_(<=1_falla)": 10
}
```

## Candidatos (fundamentales OK; columna operable)

| origen | simbolo | operable | mcap USD M | NI0 M | CAGR NI | ROIC | ND/EBITDA | EV/EBIT | costo RT 2k | edgar |
|---|---|---|---|---|---|---|---|---|---|---|
| BMV | CIEB.MX | NO | 991 | 11134.4 | 2.031 | 0.957 | -0.34 | 1.0 | 0.0088 | BMV: segunda fuente no disponi |
| BMV | PINFRAL.MX | NO | 4104 | 14643.3 | 0.557 | 0.272 | -1.02 | 1.8 | 0.0088 | BMV: segunda fuente no disponi |
| BMV | HERDEZ.MX | SI | 974 | 1786.4 | 0.163 | 0.287 | 0.27 | 3.4 | 0.0097 | BMV: segunda fuente no disponi |
| BMV | GPROFUT.MX | NO | 1878 | 4067.7 | 0.239 | 0.277 | 0.62 | 5.4 | 0.0088 | BMV: segunda fuente no disponi |
| BMV | CMOCTEZ.MX | NO | 3985 | 6260.6 | 0.008 | 0.423 | -0.77 | 6.7 | 0.0088 | BMV: segunda fuente no disponi |
| BMV | LABB.MX | SI | 678 | 1614.0 | 0.254 | 0.109 | 1.54 | 5.7 | 0.0131 | BMV: segunda fuente no disponi |
| BMV | FRAGUAB.MX | NO | 2248 | 4902.0 | 0.242 | 0.12 | -0.38 | 7.9 | 0.0088 | BMV: segunda fuente no disponi |
| BMV | BOLSAA.MX | SI | 1167 | 1602.0 | 0.031 | 0.234 | -1.05 | 6.9 | 0.0131 | BMV: segunda fuente no disponi |
| BMV | OMAB.MX | SI | 4607 | 5341.7 | 0.032 | 0.263 | 1.15 | 10.3 | 0.0088 | BMV: segunda fuente no disponi |
| BMV | GRUMAB.MX | SI | 4406 | 519.3 | 0.1 | 0.129 | 1.67 | 111.3 | 0.0124 | BMV: segunda fuente no disponi |

## Backtest

```json
{
 "n_anios": 6,
 "exceso_bruto_medio": 0.1669491393268567,
 "exceso_neto_medio": 0.14694913932685671,
 "aciertos": 2,
 "aciertos_neto": 2,
 "sd_exceso": 0.3847377400612668,
 "ic80_neto": [
  -0.013442527339809973,
  0.32772637362637363
 ],
 "exceso_neto_vs_iwm": 0.04921069133119286,
 "ret_S_medio": 0.17943333333333333,
 "ret_C_medio": 0.01248419400647662,
 "iwm_medio": 0.11022264200214048,
 "error_est": 0.1570685246569423,
 "efecto_min_detectable_80pot": 0.4397918690394384,
 "sens_faltantes": {
  "0.0": 0.14694913932685671,
  "-0.5": 0.14694913932685671,
  "-1.0": 0.14694913932685671
 }
}
```

{'anio': 2015, 'n_S': 1, 'faltan_S': 0, 'n_C': 13, 'faltan_C': 0, 'ret_S': -0.2024, 'ret_S_med': -0.2024, 'ret_C': -0.1389153846153846, 'iwm': -0.06574582218741132}
{'anio': 2016, 'n_S': 2, 'faltan_S': 0, 'n_C': 12, 'faltan_C': 0, 'ret_S': 0.1688, 'ret_S_med': 0.1688, 'ret_C': 0.28729166666666667, 'iwm': 0.2444121021141472}
{'anio': 2017, 'n_S': 1, 'faltan_S': 0, 'n_C': 10, 'faltan_C': 0, 'ret_S': 0.8202, 'ret_S_med': 0.8202, 'ret_C': 0.06215, 'iwm': 0.17713929186495592}
{'anio': 2018, 'n_S': 1, 'faltan_S': 0, 'n_C': 14, 'faltan_C': 0, 'ret_S': -0.1841, 'ret_S_med': -0.1841, 'ret_C': -0.07456428571428571, 'iwm': -0.03538897080372905}
{'anio': 2019, 'n_S': 1, 'faltan_S': 0, 'n_C': 7, 'faltan_C': 0, 'ret_S': -0.4014, 'ret_S_med': -0.4014, 'ret_C': -0.38662857142857143, 'iwm': -0.06586786825202895}
{'anio': 2020, 'n_S': 0, 'faltan_S': 0, 'n_C': 8, 'faltan_C': 0, 'ret_S': None, 'ret_S_med': None, 'ret_C': 0.52115, 'iwm': 0.6185550795763084}
{'anio': 2021, 'n_S': 0, 'faltan_S': 0, 'n_C': 11, 'faltan_C': 0, 'ret_S': None, 'ret_S_med': None, 'ret_C': -0.4163363636363636, 'iwm': -0.2537211378288896}
{'anio': 2022, 'n_S': 0, 'faltan_S': 0, 'n_C': 4, 'faltan_C': 0, 'ret_S': None, 'ret_S_med': None, 'ret_C': -0.31422500000000003, 'iwm': 0.12382254808702431}
{'anio': 2023, 'n_S': 0, 'faltan_S': 0, 'n_C': 7, 'faltan_C': 0, 'ret_S': None, 'ret_S_med': None, 'ret_C': 0.28054285714285715, 'iwm': 0.09831626709656405}
{'anio': 2024, 'n_S': 0, 'faltan_S': 0, 'n_C': 6, 'faltan_C': 0, 'ret_S': None, 'ret_S_med': None, 'ret_C': 0.16873333333333332, 'iwm': 0.07574736320055697}
{'anio': 2025, 'n_S': 4, 'faltan_S': 0, 'n_C': 46, 'faltan_C': 0, 'ret_S': 0.8755, 'ret_S_med': 0.16695000000000002, 'ret_C': 0.3255717391304348, 'iwm': 0.406787119276909}

Supervivencia:
{'anio': 2015, 'emisores_NI_pos': 376, 'con_ticker_vigente': 61}
{'anio': 2016, 'emisores_NI_pos': 316, 'con_ticker_vigente': 62}
{'anio': 2017, 'emisores_NI_pos': 292, 'con_ticker_vigente': 72}
{'anio': 2018, 'emisores_NI_pos': 286, 'con_ticker_vigente': 83}
{'anio': 2019, 'emisores_NI_pos': 280, 'con_ticker_vigente': 85}
{'anio': 2020, 'emisores_NI_pos': 227, 'con_ticker_vigente': 82}
{'anio': 2021, 'emisores_NI_pos': 217, 'con_ticker_vigente': 78}
{'anio': 2022, 'emisores_NI_pos': 261, 'con_ticker_vigente': 90}
{'anio': 2023, 'emisores_NI_pos': 238, 'con_ticker_vigente': 91}
{'anio': 2024, 'emisores_NI_pos': 246, 'con_ticker_vigente': 106}
{'anio': 2025, 'emisores_NI_pos': 390, 'con_ticker_vigente': 247}
