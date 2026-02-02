# Implementation Plan - HF-CLEAN-004

## Goal Description
Fix infinite loading loops and watcher errors in `ProvinciaView.vue` and `LocalidadView.vue`. The goal is to stabilize the Master Data screens by ensuring watchers do not execute logic on null/undefined values during initialization.

## Proposed Changes

### Frontend Views
#### [MODIFY] [ProvinciaView.vue](file:///home/irisso/proyectos/facturacion/frontend/src/modules/Maestros/ui/views/ProvinciaView.vue)
- **Objective**: Prevent watcher execution when dependent interactions (like Country selection) haven't occurred or are resetting.
- **Specific Changes**:
    - Add `if (!val) return;` guard clauses to watchers monitoring prop/data changes.
    - Ensure safe access to properties within watcher callbacks.

#### [MODIFY] [LocalidadView.vue](file:///home/irisso/proyectos/facturacion/frontend/src/modules/Maestros/ui/views/LocalidadView.vue)
- **Objective**: Prevent watcher execution when dependent interactions (like Province selection) haven't occurred.
- **Specific Changes**:
    - Add `if (!val) return;` guard clauses to watchers.

## Verification Plan

### Automated Tests
- `npm run build` (Frontend): Ensure checking for type errors.

### Manual Verification
- **Maestros -> Provincias**:
    - Navigate to `/provincias`.
    - Verify grid loads or empty state appears without console errors.
    - Test "Filtrar por País" (if applicable) to ensure watcher triggers correctly only when valid.
- **Maestros -> Localidades**:
    - Navigate to `/localidades`.
    - Verify grid loads.
