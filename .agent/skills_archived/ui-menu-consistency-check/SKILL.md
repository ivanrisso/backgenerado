# SKILL — UI Menu Consistency Check

## Rol autorizado
- **QA**
- **Orchestrator** (solo lectura / clasificación)

⚠️ Este skill **NO autoriza correcciones**.

---

## Objetivo

Detectar **inconsistencias observables de menú y navegación** en runtime,
cuando el comportamiento visible de la UI **no coincide** con lo esperado
a partir de las pantallas existentes o solicitadas.

Este skill permite identificar **gaps funcionales o de producto**
a partir de síntomas observables, **sin validar reglas de negocio**.

---

## Tipo de detección

- 🔍 **Observacional (UI runtime)**
- 🔍 **No inferencial**
- 🔍 **No declarativa**
- 🔍 **No basada en PRD**

---

## Qué detecta este skill

✔️ Pantallas existentes **no accesibles desde menú**  
✔️ Ítems de menú que:
- no aparecen
- aparecen duplicados
- llevan a rutas inexistentes
- llevan a vistas vacías o rotas  
✔️ Flujos creados que **no son navegables por UI**
✔️ Menús que quedaron **desalineados con la navegación real**
✔️ Acciones “huérfanas” (pantalla existe, menú no)

---

## Qué NO detecta (NO negociable)

- ❌ Reglas de negocio incorrectas
- ❌ Falta de permisos esperados
- ❌ UX mejorable
- ❌ Cambios solicitados pero no implementados
- ❌ Features nuevas

👉 Eso **NO es Stabilization Scan**  
👉 Eso se deriva a **Workflow 72 o 03**

---

## Precondiciones obligatorias

- `execution_mode = hybrid`
- Runtime browser disponible (CDP / Playwright / manual documentado)
- Rutas ya inventariadas (Stage B)
- CRUD detectados (Stage C)

Si no se cumplen → **NO ejecutar este skill**

---

## Procedimiento de Ejecución

### 1️⃣ Captura del estado real del menú

- Abrir la aplicación en runtime
- Capturar visualmente:
  - menú principal
  - submenús
  - navegación lateral / superior
- Registrar:
  - texto visible
  - orden
  - rutas asociadas

---

### 2️⃣ Cruce con rutas y vistas existentes

Comparar menú visible contra:

- `architecture/routes_inventory.md`
- `ui/crud_matrix.md`

Buscar:
- rutas existentes **no accesibles desde menú**
- ítems de menú que apuntan a rutas inexistentes
- entradas de menú sin vista funcional

---

### 3️⃣ Detección de inconsistencias

Registrar como **ISSUE OBSERVABLE** cuando ocurra cualquiera:

- La pantalla existe pero no hay forma de acceder por UI
- El menú prometía una acción que no ocurre
- Un ítem de menú desapareció sin explicación técnica
- Un ítem existe pero rompe navegación
- Se pidió explícitamente una pantalla y:
  - existe técnicamente
  - pero **no está expuesta en menú**

⚠️ No asumir intención  
⚠️ No corregir  
⚠️ No completar trabajo faltante

---

## Clasificación del Hallazgo

### Si el problema es:

| Caso observado | Clasificación |
|----------------|---------------|
Pantalla existe pero menú no | **Gap Funcional / Producto** |
Menú apunta a ruta rota | **Hotfix Técnico** |
Menú rompe navegación | **Hotfix Técnico** |
Menú incompleto respecto a flujo esperado | **Gap Funcional** |
Elemento eliminado sin romper UI | **Gap Funcional** |

---

## Output obligatorio

Uno (o ambos) de los siguientes archivos:

### Gap funcional
gaps/menu_gaps.md


### Error técnico
ui/ui_runtime_errors.md


Cada entrada debe incluir:
- ruta
- ítem de menú
- comportamiento observado
- impacto visible
- evidencia (texto / screenshot / descripción)

---

## Relación con workflows

- **Workflow 70**
  - Usa este skill para **detectar y clasificar**
- **Workflow 71**
  - ❌ NO aplica (salvo que el menú rompa técnicamente)
- **Workflow 72**
  - ✔️ Destino natural de gaps de menú / producto
- **Workflow 03**
  - ✔️ Si el cambio es una feature nueva

---

## Regla final (NO negociable)

> **Un menú inconsistente es un problema funcional  
> solo cuando se observa en runtime.**

> **Este skill detecta.  
> Nunca corrige.**

