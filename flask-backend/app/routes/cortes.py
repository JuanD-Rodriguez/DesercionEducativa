# app/routes/cortes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.corte_evaluacion import CorteEvaluacion
from app.models.historial_academico import HistorialAcademico
from app.models.curso import Curso
from app.models.estudiante import Estudiante
from app.utils.decoradores import rol_requerido

cortes_bp = Blueprint('cortes', __name__)

@cortes_bp.route('/registrar', methods=['POST'])
@jwt_required()
@rol_requerido([1, 2])  # Admin o Gestor
def registrar_corte():
    """Registra un nuevo corte de evaluación para un estudiante en un curso"""
    try:
        data = request.get_json()
        id_estudiante = data.get('id_estudiante')
        id_curso = data.get('id_curso')
        numero_corte = data.get('numero_corte')
        calificacion = data.get('calificacion')
        asistencia = data.get('asistencia')
        
        if not id_estudiante or not id_curso or not numero_corte or calificacion is None or asistencia is None:
            return jsonify({"error": "Todos los campos son obligatorios"}), 400
        
        # Verificar que estudiante y curso existen
        estudiante = Estudiante.query.get(id_estudiante)
        curso = Curso.query.get(id_curso)
        
        if not estudiante:
            return jsonify({"error": "Estudiante no encontrado"}), 404
        if not curso:
            return jsonify({"error": "Curso no encontrado"}), 404
        
        # Buscar o crear el historial académico
        historial = HistorialAcademico.query.filter_by(
            id_estudiante=id_estudiante,
            id_curso=id_curso
        ).first()
        
        if not historial:
            historial = HistorialAcademico(
                id_estudiante=id_estudiante,
                id_curso=id_curso,
                calificacion_final=0  # Se actualizará después
            )
            db.session.add(historial)
            db.session.flush()
        
        # Verificar si ya existe un corte igual
        corte_existente = CorteEvaluacion.query.filter_by(
            id_historial=historial.id_historial,
            id_curso=id_curso,
            numero_corte=numero_corte
        ).first()
        
        if corte_existente:
            # Actualizar corte existente
            corte_existente.calificacion_corte = calificacion
            corte_existente.asistencia_corte = asistencia
        else:
            # Crear nuevo corte
            nuevo_corte = CorteEvaluacion(
                id_historial=historial.id_historial,
                id_curso=id_curso,
                numero_corte=numero_corte,
                calificacion_corte=calificacion,
                asistencia_corte=asistencia
            )
            db.session.add(nuevo_corte)
        
        # Calcular calificación final (promedio de los cortes)
        cortes = CorteEvaluacion.query.filter_by(id_historial=historial.id_historial).all()
        if cortes:
            total_calificacion = sum(float(c.calificacion_corte) for c in cortes)
            historial.calificacion_final = total_calificacion / len(cortes)
        
        # Actualizar promedio del estudiante
        historiales = HistorialAcademico.query.filter_by(id_estudiante=id_estudiante).all()
        if historiales:
            total_promedio = sum(float(h.calificacion_final) for h in historiales if h.calificacion_final is not None)
            estudiante.promedio = total_promedio / len(historiales)
        
        db.session.commit()
        
        return jsonify({
            "mensaje": "Corte de evaluación registrado exitosamente",
            "calificacion_final": float(historial.calificacion_final),
            "promedio_estudiante": float(estudiante.promedio)
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@cortes_bp.route('/estudiante/<int:id_estudiante>', methods=['GET'])
@jwt_required()
def obtener_cortes_estudiante(id_estudiante):
    """Obtiene los cortes de evaluación de un estudiante"""
    try:
        identidad = get_jwt_identity()
        # Verificar que sea el propio estudiante o un administrador/gestor
        if identidad["rol"] == 3 and identidad["id"] != id_estudiante:
            return jsonify({"error": "No autorizado"}), 403
        
        # Obtener historial académico con cortes
        historiales = db.session.query(
            HistorialAcademico,
            Curso
        ).join(
            Curso, HistorialAcademico.id_curso == Curso.id_curso
        ).filter(
            HistorialAcademico.id_estudiante == id_estudiante
        ).all()
        
        resultado = []
        
        for historial, curso in historiales:
            # Obtener cortes para este historial
            cortes = CorteEvaluacion.query.filter_by(id_historial=historial.id_historial).order_by(CorteEvaluacion.numero_corte).all()
            cortes_data = []
            
            for corte in cortes:
                cortes_data.append({
                    "numero_corte": corte.numero_corte,
                    "calificacion": float(corte.calificacion_corte),
                    "asistencia": float(corte.asistencia_corte)
                })
            
            resultado.append({
                "id_historial": historial.id_historial,
                "id_curso": curso.id_curso,
                "nombre_curso": curso.curso,
                "creditos": curso.creditos,
                "calificacion_final": float(historial.calificacion_final) if historial.calificacion_final else 0,
                "fecha_finalizacion": historial.fecha_finalizacion.strftime("%Y-%m-%d") if historial.fecha_finalizacion else None,
                "cortes": cortes_data
            })
        
        return jsonify(resultado), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cortes_bp.route('/curso/<int:id_curso>', methods=['GET'])
@jwt_required()
@rol_requerido([1, 2])  # Admin o Gestor
def obtener_cortes_curso(id_curso):
    """Obtiene los cortes de evaluación de todos los estudiantes en un curso"""
    try:
        # Verificar que el curso existe
        curso = Curso.query.get(id_curso)
        if not curso:
            return jsonify({"error": "Curso no encontrado"}), 404
        
        # Obtener historial académico con cortes para todos los estudiantes en este curso
        historiales = db.session.query(
            HistorialAcademico,
            Estudiante
        ).join(
            Estudiante, HistorialAcademico.id_estudiante == Estudiante.id_estudiante
        ).filter(
            HistorialAcademico.id_curso == id_curso
        ).all()
        
        resultado = []
        
        for historial, estudiante in historiales:
            # Obtener cortes para este historial
            cortes = CorteEvaluacion.query.filter_by(id_historial=historial.id_historial).order_by(CorteEvaluacion.numero_corte).all()
            cortes_data = []
            
            for corte in cortes:
                cortes_data.append({
                    "numero_corte": corte.numero_corte,
                    "calificacion": float(corte.calificacion_corte),
                    "asistencia": float(corte.asistencia_corte)
                })
            
            resultado.append({
                "id_historial": historial.id_historial,
                "id_estudiante": estudiante.id_estudiante,
                "nombre_estudiante": f"{estudiante.nombre} {estudiante.apellido}",
                "calificacion_final": float(historial.calificacion_final) if historial.calificacion_final else 0,
                "fecha_finalizacion": historial.fecha_finalizacion.strftime("%Y-%m-%d") if historial.fecha_finalizacion else None,
                "cortes": cortes_data
            })
        
        return jsonify({
            "curso": {
                "id_curso": curso.id_curso,
                "nombre": curso.curso,
                "creditos": curso.creditos
            },
            "estudiantes": resultado
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500