# Server Errors

**Status:** WARNING
**Issues Found:** 1 (Recent)

## Recent Errors
1. **IntegrityError (Duplicate entry)**
   - **Timestamp:** (Inferred from log position)
   - **Error:** `(1062, "Duplicate entry '999001' for key 'comprobante.numero'")`
   - **Context:** Verification Script (HF-GAP-001)
   - **Impact:** Script failure. Application logic might not handle race conditions or duplicates gracefully in this flow.
