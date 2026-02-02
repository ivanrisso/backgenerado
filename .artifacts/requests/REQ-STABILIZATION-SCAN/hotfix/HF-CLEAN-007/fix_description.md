# 🔧 Fix Description — HF-CLEAN-007

## Contexto
Login.

## Problema Detectado
Inconsistencia histórica en redirección automática post-login (aunque exitoso en última prueba, es un riesgo latente).

## Causa Raíz
Posible race condition en `router.push` vs Auth Guard.

## Alcance de la Corrección
Blindar la lógica de redirección en `LoginView.vue`.

## Archivos / Capas Afectadas
- `src/modules/Auth/ui/views/LoginView.vue`

## Restricciones
- No romper CI.

## Validaciones Esperadas
- Redirección 100% fiable.

## Notas
Este archivo **NO ejecuta correcciones**.  
Es input directo del Workflow 71.
