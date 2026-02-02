---
description: Detectar, clasificar y documentar todos los errores técnicos y gaps funcionales que impiden que el sistema opere de forma estable end-to-end, sin modificar código
---

# Workflow 70 — Stabilization Scan & Hotfix Preparation (V2.0)

## Propósito
Analizar el sistema **en su estado actual** para detectar errores técnicos que impidan un funcionamiento estable, **clasificarlos**, **priorizarlos** y **preparar hotfixes corregibles**, **sin aplicar cambios de código**.

Este workflow **NO corrige**: deja todo listo para que el Workflow 71 (o ejecución manual) aplique correcciones **de manera determinística y auditable**.

---

## REQ esperado
`REQ-STABILIZATION-SCAN`

**Base path de outputs:**
`.artifacts/requests/REQ-STABILIZATION-SCAN/`

---

## Principios (No negociables)
- ❌ No corregir código
- ❌ No introducir cambios funcionales
- ❌ No refactor / cleanup / reorganización
- ✅ Detectar, documentar y preparar correcciones
- ✅ Cada hotfix debe ser **acotado** y **ejecutable sin reinterpretación**
- ✅ Separar:
  - **Hotfix técnico** (crash, import roto, alias, guard, 401, 500, seed faltante, etc.)
  - **Gap funcional / producto** (menú faltante, feature no implementada, flujo incompleto)
- ✅ Los prompts generados en este workflow son **asistidos** (para humanos), **no autorizan ejecución automática**


## Roles involucrados
- Orchestrator
- Arquitecto de Software Senior
- Frontend Engineer
- Backend Engineer
- QA Engineer

> Nota: Antigravity no “relaciona” roles/skills/workflows mágicamente.
> El workflow **declara** roles y skills para **guiar** la ejecución y estandarizar outputs.

## Skills utilizados (declarativos)
- `route-inventory-scan`
- `lazy-import-analysis`
- `frontend-crud-detection`
- `backend-endpoint-observer`
- `auth-flow-classifier`
- `hotfix-classifier`
- `hotfix-describer`
- `fix-prompt-generator`
- `hotfix-prioritizer`

> Si algún skill no existe en `.agent/skills/...`, el Orchestrator debe:
> 1) Registrar el faltante en `gaps/skills_missing.md`
> 2) Continuar el workflow con un procedimiento manual equivalente (sin inventar código).

## Checklist/Gates usados
- `.agent/checklists/gate_stabilization_scan.md`

## Estructura esperada de outputs (por ejecución)
.artifacts/requests/REQ-STABILIZATION-SCAN/input.md
architecture/routes_inventory.md
lazy_import_issues.md
view_load_report.md
ui/crud_matrix.md
missing_operations.md
ui_runtime_errors.md
backend/endpoints_inventory.md
auth_issues.md
server_errors.mdhotfix/ORDER.md
HF-XXX/fix_description.md
analysis.md
fix_prompt.md
metadata.md
gaps/functional_gaps.md
menu_gaps.md
skills_missing.md
qa/stabilization_evidence.md
gate_result.md
run_log.md


---

## Stage A — Inicialización y Detección de Runtime Browser

**Rol:** Orchestrator  
**Objetivo:** Inicializar el Workflow 70 y determinar de forma **explícita y técnica**
si es posible ejecutar navegación y CRU(D) en runtime.

---

### Precondiciones

- Debe existir:
  - `.artifacts/requests/REQ-STABILIZATION-SCAN/input.md`
- Si existen ejecuciones previas:
  - Ignorar completamente (clean run)

---

### Registro de Ejecución

Crear:
.artifacts/requests/REQ-STABILIZATION-SCAN/run_log.md

Contenido mínimo:
- Fecha / hora
- Workflow: 70
- REQ
- Tipo: stabilization-scan

---

### Browser Context (Declarado)

- Browser: Chromium
- Protocolo: CDP
- Endpoint esperado: `ws://127.0.0.1:9222`
- Base URL App: `http://localhost:5173`

---

### Validación Técnica de Browser (OBLIGATORIA)

Ejecutar validación explícita:

- Verificar acceso a:
  - `http://127.0.0.1:9222/json/version`
- Verificar presencia de:
  - `webSocketDebuggerUrl`

#### Resultado

- Si el endpoint responde y contiene `webSocketDebuggerUrl`:
  - `execution_mode = hybrid`
  - Runtime browser **HABILITADO**
- Si NO responde:
  - `execution_mode = static`
  - Runtime browser **NO disponible**

Registrar resultado en `run_log.md`.

⚠️ Advertencias de DBUS / xdg-settings **NO invalidan** el browser si CDP responde.

### Contexto Técnico Base

- Frontend: Vue 3 + Vite (lazy routes)
- Backend: FastAPI + JWT
- Objetivo: estabilidad técnica, navegación completa y CRU(D) sin cancelaciones

### Output del Stage

- `run_log.md`
- `execution_mode` definido explícitamente
- Browser runtime habilitado o degradado con causa técnica

### Regla No Negociable

> **Si `execution_mode = hybrid`, el workflow DEBE ejecutar navegación y CRU(D) en runtime.**

# Stage B — Inventario de Rutas y Vistas

**Rol:** Frontend Engineer  
**Skills:** `route-inventory-scan`, `lazy-import-analysis`

## Acciones
1. Enumerar rutas desde el router (incluyendo módulos).
2. Detectar vistas lazy-loaded.
3. Verificar resolución estática:
   - imports relativos
   - aliases (`@domain`, `@ui`, `@shared`, etc.)
4. Documentar:
   - imports rotos
   - rutas inexistentes
   - aliases inconsistentes

## Output
- `architecture/routes_inventory.md`
- `architecture/lazy_import_issues.md`

---

# Stage C — Detección de CRU(D) en Frontend

**Rol:** Frontend Engineer + QA  
**Skill:** `frontend-crud-detection`

## Acciones
1. Detectar vistas CRUD por convención:
   - List
   - Form
   - Create / Update / Delete (si existe)
2. Para cada CRUD detectado, registrar:
   - vista list
   - vista form
   - composables usados
   - repositorios/clients usados
   - endpoints esperados
3. Identificar gaps técnicos:
   - composables stub
   - servicios no implementados
   - imports rotos
   - componentes faltantes

## Output
- `ui/crud_matrix.md`
- `ui/missing_operations.md`

---

# Stage D — Observación de Backend y Autenticación

**Rol:** Backend Engineer  
**Skills:** `backend-endpoint-observer`, `auth-flow-classifier`

## Acciones
1. Enumerar endpoints consumidos por el frontend (desde repositorios/clients).
2. Clasificar semánticamente:
   - 401 esperado (no token / expirado)
   - 401 inesperado (guard mal aplicado / endpoint debería ser público)
   - 403 (RBAC)
   - 500 (server error)
3. Documentar:
   - endpoints críticos
   - rutas bloqueadas por auth
   - 500 con posible causa raíz

## Output
- `backend/endpoints_inventory.md`
- `backend/auth_issues.md`
- `backend/server_errors.md`

---

# Stage E — Runtime Scan (si es posible) + Evidencia

**Rol:** QA  
**Skills:** (si aplica) browser automation / o procedimiento manual documentado

## Objetivo
Verificar en runtime (si se puede):
- que las rutas navegan
- que las vistas lazy-loaded cargan
- que el UI no crashea en pantalla
- que CRU(D) no revienta por errores técnicos

## Acciones (modo HYBRID con browser)
1. Abrir app en dev (ej: `http://localhost:5173/`).
2. Navegar rutas enumeradas.
3. Capturar:
   - errores de consola
   - fallas de navegación
   - fallas al cargar módulos (dynamic import)
4. Para cada CRUD:
   - cargar List
   - abrir Create
   - abrir Edit
   - ejecutar Delete si existe (sin confirmar si la UI cancela; **NO cancelar nada**)

## Acciones (modo STATIC sin browser)
1. Registrar explícitamente que no se pudo hacer runtime.
2. Producir reportes de “predicción de runtime” basados en análisis estático.
3. Marcar el Gate como FAIL si el checklist exige runtime.

## Output
- `qa/stabilization_evidence.md`
- `architecture/view_load_report.md`
- `ui/ui_runtime_errors.md` (si aplica)

---

# Stage F — Clasificación: Hotfix vs Gap

**Rol:** Arquitecto + Orchestrator  
**Skill:** `hotfix-classifier`

## Acciones
1. Agrupar issues por causa raíz.
2. Clasificar cada issue:
   - **Hotfix técnico** (crash, import, alias, guard, seed, 500, 401 inesperado)
   - **Gap funcional** (menú faltante, feature sin implementar, flujo incompleto)
3. Crear:
   - Hotfixes bajo `hotfix/HF-XXX/`
   - Gaps bajo `gaps/*.md`

## Output
- `gaps/functional_gaps.md`
- `gaps/menu_gaps.md`
- Hotfix folders creados (ver Stage G)

---

# Stage G — Creación de Hotfixes + Descripción (SIN código)

**Rol:** Arquitecto  
**Skill:** `hotfix-describer`

## Acciones (por cada hotfix `HF-XXX`)
1. Crear carpeta:
   - `.artifacts/requests/REQ-STABILIZATION-SCAN/hotfix/HF-XXX/`
2. Generar:
   - `fix_description.md` (qué falla, dónde, impacto, criterio de corrección)
   - `analysis.md` (causa raíz, opciones, riesgos)
   - `metadata.md` (severidad, capa, rutas afectadas, endpoints, tags)

## Output (por hotfix)
- `hotfix/HF-XXX/fix_description.md`
- `hotfix/HF-XXX/analysis.md`
- `hotfix/HF-XXX/metadata.md`

---

# Stage H — Generación de Fix Prompt por Hotfix (ASISTIDO / NO EJECUTABLE)

**Rol:** Arquitecto  
**Skill requerido:** `fix-prompt-generator`  
**Template obligatorio:** `.agent/templates/fix_prompt.template.md`

## Objetivo
Para cada hotfix detectado, generar un **prompt acotado, gobernado y copiable**
para que un humano lo ejecute manualmente en Antigravity (o para usarlo como input del Workflow 71).

## Características del Stage (CRÍTICO)
- Tipo: **Asistido (NO ejecutable)**
- Side effects: **Ninguno**
- Dependencia de Gate: **No bloqueante**
- Permitido con Gate FAIL: **Sí**
- Uso: **Manual por desarrollador**
- Habilita ejecución automática: ❌ No

> Este stage **NO autoriza correcciones**, solo prepara el texto/prompt.

## Acciones (por cada `hotfix/HF-XXX`)
1. Verificar existencia del template:
   - `.agent/templates/fix_prompt.template.md`
   - Si falta: registrar en `gaps/skills_missing.md` y generar un prompt básico igualmente (sin inventar hechos).
2. Completar variables mínimas del template:
   - `{{HOTFIX_ID}}`
   - `{{WORKFLOW_ID}}` = `71` (o `05` si tu nomenclatura interna lo define así)
   - `{{ROL_EJECUTOR}}` (Frontend/Backend según metadata)
   - `{{DESCRIPCION_PROBLEMA}}` (desde `fix_description.md`)
   - `{{ARCHIVOS_INVOLUCRADOS}}` (estimados/observados)
   - `{{VALIDACIONES_ESPERADAS}}` (criterio de “fix done”)
   - `{{EVIDENCIA_REQUERIDA}}` (logs, screenshots, tests, etc.)
3. Generar:
   - `hotfix/HF-XXX/fix_prompt.md`

## Output (por hotfix)
- `hotfix/HF-XXX/fix_prompt.md`

---

# Stage I — Priorización de Hotfixes

**Rol:** Arquitecto  
**Skill:** `hotfix-prioritizer`

## Criterios de prioridad (en orden)
1. Bloqueo total de navegación
2. Fallo de load de vistas (dynamic import)
3. Autenticación rota (login loop / 401 sistemático)
4. 500 del backend en endpoints core
5. CRU(D) rompe UI (crash)
6. Inestabilidad JS / componentes
7. Deuda técnica no bloqueante

## Output
- `hotfix/ORDER.md`

---

# Stage J — Gate: Stabilization Scan

**Checklist aplicado:** `.agent/checklists/gate_stabilization_scan.md`

## Condiciones PASS (mínimas)
- Rutas enumeradas ✅
- Issues clasificados ✅
- Hotfixes documentados ✅
- Existe `hotfix/ORDER.md` ✅
- (Si el checklist lo exige) runtime navegó rutas / cargó vistas / probó CRUD ✅

## Condiciones FAIL (típicas)
- No se pudo hacer runtime y el checklist lo exige
- Quedan rutas sin evaluar
- No se pudieron cargar vistas lazy-loaded
- No hay evidencia de CRUD
- Hotfixes sin descripción o sin orden

## Output
- `gate_result.md` (incluye PASS/FAIL + motivos)
- `qa/stabilization_evidence.md` (siempre)

---

## Resultado esperado del Workflow 70
### Si Gate = PASS
Deja todo listo para ejecutar Workflow 71 (Hotfix Execution).

### Si Gate = FAIL
Igualmente deja:
- inventarios
- clasificación
- hotfix descriptions
- prompts asistidos (Stage H)
- ORDER.md
pero **bloquea** correcciones automáticas hasta re-ejecución o habilitación explícita.

---

## Relación con otros Workflows
- **Workflow 71**: ejecuta **un solo hotfix** (tomando `fix_prompt.md` + `fix_description.md`)
- **Workflow 03**: NO aplica durante estabilización
- **Workflow 70**: puede re-ejecutarse “desde cero” creando una nueva corrida (ver nota abajo)

---

## Nota operativa: “Ejecutar desde cero”
Para evitar que Antigravity “use memoria” de ejecuciones previas:

1. Crear un nuevo REQ de corrida:
   - `REQ-STABILIZATION-SCAN-RUN-YYYYMMDD-HHMM` (o similar)
2. Copiar `input.md` a ese nuevo folder.
3. Ejecutar Workflow 70 apuntando al nuevo REQ.

> Regla: **cada corrida = un folder nuevo**, nunca se pisa el anterior.

---

## Regla Final
**Workflow 70 prepara el terreno. Workflow 71 es el único autorizado a corregir.**