# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os

# Inicializar extensiones
db = SQLAlchemy()
jwt = JWTManager()

def create_app(config=None):
    """Crea y configura la aplicación Flask"""
    app = Flask(__name__)

    # Configuración básica
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'clave-secreta-desarrollo')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'mysql+mysqlconnector://flask_user:flaskpass@mysql:3306/desercion_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-clave-secreta-desarrollo')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=8)

    if config:
        app.config.update(config)

    db.init_app(app)
    jwt.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*"}}, methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], allow_headers=["Content-Type", "Authorization"])

    with app.app_context():
        from app.routes.main import main
        from app.routes.auth import auth_bp
        from app.routes.usuarios import usuarios_bp
        from app.routes.cursos import cursos_bp
        from app.routes.cortes import cortes_bp
        # from app.routes.comunicacion import comunicacion_bp
        from app.routes.reportes import reportes_bp
        from app.routes.formulario import formulario_bp
        from app.routes.prediccion import prediccion_bp
        from app.routes.talend_integration import talend_bp

        app.register_blueprint(main, url_prefix='/')
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
        app.register_blueprint(cursos_bp, url_prefix='/cursos')
        app.register_blueprint(cortes_bp, url_prefix='/cortes')
        # app.register_blueprint(comunicacion_bp, url_prefix='/comunicacion')
        app.register_blueprint(reportes_bp, url_prefix='/reportes')
        app.register_blueprint(formulario_bp, url_prefix='/formulario')
        app.register_blueprint(prediccion_bp, url_prefix='/prediccion')
        app.register_blueprint(talend_bp, url_prefix='/talend')

        db.create_all()

        from app.models.rol import Rol
        from app.models.usuario import Usuario
        from app.models.gestor import Gestor
        from werkzeug.security import generate_password_hash

        admin_role = Rol.query.filter_by(id_rol=1).first()
        if not admin_role:
            admin_role = Rol(id_rol=1, nombre="Administrador")
            db.session.add(admin_role)

        gestor_role = Rol.query.filter_by(id_rol=2).first()
        if not gestor_role:
            gestor_role = Rol(id_rol=2, nombre="Gestor")
            db.session.add(gestor_role)

        estudiante_role = Rol.query.filter_by(id_rol=3).first()
        if not estudiante_role:
            estudiante_role = Rol(id_rol=3, nombre="Estudiante")
            db.session.add(estudiante_role)

        admin_user = Usuario.query.filter_by(nombre_usuario="admin").first()
        if not admin_user:
            admin_user = Usuario(
                nombre_usuario="admin",
                contrasena=generate_password_hash("admin123"),
                id_rol=1
            )
            db.session.add(admin_user)
            print("[✔] Usuario admin creado con éxito.")
        else:
            admin_user.contrasena = generate_password_hash("admin123")
            print("[✔] Contraseña del usuario admin actualizada.")

        gestor_user = Usuario.query.filter_by(nombre_usuario="gestor1").first()
        if not gestor_user:
            gestor_user = Usuario(
                nombre_usuario="gestor1",
                contrasena=generate_password_hash("gestor123"),
                id_rol=2
            )
            db.session.add(gestor_user)
            db.session.flush()

            nuevo_gestor = Gestor(
                nombre='Gestor',
                apellido='Uno',
                id_usuario=gestor_user.id_usuario
            )
            db.session.add(nuevo_gestor)
            print("[✔] Usuario gestor1 y perfil Gestor creado con éxito.")
        else:
            gestor_user.contrasena = generate_password_hash("gestor123")
            print("[✔] Contraseña del usuario gestor1 actualizada.")

        db.session.commit()

    return app