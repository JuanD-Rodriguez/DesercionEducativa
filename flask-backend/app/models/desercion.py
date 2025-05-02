# Archivo: app/models/desercion.py (corregido)
from app import db

class Desercion(db.Model):
    __tablename__ = 'desercion'
    id_desercion = db.Column(db.Integer, primary_key=True)
    id_estudiante = db.Column(db.Integer, db.ForeignKey('estudiante.id_estudiante'), nullable=False)
    id_riesgo = db.Column(db.Integer, db.ForeignKey('riesgo_socioeconomico.id_riesgo'), nullable=False)
    id_formulario = db.Column(db.Integer, db.ForeignKey('formulario_desercion.id_formulario'), nullable=False)
    riesgo_desercion = db.Column(db.Numeric)
    factores_riesgo = db.Column(db.Text)
    fecha_analisis = db.Column(db.Date)

    estudiante = db.relationship('Estudiante', back_populates='deserciones')
    riesgo = db.relationship('RiesgoSocioeconomico')
    formulario = db.relationship('FormularioDesercion')
