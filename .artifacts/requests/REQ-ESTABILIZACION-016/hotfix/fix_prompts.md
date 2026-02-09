# Fix Prompts (For Workflow 71)

## Prompt 1: Fix Roles Import
```text
CONTEXT:
The route `/roles` crashes with a Vite error: "Missing 'Rol' entity".
Use `find_by_name` to locate `Rol.ts` (domain definition).
Check `src/modules/Auth/ui/views/RolList.vue` or `RolForm.vue`.
Verify imports (e.g. `import type { Rol } ...`).
Fix the path or export.
Verify by running strict_menu_scan on /roles.
```

## Prompt 2: Fix Menus Import
```text
CONTEXT:
The route `/menus` crashes with a Vite error: "Missing 'useMenuItems'".
Use `find_by_name` to locate `useMenuItems.ts`.
Check `src/modules/Auth/ui/views/MenuItemTree.vue`.
Adjust import path (e.g. `@shared/composables` vs `@modules/Auth/composables`).
Verify by running strict_menu_scan on /menus.
```
