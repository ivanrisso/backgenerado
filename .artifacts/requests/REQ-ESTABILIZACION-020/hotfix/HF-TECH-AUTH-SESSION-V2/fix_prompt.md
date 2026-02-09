Contexto:
La aplicación genera múltiples errores 401 en consola al navegar, intentando verificar la sesión (`fetchUser` en `api/v1/auth/me`) cuando probablemente el token no está listo o es inválido, pero sin redirigir al login (lo cual es correcto si es un check background, pero el error 401 ensucia la consola).

Objetivo:
Eliminar el ruido de 401s sin comprometer la seguridad.

Pasos:
1. En `auth.ts`, verificar si existe token en `localStorage` antes de llamar a la API. Si no hay token, no llamar y asumir `isAuthenticated = false`.
2. Si el llamado es necesario, asegurar que el `httpClient` o el store maneje el 401 silenciosamente durante la hidratación de sesión, o usar un endpoint que no devuelva 401 sino 200 { guest: true } si fuera posible (limitado a hotfix frontend: solo manejar error).

Output esperado:
Navegación limpia de errores de consola.
