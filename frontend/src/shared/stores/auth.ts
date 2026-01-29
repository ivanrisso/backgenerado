import { defineStore } from 'pinia';
import { httpClient } from '../http/client';

// Define interfaces based on Backend Contracts
export interface Usuario {
    id: number;
    email: string;
    // Add other user fields as needed
}

export interface AuthState {
    user: Usuario | null;
    roles: string[];
    permissions: string[];
    hydrationState: 'idle' | 'loading' | 'loaded' | 'failed';
}

export interface AccessRequirement {
    roles?: string[];
    permissions?: string[];
    mode?: 'AND' | 'OR'; // Default OR if mixed
}

// Promise cache for deduplication
let fetchPromise: Promise<void> | null = null;

export const useAuthStore = defineStore('auth', {
    state: (): AuthState => ({
        user: null,
        roles: [], // backend returns roles/scopes
        permissions: [],
        hydrationState: 'idle'
    }),

    getters: {
        isAuthenticated: (state) => !!state.user,
        isLoading: (state) => state.hydrationState === 'loading',

        hasRole: (state) => (role: string) => {
            return state.roles.includes(role) || state.roles.includes('admin'); // Admin superuser override
        },

        hasPermission: (state) => (permission: string) => {
            return state.permissions.includes(permission) || state.roles.includes('admin');
        },

        canAccess: (state) => (requirements: string | string[] | AccessRequirement) => {
            if (state.roles.includes('admin')) return true;

            let req: AccessRequirement;

            // Normalize input
            if (typeof requirements === 'string') {
                req = { roles: [requirements] };
            } else if (Array.isArray(requirements)) {
                req = { roles: requirements };
            } else {
                req = requirements;
            }

            // Fallback logic:
            // 1. If permissions explicitly requested, check them.
            // 2. If roles explicitly requested, check them.
            // 3. Fallback: If permissions check fails (or not requested) but roles match, pass?
            //    No, the prompt says "fallback a roles si no existen [permisos]".
            //    Implementation: Check permissions if present. Check roles if present.
            //    Mode matches user intent.

            const hasPermissionsReq = req.permissions && req.permissions.length > 0;
            const hasRolesReq = req.roles && req.roles.length > 0;

            const permMatch = hasPermissionsReq
                ? req.permissions!.some(p => state.permissions.includes(p))
                : null; // null = not queried

            const roleMatch = hasRolesReq
                ? req.roles!.some(r => state.roles.includes(r))
                : null;

            if (permMatch === null && roleMatch === null) return true; // Empty requirement allowed

            const mode = req.mode || 'OR';

            if (mode === 'OR') {
                // OR: If either is true, pass. Treat null as false unless both null.
                return (permMatch === true) || (roleMatch === true);
            } else {
                // AND: All required (non-null) must be true.
                const p = permMatch !== false;
                const r = roleMatch !== false;
                return p && r;
            }
        }
    },

    actions: {
        async fetchUser(force = false) {
            // Deduplication: If a fetch is already in progress and we don't force, return it.
            if (fetchPromise && !force) {
                return fetchPromise;
            }

            if (this.hydrationState === 'loaded' && !force) return;

            this.hydrationState = 'loading';

            // Create the promise and cache it
            fetchPromise = (async () => {
                try {
                    // Ensure backend endpoint matches. Based on previous audit: GET /auth/me
                    const response = await httpClient.get<Usuario & { roles: string[] }>('/auth/me');

                    // MAPPING
                    this.user = response.data;

                    // Safe guard:
                    this.roles = (response.data as any).roles || [];

                    this.hydrationState = 'loaded';
                } catch (error) {
                    this.user = null;
                    this.roles = [];
                    this.hydrationState = 'loaded'; // Finished but failed (Guest)
                } finally {
                    fetchPromise = null; // Clear promise when done
                }
            })();

            return fetchPromise;
        },

        async login(credentials: any) {
            // Adjust payload to match backend schema (UsuarioLogin)
            await httpClient.post('/auth/login', credentials);
            await this.fetchUser(true);
        },

        async logout(callApi = true) {
            if (callApi) {
                try {
                    await httpClient.post('/auth/logout');
                } catch (e) {
                    console.error('Logout API failed', e);
                }
            }
            this.user = null;
            this.roles = [];
            this.hydrationState = 'idle';

            // Note: We don't force window.location.href = '/login' here anymore
            // because the Router Guard will detect (!isAuthenticated) and redirect to login
            // on the next navigation or immediately if we are on a protected route.
            // If we are in the interceptor context, the router might need a push.
            // However, to keep store pure, we leave redirection to the consumer or router.
            // But for safety in specific logout clicks, we might want to reload or use router.
            // Given the constraints, let's allow the caller to handle redirect or simple location reload if needed.
            // For now, removing the forced reload to avoid loops during auto-logout sequences.
            // window.location.href = '/login'; 

        }
    }
});
