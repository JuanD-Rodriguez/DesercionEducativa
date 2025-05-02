# Archivo: app/models/historial_academico.py (corregido)
from app import db

class HistorialAcademico(db.Model):
    __tablename__ = 'historial_academico'

    id_historial = db.Column(db.Integer, primary_key=True)
    id_estudiante = db.Column(db.Integer, db.ForeignKey('estudiante.id_estudiante'), nullable=False)
    id_curso = db.Column(db.Integer, db.ForeignKey('curso.id_curso'), nullable=False)
    calificacion_final = db.Column(db.Numeric)
    fecha_finalizacion = db.Column(db.Date)

    estudiante = db.relationship('Estudiante', back_populates='historiales')
    curso = db.relationship('Curso', back_populates='historiales')
    cortes = db.relationship('CorteEvaluacion', back_populates='historial', lazy=True)
