---
description: Hotfix Funcional / Producto
---

# Workflow 72 — Hotfix Funcional / Producto

**Nivel:** ALTO  
**Tipo:** Correctivo Funcional / Producto  

**Dependencias obligatorias:**
- Workflow 70 — Stabilization Scan (**ejecutado**)
- Hotfix clasificado como **FUNCIONAL** o **PRODUCTO**

---

## 📌 Regla de Idioma (CRÍTICA)

Todos los artefactos generados por este workflow  
**DEBEN estar redactados en ESPAÑOL CLARO, FUNCIONAL Y NO TÉCNICO**:

- `functional_definition.md`
- `impact_analysis.md`
- `implementation_plan.md`
- casos de prueba
- evidencias
- `status.md`

El objetivo es que puedan ser comprendidos **sin reinterpretación técnica** por:
- Producto
- QA
- Negocio

⚠️ Si algún artefacto se genera en otro idioma → **FAIL inmediato del workflow**.

---

## Propósito

Corregir **un único hotfix funcional o de producto** que:

- no rompe técnicamente el sistema,
- pero impide o degrada el uso correcto del producto,

garantizando que el comportamiento final sea:

- explícito,
- validado,
- documentado,
- auditable.

Este workflow:

- ✔️ Corrige **comportamiento**
- ✔️ Ajusta **flujos funcionales**
- ✔️ Genera **casos de prueba funcionales**
- ❌ NO corrige bugs técnicos puros (eso corresponde a **Workflow 71**)

---

## Qué corrige este workflow

✔️ Flujos incompletos  
✔️ Menús que no exponen funcionalidades existentes  
✔️ CRU(D) funcionalmente incorrectos  
✔️ Validaciones faltantes o incorrectas  
✔️ UX que bloquea tareas válidas  
✔️ Reglas de negocio mal reflejadas en UI o Backend  

---

## Qué NO hace este workflow (NO NEGOCIABLE)

- ❌ No arregla crashes técnicos
- ❌ No corrige imports / aliases / DI
- ❌ No resuelve errores 500 o 401 técnicos
- ❌ No refactoriza masivamente
- ❌ No introduce nuevas features
- ❌ **Workflow 72 NO detecta problemas nuevos**

### Regla crítica de no-detección

Si durante la ejecución se observa:
- un problema funcional **no documentado**, o
- un desvío **distinto** al descripto en `fix_description.md`,

👉 el workflow **DEBE detenerse inmediatamente**  
👉 y derivar nuevamente a **Workflow 70**.

> **Si aparece un error técnico → volver a Workflow 70 o 71**

---

## Resolución del REQ activo

1. Leer el REQ desde:  
   `.artifacts/requests/current.req`
2. El valor leído se considera `{{CURRENT_REQ}}`
3. Todos los artefactos del workflow se escriben bajo:

.artifacts/requests/{{CURRENT_REQ}}/


⚠️ Workflow 72 **NO crea REQs nuevos**  
⚠️ Workflow 72 **NO utiliza `input.md`**

---

## Input obligatorio

Debe existir **exactamente uno** de los siguientes:

- `hotfix/HF-FUNC-XXX/fix_description.md`
- `hotfix/HF-FUNC-XXX/metadata.md`

### Requisitos del metadata

`metadata.md` debe indicar explícitamente:
- `tipo: FUNCIONAL | PRODUCTO`

### Reglas

- Un Workflow 72 = **un solo hotfix funcional**
- El hotfix debe estar clasificado como `FUNCIONAL` o `PRODUCTO`
- El hotfix **DEBE existir previamente** en el REQ activo
- `hotfix/ORDER.md` es informativo y de gobierno  
  **NO es una fuente automática de selección**

---

## Roles involucrados

- **Product Owner / Analista Funcional**
- **Frontend Engineer**
- **Backend Engineer**
- **QA**
- **Release Manager**
- **Arquitecto** (supervisión, no implementación)

---

## Principio rector

> **Un hotfix funcional se corrige con comportamiento claro y pruebas claras.**  
> No existe el “arreglo implícito”.

---

## Stage A — Clarificación funcional del Hotfix

**Rol activo:** Product Owner / Analista Funcional  
**Skill:** `functional-clarifier`

### Acciones
1. Leer `fix_description.md`
2. Definir explícitamente:
   - Comportamiento actual (incorrecto)
   - Comportamiento esperado (correcto)
   - Casos borde
3. Validar alcance:
   - Qué entra
   - Qué NO entra

### Output obligatorio
hotfix/HF-FUNC-XXX/functional_definition.md


---

## Stage B — Impact Analysis Funcional

**Rol activo:** Arquitecto + Backend / Frontend  
**Skill:** `functional-impact-analysis`

### Acciones
1. Identificar:
   - Pantallas afectadas
   - Endpoints afectados
   - Reglas impactadas
2. Evaluar riesgo funcional:
   - Bajo / Medio / Alto

### Output obligatorio
hotfix/HF-FUNC-XXX/impact_analysis.md


---

## Stage C — Plan de Implementación Funcional

**Rol activo:** Frontend / Backend  
**Skill:** `functional-planner`

### Acciones
1. Definir cambios necesarios:
   - UI
   - Backend
   - Validaciones
2. Detallar pasos mínimos
3. Evitar cambios colaterales

### Output obligatorio
hotfix/HF-FUNC-XXX/implementation_plan.md


---

## Stage D — Implementación Funcional

**Rol activo:** Frontend / Backend  
**Skill:** `functional-implementation`

### Acciones
1. Implementar **solo** lo definido en el plan
2. Mantener backward compatibility
3. No alterar reglas no involucradas

### Reglas duras
- ❌ No refactor general
- ❌ No mejoras estéticas no solicitadas
- ❌ No lógica “aprovechando”

### Regla crítica
Si durante la implementación surge una ambigüedad funcional:
- detener implementación
- volver a **Stage A — Clarificación funcional**

---

## Stage E — Generación de Casos de Prueba Funcionales

**Rol activo:** QA  
**Skill:** `functional-test-designer`

### Acciones
1. Diseñar casos de prueba:
   - Happy path
   - Error controlado
   - Permisos / roles
   - Casos borde
2. Alinear cada caso con el comportamiento esperado

### Output obligatorio
qa/cases/HF-FUNC-XXX.md


---

## Stage F — Ejecución de Pruebas Funcionales (Manual / E2E)

**Rol activo:** QA  
**Skill:** `functional-test-execution`

### Acciones
1. Ejecutar **todos** los casos definidos
2. Registrar para cada caso:
   - ID del caso
   - Resultado (PASS / FAIL)
   - Evidencia
   - Observaciones

### Output obligatorio
hotfix/HF-FUNC-XXX/test_evidence.md


---

## Stage G — Smoke Test Integrado

**Rol activo:** QA  
**Skill:** `functional-smoke-test`

### Acciones
1. Navegar flujos relacionados
2. Verificar que no se rompió nada adyacente
3. Validar UX básica
4. Confirmar que NO se reintrodujeron:
   - errores técnicos previos
   - crashes
   - loops de navegación

### Output obligatorio
hotfix/HF-FUNC-XXX/smoke_evidence.md


---

## Stage H — Cierre del Hotfix Funcional

**Rol activo:** Release Manager  
**Skill:** `hotfix-closure`  

**Template obligatorio:**  
.agent/templates/status_functional.md


### Acciones
1. Verificar evidencia completa
2. Marcar hotfix como cerrado
3. Registrar estado final

### Output obligatorio
hotfix/HF-FUNC-XXX/status.md


---

## Gate — Functional Hotfix Validation

**Checklist aplicado:** `gate_functional_hotfix.md`

### PASS si:
- Existe `functional_definition.md`
- Existe `impact_analysis.md`
- Existe `implementation_plan.md`
- Existe `qa/cases/HF-FUNC-XXX.md`
- Existe `test_evidence.md` (PASS)
- Existe `smoke_evidence.md` (PASS)
- Existe `status.md`
- No hay regresiones visibles

### FAIL si:
- Falta evidencia
- El comportamiento no es claro
- QA no valida el resultado

---

## Resultado esperado

✔️ Comportamiento funcional corregido  
✔️ Flujos claros y validados  
✔️ Casos de prueba documentados  
✔️ Evidencia reproducible  
✔️ Hotfix cerrado formalmente  

---

## Relación con otros Workflows

- **Workflow 70**: detecta y clasifica
- **Workflow 71**: corrige hotfix técnico
- **Workflow 72**: corrige hotfix funcional / producto
- **Workflow 03**: evolución funcional (features)

---

## Regla final (NO NEGOCIABLE)

> **Un hotfix funcional sin casos de prueba NO existe.**  
> **Un hotfix funcional sin status.md NO está cerrado.**
