# Menu Inventory (REQ-FUNC-004)

```
ID    | Nombre               | Path                           | Parent
----------------------------------------------------------------------
3     | Configuración        | None                           | None 
4     | Seguridad            | None                           | None 
7     | Operadores           | /operadores                    | 3    
8     | Tipos Comprobante    | /tipos-comprobante             | 3    
9     | Conceptos            | /conceptos                     | 3    
10    | Monedas              | /monedas                       | 3    
11    | IVAs                 | /ivas                          | 3    
12    | Tipos Impuesto       | /tipos-impuesto                | 3    
13    | Usuarios             | /usuarios                      | 4    
14    | Roles                | /roles                         | 4    
15    | Menús                | /menus                         | 4    
16    | Clientes             | /clientes                      | 3    
17    | Países               | /paises                        | 3    
18    | Provincias           | /provincias                    | 3    
19    | Localidades          | /localidades                   | 3    
20    | Tipos Domicilio      | /tipodoms                      | 3    
21    | Tipos Teléfono       | /tipotels                      | 3    
22    | Comprobantes         | None                           | None 
23    | Domicilios           | /domicilios                    | 3    
24    | Teléfonos            | /telefonos                     | 3    
26    | Listado              | /comprobantes                  | 22   
27    | Facturas             | /comprobantes                  | 22   
28    | Cuenta Corriente     | /cuentacorriente               | None 
29    | Dashboard            | /                              | None 
31    | Tesorería            | None                           | None 
32    | Recibos              | /recibos                       | 31   
33    | Puntos de Venta      | /puntos-venta                  | 3
```

## Observations
- **Orphans Resolves:** 26_27 -> 22.
- **Paths Fixed:** 29 -> `/`.
