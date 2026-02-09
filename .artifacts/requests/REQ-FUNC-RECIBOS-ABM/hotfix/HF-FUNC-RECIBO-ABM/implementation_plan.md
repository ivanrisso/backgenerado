# Plan de Implementación — HF-FUNC-RECIBO-ABM

## Objetivo
Implementar el listado y detalle de Recibos para completar el ABM de Tesorería.

## Componentes

### Backend (`app/`)
1.  **Repository (`repositories/comprobante_repository.py`)**
    -   [MODIFY] Actualizar `get_all` para aceptar filtros opcionales (tipo_comprobante_id, cliente_id, rango fechas).
    -   [MODIFY] Actualizar Interface `domain/repository/comprobante_repository_interfase.py`.
2.  **Service (`services/recibo_service.py`)**
    -   [NEW] Método `get_all(filters)` que llame al repositorio filtrando por Tipo `Recibo`.
    -   [NEW] Método `get_by_id(id)`.
3.  **Routes (`routes/recibo_routes.py`)**
    -   [NEW] `GET /` con parámetros de query (skip, limit, filters).
    -   [NEW] `GET /{id}`.

### Frontend (`src/`)
1.  **Service (`modules/Tesoreria/infrastructure/api/ReciboService.ts`)**
    -   [MODIFY] Agregar `getAll(params)` y `getById(id)`.
2.  **Views (`modules/Tesoreria/ui/views/`)**
    -   [NEW] `ReciboListView.vue`: Grilla de recibos con filtros.
        -   Reutilizar estilos y lógica de `InvoiceListView.vue`.
        -   Columnas: Fecha, Número, Cliente, Total, Saldo.
3.  **Router (`router/index.ts`)**
    -   [MODIFY] Agregar ruta `/recibos` apuntando a `ReciboListView`.

## Pasos de Ejecución
1.  Actualizar Repositorio Backend (Soporte de filtros).
2.  Implementar Service y Route Backend.
3.  Verificar Backend con `curl`.
4.  Implementar Service Frontend.
5.  Crear Vista Frontend.
6.  Configurar Router.
7.  Verificar E2E.
