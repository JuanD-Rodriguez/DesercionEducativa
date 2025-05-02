from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.utils.decoradores import rol_requerido
from app.models.desercion import Desercion
from app.models.estudiante import Estudiante
from app.models.ingenieria import Ingenieria
from app.models.riesgo_socioeconomico import RiesgoSocioeconomico
from app.models.respuesta import Respuesta
from app.models.pregunta import Pregunta
from sqlalchemy import func, desc
from app import db

reportes_bp = Blueprint('reportes', __name__)

@reportes_bp.route('/desercion', methods=['GET'])
@jwt_required()
@rol_requerido([1, 2])  # Admin o Gestor
def obtener_reportes_desercion():
    """Obtiene los reportes de deserción de todos los estudiantes"""
    try:
        datos = db.session.query(
            Desercion,
            Estudiante
        ).join(
            Estudiante, Desercion.id_estudiante == Estudiante.id_estudiante
        ).all()
        
        resultado = []
        for desercion, estudiante in datos:
            resultado.append({
                "id_desercion": desercion.id_desercion,
                "id_estudiante": desercion.id_estudiante,
                "nombre_estudiante": f"{estudiante.nombre} {estudiante.apellido}",
                "riesgo_desercion": float(desercion.riesgo_desercion),
                "factores_riesgo": desercion.factores_riesgo,
                "fecha_analisis": desercion.fecha_analisis.strftime("%Y-%m-%d") if desercion.fecha_analisis else None
            })
        
        return jsonify(resultado), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@reportes_bp.route('/desercion/alto_riesgo', methods=['GET'])
@jwt_required()
@rol_requerido([1, 2])  # Admin o Gestor
def obtener_estudiantes_alto_riesgo():
    """Obtiene los estudiantes con alto riesgo de deserción"""
    try:
        umbral = request.args.get('umbral', 0.7, type=float)
        
        datos = db.session.query(
            Desercion,
            Estudiante,
            Ingenieria
        ).join(
            Estudiante, Desercion.id_estudiante == Estudiante.id_estudiante
        ).join(
            Ingenieria, Estudiante.id_ingenieria == Ingenieria.id_ingenieria
        ).filter(
            Desercion.riesgo_desercion >= umbral
        ).order_by(
            desc(Desercion.riesgo_desercion)
        ).all()
        
        resultado = []
        for desercion, estudiante, ingenieria in datos:
            resultado.append({
                "id_estudiante": desercion.id_estudiante,
                "nombre_estudiante": f"{estudiante.nombre} {estudiante.apellido}",
                "ingenieria": ingenieria.nombre_ingenieria,
                "riesgo_desercion": float(desercion.riesgo_desercion),
                "factores_riesgo": desercion.factores_riesgo,
                "fecha_analisis": desercion.fecha_analisis.strftime("%Y-%m-%d") if desercion.fecha_analisis else None
            })
        
        return jsonify(resultado), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@reportes_bp.route('/desercion/por_ingenieria', methods=['GET'])
@jwt_required()
@rol_requerido([1, 2])  # Admin o Gestor
def obtener_desercion_por_ingenieria():
    """Obtiene estadísticas de deserción agrupadas por carrera de ingeniería"""
    try:
        datos = db.session.query(
            Ingenieria.id_ingenieria,
            Ingenieria.nombre_ingenieria,
            func.count(Estudiante.id_estudiante).label('total_estudiantes'),
            func.avg(Desercion.riesgo_desercion).label('riesgo_promedio'),
            func.count(func.case([(Desercion.riesgo_desercion > 0.7, 1)])).label('alto_riesgo')
        ).join(
            Estudiante, Ingenieria.id_ingenieria == Estudiante.id_ingenieria
        ).join(
            Desercion, Estudiante.id_estudiante == Desercion.id_estudiante
        ).group_by(
            Ingenieria.id_ingenieria,
            Ingenieria.nombre_ingenieria
        ).all()
        
        resultado = []
        for id_ingenieria, nombre, total, riesgo_promedio, alto_riesgo in datos:
            resultado.append({
                "id_ingenieria": id_ingenieria,
                "nombre_ingenieria": nombre,
                "total_estudiantes": total,
                "riesgo_promedio": float(riesgo_promedio) if riesgo_promedio is not None else 0,
                "estudiantes_alto_riesgo": alto_riesgo,
                "porcentaje_alto_riesgo": round((alto_riesgo / total) * 100, 2) if total > 0 else 0
            })
        
        return jsonify(resultado), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@reportes_bp.route('/factores_desercion', methods=['GET'])
@jwt_required()
@rol_requerido([1, 2])  # Admin o Gestor
def obtener_factores_desercion():
    """Analiza y agrupa los factores comunes de deserción"""
    try:
        # Este es un enfoque simplificado. En la práctica, necesitarías un análisis más sofisticado
        # de los textos en factores_riesgo para identificar correctamente todos los factores comunes
        factores_comunes = [
            "Bajo promedio académico",
            "Bajo rendimiento en cursos recientes",
            "Baja asistencia a clases",
            "Situación económica vulnerable",
            "Sin apoyo de becas"
        ]
        
        resultados = {}
        for factor in factores_comunes:
            # Contar cuántas veces aparece cada factor
            count = Desercion.query.filter(
                Desercion.factores_riesgo.like(f"%{factor}%")
            ).count()
            resultados[factor] = count
        
        # Convertir a formato de lista para la respuesta
        resultado_final = []
        for factor, count in resultados.items():
            resultado_final.append({
                "factor": factor,
                "cantidad": count
            })
        
        # Ordenar por cantidad descendente
        resultado_final.sort(key=lambda x: x["cantidad"], reverse=True)
        
        return jsonify(resultado_final), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@reportes_bp.route('/respuestas_analisis', methods=['GET'])
@jwt_required()
@rol_requerido([1, 2])  # Admin o Gestor
def analisis_respuestas():
    """Analiza las respuestas de los formularios para identificar patrones"""
    try:
        # Agrupar respuestas por pregunta y opción seleccionada
        datos = db.session.query(
            Pregunta.id_pregunta,
            Pregunta.texto_pregunta,
            Pregunta.categoria,
            Respuesta.opcion_seleccionada,
            func.count(Respuesta.id_respuesta).label('cantidad')
        ).join(
            Pregunta, Respuesta.id_pregunta == Pregunta.id_pregunta
        ).group_by(
            Pregunta.id_pregunta,
            Pregunta.texto_pregunta,
            Pregunta.categoria,
            Respuesta.opcion_seleccionada
        ).order_by(
            Pregunta.id_pregunta,
            desc('cantidad')
        ).all()
        
        # Organizar resultados por pregunta
        preguntas = {}
        for id_pregunta, texto, categoria, opcion, cantidad in datos:
            if id_pregunta not in preguntas:
                preguntas[id_pregunta] = {
                    "id_pregunta": id_pregunta,
                    "texto_pregunta": texto,
                    "categoria": categoria,
                    "opciones": []
                }
            
            preguntas[id_pregunta]["opciones"].append({
                "opcion": opcion,
                "cantidad": cantidad
            })
        
        return jsonify(list(preguntas.values())), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@reportes_bp.route('/estadisticas_generales', methods=['GET'])
@jwt_required()
@rol_requerido([1, 2])  # Admin o Gestor
def estadisticas_generales():
    """Proporciona estadísticas generales del sistema"""
    try:
        # Total de estudiantes
        total_estudiantes = Estudiante.query.count()
        
        # Total con predicciones
        total_con_prediccion = Desercion.query.count()
        
        # Estudiantes en riesgo (>70%)
        alto_riesgo = Desercion.query.filter(Desercion.riesgo_desercion > 0.7).count()
        
        # Riesgo promedio
        riesgo_promedio_query = db.session.query(func.avg(Desercion.riesgo_desercion)).first()
        riesgo_promedio = float(riesgo_promedio_query[0]) if riesgo_promedio_query[0] is not None else 0
        
        # Total de respuestas a formularios
        total_respuestas = Respuesta.query.count()
        
        return jsonify({
            "total_estudiantes": total_estudiantes,
            "estudiantes_con_prediccion": total_con_prediccion,
            "estudiantes_alto_riesgo": alto_riesgo,
            "porcentaje_alto_riesgo": round((alto_riesgo / total_con_prediccion) * 100, 2) if total_con_prediccion > 0 else 0,
            "riesgo_promedio": round(riesgo_promedio, 4),
            "total_respuestas_formularios": total_respuestas
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500