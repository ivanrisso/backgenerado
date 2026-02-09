# Fix Description — HF-FUNC-MENU-FE-ORDER-COLLAPSE

## Origen

Requerimiento funcional detectado durante la corrección y uso
del módulo de **Configuración de Menús** en frontend.

El comportamiento actual del sidebar y del configurador
no permite reflejar correctamente la jerarquía ni el orden esperado
de los ítems de menú.

---

## Problema funcional

Actualmente, en el frontend:

- Los **menús padres no son colapsables** en el CRUD de menues.
- Los ítems de menú aparecen:
  - sueltos
  - fuera de su jerarquía lógica
  - sin control explícito de orden
- El módulo de **Configuración de Menús**:
  - muestra relaciones padre/hijo
  - ordena los menues por orden de insercion
- No existe forma de definir:
  - el orden de los menús padres
  - el orden de los ítems hijos dentro de cada padre

Esto genera inconsistencia entre:
- lo que el administrador configura
- lo que el usuario final ve y navega

---

## Comportamiento actual

- El sidebar renderiza ítems:
  - sin orden funcional explícito
- El orden depende de:
  - inserción
  - orden implícito del frontend
  - comportamiento no gobernado

---

## Comportamiento esperado

### Jerarquía

- Los **menús padres deben ser colapsables** en el CRUD de menues.
- Los ítems hijos:
  - solo se muestran dentro de su padre
  - no deben aparecer como menús principales.
  - deben de poder ser ordenados mediante un campo orden

### Orden

Desde el frontend debe poder configurarse:

- El **orden de los menús padres**.
- El **orden de los ítems hijos** dentro de cada padre.

El orden definido debe ser:

- explícito
- persistente
- respetado por el sidebar en runtime.
- el orden debe estar dado por el api en el backend

---

## Alcance del cambio

Incluye:
- Lógica frontend para:
  - colapso/expansión de menús padres en el CRUD de menues
  - ordenamiento de padres
  - ordenamiento de hijos
- Render del sidebar respetando:
  - orden configurado tanto de padres como de hijos

---

## Restricciones

- ❌ No modificar reglas de negocio
- ✔️ Cambio funcional controlado y explícito
