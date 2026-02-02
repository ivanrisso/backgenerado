---
description: Workflow 80 — System Coverage & CRUD Verification (CRÍTICO)
---

# Workflow 80 — System Coverage & CRUD Verification (CRÍTICO)

## Objetivo
Detectar de forma automática y auditable:
- Endpoints existentes vs usados
- Menús faltantes o inconsistentes
- Rutas huérfanas
- CRUDs incompletos o rotos
- Errores backend que rompen UI

Este workflow NO ejecuta clicks de navegador.
Se basa en análisis estructural + pruebas funcionales dirigidas.

---

## REQ recomendado
REQ-SYSTEM-COVERAGE-001

---

## Stage A — API Inventory (Backend)

Responsable: Architect + Backend Agent

Acciones:
- Recorrer `app/routes/**`
- Detectar todos los endpoints REST
- Clasificar por:
  - entidad
  - operación (list, get, create, update, delete)
- Detectar endpoints sin tests

Artifacts:
- `architecture/api_inventory.md`
- `architecture/api_orphans.md`

---

## Stage B — UI Coverage (Frontend)

Responsable: Frontend Architect

Acciones:
- Recorrer:
  - router
  - layouts
  - guards
  - configuración de menú
- Mapear:
  - ruta UI → entidad
  - ruta UI → endpoint backend
- Detectar:
  - rutas sin menú
  - menú sin backend
  - pantallas huérfanas

Artifacts:
- `ui/menu_coverage.md`
- `ui/orphan_routes.md`

---

## Stage C — CRUD Verification (QA)

Responsable: QA Agent

Acciones:
- Para cada entidad detectada:
  - CREATE → POST payload mínimo válido
  - READ   → GET list / GET by id
  - UPDATE → PUT parcial
  - DELETE → DELETE lógico/físico
- Usar:
  - base de datos de test
  - datos mock
  - AFIP deshabilitado
- Registrar errores exactos (500, 404, 401)

Artifacts:
- `qa/crud_matrix.md`
- `qa/crud_failures.md`

---

## Stage D — UI Smoke (Opcional)

Responsable: Frontend QA

Acciones:
- Verificar que cada ruta:
  - monta sin error JS
  - no lanza excepción fatal
- NO navegación automática

Artifacts:
- `qa/ui_smoke.md`

---

## Gate — System Integrity

Checklist:
- No endpoints huérfanos críticos
- CRUDs core (Clientes, Usuarios, Facturas) funcionales
- Backend no devuelve 500 en flujos base
- Auth consistente

Resultado:
- PASS → habilita nuevos features
- FAIL → bloqueo de evolución

Checklist aplicado:
`.agent/checklists/gate_system_integrity.md`
