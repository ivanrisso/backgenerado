# SYSTEM FOUNDATION
Base técnica y conceptual para Operating Manual, Design System y Domain Rules

---

## 0. Propósito de este Documento

Este documento actúa como **capa fundacional** del sistema, y debe leerse **junto con el System Design existente**.

Su objetivo es:
- Consolidar el **stack técnico real** (backend + frontend)
- Establecer **principios operativos** del sistema
- Definir **reglas de desarrollo y uso**
- Servir como base para construir:
  - Operating Manual
  - Design System
  - Domain Rules

Este documento **NO define features**, **NO redefine arquitectura**, y **NO reemplaza** al System Design.
Es un complemento operativo y normativo.

---

## 1. Visión General del Sistema

El sistema es una plataforma de facturación con arquitectura moderna, orientada a escalabilidad, seguridad y mantenibilidad.

### Componentes principales
- **Frontend SPA** (Vue 3)
- **Backend API** (FastAPI)
- **Base de Datos relacional**
- **Autenticación basada en Cookies HTTPOnly**
- **Control de Acceso por Roles (con abstracción de permisos en UI)**

### Principios rectores
- Backend como **Source of Truth**
- Clean Architecture en backend
- Arquitectura modular en frontend
- Seguridad por defecto
- Trade-offs explícitos y documentados

---

## 2. Stack Técnico (Referencia Base)

### 2.1 Backend
- Lenguaje: **Python 3.11**
- Framework: **FastAPI**
- ORM: **SQLAlchemy 2.x (Async)**
- Validación: **Pydantic v2**
- Auth: **JWT (access + refresh)**
- Transporte de sesión: **HTTPOnly Cookies**
- DB Driver: **AsyncMy / MySQL**
- Migraciones: **Alembic**

**Patrones obligatorios:**
- Clean Architecture
- Async I/O
- Separación dominio / infraestructura
- Excepciones de dominio (no lógica en controllers)

---

### 2.2 Frontend
- Framework: **Vue 3**
- Lenguaje: **TypeScript**
- Build Tool: **Vite**
- State Management: **Pinia**
- Routing: **Vue Router**
- Estilos: **TailwindCSS**

**Patrones obligatorios:**
- Arquitectura modular (`src/modules`)
- `src/shared` solo para lógica transversal
- Estado global centralizado (AuthStore)
- Guards + Directivas para seguridad UI

---

## 3. Modelo de Seguridad (Resumen)

### Autenticación
- JWT almacenado exclusivamente en **cookies HTTPOnly**
- El frontend **no maneja tokens**
- Persistencia de sesión vía `/auth/me`

### Autorización
- **Backend:** valida únicamente **Roles**
- **Frontend:** usa Roles + Permisos como abstracción de UX
- Esta estrategia es **intencional** y documentada como trade-off

### Postura CSRF
- Mitigación vía `SameSite=Lax`
- Sin tokens CSRF por ahora
- Revisable si cambian los supuestos de integración

---

## 4. Reglas Operativas (Operating Manual – Base)

### Qué SÍ se puede hacer
- Agregar nuevos módulos de negocio
- Extender UI usando componentes compartidos
- Crear nuevos endpoints siguiendo Clean Architecture

### Qué NO se debe hacer
- Poner lógica de negocio en controllers
- Validar reglas de negocio solo en frontend
- Acceder a DB fuera de repositories
- Hardcodear decisiones de seguridad

### Entornos
- DEV: localhost, cookies `secure=false`
- PROD: HTTPS obligatorio, cookies `secure=true`

---

## 5. Frontend Operating Rules

### Arquitectura
- Cada dominio vive en `src/modules/{Domain}`
- Cada módulo puede tener:
  - ui / views
  - application
  - domain (si aplica)

### Auth & Estado
- `AuthStore` es la única fuente de sesión
- No usar localStorage para auth
- Todo control de acceso pasa por:
  - `canAccess()`
  - `v-permission`

### Navegación
- Sidebar dinámico basado en configuración central
- Guards de router obligatorios para rutas protegidas

---

## 6. Design System (Base Contractual)

Este documento **no define diseño visual**, sino **reglas contractuales** de UI.

### Principios
- Consistencia visual
- Feedback inmediato al usuario
- Estados claros (loading, error, empty)
- Accesibilidad básica (focus, contrastes)

### Componentes Base
- Botones
- Inputs
- Modales
- Tablas
- Notificaciones

### Reglas
- Los componentes base viven en `shared/ui`
- Los módulos NO redefinen estilos globales
- Tailwind se usa con convenciones acordadas

---

## 7. Domain Rules (Base)

### Dominios Identificados
- Auth / Usuarios / Roles
- Clientes
- Facturación
- Maestros

### Reglas Generales
- El backend valida reglas críticas
- El frontend valida experiencia de uso
- Estados y transiciones viven en backend

### Anti-reglas
- No duplicar reglas en múltiples capas
- No hardcodear estados
- No acoplar UI a estructura de DB

---

## 8. Relación con Otros Documentos

Este documento debe usarse junto con:
- System Design
- Auditorías técnicas
- ADRs
- Core Definition of Done

En caso de conflicto:
1. ADR aprobado
2. System Design
3. SYSTEM FOUNDATION
4. Implementación

---

## 9. Uso con IA / LLMs

Cuando se use este sistema como contexto para IA:
- Este documento define el **marco operativo**
- El System Design define la **arquitectura**
- Las IA no deben proponer cambios que contradigan estos documentos

Si hay conflicto:
- Debe explicitarse como trade-off
- No se asume refactor automático

---

## 10. Estado del Documento
Este documento es:
- Vivo
- Versionable
- Parte del gobierno del sistema

No debe modificarse sin revisión técnica.
