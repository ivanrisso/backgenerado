Modificar `app/services/recibo_service.py` para poblar correctamente los datos del Cliente en los Recibos.

**Requerimientos:**
1.  Inyectar `ClienteRepositoryInterface` (o su implementación) en `ReciboService.__init__`.
2.  En `create_recibo`, utilizar `cliente_repo.get_by_id(data.cliente_id)` para obtener el Cliente.
3.  Si el cliente no se encuentra, lanzar `ClienteNoEncontrado` (importar o crear si no existe).
4.  Reemplazar los valores placeholder en el constructor de `Comprobante(...)` con datos reales:
    *   `doc_nro`: Usar `cliente.cuit` (o DNI si aplica).
    *   `nombre_cliente`: Usar `cliente.razon_social` o `cliente.nombre` + `cliente.apellido`.
    *   `cuit_cliente`: Usar `cliente.cuit`.
    *   `domicilio_cliente`: Usar `cliente.domicilio` (si existe) o un string formateado.
    *   `localidad_cliente`, `cod_postal_cliente`, `provincia_cliente`: Poblar desde los atributos del cliente (si existen) o "-".
5.  Mantener la lógica existente para `concepto_id` y `tipo_doc_id` si el Cliente no los provee directamente.

**Verificación:**
- Crear un Recibo vía API o Test.
- Verificar que la tabla `Comprobante` tenga los datos correctos en `nombre_cliente` y `cuit_cliente` en lugar de "Cliente"/"00000000".
