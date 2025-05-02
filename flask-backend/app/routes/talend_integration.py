# app/routes/talend_integration.py
from flask import Blueprint, jsonify, request
from app import db
from app.models.usuario import Usuario
from app.models.estudiante import Estudiante
from app.models.historial_academico import HistorialAcademico
from app.models.corte_evaluacion import CorteEvaluacion
from app.models.curso import Curso
from app.models.riesgo_socioeconomico import RiesgoSocioeconomico
from sqlalchemy import desc
import datetime

talend_bp = Blueprint('talend', __name__)

@talend_bp.route('/api/schema', methods=['GET'])
def get_schema():
    """Devuelve el esquema de la base de datos para integración con Talend"""
    tables = {
        "usuario": ["id_usuario", "nombre_usuario", "id_rol"],
        "estudiante": ["id_estudiante", "id_usuario", "nombre", "apellido", "correo_electronico", "id_ingenieria", "promedio", "fecha_registro"],
        "curso": ["id_curso", "curso", "creditos"],
        "historial_academico": ["id_historial", "id_estudiante", "id_curso", "calificacion_final", "fecha_finalizacion"],
        "corte_evaluacion": ["id_corte", "id_historial", "id_curso", "numero_corte", "calificacion_corte", "asistencia_corte"],
        "riesgo_socioeconomico": ["id_riesgo", "id_estudiante", "nivel_ingreso", "situacion_vivienda", "dependencia_economica", "acceso_becas"],
        "desercion": ["id_desercion", "id_estudiante", "id_riesgo", "id_formulario", "riesgo_desercion", "factores_riesgo", "fecha_analisis"]
    }
    
    return jsonify({
        "schema": tables,
        "status": "success"
    }), 200

@talend_bp.route('/api/test', methods=['GET'])
def test_connection():
    """Prueba la conexión a la base de datos desde Talend"""
    try:
        # Intenta hacer una consulta simple
        estudiantes_count = Estudiante.query.count()
        cursos_count = Curso.query.count()
        cortes_count = CorteEvaluacion.query.count()
        
        return jsonify({
            "status": "success",
            "message": "Conexión a la base de datos exitosa",
            "counts": {
                "estudiantes": estudiantes_count,
                "cursos": cursos_count,
                "cortes": cortes_count
            }
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error de conexión: {str(e)}"
        }), 500

@talend_bp.route('/api/estudiantes', methods=['GET'])
def get_estudiantes():
    """Obtiene datos de estudiantes para Talend"""
    try:
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        estudiantes = Estudiante.query.limit(limit).offset(offset).all()
        
        result = []
        for e in estudiantes:
            result.append({
                "id_estudiante": e.id_estudiante,
                "nombre": e.nombre,
                "apellido": e.apellido,
                "correo_electronico": e.correo_electronico,
                "id_ingenieria": e.id_ingenieria,
                "promedio": float(e.promedio) if e.promedio else 0.0,
                "fecha_registro": e.fecha_registro.isoformat() if e.fecha_registro else None
            })
        
        return jsonify({
            "data": result,
            "count": len(result),
            "status": "success"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@talend_bp.route('/api/deserciones', methods=['GET'])
def get_deserciones():
    """Obtiene datos de deserción para Talend"""
    try:
        from app.models.desercion import Desercion
        
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        deserciones = Desercion.query.limit(limit).offset(offset).all()
        
        result = []
        for d in deserciones:
            result.append({
                "id_desercion": d.id_desercion,
                "id_estudiante": d.id_estudiante,
                "riesgo_desercion": float(d.riesgo_desercion) if d.riesgo_desercion else 0.0,
                "factores_riesgo": d.factores_riesgo,
                "fecha_analisis": d.fecha_analisis.isoformat() if d.fecha_analisis else None
            })
        
        return jsonify({
            "data": result,
            "count": len(result),
            "status": "success"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@talend_bp.route('/api/historiales', methods=['GET'])
def get_historiales():
    """Obtiene historiales académicos para Talend"""
    try:
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        historiales = HistorialAcademico.query.limit(limit).offset(offset).all()
        
        result = []
        for h in historiales:
            result.append({
                "id_historial": h.id_historial,
                "id_estudiante": h.id_estudiante,
                "id_curso": h.id_curso,
                "calificacion_final": float(h.calificacion_final) if h.calificacion_final else 0.0,
                "fecha_finalizacion": h.fecha_finalizacion.isoformat() if h.fecha_finalizacion else None
            })
        
        return jsonify({
            "data": result,
            "count": len(result),
            "status": "success"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500