# Usa la imagen oficial de Python para tu versión
FROM python:3.12

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de requerimientos al contenedor
COPY requirements.txt /app/

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de tu aplicación al contenedor
COPY . /app/

# Expón el puerto en el que tu aplicación se ejecutará
EXPOSE 8000

# Comando para ejecutar tu aplicación cuando se inicie el contenedor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
