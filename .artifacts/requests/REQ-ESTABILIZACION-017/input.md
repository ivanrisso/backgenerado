# REQ-ESTABILIZACION-017 - Stabilization Scan (Strict Skills)

## Contexto
Scan de estabilización (Clean Run).
Re-ejecución tras consolidación de skills.
Uso ESTRICTO de skills activas en `skills/active/workflow-70`.

## Objetivo
Garantizar estabilidad operativa.
Validación de Menu Consistency y Runtime Scan.

## Alcance
-   **Runtime:** Admin (Mandatorio).
-   **Skills Autorizadas:** `route-inventory-scan`, `frontend-crud-detection`, etc.
-   **Target:** Facturación, Tesorería, Clientes, Maestros, Sistema.

## Nota
Al no existir `ui-runtime-menu-scan`, se utilizará el procedimiento manual documentado en el Runbook (Stage E) o `frontend-crud-detection` si aplica.
