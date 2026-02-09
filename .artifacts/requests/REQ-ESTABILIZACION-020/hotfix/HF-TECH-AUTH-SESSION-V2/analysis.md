# Analysis: HF-TECH-AUTH-SESSION-V2

## Causa Raíz Probable
El frontend intenta verificar la sesión (`fetchUser` o similar) en cada cambio de ruta o recarga, pero lo hace ANTES de que el token esté correctamente cargado desde `localStorage` o DESPUÉS de un evento que lo invalida pero no redirige.
El backend responde correctamente con 401 si no hay token, pero el frontend no debería preguntar si sabe que no tiene token (o debería manejar el 401 sin error de consola).

## Componentes Involucrados
- `auth.ts` (Store)
- `router/index.ts` (Guard global)

## Solución Propuesta
- Verificar existencia de token antes de llamar a endpoints protegidos.
- Ajustar lógica de `isAuthenticated` en el store.
