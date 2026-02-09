# Runbook — Workflow 70: Stabilization Scan

## Objetivo

Ejecutar un escaneo técnico integral del sistema para **detectar, clasificar y preparar hotfixes**
que impidan la estabilidad operativa, **sin aplicar correcciones de código**.

Este runbook define **cómo** se ejecuta el Workflow 70.  
El workflow solo lo referencia.

---

## Regla Crítica de Rol para Runtime Scan

El escaneo de estabilización en runtime **DEBE ejecutarse siempre con el rol de máxima visibilidad funcional**.

En este sistema:

- Rol obligatorio para Stage E: **ADMIN**

Motivo:
- Garantizar detección completa de:
  - menús
  - rutas
  - flujos
  - funcionalidades existentes

⚠️ Ejecutar runtime scan con roles restringidos genera **falsos negativos**
y **gaps funcionales no detectados**.

---

## Contexto de Ejecución

- Workflow: **70**
- Tipo: **Stabilization Scan**
- Correcciones: ❌ NO
- Preparación de hotfixes: ✅ SÍ
- Runtime browser: **Condicional (CDP)**

---

## Resolución del REQ Activo

1. Leer el archivo:
.artifacts/requests/current.req
2. El valor leído se considera `{{CURRENT_REQ}}`
3. **Todos los artefactos** del workflow se escriben bajo:
.artifacts/requests/{{CURRENT_REQ}}/

⚠️ Nunca se hardcodea el REQ dentro del workflow o los skills.

---

## Outputs Esperados (por corrida)

.artifacts/requests/{{CURRENT_REQ}}/
├─ input.md
├─ run_log.md
├─ architecture/
│ ├─ routes_inventory.md
│ ├─ lazy_import_issues.md
│ └─ view_load_report.md
├─ ui/
│ ├─ crud_matrix.md
│ ├─ missing_operations.md
│ ├─ menu_runtime_report.md
│ └─ ui_runtime_errors.md
├─ backend/
│ ├─ endpoints_inventory.md
│ ├─ auth_issues.md
│ └─ server_errors.md
├─ hotfix/
│ ├─ ORDER.md
│ └─ HF-XXX/
│ ├─ fix_description.md
│ ├─ analysis.md
│ ├─ metadata.md
│ └─ fix_prompt.md
├─ gaps/
│ ├─ functional_gaps.md
│ ├─ menu_gaps.md
│ └─ skills_missing.md
├─ qa/
│ └─ stabilization_evidence.md
└─ gate_result.md


---

## Stage A — Inicialización y Detección de Runtime Browser

**Rol:** Orchestrator  
**Objetivo:** Inicializar la corrida y determinar de forma **técnica y explícita**
si es posible ejecutar navegación y CRU(D) en runtime.

### A1 — Resolución del REQ

1. Leer `.artifacts/requests/current.req`
2. Si no existe → **ABORTAR**
3. Usar su valor como `{{CURRENT_REQ}}`

---

### A2 — Validación de Input

Debe existir:
.artifacts/requests/{{CURRENT_REQ}}/input.md


Si no existe → **ABORTAR**

---

### A3 — Registro de Ejecución

Crear:
.artifacts/requests/{{CURRENT_REQ}}/run_log.md


Contenido mínimo:
- Fecha / hora
- Workflow: 70
- REQ activo
- Tipo: stabilization-scan

---

### A4 — Detección Técnica de Browser Runtime (CDP)

**Browser declarado:**
- Chromium
- Protocolo: CDP
- Endpoint esperado:

http://127.0.0.1:9222/json/version


**Validación obligatoria:**
- El endpoint responde
- Existe `webSocketDebuggerUrl`

---

### A5 — Determinación del Modo de Ejecución

- Si la validación CDP es exitosa:
- `execution_mode = hybrid`
- Runtime browser habilitado

- Si la validación CDP falla:
- `execution_mode = static`
- Runtime browser NO disponible
- Registrar causa técnica

⚠️ Warnings de DBUS / xdg-settings **NO invalidan** el browser  
si el endpoint CDP responde correctamente.

---

### A6 — Registro Final del Stage

Registrar en `run_log.md`:
- `execution_mode`
- Resultado de validación CDP
- Motivo de degradación (si aplica)

---

### Regla No Negociable

> Si `execution_mode = hybrid`,  
> el workflow **DEBE ejecutar navegación y CRU(D) en runtime**.

---

## Stage B — Inventario de Rutas y Vistas

**Rol:** Frontend Engineer  
**Skills:** `route-inventory-scan`, `lazy-import-analysis`

### Acciones
1. Enumerar rutas desde el router (incluyendo módulos).
2. Detectar vistas lazy-loaded.
3. Verificar resolución estática:
 - imports relativos
 - aliases (`@domain`, `@ui`, `@shared`)
4. Documentar:
 - imports rotos
 - rutas inexistentes
 - aliases inconsistentes

### Output
- `architecture/routes_inventory.md`
- `architecture/lazy_import_issues.md`

---

## Stage C — Detección de CRU(D) Frontend

**Rol:** Frontend Engineer + QA  
**Skill:** `frontend-crud-detection`

### Acciones
1. Detectar vistas CRUD por convención:
 - List
 - Form
 - Create / Update / Delete (si existe)
2. Registrar por CRUD:
 - vistas
 - composables
 - repositorios / clients
 - endpoints esperados
3. Identificar gaps técnicos:
 - stubs
 - servicios no implementados
 - imports rotos

### Output
- `ui/crud_matrix.md`
- `ui/missing_operations.md`

---

## Stage D — Observación de Backend y Autenticación

**Rol:** Backend Engineer  
**Skills:** `backend-endpoint-observer`, `auth-flow-classifier`

### Acciones
1. Enumerar endpoints consumidos por frontend.
2. Clasificar:
 - 401 esperado
 - 401 inesperado
 - 403 (RBAC)
 - 500 técnicos
3. Documentar endpoints críticos y errores.

### Output
- `backend/endpoints_inventory.md`
- `backend/auth_issues.md`
- `backend/server_errors.md`

⚠️ El inventario backend **NO se infiere**.  
Si no se observa → `UNKNOWN`.

---

## Stage D1 — Validación Arquitectónica contra SAD (PRE Runtime)

**Workflow:** 70 — Stabilization Scan  
**Dependencia obligatoria:** Workflow 10 — System Architecture Definition (SAD) = PASS  
**Rol activo:** Arquitecto  
**Skills utilizados:**
- sad-compliance-check
- architecture-drift-detector

---

## Objetivo del Stage

Validar que la **arquitectura real observada** del sistema
**cumple estrictamente** con el contrato definido en el
**System Architecture Definition (SAD)** aprobado en el Workflow 10,
**antes de ejecutar cualquier scan runtime o clasificación de issues**.

Este stage:

- ✔️ Valida cumplimiento arquitectónico
- ✔️ Detecta desvíos estructurales
- ✔️ Clasifica violaciones arquitectónicas
- ❌ NO ejecuta runtime
- ❌ NO genera hotfixes
- ❌ NO genera gaps funcionales

---

## Precondiciones obligatorias

Deben existir bajo el REQ activo los artefactos del SAD:

.architecture/
├─ architectural_principles.md
├─ allowed_stack.md
├─ forbidden_patterns.md
├─ deployment_topology.md
├─ security_baseline.md
├─ integration_constraints.md


---

## Stage E — Runtime Scan (OBLIGATORIO si execution_mode = hybrid)

**Rol:** QA  
**Usuario obligatorio:**  
- admin@facturacion.local  
- admin.password.dev  

### Orden obligatorio de ejecución de skills

1. `ui-runtime-scan`  
2. `ui-runtime-menu-scan`  
3. `ui-menu-consistency-check`

Los tres **DEBEN ejecutarse**.  
Ninguno decide PASS / FAIL por sí solo.

---

### Objetivo del Stage E

Verificar en **runtime real** que:

- las rutas renderizan
- las vistas lazy cargan
- la UI no crashea
- los CRU(D) no fallan técnicamente
- la navegación desde menú es completa y consistente

---

### Regla Anti-PASS Incompleto (CRÍTICA)

El Stage E **FALLA automáticamente** si:

- existe al menos un menú padre
- con subítems detectados
- y **NO hay evidencia explícita** de navegación para cada subítem

No se acepta:
- “probé uno”
- “probé el principal”
- “volví al dashboard”

---

## Stage F — Clasificación de Issues y Generación de Drafts (Workflow 70)

**Workflow:** 70 — Stabilization Scan  
**Rol activo:** Arquitecto + Orchestrator  

**Skills utilizados:**
- `hotfix-classifier`
- `ui-menu-consistency-check`

---

## Objetivo del Stage

Clasificar **todos los issues detectados** durante el Workflow 70 y generar
los artefactos correspondientes **sin ejecutar correcciones**.

Este stage:

- ✔️ Clasifica issues
- ✔️ Genera hotfixes técnicos ejecutables
- ✔️ Genera drafts documentales para gaps funcionales
- ❌ NO ejecuta correcciones
- ❌ NO habilita Workflow 72
- ❌ NO toma decisiones de producto

---

## Clasificación obligatoria de issues

Cada issue detectado **DEBE** clasificarse en **una sola** de las siguientes categorías.

---

### 🛠️ Hotfix Técnico

**Criterios de clasificación:**
- Crash de vista
- Import roto
- Error de bundler (Vite)
- Alias incorrecto
- Guard mal aplicado
- Error 401 / 500 técnico
- Acción CRU(D) que rompe la UI

**Acciones obligatorias del Stage:**

1) Crear carpeta:

~~~text
hotfix/HF-TECH-XXX/
~~~

2) Generar los siguientes archivos:

~~~text
hotfix/HF-TECH-XXX/fix_description.md
hotfix/HF-TECH-XXX/analysis.md
hotfix/HF-TECH-XXX/metadata.md
~~~

📌 Estos hotfixes quedan **habilitados exclusivamente** para Workflow 71.

---

### 🧩 Gap Funcional / Producto

**Criterios de clasificación:**
- Funcionalidad existente no accesible
- Menú incompleto o inconsistente
- Flujo funcional degradado
- Comportamiento esperado no reflejado
- Feature existente pero no expuesta en UI

**Acciones obligatorias del Stage (solo documentales):**

1) Crear carpeta:

```text
gaps/GAP-XXX/
```

2) Generar **únicamente** los siguientes archivos DRAFT.

---

#### 📄 `gaps/GAP-XXX/fix_description.draft.md`

Contenido mínimo obligatorio:

```md
Origen:
Detectado en Workflow 70 — Stabilization Scan.

Síntoma observable:
<descripción objetiva basada en evidencia runtime>

Evidencia asociada:
- qa/stabilization_evidence.md
- ui/menu_runtime_report.md
- ui/ui_runtime_errors.md (si aplica)

Impacto funcional:
<impacto visible para el usuario final>

Nota:
Este documento es un DRAFT.
No habilita corrección automática.
Requiere decisión humana explícita.

Reglas:
- No proponer soluciones
- No definir implementación
- No asignar prioridad
```

---

#### 📄 `gaps/GAP-XXX/metadata.draft.md`

Contenido mínimo obligatorio:

```yaml
gap_id: GAP-XXX
origen_workflow: 70
tipo_sugerido: FUNCIONAL | PRODUCTO
area_afectada: menu | flujo | pantalla | negocio
impacto_usuario: <descripción breve>
requiere_decision_humana: true
estado: DRAFT
```

---

## Reglas de Gobierno del Stage

- El Stage F **NO crea** hotfixes funcionales.
- El Stage F **NO ejecuta** Workflow 72.
- El Stage F **NO mueve ni renombra** artefactos.
- Todo lo generado bajo `gaps/` es **NO ejecutable**.

El pasaje de:

```text
gaps/GAP-XXX/
```

a:

```text
hotfix/HF-FUNC-XXX/
```

es **manual, explícito y humano**.

---

## Condición de Completitud del Stage

El Stage F se considera **INCOMPLETO** si:

- Existe al menos un gap funcional detectado
- y **NO existe** su carpeta:

```text
gaps/GAP-XXX/
```

- o falta alguno de los archivos `.draft.md`

Si el Stage F está incompleto → **Workflow 70 = FAIL**.

---

## Regla Final del Stage

Workflow 70 **escribe el análisis**.  
El humano **decide si se corrige**.  
Workflow 72 **solo ejecuta lo decidido**.


---

## Stage G — Documentación de Hotfixes Técnicos

**Workflow:** 70 — Stabilization Scan  
**Rol activo:** Arquitecto  
**Skill:** hotfix-describer

---

## Objetivo del Stage

Documentar formalmente cada **hotfix técnico** detectado y clasificado
en el Stage F, dejando los artefactos listos para su ejecución en el
**Workflow 71**.

Este stage:

- ✔️ Documenta hotfixes técnicos
- ✔️ Genera descripciones auditables
- ✔️ Produce metadata estructurada
- ❌ NO ejecuta correcciones
- ❌ NO prioriza hotfixes
- ❌ NO documenta gaps funcionales
- ❌ NO habilita Workflow 72

---

## Alcance del Stage

Este stage aplica **exclusivamente** a issues clasificados como:

- HF-TECH-XXX

Cualquier issue clasificado como **Gap Funcional / Producto**:

- NO se documenta aquí
- Permanece bajo `gaps/`
- NO es ejecutable

---

## Acciones obligatorias del Stage

Por **cada hotfix técnico** generado en el Stage F:

---

### 1. Verificación de carpeta

Debe existir previamente la carpeta:

```
hotfix/HF-TECH-XXX/
```

Si la carpeta **NO existe** → FAIL inmediato del Stage.

---

### 2. Generación de documentación obligatoria

Dentro de la carpeta del hotfix se deben generar **TODOS** los siguientes archivos:

```
hotfix/HF-TECH-XXX/fix_description.md
hotfix/HF-TECH-XXX/analysis.md
hotfix/HF-TECH-XXX/metadata.md
```

La ausencia de cualquiera de estos archivos invalida el Stage.

---

## Contenido mínimo obligatorio por archivo

### fix_description.md

Debe describir:

- Qué falla
- Dónde ocurre
- Cómo se manifiesta
- Impacto técnico observable

Reglas:

- Basado solo en evidencia del Workflow 70
- No proponer soluciones
- No definir implementación
- No asignar prioridad
- No incluir decisiones funcionales

---

### analysis.md

Debe incluir:

- Causa raíz técnica probable
- Capas o componentes involucrados
- Riesgos de corrección
- Alternativas técnicas (si existen)

---

### metadata.md

Contenido mínimo obligatorio:

```yaml
hotfix_id: HF-TECH-XXX
origen_workflow: 70
tipo: TECNICO
capa: frontend | backend | auth | infra
impacto: bloqueo_total | parcial | degradacion
rutas_afectadas:
  - /ruta-ejemplo
estado: DOCUMENTADO
```

---

## Reglas de Gobierno del Stage

El Stage G:

- NO crea hotfixes funcionales
- NO escribe archivos bajo `gaps/`
- NO genera drafts
- NO mueve ni renombra carpetas
- NO ejecuta correcciones

El Stage G **SOLO documenta hotfixes técnicos ya clasificados**.

---

## Condición de Completitud del Stage

El Stage G se considera **INCOMPLETO** si:

- Existe al menos un hotfix técnico creado en Stage F
- y falta alguno de los siguientes archivos:
  - fix_description.md
  - analysis.md
  - metadata.md

Si el Stage G está incompleto → **Workflow 70 = FAIL**.

---

## Regla Final del Stage

Workflow 70 detecta y documenta.  
Workflow 71 corrige.

Un hotfix técnico sin documentación completa **NO puede ejecutarse**.

---

## Stage H — Generación de Fix Prompts (Asistido)

**Rol:** Arquitecto  
**Skill:** `fix-prompt-generator`

⚠️ Este stage **NO autoriza correcciones**.  
Solo prepara prompts asistidos.

---

## Stage I — Priorización

**Rol:** Arquitecto  
**Skill:** `hotfix-prioritizer`

### Output
- `hotfix/ORDER.md`

---

## Stage J — Gate Final del Workflow 70: Stabilization Scan

**Checklist aplicado:** `.agent/checklists/stabilization-scan.md`  
**Rol responsable:** Arquitecto

---

## Objetivo del Gate

Garantizar que el sistema fue **completamente relevado, clasificado y documentado**
antes de permitir **cualquier corrección técnica o funcional**.

Este Gate es **bloqueante y no negociable**.

---

## Condiciones de PASS (TODAS obligatorias)

### 1️⃣ Inventarios Técnicos

- Existen y están completos:
  - `architecture/routes_inventory.md`
  - `architecture/view_load_report.md`
  - `ui/crud_matrix.md`
  - `backend/endpoints_inventory.md`

---

### 2️⃣ Runtime Scan (si `execution_mode = hybrid`)

- Stage E fue ejecutado completamente
- Existe `qa/stabilization_evidence.md`
- Existe `ui/menu_runtime_report.md`
- No existen menús o subítems **sin evidencia explícita de navegación**

---

### 3️⃣ Clasificación de Issues

- **Todos los issues detectados** fueron clasificados
- No existen issues sin categoría asignada

---

### 4️⃣ Hotfixes Técnicos

- Existe al menos uno o más hotfixes técnicos **si fueron detectados**
- **Todos los hotfixes técnicos detectados en Stage F**
  están **completamente documentados** en Stage G
- Para cada `hotfix/HF-TECH-XXX/` existen obligatoriamente:
  - `fix_description.md`
  - `analysis.md`
  - `metadata.md`

---

### 5️⃣ Gobierno y Priorización

- Existe el archivo `hotfix/ORDER.md`
- No existen hotfixes técnicos sin documentación completa
- No existen hotfixes técnicos fuera de `hotfix/ORDER.md`

---

## Condiciones de FAIL (cualquiera)

- Falta algún inventario obligatorio
- Runtime incompleto o no ejecutado cuando correspondía
- Evidencia insuficiente o inexistente
- Existe al menos un hotfix técnico sin:
  - `fix_description.md`
  - `analysis.md`
  - `metadata.md`
- Existen issues no clasificados
- Existen gaps funcionales **sin drafts documentales**

---

## Efecto del Gate

### Gate = PASS

Se habilita la ejecución de:

- **Workflow 71 — Hotfix Técnico**
- **Workflow 72 — Hotfix Funcional / Producto**
- **Workflow 03 — Feature Evolution**

---

### Gate = FAIL

- Se bloquea la ejecución de:
  - Workflow 71
  - Workflow 72
  - Workflow 03
- El sistema queda en estado **NO CORREGIBLE**

---

## Regla Operativa Final

**Workflow 70 detecta y prepara.  
Workflow 71 corrige lo técnico.  
Workflow 72 corrige lo funcional.  
Sin Gate PASS, no se toca código.**

