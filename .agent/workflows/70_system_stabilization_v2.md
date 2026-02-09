---
description: Preparar entrega con seguridad operativa.. regresión, monitoreo,   runbooks, rollback, controles de seguridad, y checklist de release.
---

# Workflow 70 — Stabilization Scan

## Propósito

Detectar, clasificar y preparar **hotfixes técnicos y gaps funcionales**
que impidan la estabilidad operativa del sistema,
**sin aplicar cambios de código ni correcciones funcionales**.

Este workflow **NO corrige**.  
Este workflow **observa, evidencia y prepara**.

---

## Principios (NO negociables)

- ❌ No corregir código
- ❌ No introducir cambios funcionales
- ❌ No refactorizar
- ❌ No “aprovechar” para mejorar nada
- ✅ Observar comportamiento real
- ✅ Evidenciar fallas técnicas
- ✅ Preparar hotfixes ejecutables y auditables
- ✅ Separar estrictamente:
  - Hotfix técnico
  - Gap funcional / producto

---

## REQ Activo

- Leer el REQ desde:
.artifacts/requests/current.req

- El valor leído se considera `{{CURRENT_REQ}}`
- **Todos los artefactos** del workflow se escriben bajo:
.artifacts/requests/{{CURRENT_REQ}}/


⚠️ Nunca se hardcodea el REQ dentro del workflow ni de las skills.

---

## Idioma de los Artefactos (CRÍTICO)

Todos los archivos generados por este workflow  
**DEBEN estar escritos en ESPAÑOL**.

Incluye:
- Inventarios
- Reportes
- Evidencia QA
- Descripciones de hotfix
- Fix prompts asistidos
- Gate result

Si **algún artefacto** se genera en otro idioma → **Gate = FAIL**.

---

## Roles Involucrados

- **Orchestrator**
- **Arquitecto**
- **Frontend Engineer**
- **Backend Engineer**
- **QA**

---

## Skills Usadas (fuente de verdad)

### Stage B — Inventario Frontend
- `route-inventory-scan`
- `lazy-import-analysis`

### Stage C — CRU(D) Frontend
- `frontend-crud-detection`

### Stage D — Backend & Auth
- `backend-endpoint-observer`
- `auth-flow-classifier`

### Stage E — Runtime Scan (OBLIGATORIO si hybrid)
- `ui-runtime-scan`
- `ui-runtime-menu-scan`
- `ui-menu-consistency-check`

### Stage F — Clasificación
- `hotfix-classifier`

### Stage G — Documentación
- `hotfix-describer`

### Stage H — Fix Prompt (asistido)
- `fix-prompt-generator`

### Stage I — Priorización
- `hotfix-prioritizer`

---

## Runbook

La ejecución de este workflow se rige **exclusivamente** por el runbook:
.agent/runbooks/70_runbook_stabilization_scan.md


El workflow **no redefine procedimientos**.  
El runbook es la fuente operativa.

---

## Gate

Checklist aplicado:
.agent/checklists/stabilization-scan.md


El Gate es el **único** responsable de decidir PASS / FAIL.

---

## Resultado del Workflow

Al finalizar, el workflow **DEBE dejar**:

- Inventarios técnicos completos
- Evidencia runtime (si execution_mode = hybrid)
- Hotfixes técnicos documentados
- Gaps funcionales documentados
- Fix prompts asistidos generados
- Orden de ejecución definido (`hotfix/ORDER.md`)
- Resultado de Gate persistido

---

## Gate = PASS

El sistema queda **habilitado** para ejecutar:

> **Workflow 71 — Hotfix Técnico**

---

## Gate = FAIL

El workflow finaliza dejando **TODOS los artefactos técnicos completos**, pero:

- ❌ Bloquea cualquier corrección automática
- ❌ No habilita Workflow 71 ni 72

Hasta nueva ejecución o habilitación explícita.

---

## Regla de Nomenclatura (NO negociable)

- `HF-CLEAN-XXX` / `HF-TECH-XXX` → Hotfix técnico (Workflow 71)
- `HF-FUNC-XXX` → Hotfix funcional / producto (Workflow 72)
- `GAP-XXX` → Gap funcional o de producto

⚠️ Nunca combinar prefijos HF y GAP.

---

## Regla Final

**Workflow 70 detecta y prepara.  
Workflow 71 corrige hotfixes técnicos.  
Workflow 72 corrige hotfixes funcionales.**

Nada se corrige sin haber sido detectado aquí.








