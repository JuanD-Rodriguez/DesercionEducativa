# Archivo: app/models/formulario_desercion.py (corregido)
from app import db
from datetime import datetime

class FormularioDesercion(db.Model):
    __tablename__ = 'formulario_desercion'

    id_formulario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(150), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now, nullable=False)
    id_gestor = db.Column(db.Integer, db.ForeignKey('gestor.id_gestor'), nullable=False)
    activo = db.Column(db.Boolean, default=True)  # Nueva columna

    preguntas = db.relationship('Pregunta', back_populates='formulario', lazy=True)
    gestor = db.relationship('Gestor', back_populates='formularios')
    deserciones = db.relationship('Desercion', back_populates='formulario')