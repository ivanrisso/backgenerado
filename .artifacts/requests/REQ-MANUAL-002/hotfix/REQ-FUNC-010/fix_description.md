# Fix Description — HF-FUNC-MENU-ORDER

## Origen

Requerimiento funcional detectado durante el uso del sistema de configuración
de menús.

El sistema actualmente **no permite definir el orden relativo** de los ítems
de menú, lo que impide controlar la prioridad visual y funcional de la navegación.

---

## Problema funcional

En la configuración actual del menú:

- Los ítems se renderizan en el sidebar
  sin un criterio de orden explícito configurable.
- El orden depende de:
  - inserción
  - orden natural de datos
  - comportamiento implícito del frontend

Esto genera que:

- Menús principales aparezcan después de secundarios.
- Cambios de menú no reflejen una intención clara de orden.
- No exista forma de priorizar flujos críticos.

---

## Comportamiento actual

- El menú se muestra en un orden implícito.
- No existe un atributo funcional de orden.
- El usuario administrador no puede controlar
  qué menú aparece antes que otro.

---

## Comportamiento esperado

- Cada ítem de menú debe tener un **orden configurable**.
- El orden debe ser:
  - explícito
  - persistente
  - respetado por el sidebar
- El usuario debe poder definir:
  - qué menú aparece primero
  - qué menú aparece después

El orden definido debe reflejarse **directamente en la navegación lateral**.

---

## Alcance del cambio

Incluye:
- Configuración funcional de orden de menú.
- Render del sidebar respetando dicho orden.

No incluye:
- Nuevas funcionalidades de negocio.
- Cambios de permisos.
- Cambios visuales no relacionados con orden.

---

## Restricciones

- ❌ No modificar reglas de negocio
- ❌ No introducir nuevas features no relacionadas
- ❌ No refactor técnico general
- ✔️ Cambio funcional controlado y explícito
