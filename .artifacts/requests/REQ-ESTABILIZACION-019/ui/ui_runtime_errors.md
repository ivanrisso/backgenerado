# UI Runtime Errors (REQ-019)

## 1. Auth 401 (Persistent)
- **Error:** `GET /api/v1/auth/me 401 (Unauthorized)`
- **Frecuencia:** Alta (en navegación).
- **Impacto:** Ruido en consola. Posible desincronización de estado si el token expira realmente.
- **Causa:** El frontend intenta rehidratar sesión (`auth.ts`) posiblemente antes de tener el token listo o el token es inválido pero no se limpia correctamente.

## 2. Rutas 404 (Configuración)
- **Error:** `[Vue Router warn]: No match found for location with path "/dashboard"`
- **Causa:** El Sidebar link apunta o se asume a `/dashboard`, pero la ruta real es `/`.
- **Acción:** Unificar criterio (alias `/dashboard` -> `/` o cambiar link).

## 3. Rutas 404 (Estructurales)
- **Error:** `[Vue Router warn]: No match found for location with path "/facturacion"`
- **Causa:** `/facturacion` es un agrupador en el menú, no una vista.
- **Acción:** Ninguna (comportamiento esperado si no se navega directo).
