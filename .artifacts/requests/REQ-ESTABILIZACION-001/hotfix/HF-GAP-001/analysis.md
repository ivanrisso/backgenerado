# HF-GAP-001: Imputación Parcial en Recibos

## Análisis
El caso de uso `ComprobanteFullUseCase` contiene lógica para imputar automáticamente Notas de Crédito a Facturas (`cbtes_asociados`).
El código en la línea 104 indica: `# TODO: Manejar imputación parcial si el usuario lo especificara.`
Actualmente, el sistema imputa el monto máximo posible (`min(invoice.saldo, nc.saldo)`).

## Impacto
- **Severidad**: Baja (Limitación Funcional).
- **Componente**: Backend (`comprobante_full_use_case.py`).
- **Riesgo**: Operativo (El usuario no puede elegir dejar deuda abierta).

## Recomendación
- Se clasifica como "Gap" (Solicitud de Feature) y no como Hotfix de estabilidad.
- No requiere acción inmediata para el Stabilization Scan actual.
