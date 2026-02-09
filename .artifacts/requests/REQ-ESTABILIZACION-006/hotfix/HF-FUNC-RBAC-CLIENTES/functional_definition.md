# Functional Definition - HF-FUNC-RBAC-CLIENTES

## Problema Actual
El endpoint `GET /api/v1/clientes/` exige rol `admin`.
Usuarios operativos (Tesorería, Ventas) no pueden ver clientes, bloqueando ABMs.

## Solución Propuesta
Cambiar la dependencia de autorización en `cliente_routes.py`.
-   **Antes:** `Depends(require_roles("admin"))`
-   **Después:** `Depends(get_current_active_user)` (Usuario autenticado y activo).

## Justificación
La lista de clientes es información operativa básica requerida por cualquier usuario del sistema para facturar o cobrar. No debe estar restringida a administradores.
