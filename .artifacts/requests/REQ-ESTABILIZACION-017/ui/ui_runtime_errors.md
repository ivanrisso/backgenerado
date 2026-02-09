# UI Runtime Errors

## Critical Failures

### 1. Roles View (`/roles`)
- **Error:** `Failed to resolve import "../../../domain/entities/Rol" from "src/modules/Auth/ui/views/RolForm.vue".`
- **Location:** `src/modules/Auth/ui/views/RolForm.vue`
- **Type:** Vite Build Error (Import Analysis)
- **Impact:** View crash. Navigation blocked.
- **Root Cause:** Incorrect relative path. Resolves to `src/modules/domain/...` instead of `src/domain/...`.

### 2. Menus View (`/menus`)
- **Error:** `Failed to resolve import` (Presumed `MenuItem` or `Rol` dependency).
- **Location:** `src/modules/Auth/ui/views/MenuItemTree.vue`
- **Type:** Vite Build Error (Import Analysis)
- **Impact:** View crash. Navigation blocked.
- **Root Cause:** Incorrect relative path for `MenuItem` import.

## Non-Critical
- None observed (Navigation to other 19 items was successful).
