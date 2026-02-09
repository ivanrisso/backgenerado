# UI Runtime Errors

## Critical Technical Failures (Vite/Bundler)

### 1. `/roles`
- **Action:** Direct Navigation / Menu Click
- **Error:** `Failed to resolve import "../../../domain/entities/Rol" from "src/modules/Auth/ui/views/RolForm.vue"`
- **Type:** HOTFIX_TECNICO

### 2. `/menus`
- **Action:** Direct Navigation / Menu Click
- **Error:** `Failed to resolve import "@ui/composables/auth/useMenuItems" from "src/modules/Auth/ui/views/MenuItemTree.vue"`
- **Type:** HOTFIX_TECNICO

### 3. `/domicilios`
- **Action:** Direct Navigation (Route exists, Missing from Menu)
- **Error:** `Failed to resolve import "@modules/Maestros/composables/useDomicilios" from "src/modules/Maestros/ui/views/DomicilioView.vue"`
- **Type:** HOTFIX_TECNICO

## API / Integration Errors

### 4. `/recibos/nuevo`
- **Action:** Open Form
- **Error:** 401 Unauthorized / AxiosError (Session Instability)
- **Type:** HOTFIX_TECNICO (Auth state handling)
