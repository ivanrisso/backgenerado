# Implementation Plan - Dashboard

## UI Components
### [NEW] `frontend/src/modules/Dashboard/ui/views/DashboardView.vue`
- Layout simple con Grid/Flex.
- Tarjetas de acceso directo:
  - Nueva Factura (`/comprobantes/nuevo`)
  - Nuevo Recibo (`/recibos/nuevo`)
  - Nuevo Cliente (`/clientes`) - *Verificar ruta de creación*

## Router
### [MODIFY] `frontend/src/router/index.ts`
- Importar `DashboardView`.
- Actualizar `path: '/'` para usar `component: DashboardView`.
- Eliminar `redirect`.

## Dependencies
- Verificar si existe módulo `Dashboard`. Si no, crearlo o usar `shared` provisionalmente (Recomendado: Crear carpeta módulo `Dashboard`).
