from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models.formulario_desercion import FormularioDesercion
from app.models.pregunta import Pregunta
from app.models.respuesta import Respuesta
from app.models.gestor import Gestor
from app import db
from datetime import datetime, date

formulario_bp = Blueprint('formulario', __name__)

@formulario_bp.route('/crear', methods=['POST'])
@jwt_required()
def crear_formulario():
    """Crea un nuevo formulario de deserción"""
    try:
        # Verificar que sea un gestor
        user_id = get_jwt_identity()  # Ahora es un string con el ID del usuario
        claims = get_jwt()  # Obtener los claims adicionales
        user_rol = claims.get("rol")  # Obtener el rol de los claims
        
        if user_rol != 2:  # Rol de Gestor
            return jsonify({"error": "Solo los gestores pueden crear formularios"}), 403
        
        # Log para depuración
        print("Datos recibidos:", request.get_json())
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se recibieron datos JSON"}), 400
            
        # Extraer el título, permitiendo cualquiera de los dos nombres de campo
        titulo = data.get('titulo') or data.get('nombre', "Formulario sin título")
        
        # Extraer preguntas, permitiendo formato más flexible
        preguntas_raw = data.get('preguntas', [])
        preguntas = []
        
        # Normalizar formato de preguntas
        for pregunta in preguntas_raw:
            # Adaptar el formato si viene del frontend
            if 'textoPregunta' in pregunta:
                preguntas.append({
                    'texto': pregunta.get('textoPregunta', ''),
                    'categoria': pregunta.get('categoria', 'academico')
                })
            # Ya tiene el formato correcto
            elif 'texto' in pregunta:
                preguntas.append({
                    'texto': pregunta.get('texto', ''),
                    'categoria': pregunta.get('categoria', 'academico')
                })
        
        # Más logs para depuración
        print("Título procesado:", titulo)
        print("Preguntas procesadas:", preguntas)
        
        if not titulo:
            return jsonify({"error": "El título es obligatorio"}), 400
        
        if not preguntas:
            return jsonify({"error": "Debe incluir al menos una pregunta"}), 400
        
        # Crear el formulario
        nuevo_formulario = FormularioDesercion(
            titulo=titulo,
            fecha_creacion=datetime.now(),
            id_gestor=int(user_id)  # Convertir de string a int
        )
        
        db.session.add(nuevo_formulario)
        db.session.flush()  # Para obtener el ID asignado
        
        # Crear las preguntas
        for pregunta_data in preguntas:
            texto = pregunta_data.get('texto')
            categoria = pregunta_data.get('categoria')
            
            # Más validaciones
            if not texto:
                return jsonify({"error": "El texto de la pregunta no puede estar vacío"}), 422
                
            if not categoria:
                return jsonify({"error": "La categoría de la pregunta no puede estar vacía"}), 422
            
            nueva_pregunta = Pregunta(
                id_formulario=nuevo_formulario.id_formulario,
                texto_pregunta=texto,
                categoria=categoria
            )
            db.session.add(nueva_pregunta)
        
        db.session.commit()
        
        return jsonify({
            "mensaje": "Formulario creado exitosamente",
            "id_formulario": nuevo_formulario.id_formulario
        }), 201
    
    except Exception as e:
        db.session.rollback()
        print("Error en crear_formulario:", str(e))  # Log para depuración
        return jsonify({"error": str(e)}), 500
    
    
@formulario_bp.route('/formularios', methods=['GET'])
@jwt_required()
def obtener_formularios():
    """Obtiene todos los formularios"""
    try:
        formularios = FormularioDesercion.query.all()
        resultado = []
        
        for f in formularios:
            gestor = Gestor.query.get(f.id_gestor)
            nombre_gestor = f"{gestor.nombre} {gestor.apellido}" if gestor else "Desconocido"
            
            resultado.append({
                "id_formulario": f.id_formulario,
                "titulo": f.titulo,
                "fecha_creacion": f.fecha_creacion.strftime("%Y-%m-%d"),
                "gestor": nombre_gestor,
                "activo": getattr(f, 'activo', True)  # Por defecto True si no existe la columna
            })
        
        return jsonify(resultado), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@formulario_bp.route('/formularios/<int:id_formulario>', methods=['GET'])
@jwt_required()
def obtener_formulario(id_formulario):
    """Obtiene un formulario específico con sus preguntas"""
    try:
        formulario = FormularioDesercion.query.get(id_formulario)
        
        if not formulario:
            return jsonify({"error": "Formulario no encontrado"}), 404
        
        preguntas = Pregunta.query.filter_by(id_formulario=id_formulario).all()
        preguntas_data = []
        
        for p in preguntas:
            preguntas_data.append({
                "id_pregunta": p.id_pregunta,
                "texto": p.texto_pregunta,
                "categoria": p.categoria
            })
        
        gestor = Gestor.query.get(formulario.id_gestor)
        nombre_gestor = f"{gestor.nombre} {gestor.apellido}" if gestor else "Desconocido"
        
        resultado = {
            "id_formulario": formulario.id_formulario,
            "titulo": formulario.titulo,
            "fecha_creacion": formulario.fecha_creacion.strftime("%Y-%m-%d"),
            "gestor": nombre_gestor,
            "preguntas": preguntas_data,
            "activo": getattr(formulario, 'activo', True)  # Por defecto True si no existe la columna
        }
        
        return jsonify(resultado), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@formulario_bp.route('/formularios/<int:id_formulario>', methods=['DELETE'])
@jwt_required()
def eliminar_formulario(id_formulario):
    """Elimina un formulario específico"""
    try:
        # Verificar que sea un gestor
        user_id = get_jwt_identity()  # Ahora es un string con el ID del usuario
        claims = get_jwt()  # Obtener los claims adicionales
        user_rol = claims.get("rol")  # Obtener el rol de los claims
        
        if user_rol != 2:  # Rol de Gestor
            return jsonify({"error": "Solo los gestores pueden eliminar formularios"}), 403
        
        formulario = FormularioDesercion.query.get(id_formulario)
        
        if not formulario:
            return jsonify({"error": "Formulario no encontrado"}), 404
        
        # Eliminar las preguntas asociadas primero
        preguntas = Pregunta.query.filter_by(id_formulario=id_formulario).all()
        
        for pregunta in preguntas:
            # También eliminar respuestas asociadas a cada pregunta
            respuestas = Respuesta.query.filter_by(id_pregunta=pregunta.id_pregunta).all()
            for respuesta in respuestas:
                db.session.delete(respuesta)
            
            db.session.delete(pregunta)
        
        # Finalmente, eliminar el formulario
        db.session.delete(formulario)
        db.session.commit()
        
        return jsonify({"mensaje": "Formulario eliminado exitosamente"}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@formulario_bp.route('/formularios/<int:id_formulario>/estado', methods=['PUT'])
@jwt_required()
def cambiar_estado_formulario(id_formulario):
    """Cambia el estado (activo/inactivo) de un formulario"""
    try:
        # Verificar que sea un gestor
        user_id = get_jwt_identity()  # Ahora es un string con el ID del usuario
        claims = get_jwt()  # Obtener los claims adicionales
        user_rol = claims.get("rol")  # Obtener el rol de los claims
        
        if user_rol != 2:  # Rol de Gestor
            return jsonify({"error": "Solo los gestores pueden modificar formularios"}), 403
        
        data = request.get_json()
        activo = data.get('activo')
        
        if activo is None:
            return jsonify({"error": "El estado 'activo' es requerido"}), 400
        
        formulario = FormularioDesercion.query.get(id_formulario)
        
        if not formulario:
            return jsonify({"error": "Formulario no encontrado"}), 404
        
        # Verificar si la columna activo existe en el modelo
        if hasattr(formulario, 'activo'):
            # Si existe la columna, actualiza el estado
            formulario.activo = activo
            db.session.commit()
            
            return jsonify({
                "mensaje": "Estado del formulario actualizado exitosamente",
                "activo": activo
            }), 200
        else:
            # Si no existe la columna, informa que no se puede cambiar el estado
            return jsonify({
                "mensaje": "La funcionalidad de cambiar estado no está disponible actualmente",
                "activo": True  # Por defecto consideramos todo activo
            }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@formulario_bp.route('/preguntas', methods=['GET'])
@jwt_required()
def obtener_preguntas():
    """Obtiene todas las preguntas, opcionalmente filtradas por formulario"""
    try:
        id_formulario = request.args.get('id_formulario')
        
        # Base query
        query = Pregunta.query
        
        # Filtrar por formulario si se especifica
        if id_formulario:
            query = query.filter_by(id_formulario=id_formulario)
        
        preguntas = query.all()
        resultado = []
        
        for p in preguntas:
            resultado.append({
                "id_pregunta": p.id_pregunta,
                "id_formulario": p.id_formulario,
                "texto_pregunta": p.texto_pregunta,
                "categoria": p.categoria
            })
        
        return jsonify(resultado), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@formulario_bp.route('/respuestas', methods=['POST'])
@jwt_required()
def guardar_respuestas():
    """Guarda las respuestas de un estudiante a un formulario"""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()  # Ahora es un string con el ID del usuario
        id_estudiante = int(user_id)  # Convertir de string a int
        respuestas = data.get('respuestas', [])
        
        if not respuestas:
            return jsonify({"error": "No se proporcionaron respuestas"}), 400
        
        for r in respuestas:
            # Verificar si ya existe una respuesta para esta pregunta
            respuesta_existente = Respuesta.query.filter_by(
                id_pregunta=r['id_pregunta'],
                id_estudiante=id_estudiante
            ).first()
            
            if respuesta_existente:
                # Actualizar respuesta existente
                respuesta_existente.opcion_seleccionada = r['opcion_seleccionada']
                respuesta_existente.fecha_respuesta = date.today()
            else:
                # Crear nueva respuesta
                nueva_respuesta = Respuesta(
                    id_pregunta=r['id_pregunta'],
                    id_estudiante=id_estudiante,
                    opcion_seleccionada=r['opcion_seleccionada'],
                    fecha_respuesta=date.today()
                )
                db.session.add(nueva_respuesta)

        db.session.commit()
        return jsonify({"mensaje": "Respuestas guardadas correctamente"}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@formulario_bp.route('/respuestas/estudiante/<int:id_estudiante>', methods=['GET'])
@jwt_required()
def obtener_respuestas_estudiante(id_estudiante):
   """Obtiene todas las respuestas de un estudiante"""
   try:
       user_id = get_jwt_identity()  # Ahora es un string con el ID del usuario
       claims = get_jwt()  # Obtener los claims adicionales
       user_rol = claims.get("rol")  # Obtener el rol de los claims
       
       # Solo el propio estudiante, los gestores o administradores pueden ver sus respuestas
       if user_rol == 3 and int(user_id) != id_estudiante:
           return jsonify({"error": "No autorizado"}), 403
       
       respuestas = Respuesta.query.filter_by(id_estudiante=id_estudiante).all()
       resultado = []
       
       for r in respuestas:
           pregunta = Pregunta.query.get(r.id_pregunta)
           formulario = None
           if pregunta:
               formulario = FormularioDesercion.query.get(pregunta.id_formulario)
           
           resultado.append({
               "id_respuesta": r.id_respuesta,
               "id_pregunta": r.id_pregunta,
               "texto_pregunta": pregunta.texto_pregunta if pregunta else "Desconocida",
               "categoria": pregunta.categoria if pregunta else "Desconocida",
               "formulario": formulario.titulo if formulario else "Desconocido",
               "opcion_seleccionada": r.opcion_seleccionada,
               "fecha_respuesta": r.fecha_respuesta.strftime("%Y-%m-%d")
           })
       
       return jsonify(resultado), 200
   
   except Exception as e:
       return jsonify({"error": str(e)}), 500

@formulario_bp.route('/diagnostico', methods=['POST'])
def diagnostico_formulario():
    """Endpoint de diagnóstico para pruebas"""
    try:
        # Imprimir todos los datos recibidos para diagnóstico
        print("Headers completos:", dict(request.headers))
        print("Método HTTP:", request.method)
        print("URL:", request.url)
        print("Datos JSON:", request.get_json())
        print("Datos de formulario:", request.form)
        
        return jsonify({
            "mensaje": "Diagnóstico completado",
            "datos_recibidos": request.get_json()
        }), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@formulario_bp.route('/respuestas/formulario/<int:id_formulario>', methods=['GET'])
@jwt_required()
def obtener_respuestas_formulario(id_formulario):
   """Obtiene todas las respuestas para un formulario específico"""
   try:
       user_id = get_jwt_identity()  # Ahora es un string con el ID del usuario
       claims = get_jwt()  # Obtener los claims adicionales
       user_rol = claims.get("rol")  # Obtener el rol de los claims
       
       # Solo gestores o administradores pueden ver todas las respuestas
       if user_rol not in [1, 2]:  # Admin o Gestor
           return jsonify({"error": "No autorizado"}), 403
       
       # Obtener todas las preguntas del formulario
       preguntas = Pregunta.query.filter_by(id_formulario=id_formulario).all()
       id_preguntas = [p.id_pregunta for p in preguntas]
       
       if not id_preguntas:
           return jsonify({"error": "Formulario sin preguntas"}), 404
       
       # Obtener respuestas para esas preguntas
       respuestas = Respuesta.query.filter(Respuesta.id_pregunta.in_(id_preguntas)).all()
       
       resultado = []
       for r in respuestas:
           pregunta = next((p for p in preguntas if p.id_pregunta == r.id_pregunta), None)
           
           resultado.append({
               "id_respuesta": r.id_respuesta,
               "id_estudiante": r.id_estudiante,
               "id_pregunta": r.id_pregunta,
               "texto_pregunta": pregunta.texto_pregunta if pregunta else "Desconocida",
               "categoria": pregunta.categoria if pregunta else "Desconocida",
               "opcion_seleccionada": r.opcion_seleccionada,
               "fecha_respuesta": r.fecha_respuesta.strftime("%Y-%m-%d")
           })
       
       return jsonify(resultado), 200
   
   except Exception as e:
       return jsonify({"error": str(e)}), 500