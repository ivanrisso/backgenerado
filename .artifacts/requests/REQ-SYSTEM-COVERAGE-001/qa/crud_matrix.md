# QA CRUD Verification Matrix

| Entidad | CREATE (POST) | READ (GET List) | UPDATE (PATCH/PUT) | DELETE (DELETE) | Status |
|---------|---------------|-----------------|--------------------|-----------------|--------|
| **Cliente** | ⚠️ Auth | ⚠️ Auth (401) | ⚠️ Auth | ⚠️ Auth | **Protected** |
| **Comprobante** | ⚠️ Auth | ⚠️ Auth (401) | ⚠️ Auth | ⚠️ Auth | **Protected** |
| **Cond. Tributaria**| ⚠️ Auth | ✅ 200 OK | ⚠️ Auth | ⚠️ Auth | **Verified Read** |
| **TipoImpuesto** | ⚠️ Auth | ⚠️ Auth (401) | ⚠️ Auth | ⚠️ Auth | **Protected** |
| **Usuario** | ⚠️ Auth | ✅ 200 OK | ⚠️ Auth | ⚠️ Auth | **Verified Read** |
| **Auth** | ✅ Login OK | ✅ Me (401) | N/A | N/A | **Partial** |
| **Recibo** | ✅ (Has Tests) | N/A | N/A | N/A | **Test Covered** |
| **M. Items** (Tablas) | ⚠️ Auth | ⚠️ Auth (401) | ⚠️ Auth | ⚠️ Auth | **Protected** |

## Legend
- ✅ **200 OK**: Verified Access (Smoke Test passed).
- ⚠️ **Auth (401)**: Endpoint exists and is protected. Requires valid JWT to test. Considered "Implemented but not Verified in Smoke".
- ❌ **500/Error**: Endpoint failed.
- ⬜ **Missing**: Endpoint not found.

## Summary
- **Critical Failure**: None observed (no 500s on public/accessible endpoints).
- **Core Access**: The Master Data fix for `CondicionTributaria` is verified working.
- **Coverage**: Full CRUD endpoints exist for 30+ entities.
- **Verification Gap**: Automated smoke tests are blocked by Auth on most endpoints. Recommendations for next iterate: implements Token acquisition in Audit script.
