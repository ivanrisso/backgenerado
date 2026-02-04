# HOTFIX-BE-002: Recibo Service Data Integrity

## Goal Description
Modify `ReciboService` to populate receipt data (Concepto, Type, etc.) correctly using the `Cliente` entity, resolving the current issue where placeholder data ("00000000", "Cliente") is used.

## User Review Required
> [!IMPORTANT]
> This change modifies the constructor of `ReciboService`. Any other instantiation points (besides `recibo_routes.py`) would break. I have verified `recibo_routes.py` is the only usage.

## Proposed Changes

### Backend

#### [MODIFY] [recibo_routes.py](file:///home/irisso/proyectos/facturacion/app/routes/recibo_routes.py)
 - Import `ClienteRepositoryImpl`.
 - Instantiate `cliente_repo`.
 - Pass `cliente_repo` to `ReciboService`.
 - Catch `ClienteNoEncontrado` and return 404.

#### [MODIFY] [recibo_service.py](file:///home/irisso/proyectos/facturacion/app/services/recibo_service.py)
 - Import `ClienteRepositoryInterface` and `ClienteNoEncontrado`.
 - Update `__init__` to accept `cliente_repo`.
 - In `create_recibo`:
   - Fetch client by ID.
   - Guard against missing client.
   - Populate `nombre_cliente`, `cuit_cliente`, `domicilio_cliente`, etc., from the returned `Cliente` entity.
   - Use `doc_nro` = `cliente.cuit` (Receipts usually use CUIT/DNI).

## Verification Plan

### Automated Verification
Create a script `repro_hotfix_be_002.py`:
1.  Initialize database connection.
2.  Instantiate `ReciboService` with all repositories.
3.  Attempt to create a receipt for an existing client.
4.  Assert `receipt.nombre_cliente` is not "Cliente".
5.  Attempt to create a receipt for a non-existing client.
6.  Assert `ClienteNoEncontrado` is raised.
