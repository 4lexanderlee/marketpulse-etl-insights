from airflow import DAG 
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta 

# 1. ARGUMENTOS POR DEFECTO: Las reglas generales para todas las tareas
default_args = {
    'owner': 'data_engineering_team',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# 2. DEFINICIÓN DEL DAG: El "Contrato" de ejecución
with DAG(
    dag_id='marketpulse_medallion_pipeline',
    default_args=default_args,
    description='Pipeline Lakehouse (Bronce -> Plata -> Oro) para ETFs',
    schedule_interval='0 6 * * *',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['finance','gcp','lakehouse']
) as dag:
    
    # 3. DEFINICIÓN DE TAREAS (Los Operadores)
    # Tarea 1: Ejecutar el script de la Capa Bronce
    extract_bronze = BashOperator(
        task_id = 'extract_tiingo_to_gcs',
        bash_command = 'python /home/jovyan/work/src/extract/tiingo_client.py'
    )
    # Tarea 2: Ejecutar el script de PySpark de la Capa Plata
    transform_silver = BashOperator(
        task_id = 'transform_spark_to_parquet',
        bash_command = 'python /home/jovyan/work/src/transform/spark_processor.py'
    )
    # Tarea 3: Ejecutar el script de BigQuery de la Capa Oro
    load_gold = BashOperator(
        task_id = 'load_bigquery_native_tables',
        bash_command = 'python /home/jovyan/work/src/load/bigquery_loader.py'
    )
    # 4. LAS DEPENDENCIAS: El orden de la orquesta
    extract_bronze >> transform_silver >> load_gold