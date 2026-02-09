# Plan de Implementación: REQ-FUNC-005

## Objetivo
Restaurar la jerarquía del menú de Seguridad insertando el ítem padre faltante "Seguridad" (ID 4) en la base de datos.

## User Review Required
None. Data fix only.

## Proposed Changes
### Database (via Script)
#### [NEW] [fix_seguridad_menu.py](file:///home/irisso/proyectos/facturacion/scripts/fix_seguridad_menu.py)
- Verificar existencia de ID 4.
- Insertar MenuItem: `id=4`, `nombre='Seguridad'`, `path=None`, `parent_id=None`.
- Asociar ID 4 al Rol 'Admin'.

## Verification Plan
### Automated Tests
- Ejecutar `inspect_seguridad_menu.js` después del fix.
- Resultado esperado: ID 4 encontrado, children mapeados.

### Manual Verification
1. Recargar Frontend.
2. Verificar que "Usuarios", "Roles", "Menús" ya no están en root.
3. Verificar que aparece grupo "Seguridad".
4. Expandir y verificar hijos.
