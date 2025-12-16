import { ref } from 'vue';
import { authUseCase } from '../../../di';
import { Usuario } from '../../../domain/entities/Usuario';

// Global state for Auth could be PINIA or a singleton reactive obj, 
// using simple composable state for now as requested (no Pinia specific reqs but Vue 3)
const currentUser = ref<Usuario | null>(null);
const isAuthenticated = ref(false);

export function useAuth() {
    const isLoading = ref(false);
    const error = ref<string | null>(null);

    const login = async (email: string, pass: string) => {
        isLoading.value = true;
        error.value = null;
        try {
            const success = await authUseCase.login(email, pass);
            if (success) {
                isAuthenticated.value = true;
                currentUser.value = await authUseCase.getCurrentUser();
            } else {
                error.value = 'Invalid Credentials';
            }
            return success;
        } catch (e: any) {
            error.value = e.message;
            return false;
        } finally {
            isLoading.value = false;
        }
    };

    const logout = () => {
        authUseCase.logout();
        currentUser.value = null;
        isAuthenticated.value = false;
        window.location.href = '/login';
    };

    const checkAuth = async () => {
        try {
            const user = await authUseCase.getCurrentUser();
            if (user) {
                currentUser.value = user;
                isAuthenticated.value = true;
                return true;
            }
            return false;
        } catch {
            return false;
        }
    };

    return {
        currentUser,
        isAuthenticated,
        isLoading,
        error,
        login,
        logout,
        checkAuth
    };
}
