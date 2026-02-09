# Análisis de Impacto: REQ-FUNC-005

## Componentes Afectados
1. **Base de Datos:**
   - Tabla `menuitem`: Se debe insertar el registro faltante (ID 4 - Seguridad).
   - Tabla `rolmenuitem`: Se debe asignar permisos de este nuevo ítem a los roles correspondientes (Admin).

## Riesgos
- **Conflicto de IDs:** Si el ID 4 ya fuera usado por otro proceso (aunque el chequeo dijo que no existe). Se forzará ID 4 para mantener integridad con hijos.
- **Cache:** Si el backend cachea menús, podría requerir reinicio (FastAPI no cachea por defecto queries, ok).

## Estrategia de Solución
- Script Python (`fix_seguridad_menu.py`) para:
  1. Verificar si ID 4 existe.
  2. Si no, insertarlo como `parent_id=None`, `nombre='Seguridad'`.
  3. Asociarlo al Rol Admin.

## Esfuerzo Estimado
- **Bajo (XS):** Data fix script.

## Plan de Pruebas
- Ejecutar script.
- Verificar API response (debe incluir Seguridad).
- Verificar Sidebar (debe mostrar grupo Seguridad con hijos).
