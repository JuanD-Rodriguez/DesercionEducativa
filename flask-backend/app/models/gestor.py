# Archivo: app/models/gestor.py (corregido)
from app import db

class Gestor(db.Model):
    __tablename__ = 'gestor'
    id_gestor = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))

    usuario = db.relationship('Usuario', back_populates='gestor')
    formularios = db.relationship('FormularioDesercion', back_populates='gestor')
