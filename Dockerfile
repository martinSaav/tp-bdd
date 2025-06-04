# Imagen base con Python y soporte gráfico
FROM python:3.11-slim

# Instala dependencias del sistema (incluye tcl/tk)
RUN apt-get update && apt-get install -y \
    python3-tk \
    libpq-dev \
    gcc \
    && apt-get clean

# Crea y define directorio de trabajo
WORKDIR /app

# Copia tus archivos al contenedor
COPY . /app

# Instala dependencias del proyecto (Pandas, Seaborn, Psycopg2, etc.)
RUN pip install --no-cache-dir -r requirements.txt

# Comando para ejecutar tu script
CMD ["python", "statistics_people.py"]
