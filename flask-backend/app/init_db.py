# Dentro del contenedor de flask-backend
from app import create_app, db
from app.models.rol import Rol
from app.models.usuario import Usuario
from app.models.estudiante import Estudiante
from app.models.curso import Curso
from app.models.historial_academico import HistorialAcademico
from app.models.gestor import Gestor
from app.models.admin import Admin
from app.models.ingenieria import Ingenieria
from app.models.formulario_desercion import FormularioDesercion
from app.models.pregunta import Pregunta
from app.models.respuesta import Respuesta
from app.models.corte_evaluacion import CorteEvaluacion
from app.models.riesgo_socioeconomico import RiesgoSocioeconomico
from app.models.desercion import Desercion
from app.models.mensaje import Mensaje

app = create_app()

with app.app_context():
    print("Creando todas las tablas...")
    db.create_all()
    
    # Crear rol de administrador
    print("Creando rol de administrador...")
    admin_role = Rol(id_rol=1, nombre="Administrador")
    db.session.add(admin_role)
    
    # Crear usuario admin
    print("Creando usuario administrador...")
    admin_user = Usuario(
        id_usuario=1,
        nombre_usuario="admin",
        contrasena="admin123",
        id_rol=1
    )
    db.session.add(admin_user)
    
    # Crear un rol de gestor
    print("Creando rol de gestor...")
    gestor_role = Rol(id_rol=2, nombre="Gestor")
    db.session.add(gestor_role)
    
    # Crear rol de estudiante
    print("Creando rol de estudiante...")
    estudiante_role = Rol(id_rol=3, nombre="Estudiante")
    db.session.add(estudiante_role)
    
    # Crear una ingeniería
    print("Creando ingeniería de ejemplo...")
    ingenieria = Ingenieria(id_ingenieria=1, nombre_ingenieria="Ingeniería de Sistemas")
    db.session.add(ingenieria)
    
    db.session.commit()
    print("Inicialización completada!")
