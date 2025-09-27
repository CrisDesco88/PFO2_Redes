# Servidor API Flask para Gestión de Tareas

Este proyecto es un servidor API desarrollado en Flask que permite el registro de usuarios, inicio de sesión y visualización de una página de bienvenida para tareas.

## Funcionalidades

- **Registro de Usuarios**: Endpoint POST /registro para crear cuentas con contraseñas hasheadas.
- **Inicio de Sesión**: Endpoint POST /login para verificar credenciales.
- **Gestión de Tareas**: Endpoint GET /tareas que muestra una página HTML de bienvenida.
- **Página Estática**: Endpoint GET / para una página de introducción (útil para Github Pages).

## Requisitos Técnicos

- Python 3.x
- Librerías: Flask, Werkzeug (incluido con Flask)
- Base de datos: SQLite (integrada en Python)

## Instalación

1. Asegúrate de tener Python instalado.
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución

1. Navega a la carpeta del proyecto (PFO2).
2. Ejecuta el servidor:
   ```bash
   python servidor.py
   ```
3. El servidor correrá en `http://127.0.0.1:5000/` por defecto.

## Pruebas

El proyecto incluye una suite de pruebas automatizadas usando pytest.

1. Instala pytest si no está incluido:
   ```bash
   pip install pytest
   ```

2. Ejecuta las pruebas:
   ```bash
   pytest test_servidor.py
   ```

Las pruebas cubren:
- Registro de usuarios (éxito, duplicado, datos faltantes)
- Inicio de sesión (éxito, fallo, datos faltantes)
- Endpoints GET para tareas e index

## Endpoints

### POST /registro
Registra un nuevo usuario.

- **Request Body** (JSON):
  ```json
  {
    "usuario": "ejemplo",
    "contraseña": "1234"
  }
  ```
- **Respuesta Exitosa** (201):
  ```json
  {
    "mensaje": "Usuario registrado exitosamente"
  }
  ```
- **Errores**:
  - 400: Datos faltantes
  - 409: Usuario ya existe

### POST /login
Verifica credenciales de usuario.

- **Request Body** (JSON):
  ```json
  {
    "usuario": "ejemplo",
    "contraseña": "1234"
  }
  ```
- **Respuesta Exitosa** (200):
  ```json
  {
    "mensaje": "Inicio de sesión exitoso"
  }
  ```
- **Error** (401): Credenciales inválidas

### GET /tareas
Muestra una página HTML de bienvenida (requiere sesión iniciada conceptualmente, pero no implementado en este endpoint).

- **Respuesta**: HTML con página de bienvenida.

### GET /
Página estática de introducción.

- **Respuesta**: HTML simple.

## Pruebas

Usa herramientas como Postman, curl o un navegador para probar los endpoints.

Ejemplos con curl:

- Registro:
  ```bash
  curl -X POST http://127.0.0.1:5000/registro -H "Content-Type: application/json" -d '{"usuario":"test","contraseña":"pass"}'
  ```

- Login:
  ```bash
  curl -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d '{"usuario":"test","contraseña":"pass"}'
  ```

- Tareas:
  Abre en navegador: `http://127.0.0.1:5000/tareas`

- Página raíz:
  Abre en navegador: `http://127.0.0.1:5000/`



Nota: Github Pages aloja contenido estático; la API Flask debe ejecutarse localmente o en un servidor compatible con Python.