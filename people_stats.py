import psycopg2
from datetime import datetime
from collections import Counter
import os
from dotenv import load_dotenv
import redis

load_dotenv()


# Conexión local por defecto (localhost:6379)
r = redis.Redis(host='localhost', port=6379, db=0)

# Conexión a la base de datos
conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)
cur = conn.cursor()

# Obtener todos los datos necesarios
cur.execute("""
    SELECT p.nombre, p.apellido, p.genero, p.fecha_nacimiento, pa.nombre
    FROM Personas p
    JOIN paises pa ON p.pais_id = pa.id
""")
rows = cur.fetchall()

# Cerrar conexión
cur.close()
conn.close()

# Procesar datos
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

# 1. Edad promedio de todas las personas
edad_promedio = sum(p['edad'] for p in data) / len(data)
print(f"1. Edad promedio: {edad_promedio:.2f}")

# Guardar datos en Redis
r.set('edad_promedio', edad_promedio)

# 2. Cant. personas por género
generos = Counter(p['genero'] for p in data)
print("2. Cantidad de personas por género:", generos)

# Guardar conteo de géneros en Redis
for genero, cantidad in generos.items():
    r.hset('conteo_generos', genero, cantidad)

# 3. Cant. personas por país
personas_por_pais = Counter(p['pais'] for p in data)
print("3. Cantidad de personas por país:", personas_por_pais)

# Guardar conteo de países en Redis
for pais, cantidad in personas_por_pais.items():
    r.hset('conteo_paises', pais, cantidad)

# 4. Género más frecuente por país
genero_por_pais = {}
for p in data:
    genero_por_pais.setdefault(p['pais'], []).append(p['genero'])

genero_mas_frecuente_por_pais = {
    pais: Counter(generos).most_common(1)[0][0]
    for pais, generos in genero_por_pais.items()
}
print("4. Género más frecuente por país:", genero_mas_frecuente_por_pais)

# Guardar género más frecuente por país en Redis
for pais, genero in genero_mas_frecuente_por_pais.items():
    r.hset('genero_mas_frecuente_por_pais', pais, genero)

# 5. Persona más joven y más vieja
persona_mas_joven = min(data, key=lambda p: p['fecha_nacimiento'])
persona_mas_vieja = max(data, key=lambda p: p['fecha_nacimiento'])

print(f"5. Persona más joven: {persona_mas_joven['nombre']} {persona_mas_joven['apellido']}, Fecha nacimiento: {persona_mas_joven['fecha_nacimiento']}")
print(f"   Persona más vieja: {persona_mas_vieja['nombre']} {persona_mas_vieja['apellido']}, Fecha nacimiento: {persona_mas_vieja['fecha_nacimiento']}")

# Guardar personas más joven y más vieja en Redis
r.hset('persona_mas_joven', 'nombre', persona_mas_joven['nombre'])
r.hset('persona_mas_joven', 'apellido', persona_mas_joven['apellido'])
r.hset('persona_mas_joven', 'fecha_nacimiento', persona_mas_joven['fecha_nacimiento'].isoformat())
r.hset('persona_mas_vieja', 'nombre', persona_mas_vieja['nombre'])
r.hset('persona_mas_vieja', 'apellido', persona_mas_vieja['apellido'])
r.hset('persona_mas_vieja', 'fecha_nacimiento', persona_mas_vieja['fecha_nacimiento'].isoformat())

# 6. Edad promedio por país
edades_por_pais = {}
for p in data:
    edades_por_pais.setdefault(p['pais'], []).append(p['edad'])

edad_prom_por_pais = {
    pais: sum(edades) / len(edades)
    for pais, edades in edades_por_pais.items()
}
print("6. Edad promedio por país:")
for pais, promedio in edad_prom_por_pais.items():
    print(f"   {pais}: {promedio:.2f}")

# Guardar edad promedio por país en Redis
for pais, promedio in edad_prom_por_pais.items():
    r.hset('edad_promedio_por_pais', pais, promedio)

# 7. Top 3 países con más personas
top3_paises = personas_por_pais.most_common(3)
print("7. Top 3 países con más personas:", top3_paises)

# Guardar top 3 países en Redis
for pais, cantidad in top3_paises:
    r.hset('top3_paises', pais, cantidad)
