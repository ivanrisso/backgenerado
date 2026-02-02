# Evidencia de Testing - HF-CLEAN-006

## Test Case: Login Payload Correction
**ID**: TC-AUTH-006
**Tipo**: Manual / Exploratorio (Automatizado por Agente)
**Componente**: `LoginView` + `AxiosAuthRepository`

### Pre-condiciones
- Backend online.
- Hotfix 006 aplicado (Corrección de DI en LoginView).

### Pasos
1. Navegar a `/login`.
2. Ingresar credenciales válidas.
3. Hacer clic en "Ingresar".

### Resultado Deseado
- No aparece error `422 Unprocessable Entity` en Network panel.
- Redirección exitosa a ruta autenticada.

### Resultado Obtenido
- Request API: 200 OK.
- Redirección: Correcta (`/usuarios`).

**Veredicto**: PASS
**Ejecutado por**: Antigravity
**Fecha**: 2026-02-02
