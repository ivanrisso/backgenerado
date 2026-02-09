# UI Runtime Errors

## Critical
- **Ruta:** `/` (Dashboard)
- **Error:** Redirects to `/usuarios`.
- **Status:** 403 Forbidden (for Role: Operador).
- **Impact:** User lands on an error page immediately after login.
- **Class:** HOTFIX_TECNICO (HF-TECH-DEFAULT-ROUTE).

## Non-Critical
- `GET /api/v1/auth/me` 401: Expected / Handled.
