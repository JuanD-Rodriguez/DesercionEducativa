# Archivo: app/models/pregunta.py (corregido)
from app import db

class Pregunta(db.Model):
    __tablename__ = 'pregunta'
    id_pregunta = db.Column(db.Integer, primary_key=True)
    id_formulario = db.Column(db.Integer, db.ForeignKey('formulario_desercion.id_formulario'), nullable=False)
    texto_pregunta = db.Column(db.String(255))
    categoria = db.Column(db.String(50))

    formulario = db.relationship('FormularioDesercion', back_populates='preguntas')
    respuestas = db.relationship('Respuesta', back_populates='pregunta')