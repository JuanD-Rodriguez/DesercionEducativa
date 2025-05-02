# Archivo: app/models/ingenieria.py (corregido)
from app import db

class Ingenieria(db.Model):
    __tablename__ = 'ingenieria'
    id_ingenieria = db.Column(db.Integer, primary_key=True)
    nombre_ingenieria = db.Column(db.String(50), nullable=False)
    
    estudiantes = db.relationship('Estudiante', back_populates='ingenieria')

