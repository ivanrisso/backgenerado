# Gate — Workflow 10: System Architecture Definition (SAD)

## Objetivo

Garantizar que el sistema cuente con una **arquitectura definida, explícita,
coherente y verificable** antes de permitir cualquier workflow operativo.

Este Gate convierte al **System Architecture Definition (SAD)** en un
**contrato obligatorio del sistema**.

---

## Artefactos obligatorios del SAD

El Gate DEBE verificar la existencia de los siguientes archivos
bajo el REQ activo:

```text
.architecture/
├─ architectural_principles.md
├─ allowed_stack.md
├─ forbidden_patterns.md
├─ deployment_topology.md
├─ security_baseline.md
├─ integration_constraints.md
```

---

## Reglas de validación por archivo

Cada archivo del SAD DEBE cumplir **TODAS** las siguientes condiciones:

- Estar redactado en **ESPAÑOL**
- Tener contenido explícito (no placeholders)
- Definir reglas **verificables**
- No contener ambigüedades del tipo:
  - “a definir”
  - “depende”
  - “según implementación”

Si algún archivo:
- no existe
- está vacío
- contiene definiciones vagas  

→ **FAIL inmediato del Gate**

---

## Checklist del Gate

### Principios de Arquitectura
- [ ] Existen principios numerados y claros
- [ ] Cada principio es verificable
- [ ] No hay contradicciones internas

### Stack Tecnológico
- [ ] Stack permitido definido explícitamente
- [ ] Tecnologías prohibidas listadas
- [ ] Versiones o familias establecidas

### Patrones y Antipatrones
- [ ] Patrones obligatorios definidos
- [ ] Antipatrones prohibidos definidos
- [ ] No hay solapamientos

### Topología de Despliegue
- [ ] Modelo definido (monolito / microservicios / híbrido)
- [ ] Entornos definidos (dev / qa / prod)
- [ ] Responsabilidades claras por servicio

### Seguridad
- [ ] Modelo de autenticación definido
- [ ] Modelo de autorización definido
- [ ] Gestión de secretos definida

### Integraciones
- [ ] Contratos externos definidos
- [ ] Límites del sistema explícitos
- [ ] Responsabilidades claras

---

## Condiciones de PASS

El Gate se considera **PASS** únicamente si:

- Todos los artefactos obligatorios existen
- Todos cumplen las reglas de validación
- No existen contradicciones entre documentos
- El Arquitecto valida formalmente el SAD

---

## Condiciones de FAIL

El Gate se considera **FAIL** si:

- Falta al menos un artefacto obligatorio
- Algún archivo es ambiguo o incompleto
- El SAD no es verificable
- Existen contradicciones arquitectónicas

---

## Efecto del Gate

### Gate = PASS
Se habilita la ejecución de:
- Workflow 70 — Stabilization Scan
- Workflow 03 — Feature Evolution

### Gate = FAIL
Se bloquea la ejecución de:
- Workflow 70
- Workflow 71
- Workflow 72
- Workflow 03

---

## Regla Final del Gate

> **Sin SAD aprobado, no existe sistema gobernado.**  
> **Sin Gate PASS, ningún workflow operativo puede ejecutarse.**
