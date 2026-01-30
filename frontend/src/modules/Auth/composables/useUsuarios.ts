import { ref } from 'vue';
import { AxiosUsuarioRepository } from '@infra/repositories/AxiosUsuarioRepository';
import type { Usuario } from '@domain/entities/Usuario';

const repository = new AxiosUsuarioRepository();

export function useUsuarios() {
    const usuarios = ref<Usuario[]>([]);
    const isLoading = ref(false);
    const error = ref<string | null>(null);

    const loadUsuarios = async () => {
        isLoading.value = true;
        error.value = null;
        try {
            usuarios.value = await repository.getAll();
        } catch (e: any) {
            error.value = e.message || 'Error cargando usuarios';
        } finally {
            isLoading.value = false;
        }
    };

    const saveUsuario = async (usuario: Usuario) => {
        isLoading.value = true;
        error.value = null;
        try {
            if (usuario.id) {
                await repository.update(usuario);
            } else {
                await repository.create(usuario);
            }
        } catch (e: any) {
            error.value = e.message || 'Error guardando usuario';
            throw e;
        } finally {
            isLoading.value = false;
        }
    };

    const deleteUsuario = async (id: number) => {
        isLoading.value = true;
        error.value = null;
        try {
            await repository.delete(id);
            await loadUsuarios();
        } catch (e: any) {
            error.value = e.message || 'Error eliminando usuario';
            throw e;
        } finally {
            isLoading.value = false;
        }
    };

    // Stub for assignRoles if used by view, even if not in repo wrapper fully
    const assignRoles = async (usuarioId: number, roleIds: number[]) => {
        isLoading.value = true;
        try {
            await repository.assignRoles(usuarioId, roleIds);
        } catch (e: any) {
            error.value = e.message || 'Error asignando roles';
            throw e;
        } finally {
            isLoading.value = false;
        }
    };

    return {
        usuarios,
        isLoading,
        error,
        loadUsuarios,
        saveUsuario,
        deleteUsuario,
        assignRoles
    };
}
