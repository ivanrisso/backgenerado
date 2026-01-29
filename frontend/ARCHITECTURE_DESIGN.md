# Arquitectura Frontend - Clean Architecture + DDD

Este documento define la estructura base y las reglas de arquitectura para el frontend del proyecto de facturación, centrándose en los modelos: **Domicilio, Teléfono, Operador, TipoComprobante, Concepto, Moneda, Iva, TipoImpuesto**.

## 1. Estructura de Carpetas

La estructura sigue estrictamente los principios de Clean Architecture:

```
src/
├── domain/                  # Lógica de Negocio Pura (Enterprise Business Rules)
│   ├── entities/            # Modelos de datos y reglas de negocio centrales
│   └── repositories/        # Contratos (Interfaces) para acceso a datos
│
├── application/             # Lógica de Aplicación (Application Business Rules)
│   ├── use-cases/           # Orquestación de flujos de usuario
│   └── dtos/                # Objetos de transferencia de datos (opcional)
│
├── infrastructure/          # Detalles de Implementación (Interface Adapters & Frameworks)
│   ├── api/                 # Clientes HTTP y configuración de red
│   └── repositories/        # Implementación concreta de los repositorios del dominio
│
├── ui/                      # Presentación (Vue Components)
│   ├── views/               # Páginas de la aplicación
│   ├── components/          # Componentes reusables
│   └── composables/         # Adaptadores reactivos (Vue <-> Application Layer)
│
└── shared/                  # Utilidades transversales
```

## 2. Responsabilidad de cada Capa

- **Domain**:
  - **Responsabilidad**: Definir las "verdades" del negocio. Contiene las Entidades (ej. `Domicilio`, `Iva`) y las interfaces de los Repositorios (ej. `IIvaRepository`).
  - **Conocimiento**: No conoce NADA del exterior. No sabe que existe Vue, Axios, o el navegador. Es puro TypeScript.

- **Application**:
  - **Responsabilidad**: Ejecutar los casos de uso específicos de la aplicación (ej. "Obtener lista de monedas", "Crear un domicilio"). Orquesta la interacción entre el dominio y el mundo exterior.
  - **Conocimiento**: Conoce el Dominio. No conoce detalles de UI ni de infraestructura (repositorios concretos).

- **Infrastructure**:
  - **Responsabilidad**: Proveer implementaciones reales para las interfaces del dominio (ej. `HttpIvaRepository` que usa Axios). Maneja llamadas API, LocalStorage, etc.
  - **Conocimiento**: Conoce el Dominio (para implementar sus interfaces) y librerías externas.

- **UI**:
  - **Responsabilidad**: Presentar datos al usuario y capturar interacciones.
  - **Conocimiento**: Usa la capa de Application (Casos de uso). Observa entidades del Dominio para renderizar.

- **Shared**:
  - **Responsabilidad**: Código genérico reutilizable (formatos de fecha, validaciones simples) que no depende de reglas de negocio complejas.

## 3. Contratos entre Capas (Repositories)

La comunicación entre _Application_ e _Infrastructure_ se realiza a través de **Interfaces de Repositorio** definidas en el _Domain_.

Ejemplo conceptual:

- **Contrato (Domain)**:
  `export interface IIvaRepository { getAll(): Promise<Iva[]>; }`

- **Implementación (Infrastructure)**:
  `class HttpIvaRepository implements IIvaRepository { ... }`

- **Uso (Application)**:
  `constructor(private ivaRepo: IIvaRepository) { ... }`

Esto permite cambiar la implementación (ej. de HTTP a Mock) sin tocar la lógica de negocio.

## 4. Reglas Claras de Dependencia

1.  **Regla de Dependencia**: Las dependencias de código fuente solo pueden apuntar hacia adentro, hacia políticas de nivel más alto.
    - `UI` -> `Application` -> `Domain`
    - `Infrastructure` -> `Domain`
2.  **Independencia del Framework**: El Dominio y la Aplicación no deben depender de Vue.js.
3.  **Independencia de la UI**: La UI puede cambiar sin afectar las reglas de negocio.
4.  **Independencia de la Base de Datos/API**: El dominio no sabe de dónde vienen los datos.

## 5. Modelos Requeridos

Se han generado/validado las entidades y repositorios para:

- Domicilio
- Teléfono
- Operador
- TipoComprobante
- Concepto
- Moneda
- Iva
- TipoImpuesto
