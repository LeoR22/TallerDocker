# Utiliza una imagen base con Python 3.11 y Uvicorn
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim

# Establece el directorio de trabajo en /app
#WORKDIR /app

# Copia los archivos locales al directorio /app en el contenedor
COPY . /app

# Instala las dependencias desde el archivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 80 (esto es más descriptivo, pero opcional ya que la imagen base ya lo hace)
EXPOSE 8000

# Define el comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
