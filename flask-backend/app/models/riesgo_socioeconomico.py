# Archivo: app/models/riesgo_socioeconomico.py (corregido)
from app import db

class RiesgoSocioeconomico(db.Model):
    __tablename__ = 'riesgo_socioeconomico'
    id_riesgo = db.Column(db.Integer, primary_key=True)
    id_estudiante = db.Column(db.Integer, db.ForeignKey('estudiante.id_estudiante'), nullable=False)
    nivel_ingreso = db.Column(db.String(100))
    situacion_vivienda = db.Column(db.String(50))
    dependencia_economica = db.Column(db.Integer)
    acceso_becas = db.Column(db.Boolean)
    nivel_educativo_padres = db.Column(db.String(50))
    situacion_laboral = db.Column(db.String(50))

    estudiante = db.relationship('Estudiante', back_populates='riesgos')
    deserciones = db.relationship('Desercion', back_populates='riesgo')