# Fix Description: HF-TECH-AUTH-SESSION-V2 (REQ-020)

## Qué falla
- Errores consistentes `401 Unauthorized` en la consola del navegador al navegar entre páginas.

## Dónde ocurre
- `frontend/src/shared/stores/auth.ts` (acción `fetchUser` o `checkSession`).
- `frontend/src/infrastructure/api/axiosClient.ts` (interceptores).

## Cómo se manifiesta
- Ruido en consola.
- Posible riesgo de desincronización de sesión si el token realmente expira y no se renueva.
- UX degradada si se muestran alertas (aunque actualmente parece silencioso excepto en consola).

## Impacto técnico
- Dificulta debugging.
- Indica manejo incorrecto del ciclo de vida del token o check proactivo innecesario.
