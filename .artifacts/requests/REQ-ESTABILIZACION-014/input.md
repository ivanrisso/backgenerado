# REQ-ESTABILIZACION-014 - Stabilization Scan

## Contexto
Scan de estabilización (Clean Run).
Validación estricta **iterativa** de menús usando el skill `ui-runtime-menu-scan` actualizado.

## Objetivo
Validar que todos los submenús se puedan abrir y navegar repetidamente.
Evitar falsos positivos de "menú ya abierto".

## Alcance
-   **Runtime:** Admin (Mandatorio).
-   **Skill:** `ui-runtime-menu-scan` (Iterative Mode).
