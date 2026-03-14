# Sistema de Gestión de Libros — Backend

API REST desarrollada con **FastAPI** y **PostgreSQL**.  
Autora: Sol Andriani · 2025

---

## Tecnologías

- Python 3.10+
- FastAPI
- PostgreSQL
- SQLAlchemy (ORM)
- Pydantic (validación)
- bcrypt (hashing de contraseñas)
- JWT (autenticación)

---

## Requisitos previos

- Python 3.10 o superior instalado
- PostgreSQL instalado y corriendo
- Git

---

## Instalación y ejecución local

### 1. Clonar el repositorio

git clone https://github.com/SolAndriani/sistema-libros-backend
cd sistema-libros-backend

### 2. Crear y activar el entorno virtual

# Crear
python -m venv venv

# Activar en Windows
venv\Scripts\activate

# Activar en Mac/Linux
source venv/bin/activate

### 3. Instalar dependencias

pip install -r requirements.txt

### 4. Configurar variables de entorno

cp .env.example .env

Editar .env con tus datos de PostgreSQL.

### 5. Crear la base de datos en PostgreSQL

Abrir psql o pgAdmin y ejecutar:

CREATE DATABASE sistema_libros;

Las tablas se crean automáticamente al iniciar la aplicación.

### 6. Iniciar el servidor

uvicorn app.main:app --reload

El servidor queda disponible en: http://localhost:8000
La documentación de la API: http://localhost:8000/docs

---

## Variables de entorno

DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/sistema_libros
SECRET_KEY=tu_clave_secreta_aqui

---

## Estructura del proyecto

app/
├── main.py         # Rutas y endpoints
├── models.py       # Modelos de base de datos (SQLAlchemy)
├── schemas.py      # Validación de datos (Pydantic)
├── crud.py         # Operaciones CRUD
├── auth.py         # Verificación de token JWT
├── security.py     # Hashing y generación de tokens
└── database.py     # Conexión a la base de datos

---

## Endpoints principales

| Método | Ruta | Descripción | Autenticación |
|--------|------|-------------|---------------|
| POST | /register | Registrar usuario | No |
| POST | /login | Iniciar sesión | No |
| GET | /books | Listar libros del usuario | Sí |
| POST | /books | Crear libro | Sí |
| PUT | /books/{id} | Editar libro | Sí |
| DELETE | /books/{id} | Eliminar libro | Sí |
```

---

## .env.example backend

Creá un archivo llamado `.env.example` en la carpeta del backend y pegá esto:
```
# Copiar este archivo como .env y completar los valores

# Cadena de conexión a PostgreSQL
# Formato: postgresql://usuario:contraseña@host:puerto/nombre_base_de_datos
DATABASE_URL=postgresql://postgres:tu_contraseña@localhost:5432/sistema_libros

# Clave secreta para firmar los tokens JWT
# Puede ser cualquier cadena larga y aleatoria
SECRET_KEY=cambia_esto_por_una_clave_segura_y_larga
```

---

## .env.example frontend

Creá un archivo llamado `.env.example` en la carpeta del frontend y pegá esto:
```
# Copiar este archivo como .env y completar los valores

# URL base del backend
# En local, el backend corre en el puerto 8000
VITE_API_URL=http://localhost:8000