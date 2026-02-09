# Plan de Implementación - HF-TECH-ROLES-IMPORT

## Descripción del Problema
La vista de Roles (`/roles`) falla al cargar debido a un error de importación estática en el componente `RolForm.vue`. El path `../../../domain/entities/Rol` no resuelve correctamente.

## Cambios Propuestos

### Frontend
#### [MODIFICAR] [RolForm.vue](file:///home/irisso/proyectos/facturacion/frontend/src/modules/Auth/ui/views/RolForm.vue)
- Reemplazar el import relativo roto por el alias `@domain/entities/Rol`.

## Plan de Verificación

### Tests Manuales
1. Login como Admin.
2. Navegar a `/roles`.
3. Verificar que la vista carga y se muestra la lista (o formulario vacío) sin error de Vite.
