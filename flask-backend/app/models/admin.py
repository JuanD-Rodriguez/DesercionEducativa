# Archivo: app/models/admin.py (corregido)
from app import db

class Admin(db.Model):
    __tablename__ = 'admin'
    id_admin = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    nombre = db.Column(db.String(50))
    apellido = db.Column(db.String(50))
    telefono = db.Column(db.String(15))

    usuario = db.relationship('Usuario', back_populates='admin')