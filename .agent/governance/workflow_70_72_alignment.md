
---

### 📄 Archivo 2 — Alineación Workflow 72 ↔ Workflow 70

```md
# Alineación de Gobierno — Workflow 72 ↔ Workflow 70

## Propósito

Garantizar que **Workflow 72 (Hotfix Funcional / Producto)** solo pueda ejecutarse
a partir de **gaps funcionales explícitamente documentados**
o por **decisión humana consciente y explícita**.

---

## Formas válidas de iniciar Workflow 72

Workflow 72 **SOLO puede iniciarse** si se cumple **UNA** de las siguientes condiciones.

---

### Opción A — Gap detectado por Workflow 70

Debe existir:

```text
gaps/GAP-XXX/
├─ fix_description.draft.md
├─ metadata.draft.md
