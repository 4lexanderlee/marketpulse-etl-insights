# 📈 MarketPulse ETL & Insights: Lakehouse Architecture on GCP

Un pipeline de ingeniería de datos *End-to-End* diseñado para la extracción, procesamiento distribuido y análisis de ETFs estratégicos (SPY, VOO, QQQ). Este proyecto implementa una **Arquitectura Medallón** orientada a la nube, priorizando la escalabilidad, la orquestación automatizada y la optimización de costos (FinOps).

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Apache Spark](https://img.shields.io/badge/PySpark-Data_Processing-orange.svg)](https://spark.apache.org/)
[![Airflow](https://img.shields.io/badge/Apache_Airflow-Orchestration-007A33.svg)](https://airflow.apache.org/)
[![GCP](https://img.shields.io/badge/Google_Cloud-GCS_%7C_BigQuery-4285F4.svg)](https://cloud.google.com/)
[![Power BI](https://img.shields.io/badge/Power_BI-Data_Viz-F2C811.svg)](https://powerbi.microsoft.com/)

---

## 🏗️ Arquitectura del Sistema (Data Lakehouse)

El sistema sigue el paradigma Medallón para garantizar la calidad progresiva del dato:

1. **Capa Bronce (Ingesta Raw):** Extracción automatizada de datos financieros globales desde la API de Tiingo mediante Python. Los datos crudos aterrizan en un Data Lake en Google Cloud Storage (GCS).
2. **Capa Plata (Transformación):** Procesamiento distribuido utilizando **PySpark**. Se realiza la limpieza de datos, el tipado de esquemas y el cálculo de hechos derivados financieros (Medias Móviles de 50 y 200 días, retornos diarios y detección de anomalías). Los datos se guardan en formato `Parquet` particionado por Ticker para optimizar la lectura.
3. **Capa Oro (Serving):** Ingesta física automatizada hacia **Google BigQuery** mediante *Load Jobs* nativos (`WRITE_TRUNCATE`). Esta decisión arquitectónica elimina la latencia de las tablas externas, garantizando tiempos de consulta en milisegundos para la herramienta de BI.

## 🚀 Tecnologías Clave y Buenas Prácticas

* **Orquestación:** `Apache Airflow` contenedorizado para la gestión de dependencias, reintentos y programación de flujos de trabajo (*DAGs*).
* **Infraestructura como Código (IoC):** Entorno de desarrollo 100% reproducible mediante `Docker` y `docker-compose`.
* **FinOps:** Minimización de costos de escaneo en BigQuery al utilizar tablas nativas particionadas e Import Mode en la capa de visualización.
* **Control de Versiones y Modularidad:** Código estructurado bajo principios SOLID en la carpeta `src/`, separando responsabilidades de extracción, transformación y carga.

## 📊 Dashboard y Visualización Financiera

El producto final es un tablero analítico construido en **Power BI**, el cual se conecta directamente a la Capa Oro en BigQuery. 

**Características del Tablero:**
* Inteligencia de tiempo implementada con DAX (Tabla Calendario).
* Visualización de "Cruces Dorados" y volatilidad diaria de los ETFs.
* Controles de segmentación dinámica para un análisis profundo de rangos de fechas específicos.

👉 *[Haz clic aquí para ver el PDF exportado del Dashboard interactivo](./docs/MarketPulse_Dashboard.pdf)*

## ⚙️ Cómo ejecutar este proyecto localmente

1. Clona este repositorio.
2. Configura tus credenciales de Google Cloud (`gcp-key.json`) en la carpeta `credentials/` y tu API Key de Tiingo en un archivo `.env`.
3. Levanta la infraestructura con Docker:
   ```bash
   docker-compose up -d
   
4. Inicializa la base de datos de metadatos de Airflow y arranca el planificador y el servidor web en el puerto 8080.

5. Accede a Airflow, activa el DAG marketpulse_etl y monitorea la ejecución del pipeline en tiempo real.

