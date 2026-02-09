# REQ-ID: REQ-FUNC-RECIBOS-002

## Contexto
Sistema de facturación AR en desarrollo local.
Se detectan errores en el menu y en la llamada a la pantalla de recibos.

## Objetivo
Agregar al menu de tesoreria una pantalla de recibos donde se vean todos los recibos y que existan filtros obligatorio por clientes. Este filtro debe traer todos los recibos del cliente seleccionado. El cliente debe poder seleccionarse desde un select.

La pantalla debe tener un boton de agregar recibo que redirija a la pantalla de creacion de recibo. 
La pantalla debe tener un boton de imprimir recibo que redirija a la pantalla de impresion de recibo.
La pantalla debe tener un boton de eliminar recibo que redirija a la pantalla de eliminacion de recibo.
La pantalla debe tener un boton de modificar recibo que redirija a la pantalla de modificacion de recibo.

## AFIP / Fiscalidad
No aplicar cambios fiscales.
Solo validar estabilidad técnica.

## Criterios de aceptación
- Todas las rutas cargan o fallan de forma documentada
- Hotfixes técnicos identificados y clasificados
- ORDER.md generado

## Riesgos / Supuestos
- Navegador puede no estar disponible (degradar a static)
- CI puede no ejecutarse en local

## Notas técnicas
Base URL: http://localhost:5173
Backend: http://localhost:8000
