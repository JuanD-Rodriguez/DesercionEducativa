import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import os
from datetime import datetime
from app import db
from app.models.estudiante import Estudiante
from app.models.historial_academico import HistorialAcademico
from app.models.corte_evaluacion import CorteEvaluacion
from app.models.riesgo_socioeconomico import RiesgoSocioeconomico
from app.models.desercion import Desercion

class ModeloPrediccion:
    def __init__(self):
        self.modelo = None
        self.ruta_modelo = 'modelo_desercion.pkl'
        self.cargar_modelo()
    
    def cargar_modelo(self):
        """Carga el modelo entrenado si existe, de lo contrario crea uno nuevo"""
        try:
            if os.path.exists(self.ruta_modelo):
                with open(self.ruta_modelo, 'rb') as archivo:
                    self.modelo = pickle.load(archivo)
                print(f"Modelo cargado desde {self.ruta_modelo}")
            else:
                print("No se encontró un modelo entrenado. Se usará un modelo por defecto.")
                self.modelo = DecisionTreeClassifier()
        except Exception as e:
            print(f"Error al cargar el modelo: {e}")
            self.modelo = DecisionTreeClassifier()
    
    def obtener_datos_entrenamiento(self):
        """Obtiene los datos para entrenar el modelo desde la base de datos"""
        try:
            # Esta es una consulta simplificada. En la implementación real, 
            # necesitarías una consulta más compleja que una todos los datos necesarios.
            estudiantes = db.session.query(
                Estudiante.id_estudiante,
                Estudiante.promedio,
                HistorialAcademico.calificacion_final,
                CorteEvaluacion.asistencia_corte,
                RiesgoSocioeconomico.nivel_ingreso,
                RiesgoSocioeconomico.acceso_becas,
                Desercion.riesgo_desercion
            ).join(
                HistorialAcademico, HistorialAcademico.id_estudiante == Estudiante.id_estudiante
            ).join(
                CorteEvaluacion, CorteEvaluacion.id_historial == HistorialAcademico.id_historial
            ).join(
                RiesgoSocioeconomico, RiesgoSocioeconomico.id_estudiante == Estudiante.id_estudiante
            ).join(
                Desercion, Desercion.id_estudiante == Estudiante.id_estudiante
            ).all()
            
            # Convertir a DataFrame
            df = pd.DataFrame(estudiantes, columns=[
                'id_estudiante', 'promedio', 'calificacion_final', 'asistencia_corte',
                'nivel_ingreso', 'acceso_becas', 'riesgo_desercion'
            ])
            
            # Preprocesamiento básico
            # Convertir 'nivel_ingreso' a numérico (bajo=1, medio=2, alto=3)
            df['nivel_ingreso_num'] = df['nivel_ingreso'].map({'bajo': 1, 'medio': 2, 'alto': 3})
            
            # Crear variable objetivo (1 si riesgo_desercion > 0.5, 0 en caso contrario)
            df['desercion'] = (df['riesgo_desercion'] > 0.5).astype(int)
            
            # Seleccionar features para entrenamiento
            X = df[['promedio', 'calificacion_final', 'asistencia_corte', 'nivel_ingreso_num', 'acceso_becas']]
            y = df['desercion']
            
            return X, y
        except Exception as e:
            print(f"Error al obtener datos para entrenamiento: {e}")
            return None, None
    
    def entrenar_modelo(self):
        """Entrena el modelo con los datos actuales de la base de datos"""
        X, y = self.obtener_datos_entrenamiento()
        
        if X is None or len(X) < 10:  # Verificar si hay suficientes datos
            print("No hay suficientes datos para entrenar el modelo")
            return False
        
        try:
            # Dividir datos en entrenamiento y prueba
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
            
            # Crear y entrenar el modelo
            modelo = DecisionTreeClassifier(
                criterion='entropy',  # Algoritmo C4.5 usa ganancia de información (entropy)
                max_depth=10,  # Evitar sobreajuste
                min_samples_split=5,
                min_samples_leaf=2
            )
            
            modelo.fit(X_train, y_train)
            
            # Evaluar el modelo
            y_pred = modelo.predict(X_test)
            precision = accuracy_score(y_test, y_pred)
            print(f"Precisión del modelo: {precision:.4f}")
            print(classification_report(y_test, y_pred))
            
            # Guardar el modelo
            self.modelo = modelo
            with open(self.ruta_modelo, 'wb') as archivo:
                pickle.dump(modelo, archivo)
            
            print(f"Modelo entrenado y guardado en {self.ruta_modelo}")
            return True
        
        except Exception as e:
            print(f"Error al entrenar el modelo: {e}")
            return False
    
    def predecir_riesgo(self, datos_estudiante):
        """
        Predice el riesgo de deserción para un estudiante
        
        :param datos_estudiante: diccionario con los datos del estudiante
        :return: probabilidad de deserción (entre 0 y 1)
        """
        try:
            # Preparar los datos en el formato correcto
            features = np.array([
                datos_estudiante.get('promedio', 0),
                datos_estudiante.get('calificacion_final', 0),
                datos_estudiante.get('asistencia_corte', 0),
                datos_estudiante.get('nivel_ingreso_num', 2),  # valor por defecto medio (2)
                datos_estudiante.get('acceso_becas', 0)
            ]).reshape(1, -1)
            
            # Verificar si hay un modelo cargado
            if self.modelo is None:
                self.cargar_modelo()
                
            # Realizar la predicción
            if hasattr(self.modelo, 'predict_proba'):
                # Si el modelo puede dar probabilidades
                proba = self.modelo.predict_proba(features)[0][1]  # probabilidad de clase 1 (deserción)
                return float(proba)
            else:
                # Si solo puede hacer clasificación binaria
                pred = self.modelo.predict(features)[0]
                return float(pred)
                
        except Exception as e:
            print(f"Error al realizar la predicción: {e}")
            return 0.5  # Valor por defecto en caso de error
    
    def guardar_prediccion(self, id_estudiante, riesgo, factores):
        """
        Guarda la predicción en la base de datos
        
        :param id_estudiante: ID del estudiante
        :param riesgo: valor numérico de riesgo (entre 0 y 1)
        :param factores: texto con factores que contribuyen al riesgo
        """
        try:
            # Verificar si ya existe una predicción para este estudiante
            desercion_existente = Desercion.query.filter_by(id_estudiante=id_estudiante).first()
            
            if desercion_existente:
                # Actualizar predicción existente
                desercion_existente.riesgo_desercion = riesgo
                desercion_existente.factores_riesgo = factores
                desercion_existente.fecha_analisis = datetime.now().date()
            else:
                # Crear nueva predicción
                nueva_desercion = Desercion(
                    id_estudiante=id_estudiante,
                    id_riesgo=1,  # Este valor debería obtenerse correctamente
                    id_formulario=1,  # Este valor debería obtenerse correctamente
                    riesgo_desercion=riesgo,
                    factores_riesgo=factores,
                    fecha_analisis=datetime.now().date()
                )
                db.session.add(nueva_desercion)
            
            db.session.commit()
            return True
            
        except Exception as e:
            print(f"Error al guardar la predicción: {e}")
            db.session.rollback()
            return False