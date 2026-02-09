# REQ-ESTABILIZACION-006 - Fix RBAC Clientes

## Contexto
El Workflow 70 detectó que usuarios no administradores no pueden ver la lista de clientes, lo que rompe la funcionalidad de creación de recibos (el filtro/select de clientes aparece vacío).

## Objetivo
Permitir que usuarios autenticados (incluso sin rol 'admin') puedan listar clientes para poder operar en los módulos de Facturación y Tesorería.

## Alcance
-   **Backend:** Modificar `cliente_routes.py` para relajar la restricción `require_roles("admin")` en `GET /`.

## Criterios de Aceptación
-   Usuario con rol 'user' (o sin rol específico pero autenticado) puede obtener la lista de clientes.
-   El dropdown de clientes en `/recibos` se puebla correctamente.
