# Fix Description — HF-TECH-003

## Problema
Items de menú huérfanos en la base de datos.
Existen items que apuntan a un `parent_id` (22) que no existe.

## Síntoma
- Items "Listado" y "Facturas" aparecen incorrectamente en la jerarquía (posiblemente como raíz o rotos).
- Advertencia en logs de inspección.

## Evidencia
- `ui_runtime_errors.md`
- Logs de inspección.

## Datos Técnicos
- Item ID 26 (Listado) -> Parent 22
- Item ID 27 (Facturas) -> Parent 22
- Parent 22 NO existe.
