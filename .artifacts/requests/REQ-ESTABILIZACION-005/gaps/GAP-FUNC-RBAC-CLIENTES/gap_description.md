# GAP-FUNC-RBAC-CLIENTES

## Problema
Usuarios no administradores (como el test user creado) reciben un error `403 Forbidden` al intentar listar clientes (`GET /api/v1/clientes/`).

## Impacto
-   El filtro de "Cliente" en `ReciboListView` aparece vacío.
-   No se puede crear un recibo seleccionando cliente desde la UI (dropdown vacío).

## Causa Probable
El endpoint `clientes` tiene la dependencia `require_roles("admin")` estricta, o el usuario de prueba no tiene el rol asignado correctamente.

## Recomendación
-   Revisar política de permisos: ¿Solo admin puede ver clientes?
-   Si es así, el usuario de tesorería necesita rol admin o un rol específico "tesoreria" con permiso de lectura de clientes.
