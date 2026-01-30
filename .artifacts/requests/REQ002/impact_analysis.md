# Impact Analysis - REQ-002

## Componentes Afectados
- **Backend**:
    - `app/services/cliente_service.py`: Nuevo método `obtener_saldos_deudores()`.
    - `app/infrastructure/repositories/cliente_repository.py`: Nueva query para calcular saldos.
    - `app/routes/cliente_routes.py`: Nuevo endpoint `GET /clientes/deudores`.
    - **Database**: No requiere cambios de esquema (lectura de `comprobantes`, `pagos`, `notas_credito`).
- **Frontend**:
    - `src/modules/Clientes/composables/useClientes.ts`: Nuevo método `loadClientesDeudores()`.
    - `src/modules/Clientes/ui/views/ClienteDeudorList.vue`: Nueva vista.
    - `src/router/index.ts`: Nueva ruta `/clientes/deudores`.
    - `src/shared/ui/components/Sidebar.vue`: Nuevo ítem de menú.

## Riesgos
- **Performance**: Calcular el saldo on-the-fly iterando todos los comprobantes y pagos puede ser lento si el volumen de datos es alto.
    - *Mitigación*: Implementar paginación en el endpoint y, idealmente, query optimizada a nivel SQL (SUM/GROUP BY) en lugar de lógica en código.
- **Consistencia**: Asegurar que las Notas de Crédito resten correctamente.

## Estrategia de Pruebas
1.  **Unit**: Testear el servicio de cálculo de saldo con mocks de repositorios.
2.  **Integration**: Testear la query SQL con datos de prueba en DB.
3.  **E2E/Manual**: Verificar en frontend que el saldo mostrado coincide con Invoices - Payments - NCs.

## Cambios en API
- `GET /api/v1/clientes/deudores`: Retorna lista de clientes con saldo > 0.
    - Query params: `min_saldo`, `fecha_corte` (opcional).
