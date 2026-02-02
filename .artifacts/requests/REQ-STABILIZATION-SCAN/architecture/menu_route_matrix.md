# Matriz de Cobertura Menú vs Rutas

## 1. Análisis de Coincidencias

| Etiqueta Menú | ID | Ruta Definida en Menú | Ruta en Router | Coincidencia |
|---------------|----|-----------------------|----------------|--------------|
| Dashboard | dashboard | `/` | `/` | ✅ |
| Comprobantes | comprobantes | `/comprobantes` | `/comprobantes` | ✅ |
| Nueva Factura | nuevo-comprobante | `/comprobantes/nuevo` | `/comprobantes/nuevo` | ✅ |
| Directorio | lista-clientes | `/clientes` | `/clientes` | ✅ |
| Cuenta Corriente | cuenta-corriente | `/cuentacorriente` | `/cuentacorriente` | ✅ |
| Saldos Deudores | deudores | `/clientes/deudores` | `/clientes/deudores` | ✅ |
| Maestros (Varios) | varies | `/monedas`... | `/monedas`... | ✅ |

## 2. Gaps Detectados (Rutas Huérfanas)

Las siguientes rutas existen en el Router pero **NO tienen entrada en el Menú**:

1. **`/tipos-comprobante`** (Maestros)
2. **`/domicilios`** (Maestros)
3. **`/telefonos`** (Maestros)
4. **`/recibos/nuevo`** (Tesorería)
5. **`/tipodoms`** (Maestros)

## 3. Conclusión Stage A
Análisis completado. Gaps confirmados.
