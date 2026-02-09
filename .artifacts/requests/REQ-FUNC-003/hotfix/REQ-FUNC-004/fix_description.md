# Fix Description — HF-FUNC-004

## Origen
Corrección funcional iniciada por decisión humana.
Problema detectado fuera del Workflow 70 durante validación manual de UI.

## Contexto
Sistema de navegación (sidebar).
Gestión de Menú mediante CRUD de Menús.

## Síntoma observable
Al aplicar una corrección funcional sobre el sistema de menús, los ítems que
deberían renderizarse como **submenús** aparecen en runtime como
**ítems de primer nivel** del sidebar.

El árbol de navegación visible no respeta la jerarquía definida
en la configuración de menús.

## Comportamiento actual (incorrecto)
- Ítems hijos se renderizan como menús principales.
- El sidebar pierde jerarquía visual y funcional.
- Se exponen entradas duplicadas o fuera de contexto.
- La navegación resulta confusa para el usuario.

## Comportamiento esperado (correcto)
- Los ítems de menú respetan la jerarquía definida:
  - Menús principales como contenedores.
  - Submenús renderizados únicamente dentro de su menú padre.
- El sidebar refleja fielmente la estructura configurada en el sistema de menús.
- No existen ítems de primer nivel que conceptualmente no lo sean.

## Impacto funcional
- Confusión en la navegación.
- Dificultad para descubrir funcionalidades reales.
- Riesgo de uso incorrecto del sistema.
- Inconsistencia entre configuración y UI visible.

## Evidencia asociada
- Validación manual de UI (sidebar).
- Configuración correcta observada en el CRUD de Menús.
- Render incorrecto observado en runtime tras la corrección funcional.

## Alcance del fix
Este hotfix aborda **únicamente** la representación funcional del menú.
No incluye:
- cambios técnicos de infraestructura,
- refactor general,
- nuevas funcionalidades.

## Nota de gobierno
Este hotfix es de tipo **FUNCIONAL / PRODUCTO**.
Su corrección debe ejecutarse exclusivamente mediante **Workflow 72**.
