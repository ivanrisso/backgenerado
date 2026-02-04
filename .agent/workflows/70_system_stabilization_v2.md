---
description: Preparar entrega con seguridad operativa.. regresión, monitoreo,   runbooks, rollback, controles de seguridad, y checklist de release.
---

# Workflow 70 — Stabilization Scan

## Propósito
Detectar, clasificar y preparar hotfixes técnicos que impidan la
estabilidad operativa del sistema, sin aplicar cambios de código.

## Principios
- No corregir código
- No introducir cambios funcionales
- Preparar hotfixes ejecutables y auditables
- Separar hotfix técnico vs gap funcional

## REQ activo
- Leer REQ desde `.artifacts/requests/current.req`
- Usar ese REQ como base de todos los outputs

## Idioma de los Artefactos

Todos los archivos generados por este workflow
DEBEN estar escritos en **ESPAÑOL**.

Esto incluye:
- Inventarios
- Reportes
- Descripciones de hotfix
- Fix prompts asistidos
- Evidencia QA
- Gate result

Si algún artefacto se genera en otro idioma → Gate FAIL.

## Roles
- Orchestrator
- Arquitecto
- Frontend Engineer
- Backend Engineer
- QA

## Skills usados
- route-inventory-scan
- lazy-import-analysis
- frontend-crud-detection
- backend-endpoint-observer
- auth-flow-classifier
- hotfix-classifier
- hotfix-describer
- fix-prompt-generator
- hotfix-prioritizer

## Runbook
Este workflow se ejecuta siguiendo el procedimiento definido en:

`.agent/runbooks/70_runbook_stabilization_scan.md`

## Gate
Checklist aplicado:
`.agent/checklists/stabilization-scan.md`

## Resultado
- Hotfixes documentados
- Prompts asistidos generados
- Orden de ejecución definido
- Gate PASS / FAIL registrado

## Gate = PASS
El sistema queda habilitado para ejecutar el **Workflow 71 (Hotfix Execution)**.

## Gate = FAIL
El workflow finaliza dejando artefactos técnicos completos
(inventarios, clasificación, hotfix descriptions, fix prompts asistidos y ORDER.md),
pero **bloquea cualquier corrección automática**.

---

## Regla de Nomenclatura (NO negociable)

- HF-CLEAN-XXX / HF-TECH-XXX → Hotfix técnico (Workflow 71)
- HF-FUNC-XXX → Hotfix funcional (Workflow 72)
- GAP-XXX → Gap funcional o de producto (NO hotfix)

Nunca combinar prefijos HF y GAP.

---

## Regla Final

**Workflow 70 detecta y prepara.  
Workflow 71 es el único autorizado a corregir hotfix técnicos.**