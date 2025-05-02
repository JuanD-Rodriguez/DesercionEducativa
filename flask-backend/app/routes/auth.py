# app/routes/auth.py
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta

from app import db
from app.models.usuario import Usuario
from app.models.rol import Rol

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('nombre_usuario')
        password = data.get('contrasena')

        # Buscar el usuario en la base de datos
        user = Usuario.query.filter_by(nombre_usuario=username).first()

        if not user:
            # Para pruebas iniciales, loguear información
            print(f"Usuario no encontrado: {username}")
            return jsonify({"message": "Credenciales inválidas"}), 401

        # Opciones de bypass para desarrollo (para admin/admin123 y gestor1/gestor123)
        if (username == 'admin' and password == 'admin123') or (username == 'gestor1' and password == 'gestor123'):
            access_token = create_access_token(identity={
                "id": user.id_usuario,
                "rol": user.id_rol,
                "usuario": user.nombre_usuario
            })
            return jsonify({"access_token": access_token}), 200
            
        # Verificación normal de contraseña
        if check_password_hash(user.contrasena, password):
            access_token = create_access_token(identity={
                "id": user.id_usuario,
                "rol": user.id_rol,
                "usuario": user.nombre_usuario
            })
            return jsonify({"access_token": access_token}), 200
        else:
            # Para pruebas iniciales, loguear información
            print(f"Contraseña incorrecta para usuario: {username}")
            return jsonify({"message": "Credenciales inválidas"}), 401
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/check', methods=['GET'])
def check_connection():
    """Endpoint para verificar la conexión a la base de datos"""
    try:
        # Contar usuarios
        user_count = Usuario.query.count()
        role_count = Rol.query.count()
        
        # Ver todos los roles
        roles = Rol.query.all()
        roles_list = [{"id": r.id_rol, "nombre": r.nombre} for r in roles]
        
        # Ver todos los usuarios
        users = Usuario.query.all()
        users_list = [{"id": u.id_usuario, "nombre": u.nombre_usuario, "rol": u.id_rol} for u in users]
        
        return jsonify({
            "status": "ok",
            "message": "Conexión a la base de datos establecida correctamente",
            "counts": {
                "usuarios": user_count,
                "roles": role_count
            },
            "roles": roles_list,
            "usuarios": users_list
        }), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# Endpoint para generar hashes de contraseñas (útil para desarrollo)
@auth_bp.route('/generate-hash/<password>', methods=['GET'])
def generate_hash(password):
    """Genera un hash para una contraseña dada"""
    try:
        hashed_password = generate_password_hash(password)
        return jsonify({
            "password": password,
            "hash": hashed_password
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500