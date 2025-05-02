# setup_admin.py
from app import create_app, db
from app.models.usuario import Usuario
from werkzeug.security import generate_password_hash

def crear_o_actualizar_admin():
    app = create_app()
    with app.app_context():
        admin = Usuario.query.filter_by(Nombre_Usuario='admin').first()
        if not admin:
            admin = Usuario(
                Nombre_Usuario='admin',
                Contrasena=generate_password_hash('admin123'),
                ID_Rol=1
            )
            db.session.add(admin)
            print("[✔] Usuario admin creado con éxito.")
        else:
            admin.Contrasena = generate_password_hash('admin123')
            print("[✔] Contraseña del usuario admin actualizada.")
        db.session.commit()

if __name__ == '__main__':
    crear_o_actualizar_admin()

#ejecutar esto en el contenedor docker exec -it flask-backend python setup_admin.py
