# E2E Evidence - HF-FUNC-RBAC-CLIENTES

**Date:** 2026-02-04
**Result:** PASS

## Scenario
Verify non-admin user can access Client list in Recibos module.

## Verification Steps
1.  **User:** `newtester@gmail.com` (Non-admin).
2.  **Action:** Navigate to `/recibos`.
3.  **Check:** Inspect "Cliente" dropdown.
    -   **Expected:** List > 1 item (populated).
    -   **Actual:** 3 items found ("Todos", "pepe", "Test Hotfix...").
4.  **Network Check:**
    -   `GET /api/v1/clientes/` -> **200 OK**.
    -   No 403 Forbidden errors in console.

## Screenshot Evidence
*Refer to Browser Subagent recording `verify_rbac_fix`.*
