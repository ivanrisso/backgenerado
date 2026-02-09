# Impact Analysis - HF-FUNC-RBAC-CLIENTES

## Componentes Afectados
1.  **Backend:** `app/routes/cliente_routes.py`.
    -   Modificación de decorador en `get_clientes`.

## Riesgos
-   **Seguridad:** Se expone la lista de clientes a cualquier usuario con credenciales válidas.
    -   **Mitigación:** Aceptable para este sistema interno. Si se requiere más granularidad, crear roles específicos (ej. "facturacion") en el futuro.
-   **Performance:** No hay impacto adicional.

## Dependencias
-   `app.dependencies.auth.get_current_active_user` debe estar disponible e importado.
