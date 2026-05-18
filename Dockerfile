# Usamos la imagen oficial de Jupyter con PySpark preconfigurado
FROM jupyter/pyspark-notebook:spark-3.5.0

# Cambiamos a root temporalmente para instalar dependencias
USER root

# Copiamos el archivo de requerimientos
COPY requirements.txt /tmp/

# Instalamos las librerías de Python
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Volvemos al usuario estándar por seguridad
USER $NB_UID