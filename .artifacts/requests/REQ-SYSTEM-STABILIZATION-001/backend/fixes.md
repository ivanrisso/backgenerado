# Backend Fixes Report

## Security Hotfix: Usuario Routes
- **Issue**: `GET /api/v1/usuarios/` and other user endpoints were publicly accessible.
- **Fix**: Added `dependencies=[Depends(require_roles("admin"))]` to the `APIRouter` initialization in `app/routes/usuario_routes.py`.
- **Verification**: `audit_backend.py` v2 confirms endpoints now return `401 Unauthorized`.

## Master Data Seeds
- **Status**: `seed_dev_fiscal.py` previously executed and `CondicionTributaria` endpoints verified as `200 OK`. No additional seeding was required for critical paths.
