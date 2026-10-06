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
 "n_anios": 11,
 "exceso_bruto_medio": 0.01228871790737719,
 "exceso_neto_medio": -0.007711282092622813,
 "aciertos": 6,
 "aciertos_neto": 4,
 "sd_exceso": 0.09226850455626243,
 "ic80_neto": [
  -0.04159782508479346,
  0.026660441864424456
 ],
 "exceso_neto_vs_iwm": 0.005440956431318308,
 "ret_S_medio": 0.14580968117171894,
 "ret_C_medio": 0.13352096326434176,
 "iwm_medio": 0.12036872474040063,
 "error_est": 0.027820000870938194,
 "efecto_min_detectable_80pot": 0.07789600243862693
}
```

{'anio': 2015, 'n_S': 14, 'faltan_S': 0, 'n_C': 65, 'faltan_C': 0, 'ret_S': -0.0706857142857143, 'ret_S_med': -0.16975, 'ret_C': -0.0022138461538461504, 'iwm': -0.06574582218741132}
{'anio': 2016, 'n_S': 30, 'faltan_S': 0, 'n_C': 55, 'faltan_C': 0, 'ret_S': 0.28201333333333334, 'ret_S_med': 0.2813, 'ret_C': 0.3332145454545455, 'iwm': 0.2444121021141472}
{'anio': 2017, 'n_S': 33, 'faltan_S': 0, 'n_C': 57, 'faltan_C': 0, 'ret_S': 0.1471090909090909, 'ret_S_med': 0.058, 'ret_C': 0.09818771929824562, 'iwm': 0.17713929186495592}
{'anio': 2018, 'n_S': 30, 'faltan_S': 0, 'n_C': 61, 'faltan_C': 0, 'ret_S': -0.02144333333333334, 'ret_S_med': -0.0561, 'ret_C': 0.039336065573770486, 'iwm': -0.03538897080372905}
{'anio': 2019, 'n_S': 44, 'faltan_S': 0, 'n_C': 53, 'faltan_C': 0, 'ret_S': 0.05002727272727273, 'ret_S_med': 0.0128, 'ret_C': -0.11446226415094339, 'iwm': -0.06586786825202895}
{'anio': 2020, 'n_S': 34, 'faltan_S': 0, 'n_C': 59, 'faltan_C': 0, 'ret_S': 0.6334147058823529, 'ret_S_med': 0.51, 'ret_C': 0.6233576271186441, 'iwm': 0.6185550795763084}
{'anio': 2021, 'n_S': 29, 'faltan_S': 0, 'n_C': 54, 'faltan_C': 0, 'ret_S': -0.12688275862068965, 'ret_S_med': -0.0744, 'ret_C': -0.15764074074074075, 'iwm': -0.2537211378288896}
{'anio': 2022, 'n_S': 47, 'faltan_S': 0, 'n_C': 51, 'faltan_C': 0, 'ret_S': 0.23441702127659575, 'ret_S_med': 0.2055, 'ret_C': 0.0562313725490196, 'iwm': 0.12382254808702431}
{'anio': 2023, 'n_S': 32, 'faltan_S': 0, 'n_C': 45, 'faltan_C': 0, 'ret_S': 0.073246875, 'ret_S_med': 0.0037, 'ret_C': 0.09186888888888889, 'iwm': 0.09831626709656405}
{'anio': 2024, 'n_S': 36, 'faltan_S': 0, 'n_C': 45, 'faltan_C': 0, 'ret_S': -0.02578333333333333, 'ret_S_med': -0.0038000000000000004, 'ret_C': 0.08802666666666667, 'iwm': 0.07574736320055697}
{'anio': 2025, 'n_S': 30, 'faltan_S': 0, 'n_C': 57, 'faltan_C': 0, 'ret_S': 0.4284733333333333, 'ret_S_med': 0.1425, 'ret_C': 0.41282456140350876, 'iwm': 0.406787119276909}

Supervivencia:
{'anio': 2015, 'emisores_NI_pos': 3073, 'con_ticker_vigente': 1549}
{'anio': 2016, 'emisores_NI_pos': 2766, 'con_ticker_vigente': 1532}
{'anio': 2017, 'emisores_NI_pos': 2719, 'con_ticker_vigente': 1629}
{'anio': 2018, 'emisores_NI_pos': 2759, 'con_ticker_vigente': 1732}
{'anio': 2019, 'emisores_NI_pos': 2696, 'con_ticker_vigente': 1780}
{'anio': 2020, 'emisores_NI_pos': 2569, 'con_ticker_vigente': 1816}
{'anio': 2021, 'emisores_NI_pos': 2243, 'con_ticker_vigente': 1692}
{'anio': 2022, 'emisores_NI_pos': 2715, 'con_ticker_vigente': 2100}
{'anio': 2023, 'emisores_NI_pos': 2531, 'con_ticker_vigente': 2055}
{'anio': 2024, 'emisores_NI_pos': 2647, 'con_ticker_vigente': 2234}
{'anio': 2025, 'emisores_NI_pos': 2658, 'con_ticker_vigente': 2337}
