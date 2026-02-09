# Plan de Implementación: REQ-FUNC-004

## Objetivo
Corregir la renderización plana del menú dinámico en el Sidebar, asegurando que los ítems hijos se muestren anidados bajo sus padres.

## User Review Required
No major breaking changes. Verification steps included.

## Proposed Changes
### Frontend
#### [MODIFY] [useUserMenu.ts](file:///home/irisso/proyectos/facturacion/frontend/src/shared/composables/useUserMenu.ts)
- Agregar logging para inspeccionar la respuesta del API.
- Asegurar que la comparación de `id` y `parent_id` sea robusta (manejo de tipos string/int).
- Mejorar la lógica de construcción del árbol para manejar "huérfanos" (items con padre no encontrado) moviéndolos a la raíz o logueando warning.

## Verification Plan
### Automated Tests
- No hay tests unitarios de frontend configurados para esto. Se usará verificación manual con script de navegador.

### Manual Verification
1. Login como Admin.
2. Verificar consola del navegador para ver logs de construcción del árbol.
3. Verificar visualmente que "Puntos de Venta" no está en el primer nivel.
4. Expandir "Configuración" (o "Maestros") y verificar que "Puntos de Venta" aparece ahí.
