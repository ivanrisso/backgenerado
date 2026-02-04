---
description: Entregar features por slices verticales con PRD, ADR, evidencia y no-regresión.
---

---
name: feature-evolution
version: 2.0.0
workflow_type: feature
domain: facturacion
jurisdiction: AR-AFIP
purpose: >
  Entregar nuevas funcionalidades mediante slices verticales,
  con PRD, ADR, implementación controlada, validación funcional
  y evidencia de no-regresión, sobre una base técnica estable.
entrypoint: false
artifacts:
  root: .artifacts/requests
constraints:
  - fiscal_changes_require_adr
  - idempotent_emission_required
  - no_technical_hotfixes_allowed
---

# Workflow 03 — Feature Evolution (Facturación AR)

## Propósito

Desarrollar **features nuevas o ampliaciones funcionales**
sobre un sistema **técnicamente estable**, garantizando:

- Gobierno funcional
- Cumplimiento fiscal AFIP
- Trazabilidad de decisiones
- Evidencia de no-regresión

⚠️ Este workflow **NO corrige errores técnicos**  
⚠️ Este workflow **NO estabiliza el sistema**

---

## Cuándo usar este workflow

✔️ Feature nueva  
✔️ Cambio funcional validado por negocio  
✔️ Nueva pantalla / flujo / regla  
✔️ Ampliación de comportamiento existente  

✔️ Cambio funcional aprobado y definido  
✔️ Comportamiento nuevo o ampliado  

❌ Crash  
❌ Error técnico  
❌ Import roto  
❌ Loop / watcher  
❌ 401 / 500 técnicos  

❌ Corrección funcional reactiva  
❌ Bug funcional detectado en producción  

👉 Correcciones funcionales reactivas o bugs funcionales existentes
   se gestionan exclusivamente mediante **Workflow 72**.


---

## Precondiciones (NO negociables)

- Workflow 70 ejecutado **y en PASS**
- No hotfix técnicos abiertos
- Base navegable y estable

---

## Roles involucrados

- **Product Owner** — definición funcional
- **Domain Guardian** — reglas fiscales / negocio
- **Arquitecto** — impacto técnico + ADR
- **Backend Engineer** — implementación backend
- **Frontend Engineer** — implementación UI
- **QA** — validación funcional y no-regresión
- **Security** — controles y cumplimiento
- **Reviewer** — gates y aprobación

---

## Stage 1 — Descubrimiento Funcional (PRD)

**Roles:** Product Owner + Domain Guardian  

### Objetivo
Definir **qué se va a construir y por qué**.

### Artefactos
- `prd.md`
- `user_stories.md`
- `reglas_fiscales_ar.md` (si aplica)

### Gate
- `gate_prd.md`

**Criterio de PASS**
- Alcance claro
- No contradice reglas fiscales
- No intenta resolver errores técnicos

---

## Stage 2 — Impacto & Decisiones (ADR)

**Roles:** Arquitecto + Security  

### Objetivo
Evaluar impacto técnico, fiscal y operativo **antes de tocar código**.

### Artefactos
- `impact_analysis.md`
- `architecture/adrs/ADR-<REQ-ID>.md`
- `architecture/security_controls.md`

### Gate
- `gate_architecture.md`

**Regla dura**
> Cambios AFIP ⇒ ADR obligatorio

---

## Stage 3 — Implementación por Slice Vertical

**Roles:** Backend + Frontend  

### Objetivo
Implementar **solo lo definido en PRD + ADR**.

### Artefactos
- `delivery/iteration-XX.md`
- `delivery/change_log.md`

### Reglas duras
- ❌ No refactor técnico
- ❌ No hotfix encubierto
- ❌ No cambios no declarados

### Gate
- `gate_delivery.md`

---

## Stage 4 — QA Funcional & No-Regresión

**Rol:** QA  

### Objetivo
Verificar que:
- La feature funciona
- Nada existente se rompió
- Estados fiscales son correctos

### Artefactos
- `qa/test_plan.md` (si aplica)
- `qa/evidencia.md`

### Gate
- `gate_qa.md`

---

## Gate Final — Feature Delivery

**Rol:** Reviewer  

### PASS si:
- Todos los gates anteriores en verde
- Evidencia completa
- No hay hotfix técnicos nuevos

### FAIL si:
- Aparece un error técnico
- La feature rompe navegación
- Se detecta deuda técnica encubierta

---

## Regla AFIP (obligatoria)

Si el REQ toca:
- CAE
- WSAA / WSFE
- Tokens
- Certificados
- Estados fiscales
- Manejo de errores SOAP

👉 Ejecutar:
- `04_afip_compliance_reconciliation.md`
- Gate: `gate_afip.md`

---

## Relación con otros workflows

- **Workflow 70**: Detecta problemas técnicos
- **Workflow 71**: Corrige hotfix técnico
- **Workflow 72**: Corrige hotfix funcional / producto
- **Workflow 03**: SOLO features nuevas

---

## Regla Final

**Si algo falla técnicamente → NO se arregla acá.  Se corta y vuelve a 70.**

---

## Pilares obligatorios del Workflow 03

Toda feature debe dejar:

1. Decisión (ADR)
2. Comportamiento validado (QA)
3. Evidencia persistente (artefactos)


