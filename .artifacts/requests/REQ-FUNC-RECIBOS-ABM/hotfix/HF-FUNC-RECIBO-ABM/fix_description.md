# Recibo List Missing (ABM Incompleto)

## Problema
El módulo de Tesorería permite crear recibos (`ReciboCreateView`) pero no ofrece una vista para listarlos, buscarlos o anularlos.
El usuario no tiene visibilidad de las cobranzas registradas.

## Comportamiento Actual
- Ruta `/recibos/nuevo` activa.
- Ruta `/recibos` no existe o no tiene componente asignado.
- No hay acceso a historial de recibos.

## Comportamiento Esperado
- Nueva vista `/recibos` (`ReciboListView`).
- Listado paginado de recibos.
- Filtros básicos (cliente, fecha, número).
- Acciones: Ver Detalle, Anular (si aplica). (MVP: Listar + Detalle/Imprimir).
