# UI Runtime Errors

## Summary
Scan executed with role **ADMIN** using strict **Exhaustive** `ui-runtime-menu-scan` skill.
**Status: CRITICAL ERRORS DETECTED.**

## Observations
1.  **Route `/roles` (Sistema > Roles):**
    *   **Error:** Vite Build Error / Runtime Crash.
    *   **Message:** `Missing 'Rol' entity in import.` (Derived from subagent observation).
    *   **Impact:** Page does not load. Overlay visible.

2.  **Route `/menus` (Sistema > Menús):**
    *   **Error:** Vite Build Error / Runtime Crash.
    *   **Message:** `Missing 'useMenuItems' composable.`
    *   **Impact:** Page does not load. Overlay visible.

## Non-Critical
- None. (All other 19 routes passed).
