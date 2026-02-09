# Checklist — Stabilization Scan
# Workflow 70

## Objetivo

Validar que el sistema fue **completamente relevado, clasificado y documentado**
antes de permitir **cualquier corrección técnica o funcional**.

Este checklist es **bloqueante** y se evalúa en el **Stage J — Gate** del Workflow 70.

---

## 1️⃣ Inventarios Técnicos (OBLIGATORIO)

Marcar PASS solo si **TODOS** existen y tienen contenido explícito:

- [ ] `architecture/routes_inventory.md`
- [ ] `architecture/view_load_report.md`
- [ ] `architecture/lazy_import_issues.md`
- [ ] `ui/crud_matrix.md`
- [ ] `backend/endpoints_inventory.md`

❌ FAIL si falta alguno  
❌ FAIL si algún archivo está vacío o incompleto

---

## 2️⃣ Runtime Scan (solo si `execution_mode = hybrid`)

### Evidencia obligatoria

- [ ] `qa/stabilization_evidence.md`
- [ ] `ui/menu_runtime_report.md`
- [ ] `ui/ui_runtime_errors.md` (si hubo errores)

### Validaciones críticas

- [ ] Todas las rutas fueron navegadas
- [ ] Todas las vistas lazy-loaded fueron cargadas
- [ ] No existen overlays de error (Vite / runtime)
- [ ] Todos los menús padres fueron expandidos
- [ ] Todos los subítems fueron navegados con evidencia explícita

❌ FAIL si falta evidencia  
❌ FAIL si existe navegación parcial  
❌ FAIL si algún submenú no fue recorrido

---

## 3️⃣ Clasificación de Issues (OBLIGATORIO)

- [ ] Todos los issues detectados están clasificados
- [ ] No existen issues sin categoría
- [ ] Cada issue pertenece a **una sola** categoría:
  - Hotfix Técnico
  - Gap Funcional / Producto

❌ FAIL si existe un issue sin clasificar  
❌ FAIL si un issue tiene doble clasificación

---

## 4️⃣ Hotfixes Técnicos (si fueron detectados)

Para **cada** `hotfix/HF-TECH-XXX/`:

- [ ] Existe la carpeta del hotfix
- [ ] Existe `fix_description.md`
- [ ] Existe `analysis.md`
- [ ] Existe `metadata.md`

❌ FAIL si falta cualquiera  
❌ FAIL si existe hotfix técnico sin documentación completa

---

## 5️⃣ Gaps Funcionales / Producto

Para **cada** gap funcional detectado:

- [ ] Existe `gaps/GAP-XXX/`
- [ ] Existe `fix_description.draft.md`
- [ ] Existe `metadata.draft.md`

❌ FAIL si existe gap sin drafts  
❌ FAIL si un gap habilita ejecución automática

---

## 6️⃣ Gobierno y Priorización

- [ ] Existe `hotfix/ORDER.md`
- [ ] Todos los hotfixes técnicos están incluidos en `ORDER.md`
- [ ] No existen hotfixes técnicos fuera del orden definido

❌ FAIL si falta ORDER.md  
❌ FAIL si el orden no coincide con los hotfixes detectados

---

## Resultado del Checklist

### PASS

- El sistema queda **habilitado** para:
  - Workflow 71 — Hotfix Técnico
  - Workflow 72 — Hotfix Funcional / Producto
  - Workflow 03 — Feature Evolution

---

### FAIL

- Se bloquea la ejecución de:
  - Workflow 71
  - Workflow 72
  - Workflow 03

---

## Regla Final

**Sin checklist PASS, no se toca código.**  
**Sin evidencia persistida, no hay corrección.**  
**Workflow 70 detecta y prepara.**
