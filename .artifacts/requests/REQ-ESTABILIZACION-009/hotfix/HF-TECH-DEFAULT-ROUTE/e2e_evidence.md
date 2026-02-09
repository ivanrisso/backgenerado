# E2E Evidence

## Test Scenario
1. Login with `newtester@gmail.com` (Role: Operador).
2. Observe post-login redirect.
3. Explicitly navigate to `/`.

## Results
- **Post-Login:** Automatically redirected to `/recibos`.
- **Root Navigation:** Redirected to `/recibos`.
- **Error State:** No 403 Forbidden observed.
- **Content:** Recibos table loaded successfully.

## Evidence
- Screenshot: `final_verification_default_route_1770251346772.png`
- Status: **PASS**
