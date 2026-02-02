---
description: Corregir  exclusivamente los hotfix técnicos documentados por el Workflow 04
---

# Workflow 71 — Hotfix Execution & Stabilization Hardening

**Nivel:** CRÍTICO  
**Tipo:** Correctivo / Técnico  
**Dependencia obligatoria:**  
- Workflow 70 — Stabilization Scan (**PASS**)

---

## Propósito

Aplicar **un único hotfix a la vez**, previamente detectado, clasificado y documentado,
asegurando que el sistema recupere **estabilidad técnica real**, validada en runtime,
sin introducir cambios funcionales ni de negocio.

Este workflow **EJECUTA** correcciones.  
La detección, clasificación y priorización **NO ocurren aquí**.  

📌 Todo archivo generado por este workflow debe estar escrito en **ESPAÑOL**.
📌 Siempre que tenga que acceder de forma interactiva al login hacerlo con:

      Usuario: admin@facturacion.local
      Password: admin.password.dev
---

## Qué corrige este workflow

✔️ Imports rotos  
✔️ Rutas que no cargan vistas  
✔️ Aliases incorrectos  
✔️ Guards mal aplicados  
✔️ Endpoints que devuelven 500 técnicos  
✔️ Seeds mínimos faltantes  

---

## Qué NO hace este workflow (NO negociable)

- ❌ No agrega features
- ❌ No redefine reglas de negocio
- ❌ No mejora UX
- ❌ No refactoriza código existente
- ❌ No corrige errores no documentados

> **Si aparece un error nuevo → vuelve obligatoriamente a Workflow 70**

---

## Input obligatorio

Este workflow **NO puede iniciar** si no existe exactamente uno de los siguientes:
hotfix/HF-XXX/fix_description.md


### Reglas
- Un Workflow 71 = **un solo hotfix**
- El hotfix debe ser el **primero** en `hotfix/ORDER.md`

---

## Roles involucrados (exclusivos)

- **Backend Engineer** (si afecta backend)
- **Frontend Engineer** (si afecta frontend)
- **QA**
- **Release Manager**

> El **Arquitecto NO implementa**, solo supervisa cumplimiento.

---

## Principio rector

**Un hotfix = un cambio mínimo, aislado, verificable y revalidado en runtime**  
  Nada “aprovechando que estoy”.

---

## Stage A — Plan de implementación del Hotfix

**Rol activo:** Backend Engineer o Frontend Engineer  
**Skill:** `hotfix-planner`

### Acciones
1. Leer `fix_description.md`
2. Determinar:
   - Archivos exactos a tocar
   - Tipo de corrección (import / alias / endpoint / guard / seed)
   - Riesgo técnico
3. Definir el plan mínimo de cambio

### Output obligatorio
hotfix/HF-XXX/implementation_plan.md


---

## Stage B — Implementación controlada

**Rol activo:** Backend Engineer o Frontend Engineer  
**Skill:** `hotfix-implementation`

### Acciones
1. Implementar **solo** lo definido en `implementation_plan.md`
2. Cambios pequeños, explícitos y rastreables
3. Sin modificar comportamiento no relacionado

### Reglas duras
- ❌ No refactor
- ❌ No cleanup general
- ❌ No cambio de contratos
- ❌ No cambios estéticos

---

## Stage C — Ajuste y validación de tests

**Rol activo:** QA  
**Skill:** `hotfix-test-adjustment`

### Acciones
1. Ejecutar tests existentes
2. Si el hotfix rompe tests:
   - Ajustar el test afectado **solo si corresponde**
   - O agregar test mínimo de no-regresión
3. Verificar que el hotfix quede cubierto

### Output obligatorio
hotfix/HF-XXX/test_evidence.md


---

## Stage D — Revalidación funcional dirigida del Hotfix (OBLIGATORIA)

**Rol activo:** QA  
**Skill:** `hotfix-e2e-verification`  
**Tipo:** Runtime / Interactivo  
**Bloqueante:** SÍ

### Objetivo

Re-ejecutar **exactamente el escenario que fallaba**, tal como fue documentado
en `fix_description.md`, y confirmar que **ya no falla**.

### Acciones
1. Navegar **la misma ruta** afectada por el hotfix
2. Ejecutar **la misma acción** que antes producía el error
3. Verificar explícitamente:
   - La vista carga completamente
   - No hay errores JS en consola
   - No hay navegación abortada
   - El backend responde sin errores técnicos
4. Si el hotfix es de tipo CRUD:
   - List → Create → Update → Delete (si aplica)
   - **No cancelar flujos**
   - **No simular datos**
   - **No evitar acciones**

### Output obligatorio
hotfix/HF-XXX/e2e_evidence.md


📌 Este archivo debe indicar explícitamente:
- Qué fallaba antes
- Qué se volvió a probar
- Resultado: **PASS / FAIL**

---

## Stage E — Validación de CI

**Rol activo:** Release Manager  
**Skill:** `ci-validation`

### Acciones
1. Ejecutar pipeline CI
2. Verificar:
   - Backend job PASS
   - Frontend job PASS
3. Bloquear cierre si CI falla

---

## Stage F — Cierre del Hotfix

**Rol activo:** Release Manager  
**Skill:** `hotfix-closure`

### Acciones
1. Verificar que TODA la evidencia existe
2. Marcar el hotfix como cerrado
3. Registrar estado final

### Output obligatorio
hotfix/HF-XXX/status.md


---

## Gate — Stabilization Fix (ENDURECIDO)

**Checklist aplicado:** `gate_stabilization_fix.md`

### PASS solo si:
- Existe `implementation_plan.md`
- Existe `test_evidence.md`
- Existe `e2e_evidence.md` **(obligatorio)**
- `e2e_evidence.md` indica **PASS**
- Existe `status.md`
- CI está en verde
- No hay hotfixes anteriores abiertos

### FAIL si:
- Falta evidencia
- La revalidación funcional no se ejecutó
- El escenario original sigue fallando
- CI falla
- Se corrigió algo fuera del alcance

---

## Resultado esperado

✔️ Sistema estable **en runtime**  
✔️ Frontend navegable  
✔️ CRU(D) ejecutables sin errores técnicos  
✔️ Backend sin 500  
✔️ Base lista para desarrollo funcional

---

## Reglas finales (NO negociable)

- ** Workflow 71 NO se considera exitoso si el hotfix no fue revalidado manualmente en runtime.**
- ** Workflow 71 corrige. Workflow 70 detecta. Jamás al revés.**
- ** Un hotfix NO se considera corregido si no existe:
   - e2e_evidence.md
   - status.md
- Los mensajes de resumen o smoke tests narrativos NO sustituyen evidencia persistida.


