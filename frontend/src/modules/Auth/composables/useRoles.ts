import { ref } from 'vue';
import { AxiosRolRepository } from '@infra/repositories/AxiosRolRepository';
import type { Rol } from '@domain/entities/Rol';

const repository = new AxiosRolRepository();

export function useRoles() {
    const roles = ref<Rol[]>([]);
    const isLoading = ref(false);
    const error = ref<string | null>(null);

    const loadRoles = async () => {
        isLoading.value = true;
        error.value = null;
        try {
            roles.value = await repository.getAll();
        } catch (e: any) {
            error.value = e.message || 'Error cargando roles';
        } finally {
            isLoading.value = false;
        }
    };

    const saveRol = async (rol: Rol) => {
        isLoading.value = true;
        error.value = null;
        try {
            if (rol.id) {
                await repository.update(rol);
            } else {
                await repository.create(rol);
            }
        } catch (e: any) {
            error.value = e.message || 'Error guardando rol';
            throw e;
        } finally {
            isLoading.value = false;
        }
    };

    const deleteRol = async (id: number) => {
        isLoading.value = true;
        error.value = null;
        try {
            await repository.delete(id);
            // Optimistic update or reload? Reload is safer for consistency
            await loadRoles();
        } catch (e: any) {
            error.value = e.message || 'Error eliminando rol';
            throw e;
        } finally {
            isLoading.value = false;
        }
    };

    return {
        roles,
        isLoading,
        error,
        loadRoles,
        saveRol,
        deleteRol
    };
}
