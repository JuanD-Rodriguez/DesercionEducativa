from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.estudiante import Estudiante
from app.models.historial_academico import HistorialAcademico
from app.models.corte_evaluacion import CorteEvaluacion
from app.models.riesgo_socioeconomico import RiesgoSocioeconomico
from app.services.modelo_prediccion import ModeloPrediccion
from app import db

prediccion_bp = Blueprint('prediccion', __name__)

modelo = ModeloPrediccion()

@prediccion_bp.route('/entrenar', methods=['POST'])
@jwt_required()
def entrenar_modelo():
    """Endpoint para entrenar el modelo con los datos actuales"""
    # Verificar que sea un administrador o gestor
    identidad = get_jwt_identity()
    if identidad["rol"] not in [1, 2]:  # Admin o Gestor
        return jsonify({"error": "No autorizado"}), 403
    
    resultado = modelo.entrenar_modelo()
    
    if resultado:
        return jsonify({"mensaje": "Modelo entrenado con éxito"}), 200
    else:
        return jsonify({"error": "Error al entrenar el modelo"}), 500

@prediccion_bp.route('/predecir/<int:id_estudiante>', methods=['GET'])
@jwt_required()
def predecir_estudiante(id_estudiante):
    """Endpoint para predecir el riesgo de deserción de un estudiante específico"""
    try:
        # Obtener datos del estudiante
        estudiante = Estudiante.query.get(id_estudiante)
        if not estudiante:
            return jsonify({"error": "Estudiante no encontrado"}), 404
        
        # Obtener datos académicos
        historial = HistorialAcademico.query.filter_by(id_estudiante=id_estudiante).order_by(HistorialAcademico.id_historial.desc()).first()
        corte = None
        if historial:
            corte = CorteEvaluacion.query.filter_by(id_historial=historial.id_historial).order_by(CorteEvaluacion.numero_corte.desc()).first()
        
        # Obtener datos socioeconómicos
        riesgo_socio = RiesgoSocioeconomico.query.filter_by(id_estudiante=id_estudiante).first()
        
        # Preparar datos para predicción
        datos_estudiante = {
            'promedio': estudiante.promedio if estudiante else 0,
            'calificacion_final': historial.calificacion_final if historial else 0,
            'asistencia_corte': corte.asistencia_corte if corte else 0,
            'nivel_ingreso_num': 1 if riesgo_socio and riesgo_socio.nivel_ingreso == 'bajo' else (
                                3 if riesgo_socio and riesgo_socio.nivel_ingreso == 'alto' else 2),
            'acceso_becas': 1 if riesgo_socio and riesgo_socio.acceso_becas else 0
        }
        
        # Realizar predicción
        riesgo = modelo.predecir_riesgo(datos_estudiante)
        
        # Determinar factores de riesgo
        factores = []
        if estudiante.promedio < 3.0:
            factores.append("Bajo promedio académico")
        if historial and historial.calificacion_final < 3.0:
            factores.append("Bajo rendimiento en cursos recientes")
        if corte and corte.asistencia_corte < 70:
            factores.append("Baja asistencia a clases")
        if riesgo_socio:
            if riesgo_socio.nivel_ingreso == 'bajo':
                factores.append("Situación económica vulnerable")
            if not riesgo_socio.acceso_becas:
                factores.append("Sin apoyo de becas")
        
        # Guardar predicción
        modelo.guardar_prediccion(
            id_estudiante=id_estudiante,
            riesgo=riesgo,
            factores=", ".join(factores)
        )
        
        return jsonify({
            "id_estudiante": id_estudiante,
            "nombre": f"{estudiante.nombre} {estudiante.apellido}",
            "riesgo_desercion": round(float(riesgo), 4),
            "factores_riesgo": factores,
            "datos_usados": datos_estudiante
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@prediccion_bp.route('/predecir_grupo', methods=['POST'])
@jwt_required()
def predecir_grupo():
    """Predice el riesgo de deserción para un grupo de estudiantes"""
    try:
        data = request.get_json()
        id_ingenieria = data.get('id_ingenieria')
        
        # Construir la consulta base
        estudiantes_query = Estudiante.query
        
        # Filtrar por ingeniería si se especifica
        if id_ingenieria:
            estudiantes_query = estudiantes_query.filter_by(id_ingenieria=id_ingenieria)
        
        # Obtener estudiantes
        estudiantes = estudiantes_query.all()
        
        resultados = []
        for estudiante in estudiantes:
            # Para cada estudiante, llamar al endpoint individual (reutilizando lógica)
            # En una implementación real, probablemente querrías hacer esto más eficiente
            try:
                # Obtener datos académicos
                historial = HistorialAcademico.query.filter_by(id_estudiante=estudiante.id_estudiante).order_by(HistorialAcademico.id_historial.desc()).first()
                corte = None
                if historial:
                    corte = CorteEvaluacion.query.filter_by(id_historial=historial.id_historial).order_by(CorteEvaluacion.numero_corte.desc()).first()
                
                # Obtener datos socioeconómicos
                riesgo_socio = RiesgoSocioeconomico.query.filter_by(id_estudiante=estudiante.id_estudiante).first()
                
                # Preparar datos para predicción
                datos_estudiante = {
                    'promedio': estudiante.promedio if estudiante else 0,
                    'calificacion_final': historial.calificacion_final if historial else 0,
                    'asistencia_corte': corte.asistencia_corte if corte else 0,
                    'nivel_ingreso_num': 1 if riesgo_socio and riesgo_socio.nivel_ingreso == 'bajo' else (
                                        3 if riesgo_socio and riesgo_socio.nivel_ingreso == 'alto' else 2),
                    'acceso_becas': 1 if riesgo_socio and riesgo_socio.acceso_becas else 0
                }
                
                # Realizar predicción
                riesgo = modelo.predecir_riesgo(datos_estudiante)
                
                # Determinar factores de riesgo
                factores = []
                if estudiante.promedio < 3.0:
                    factores.append("Bajo promedio académico")
                if historial and historial.calificacion_final < 3.0:
                    factores.append("Bajo rendimiento en cursos recientes")
                if corte and corte.asistencia_corte < 70:
                    factores.append("Baja asistencia a clases")
                if riesgo_socio:
                    if riesgo_socio.nivel_ingreso == 'bajo':
                        factores.append("Situación económica vulnerable")
                    if not riesgo_socio.acceso_becas:
                        factores.append("Sin apoyo de becas")
                
                # Guardar predicción
                modelo.guardar_prediccion(
                    id_estudiante=estudiante.id_estudiante,
                    riesgo=riesgo,
                    factores=", ".join(factores)
                )
                
                # Añadir a resultados
                resultados.append({
                    "id_estudiante": estudiante.id_estudiante,
                    "nombre": f"{estudiante.nombre} {estudiante.apellido}",
                    "riesgo_desercion": round(float(riesgo), 4),
                    "factores_riesgo": factores
                })
            
            except Exception as e:
                # Si falla un estudiante, continuar con el siguiente
                print(f"Error al procesar estudiante {estudiante.id_estudiante}: {e}")
        
        return jsonify({
            "total_estudiantes": len(estudiantes),
            "estudiantes_procesados": len(resultados),
            "resultados": resultados
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500