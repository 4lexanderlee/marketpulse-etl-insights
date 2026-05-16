import time
from src.extract.extract import download_market_data_stooq
from src.transform.transform import transform_raw_data

def run_pipeline():
    """
    Coordina la ejecución de todo el proceso ETL.
    """
    print("🚀 Inciando el Pipeline: MarketPulse-ETL-Insights")
    start_total = time.time()

    # Definir activos
    assets = ["VOO", "QQQ", "SCHD"]

    # PASO 1: Extracción (E)
    print("\n--- PASO 1: Extracción ---")
    try:
        download_market_data_stooq(assets)
    except Exception as e:
        print(f"❌ Error crítico en la extracción: {e}")
        return

    # PASO 2: Transformación (T)
    print("\n--- PASO 2: Transformación ---")
    try:
        transform_raw_data()
    except Exception as e:
        print(f"❌ Error crítico en la transformación: {e}")
        return

    end_total = time.time()
    duration = end_total - start_total
    
    print("\n" + "="*40)
    print(f"✅ Pipeline finalizado con éxito en {duration:.2f} segundos.")
    print(f"📁 Datos listos en: data/processed/")
    print("="*40)

if __name__ == "__main__":
    run_pipeline()