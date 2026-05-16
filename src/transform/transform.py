"""
OBJETIVOS DE LA TRANSFORMACION
    - Estandarizar nombres: Pasar de 'Close' o 'Date' a minusculas y nombres consistentes
    - Manejo de nulos: Rellenar huecos de dias feriados
    -Cálculo de retornos: Agregar columna de cambio porcentual diario, que es la base de nuestro insigths
"""
import pandas as pd
from pathlib import Path

def transform_raw_data():
    base_path = Path(__file__).resolve().parent.parent
    raw_path = base_path / "data" / "raw"
    processed_path = base_path / "data" / "processed"
    processed_path.mkdir(parents=True, exist_ok=True)
    
    for file in raw_path.glob("*.csv"):
        ticker = file.stem.split('_')[0]
        df = pd.read_csv(file, index_col='Date', parse_dates=True)
        
        #1. Limpieza: Eliminar duplicados y ordenar
        df = df.drop_duplicates().sort_index()
        
        #2. Manejo de nulos: Forward fill (Usa el precio del día anterior)
        df = df.ffill()
        
        #3. Feature Engineering básico: Retornos diarios
        #$Retorno_t = \frac{Precio_t - Precio_{t-1}}{Precio_{t-1}}$
        df['daily_return'] = df['Close'].pct_change()
        
        #4. Estandarizar nombres de columnas a snake_case
        df.columns = [col.lower().replace(' ','_') for col in df.columns]
        
        #Guardar en la capa Processed
        output_file = processed_path / f"{ticker}_cleaned.csv"
        df.to_csv(output_file)
        print(f"✨ {ticker} transformado y guardado en processed/")

if __name__ == '__main__':
    transform_raw_data()