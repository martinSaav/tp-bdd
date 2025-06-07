# Trabajo Práctico de Base de Datos: Estadísticas de Personas con PostgreSQL y Redis

Este proyecto en Python se conecta a una base de datos **PostgreSQL** para obtener información sobre personas y sus países, calcula estadísticas relevantes, y guarda los resultados en una instancia de **Redis**.

## ¿Qué hace el script?

Procesa datos de personas (nombre, apellido, género, fecha de nacimiento, país) y calcula:

1. Edad promedio general.
2. Cantidad de personas por género.
3. Cantidad de personas por país.
4. Género más frecuente por país.
5. Persona más joven y más vieja.
6. Edad promedio por país.
7. Top 3 países con más personas.

Todos estos resultados se guardan en **Redis** para consultas rápidas posteriores.

---

## Requisitos

- Python 3.8 o superior
- PostgreSQL con las tablas `Personas` y `Paises` (local o remoto)
- Redis (local o remoto)
- Archivo `.env` con las credenciales

## Dependencias

Instalalar con pip

```bash
pip install -r requirements.txt
```
## Estructura de la Base de Datos

La base de datos fue creada con el siguiente script SQL:

```sql
CREATE TABLE paises (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

CREATE TABLE personas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50),
    apellido VARCHAR(50),
    genero VARCHAR(20), -- masculino, femenino, otro
    fecha_nacimiento DATE,
    pais_id INTEGER NOT NULL,
    FOREIGN KEY (pais_id) REFERENCES paises(id)
);
```

## Configuración del Entorno

Para conectar con PostgreSQL y Redis, crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```plaintext
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=tu_base_de_datos
POSTGRES_USER=tu_usuario
POSTGRES_PASSWORD=tu_contraseña

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```
## Ejecución

Para ejecutar el script, simplemente corre:

```bash
python3 people_stats.py 
```

## Resultados almacenados en Redis
- edad_promedio: float

- conteo_generos: hash (genero → cantidad)

- conteo_paises: hash (país → cantidad)

- genero_mas_frecuente_por_pais: hash (país → género)

- persona_mas_joven, persona_mas_vieja: hashes con nombre, apellido, fecha

- edad_promedio_por_pais: hash (país → edad promedio)

- top3_paises: hash (país → cantidad)

## Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

