
import axios from 'axios';
import type { AxiosInstance, InternalAxiosRequestConfig, AxiosError } from 'axios';

// Define base URL - can be from environment variables
const BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

export const axiosClient: AxiosInstance = axios.create({
    baseURL: BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true, // Enable sending cookies
});

// Request Interceptor: No longer needed for Token Injection (Cookies used)
// Keeping it clean or removing completely. Let's remove the token injection logic.
axiosClient.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response Interceptor: Error Handling and 401 Redirect
axiosClient.interceptors.response.use(
    (response) => response,
    (error: AxiosError) => {
        if (error.response) {
            if (error.response.status === 401) {
                console.warn(`Unauthorized access at ${error.config?.url}. Redirecting to login...`);
                localStorage.removeItem('isLoggedIn'); // Clear session flag
                // Use window.location to force full reload or router if available
                if (window.location.pathname !== '/login') {
                    window.location.href = '/login';
                }
            }
        }
        return Promise.reject(error);
    }
);
