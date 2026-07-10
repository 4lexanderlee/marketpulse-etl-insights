# MarketPulse: ETL & Insights Financieros 🚀

MarketPulse es un pipeline de ingeniería de datos *end-to-end* diseñado bajo una arquitectura **Lakehouse (Medallion Architecture)** en la nube. El objetivo principal es automatizar la ingesta, limpieza, transformación avanzada y exposición analítica de datos de mercado correspondientes a ETFs de crecimiento estratégico a largo plazo (`SPY`, `VOO`, `QQQ`).

Originalmente concebido como un entorno puramente local, el proyecto ha migrado hacia un ecosistema **Cloud-Native en Google Cloud Platform (GCP)** enfocado en la eficiencia, escalabilidad y control de costos (FinOps).

---

## 🏗️ Arquitectura del Sistema

El flujo de datos sigue los principios de la arquitectura de medallas, ejecutándose de forma híbrida e integrada:

[ API Tiingo ]
│
▼ (Extracción - Pandas + gcsfs)
┌────────────────────────────────────────────────────────┐
│ Capa Bronce (Raw Data)                                 │
│ - Bucket GCS: gs://marketpulse-bronze-ale/             │
│ - Formato: CSV crudo por ETF                           │
└────────────────────────────────────────────────────────┘
│
▼ (Procesamiento Distribuido - PySpark + Uber JAR)
┌────────────────────────────────────────────────────────┐
│ Capa Plata (Enriched / Conformed)                     │
│ - Bucket GCS: gs://marketpulse-silver-ale/             │
│ - Formato: Parquet altamente comprimido                │
│ - Particionado por: ticker_etf                         │
└────────────────────────────────────────────────────────┘
### Componentes Clave:
1. **Ingesta (Capa Bronce):** Cliente en Python (`requests`) que extrae el historial financiero desde la API de **Tiingo**. Utiliza la librería `gcsfs` para transmitir los DataFrames de Pandas de forma directa hacia Google Cloud Storage sin persistir residuos en el almacenamiento local.
2. **Procesamiento (Capa Plata):** Motor de cálculo distribuido optimizado con **PySpark**. Lee el almacenamiento de objetos en la nube, procesa ventanas temporales y genera métricas analíticas avanzadas.
3. **Almacenamiento e Infraestructura local:** Entorno contenedorizado mediante **Docker**, aislando los procesos de desarrollo y mapeando volúmenes seguros para las credenciales de GCP (Service Accounts).

---

## 📈 Ingeniería de Características (Capa Plata)

Durante la fase de transformación en PySpark, los datos analíticos se enriquecen calculando indicadores financieros clave mediante funciones de ventana (`Window.partitionBy`):
* **Retornos Diarios:** Fluctuación porcentual del precio de cierre ajustado de un día para otro.
* **Medias Móviles (MA50 y MA200):** Indicadores de tendencia de mercado calculados sobre ventanas históricas móviles de 50 y 200 días.

---

## 🛠️ Stack Tecnológico

* **Lenguaje Principal:** Python 3.11
* **Procesamiento de Datos:** PySpark (Apache Spark 3.5), Pandas
* **Infraestructura Cloud:** Google Cloud Storage (GCS)
* **Contenedores y Entornos:** Docker / Docker Compose & JupyterLab
* **Conectores de Infraestructura:** Hadoop GCS Connector (Fat JAR)

---

## 🚀 Próximos Pasos (Roadmap del Proyecto)

- [x] **Fase 1 (Bronze):** Ingesta automatizada directa a la nube (GCS).
- [x] **Fase 2 (Silver):** Procesamiento analítico distribuido con PySpark y almacenamiento eficiente en Parquet particionado.
- [x] **Fase 3 (Gold):** Creación de tablas y vistas analíticas optimizadas en **Google BigQuery** conectadas al Data Lake de forma directa.
- [x] **Fase 4 (Orquestación):** Construcción de DAGs funcionales en **Apache Airflow (Cloud Composer)** para automatizar el ciclo completo del pipeline.
- [ ] **Fase 5 (Visualización):** Construcción de un cuadro de mando financiero dinámico utilizando **Looker Studio**.