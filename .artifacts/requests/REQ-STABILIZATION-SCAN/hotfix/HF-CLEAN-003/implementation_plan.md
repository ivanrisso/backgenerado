# Implementation Plan - HF-CLEAN-003

## Goal Description
Fix system-wide crash caused by broken Dependency Injection container (`di.ts`) and specific import errors in `InvoiceCreateView.vue`. The goal is to restore the ability to load the "New Invoice" screen and ensure the application architecture correctly reflects the modular structure.

## Proposed Changes

### Frontend Infrastructure
#### [MODIFY] [di.ts](file:///home/irisso/proyectos/facturacion/frontend/src/di.ts)
- **Objective**: Redirect all Use Case imports from the obsolete `@app` alias to their correct `@modules` locations.
- **Specific Changes**:
    - **Clientes**: `@app/use-cases/GetClientesUseCase` -> `@modules/Clientes/application/GetClientesUseCase` (and related C/U/D uses cases).
    - **Auth**: `@app/use-cases/LoginUseCase` -> `@modules/Auth/application/LoginUseCase` (and Profile/Logout).
    - **Facturacion**: `@app/use-cases/GetComprobantesUseCase` -> `@modules/Facturacion/application/GetComprobantesUseCase`.
    - **Maestros**: Redirect all sub-folder imports:
        - `CondicionesTributarias` -> `@modules/Maestros/application/condiciontributaria/...`
        - `Paises` -> `@modules/Maestros/application/Pais/...`
        - `Provincias` -> `@modules/Maestros/application/Provincia/...`
        - `Localidades` -> `@modules/Maestros/application/Localidad/...`
        - `TiposDoc`, `TiposDom`, `TiposTel`, `Conceptos`, `Monedas`, `Ivas`, `TiposComprobante` -> `@modules/Maestros/application/...`

### Frontend Views
#### [MODIFY] [InvoiceCreateView.vue](file:///home/irisso/proyectos/facturacion/frontend/src/modules/Facturacion/ui/views/InvoiceCreateView.vue)
- **Objective**: Fix fragile relative imports and missing composables.
- **Specific Changes**:
    - Update relative paths `../../composables/...` to `@modules/...` aliases.
    - Replace `useCondicionIva` with `useCondicionesTributarias` (destructured with aliases).
    - Update `di` import to `@/di`.
    - Update `Money` import to `@domain/value-objects/Money`.

## Verification Plan

### Automated Tests
- `npm run build` (Frontend): Ensure checking for type errors or missing modules.

### Manual Verification
- **Login**: Verify login still works (depends on `di.ts`).
- **Invoice Create**: Navigate to `/comprobantes/nuevo`.
    - Success Criteria: View loads, no white screen, no console errors.
    - Interaction: Click "Cliente" dropdown to ensure `GetClientesUseCase` is wired correctly.
