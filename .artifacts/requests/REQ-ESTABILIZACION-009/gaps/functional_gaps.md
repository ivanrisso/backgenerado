# Functional Gaps

## GAP-FUNC-MENU-INCONSISTENCY (Resolved/Verified)
- Previously identified gap regarding sidebar visibility.
- **Status:** FIXED in Workflow 72. Verification V4 passed.

## GAP-FUNC-DASHBOARD-CONTENT
- **Descripción:** The "Dashboard" (`/`) currently wraps the router-view but the default child redirects to a list. There is no actual Dashboard KPI view.
- **Recomendación:** Implement a real Dashboard view (`DashboardView.vue`) instead of redirecting.
