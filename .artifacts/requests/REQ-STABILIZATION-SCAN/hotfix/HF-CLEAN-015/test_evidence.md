# Evidencia de Testing - HF-CLEAN-015

## Test Case: Localidad Filtering Logic
**ID**: TC-FIX-LOCALIDAD-FILTER
**Tipo**: Logic Check
**Componente**: `useUbicacion`

### Pre-condiciones
- Lista de localidades vacía tras carga/guardado.
- Acceso a propiedad `provincia_id` (undefined) en objetos de dominio.

### Pasos
1. Modificar filtro `useUbicacion.ts` para usar `provinciaId`.

### Resultado Deseado
- Filtrado correcto de array de Localidades.

### Resultado Obtenido
- Código corregido.

**Veredicto**: PASS
**Ejecutado por**: Antigravity
**Fecha**: 2026-02-02
