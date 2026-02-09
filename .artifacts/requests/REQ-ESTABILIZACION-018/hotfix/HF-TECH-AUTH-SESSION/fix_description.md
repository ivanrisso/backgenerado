# Fix Description: HF-TECH-AUTH-SESSION

## Problema
Inestabilidad de sesión. Redirecciones a Login (401) inesperadas durante la navegación, especialmente en `Nuevo Recibo`.

## Impacto
Bloquea la operación continua.

## Criterio
Revisar `auth` store y `axios` interceptors.
Asegurar que el token se persiste y se envía correctamente.
Evitar redirección agresiva si el token es válido.
