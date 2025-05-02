# app/utils/decoradores.py
from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask import jsonify

def rol_requerido(roles_requeridos):
    """
    Decorador que verifica si el usuario tiene uno de los roles requeridos
    :param roles_requeridos: ID de rol o lista de IDs de roles permitidos
    """
    def decorador(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                identidad = get_jwt_identity()
                
                # Verificar si la identidad tiene la estructura esperada
                if not isinstance(identidad, dict) or 'rol' not in identidad:
                    print("Estructura de identidad JWT inválida:", identidad)
                    return jsonify({"message": "Token de autenticación inválido"}), 401
                
                # Convertir a lista si es un solo rol
                if not isinstance(roles_requeridos, list):
                    roles_lista = [roles_requeridos]
                else:
                    roles_lista = roles_requeridos
                    
                if identidad["rol"] not in roles_lista:
                    return jsonify({"message": "No autorizado para realizar esta acción"}), 403
                
                return f(*args, **kwargs)
            except Exception as e:
                import traceback
                traceback.print_exc()
                return jsonify({"message": f"Error de autenticación: {str(e)}"}), 401
        return wrapper
    return decorador