# SKILL — CI Validation

## Rol autorizado
- Release Manager

## Objetivo
Verificar que CI pase completamente.

Debe verificar explícitamente:
- Backend job: PASS
- Frontend job: PASS

Debe fallar si:
- algún job no existe
- algún job está SKIPPED
- el pipeline no se ejecutó en esta corrida

