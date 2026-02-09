# Impact Analysis

## Componentes Afectados
- `frontend/src/router/index.ts`: Modificar ruta `/` para apuntar a `DashboardView`.
- `frontend/src/modules/Dashboard/ui/views/DashboardView.vue` (Nuevo): Vista principal.

## Dependencias
- Requiere autenticación (existente en `MainLayout`).
- Accesos directos requieren rutas existentes (`/recibos/nuevo`, `/comprobantes/nuevo`).

## Riesgo
- **Bajo.** Solo afecta la vista landing. No altera lógica de negocio existente.
