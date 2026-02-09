# HF-TECH-RECIBO-CREATE-500

## Problema
El endpoint `POST /api/v1/recibos/` devuelve un error **500 Internal Server Error** al intentar crear un recibo válido.

## Síntoma Runtime
-   El usuario completa el formulario de "Nuevo Recibo".
-   Al hacer click en "Crear Recibo", la operación falla silenciosamente en UI o muestra error genérico.
-   En consola de red se observa el 500.

## Causa Probable (Hipótesis)
Revisión necesaria de logs del backend. Posibles causas:
1.  Error en `ReciboService.create_recibo`.
2.  Problema de integridad referencial (Cliente, Cuenta Corriente).
3.  Error al generar el número de comprobante.
4.  Fallo en la persistencia (commit).

## Evidencia
Browser Subagent reporta: "Al intentar crear el recibo 'Test Scan 007' ... el backend respondió con un 500 Internal Server Error".
