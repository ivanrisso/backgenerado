# QA Failures & Observations

## 1. Authentication Barriers
The majority of the system is correctly behind `require_roles('admin')`.
- **Observation**: `audit_backend.py` yielded 401 for most endpoints.
- **Implication**: This confirms Security is active. However, it prevents automated "Deep Smoke" testing without a seeding/login step.

## 2. Public Endpoints Anomaly?
- `GET /api/v1/usuarios/` returned **200 OK**.
- **Risk**: User list might be public? Or the `audit_backend.py` environment has some default local config.
- **Action**: Verify if `Usuario` router has `dependencies=[Depends(require_roles...)]`.
    - *Check*: `usuario_routes.py` line 31: `@router.get("/", response_model=List[UsuarioResponse])`. **MISSING DEPENDENCY**.
    - **Critical Finding**: Users list is potentially public.

## 3. Orphans in Menu
Frontend has views for:
- `TipoDoc`
- `TipoImpuesto`
- `CondicionTributaria`
But these are **not** reachable via the customized `menu.ts`. Users cannot navigate to them easily.

## 4. Master Data Stability
- `CondicionTributaria` now returns 200 OK. Previous 500 fixed.
