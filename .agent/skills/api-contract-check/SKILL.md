# SKILL — API Contract Check

## Rol autorizado
- QA
- Backend Engineer

## Objetivo
Verificar que las llamadas reales del frontend al backend cumplen el contrato esperado.

## Inputs
- OpenAPI
- Llamadas reales observadas

## Pasos
1. Observar requests desde UI.
2. Verificar status HTTP.
3. Detectar:
   - 500 inesperados
   - contratos rotos
   - endpoints inexistentes

## Output
- `backend/api_runtime_report.md`

## Restricciones
- No modificar endpoints.
