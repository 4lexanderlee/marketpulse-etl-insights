import os
import logging
from google.cloud import bigquery

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BigQueryLoader:
    """
    Módulo para crear Tablas Externas en BigQuery leyendo directamente desde los archivos de 
    la capa plata en Cloud Storage
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
    
    def create_external_table(self, table_name: str, gcs_uri: str, source_uri_prefix: str):
        """Crear la tabla externa apuntando a GCS y configurando particiones."""
        table_id = f"{self.dataset_id}.{table_name}"
        
        #1 -> Configurar la lectura externa de archivos Parquet
        external_config = bigquery.ExternalConfig("PARQUET")
        external_config.source_uris = [gcs_uri]
        external_config.autodetect = True # BigQuery lee el esquema de Parquet automáticamente
        
        #2 -> Configurar Hive Partitioning (por el partitionBy("ticker_etf") de la capa Plata)
        hive_partitioning = bigquery.HivePartitioningOptions()
        hive_partitioning.mode = "AUTO"
        hive_partitioning.source_uri_prefix = source_uri_prefix
        external_config.hive_partitioning = hive_partitioning
        
        #3 -> Definir la tabla y asignarle la configuración
        table = bigquery.Table(table_id)
        table.external_data_configuration = external_config
        
        #4 -> Eliminar si existe (para recrear la estructura) y crear tabla
        try: 
            self.client.delete_table(table_id, not_found_ok=True)
            table = self.client.create_table(table)
            logging.info(f"Tabla externa '{table_name}' creada con éxito en BigQuery.")
            logging.info(f"Apuntando a los datos en el Data Lake: {gcs_uri}")
        except Exception as e:
            logging.error(f"Fallo al crear la tabla externa: {e}")

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
    loader.create_external_table(table_name=TABLE_NAME, gcs_uri=GCS_URI, source_uri_prefix=GCS_PREFIX)