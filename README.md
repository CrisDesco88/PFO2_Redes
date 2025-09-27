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


## ¿Por qué hashear contraseñas? 🔐

Hashear contraseñas es una práctica **esencial de seguridad** en el desarrollo de aplicaciones que manejan autenticación de usuarios. A continuación, las razones principales:

### 1. **Protección contra Brechas de Seguridad** 🛡️
   - Si un atacante accede a la base de datos, las contraseñas hasheadas **no se pueden leer directamente**. Un hash es una representación irreversible de la contraseña (ej. `pbkdf2:sha256:260000$...` generado por Werkzeug).
   - Sin hashear, si alguien roba la DB, tendría todas las contraseñas en texto plano y podría usarlas en otros sitios (**ataque de credential stuffing**).

### 2. **Función de Un Solo Sentido** 🔒
   - Los algoritmos de hash (como SHA-256 o PBKDF2) son **unidireccionales**: conviertes una contraseña en hash, pero no al revés. Durante el login, se hashea la entrada y se compara con el almacenado.
   - Previene que incluso administradores vean las contraseñas reales.

### 3. **Prevención de Ataques por Fuerza Bruta y Rainbow Tables** ⚡
   - Hashes con **"salt"** (valor aleatorio) dificultan ataques precomputados. `werkzeug.security.generate_password_hash` incluye salt automáticamente.
   - Ataques como rainbow tables (tablas precomputadas) se vuelven ineficientes.

### 4. **Cumplimiento con Estándares de Seguridad** 📜
   - Es un estándar en la industria (OWASP, NIST). No almacenar contraseñas en texto plano es **inseguro** y puede violar leyes como GDPR o leyes de protección de datos.

## Ventajas de Usar SQLite en Este Proyecto 💾

SQLite es una **excelente elección** para este proyecto de servidor API Flask pequeño. Sus ventajas incluyen:

### 1. **Simplicidad y Facilidad de Uso** 🛠️
   - **No requiere servidor** separado (como MySQL o PostgreSQL). Es un archivo único (`.db`) que se crea automáticamente.
   - **Zero configuración**: solo `import sqlite3` en Python. Ideal para prototipos o proyectos pequeños.

### 2. **Portabilidad y Despliegue Fácil** 🚀
   - Todo en un archivo: fácil de copiar o versionar en Git. Sin dependencias externas.
   - Perfecto para despliegue en Heroku, Railway o local, sin configurar un DB server.

### 3. **Rendimiento para Cargas Pequeñas** 📈
   - Para pocos usuarios (como esta API), es **rápido y eficiente**. Maneja lecturas/escrituras concurrentes básicas.
   - **ACID compliant**: garantiza integridad (Atomicidad, Consistencia, Aislamiento, Durabilidad).

### 4. **Integración Nativa con Python** 🐍
   - Incluido en Python estándar (`import sqlite3`), sin librerías extras.
   - ORM opcional: usa SQLAlchemy si crece, pero queries directas bastan aquí.

### 5. **Bajo Overhead** ⚡
   - No consume recursos como un DB server. Útil para apps embebidas o bajo tráfico.
   - **Tamaño pequeño**: el archivo DB crece solo con datos.