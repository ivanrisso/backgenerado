# Implementation Plan - HF-FUNC-RBAC-CLIENTES

## Backend (`app/routes/cliente_routes.py`)
1.  **Importar:** `get_current_active_user` desde `app.dependencies.auth`.
2.  **Modificar:** Endpoint `GET /` (list customers).
    -   Cambiar `Depends(require_roles("admin"))` por `Depends(get_current_active_user)`.

## Verificación
1.  **Manual:** Loguearse como `newtester@gmail.com` (rol no admin).
2.  **Acción:** Ir a `/recibos`.
3.  **Resultado:** El dropdown de "Cliente" debe mostrar resultados (y no estar vacío).
4.  **Backend Check:** El request a `/api/v1/clientes/` debe devolver `200 OK` en lugar de `403`.
