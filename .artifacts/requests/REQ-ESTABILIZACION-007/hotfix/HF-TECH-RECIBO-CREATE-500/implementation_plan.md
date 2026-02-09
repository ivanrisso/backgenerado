# Implementation Plan - HF-TECH-RECIBO-CREATE-500

## Diagnosis
The error `Duplicate entry '999001' for key 'comprobante.numero'` confirms a schema verification failure.
The `Comprobante` model currently defines `numero` as globally unique:
```python
numero: Mapped[int] = mapped_column(nullable=False, unique=True)
```
This is incorrect for an invoicing system where numbering resets by `tipo_comprobante` and `punto_venta`.

## Solution (Backend)
1.  **Modify `app/infrastructure/db/orm_models.py`:**
    *   Remove `unique=True` from `numero`.
    *   Add `__table_args__` with `UniqueConstraint("tipo_comprobante_id", "punto_venta", "numero", name="uq_comprobante_numero")`.

2.  **Apply Schema Change:**
    *   Since we are in a hotfix workflow, we must ensure the DB is updated.
    *   We will attempt to generate an automated Alembic migration and apply it.
    *   If Alembic fails, we will provide a raw SQL fallback script for the user or attempt to execute it via python script.

## Verification
1.  Run reproduction script `reproduce_500.py`.
2.  Or simply verify via Browser manually (Create Recibo).
