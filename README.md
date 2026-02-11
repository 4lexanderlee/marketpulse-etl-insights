# 📈 MarketPulse ETL & Insights

**MarketPulse ETL & Insights** es un pipeline de ingeniería de datos diseñado para automatizar la extracción, limpieza y análisis de activos financieros (ETFs como VOO, QQQ, SCHD). El proyecto transforma datos crudos de mercados bursátiles en información lista para la toma de decisiones de inversión.



## 🚀 Arquitectura del Proyecto

El proyecto sigue una estructura de capas para garantizar la integridad de los datos:

1.  **Capa Raw (Bronce):** Datos históricos extraídos directamente de Stooq en formato CSV.
2.  **Capa Processed (Plata):** Datos normalizados, con manejo de valores nulos y cálculo de retornos diarios.
3.  **Capa Insights (Oro):** (En desarrollo) Generación de métricas clave como volatilidad y correlación.

---

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python 3.x
* **Librerías principales:** * `Pandas`: Manipulación y transformación de datos.
    * `Pandas_datareader`: Conexión con APIs financieras.
    * `Pathlib`: Gestión de rutas de archivos entre sistemas operativos.
* **Fuente de Datos:** [Stooq](https://stooq.com/)

---

## 📁 Estructura de Carpetas

```text
marketpulse-etl-insights/
├── data/
│   ├── raw/           # CSVs originales (orden descendente, sin limpiar)
│   ├── processed/     # CSVs limpios (orden cronológico, con retornos)
│   └── outputs/       # Reportes y gráficos finales
├── src/
│   ├── extract.py     # Script de extracción robusta con reintentos
│   ├── transform.py   # Lógica de limpieza y feature engineering
│   └── main.py        # Orquestador del pipeline
├── requirements.txt   # Dependencias del proyecto
└── README.md          # Documentación

⚙️ Funcionamiento del Pipeline
1. Extracción (Extract)
El módulo extract.py se encarga de conectar con el servidor de Stooq.

Robustez: Implementa una lógica de hasta 3 reintentos en caso de fallo de red.

Mapeo: Traduce tickers comunes a la nomenclatura de Stooq (ej. VOO -> ^SPX).

Cortesía: Incluye pausas programadas para evitar bloqueos de IP.


2. Transformación (Transform)
El módulo transform.py procesa los archivos de la carpeta raw:

Ordenamiento: Invierte los datos para que sean cronológicos.

Limpieza: Aplica Forward Fill para completar huecos en días feriados.

Ingeniería de Datos: Calcula el daily_return (retorno diario) mediante la fórmula:

$$Retorno_t = \frac{Precio_t - Precio_{t-1}}{Precio_{t-1}}$$


3. Orquestación
El archivo main.py actúa como el cerebro del sistema, asegurando que la transformación solo ocurra si la extracción fue exitosa.

🚀 Cómo empezar
    - Clonar el repositorio:
    git clone [https://github.com/tu-usuario/marketpulse-etl-insights.git](https://github.com/tu-usuario/marketpulse-etl-insights.git)

    - Instalar dependencias:
    pip install -r requirements.txt

    - Ejecutar el pipeline:
    python src/main.py

📊 Próximos Pasos
[ ] Implementar un dashboard visual con Plotly o Streamlit.

[ ] Agregar cálculos de indicadores técnicos (RSI, Medias Móviles).

[ ] Automatizar la ejecución semanal mediante GitHub Actions.

Desarrollado por: Alexander Lee Melgarejo Romero

Propósito: Proyecto de Portafolio - Data Engineering