# Arquitectura del Frontend (Vue 3 + TS + Clean Architecture)

Este proyecto sigue una arquitectura "Clean" adaptada al frontend, buscando desacoplar la lógica de negocio (dominio y aplicación) del framework (Vue) y la infraestructura (API/Axios).

## 1. Estructura de Carpetas

```
src/
├── domain/            # El "corazón" de la aplicación. Pura lógica TS.
│   ├── entities/      # Modelos de datos (Interfaces/Clases).
│   └── repositories/  # Contratos (Interfaces) de cómo acceder a datos.
│
├── application/       # Casos de Uso (Acciones del usuario).
│   └── use-cases/     # Clases que orquestan la lógica.
│
├── infrastructure/    # Implementaciones concretas.
│   ├── api/           # Configuración HTTP (Axios).
│   └── repositories/  # Implementación de los repositorios del dominio.
│
├── ui/                # Capa Presentacional (Vue).
│   ├── components/    # Componentes reutilizables.
│   ├── views/         # Páginas completas.
│   ├── composables/   # Lógica reactiva (Glue code entre UI y Use Cases).
│   └── router/        # Configuración de rutas.
│
└── shared/            # Utilidades transversales (Formatters, Helpers).
```

## 2. Responsabilidad de cada Capa

### **Domain (Dominio)**

- **Qué contiene:** Entidades (`Cliente`, `TipoDoc`), Value Objects y las Interfaces de los Repositorios (`ITipoDocRepository`).
- **Dependencias:** NINGUNA. No conoce Axios, ni Vue, ni el Router.
- **Objetivo:** Definir _qué_ es el negocio y _qué_ operaciones existen, sin definir _cómo_ se hacen.

### **Application (Aplicación)**

- **Qué contiene:** Casos de Uso (`GetTiposDocUseCase`).
- **Dependencias:** Solo del Dominio.
- **Objetivo:** Orquestar flujos. Ejemplo: "Pedir datos al repo -> Validar -> Devolver".

### **Infrastructure (Infraestructura)**

- **Qué contiene:** Implementaciones reales de los repositorios (`AxiosTipoDocRepository`), clientes HTTP.
- **Dependencias:** Dominio (para cumplir los contratos) y librerías externas (Axios).
- **Objetivo:** "Ensuciarse" las manos con la IO (Internet, LocalStorage, etc.).

### **UI (Interfaz de Usuario)**

- **Qué contiene:** Todo lo visual (Vue).
- **Dependencias:** Application (para ejecutar acciones) y Domain (para mostrar datos).
- **Objetivo:** Mostrar datos al usuario y capturar eventos.

### **Shared (Compartido)**

- **Qué contiene:** Funciones puras de utilidad (fechas, strings).
- **Dependencias:** Mínimas.

## 3. Reglas de Dependencia

1. **La dependencia apunta hacia adentro:** `UI -> Application -> Domain`.
2. `Domain` no importa nada de nadie.
3. `Infrastructure` importa `Domain` (para implementar interfaces).
4. `UI` _nunca_ llama a `Infrastructure` directamente (idealmente usa Inyección de Dependencias).

## 4. Contratos (Interfaces / Ports)

Los contratos se definen en `domain/repositories`.

Ejemplo para `Tipos`:

```typescript
// domain/entities/TipoDoc.ts
export interface TipoDoc {
    id: number;
    nombre: string;
    habilitado: boolean;
    codigoArca: string;
}

// domain/repositories/ITipoDocRepository.ts
export interface ITipoDocRepository {
    getAll: () => Promise<TipoDoc[]>;
    getById: (id: number) => Promise<TipoDoc | null>;
}
```
