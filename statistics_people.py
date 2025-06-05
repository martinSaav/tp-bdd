# 📌 Celdas del notebook
# 1️⃣ - Imports
import psycopg2
from datetime import datetime
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de gráficos
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 5)

# 2️⃣ - Conexión y carga de datos
conn = psycopg2.connect(
    host='ep-lucky-bird-a5jc5s8y-pooler.us-east-2.aws.neon.tech',
    database='neondb',
    user='neondb_owner',
    password='75ijuoyJAwRG'
)
cur = conn.cursor()

cur.execute("""
    SELECT p.nombre, p.apellido, p.genero, p.fecha_nacimiento, pa.nombre
    FROM Personas p
    JOIN paises pa ON p.pais_id = pa.id
""")
rows = cur.fetchall()
cur.close()
conn.close()

# 3️⃣ - Procesamiento de datos
today = datetime.today()
data = []
for nombre, apellido, genero, fecha_nac, pais in rows:
    edad = today.year - fecha_nac.year - ((today.month, today.day) < (fecha_nac.month, fecha_nac.day))
    data.append({
        'nombre': nombre,
        'apellido': apellido,
        'genero': genero.lower(),
        'fecha_nacimiento': fecha_nac,
        'edad': edad,
        'pais': pais
    })

df = pd.DataFrame(data)

# 4️⃣ - Estadísticas
print("Edad promedio:", df['edad'].mean())
print("Cantidad por género:\n", df['genero'].value_counts())
print("Cantidad por país:\n", df['pais'].value_counts())

# Persona más joven y más vieja
joven = df.sort_values('fecha_nacimiento').iloc[0]
viejo = df.sort_values('fecha_nacimiento').iloc[-1]
print("Persona más joven:", joven['nombre'], joven['apellido'], joven['fecha_nacimiento'])
print("Persona más vieja:", viejo['nombre'], viejo['apellido'], viejo['fecha_nacimiento'])

# Género más frecuente por país
genero_por_pais = df.groupby('pais')['genero'].agg(lambda x: x.value_counts().idxmax())
print("Género más frecuente por país:\n", genero_por_pais)

# Edad promedio por país
edad_prom_pais = df.groupby('pais')['edad'].mean().sort_values(ascending=False)

# 5️⃣ - Gráficos

# Personas por género
sns.countplot(data=df, x='genero', hue='genero', palette='pastel', legend=False)
plt.title("Cantidad de personas por género")
plt.xlabel("Género")
plt.ylabel("Cantidad")
plt.show()

# Personas por país
sns.countplot(data=df, y='pais', hue='pais', order=df['pais'].value_counts().index, palette='viridis', legend=False)
plt.title("Cantidad de personas por país")
plt.xlabel("Cantidad")
plt.ylabel("País")
plt.show()

# Edad promedio por país
edad_prom_pais.plot(kind='barh', color='skyblue')
plt.title("Edad promedio por país")
plt.xlabel("Edad promedio")
plt.ylabel("País")
plt.show()

# Top 3 países con más personas
top3 = df['pais'].value_counts().head(3)
top3.plot(kind='bar', color='orange')
plt.title("Top 3 países con más personas")
plt.ylabel("Cantidad")
plt.show()
