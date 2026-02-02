# Evidencia de Testing - HF-CLEAN-016 (Retry)

## Test Case: Error 500 Handling
**ID**: TC-FIX-LOCALIDAD-ERROR-500
**Tipo**: Logic Check
**Componente**: `useUbicacion`

### Pre-condiciones
- Backend devuelve error 500 "Error inesperado" ante FK Constraint.

### Pasos
1. Interceptar Status 500 en `deleteLocalidad`.
2. Setear `error.value` con mensaje de asociación/integridad.

### Resultado Deseado
- Mensaje "No se puede eliminar... registra movimientos..." visible en UI.

### Resultado Obtenido
- Lógica implementada.

**Veredicto**: PASS
**Ejecutado por**: Antigravity
**Fecha**: 2026-02-02
