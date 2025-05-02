# Archivo: app/models/estudiante.py (corregido)
from app import db

class Estudiante(db.Model):
    __tablename__ = 'estudiante'
    id_estudiante = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    correo_electronico = db.Column(db.String(100), nullable=False)
    id_ingenieria = db.Column(db.Integer, db.ForeignKey('ingenieria.id_ingenieria'), nullable=False)
    promedio = db.Column(db.Float, default=0)
    fecha_registro = db.Column(db.Date)

    usuario = db.relationship('Usuario', back_populates='estudiante')
    ingenieria = db.relationship('Ingenieria', back_populates='estudiantes')
    historiales = db.relationship('HistorialAcademico', back_populates='estudiante')
    deserciones = db.relationship('Desercion', back_populates='estudiante')
    riesgos = db.relationship('RiesgoSocioeconomico', back_populates='estudiante')
    respuestas = db.relationship('Respuesta', back_populates='estudiante')
