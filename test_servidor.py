import pytest
import os
from servidor import app, init_db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['DATABASE'] = 'test.db'
    with app.test_client() as client:
        with app.app_context():
            init_db()  # Crea la tabla
        yield client
    # Limpiar DB de prueba
    if os.path.exists('test.db'):
        os.remove('test.db')

def test_registro_exitoso(client):
    response = client.post('/registro', json={'usuario': 'testuser', 'contraseña': 'testpass'})
    assert response.status_code == 201
    data = response.get_json()
    assert 'mensaje' in data
    assert 'Usuario registrado exitosamente' in data['mensaje']

def test_registro_usuario_duplicado(client):
    client.post('/registro', json={'usuario': 'testuser', 'contraseña': 'testpass'})
    response = client.post('/registro', json={'usuario': 'testuser', 'contraseña': 'otherpass'})
    assert response.status_code == 409
    data = response.get_json()
    assert 'error' in data
    assert 'ya existe' in data['error']

def test_registro_datos_faltantes(client):
    response = client.post('/registro', json={'usuario': 'testuser'})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_registro_campos_vacios(client):
    response = client.post('/registro', json={'usuario': '', 'contraseña': '123'})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'no pueden estar vacíos' in data['error']

    response = client.post('/registro', json={'usuario': 'test', 'contraseña': ''})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_login_exitoso(client):
    client.post('/registro', json={'usuario': 'testuser', 'contraseña': 'testpass'})
    response = client.post('/login', json={'usuario': 'testuser', 'contraseña': 'testpass'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'mensaje' in data
    assert 'Inicio de sesión exitoso' in data['mensaje']

def test_login_fallido_credenciales_invalidas(client):
    response = client.post('/login', json={'usuario': 'nonexistent', 'contraseña': 'wrong'})
    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data
    assert 'Credenciales inválidas' in data['error']

def test_login_datos_faltantes(client):
    response = client.post('/login', json={'usuario': 'testuser'})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_tareas(client):
    response = client.get('/tareas')
    assert response.status_code == 200
    assert b'Bienvenido a tu Gestor de Tareas' in response.data

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Servidor API de Gesti' in response.data