# Implementation Plan: REQ-FUNC-003 (Menú Dinámico)

## Goal
Hacer que el Sidebar refleje dinámicamente la estructura de menús definida en la Base de Datos, respetando los permisos de rol.

## User Review Required
> [!NOTE]
> Se modificará el endpoint `GET /menuitems/` para que sea accesible por cualquier usuario autenticado (actualmente Admin-only). Esto permite al frontend obtener la estructura del menú. La seguridad se mantiene ya que solo se expone la estructura de navegación.

## Proposed Changes

### Backend
#### [MODIFY] [menuitem_routes.py](file:///home/irisso/proyectos/facturacion/app/routes/menuitem_routes.py)
- Cambiar dependencia de `require_roles("admin")` a `get_current_active_user` en el endpoint `GET /`.

### Frontend
#### [MODIFY] [Sidebar.vue](file:///home/irisso/proyectos/facturacion/frontend/src/shared/ui/components/Sidebar.vue)
- Importar `useMenuItems`.
- Eliminar import estático `config/menu`.
- En `onMounted`, llamar a `loadMenuTree()`.
- Reemplazar `menuConfig` por `menuTree` en el `computed`.
- Adaptar `filteredMenu` para mapear `item.roles` (Objetos) a Strings para `authStore`.

## Verification Plan

### Manual Verification
1. **Login como Admin:**
    - Verificar que el sidebar carga items desde DB.
2. **Login como Operador:**
    - Verificar que el sidebar carga.
    - Verificar que NO ve items restringidos.
