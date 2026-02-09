# Prompt de Corrección: HF-TECH-DEFAULT-ROUTE

## Contexto
El usuario Operador recibe un error 403 al ingresar a `/` porque redirige a `/usuarios` (solo Admin).

## Objetivo
Cambiar el redirect default en `frontend/src/router/index.ts`.

## Instrucciones
1. Editar `frontend/src/router/index.ts`.
2. Ubicar ruta `path: '/'`.
3. Cambiar `redirect: '/usuarios'` por `redirect: '/recibos'` O crear una vista de Dashboard real.
   - *Nota:* Para este hotfix, apuntar a `/recibos` es aceptable si el Dashboard no está listo.

## Verificación
1. Login como `newtester`.
2. Ir a `/`.
3. Verificar que redirige a una página válida (no 403).
