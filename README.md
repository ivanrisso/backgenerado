# Backend de Facturación 🧾

Backend desarrollado con **FasAPI**, **SQLAlchemy (Async)**, **Pydantic v2** y arquitectura limpia (Clean Architecture).

## 📋 Requisitos Previos

- Python 3.11+
- [Poetry](https://python-poetry.org/docs/) (Gestor de dependencias)
- Servidor de Base de Datos (MySQL / MariaDB compatible)

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd backendfacturacion
```

### 2. Instalar dependencias
Usando Poetry:
```bash
poetry install
```

### 3. Configurar Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto. Puedes usar el siguiente template:

```ini
# .env

# Base de Datos (Formato: driver+async_driver://user:pass@host:port/dbname)
DATABASE_URL="mysql+aiomysql://usuario:password@localhost:3306/facturacion_db"

# Seguridad JWT
JWT_SECRET_KEY="tu_super_secreto_aqui_generalo_con_openssl_rand_hex_32"
JWT_ALGORITHM="HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Configuración AFIP
AFIP_CERT_CRT_PATH="/path/absoluto/a/certificado.crt"
AFIP_KEY_CRT_PATH="/path/absoluto/a/private.key"
AFIP_CUIT=20123456789
AFIP_ENVIRONMENT="production" # o "testing"
```

> **Nota**: Asegúrate de tener los certificados de AFIP en la ruta especificada.

## 🛠️ Ejecución

Para levantar el servidor de desarrollo (con hot-reload):

```bash
poetry run uvicorn app.main:app --reload
```
O si activaste el entorno virtual:
```bash
# Para Poetry 2.0+
poetry env activate
# (Luego de ejecutar el comando que te devuelve)
uvicorn app.main:app --reload
```
*Si usas una versión anterior de Poetry, puedes usar `poetry shell`.*
El servidor correrá en `http://localhost:8000`.

Documentación interactiva disponible en:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## 🐘 Gestión de Base de Datos con Alembic

El proyecto utiliza **Alembic** para las migraciones de base de datos.

### Comandos Comunes

#### 1. Crear una nueva migración (Generar cambios)
Cada vez que modifiques un modelo en `app/domain` o `app/infrastructure/db/orm_models.py`, debes generar una migración:

```bash
poetry run alembic revision --autogenerate -m "Descripción del cambio"
```
*Esto crea un archivo en `alembic/versions` con las instrucciones SQL.*

#### 2. Aplicar migraciones (Actualizar DB)
Para aplicar los cambios pendientes a la base de datos:

```bash
poetry run alembic upgrade head
```

#### 3. Revertir migraciones (Downgrade)
Para deshacer la última migración aplicada:

```bash
poetry run alembic downgrade -1
```

### Flujo de Trabajo Recomendado

1.  Hacer cambios en los modelos de SQLAlchemy.
2.  Ejecutar `alembic revision --autogenerate -m "..."`.
3.  Verificar el archivo generado en `alembic/versions/` (asegurarse que detectó los cambios correctamente).
4.  Ejecutar `alembic upgrade head` para impactar en tu DB local.
5.  Comitear tanto los cambios de código como el archivo de versión de Alembic.

---

## 🧪 Tests

*(Se recomienda implementar tests con pytest)*

```bash
poetry run pytest
```
