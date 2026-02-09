# SKILL — Menu Mapping

## Rol autorizado
- Arquitecto de Software Senior
- Frontend Engineer

## Objetivo
Verificar la coherencia entre rutas del sistema y entradas visibles en el menú según rol.

## Inputs
- Menú dinámico
- Roles y permisos
- Rutas detectadas

## Pasos
1. Enumerar ítems del menú por rol.
2. Mapear cada ítem a su ruta esperada.
3. Detectar:
   - rutas sin menú
   - menú sin ruta
   - menú visible sin permiso

## Output
- `architecture/menu_route_matrix.md`

## Restricciones
- No alterar permisos ni menú.
