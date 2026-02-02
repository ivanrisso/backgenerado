# SKILL — UI View Loader

## Rol autorizado
- Frontend Engineer

## Objetivo
Verificar que todas las vistas frontend se cargan correctamente mediante imports dinámicos.

## Inputs
- Rutas detectadas
- Componentes lazy-loaded

## Pasos
1. Navegar a cada ruta.
2. Forzar carga del componente.
3. Detectar errores de:
   - import
   - alias
   - path relativo
   - compilación Vite

## Output
- `ui/view_load_report.md`

## Restricciones
- No corregir imports.
