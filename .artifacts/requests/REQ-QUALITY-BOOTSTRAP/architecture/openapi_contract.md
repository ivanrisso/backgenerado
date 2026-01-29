# OpenAPI Contract Status

## Estado actual
- FastAPI genera OpenAPI dinámicamente.
- Existe openapi.yaml manual (posible drift).

## Riesgo
Desalineación FE/BE y documentación incorrecta.

## Recomendación
- Definir FastAPI como fuente de verdad.
- Generar OpenAPI automáticamente en CI.
- Usar openapi.yaml solo como snapshot/documentación.

## Próximo paso (futuro)
Comparación automática de diffs OpenAPI.
