import pandas_datareader.data as web
import os
import time
from datetime import datetime
from pathlib import Path

def download_market_data_stooq(tickers):
    
    # Detectamos la raíz del proyecto (un nivel arriba de 'src')
    base_path = Path(__file__).resolve().parent.parent
    output_path = base_path / "data" / "raw"
    
    if not output_path.exists():
        output_path.mkdir(parents=True)
    
    # Definimos el rango de fechas
    start = datetime(2021, 1, 1)
    end = datetime.now()
    
    print(f"--- Iniciando extracción vía STOOQ  ---")
    
    for ticker in tickers:
        try:
            print(f"Solicitando {ticker} de Stooq...")
            
            # Stooq usa nombres ligeramente distintos para índices
            # Para el S&P 500 es '^SPX'
            search_ticker = '^SPX' if ticker == 'VOO' or ticker == '^GSPC' else ticker
            
            df = web.DataReader(search_ticker, 'stooq', start, end)
            
            if not df.empty:
                # Stooq devuelve los datos del más reciente al más antiguo, los invertimos
                df = df.sort_index()
                
                file_name = f"{output_path}/{ticker}_historical.csv"
                df.to_csv(file_name)
                print(f"✅ ¡Éxito! {ticker} guardado en {file_name}")
            
            # Pausa de cortesía
            time.sleep(3)
            
        except Exception as e:
            print(f"❌ Error con {ticker}: {e}")

if __name__ == "__main__":
    # Usaremos los nombres de tus ETFs elegidos
    assets = ["VOO", "QQQ", "SCHD"]
    download_market_data_stooq(assets)