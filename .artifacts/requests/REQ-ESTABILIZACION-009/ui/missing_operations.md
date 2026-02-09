# Missing Operations

## Analysis
- **Facturacion**: No Update View for Invoices (`InvoiceCreateView` exists, but editing invoices is typically restricted by fiscal rules. Checking if `InvoiceModify` exists... Not found in file list).
- **Clientes**: `ClienteDeudorList` exists (Read Only).
- **Maestros**: Most masters use a consolidated `View + Form` pattern.

## Technical Gaps
None explicitly detected by static analysis. Runtime check required to verify Delete operations.
