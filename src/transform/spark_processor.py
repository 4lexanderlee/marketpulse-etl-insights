import os
import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, lag, avg, round
from pyspark.sql.window import Window

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SparkProcesador:
    """
    Pipeline de Spark para transformación de la capa Bronce a Plata (Data analítica).
    Lee desde Google Cloud Storage, aplica transformaciones y guarda en GCS como Parquet.
    """
    def __init__(self, input_dir: str, output_dir: str, key_path: str):
        self.input_dir = input_dir
        self.output_dir = output_dir
        # Iniciar la sesión de spark configurada con el conector de GCS
        self.spark = SparkSession.builder \
            .appName('MarketPulse_SilverLayer') \
            .master('local[*]') \
            .config("spark.jars", "/home/jovyan/work/src/transform/gcs-connector-hadoop3-latest.jar") \
            .config("spark.hadoop.fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem") \
            .config("spark.hadoop.fs.AbstractFileSystem.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS") \
            .config("spark.hadoop.google.cloud.auth.service.account.enable", "true") \
            .config("spark.hadoop.google.cloud.auth.service.account.json.keyfile", key_path) \
            .getOrCreate()
        
        self.spark.sparkContext.setLogLevel("WARN")
            
    def process_data(self):
        logging.info("Inicializando el proceso de la capa Plata...")
        
        # Ingesta de todos los archivos CSV desde la capa bronce
        bronze_path = f"{self.input_dir}*_raw.csv"
        try:
            df_raw = self.spark.read.csv(bronze_path, header=True, inferSchema=True)
        except Exception as e:
            logging.error(f"Fallo leer los datos crudos: {e}")
            return
        
        # Proyección explicita y renombramiento de columnas
        df_clean = df_raw.select(
            to_date(col("date")).alias("fecha"),
            col("open").alias("precio_apertura"),
            col("high").alias("precio_maximo"),
            col("low").alias("precio_minimo"),
            col("close").alias("precio_cierre_bruto"),
            col("adjClose").alias("precio_cierre_ajustado"),
            col("volume").alias("volumen_operaciones"),
            col("Symbol").alias("ticker_etf")
        )
        
        # Especificaciones de la windows functions temporales
        window_spec = Window.partitionBy("ticker_etf").orderBy("fecha")
        window_50 = Window.partitionBy("ticker_etf").orderBy("fecha").rowsBetween(-49, Window.currentRow)
        window_200 = Window.partitionBy("ticker_etf").orderBy("fecha").rowsBetween(-199, Window.currentRow)
        
        # Ingenieria de características: Retornos diarios y medias moviles(MA50 y MA200)
        df_silver = df_clean \
            .withColumn("prev_close", lag(col("precio_cierre_ajustado"),1).over(window_spec)) \
            .withColumn("retorno_diario", round((col("precio_cierre_ajustado") - col("prev_close")) / col("prev_close"), 4)) \
            .withColumn("ma_50", round(avg(col("precio_cierre_ajustado")).over(window_50), 2)) \
            .withColumn("ma_200", round(avg(col("precio_cierre_ajustado")).over(window_200),2 )) \
            .drop("prev_close")
        
        # Persistir como archivos particionados
        try:
            df_silver.write.mode("overwrite") \
                .partitionBy("ticker_etf") \
                .parquet(self.output_dir)
            logging.info(f"La capa de plata se completo con exito en -> {self.output_dir}")
        except Exception as e:
            logging.error(f"Fallo al guardar como archivo Parquet: {e}")
    
    def stop(self):
        self.spark.stop()
        
if __name__ == "__main__":
    INPUT_DIR = "gs://marketpulse-bronze-ale/raw_data/"
    OUTPUT_DIR = "gs://marketpulse-silver-ale/processed_data/"
    KEY_PATH = "/home/jovyan/work/credentials/gcp-key.json"
    
    proceso = SparkProcesador(input_dir=INPUT_DIR, output_dir=OUTPUT_DIR, key_path=KEY_PATH)
    proceso.process_data()
    proceso.stop()