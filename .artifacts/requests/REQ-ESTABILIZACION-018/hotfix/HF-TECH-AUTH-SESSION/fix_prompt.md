# Fix Prompt: HF-TECH-AUTH-SESSION

## Contexto
Errores 401 recurrentes y redirecciones al login durante el uso del sistema.

## Instrucción
1. Revisar `src/modules/Auth/store/auth.ts` y `src/core/api/httpClient.ts` (o similar).
2. Verificar lógica de persistencia de token (localStorage vs Cookies).
3. Verificar interceptores de respuesta.
4. Asegurar que `checkAuth` o similar no falle falsamente.

## Evidencia
Navegación fluida por Menú -> Tesorería -> Nuevo Recibo sin logout forzado.
