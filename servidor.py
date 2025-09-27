from flask import Flask, request, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Función para conectar a la base de datos
def get_db_connection():
    conn = sqlite3.connect('usuarios.db')
    conn.row_factory = sqlite3.Row
    return conn

# Crear tabla de usuarios si no existe
def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, usuario TEXT UNIQUE NOT NULL, contraseña_hash TEXT NOT NULL)')
    conn.commit()
    conn.close()

# Inicializar la base de datos al iniciar la app
init_db()

# Endpoint de registro
@app.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()
    if not data or 'usuario' not in data or 'contraseña' not in data:
        return jsonify({'error': 'Faltan datos: usuario y contraseña requeridos'}), 400

    usuario = data['usuario']
    contraseña = data['contraseña']

    # Hashear la contraseña
    contraseña_hash = generate_password_hash(contraseña)

    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO usuarios (usuario, contraseña_hash) VALUES (?, ?)', (usuario, contraseña_hash))
        conn.commit()
        conn.close()
        return jsonify({'mensaje': 'Usuario registrado exitosamente'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'El usuario ya existe'}), 409

# Endpoint de login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'usuario' not in data or 'contraseña' not in data:
        return jsonify({'error': 'Faltan datos: usuario y contraseña requeridos'}), 400

    usuario = data['usuario']
    contraseña = data['contraseña']

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM usuarios WHERE usuario = ?', (usuario,)).fetchone()
    conn.close()

    if user and check_password_hash(user['contraseña_hash'], contraseña):
        return jsonify({'mensaje': 'Inicio de sesión exitoso'}), 200
    else:
        return jsonify({'error': 'Credenciales inválidas'}), 401

# Endpoint de tareas (devuelve HTML de bienvenida)
@app.route('/tareas', methods=['GET'])
def tareas():
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bienvenido a la Gestión de Tareas</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
            h1 { color: #333; }
            p { color: #666; }
        </style>
    </head>
    <body>
        <h1>¡Bienvenido a tu Gestor de Tareas!</h1>
        <p>Has iniciado sesión exitosamente. Aquí puedes gestionar tus tareas.</p>
    </body>
    </html>
    """
    return html

# Endpoint raíz para servir HTML estático (para Github Pages)
@app.route('/', methods=['GET'])
def index():
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Servidor de Tareas</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
            h1 { color: #333; }
            p { color: #666; }
        </style>
    </head>
    <body>
        <h1>Servidor API de Gestión de Tareas</h1>
        <p>Usa los endpoints /registro, /login y /tareas para interactuar con la API.</p>
    </body>
    </html>
    """
    return html

if __name__ == '__main__':
    app.run(debug=True)