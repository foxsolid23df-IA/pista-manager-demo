# 1. Usamos una imagen base de Python ligera (Linux)
FROM python:3.10-slim

# 2. Evita que Python guarde archivos caché .pyc y fuerza logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Directorio de trabajo dentro del contenedor
WORKDIR /code

# 4. Instalamos dependencias del sistema (necesarias para psycopg2)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 5. Copiamos los requisitos e instalamos
COPY requirements.txt /code/
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 6. Copiamos TODO el código del proyecto al contenedor
COPY . /code/

# 7. Comando para arrancar la app (Usamos host 0.0.0.0 para que sea visible desde fuera)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
