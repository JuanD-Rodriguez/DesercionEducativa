# app/routes/cursos.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.curso import Curso
from app.utils.decoradores import rol_requerido

cursos_bp = Blueprint('cursos', __name__)

@cursos_bp.route('/', methods=['GET'])
@jwt_required()
def obtener_cursos():
    """Obtiene la lista de todos los cursos"""
    try:
        cursos = Curso.query.all()
        resultado = []
        
        for curso in cursos:
            resultado.append({
                "id_curso": curso.id_curso,
                "nombre": curso.curso,
                "creditos": curso.creditos
            })
        
        return jsonify(resultado), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cursos_bp.route('/<int:id_curso>', methods=['GET'])
@jwt_required()
def obtener_curso(id_curso):
    """Obtiene detalles de un curso específico"""
    try:
        curso = Curso.query.get(id_curso)
        
        if not curso:
            return jsonify({"error": "Curso no encontrado"}), 404
        
        return jsonify({
            "id_curso": curso.id_curso,
            "nombre": curso.curso,
            "creditos": curso.creditos
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cursos_bp.route('/', methods=['POST'])
@jwt_required()
@rol_requerido([1, 2])  # Admin o Gestor
def crear_curso():
    """Crea un nuevo curso"""
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        creditos = data.get('creditos')
        
        if not nombre or creditos is None:
            return jsonify({"error": "Nombre y créditos son obligatorios"}), 400
        
        # Verificar si ya existe un curso con el mismo nombre
        curso_existente = Curso.query.filter_by(curso=nombre).first()
        if curso_existente:
            return jsonify({"error": "Ya existe un curso con ese nombre"}), 409
        
        nuevo_curso = Curso(
            curso=nombre,
            creditos=creditos
        )
        
        db.session.add(nuevo_curso)
        db.session.commit()
        
        return jsonify({
            "mensaje": "Curso creado exitosamente",
            "id_curso": nuevo_curso.id_curso
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@cursos_bp.route('/<int:id_curso>', methods=['PUT'])
@jwt_required()
@rol_requerido([1, 2])  # Admin o Gestor
def actualizar_curso(id_curso):
    """Actualiza un curso existente"""
    try:
        curso = Curso.query.get(id_curso)
        
        if not curso:
            return jsonify({"error": "Curso no encontrado"}), 404
        
        data = request.get_json()
        nombre = data.get('nombre')
        creditos = data.get('creditos')
        
        if nombre:
            # Verificar si existe otro curso con el mismo nombre
            curso_existente = Curso.query.filter(Curso.curso == nombre, Curso.id_curso != id_curso).first()
            if curso_existente:
                return jsonify({"error": "Ya existe otro curso con ese nombre"}), 409
            
            curso.curso = nombre
        
        if creditos is not None:
            curso.creditos = creditos
        
        db.session.commit()
        
        return jsonify({
            "mensaje": "Curso actualizado exitosamente",
            "curso": {
                "id_curso": curso.id_curso,
                "nombre": curso.curso,
                "creditos": curso.creditos
            }
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@cursos_bp.route('/<int:id_curso>', methods=['DELETE'])
@jwt_required()
@rol_requerido(1)  # Solo Admin
def eliminar_curso(id_curso):
    """Elimina un curso existente"""
    try:
        curso = Curso.query.get(id_curso)
        
        if not curso:
            return jsonify({"error": "Curso no encontrado"}), 404
        
        # Verificar que no haya historiales académicos asociados
        from app.models.historial_academico import HistorialAcademico
        historiales = HistorialAcademico.query.filter_by(id_curso=id_curso).first()
        
        if historiales:
            return jsonify({"error": "No se puede eliminar el curso porque tiene historiales académicos asociados"}), 400
        
        db.session.delete(curso)
        db.session.commit()
        
        return jsonify({"mensaje": "Curso eliminado exitosamente"}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500