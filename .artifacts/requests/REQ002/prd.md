# PRD — REQ-002

## Resumen
Este requerimiento define la funcionalidad para visualizar un **listado de clientes con saldo deudor** dentro del sistema de facturación.  
La funcionalidad permitirá identificar de manera rápida y confiable qué clientes poseen deuda vigente, facilitando tareas operativas de control, análisis y seguimiento de cobranzas, sin incorporar lógica de cobro ni acciones automáticas.

## Usuarios / Roles
- **Administrador**
  - Acceso completo al listado y a todos los filtros.
- **Usuario administrativo / facturación**
  - Consulta de clientes con saldo deudor.
- **Usuario de cobranzas** (si aplica)
  - Visualización de saldos para seguimiento manual.

## Problema
Actualmente, para conocer qué clientes poseen deuda es necesario:
- Revisar comprobantes de manera individual.
- Calcular saldos manualmente o mediante reportes parciales.
- Cruzar información de facturas, pagos y notas de crédito.

Esto genera:
- Pérdida de tiempo operativo.
- Riesgo de errores en el cálculo.
- Falta de visibilidad clara sobre la deuda total por cliente.

## Solución propuesta
Incorporar una vista/listado que:
- Calcule automáticamente el saldo deudor por cliente.
- Muestre únicamente clientes con saldo mayor a cero.
- Permita ordenar y filtrar por distintos criterios.
- Brinde información clara y actualizada para la toma de decisiones.

La solución será de **consulta**, sin modificar datos ni ejecutar acciones sobre los clientes.

## Alcance / Fuera de alcance
**Alcance**
- Cálculo de saldo deudor consolidado por cliente.
- Listado consultable, ordenable y filtrable.
- Visualización de datos identificatorios del cliente y saldo.

**Fuera de alcance**
- Registro de pagos.
- Gestión de cobranzas.
- Aplicación de intereses, punitorios o recargos.
- Automatizaciones (recordatorios, emails, alertas).
- Conciliación bancaria.

## Reglas de negocio
- El saldo deudor se define como:  
  **Total facturado – pagos imputados – notas de crédito aplicadas**.
- Solo se incluyen clientes con saldo final **mayor a cero**.
- Movimientos anulados o inválidos no deben ser considerados.
- El cálculo debe ser consistente para una misma fecha de corte.
- Los clientes inactivos pueden incluirse o excluirse mediante filtro.

## Si aplica: Reglas fiscales AFIP
- Solo se consideran comprobantes fiscales válidos.
- Las notas de crédito deben estar correctamente asociadas a comprobantes originales.
- No se realizan validaciones en tiempo real contra AFIP.
- El listado no reemplaza reportes fiscales oficiales.

## Casos de ejemplo
- **Cliente A**
  - Facturas: $150.000  
  - Pagos: $100.000  
  - Saldo deudor: $50.000 → **Aparece en el listado**.
- **Cliente B**
  - Facturas: $80.000  
  - Pagos: $80.000  
  - Saldo deudor: $0 → **No aparece**.
- **Cliente C**
  - Facturas: $120.000  
  - Notas de crédito: $20.000  
  - Pagos: $50.000  
  - Saldo deudor: $50.000 → **Aparece en el listado**.

## Métricas de éxito
- Reducción del tiempo necesario para identificar clientes deudores.
- Disminución de errores manuales en el cálculo de saldos.
- Uso recurrente del listado por usuarios administrativos.
- Tiempo de respuesta aceptable del listado bajo carga normal.

## Riesgos y supuestos
- Se asume consistencia en la imputación de pagos y notas de crédito.
- Datos históricos incorrectos pueden impactar el resultado.
- Volúmenes grandes de datos pueden requerir optimización técnica.
- Se asume una única moneda o saldos previamente normalizados.
