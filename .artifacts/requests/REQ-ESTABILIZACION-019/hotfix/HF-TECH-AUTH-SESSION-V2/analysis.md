# Analysis: HF-TECH-AUTH-SESSION-V2

## Problem
Persistent `GET /api/v1/auth/me 401 (Unauthorized)` errors in console during navigation, even when user appears logged in.

## Root Cause
The `httpClient` interceptor or `auth.ts` store logic attempts to fetch user details (`fetchUser`) aggressively, possibly before the token is set or after an expiry that isn't handled by a silent refresh.
Previous fix harmonized local storage keys, but didn't solve the *timing* or *check* before request.

## Solution
1. In `auth.ts`, check for token existence before calling `fetchUser`.
2. Ensure `httpClient` doesn't fire 401 alerts for background checks if possible, or handles them silently.
