# app/utils/validacion.py
from flask import request, jsonify
from functools import wraps

def validar_json(*campos_requeridos):
    """
    Decorador para validar que la petición contiene un JSON válido con los campos requeridos
    :param campos_requeridos: Nombres de los campos que deben estar presentes en el JSON
    """
    def decorador(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Verificar que hay datos JSON en la petición
            if not request.is_json:
                return jsonify({"error": "Se esperaba un contenido JSON"}), 400
            
            # Obtener los datos JSON
            data = request.get_json()
            
            # Verificar que todos los campos requeridos estén presentes
            campos_faltantes = []
            for campo in campos_requeridos:
                if campo not in data or data[campo] is None:
                    campos_faltantes.append(campo)
            
            if campos_faltantes:
                return jsonify({
                    "error": "Campos requeridos faltantes",
                    "campos": campos_faltantes
                }), 400
            
            # Si todo está bien, continuar con la función original
            return f(*args, **kwargs)
        return wrapper
    return decorador

def validar_parametros_url(*params_requeridos):
    """
    Decorador para validar que la petición contiene los parámetros URL requeridos
    :param params_requeridos: Nombres de los parámetros que deben estar presentes en la URL
    """
    def decorador(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Verificar que todos los parámetros requeridos estén presentes
            params_faltantes = []
            for param in params_requeridos:
                if param not in request.args:
                    params_faltantes.append(param)
            
            if params_faltantes:
                return jsonify({
                    "error": "Parámetros URL requeridos faltantes",
                    "parametros": params_faltantes
                }), 400
            
            # Si todo está bien, continuar con la función original
            return f(*args, **kwargs)
        return wrapper
    return decorador