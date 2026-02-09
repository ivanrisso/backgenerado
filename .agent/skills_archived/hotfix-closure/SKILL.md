# SKILL — Hotfix Closure

## Rol autorizado
- **Release Manager**

⚠️ Ningún otro rol está autorizado a cerrar un hotfix.

---

### Validación de Idioma

Antes de instanciar el status:

- Verificar que los archivos de evidencia
  estén redactados en **ESPAÑOL**.
- Si se detecta idioma distinto → FAIL inmediato.

---

## Objetivo

Cerrar **formal y persistentemente** un hotfix **solo si** existe evidencia
completa y validada, dejando constancia auditable del estado final mediante
el archivo:
hotfix/HF-XXX/status.md


Este skill es el **ÚNICO AUTORIZADO** a generar `status.md`.

---

## Principio rector (NO negociable)

> **Un hotfix sin status.md NO está cerrado.**  
> **Un hotfix con status.md es la única fuente de verdad.**

Narrativas, resúmenes, smoke tests verbales o mensajes de éxito
**NO sustituyen** este archivo.

---

## Precondiciones obligatorias

1. El workflow que invoca este skill **DEBE** proveer explícitamente:
- HOTFIX_TYPE = TECHNICAL | FUNCTIONAL
- WORKFLOW_ID = 71 | 72
- STATUS_TEMPLATE_PATH



2. Debe existir exactamente **un hotfix activo** (`HF-XXX`)
   en proceso de cierre.

Si alguna precondición no se cumple → **FAIL inmediato**.

---

## Template obligatorio

El workflow **DEBE** declarar explícitamente el template a usar.

Templates válidos:

- Hotfix técnico (Workflow 71):
.agent/templates/status_technical.template.md


- Hotfix funcional / producto (Workflow 72):
.agent/templates/status_functional.template.md

Si el template **no existe** o **no es indicado** → **FAIL inmediato**.

---

## Inputs obligatorios (según tipo de hotfix)

### 🛠️ Hotfix TÉCNICO — Workflow 71

Para el hotfix `HF-XXX` deben existir **TODOS** los siguientes archivos:

- `hotfix/HF-XXX/implementation_plan.md`
- `hotfix/HF-XXX/test_evidence.md`
- `hotfix/HF-XXX/e2e_evidence.md`

Condiciones obligatorias:
- `e2e_evidence.md` **DEBE** contener explícitamente:
Resultado: PASS

- El pipeline de CI debe estar **VERDE**:
- Backend: PASS
- Frontend: PASS

Si **alguno falta** o indica FAIL → **FAIL inmediato**.

---

### 🧩 Hotfix FUNCIONAL / PRODUCTO — Workflow 72

Para el hotfix `HF-FUNC-XXX` deben existir **TODOS** los siguientes archivos:

- `hotfix/HF-FUNC-XXX/functional_definition.md`
- `hotfix/HF-FUNC-XXX/impact_analysis.md`
- `hotfix/HF-FUNC-XXX/implementation_plan.md`
- `qa/cases/HF-FUNC-XXX.md`
- `hotfix/HF-FUNC-XXX/test_evidence.md`
- `hotfix/HF-FUNC-XXX/smoke_evidence.md`

Condiciones obligatorias:
- `test_evidence.md` **DEBE** indicar resultado **PASS**
- `smoke_evidence.md` **DEBE** indicar resultado **PASS**

⚠️ CI **NO es obligatorio** para hotfix funcional,
salvo que el workflow lo declare explícitamente.

Si **alguno falta** o indica FAIL → **FAIL inmediato**.

---

## Acciones del Skill

### 1️⃣ Validación de Evidencia

- Verificar existencia de **todos** los inputs requeridos
según el tipo de hotfix.
- Si algún archivo requerido:
- no existe
- está vacío
- indica FAIL  
→ **FAIL inmediato**

---

Convención:
- HF-CLEAN-XXX → Hotfix Técnico (Workflow 71)
- HF-FUNC-XXX → Hotfix Funcional / Producto (Workflow 72)

---

### 2️⃣ Resolución de Variables del Status

El skill debe completar **únicamente** las variables definidas
en el template indicado por el workflow.

Variables mínimas comunes:

- `{{ESTADO}}` → `CLOSED`
- `{{FECHA}}` → fecha actual (YYYY-MM-DD)
- `{{HOTFIX_ID}}` → HF-XXX
- `{{WORKFLOW_ID}}` → 71 o 72

Variables **condicionales** (según template):

- Técnicos:
- `{{RESULTADO_E2E}}`
- `{{RESULTADO_CI}}`

- Funcionales:
- `{{RESULTADO_PRUEBAS_FUNCIONALES}}`
- `{{RESULTADO_SMOKE_TEST}}`

⚠️ El skill **NO inventa variables**  
⚠️ El template define la estructura final

---

### 3️⃣ Instanciación del Status

Instanciar el template indicado, completando los valores resueltos,
y generar el archivo final:

hotfix/HF-XXX/status.md

---

## Output obligatorio
hotfix/HF-XXX/status.md

Este archivo es la **única evidencia válida de cierre**.

---

Si `hotfix/HF-XXX/status.md` ya existe → FAIL inmediato.
El cierre de un hotfix es una operación **idempotente y única**.

---

## Ejemplos mínimos válidos

### ✅ Hotfix Técnico (Workflow 71)

```md
Estado: CLOSED
Fecha: 2026-02-02
Hotfix: HF-CLEAN-003
Workflow: 71
Resultado e2e: PASS
CI: PASS

### ✅ Hotfix Funcional (Workflow 72)

```md
Estado: CLOSED
Tipo: FUNCIONAL
Hotfix: HF-FUNC-012
Workflow: 72
Resultado pruebas funcionales: PASS
Smoke test: PASS
Fecha: 2026-02-02


