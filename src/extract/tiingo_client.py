import os
import logging
import pandas as pd
import requests 
from datetime import datetime, timedelta
from dotenv import load_dotenv

#Configuración de logs para controlar el ETL
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#Cargar las variables de entorno desde el archivo
load_dotenv()
class TiingoExtractor:
    """
    Clase para extraer los datos financieros desde la API 
    """
    def __init__(self, tickers, year_back, output_dir):
        self.tickers = tickers
        self.end_date = datetime.now().strftime("%Y-%m-%d")
        self.start_date = (datetime.now() - timedelta(days=year_back * 365)).strftime("%Y-%m-%d")
        self.output_dir = output_dir 
        #API KEY ALMACENADA EN .env
        self.api_key = os.getenv("TIINGO_API_KEY")
        if not self.api_key:
            raise ValueError("ERRO CRITICO -> No se encontró la variable TIINGO_API_KEY en .env")
        
    def fetch_data(self):
        """Descarga los datos y los guarda en el Data Lake local"""
        os.makedirs(self.output_dir, exist_ok=True)
        
        for ticker in self.tickers:
            logging.info(f"Extrayendo datos para {ticker} desde Tiingo API...")
            
            #Construimos la URL del endpoint de Tiingo 
            URL = f"https://api.tiingo.com/tiingo/daily/{ticker}/prices"
            # Configuramos los parámetros requeridos por la API y las credenciales de autorización
            headers = {
                'Content-Type':'application/json',
                'Authorization': f'Token {self.api_key}'
            }
            params = {
                'startDate': self.start_date,
                'endDate': self.end_date
            }
            
            try:
                # Realizamos la petición HTTP GET de forma directa y limpia
                response = requests.get(URL, headers=headers, params=params)
                # Si la API responde con un error (ej. token inválido), esto lanzará una excepción
                response.raise_for_status()
                # Transformamos la respuesta JSON estructurada en un DataFrame de Pandas
                data = response.json()
                if not data:
                    logging.warning(f"No se devolvieron datos para {ticker}.")
                    continue
                
                df = pd.DataFrame(data)
                # Agregamos la columna de identificación del activo
                df['Symbol'] = ticker
                # Guardamos como CSV 
                file_path = os.path.join(self.output_dir, f"{ticker}_raw.csv")
                df.to_csv(file_path, index=False)
                
                logging.info(f"Éxito: {len(df)} registros de {ticker} guardado en {file_path}")
            except Exception as e:
                logging.error(f"Falló del pipeline al procesar {ticker}. Detalle {e}")

if __name__ == "__main__":
    target_etfs = ['SPY', 'VOO', 'QQQ']
    year_back = 5
    output_dir = "/home/jovyan/work/data/01_bronze_raw"
    
    extractor = TiingoExtractor(tickers=target_etfs, year_back=year_back, output_dir=output_dir)
    extractor.fetch_data()