from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.formulario_desercion import FormularioDesercion

formulario_bp = Blueprint('formulario', __name__)

@formulario_bp.route('/crear', methods=['POST', 'OPTIONS'])
@jwt_required(optional=True)
def crear_formulario():
    if request.method == 'OPTIONS':
        return '', 200

    identity = get_jwt_identity()
    if not identity:
        return jsonify({"msg": "Token requerido"}), 401

    data = request.get_json()

    if not data or 'titulo' not in data or 'estructura_json' not in data:
        return jsonify({'error': 'Datos incompletos'}), 400

    nuevo_formulario = FormularioDesercion(
        titulo=data['titulo'],
        descripcion=data.get('descripcion', ''),
        estructura_json=data['estructura_json']
    )
    db.session.add(nuevo_formulario)
    db.session.commit()

    return jsonify({'msg': 'Formulario creado exitosamente', 'id': nuevo_formulario.id_formulario}), 201


@formulario_bp.route('/formularios', methods=['GET'])
@jwt_required()
def listar_formularios():
    formularios = FormularioDesercion.query.all()
    resultado = [
        {
            'id': f.id_formulario,
            'titulo': f.titulo,
            'descripcion': f.descripcion,
            'estructura_json': f.estructura_json,
            'fecha_creacion': f.fecha_creacion.isoformat()
        }
        for f in formularios
    ]
    return jsonify(resultado), 200

@formulario_bp.route('/formularios/<int:id_formulario>', methods=['GET'])
@jwt_required()
def obtener_formulario(id_formulario):
    formulario = FormularioDesercion.query.get(id_formulario)
    if not formulario:
        return jsonify({'error': 'Formulario no encontrado'}), 404

    return jsonify({
        'id': formulario.id_formulario,
        'titulo': formulario.titulo,
        'descripcion': formulario.descripcion,
        'estructura_json': formulario.estructura_json,
        'fecha_creacion': formulario.fecha_creacion.isoformat()
    }), 200