# Status de Hotfix Funcional

Estado: CLOSED
Fecha: 2026-02-04
Hotfix: HF-GAP-001
Workflow: 72

Resultado e2e: PASS
CI: PASS

Observaciones:
Se implementó soporte para imputación parcial mediante el campo `importe_imputar` en `CbteAsoc`.
Se validó que el sistema respete los saldos y rechace imputaciones excesivas (HTTP 400).
Se aseguró retrocompatibilidad (imputación automática si no se envia el campo).
