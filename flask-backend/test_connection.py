import pymysql
import json

# Configuración de conexión directa
config = {
    'host': 'mysql',
    'user': 'flask_user',
    'password': 'flaskpass',
    'database': 'desercion_db',
    'port': 3306,
    'cursorclass': pymysql.cursors.DictCursor
}

def main():
    try:
        # Conectar directamente
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        
        # Consulta usuarios
        cursor.execute("SELECT * FROM usuario")
        usuarios = cursor.fetchall()
        print(f"Usuarios encontrados: {len(usuarios)}")
        print(json.dumps(usuarios, indent=2))
        
        # Intentar login
        username = 'admin'
        password = 'admin123'
        cursor.execute("SELECT * FROM usuario WHERE nombre_usuario = %s", (username,))
        user = cursor.fetchone()
        
        if user:
            print(f"Usuario encontrado: {user}")
            if password == user['contrasena']:
                print("¡Autenticación exitosa!")
            else:
                print(f"Contraseña incorrecta. Esperada: {user['contrasena']}, Recibida: {password}")
        else:
            print("Usuario no encontrado")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()