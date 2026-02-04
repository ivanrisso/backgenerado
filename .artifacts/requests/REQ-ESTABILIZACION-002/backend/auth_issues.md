# Problemas de Autenticación

**Estado:** En análisis...

## Riesgos Potenciales
- `endpoints_inventory.md` muestra múltiples endpoints CRUD. Se debe verificar si el RBAC se aplica en todos ellos (Ver decoradores `@Roles` en el código o 403 en tiempo de ejecución).
- `/comprobantes/full` requiere validación pesada (interacción CAE).
