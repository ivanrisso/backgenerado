# SKILL — UI CRUD Sweep

## Rol autorizado
- QA

## Objetivo
Ejecutar visualmente todos los CRU(D) detectados en el frontend para validar estabilidad técnica.

## Inputs
- Vistas CRUD detectadas
- Backend en entorno dev/test

## Pasos
Para cada vista CRUD:
1. Abrir listado.
2. Crear entidad (Create).
3. Leer detalle (Read).
4. Editar entidad (Update).
5. Eliminar si aplica (Delete).

## Validaciones
- No errores JS fatales.
- UI no se rompe.
- Estados loading/error funcionan.

## Output
- `qa/crud_execution_matrix.md`

## Restricciones
- No validar reglas de negocio profundas.
