# Análisis de Impacto: REQ-FUNC-004

## Componentes Afectados
1. **Frontend:**
   - `useUserMenu.ts`: Responsable de transformar la lista plana en árbol.
   - `Sidebar.vue`: Consumidor de la estructura de árbol.
2. **Backend:**
   - No se prevén cambios (el endpoint ya retorna `parent_id`).

## Riesgos
- **Regresión:** Si la lógica de árbol falla, el menú podría quedar vacío o inutilizable.
- **Ciclos Infinitos:** Si hay referencias circulares en `parent_id` (improbable pero posible).

## Estrategia de Solución
- Revisar y robustecer `buildTree` en `useUserMenu.ts`.
- Asegurar conversión de tipos (ids comparados como strings/números de forma segura).
- Manejar casos de huérfanos (ítems con `parent_id` que no existe en la lista).

## Esfuerzo Estimado
- **Bajo (XS):** Corrección lógica en JS/TS.

## Plan de Pruebas
- Verificar visualmente la anidación.
- Verificar que los padres se pueden expandir/colapsar.
- Verificar navegación en hojas (hijos).
