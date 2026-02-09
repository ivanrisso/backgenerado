# Implementation Plan - HF-TECH-DEFAULT-ROUTE

## Goal Description
Fix the 403 Forbidden error experienced by non-admin users (e.g., Operador) when landing on the root URL `/`. Currently, it redirects to `/usuarios`, which is admin-restricted. It should redirect to a common accessible route.

## Proposed Changes
### Frontend
#### [MODIFY] [index.ts](file:///home/irisso/proyectos/facturacion/frontend/src/router/index.ts)
- Change default redirect from `/usuarios` to `/recibos`.
- Rationale: `/recibos` is accessible by `Operador` and `Cobranzas`.

## Verification Plan
### Manual Verification
1. Login as `newtester@gmail.com`.
2. Navigate to `/`.
3. Verify redirect to `/recibos` (HTTP 200).
4. Verify no 403 error.
