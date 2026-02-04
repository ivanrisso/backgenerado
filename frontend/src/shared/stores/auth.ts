import { defineStore } from 'pinia';
import { httpClient } from '../http/client';

// LocalStorage Key
const AUTH_FLAG_KEY = 'auth_logged_in';

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

            // Check Local Flag before making ANY request
            const hasLocalFlag = localStorage.getItem(AUTH_FLAG_KEY) === 'true';

            if (!hasLocalFlag && !force) {
                this.user = null;
                this.roles = [];
                this.hydrationState = 'loaded'; // Considered "loaded" as Guest
                return;
            }

            this.hydrationState = 'loading';

            // Create the promise and cache it
            fetchPromise = (async () => {
                try {
                    // Ensure backend endpoint matches. Based on previous audit: GET /auth/me
                    const response = await httpClient.get<any>('/auth/me');
                    const data = response.data;

                    // MAPPING to Store Interface
                    this.user = {
                        id: data.id,
                        email: data.usuario_email
                    };

                    // Map Roles Objects to Strings
                    const rawRoles = data.roles || [];
                    this.roles = rawRoles.map((r: any) => r.rol_nombre?.toLowerCase() || r);
                    this.roles = this.roles.map(r => r.toLowerCase());

                    // Confirm Flag
                    localStorage.setItem(AUTH_FLAG_KEY, 'true');

                    this.hydrationState = 'loaded';
                } catch (error) {
                    this.user = null;
                    this.roles = [];
                    // Clear Flag on error (invalid session)
                    localStorage.removeItem(AUTH_FLAG_KEY);
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
            localStorage.setItem(AUTH_FLAG_KEY, 'true');
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
            localStorage.removeItem(AUTH_FLAG_KEY);
            this.hydrationState = 'idle';
        }
    }
});
