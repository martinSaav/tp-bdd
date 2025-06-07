import redis



# Conexión local por defecto (localhost:6379)
r = redis.Redis(host='localhost', port=6379, db=0)

# consultar datos de Redis
def get_redis_data(key):
    """Obtener datos de Redis por clave."""
    value = r.get(key)
    if value is not None:
        return value.decode('utf-8')  # Decodificar bytes a string
    return None

def get_redis_keys(pattern='*'):
    """Obtener todas las claves de Redis que coincidan con un patrón."""
    return r.keys(pattern)

def get_redis_all_data():
    """Obtener todos los datos almacenados en Redis."""
    keys = get_redis_keys()
    data = {}
    for key in keys:
        value = get_redis_data(key)
        if value is not None:
            data[key.decode('utf-8')] = value
    return data

# Ejemplo de uso
if __name__ == "__main__":
    # Obtener todos los datos de Redis
    all_data = get_redis_all_data()
    for key, value in all_data.items():
        print(f"{key}: {value}")
    
    # Obtener un valor específico
    edad_promedio = get_redis_data('edad_promedio')
    print(f"Edad promedio: {edad_promedio}")
