# Alembic Playbook

## Objetivo
Estandarizar el manejo de schema DB.

## Flujo recomendado
1. Crear migración:
   alembic revision -m "descripcion"
2. Editar script (no autogenerate a ciegas).
3. Aplicar:
   alembic upgrade head
4. Rollback (si aplica):
   alembic downgrade -1

## Scripts sueltos
- Identificar scripts legacy.
- Documentar su uso.
- No ejecutarlos en CI sin validación.

## Regla dura
No se usa `drop_all` ni `reset_db` sin aprobación explícita.
