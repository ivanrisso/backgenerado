# Alineación de Gobierno — Workflow 71 ↔ Workflow 70

## Propósito

Garantizar que **Workflow 71 (Hotfix Técnico)** solo pueda ejecutarse
si el sistema fue **correctamente detectado, clasificado y documentado**
por el **Workflow 70** y su Gate asociado.

---

## Precondición Obligatoria (NO negociable)

Workflow 71 **NO PUEDE iniciar** si:

- No existe un Workflow 70 previo
- El Gate del Workflow 70 **NO está en estado PASS**
- No existe `hotfix/ORDER.md`
- El hotfix a ejecutar **NO es el primero** en `hotfix/ORDER.md`

Si alguna condición falla → **ABORTAR Workflow 71**

---

## Artefactos obligatorios provenientes del Workflow 70

Para el hotfix `HF-TECH-XXX` a ejecutar, deben existir **ANTES de iniciar**:

```text
hotfix/HF-TECH-XXX/
├─ fix_description.md
├─ analysis.md
├─ metadata.md
