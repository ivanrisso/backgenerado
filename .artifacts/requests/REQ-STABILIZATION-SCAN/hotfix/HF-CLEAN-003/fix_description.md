# 🔧 Fix Description — HF-CLEAN-003

## Contexto
Facturación Electrónica (`/comprobantes/nuevo`).

## Problema Detectado
Crash sistémico Javascript. La aplicación no carga (`Blank Screen` o errores de consola).

## Causa Raíz
Fallo masivo de Inyección de Dependencias en `di.ts`.
- Imports apuntando a rutas inexistentes.
- UseCases sin instanciar (`CreateComprobanteFullUseCase`).
- Referencias rotas a RBAC.

## Alcance de la Corrección
- Reescritura completa de `di.ts`.
- Mapeo de `CreateComprobanteFullUseCase`.
- Corrección de imports en vistas.

## Validación
- Carga de formulario de factura sin errores.
