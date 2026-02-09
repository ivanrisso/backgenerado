# REQ-ESTABILIZACION-016 - Stabilization Scan

## Contexto
Scan de estabilización (Clean Run).
Validación **Strict Completitud** de menús.
Regla CRÍTICA: "Un menú padre NO puede considerarse validado hasta que TODOS sus subítems visibles hayan sido navegados individualmente".

## Objetivo
Garantizar exhaustividad total en la navegación del menú.
Pasar el Gate Anti-Pass Incompleto.

## Alcance
-   **Runtime:** Admin (Mandatorio).
-   **Skill:** `ui-runtime-menu-scan` (Strict Completitud Mode).
-   **Target:** Facturación, Tesorería, Clientes, Maestros, Sistema.
