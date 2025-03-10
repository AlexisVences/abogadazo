import sqlite3

# Ruta de la base de datos
DB_PATH = "../data/raw/legal_database.sqlite"

def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabla de artículos legales (contenido principal sin los subapartados)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS articulos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fuente TEXT NOT NULL,   -- Ejemplo: "Reglamento de Tránsito", "Constitución", etc.
        numero TEXT,            -- Número del artículo (por ejemplo, "Artículo 1")
        contenido TEXT NOT NULL -- Texto principal del artículo (antes de subapartados)
    )
    ''')

    # Tabla de subapartados de los artículos (sub secciones identificadas por números romanos)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sub_articulos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        articulo_id INTEGER NOT NULL,
        numero TEXT,           -- Número en romano (por ejemplo, "I", "II", etc.)
        contenido TEXT NOT NULL,
        FOREIGN KEY (articulo_id) REFERENCES articulos(id)
    )
    ''')

    # Tabla de agentes facultados (para multas)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS agentes_facultados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        placa TEXT NOT NULL,
        nombre TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()
    print("Base de datos creada exitosamente.")

if __name__ == "__main__":
    create_database()
