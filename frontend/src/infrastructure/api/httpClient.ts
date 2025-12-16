import axios from 'axios';

const httpClient = axios.create({
    baseURL: import.meta.env.VITE_API_URL || '/api/v1',
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true // Importante: Permite enviar/recibir cookies (HttpOnly)
});

httpClient.interceptors.response.use(
    (response) => response,
    (error) => {
        // Si recibimos un 401 (Unauthorized), redirigimos al login
        if (error.response && error.response.status === 401) {
            // Evitar redirigir si ya estamos en el login para prevenir bucles
            if (!window.location.pathname.includes('/login')) {
                window.location.href = '/login';
            }
        }
        return Promise.reject(error);
    }
);

export { httpClient };
