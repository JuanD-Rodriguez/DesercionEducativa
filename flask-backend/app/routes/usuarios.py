# app/routes/usuarios.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
import random, string
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.usuario import Usuario
from app.models.estudiante import Estudiante
from app.models.gestor import Gestor
from app.models.ingenieria import Ingenieria
from app.utils.decoradores import rol_requerido

usuarios_bp = Blueprint('usuarios', __name__)

def generar_contrasena_aleatoria(longitud=10):
    """Genera una contraseña aleatoria segura"""
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(caracteres) for _ in range(longitud))

@usuarios_bp.route('/crear', methods=['POST'])
def crear_usuario():
    """Crea un nuevo usuario (estudiante o gestor) - versión simplificada para depuración"""
    try:
        # Obtener datos de la solicitud
        data = request.get_json()
        
        # Imprimir los datos recibidos para depuración
        print("Datos recibidos:", data)
        
        # Verificar campos mínimos requeridos
        tipo = data.get("tipo", "")
        if not tipo:
            return jsonify({'error': 'El tipo de usuario es requerido (estudiante o gestor)'}), 400
            
        # Normalizar el tipo a minúsculas
        tipo = tipo.lower()
        if tipo not in ["estudiante", "gestor"]:
            return jsonify({'error': 'Tipo debe ser estudiante o gestor'}), 400

        # Obtener datos básicos con valores predeterminados si no existen
        nombre = data.get('nombre', 'Usuario')
        apellido = data.get('apellido', 'Nuevo')
        correo = data.get('correo_electronico', f"{nombre.lower()}.{apellido.lower()}@ejemplo.com")
        
        # Verificar duplicados
        if Usuario.query.filter_by(nombre_usuario=correo).first():
            return jsonify({'error': 'Ya existe un usuario con ese correo'}), 409

        # Generar contraseña aleatoria
        contrasena = "password123"  # Contraseña predeterminada simple para pruebas
        hash_contrasena = generate_password_hash(contrasena)
        
        # Crear usuario con id_rol apropiado (3 para estudiante, 2 para gestor)
        nuevo_usuario = Usuario(
            nombre_usuario=correo,
            contrasena=hash_contrasena,
            id_rol=3 if tipo == "estudiante" else 2
        )
        
        # Guardar usuario y obtener ID
        db.session.add(nuevo_usuario)
        db.session.flush()  # Para obtener el ID antes de commit
        
        id_usuario = nuevo_usuario.id_usuario
        print(f"Usuario creado con ID: {id_usuario}")
        
        # Crear perfil correspondiente
        if tipo == "estudiante":
            # Para estudiantes, aseguramos que haya una ingeniería válida
            id_ingenieria = data.get('id_ingenieria', 1)  # Valor predeterminado 1
            
            # Verificar si la ingeniería existe, si no, usar la primera disponible
            if not Ingenieria.query.get(id_ingenieria):
                primer_ingenieria = Ingenieria.query.first()
                id_ingenieria = primer_ingenieria.id_ingenieria if primer_ingenieria else 1
            
            nuevo_perfil = Estudiante(
                id_usuario=id_usuario,
                nombre=nombre,
                apellido=apellido,
                correo_electronico=correo,
                id_ingenieria=id_ingenieria,
                promedio=data.get('promedio', 0),
                fecha_registro=datetime.now().date()
            )
            print(f"Creando perfil de estudiante: {nombre} {apellido}")
        else:  # gestor
            nuevo_perfil = Gestor(
                id_usuario=id_usuario,
                nombre=nombre,
                apellido=apellido,
                telefono=data.get('telefono', '000-000-0000')
            )
            print(f"Creando perfil de gestor: {nombre} {apellido}")

        # Guardar el perfil
        db.session.add(nuevo_perfil)
        
        # Confirmar cambios
        db.session.commit()
        print("¡Usuario y perfil creados con éxito!")

        # Respuesta exitosa
        return jsonify({
            'mensaje': f'{tipo.capitalize()} creado exitosamente',
            'correo': correo,
            'contraseña': contrasena,  # En producción no mostrarías esto
            'id_usuario': id_usuario
        }), 201
    
    except Exception as e:
        # Revertir cambios en caso de error
        db.session.rollback()
        
        # Depuración detallada
        import traceback
        print("ERROR en crear_usuario():")
        print(str(e))
        traceback.print_exc()
        
        # Respuesta de error
        return jsonify({'error': f"No se pudo crear el usuario: {str(e)}"}), 500

@usuarios_bp.route('/estudiantes', methods=['GET'])
def obtener_estudiantes():
    """Obtiene la lista de todos los estudiantes"""
    try:
        # Consulta simple sin join para minimizar problemas
        estudiantes = Estudiante.query.all()
        
        resultado = []
        for estudiante in estudiantes:
            # Obtener ingeniería de forma segura
            ingenieria = Ingenieria.query.get(estudiante.id_ingenieria)
            ingenieria_nombre = ingenieria.nombre_ingenieria if ingenieria else "No especificada"
            
            resultado.append({
                'id_estudiante': estudiante.id_estudiante,
                'nombre': estudiante.nombre,
                'apellido': estudiante.apellido,
                'correo_electronico': estudiante.correo_electronico,
                'ingenieria': ingenieria_nombre,
                'promedio': float(estudiante.promedio) if estudiante.promedio else 0,
                'fecha_registro': estudiante.fecha_registro.strftime('%Y-%m-%d') if estudiante.fecha_registro else None
            })
        
        return jsonify(resultado), 200
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@usuarios_bp.route('/gestores', methods=['GET'])
def obtener_gestores():
    """Obtiene la lista de todos los gestores"""
    try:
        gestores = Gestor.query.all()
        
        resultado = []
        for gestor in gestores:
            resultado.append({
                'id_gestor': gestor.id_gestor,
                'nombre': gestor.nombre,
                'apellido': gestor.apellido,
                'telefono': gestor.telefono
            })
        
        return jsonify(resultado), 200
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@usuarios_bp.route('/estudiante/<int:id_estudiante>', methods=['GET'])
def obtener_estudiante(id_estudiante):
    """Obtiene detalles de un estudiante específico"""
    try:
        estudiante = Estudiante.query.get(id_estudiante)
        
        if not estudiante:
            return jsonify({'error': 'Estudiante no encontrado'}), 404
        
        ingenieria = Ingenieria.query.get(estudiante.id_ingenieria)
        
        resultado = {
            'id_estudiante': estudiante.id_estudiante,
            'id_usuario': estudiante.id_usuario,
            'nombre': estudiante.nombre,
            'apellido': estudiante.apellido,
            'correo_electronico': estudiante.correo_electronico,
            'id_ingenieria': estudiante.id_ingenieria,
            'ingenieria': ingenieria.nombre_ingenieria if ingenieria else None,
            'promedio': float(estudiante.promedio) if estudiante.promedio else 0,
            'fecha_registro': estudiante.fecha_registro.strftime('%Y-%m-%d') if estudiante.fecha_registro else None
        }
        
        return jsonify(resultado), 200
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@usuarios_bp.route('/actualizar/<int:id_usuario>', methods=['PUT'])
def actualizar_usuario(id_usuario):
    """Actualiza la información de un usuario"""
    try:
        data = request.get_json()
        usuario = Usuario.query.get(id_usuario)
        
        if not usuario:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        # Actualizar contraseña si se proporciona
        nueva_contrasena = data.get('contrasena')
        if nueva_contrasena:
            usuario.contrasena = generate_password_hash(nueva_contrasena)
        
        # Actualizar rol si se proporciona
        nuevo_rol = data.get('id_rol')
        if nuevo_rol:
            usuario.id_rol = nuevo_rol
        
        db.session.commit()
        
        # Si es estudiante o gestor, actualizar su perfil
        if usuario.id_rol == 3:  # Estudiante
            estudiante = Estudiante.query.filter_by(id_usuario=id_usuario).first()
            if estudiante and data.get('estudiante'):
                estudiante_data = data.get('estudiante')
                if 'nombre' in estudiante_data:
                    estudiante.nombre = estudiante_data['nombre']
                if 'apellido' in estudiante_data:
                    estudiante.apellido = estudiante_data['apellido']
                if 'correo_electronico' in estudiante_data:
                    estudiante.correo_electronico = estudiante_data['correo_electronico']
                if 'id_ingenieria' in estudiante_data:
                    estudiante.id_ingenieria = estudiante_data['id_ingenieria']
                if 'promedio' in estudiante_data:
                    estudiante.promedio = estudiante_data['promedio']
        
        elif usuario.id_rol == 2:  # Gestor
            gestor = Gestor.query.filter_by(id_usuario=id_usuario).first()
            if gestor and data.get('gestor'):
                gestor_data = data.get('gestor')
                if 'nombre' in gestor_data:
                    gestor.nombre = gestor_data['nombre']
                if 'apellido' in gestor_data:
                    gestor.apellido = gestor_data['apellido']
                if 'telefono' in gestor_data:
                    gestor.telefono = gestor_data['telefono']
        
        db.session.commit()
        
        return jsonify({'mensaje': 'Usuario actualizado exitosamente'}), 200
    
    except Exception as e:
        db.session.rollback()
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@usuarios_bp.route('/eliminar/<int:id_usuario>', methods=['DELETE'])
def eliminar_usuario(id_usuario):
    """Elimina un usuario y su perfil asociado"""
    try:
        usuario = Usuario.query.get(id_usuario)
        
        if not usuario:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        # Eliminar perfil asociado primero
        if usuario.id_rol == 3:  # Estudiante
            estudiante = Estudiante.query.filter_by(id_usuario=id_usuario).first()
            if estudiante:
                db.session.delete(estudiante)
        
        elif usuario.id_rol == 2:  # Gestor
            gestor = Gestor.query.filter_by(id_usuario=id_usuario).first()
            if gestor:
                db.session.delete(gestor)
        
        # Ahora eliminar el usuario
        db.session.delete(usuario)
        db.session.commit()
        
        return jsonify({'mensaje': 'Usuario eliminado exitosamente'}), 200
    
    except Exception as e:
        db.session.rollback()
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@usuarios_bp.route('/cambiar_contrasena', methods=['POST'])
def cambiar_contrasena():
    """Permite a un usuario cambiar su propia contraseña"""
    try:
        data = request.get_json()
        id_usuario = data.get('id_usuario')
        contrasena_actual = data.get('contrasena_actual')
        nueva_contrasena = data.get('nueva_contrasena')
        
        if not id_usuario or not contrasena_actual or not nueva_contrasena:
            return jsonify({'error': 'Todos los campos son requeridos'}), 400
        
        usuario = Usuario.query.get(id_usuario)
        if not usuario:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        # Actualizar contraseña
        usuario.contrasena = generate_password_hash(nueva_contrasena)
        db.session.commit()
        
        return jsonify({'mensaje': 'Contraseña actualizada exitosamente'}), 200
    
    except Exception as e:
        db.session.rollback()
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@usuarios_bp.route('/ingenierias', methods=['GET'])
def obtener_ingenierias():
    """Obtiene la lista de todas las carreras de ingeniería"""
    try:
        ingenierias = Ingenieria.query.all()
        
        resultado = []
        for ingenieria in ingenierias:
            resultado.append({
                'id_ingenieria': ingenieria.id_ingenieria,
                'nombre_ingenieria': ingenieria.nombre_ingenieria
            })
        
        return jsonify(resultado), 200
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500