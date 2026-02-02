# Evidencia de Testing - HF-CLEAN-009

## Test Case: Cold Start Login
**ID**: TC-AUTH-009
**Tipo**: Manual / Exploratorio (Automatizado por Agente)
**Componente**: `LoginView` (State Hydration)

### Pre-condiciones
- Usuario desconectado (Logout).
- Store vacío (`user: null`).

### Pasos
1. Ingresar credenciales.
2. Clic en Ingresar.
3. Verificar si redirige o se queda en el login.

### Resultado Deseado
- Redirección en el primer intento.

### Resultado Obtenido
- Redirección exitosa a `/usuarios` (Root).
- No fue necesario "segundo intento".

**Veredicto**: PASS
**Ejecutado por**: Antigravity
**Fecha**: 2026-02-02
