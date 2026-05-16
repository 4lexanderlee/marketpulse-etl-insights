import pandas_datareader.data as web 
import os
import time
from datetime import datetime
from pathlib import Path

def get_output_path():
    """Configura y retorna la ruta de la carpeta raw"""
    base_path = Path(__file__).resolve().parent.parent
    output_path = base_path / "data" / "raw"
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path

def validate_data(df):
    """Verifica si el DF contiene la información necesaria"""
    if df is None or df.empty:
        return False
    #Esta columnas deben estar si o si en el dataframe
    required_columns = ['Open', 'High', 'Low', 'Close']
    
    #El siguiente bloque se puede reducir a esto
    #return all(col in df.columns for col in required_columns)
    for col in required_columns:
        if col not in df.columns:
            return False
        
    return True

def download_market_data_stooq(tickers, max_retries=3):
    """Extrae datos de stooq, manejo de lógica de reintentos y validación"""
    output_path = get_output_path()
    start = datetime(2021, 1, 1)
    end = datetime.now()
    
    print(f"======== INICIANDO EXTRACCIÓN DE DATOS VÍA STOOQ ========")
    
    for ticker in tickers:
        success = False
        retries = 0
        
        #Mapeando al S&P 500 usando stooq
        search_ticker = '^SPX' if ticker in ['VOO', '^GSPC'] else ticker 
        
        while not success and retries < max_retries:
            try: 
                print(f"   Solicitando {ticker} (como {search_ticker}). Intento {retries + 1}... ")
                
                #Descarga de datos
                df = web.DataReader(search_ticker, 'stooq', start, end)
                
                if validate_data(df):
                    #Invertimos los datos de manera ascendente
                    df = df.sort_index()
                    
                    file_path = output_path / f"{ticker}_historico.csv"
                    df.to_csv(file_path)
                    
                    print(f"✅ ¡Éxito! {ticker} guardado en: {file_path}")
                    success = True
                else:
                    print(f"⚠️ Datos inválidos recibidos para {ticker}.")
                    retries += 1
            except Exception as e:
                retries += 1
                print(f"❌ Error al extraer {ticker}: {e}")
                if retries < max_retries:
                    print(f"Reintentando en 5 segundos...")
                    time.sleep(5)
            
            #Pausa entre ticker para simular comportamiento humano y que no bloqueen al IP
            time.sleep(3)
    print(f"======== EXTRACIÓN FINALIZADA ========")
    
if __name__ == '__main__':
    assets = ["VOO", "QQQ", "SCHD"]
    download_market_data_stooq(assets)