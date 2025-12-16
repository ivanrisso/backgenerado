import { ref } from 'vue';
import {
    getAllRolesUseCase,
    createRolUseCase,
    updateRolUseCase,
    deleteRolUseCase,
    getRolByIdUseCase
} from '../../../di';
import { Rol } from '../../../domain/entities/Rol';

export function useRoles() {
    const roles = ref<Rol[]>([]);
    const currentRol = ref<Rol | null>(null);
    const isLoading = ref(false);
    const error = ref<string | null>(null);

    const loadRoles = async () => {
        isLoading.value = true;
        error.value = null;
        try {
            roles.value = await getAllRolesUseCase.execute();
            console.log('Roles loaded:', roles.value);
        } catch (e: any) {
            console.error('Error loading roles:', e);
            error.value = e.message || 'Error loading roles';
        } finally {
            isLoading.value = false;
        }
    };

    const loadRolById = async (id: number) => {
        isLoading.value = true;
        try {
            currentRol.value = await getRolByIdUseCase.execute(id);
        } catch (e: any) {
            error.value = e.message;
        } finally {
            isLoading.value = false;
        }
    }

    const saveRol = async (rol: Rol) => {
        isLoading.value = true;
        error.value = null;
        try {
            if (rol.id && rol.id > 0) {
                await updateRolUseCase.execute(rol);
            } else {
                await createRolUseCase.execute(rol);
            }
        } catch (e: any) {
            error.value = e.message || 'Error saving role';
            throw e;
        } finally {
            isLoading.value = false;
        }
    };

    const deleteRol = async (id: number) => {
        isLoading.value = true;
        try {
            await deleteRolUseCase.execute(id);
            // Optimistic update or reload
            roles.value = roles.value.filter(r => r.id !== id);
        } catch (e: any) {
            error.value = e.message || 'Error deleting role';
        } finally {
            isLoading.value = false;
        }
    };

    return {
        roles,
        currentRol,
        isLoading,
        error,
        loadRoles,
        loadRolById,
        saveRol,
        deleteRol
    };
}
