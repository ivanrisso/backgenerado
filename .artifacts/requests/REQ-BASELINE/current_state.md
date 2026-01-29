# Estado Actual del Proyecto

## 1. Backend

### Stack Tecnológico
- **Lenguaje**: Python 3.11+
- **Framework Web**: FastAPI 0.111.0
- **Servidor WGI**: Uvicorn
- **Base de Datos**: MySQL 8.x (Connector: `mysql-connector-python`, `asyncmy`)
- **ORM**: SQLAlchemy 2.0+ (con soporte asíncrono)
- **Migraciones**: Alembic
- **Seguridad**: Passlib + Bcrypt (Hashing), PyJWT/Python-Jose (Tokens - inferred)
- **Integración Externa**: Zeep (SOAP Client) para servicios de AFIP (WSAA, WSFE)

### Estructura de Directorios (Clean Architecture)
- `/app/adapters`: Adaptadores para interfaces externas.
- `/app/core`: Configuración central, seguridad, logging.
- `/app/domain`: Entidades de negocio pura, excepciones, contratos de repositorio (Ports).
- `/app/infrastructure`: Implementación de base de datos, clientes externos (AFIP), seguridad concreta.
- `/app/repositories`: Implementaciones de repositorios.
- `/app/routes`: Endpoints de la API (Controllers).
- `/app/services`: Servicios de dominio o aplicación.
- `/app/use_cases`: Casos de uso de la aplicación (Interactors).
- `/app/schemas`: DTOs (Pydantic models) para entrada/salida de API.

### Configuración
- Gestión de dependencias: `Poetry` (`pyproject.toml`, `poetry.lock`).
- Variables de entorno: `.env` (cargado con `python-dotenv`).

## 2. Frontend

### Stack Tecnológico
- **Framework**: Vue.js 3.5+
- **Lenguaje**: TypeScript 5.9
- **Build Tool**: Vite 7.2
- **Estilos**: Tailwind CSS 4.x + PostCSS
- **Estado Global**: Pinia 3.0
- **Routing**: Vue Router 4.6
- **HTTP Client**: Axios
- **Visualización**: Chart.js + Vue-Chartjs

### Arquitectura
- SPA (Single Page Application).
- Estructura estándar de Vite/Vue.
- Integración vía API REST con el backend.

## 3. Testing
- **Estado**: CRÍTICO / INEXISTENTE
- **Unitarios/Integración**: No se encontraron tests automatizados en código (carpeta `tests` vacía de código Python/JS).
- **Manual**: Existencia de colecciones Postman (`Billing Backend System.postman_collection.json`) y definición OpenAPI (`openapi.yaml`).

## 4. Dominio de Facturación
- **Mercado**: Argentina.
- **Entidades Principales**:
  - `Comprobante` (Factura, Nota de Crédito/Débito)
  - `Cliente`
  - `Articulo`
  - `Impuesto` / `IVA`
- **Integración Fiscal**:
  - Módulos específicos para AFIP (`wsaa_client`, `wsfe_client`).
  - Cache de tokens (`afip_token_cache.json`).
  - Scripts de sembrado de datos fiscales (`seed_iva.py`, `seed_tipos_cbte.py`).
