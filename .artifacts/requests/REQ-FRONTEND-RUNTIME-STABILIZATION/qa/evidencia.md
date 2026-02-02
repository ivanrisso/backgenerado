# Evidencia de Estabilización Runtime (Error Handling & Auth)

**Fecha:** 30/01/2026
**Responsable:** Senior Frontend Architect + API Integrator
**Request:** REQ-FRONTEND-RUNTIME-STABILIZATION

## 1. Validación de Flujo de Autenticación
### Check de Auditoría
- **Mecanismo Detectado:** `Cookie-based Auth` (`withCredentials: true` en Axios).
- **Token Injection:** No se requiere header `Authorization: Bearer ...` manual ya que el navegador gestiona la cookie `access_token` automáticamente.
- **Login Flow:** El store llama a `/auth/login`, recibe la cookie, y luego verifica identidad con `/auth/me`.
- **401 Handling:** `AxiosClient` intercepta 401 y limpia `localStorage` para forzar re-evaluación de estado en Guards.

**Conclusión:** El flujo es seguro y correcto para la arquitectura actual (Session Cookies).

## 2. Hardening de Composables
Se detectaron composables que ejecutaban llamadas a API sin bloques `try/catch` en sus métodos de carga (`load*`), lo que causaba excepciones no capturadas durante el ciclo de vida de los componentes (`onMounted`).

### Modificaciones Realizadas

#### A. `useUbicacion.ts` (CRÍTICO)
Este composable es usado por múltiples vistas (`DomicilioView`, `LocalidadView`, etc.).
- **Problema:** `await repo.getAll()` lanzaba excepción si el backend retornaba 401 o 500, rompiendo la vista.
- **Solución:** Se envolvieron `loadPaises`, `loadProvincias` y `loadLocalidades` en `try/catch`. En caso de error, se asigna array vacío `[]` y se loguea el error, permitiendo que la vista se monte vacía.

#### B. `useTiposTel.ts`
- **Problema:** Mismo patrón de fallo al cargar tipos de teléfono.
- **Solución:** Implementación de `try/catch` y estado seguro de error.

#### C. Otros Composables
Se verificó que `useCondicionesTributarias`, `useTiposImpuesto` y `useTiposDoc` ya contaban con manejo de errores adecuado (`error.value = ...`).

## 3. Verificación de Aislamiento de Vistas
Debido al hardening, si una llamada de red falla (ej. 401 por sesión expirada):
1. El composable captura el error.
2. Setea `loading = false` y `data = []`.
3. La vista (`.vue`) detecta el fin de carga y renderiza su estado vacío o tabla vacía, en lugar de crashear (pantalla blanca).
4. El interceptor global de Axios puede redirigir a login si corresponde, pero la UI no explota.

## 4. Calidad de Código
- **Type Check:** `npm run typecheck` 🟢 EXITOSO.
- **Linting:** `npm run lint` 🟢 EXITOSO (Se corrigieron variables no usadas en `useUbicacion` usando prefix `_`).

## 5. Estado Final
El frontend es robusto ante fallos de red iniciales en el módulo Maestros.
