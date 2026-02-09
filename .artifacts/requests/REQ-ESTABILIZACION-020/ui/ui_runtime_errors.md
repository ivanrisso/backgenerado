# UI Runtime Errors (REQ-020)

## 1. Auth 401 (Persistent)
- **Error:** `GET /api/v1/auth/me 401 (Unauthorized)`
- **Sintoma:** Consola ruidosa al navegar.
- **Causa:** Rehidratación proactiva sin check de token o token expirado no manejado silenciosamente.

## 2. Rutas 404 (Warning)
- **Error:** `No match found for location with path "/dashboard"`
- **Causa:** Referencias internas a `/dashboard` en lugar de `/`.

## 3. Sidebar Render Failure
- **Error:** Items configurados en DB no aparecen.
- **Causa:** Posible hardcoding en `Sidebar.vue` o filtrado incorrecto en `useSidebar` (permisos/roles).
