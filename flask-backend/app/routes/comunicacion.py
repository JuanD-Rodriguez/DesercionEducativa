# app/routes/comunicacion.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.mensaje import Mensaje
from app.models.usuario import Usuario
from app.models.estudiante import Estudiante
from app.models.gestor import Gestor
from datetime import datetime

comunicacion_bp = Blueprint('comunicacion', __name__)

@comunicacion_bp.route('/enviar', methods=['POST'])
@jwt_required()
def enviar_mensaje():
    """Envía un mensaje a otro usuario"""
    try:
        data = request.get_json()
        identidad = get_jwt_identity()
        id_remitente = identidad['id']
        id_destinatario = data.get('id_destinatario')
        asunto = data.get('asunto')
        contenido = data.get('contenido')
        
        if not id_destinatario or not asunto or not contenido:
            return jsonify({"error": "Todos los campos son obligatorios"}), 400
        
        # Verificar que el destinatario existe
        destinatario = Usuario.query.get(id_destinatario)
        if not destinatario:
            return jsonify({"error": "Destinatario no encontrado"}), 404
        
        # Verificar que la comunicación es permitida (estudiante a gestor o viceversa)
        remitente = Usuario.query.get(id_remitente)
        if remitente.id_rol == 3 and destinatario.id_rol != 2:  # Estudiante a no-gestor
            return jsonify({"error": "Los estudiantes solo pueden enviar mensajes a gestores"}), 403
        
        if remitente.id_rol == 2 and destinatario.id_rol != 3:  # Gestor a no-estudiante
            return jsonify({"error": "Los gestores solo pueden enviar mensajes a estudiantes"}), 403
        
        # Crear y guardar el mensaje
        nuevo_mensaje = Mensaje(
            id_remitente=id_remitente,
            id_destinatario=id_destinatario,
            asunto=asunto,
            contenido=contenido,
            fecha_envio=datetime.now(),
            leido=False
        )
        
        db.session.add(nuevo_mensaje)
        db.session.commit()
        
        return jsonify({"mensaje": "Mensaje enviado exitosamente", "id_mensaje": nuevo_mensaje.id_mensaje}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@comunicacion_bp.route('/recibidos', methods=['GET'])
@jwt_required()
def mensajes_recibidos():
    """Obtiene los mensajes recibidos por el usuario autenticado"""
    try:
        identidad = get_jwt_identity()
        id_usuario = identidad['id']
        
        # Obtener todos los mensajes donde el usuario es destinatario
        mensajes = db.session.query(
            Mensaje,
            Usuario
        ).join(
            Usuario, Mensaje.id_remitente == Usuario.id_usuario
        ).filter(
            Mensaje.id_destinatario == id_usuario
        ).order_by(
            Mensaje.fecha_envio.desc()
        ).all()
        
        resultado = []
        for mensaje, remitente in mensajes:
            nombre_remitente = ""
            
            # Obtener nombre del remitente según su rol
            if remitente.id_rol == 2:  # Gestor
                gestor = Gestor.query.filter_by(id_usuario=remitente.id_usuario).first()
                if gestor:
                    nombre_remitente = f"{gestor.nombre} {gestor.apellido}"
            elif remitente.id_rol == 3:  # Estudiante
                estudiante = Estudiante.query.filter_by(id_usuario=remitente.id_usuario).first()
                if estudiante:
                    nombre_remitente = f"{estudiante.nombre} {estudiante.apellido}"
            
            resultado.append({
                "id_mensaje": mensaje.id_mensaje,
                "id_remitente": mensaje.id_remitente,
                "nombre_remitente": nombre_remitente,
                "asunto": mensaje.asunto,
                "contenido": mensaje.contenido,
                "fecha_envio": mensaje.fecha_envio.strftime("%Y-%m-%d %H:%M:%S"),
                "leido": mensaje.leido
            })
        
        return jsonify(resultado), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@comunicacion_bp.route('/enviados', methods=['GET'])
@jwt_required()
def mensajes_enviados():
    """Obtiene los mensajes enviados por el usuario autenticado"""
    try:
        identidad = get_jwt_identity()
        id_usuario = identidad['id']
        
        # Obtener todos los mensajes donde el usuario es remitente
        mensajes = db.session.query(
            Mensaje,
            Usuario
        ).join(
            Usuario, Mensaje.id_destinatario == Usuario.id_usuario
        ).filter(
            Mensaje.id_remitente == id_usuario
        ).order_by(
            Mensaje.fecha_envio.desc()
        ).all()
        
        resultado = []
        for mensaje, destinatario in mensajes:
            nombre_destinatario = ""
            
            # Obtener nombre del destinatario según su rol
            if destinatario.id_rol == 2:  # Gestor
                gestor = Gestor.query.filter_by(id_usuario=destinatario.id_usuario).first()
                if gestor:
                    nombre_destinatario = f"{gestor.nombre} {gestor.apellido}"
            elif destinatario.id_rol == 3:  # Estudiante
                estudiante = Estudiante.query.filter_by(id_usuario=destinatario.id_usuario).first()
                if estudiante:
                    nombre_destinatario = f"{estudiante.nombre} {estudiante.apellido}"
            
            resultado.append({
                "id_mensaje": mensaje.id_mensaje,
                "id_destinatario": mensaje.id_destinatario,
                "nombre_destinatario": nombre_destinatario,
                "asunto": mensaje.asunto,
                "contenido": mensaje.contenido,
                "fecha_envio": mensaje.fecha_envio.strftime("%Y-%m-%d %H:%M:%S"),
                "leido": mensaje.leido
            })
        
        return jsonify(resultado), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@comunicacion_bp.route('/marcar_leido/<int:id_mensaje>', methods=['PUT'])
@jwt_required()
def marcar_como_leido(id_mensaje):
    """Marca un mensaje como leído"""
    try:
        identidad = get_jwt_identity()
        id_usuario = identidad['id']
        
        mensaje = Mensaje.query.get(id_mensaje)
        
        if not mensaje:
            return jsonify({"error": "Mensaje no encontrado"}), 404
        
        # Verificar que el usuario es el destinatario del mensaje
        if mensaje.id_destinatario != id_usuario:
            return jsonify({"error": "No autorizado"}), 403
        
        mensaje.leido = True
        db.session.commit()
        
        return jsonify({"mensaje": "Mensaje marcado como leído"}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@comunicacion_bp.route('/mensaje/<int:id_mensaje>', methods=['GET'])
@jwt_required()
def obtener_mensaje(id_mensaje):
    """Obtiene un mensaje específico"""
    try:
        identidad = get_jwt_identity()
        id_usuario = identidad['id']
        
        mensaje = Mensaje.query.get(id_mensaje)
        
        if not mensaje:
            return jsonify({"error": "Mensaje no encontrado"}), 404
        
        # Verificar que el usuario es el remitente o destinatario del mensaje
        if mensaje.id_remitente != id_usuario and mensaje.id_destinatario != id_usuario:
            return jsonify({"error": "No autorizado"}), 403
        
        # Si el usuario es el destinatario, marcar como leído
        if mensaje.id_destinatario == id_usuario and not mensaje.leido:
            mensaje.leido = True
            db.session.commit()
        
        # Obtener información del remitente y destinatario
        remitente = Usuario.query.get(mensaje.id_remitente)
        destinatario = Usuario.query.get(mensaje.id_destinatario)
        
        nombre_remitente = ""
        nombre_destinatario = ""
        
        # Determinar nombres según roles
        if remitente.id_rol == 2:  # Gestor
            gestor = Gestor.query.filter_by(id_usuario=remitente.id_usuario).first()
            if gestor:
                nombre_remitente = f"{gestor.nombre} {gestor.apellido}"
        elif remitente.id_rol == 3:  # Estudiante
            estudiante = Estudiante.query.filter_by(id_usuario=remitente.id_usuario).first()
            if estudiante:
                nombre_remitente = f"{estudiante.nombre} {estudiante.apellido}"
        
        if destinatario.id_rol == 2:  # Gestor
            gestor = Gestor.query.filter_by(id_usuario=destinatario.id_usuario).first()
            if gestor:
                nombre_destinatario = f"{gestor.nombre} {gestor.apellido}"
        elif destinatario.id_rol == 3:  # Estudiante
            estudiante = Estudiante.query.filter_by(id_usuario=destinatario.id_usuario).first()
            if estudiante:
                nombre_destinatario = f"{estudiante.nombre} {estudiante.apellido}"
        
        return jsonify({
            "id_mensaje": mensaje.id_mensaje,
            "id_remitente": mensaje.id_remitente,
            "nombre_remitente": nombre_remitente,
            "id_destinatario": mensaje.id_destinatario,
            "nombre_destinatario": nombre_destinatario,
            "asunto": mensaje.asunto,
            "contenido": mensaje.contenido,
            "fecha_envio": mensaje.fecha_envio.strftime("%Y-%m-%d %H:%M:%S"),
            "leido": mensaje.leido
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500