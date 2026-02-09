---
description: Workflow 10 — System Architecture Definition (SAD)
---

# Workflow 10 — System Architecture Definition (SAD)

**Nivel:** FUNDACIONAL  
**Tipo:** Definición de Arquitectura de Sistema  
**Aplica a:** Proyectos desde cero / Redefiniciones mayores  
**Correcciones:** ❌ NO  
**Ejecución técnica:** ❌ NO  
**Código:** ❌ NO  

---

## Propósito

Definir de forma **explícita, gobernada y persistente** la arquitectura base del sistema
antes de cualquier desarrollo, corrección o evolución funcional.

Este workflow establece:

- Las **reglas del sistema**
- Las **decisiones arquitectónicas**
- El **stack permitido**
- Los **límites no negociables**

Todo workflow posterior **DEBE obedecer** lo definido aquí.

---

## Principio Rector (NO negociable)

> **La arquitectura se define una sola vez y se gobierna siempre.**  
> Ningún hotfix, feature o refactor puede reinterpretarla.

---

## Qué hace este workflow

✔️ Analiza RFP y propuesta técnica  
✔️ Define arquitectura target  
✔️ Establece reglas duras  
✔️ Genera artefactos de gobierno  
✔️ Habilita validación en workflows posteriores  

---

## Qué NO hace este workflow

- ❌ No genera código
- ❌ No ejecuta tests
- ❌ No crea REQs operativos
- ❌ No corrige bugs
- ❌ No implementa features

---

## Inputs permitidos

Debe existir al menos uno:

- RFP / Anexo técnico del cliente
- Propuesta técnica interna
- Lineamientos estratégicos (cloud, seguridad, stack)

⚠️ Estos documentos son **insumo**, no output.

---

## Roles involucrados

- **Arquitecto de Software** (responsable)
- **Arquitecto de Solución**
- **Product Owner** (validación funcional)
- **Security / Infra** (si aplica)

⚠️ QA y Developers **NO participan**.

---

## Resolución del REQ

Este workflow **NO usa** `.artifacts/requests/current.req`.

Los artefactos generados viven en:
.architecture/


Son **globales al proyecto**.

---

## Artefactos de salida (OBLIGATORIOS)

El workflow **DEBE generar** la siguiente estructura:

.architecture/
├─ system_overview.md
├─ architectural_principles.md
├─ allowed_stack.md
├─ forbidden_patterns.md
├─ service_boundaries.md
├─ api_governance.md
├─ security_baseline.md
├─ observability_baseline.md
├─ deployment_model.md
└─ workflow_contracts.md


La ausencia de cualquiera → **Workflow FAIL**.

---

## Stage A — Contexto y Alcance del Sistema

**Rol:** Arquitecto  
**Objetivo:** Definir qué sistema se está construyendo.

### Output
`system_overview.md`

Contenido mínimo:
- Objetivo del sistema
- Usuarios principales
- Contexto de negocio
- Sistemas externos
- Suposiciones explícitas

---

## Stage B — Principios Arquitectónicos

**Rol:** Arquitecto  
**Skill conceptual:** architectural-principles

### Output
`architectural_principles.md`

Debe incluir:
- Principios (ej: Microservicios, API First, Stateless)
- Justificación de cada principio
- Qué problemas resuelve
- Qué decisiones habilita

---

## Stage C — Stack Permitido

**Rol:** Arquitecto  
**Skill conceptual:** stack-definition

### Output
`allowed_stack.md`

Debe listar explícitamente:
- Lenguajes permitidos
- Frameworks permitidos
- Bases de datos
- Infraestructura
- Herramientas de observabilidad
- CI/CD

⚠️ Todo lo no listado se considera **NO permitido**.

---

## Stage D — Patrones Prohibidos

**Rol:** Arquitecto  
**Skill conceptual:** anti-patterns

### Output
`forbidden_patterns.md`

Ejemplos:
- Monolitos encubiertos
- Acceso directo a DB entre servicios
- Shared DB
- Lógica de negocio en frontend
- Endpoints sin contrato

---

## Stage E — Límites de Servicios

**Rol:** Arquitecto  
**Skill conceptual:** service-boundaries

### Output
`service_boundaries.md`

Debe definir:
- Qué es un servicio
- Qué NO es un servicio
- Comunicación permitida
- Ownership de datos
- Versionado

---

## Stage F — Gobierno de APIs

**Rol:** Arquitecto  
**Skill conceptual:** api-governance

### Output
`api_governance.md`

Debe incluir:
- OpenAPI obligatorio
- Versionado
- Errores estándar
- Autenticación
- Autorización

---

## Stage G — Baseline de Seguridad

**Rol:** Arquitecto + Security  
**Skill conceptual:** security-baseline

### Output
`security_baseline.md`

Debe definir:
- Autenticación
- Autorización
- Manejo de secretos
- Auditoría
- Cumplimiento normativo (si aplica)

---

## Stage H — Observabilidad y Operación

**Rol:** Arquitecto + Infra  
**Skill conceptual:** observability-baseline

### Output
`observability_baseline.md`

Debe incluir:
- Logging
- Métricas
- Tracing
- Alertas mínimas
- Health checks

---

## Stage I — Modelo de Despliegue

**Rol:** Arquitecto + Infra  
**Skill conceptual:** deployment-model

### Output
`deployment_model.md`

Debe definir:
- Ambientes
- Cloud / On-Prem
- Kubernetes / VM
- Escalado
- Resiliencia

---

## Stage J — Contrato con otros Workflows

**Rol:** Arquitecto  
**Skill conceptual:** workflow-contracts

### Output
`workflow_contracts.md`

Debe especificar:

- Qué valida Workflow 70 contra esta arquitectura
- Qué NO puede corregir Workflow 71
- Qué NO puede redefinir Workflow 72
- Cuándo algo es Gap Arquitectónico

---

## Gate — Architecture Baseline Approval

### PASS si:
- Todos los artefactos existen
- Las reglas son explícitas
- No hay ambigüedades
- El stack está definido
- Los límites están claros

### FAIL si:
- Hay decisiones implícitas
- El stack es ambiguo
- Faltan documentos
- Hay contradicciones

---

## Resultado del Workflow

✔️ Arquitectura definida  
✔️ Gobierno establecido  
✔️ Base obligatoria para todos los desarrollos  
✔️ Workflows 70/71/72 quedan habilitados  

---

## Regla de Autoría (Workflow 10)

El Arquitecto es la **única fuente de verdad** del SAD.

Otros roles:
- aportan insumos
- validan viabilidad
- detectan inconsistencias

Pero:
❌ NO modifican principios
❌ NO redefinen arquitectura
❌ NO aprueban el SAD

---

## Regla Final (NO negociable)

> **Ningún hotfix, feature o evolución puede violar la arquitectura definida en este workflow.**  
>  
> Si ocurre → es **Gap Arquitectónico**, no Hotfix.



