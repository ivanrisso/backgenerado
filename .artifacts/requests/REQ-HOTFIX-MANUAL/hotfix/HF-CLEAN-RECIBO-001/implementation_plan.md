# HF-CLEAN-RECIBO-001 — Plan de Implementación

## Problema
El servicio `ReciboService` actualizó su constructor para requerir `ClienteRepositoryInterface`, pero los tests unitarios en `tests/test_recibo.py` no fueron actualizados, provocando fallas en la ejecución de tests y en el CI.

## Revisión requerida
- [ ] Validar que no existan otras referencias rotas al constructor de `ReciboService` (Verificado: Solo `recibo_routes.py` lo usa y está correcto).

## Cambios Propuestos

### Backend
#### [MODIFY] [test_recibo.py](file:///home/irisso/proyectos/facturacion/tests/test_recibo.py)
- Actualizar fixture `mock_repos` para incluir `cliente`.
- Actualizar fixture `service` para inyectar `mock_repos["cliente"]`.
- En `test_create_recibo_basic` y `test_create_recibo_with_imputation`:
    - Configurar el mock de `cliente_repo.get_by_id` para devolver un cliente válido.
    - Verificar que se llama al repositorio de clientes.

## Plan de Verificación

### Tests Automatizados
1. Ejecutar el test específico:
   ```bash
   pytest tests/test_recibo.py -v
   ```

### Verificación Manual (Stage D)
Dado que el cambio es solo en tests, la verificación funcional en runtime comprobará que la ruta de creación de recibos siga funcionando correctamente (ya que la inyección en `recibo_routes.py` parecía correcta, pero debemos asegurarnos de que no haya efectos colaterales).

1. Comprobar ruta de creación de recibos (si es posible via Frontend o Curl).
   - Sin embargo, el problema reportado es explícitamente sobre el constructor en tests. El runtime debería estar bien si `recibo_routes.py` está bien.
   - De todos modos, ejecutaremos una prueba de humo en el frontend si el entorno lo permite.
