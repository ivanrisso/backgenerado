import axios, { type AxiosInstance, type AxiosError } from 'axios';


// Define base URL
const BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

export const httpClient: AxiosInstance = axios.create({
    baseURL: BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true, // Critical for HTTPOnly Cookies
});

// Define callback types
let unauthorizedCallback: ((url: string | undefined) => void) | null = null;
let forbiddenCallback: ((url: string | undefined) => void) | null = null;

export const setAuthCallbacks = (callbacks: {
    onUnauthorized: (url: string | undefined) => void,
    onForbidden: (url: string | undefined) => void
}) => {
    unauthorizedCallback = callbacks.onUnauthorized;
    forbiddenCallback = callbacks.onForbidden;
};

// Response Interceptor: Global Error Handling
httpClient.interceptors.response.use(
    (response) => response,
    async (error: AxiosError) => {
        if (error.response) {
            const status = error.response.status;

            // 401 Unauthorized - Session expired or invalid
            if (status === 401) {
                if (unauthorizedCallback) {
                    unauthorizedCallback(error.config?.url);
                }
            }

            // 403 Forbidden - Access denied
            if (status === 403) {
                console.warn('Access Forbidden');
                if (forbiddenCallback) {
                    forbiddenCallback(error.config?.url);
                }
            }
        }
        return Promise.reject(error);
    }
);
