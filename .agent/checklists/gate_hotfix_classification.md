# Gate — Hotfix Classification

## Objetivo
Garantizar que **cada issue detectado** tenga un tipo claro
y un workflow de resolución inequívoco.

---

## Checklist por Hotfix

Para cada `hotfix/HF-XXX` debe existir:

- [ ] `fix_description.md`
- [ ] Campo `tipo` definido:
  - HOTFIX_TECNICO
  - HOTFIX_FUNCIONAL
  - GAP_PRODUCTO
- [ ] Campo `workflow_destino` definido:
  - 71 (técnico)
  - 72 (funcional)
  - backlog (producto)

---

## Reglas duras (NO negociables)

- ❌ Un HOTFIX_FUNCIONAL **NO puede** ir a Workflow 71
- ❌ Un HOTFIX_TECNICO **NO puede** ir a Workflow 72
- ❌ Un GAP_PRODUCTO **NO puede** generar hotfix
- ❌ Si el tipo no está definido → FAIL

---

## Resultado

PASS:
- Todos los hotfix clasificados
- No hay ambigüedad de destino

FAIL:
- Algún hotfix sin tipo
- Tipo incompatible con workflow
