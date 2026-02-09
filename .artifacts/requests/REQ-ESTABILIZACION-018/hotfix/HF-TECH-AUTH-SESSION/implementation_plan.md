# Implementation Plan - HF-TECH-AUTH-SESSION

## Goal Description
Fix session instability and inconsistent logout behavior caused by mismatched LocalStorage keys between the HTTP Client interceptor and the Auth Store.

## User Review Required
> [!NOTE]
> This fix ensures that any 401 error consistently clears the correct session flag (`auth_logged_in`), ensuring the application reacts correctly to session expiry (redirecting to login). It does not fix the root if the backend is rejecting valid cookies (which would require backend diagnosis), but it fixes the client-side state management handling of those rejections.

## Proposed Changes

### Frontend Infrastructure
#### [MODIFY] [axiosClient.ts](file:///home/irisso/proyectos/facturacion/frontend/src/infrastructure/api/axiosClient.ts)
- Update the response interceptor to clear `auth_logged_in` instead of `isLoggedIn` when a 401 occurs.
- This aligns with the `AUTH_FLAG_KEY` defined in `auth.ts`.

## Verification Plan

### Automated Tests
- N/A (Unit tests may not cover localStorage interactions in integration context).

### Manual Verification
1. Login to application.
2. Verify `auth_logged_in` exists in LocalStorage.
3. Simulate a 401 (e.g. modify cookie or wait for expiry, or mock response).
4. Verify `auth_logged_in` is removed.
5. Verify application redirects to Login (handled by Router Guard reacting to flag removal).
