#Importamos las librerias necesarias para hacer la extracción
import yfinance as yf 
import os 
import time
import requests
from datetime import datetime 

def download_market_data(tickers, fecha_ini, fecha_fi):
    """
    Descarga datos históricos de Yahoo Finance y los guarda en CSV.
    """
    #PASO 1 - Crearé la ruta al direcctorio si no existe
    ruta_fi = './data/raw'
    if not os.path.exists(ruta_fi):
        os.makedirs(ruta_fi)
    
    # --- CONFIGURACIÓN DE SEGURIDAD ---
    # Esto hace que Yahoo crea que eres un navegador Chrome en Windows
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    session = requests.Session()
    session.headers.update(headers)
    
    print(f"--- Iniciando extracción de: {','.join(tickers)} ---")
    
    #Iteramos cada elemento de la lista tickers
    for ticker in tickers:
        try:
            print(f"  DESCARGANDO TICKER ========> {ticker}... ")
            
            #Obtuvimos un obstaculo RATE Limiting, limite de peticiones, por esa razon opté por poner un temporizador
            time.sleep(2)
            
            #PASO 2 - Usare yfinance para bajar los datos
            #auto_adjust=True - ajusta precios por splits y dividendos automáticamente
            data = yf.download(ticker, start=fecha_ini, end=fecha_fi, auto_adjust=True, session=session, threads=False)
            
            if not data.empty:
                #PASO 3 - Guardar los datos extraidos en la ruta_fi
                file_n = f"{ruta_fi}/{ticker}_historico.csv"
                data.to_csv(file_n)
                print(f"✅ ¡Éxito! Guardado: {file_n}")
            else:
                print(f"⚠️ Yahoo respondió pero no envió datos para {ticker}")
        except Exception as e:
            print(f" XXX Error al descargar {ticker}: {e}")

#Punto de entrada al Script
if __name__ == "__main__":
    #Activos de la lista a descargar
    activos = ["^GSPC", "QQQ","SCHD"]
    #Fijamos la fecha_ini
    inicio = "2021-01-01"
    #Obtenemos la fecha actual
    hoy = datetime.now().strftime('%Y-%m-%d')
    
    download_market_data(activos, inicio, hoy)
                
        