# Auth Issues

## RBAC Status
- **Usuario Routes**: Patched to allow authenticated access to `/me/menu`.
- **Cliente Routes**: Patched to allow read access to non-admins (verified in Scan 006).

## Potential Issues
- Granularity of permissions in `MenuItem` vs `Role`.
- Frontend role logic (`auth.ts`) must match backend Token claims.
