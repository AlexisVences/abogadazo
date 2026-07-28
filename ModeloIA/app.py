from flask import Flask, request, jsonify
from flask_cors import CORS 
from model import AsistenteLegal
from datetime import datetime, timedelta
import database

import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {
    "origins": ["https://gentle-sfogliatella-08f198.netlify.app"],
    "allow_headers": ["Content-Type", "Authorization", "ngrok-skip-browser-warning"],
    "methods": ["GET", "POST", "OPTIONS"],
    "supports_credentials": True
}})



legal_ai = AsistenteLegal()


@app.route("/")
def home():
    return "Hola desde ngrok en Flask"


# ==============================================
# RUTAS RELACIONADAS CON AGENTES
# ==============================================

@app.route('/api/agentes/consulta', methods=['GET'])
def consulta_agente():
    # Obtener y validar el parámetro de la placa
    id_usuario = request.args.get('id', '') # El front debe enviar el id de usuario tambien
    placa = request.args.get('placa', '').strip().upper()
    
    if not placa:
        return jsonify({
            'error': 'Número de placa requerido',
            'status_code': 400
        }), 400
    if not id_usuario:
        return jsonify({
            'error': 'Usuario no válido',
            'status_code': 400
        }), 400
    
    try:
        # Consultar la base de datos
        agente = database.agent_by_platenumber(placa)
        print(agente)
        if not agente:
            return jsonify({
                'error': f'Agente con placa {placa} no encontrado',
                'suggestions': [],
                'status_code': 404
            }), 404
        
        fecha_consulta = datetime.now().date()  # Obtenemos la fecha actual
        registro_exitoso = database.register_agent_search(
            id_usuario=int(id_usuario),
            id_agente=agente['id'],
            fecha=fecha_consulta
        )

        if not registro_exitoso:
            app.logger.warning(f"No se pudo registrar la consulta del agente {placa} por usuario {id_usuario}")
        
        return jsonify({
            'success': True,
            'agente': agente,
            'status_code': 200
        })
        
    except Exception as e:
        # Capturar errores de base de datos
        app.logger.error(f"Error en consulta_agente: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor al consultar agente',
            'details': str(e),
            'status_code': 500
        }), 500

# ==============================================
# RUTAS RELACIONADAS CON EL CHAT LEGAL (IA)
# ==============================================

@app.route('/api/chat-legal/feedback', methods=['POST'])
def agregar_feedback():
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        required_fields = ['userId', 'respuesta', 'rating']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Campo {field} es requerido',
                    'status_code': 400
                }), 400
        
        # Validar que el rating sea un número entre 1 y 5
        rating = data['rating']
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            return jsonify({
                'error': 'El rating debe ser un número entero entre 1 y 5',
                'status_code': 400
            }), 400
        
        # Registrar el feedback en la base de datos
        success = database.register_feedback(
            id_respuesta=data['respuesta'],
            estrellas=rating
        )
        
        if not success:
            app.logger.error("No se pudo registrar el feedback en la base de datos")
            return jsonify({
                'error': 'Error al registrar el feedback',
                'status_code': 500
            }), 500
        
        return jsonify({
            'success': True,
            'message': 'Feedback registrado exitosamente',
            'status_code': 201
        }), 201
        
    except Exception as e:
        app.logger.error(f"Error en agregar_feedback: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor al procesar el feedback',
            'details': str(e),
            'status_code': 500
        }), 500

@app.route('/api/chat-legal/consulta', methods=['POST'])
def consulta_legal():
    data = request.get_json()
    id_usuario = data.get('id_usuario')  # El front debe enviar el id de usuario tambien
    pregunta = data.get('pregunta', '').strip()
    
    if not pregunta:
        return jsonify({'error': 'La pregunta es requerida'}), 400
    
    try:
       # Consulta al asistente legal
        resultado = legal_ai.consultar(pregunta)

        # Registrar la consulta en la base de datos
        fecha_actual = datetime.now().date()
        consulta_id = database.register_consultation(
            id_usuario=int(id_usuario),
            fecha=fecha_actual,
            texto=pregunta
        )
        if not consulta_id:
            app.logger.error("No se pudo registrar la consulta en la base de datos")

        # Registrar la respuesta en la base de datos
        if consulta_id and "respuesta" in resultado:
            respuesta_id = database.register_response(
                texto=resultado["respuesta"],
                tipo=resultado.get("categoria", "general"),  # Usamos la categoría como tipo
                id_consulta=consulta_id
            )
            
            if not respuesta_id:
                app.logger.error("No se pudo registrar la respuesta en la base de datos")

        
        return jsonify({
            'success': True,
            'respuesta': resultado["respuesta"],
            'fuentes': resultado["fuentes"],
            'id_respuesta': respuesta_id if 'respuesta_id' in locals() else None
        })
    except Exception as e:
        return jsonify({
            'error': 'Error al procesar la consulta',
            'details': str(e)
        }), 500



#
# Obtener administrador (provisional)
#
@app.route('/api/admin/stats/daily', methods=['GET'])
def get_daily_stats():
    try:
        # Obtener estadísticas del día actual
        fecha_hoy = datetime.now().date()
        consultas_hoy = database.get_consultas_por_fecha(fecha_hoy)
        
        return jsonify({
            'success': True,
            'consultas_hoy': consultas_hoy,
            'status_code': 200
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Error al obtener estadísticas diarias',
            'details': str(e),
            'status_code': 500
        }), 500

@app.route('/api/admin/stats/monthly', methods=['GET'])
def get_monthly_stats():
    try:
        # Obtener estadísticas del mes actual
        hoy = datetime.now()
        primer_dia_mes = hoy.replace(day=1)
        ultimo_dia_mes = (hoy.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
        
        consultas_mes = database.get_consultas_por_rango_fechas(primer_dia_mes, ultimo_dia_mes)
        
        return jsonify({
            'success': True,
            'consultas_mes': consultas_mes,
            'status_code': 200
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Error al obtener estadísticas mensuales',
            'details': str(e),
            'status_code': 500
        }), 500
        
# estadisticas agentes
@app.route('/api/admin/stats/monthlyagents', methods=['GET'])
def get_monthly_stats_agents():
    try:
        # Obtener estadísticas del mes actual
        hoy = datetime.now()
        primer_dia_mes = hoy.replace(day=1)
        ultimo_dia_mes = (hoy.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
        
        consultas_mes = database.get_consultas_agentes_por_rango_fechas(primer_dia_mes, ultimo_dia_mes)
        
        return jsonify({
            'success': True,
            'consultas_mes': consultas_mes,
            'status_code': 200
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Error al obtener estadísticas mensuales',
            'details': str(e),
            'status_code': 500
        }), 500

@app.route('/api/admin/stats/types', methods=['GET'])
def get_consultation_types():
    try:
        tipos_consulta = database.get_tipos_consulta()
        
        return jsonify({
            'success': True,
            'tipos_consulta': tipos_consulta,
            'status_code': 200
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Error al obtener tipos de consulta',
            'details': str(e),
            'status_code': 500
        }), 500

@app.route('/api/admin/stats/feedback', methods=['GET'])
def get_feedback_stats():
    try:
        feedback_stats = database.get_estadisticas_feedback()
        return jsonify({
            'success': True,
            'feedback_stats': feedback_stats,
            'status_code': 200
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Error al obtener estadísticas de feedback',
            'details': str(e),
            'status_code': 500
        }), 500

# ==============================================
# RUTAS ADICIONALES
# ==============================================

@app.route('/api/status', methods=['GET'])
def status_check():
    """Ruta para verificar que el servidor está funcionando"""
    return jsonify({
        'status': 'active',
        'services': {
            'agentes': True,
            'chat-legal': True
        }
    })


#Inicio de la aplicacion
if __name__ == '__main__':
    app.run()