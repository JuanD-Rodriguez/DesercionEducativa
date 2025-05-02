# Archivo: app/models/corte_evaluacion.py (corregido)
from app import db

class CorteEvaluacion(db.Model):
    __tablename__ = 'corte_evaluacion'

    id_corte = db.Column(db.Integer, primary_key=True)
    id_historial = db.Column(db.Integer, db.ForeignKey('historial_academico.id_historial'), nullable=False)
    id_curso = db.Column(db.Integer, db.ForeignKey('curso.id_curso'), nullable=False)
    numero_corte = db.Column(db.Integer)
    calificacion_corte = db.Column(db.Numeric)
    asistencia_corte = db.Column(db.Numeric)

    historial = db.relationship('HistorialAcademico', back_populates='cortes')
    curso = db.relationship('Curso')