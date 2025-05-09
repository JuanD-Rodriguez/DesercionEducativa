from app import create_app, db
from app.models.usuario import Usuario
from app.models.gestor import Gestor
from werkzeug.security import generate_password_hash

def crear_o_actualizar_admin_y_gestor():
    app = create_app()
    with app.app_context():

        # ---------- ADMIN ----------
        admin = Usuario.query.filter_by(nombre_usuario='admin').first()
        if not admin:
            admin = Usuario(
                nombre_usuario='admin',
                contrasena=generate_password_hash('admin123'),
                id_rol=1
            )
            db.session.add(admin)
            print("[✔] Usuario admin creado con éxito.")
        else:
            admin.contrasena = generate_password_hash('admin123')
            print("[✔] Contraseña del usuario admin actualizada.")

        # ---------- GESTOR ----------
        gestor = Usuario.query.filter_by(nombre_usuario='gestor1').first()
        if not gestor:
            gestor = Usuario(
                nombre_usuario='gestor1',
                contrasena=generate_password_hash('gestor123'),
                id_rol=2
            )
            db.session.add(gestor)
            db.session.flush()

            nuevo_gestor = Gestor(
                nombre='Gestor',
                apellido='Uno',
                id_usuario=gestor.id_usuario
            )
            db.session.add(nuevo_gestor)
            print("[✔] Usuario gestor1 y perfil de Gestor creado con éxito.")
        else:
            gestor.contrasena = generate_password_hash('gestor123')
            print("[✔] Contraseña del usuario gestor1 actualizada.")

        db.session.commit()

if __name__ == '__main__':
    crear_o_actualizar_admin_y_gestor()
