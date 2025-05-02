# app/utils/errores.py

class ErrorHandler:
    """Clase para manejar errores de manera centralizada"""
    
    @staticmethod
    def handle_error(e, status_code=500):
        """
        Maneja excepciones y retorna una respuesta de error JSON
        
        :param e: La excepción capturada
        :param status_code: Código de estado HTTP (por defecto 500)
        :return: Tupla con respuesta JSON y código de estado
        """
        from flask import jsonify
        import traceback
        
        # Registrar el error en los logs
        traceback.print_exc()
        
        # Respuesta para el cliente
        response = {
            "error": True,
            "mensaje": str(e),
            "tipo": e.__class__.__name__
        }
        
        return jsonify(response), status_code