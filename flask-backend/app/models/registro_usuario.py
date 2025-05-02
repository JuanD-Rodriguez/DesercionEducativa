# Archivo: app/models/registro_usuario.py (corregido)
from app import db

class RegistroUsuario(db.Model):
    __tablename__ = 'registro_usuario'

    id_registro = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(20))
    id_ingenieria = db.Column(db.Integer, db.ForeignKey('ingenieria.id_ingenieria'), nullable=False)
    fecha_registro = db.Column(db.Date)

    usuario = db.relationship('Usuario', backref='registro')
    ingenieria = db.relationship('Ingenieria')
