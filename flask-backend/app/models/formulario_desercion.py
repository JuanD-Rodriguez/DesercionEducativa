# app/models/formulario_desercion.py
from app import db
from datetime import datetime
from sqlalchemy.dialects.mysql import JSON

class FormularioDesercion(db.Model):
    __tablename__ = 'formulario_desercion'

    id_formulario = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, default='')
    estructura_json = db.Column(JSON, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
