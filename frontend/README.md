# Arquitectura Frontend (Clean Architecture + DDD)

Este proyecto sigue una arquitectura limpia basada en principios de Domain-Driven Design (DDD) liviano.
El objetivo es desacoplar la lógica de negocio del framework (Vue) y de los detalles de infraestructura (API, Storage).

## Reglas de Dependencia
La regla más importante es la dirección de las dependencias: **Hacia adentro**.

*   **Domain**: No depende de NADA.
*   **Application**: Depende solo de **Domain**.
*   **Infrastructure**: Depende de **Domain** y **Application**.
*   **UI**: Depende de **Application**, **Domain** y **Shared**.

El flujo de control suele ser: `UI -> Application -> Domain`.
La inversión de dependencias se usa para Infraestructura: `Application` define una interfaz (Repository) y `Infrastructure` la implementa.

## Estructura de Carpetas

### 1. Domain (`src/domain`)
**Núcleo de la aplicación.** Contiene la lógica de negocio pura y los tipos de datos.
*   `entities/`: Objetos de negocio con identidad (ej: `Cliente`, `Factura`).
*   `value-objects/`: Objetos inmutables definidos por su valor (ej: `Email`, `Moneda`).
*   **`repositories/` (Interfaces)**: Contratos que definen cómo se accede a los datos. **SOLO Interfaces**, sin implementación.
*   `services/`: Lógica de dominio puro que no pertenece a una sola entidad.
*   `errors/`: Errores específicos del dominio.

### 2. Application (`src/application`)
**Casos de Uso.** Orquesta la lógica de negocio llamando al dominio y repositorios.
*   `use-cases/`: Acciones específicas del usuario (ej: `CrearFactura`, `ListarClientes`). Contiene la lógica orquestadora.
*   `dtos/`: (Data Transfer Objects) Estructuras de datos para entrada/salida de los casos de uso.
*   `services/`: Servicios de aplicación.

### 3. Infrastructure (`src/infrastructure`)
**Implementación y Detalles Técnicos.** El "mundo exterior".
*   `repositories/`: **Implementación concreta** de los repositorios del dominio (ej: `AxiosClienteRepository` que implementa `ClienteRepository`).
*   `api/`: Configuración de clientes HTTP (Axios, Fetch).
*   `adapters/`: Adaptadores para servicios externos (ej: `LocalStorageService`, `Logger`).

### 4. UI (`src/ui`)
**Capa de Presentación (Vue 3).**
*   `components/`: Componentes reutilizables, visuales y "tontos" (sin lógica de negocio compleja).
*   `views/`: Páginas completas. Son el punto de entrada que conecta la UI con la capa de Application.
*   `layouts/`: Estructuras de página (Sidebar, Header).
*   `composables/`: Lógica de estado reactivo de Vue (usando Composition API) para conectar la UI con los Casos de Uso.
*   `stores/`: Gestión de estado global (Pinia), si es necesario para cache o UI state.

### 5. Shared (`src/shared`)
**Utilidades compartidas.**
*   `types/`: Tipos de TypeScript genéricos.
*   `utils/`: Funciones puras de utilidad (formato de fechas, números).
*   `constants/`: Constantes globales.

## Ejemplo de Flujo (Crear Cliente)

1.  **UI (`views/ClienteNew.vue`)**: El usuario llena el form y hace click en "Guardar". Llama a un composable.
2.  **UI (`composables/useClientes.ts`)**: Instancia el caso de uso `CreateClienteUseCase`.
3.  **Application (`use-cases/CreateClienteUseCase.ts`)**:
    *   Recibe un DTO con los datos.
    *   Valida reglas de negocio.
    *   Crea una entidad `Cliente` (Domain).
    *   Llama a `clienteRepository.save(cliente)` (Interfaz definida en Domain).
4.  **Infrastructure (`repositories/AxiosClienteRepository.ts`)**:
    *   Implementa `save()`.
    *   Hace el `POST` a la API real.
    *   Retorna el resultado.
