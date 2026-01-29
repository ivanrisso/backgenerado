# Critical Paths — Facturación AR (Bootstrap)

## Backend
1. Healthcheck / arranque de API.
2. Creación de comprobante en estado Draft.
3. Transición de estado local SIN llamada real a AFIP.
4. Consulta de comprobante por ID.

## AFIP (simulado)
- Timeout simulado de WSFE.
- Rechazo simulado (error de validación).
- Reintento NO duplica comprobante.

## Frontend
1. Carga de SPA.
2. Navegación básica (router).
3. Acceso a vista principal de facturación.

## Base de Datos
- Conexión OK.
- Migraciones aplicables sin error.
