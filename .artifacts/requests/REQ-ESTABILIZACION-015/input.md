# REQ-ESTABILIZACION-015 - Stabilization Scan

## Contexto
Scan de estabilización (Clean Run).
Validación **Strict Anti-Stale** de menús. prohibido reutilizar referencias DOM.
Cada navegación debe ser atómica: Dashboard -> Expand -> Re-Query -> Click -> Dashboard.

## Objetivo
Garantizar que el menú es robusto bajo uso repetido y no depende de estado DOM transitorio.

## Alcance
-   **Runtime:** Admin (Mandatorio).
-   **Skill:** `ui-runtime-menu-scan` (Strict Anti-Stale Mode).
