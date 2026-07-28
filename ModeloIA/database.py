import psycopg2
from psycopg2 import Error
from psycopg2.extras import DictCursor
import csv
from datetime import date, timedelta

# Configuración de la base de datos PostgreSQL para Neon.tech
DB_CONFIG = {
    'host': 'ep-fancy-term-a8kbdvwm-pooler.eastus2.azure.neon.tech',
    'dbname': 'neondb',
    'user': 'neondb_owner',
    'password': 'npg_h8McrZw6PHoY',
    'sslmode': 'require'
}

def get_connection():
    """Establece conexión con la base de datos PostgreSQL"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error al conectar a PostgreSQL: {e}")
        return None

def submit_agents(route):
    conn = get_connection()
    if conn is None:
        return None

    cursor = conn.cursor()
    total = 0
    insertados = 0
    duplicados = 0
    try:
        with open(route, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            for row in csv_reader:
                total += 1
                placa = row['placa']
                nombre = row['nombre_completo']
                
                cursor.execute("SELECT id FROM agentes_facultados WHERE placa = %s", (placa,))
                if cursor.fetchone() is None:
                    cursor.execute(
                        "INSERT INTO agentes_facultados (placa, nombre) VALUES (%s, %s)",
                        (placa, nombre)
                    )
                    insertados += 1
                else:
                    duplicados += 1
                
                if total % 100 == 0:
                    conn.commit()
            
            conn.commit()
                
            print(f"\nResumen de carga:")
            print(f"Total de registros en CSV: {total}")
            print(f"Registros insertados: {insertados}")
            print(f"Registros duplicados (no insertados): {duplicados}")
            
    except Error as e:
        print(f"Error al conectar o insertar en PostgreSQL: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
        print("Conexión a PostgreSQL cerrada")

def agent_by_platenumber(placa):
    conn = get_connection()
    if conn is None:
        return None
        
    cursor = conn.cursor(cursor_factory=DictCursor)
    
    try:
        cursor.execute("SELECT id, placa, nombre FROM agentes_facultados WHERE placa = %s", (placa,))    
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

def register_agent_search(id_usuario, id_agente, fecha):
    conn = get_connection()
    if conn is None:
        return False
        
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO consulta_agentes (fecha, id_usuario, id_agente) VALUES (%s, %s, %s)",
            (fecha, id_usuario, id_agente))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al registrar consulta de agente: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def register_consultation(id_usuario, fecha, texto):
    conn = get_connection()
    if conn is None:
        return None
        
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO consulta (fecha, texto, id_usuario) VALUES (%s, %s, %s) RETURNING id",
            (fecha, texto, id_usuario))
        inserted_id = cursor.fetchone()[0]
        conn.commit()
        return inserted_id
    except Error as e:
        print(f"Error al registrar consulta: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def register_response(id_consulta, texto, tipo):
    conn = get_connection()
    if conn is None:
        return None
        
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO respuesta (texto, tipo, id_consulta) VALUES (%s, %s, %s) RETURNING id",
            (texto, tipo, id_consulta))
        inserted_id = cursor.fetchone()[0]
        conn.commit()
        return inserted_id
    except Error as e:
        print(f"Error al registrar respuesta: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def register_feedback(id_respuesta, estrellas):
    conn = get_connection()
    if conn is None:
        return False
        
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id FROM retroalimentacion WHERE id_respuesta = %s",
            (id_respuesta,))
        existing_feedback = cursor.fetchone()
        
        if existing_feedback:
            cursor.execute(
                "UPDATE retroalimentacion SET estrellas = %s WHERE id_respuesta = %s",
                (estrellas, id_respuesta))
        else:
            cursor.execute(
                "INSERT INTO retroalimentacion (estrellas, id_respuesta) VALUES (%s, %s)",
                (estrellas, id_respuesta))
        
        conn.commit()
        return True
    except Error as e:
        print(f"Error al registrar/actualizar retroalimentación: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def get_consultation_by_user(id_usuario):
    conn = get_connection()
    if conn is None:
        return None
        
    cursor = conn.cursor(cursor_factory=DictCursor)
    try:
        cursor.execute(
            "SELECT id, fecha, texto FROM consulta WHERE id_usuario = %s ORDER BY fecha DESC",
            (id_usuario,))
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener consultas: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_responses_for_consultation(id_consulta):
    conn = get_connection()
    if conn is None:
        return None
        
    cursor = conn.cursor(cursor_factory=DictCursor)
    try:
        cursor.execute(
            "SELECT id, texto, tipo FROM respuesta WHERE id_consulta = %s ORDER BY id",
            (id_consulta,))
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener respuestas: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_feedback_for_response(id_respuesta):
    conn = get_connection()
    if conn is None:
        return None
        
    cursor = conn.cursor(cursor_factory=DictCursor)
    try:
        cursor.execute(
            "SELECT id, estrellas, comentarios FROM retroalimentacion WHERE id_respuesta = %s",
            (id_respuesta,))
        return cursor.fetchone()
    except Error as e:
        print(f"Error al obtener retroalimentación: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

# Funciones de administración
def get_consultas_por_fecha(fecha: date) -> int:
    conn = get_connection()
    if conn is None:
        return 0
        
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM consulta WHERE fecha = %s", (fecha,))
        return cursor.fetchone()[0]
    except Error as e:
        print(f"Error al obtener consultas por fecha: {e}")
        return 0
    finally:
        cursor.close()
        conn.close()

def get_consultas_por_rango_fechas(inicio: date, fin: date) -> list:
    conn = get_connection()
    if conn is None:
        return []
        
    cursor = conn.cursor(cursor_factory=DictCursor)
    try:
        cursor.execute(
            """SELECT fecha, COUNT(*) as consultas 
               FROM consulta 
               WHERE fecha BETWEEN %s AND %s
               GROUP BY fecha
               ORDER BY fecha""",
            (inicio, fin))
        
        resultados = cursor.fetchall()
        delta = fin - inicio
        consultas_por_dia = {}
        
        for i in range(delta.days + 1):
            dia = inicio + timedelta(days=i)
            consultas_por_dia[dia.day] = 0
        
        for fila in resultados:
            dia = fila['fecha'].day
            consultas_por_dia[dia] = fila['consultas']
        
        return [{'dia': dia, 'consultas': count} for dia, count in consultas_por_dia.items()]
    except Error as e:
        print(f"Error al obtener consultas por rango: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_consultas_agentes_por_rango_fechas(inicio: date, fin: date) -> list:
    conn = get_connection()
    if conn is None:
        return []
        
    cursor = conn.cursor(cursor_factory=DictCursor)
    try:
        cursor.execute(
            """SELECT fecha, COUNT(*) as consultas 
               FROM consulta_agentes 
               WHERE fecha BETWEEN %s AND %s
               GROUP BY fecha
               ORDER BY fecha""",
            (inicio, fin))
        
        resultados = cursor.fetchall()
        delta = fin - inicio
        consultas_por_dia = {}
        
        for i in range(delta.days + 1):
            dia = inicio + timedelta(days=i)
            consultas_por_dia[dia.day] = 0
        
        for fila in resultados:
            dia = fila['fecha'].day
            consultas_por_dia[dia] = fila['consultas']
        
        return [{'dia': dia, 'consultas': count} for dia, count in consultas_por_dia.items()]
    except Error as e:
        print(f"Error al obtener consultas por rango: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_tipos_consulta() -> list:
    conn = get_connection()
    if conn is None:
        return []
        
    cursor = conn.cursor(cursor_factory=DictCursor)
    try:
        cursor.execute(
            """SELECT r.tipo as name, COUNT(*) as value 
               FROM respuesta r
               JOIN consulta c ON r.id_consulta = c.id
               WHERE c.fecha BETWEEN CURRENT_DATE - INTERVAL '30 days' AND CURRENT_DATE
               GROUP BY r.tipo
               ORDER BY value DESC""")
        
        resultados = cursor.fetchall()
        mapeo_tipos = {
            'multas': 'Multas',
            'procedimientos': 'Procedimientos',
            'reglamentacion': 'Reglamentación',
            'general': 'Otras'
        }
        
        return [{
            'name': mapeo_tipos.get(row['name'], row['name']),
            'value': row['value']
        } for row in resultados]
    except Error as e:
        print(f"Error al obtener tipos de consulta: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_estadisticas_feedback() -> dict:
    conn = get_connection()
    if conn is None:
        return {}
        
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT AVG(estrellas) FROM retroalimentacion")
        promedio = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT COUNT(*) FROM retroalimentacion")
        total = cursor.fetchone()[0]
        
        hoy = date.today()
        primer_dia_mes_actual = hoy.replace(day=1)
        primer_dia_mes_pasado = (primer_dia_mes_actual - timedelta(days=1)).replace(day=1)
        ultimo_dia_mes_pasado = primer_dia_mes_actual - timedelta(days=1)
        
        cursor.execute(
            "SELECT COUNT(*) FROM consulta WHERE fecha BETWEEN %s AND %s",
            (primer_dia_mes_actual, hoy))
        consultas_mes_actual = cursor.fetchone()[0]
        
        cursor.execute(
            "SELECT COUNT(*) FROM consulta WHERE fecha BETWEEN %s AND %s",
            (primer_dia_mes_pasado, ultimo_dia_mes_pasado))
        consultas_mes_pasado = cursor.fetchone()[0] or 1
        
        crecimiento = ((consultas_mes_actual - consultas_mes_pasado) / consultas_mes_pasado) * 100
        
        return {
            'promedio_feedback': round(float(promedio), 1),
            'total_feedbacks': total,
            'crecimiento_mensual': round(crecimiento, 1)
        }
    except Error as e:
        print(f"Error al obtener estadísticas de feedback: {e}")
        return {}
    finally:
        cursor.close()
        conn.close()

#submit_agents('./agentes_procesados.csv')