import os
import logging
from google.cloud import bigquery

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BigQueryLoader:
    """
    Módulo para cargar fisicamente los datos desde GCS hacia las Tablas Nativas de BigQuery
    """
    def __init__(self, project_id: str, dataset_id: str, credentials_path: str):
        # Autenticación con GCP usando tu Service Account
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        self.client = bigquery.Client(project=project_id)
        self.project_id = project_id
        self.dataset_id = f"{project_id}.{dataset_id}"
    
    def create_dataset_if_not_exists(self, location="US"):
        """Crear el dataset (schema) en BigQuery si aún no existe."""
        dataset = bigquery.Dataset(self.dataset_id)
        dataset.location = location
        
        try:
            dataset = self.client.create_dataset(dataset, timeout=30)
            logging.info(f"Dataset creado exitosamente: {dataset.dataset_id}")
        except Exception as e:
            if "Already Exists" in str(e) or "409" in str(e):
                logging.info(f"El dataset '{self.dataset_id}' ya existe. Omitiendo creación.")
            else:
                logging.error(f"Error al crear el dataset: {e}")
    
    def load_native_table(self, table_name: str, gcs_uri: str, source_uri_prefix: str):
        """Cargar los datos físicamente desde GCS hacia una tabla nativa en BigQuery."""
        table_id = f"{self.dataset_id}.{table_name}"
        
        #1 -> Configurar el Trabajo de Carga (Load Job)
        job_config = bigquery.LoadJobConfig()
        job_config.source_format = bigquery.SourceFormat.PARQUET
        
        #2 -> Definir el comportamiento si la tabla ya existe
        job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
        
        #3 -> Configurar Hive Partitioning (reconoce las particiones de PySpark)
        hive_partitioning = bigquery.HivePartitioningOptions()
        hive_partitioning.mode = "AUTO"
        hive_partitioning.source_uri_prefix = source_uri_prefix
        job_config.hive_partitioning = hive_partitioning
        
        #4 -> Ejecutar la carga y esperar resultados
        try: 
            logging.info(f"Iniciando carga nativa desde {gcs_uri} hacia la tabla {table_name}...")
            #Iniciar el trabajp asincrono
            load_job = self.client.load_table_from_uri(
                gcs_uri, table_id, job_config=job_config
            )
            # Bloquear la ejecución hasta que BigQuery termine de procesar
            load_job.result()
            # Obtener metadatos de la tabla para confirmar la carga
            table = self.client.get_table(table_id)
            logging.info(f"Carga exitosa. La tabla nativa '{table_name}' ahora tiene {table.num_rows} filas.")
        except Exception as e:
            logging.error(f"Fallo al ejecutar el Load Job nativo: {e}")

if __name__ == "__main__":
    # ==== CONFIGURACIÓN =====
    PROJECT_ID = "marketpulse-etl-dev"
    DATASET_ID = "marketpulse_gold"
    TABLE_NAME = "etf_analytics"
    
    # Rutas de GCS
    GCS_PREFIX = "gs://marketpulse-silver-ale/processed_data/"
    GCS_URI = f"{GCS_PREFIX}*"
    
    KEY_PATH = "/home/jovyan/work/credentials/gcp-key.json"
    
    loader = BigQueryLoader(project_id=PROJECT_ID, dataset_id=DATASET_ID, credentials_path=KEY_PATH)
    loader.create_dataset_if_not_exists()
    loader.load_native_table(table_name=TABLE_NAME, gcs_uri=GCS_URI, source_uri_prefix=GCS_PREFIX)