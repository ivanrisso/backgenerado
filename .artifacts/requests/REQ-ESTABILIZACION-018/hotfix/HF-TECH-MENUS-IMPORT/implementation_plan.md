# Plan de Implementación v2 - HF-TECH-MENUS-IMPORT

## Descripción del Problema
La verificación inicial falló. Se descubrió que el crash no era solo por importar `MenuItem` mal, sino porque el composable `useMenuItems` **no existe** y el alias `@ui` apunta a una carpeta inexistente (`src/ui`).

## Solución Técnica
En lugar de crear una capa global `src/ui` vacía, se ubicará el composable dentro del módulo de Autenticación, siguiendo la arquitectura modular.

## Cambios Propuestos

### Frontend

#### [NUEVO] [useMenuItems.ts](file:///home/irisso/proyectos/facturacion/frontend/src/modules/Auth/ui/composables/useMenuItems.ts)
- Implementar el composable usando `AxiosMenuItemRepository`.
- Exponer: `menuTree`, `loadMenuTree`, `saveMenuItem`, `deleteMenuItem`.

#### [MODIFICAR] [MenuItemTree.vue](file:///home/irisso/proyectos/facturacion/frontend/src/modules/Auth/ui/views/MenuItemTree.vue)
- Actualizar el import del composable para apuntar a la nueva ubicación relativa (o corregir alias).
- `import { useMenuItems } from '../composables/useMenuItems';`

## Plan de Verificación

### Tests Manuales
1. Referencia al Plan v1 (Navegación a `/menus`).
2. Verificar funcionalidad básica: Cargar árbol de menús.
