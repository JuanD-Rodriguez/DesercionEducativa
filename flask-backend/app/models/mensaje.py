
# Archivo: app/models/mensaje.py (corregido)
from app import db
from datetime import datetime

class Mensaje(db.Model):
    __tablename__ = 'mensaje'
    id_mensaje = db.Column(db.Integer, primary_key=True)
    id_remitente = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    id_destinatario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    asunto = db.Column(db.String(100), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha_envio = db.Column(db.DateTime, default=datetime.now)
    leido = db.Column(db.Boolean, default=False)
    
    remitente = db.relationship('Usuario', foreign_keys=[id_remitente], backref='mensajes_enviados')
    destinatario = db.relationship('Usuario', foreign_keys=[id_destinatario], backref='mensajes_recibidos')
