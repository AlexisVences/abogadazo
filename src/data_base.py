import sqlite3

# Ruta de la base de datos
DB_PATH = "../data/raw/legal_database.sqlite"

def agent_by_platenumber(placa):
    # Conectar a la base de datos
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Consulta para buscar un agente por número de placa
    cursor.execute("SELECT id, placa, nombre FROM agentes_facultados WHERE placa = ?", (placa,))
    agent = cursor.fetchone()

    # Si encontramos un agente con esa placa
    if agent:
        agent_id, agent_placa, agent_name = agent
        print(f"Agente encontrado:")
        print(f"ID: {agent_id}")
        print(f"Placa: {agent_placa}")
        print(f"Nombre: {agent_name}")
    else:
        print(f"No se encontró un agente facultado con la placa: '{placa}'")

    # Cerrar la conexión
    conn.close()

def search_by_keyword(keyword):
    # Conectar a la base de datos
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Buscar en la tabla de artículos
    cursor.execute("SELECT id, fuente, numero, contenido FROM articulos WHERE contenido LIKE ?", ('%' + keyword + '%',))
    article = cursor.fetchone()

    # Si encontramos un artículo que contiene la palabra clave
    if article:
        article_id, fuente, numero, contenido = article
        print(f"Fuente: {fuente}")
        print(f"Número del artículo: {numero}")
        print(f"Contenido del artículo: {contenido}")
        print("=" * 50)
        # Ahora buscamos subartículos relacionados con este artículo
        cursor.execute("SELECT numero, contenido FROM sub_articulos WHERE articulo_id = ? AND contenido LIKE ?", (article_id, '%' + keyword + '%'))
        sub_article = cursor.fetchone()
        if sub_article:
            sub_num, sub_content = sub_article
            print(f"  Subartículo {sub_num}: {sub_content}")
        else:
            print("  No se encontraron subartículos que coincidan con la palabra clave.")
        conn.close()
        return  # Detener la búsqueda después de la primera coincidencia

    # Si no encontramos coincidencias en artículos, buscamos en los subartículos de todos los artículos
    cursor.execute("SELECT a.id, a.fuente, a.numero, a.contenido, sa.numero, sa.contenido FROM articulos a "
                   "JOIN sub_articulos sa ON a.id = sa.articulo_id "
                   "WHERE sa.contenido LIKE ?", ('%' + keyword + '%',))
    sub_article = cursor.fetchone()

    # Si encontramos un subartículo que contiene la palabra clave
    if sub_article:
        article_id, fuente, numero, article_content, sub_num, sub_content = sub_article
        print(f"Fuente: {fuente}")
        print(f"Número del artículo: {numero}")
        print(f"Contenido del artículo: {article_content}")
        print("=" * 50)
        print(f"  Subartículo {sub_num}: {sub_content}")
        conn.close()
        return  # Detener la búsqueda después de la primera coincidencia

    print(f"No se encontraron artículos o subartículos que contengan la palabra clave: '{keyword}'")
    conn.close()

def print_all_agents():
    # Conectar a la base de datos
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Consulta para obtener todos los agentes facultados
    cursor.execute("SELECT id, placa, nombre FROM agentes_facultados")
    agents = cursor.fetchall()

    # Verificamos si hay agentes registrados
    if agents:
        print(f"Total de agentes facultados encontrados: {len(agents)}\n")
        for agent in agents:
            agent_id, agent_placa, agent_name = agent
            print(f"ID: {agent_id} | Placa: {agent_placa} | Nombre: {agent_name}")
    else:
        print("No se encontraron agentes facultados en la base de datos.")

    # Cerrar la conexión
    conn.close()

def print_articles():
    # Conectar a la base de datos
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Consultar todos los artículos
    cursor.execute("SELECT id, fuente, numero, contenido FROM articulos")
    articles = cursor.fetchall()

    for article in articles:
        article_id, fuente, numero, contenido = article
        print(f"Fuente: {fuente}")
        print(f"Número del artículo: {numero}")
        print(f"Contenido: {contenido}")
        print("-" * 50)
    
    # Cerrar la conexión
    conn.close()

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
