# Runbook — Workflow 70: Stabilization Scan

## Objetivo
Ejecutar un escaneo técnico integral del sistema para detectar, clasificar y
preparar hotfixes que impidan la estabilidad operativa, sin aplicar correcciones
de código.

Este runbook define **cómo** se ejecuta el Workflow 70.
El workflow solo lo referencia.

---

## Contexto de Ejecución

- Workflow: 70
- Tipo: Stabilization Scan
- Correcciones: ❌ NO
- Preparación de hotfixes: ✅ SÍ
- Runtime browser: Condicional (CDP)

---

## Resolución del REQ Activo

1. Leer el archivo: .artifacts/requests/current.req
2. Extraer el valor leído se considera `{{CURRENT_REQ}}`
3. Todos los artefactos se escriben bajo:
.artifacts/requests/{{CURRENT_REQ}}/

⚠️ Nunca se hardcodea el REQ dentro del workflow.

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

---
### A1 — Resolución del REQ
1. Leer:.artifacts/requests/current.req
2. Si no existe → ABORTAR
3. Usar su valor como `{{CURRENT_REQ}}`
---
### A2 — Validación de Input
Debe existir:
.artifacts/requests/{{CURRENT_REQ}}/input.md

Si no existe → ABORTAR
---
### A3 — Registro de Ejecución
Crear: .artifacts/requests/{{CURRENT_REQ}}/run_log.md

Contenido mínimo:
- Fecha / hora
- Workflow: 70
- REQ activo
- Tipo: stabilization-scan

---

### A4 — Detección Técnica de Browser Runtime (CDP)

**Browser declarado:**
- Chromium (externo)
- Protocolo: CDP
- Endpoint esperado: http://127.0.0.1:9222/json/version

**Validación obligatoria:**
- El endpoint debe responder
- Debe existir el campo `webSocketDebuggerUrl`

---

### A5 — Determinación del Modo de Ejecución

- Si la validación CDP es EXITOSA:
- `execution_mode = hybrid`
- Runtime browser HABILITADO

- Si la validación CDP FALLA:
- `execution_mode = static`
- Runtime browser NO disponible
- Registrar causa técnica

⚠️ Advertencias de DBUS / xdg-settings **NO invalidan** el browser
si el endpoint CDP responde correctamente.

---

### A6 — Registro Final del Stage

Registrar en `run_log.md`:
- execution_mode
- resultado de validación CDP
- motivo de degradación (si aplica)

---

### Regla No Negociable

> Si `execution_mode = hybrid`,
> el workflow **DEBE ejecutar navegación y CRU(D) en runtime**.


## Stage B — Inventario de Rutas y Vistas

**Rol:** Frontend Engineer  
**Skills:** route-inventory-scan, lazy-import-analysis

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

## Stage C — Detección de CRU(D) Frontend

**Rol:** Frontend Engineer + QA  
**Skill:** frontend-crud-detection

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

## Stage D — Observación de Backend y Autenticación

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

## Stage E — Runtime Scan (si aplica)

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

⚠️ Si la UI presenta confirmación modal automática, el QA NO debe interactuar con el modal.


## Acciones (modo STATIC sin browser)
1. Registrar explícitamente que no se pudo hacer runtime.
2. Producir reportes de “predicción de runtime” basados en análisis estático.
3. Marcar el Gate como FAIL si el checklist exige runtime.

## Output
- `qa/stabilization_evidence.md`
- `architecture/view_load_report.md`
- `ui/ui_runtime_errors.md` (si aplica)

---

## Stage F — Clasificación Hotfix vs Gap

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

## Stage G — Documentación de Hotfixes

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

## Stage H — Generación de Fix Prompts (Asistido)

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

## Stage I — Priorización

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

## Stage J — Gate

**Checklist aplicado:** `.agent/checklists/stabilization-scan.md`

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

----

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

- **Workflow 70**: detección, clasificación y preparación de hotfixes.
- **Workflow 71**: ejecución de un hotfix técnico (uno por vez).
- **Workflow 72**: resolución de gaps funcionales o de producto.
- **Workflow 03**: evolución funcional (features). No aplica durante estabilización.

---

## Ejecución desde Cero (Clean Run)

Para evitar reutilización de contexto o artefactos previos:

1. Crear un nuevo REQ de corrida, por ejemplo:
   `REQ-STABILIZATION-SCAN-RUN-YYYYMMDD-HHMM`
2. Copiar el `input.md` base dentro de ese nuevo REQ.
3. Ejecutar el Workflow 70 apuntando a ese REQ.

**Regla:** cada corrida usa un folder nuevo. Nunca se pisa una ejecución anterior.

---

## Alcance Funcional del Workflow 70

Workflow 70 **NO valida reglas de negocio**.

Un hotfix funcional solo se detecta cuando existe
un **síntoma técnico observable**, por ejemplo:
- crash de vista
- loop de navegación
- bloqueo de acción CRUD
- error runtime que impide operar

Si el problema es de lógica de negocio o comportamiento esperado,
se registra como **Gap Funcional** y se deriva a Workflow 72.

---

## Consideraciones sobre Runtime Browser

- La ejecución runtime depende de la disponibilidad de un navegador automatizable.
- Errores de DBUS, xdg-settings o warnings del entorno **no invalidan**
  el navegador si el endpoint CDP responde correctamente.
- Si el runtime no está disponible, el workflow degrada a modo `static`
  y el Gate puede fallar según el checklist aplicado.

---

## Regla Operativa Final

**Workflow 70 prepara el terreno.  
Ninguna corrección debe realizarse sin pasar por Workflow 71 o 72.**
