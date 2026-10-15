# AC-19-R14: ejecución B independiente de R14 (rebote tras desplome de un día)

- **Auditor:** `auditor-de-replicas` (ejecución B). Fecha: 2026-10-15 (UTC).
- **Independencia:** solo se leyó el pre-registro (§1-9) de `laboratorio/replicas/R14-rebote-tras-desplome.md`. No se leyeron `R14.py` ni `R14-salida.txt`. Código propio: `b.py` (stdlib; `python3 -I b.py`). Salida completa: `salida.txt`.

## 1. Fuentes (descargadas el 2026-10-15 a las 17:50 UTC)

| Índice | Archivo (`datos/`) | URL | Periodo usado | sha256 |
|---|---|---|---|---|
| S&P 500 | yahoo_GSPC.json | `https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC?period1=-1325635200&period2=<16-oct-2026>&interval=1d` | 1927-12-30 a 2026-10-14 | 6f64b3d5ac3e28ee644a27af32bc8bbb65df53a0dddb673510715f51b0cd2513 |
| S&P 500 (cotejo) | fred_SP500.csv | `https://fred.stlouisfed.org/graph/fredgraph.csv?id=SP500` | 2016-10-17 a 2026-10-14 | c4aadc397af8eb9c4faf67aaac2eb5afcd84dc3984418d7ab420ddf66db7b7fc |
| Nasdaq Composite | fred_NASDAQCOM.csv | `https://fred.stlouisfed.org/graph/fredgraph.csv?id=NASDAQCOM` | 1971-02-05 a 2026-10-14 | 66eba78dcb17ea80adcb34a0d982d2fb862e03dbdf8eb807df860910e4c7ee3b |
| Nikkei 225 | fred_NIKKEI225.csv | `https://fred.stlouisfed.org/graph/fredgraph.csv?id=NIKKEI225` | 1949-05-16 a 2026-10-14 | f0206201d77068536cf67bc11bb3186795b5de0e85ef2bb118af011162201f72 |
| KOSPI | yahoo_KS11.json | igual que ^GSPC con `%5EKS11` | 1996-12-11 a 2026-10-14 | 611781853e3d03beef08ce8ca55ba5bca8e0da7e3c94dacf8ce2b406682301cf |

- Tamaño total de `datos/`: unos 4.0 MB, menos de 5 MB.
- **Limitaciones de fuente:** Stooq (`stooq.com` y `stooq.pl`) no respondió: el proxy cerró la conexión. FRED SP500 solo cubre 10 años. Por eso el S&P 500 y el KOSPI vienen de Yahoo, la misma fuente que A, aunque con un parser propio (fecha local = timestamp + gmtoffset). FRED SP500 sirve de cotejo: en 2,511 fechas comunes, la diferencia máxima de cierre es de 0.12% y los desplomes de 2016 en adelante coinciden en ambas fuentes (6 con −5% y 3 con −7%). Nasdaq y Nikkei sí vienen de una fuente distinta de A (FRED).
- **Diferencia esperada frente a A en el Nikkei:** la serie de FRED empieza en 1949, antes que ^N225 de Yahoo, que según sé empieza en 1965. B incluye 4 episodios previos a 1965 (1949-12-14, 1953-03-05, 1953-03-30 y 1959-12-21), y los cuatro tienen rendimiento de 11 días positivo.
- **Limpieza (§7):** se descartan los días sin cierre y los cierres repetidos exactos. Sin cierre: S&P 0, Nasdaq 487, Nikkei 980 y KOSPI 150 (en FRED son feriados en blanco). Cierres repetidos: S&P 313 (casi todos de 1928 a 1950), Nasdaq 13, Nikkei 93 y KOSPI 4.
- Corte al 2026-10-14. El 15-oct-2026 no entra. El desplome del KOSPI del 2026-10-13 queda fuera porque no tiene una ventana completa de 11 días.

## 2. Definiciones implementadas
- Desplome: r_t = C_t/C_{t−1} − 1 ≤ umbral. Rendimiento posterior: C_{t+h}/C_t − 1, con h en días hábiles de la serie limpia.
- Media incondicional: promedio de todos los rendimientos de h días del índice, con ventanas traslapadas.
- Episodio: un desplome se une al episodio del anterior (encadenado) si ocurre a menos de 11 días hábiles de él. Se usa 11 también para h = 22, como fija el §8.
- t por episodio: se promedia el exceso dentro de cada episodio y se calcula media/(sd/√n) sobre los episodios de los cuatro índices juntos.
- "Primer desplome": un evento por episodio, el primero.
- La frecuencia y el exceso medio de H1/H2 se calculan por evento, agrupando los cuatro índices.

## 3. Eventos y episodios (umbral −5%; con −7% entre paréntesis)
| Índice | Eventos | Episodios |
|---|---|---|
| S&P 500 | 87 (28) | 46 (18) |
| Nasdaq | 48 (16) | 21 (9) |
| Nikkei | 56 (15) | 36 (12) |
| KOSPI | 81 (24) | 45 (15) |
| Total | 272 (83) | 148 (54) |

## 4. Resultados agrupados

| Variante | Frec. positiva | Exceso medio (por evento) | t por episodio | 1er desplome: frec. / exceso / t | Veredicto §2 |
|---|---|---|---|---|---|
| **−5%, 11 d (principal)** | **64.0%** | **+2.35%** | **6.17** | 60.1% / +0.97% / 1.40 | **Replicado** |
| −5%, 22 d | 62.5% | +2.77% | 4.05 | 61.5% / +0.99% / 1.10 | Replicado |
| −7%, 11 d | 63.9% | +2.99% | 3.47 | 57.4% / +1.53% / 1.13 | Replicado |
| −7%, 22 d | 60.2% | +3.25% | 2.34 | 53.7% / +1.18% / 0.71 | Replicado |

Por índice, en la variante principal (frecuencia, exceso y t por episodio): S&P 60.9%, +1.48%, 3.16. Nasdaq 58.3%, +1.52%, 1.84. Nikkei 76.8%, +3.22%, 4.94. KOSPI 61.7%, +3.16%, 3.13. Las frecuencias positivas incondicionales de 11 días van de 56% a 60%.

## 5. Lectura y advertencias
- **Veredicto B, variante principal: Replicado** (H1: 64.0% > 55%; H2: exceso de +2.35% y t por episodio de 6.17 ≥ 1). Las 4 variantes cumplen §2.
- **Advertencia importante:** el efecto se concentra en los desplomes **posteriores** dentro de un episodio, es decir, ya avanzado el pánico. Si se toma solo el primer desplome de cada episodio, el exceso baja a cerca de +1%, la t queda entre 0.7 y 1.4 y la frecuencia queda entre 54% y 61%, apenas por encima de la incondicional (56% a 60%). En el S&P (t 0.12) y el Nasdaq (exceso −2.4% y t −1.32), el primer desplome no muestra rebote. Para una pregunta como P0126, en la que no se sabe si el desplome es el primero de una racha, la cifra relevante es la del primer desplome, y es mucho más débil.
- La t por episodio (6.17) supera la t ingenua por evento (4.04). La razón es que promediar dentro de los episodios largos (1929, 2008, KOSPI 2026) compensa caídas y rebotes y reduce la varianza. La media de las medias por episodio (+3.38%) también es mayor que la media por evento.
- Las ventanas de los desplomes de un mismo episodio se traslapan, de modo que la frecuencia por evento cuenta varias veces el mismo tramo de mercado.
- KOSPI y S&P vienen de Yahoo, la misma fuente que A. Para esos índices, la independencia está en el código, no en los datos.
