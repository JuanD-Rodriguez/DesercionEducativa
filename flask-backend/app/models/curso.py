# Archivo: app/models/curso.py (corregido)
from app import db

class Curso(db.Model):
    __tablename__ = 'curso'
    id_curso = db.Column(db.Integer, primary_key=True)
    curso = db.Column(db.String(100))
    creditos = db.Column(db.Integer)

    # Relación para historial académico
    historiales = db.relationship('HistorialAcademico', back_populates='curso')