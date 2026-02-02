# 🔧 Fix Description — HF-CLEAN-006

## Contexto
Flujo de Autenticación (`/login`).

## Problema Detectado
Error 422 Unprocessable Entity al intentar loguearse.
Discrepancia de Payload: Frontend enviaba `email` / `password`, Backend esperaba `usuario_email` / `usuario_password`.

## Causa Raíz
`LoginView.vue` importaba una instancia local de `LoginUseCase` (`@modules/Auth/di`) que inyectaba un Repositorio con lógica divergente o desactualizada, en lugar de usar el contenedor global (`@/di`) que tiene la configuración correcta de `AxiosAuthRepository`.

## Alcance de la Corrección
- Actualización de `LoginView.vue` para importar `loginUseCase` desde `@/di`.
- Unificación del grafo de dependencias.

## Validación
- Login exitoso con credenciales válidas.
- Redirección correcta al Dashboard.
