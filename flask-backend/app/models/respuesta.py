# Archivo: app/models/respuesta.py (corregido)
from app import db

class Respuesta(db.Model):
    __tablename__ = 'respuesta'
    id_respuesta = db.Column(db.Integer, primary_key=True)
    id_pregunta = db.Column(db.Integer, db.ForeignKey('pregunta.id_pregunta'), nullable=False)
    id_estudiante = db.Column(db.Integer, db.ForeignKey('estudiante.id_estudiante'), nullable=False)
    opcion_seleccionada = db.Column(db.String(100))
    fecha_respuesta = db.Column(db.Date)

    pregunta = db.relationship('Pregunta', back_populates='respuestas')
    estudiante = db.relationship('Estudiante', back_populates='respuestas')
