# Arquitectura Actual

## Diagrama Textual

```mermaid
graph TD
    User[Navegador Web / Usuario]
    
    subgraph Frontend [SPA - Vue.js 3]
        UI[Componentes UI]
        Store[Pinia Store]
        Router[Vue Router]
        Axios[Cliente HTTP Axios]
    end

    subgraph Backend [Monolito Modular - FastAPI]
        API[API Routes / Controllers]
        UseCases[Casos de Uso]
        Domain[Dominio / Entidades]
        RepoInt[Interfaces Repositorios]
        RepoImpl[Implementación Repositorios]
        Infra[Infraestructura]
        AFIPClient[Adaptador AFIP (SOAP)]
    end

    subgraph Data [Persistencia]
        MySQL[(MySQL 8 Database)]
    end

    subgraph External [Servicios Externos]
        AFIP[AFIP Web Services (WSAA/WSFE)]
    end

    User --> UI
    UI --> Store
    Store --> Axios
    Axios -- "JSON / HTTPS" --> API
    
    API --> UseCases
    UseCases --> Domain
    UseCases --> RepoInt
    RepoImpl ..|> RepoInt
    RepoImpl --> Infra
    Infra -- "SQLAlchemy" --> MySQL
    
    Infra --> AFIPClient
    AFIPClient -- "XML / SOAP" --> AFIP
```

## Descripción de Arquitectura

El sistema sigue una arquitectura de **Monolito Modular** con una clara separación entre Cliente (Frontend) y Servidor (Backend), siguiendo principios de **Clean Architecture** en el lado del servidor.

### 1. Capa de Presentación (Frontend)
- Aplicación de Página Única (SPA) construida con Vue.js 3.
- Responsable de la renderización, gestión de estado del cliente y ruteo.
- Se comunica con el backend exclusivamente a través de llamadas API REST (JSON).

### 2. Capa de Transporte (Backend API)
- Expuesta vía FastAPI.
- Maneja la validación de entrada (Pydantic Schemas) y serialización de respuesta.
- Delega la lógica de negocio a los Casos de Uso.

### 3. Capa de Aplicación (Use Cases)
- Orquesta la lógica de negocio específica de la aplicación.
- Interactúa con las entidades de dominio y los puertos (interfaces) de repositorios y servicios.

### 4. Capa de Dominio (Core)
- Contiene las reglas de negocio puras y las definiciones de entidades (`Comprobante`, `Cliente`, etc.).
- Desacoplada de frameworks externos y detalles de infraestructura.

### 5. Capa de Infraestructura
- Implementa los detalles técnicos: acceso a base de datos (SQLAlchemy), integración con servicios externos (AFIP/Zeep), y utilidades concretas.

## Acoplamientos Visibles
- **Backend <-> Base de Datos**: Acoplamiento fuerte a través de SQLAlchemy, aunque mitigado por el patrón Repository.
- **Backend <-> AFIP**: Dependencia crítica de los servicios externos de AFIP para la facturación electrónica. La lógica de autenticación y autorización (WSAA) es un punto de fallo central.
- **Frontend <-> API**: Acoplamiento por contrato de datos (JSON schemas).

## Puntos Críticos del Dominio Fiscal
- **Autenticación AFIP**: La gestión de tokens (Tickets de Acceso) y su ciclo de vida (expiración) es crítica. El almacenamiento en archivos JSON en raíz (`afip_token_cache.json`) es una implementación frágil.
- **Validación de Comprobantes (CAE)**: La obtención del CAE (Código de Autorización Electrónico) es síncrona y bloqueante para la emisión de facturas válidas.
- **Consistencia de Datos**: Sincronización entre estados locales de comprobantes y el estado en servidores de AFIP.
