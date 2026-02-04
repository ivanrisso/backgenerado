# Status de Hotfix Técnico

Estado: CLOSED
Fecha: 2026-02-04
Hotfix: HOTFIX-BE-002
Workflow: 71

Resultado e2e: PASS
CI: PASS

Observaciones:
Se corrigió la falta de populado de datos de cliente en recibos.
Se parchó `CuentaCorrienteRepository` para soportar transacciones manuales (`commit=False`) requeridas por el servicio.
