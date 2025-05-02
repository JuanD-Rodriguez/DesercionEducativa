# Archivo: app/models/usuario.py (corregido)
from app import db

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    id_rol = db.Column(db.Integer, db.ForeignKey('rol.id_rol'), nullable=False)

    # Relaciones
    rol = db.relationship('Rol', back_populates='usuarios')
    estudiante = db.relationship('Estudiante', back_populates='usuario', uselist=False)
    gestor = db.relationship('Gestor', back_populates='usuario', uselist=False)
    admin = db.relationship('Admin', back_populates='usuario', uselist=False)
    # Mensajes ya están referenciados usando backref

    def __repr__(self):
        return f'<Usuario {self.nombre_usuario}>'