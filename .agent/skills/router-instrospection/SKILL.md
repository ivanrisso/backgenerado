# SKILL — Router Introspection

## Rol autorizado
- Arquitecto de Software Senior
- Frontend Engineer

## Objetivo
Inspeccionar la configuración del router frontend para identificar todas las rutas existentes, su protección (auth/roles) y su vínculo con vistas y menú.

## Inputs
- Configuración de Vue Router
- Guards de navegación
- Metadata de rutas

## Pasos
1. Enumerar todas las rutas registradas.
2. Identificar:
   - Públicas
   - Autenticadas
   - Dependientes de rol
3. Asociar cada ruta con su componente de vista.
4. Detectar rutas:
   - sin vista
   - sin menú
   - inaccesibles por guards

## Output
- `architecture/routes_inventory.md`

## Restricciones
- No modificar código.
- No inferir rutas inexistentes.
