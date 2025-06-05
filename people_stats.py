import psycopg2
from datetime import datetime
from collections import Counter

# Conexión a la base de datos
conn = psycopg2.connect(
    host='ep-lucky-bird-a5jc5s8y-pooler.us-east-2.aws.neon.tech',
    database='neondb',
    user='neondb_owner',
    password='75ijuoyJAwRG'
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

# 2. Cant. personas por género
generos = Counter(p['genero'] for p in data)
print("2. Cantidad de personas por género:", generos)

# 3. Cant. personas por país
personas_por_pais = Counter(p['pais'] for p in data)
print("3. Cantidad de personas por país:", personas_por_pais)

# 4. Género más frecuente por país
genero_por_pais = {}
for p in data:
    genero_por_pais.setdefault(p['pais'], []).append(p['genero'])

genero_mas_frecuente_por_pais = {
    pais: Counter(generos).most_common(1)[0][0]
    for pais, generos in genero_por_pais.items()
}
print("4. Género más frecuente por país:", genero_mas_frecuente_por_pais)

# 5. Persona más joven y más vieja
persona_mas_joven = min(data, key=lambda p: p['fecha_nacimiento'])
persona_mas_vieja = max(data, key=lambda p: p['fecha_nacimiento'])

print(f"5. Persona más joven: {persona_mas_joven['nombre']} {persona_mas_joven['apellido']}, Fecha nacimiento: {persona_mas_joven['fecha_nacimiento']}")
print(f"   Persona más vieja: {persona_mas_vieja['nombre']} {persona_mas_vieja['apellido']}, Fecha nacimiento: {persona_mas_vieja['fecha_nacimiento']}")

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

# 7. Top 3 países con más personas
top3_paises = personas_por_pais.most_common(3)
print("7. Top 3 países con más personas:", top3_paises)
