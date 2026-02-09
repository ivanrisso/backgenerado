# Hotfix Inventory

## Technical Hotfixes (Priority: CRITICAL)

### [HF-TECH-ROLES-IMPORT] Fix `Rol` Entity Import
- **Status:** DETECTED
- **Component:** `@modules/Auth`
- **Error:** Vite Build Error (Missing `Rol` entity).
- **Location:** `src/modules/Auth/ui/views/RolForm.vue` (Likely).
- **Impact:** Crash on `/roles`.

### [HF-TECH-MENUS-IMPORT] Fix `useMenuItems` Composable Import
- **Status:** DETECTED
- **Component:** `@modules/Auth` or `@shared`
- **Error:** Vite Build Error (Missing `useMenuItems`).
- **Location:** `src/modules/Auth/ui/views/MenuItemTree.vue`.
- **Impact:** Crash on `/menus`.

## Functional Hotfixes
- None detected (Issues are technical blockers).
