from flask import Blueprint, jsonify
from app.models.ingenieria import Ingenieria
from sqlalchemy.exc import SQLAlchemyError

ingenieria_bp = Blueprint('ingenieria_bp', __name__)

@ingenieria_bp.route('/', methods=['GET'])
def obtener_ingenierias():
    try:
        ingenierias = Ingenieria.query.all()
        resultado = [{
            "id": i.id_ingenieria,
            "nombre": i.nombre_ingenieria
        } for i in ingenierias]
        return jsonify(resultado), 200
    except SQLAlchemyError as e:
        return jsonify({"error": "Error al obtener ingenierías", "detalle": str(e)}), 500
