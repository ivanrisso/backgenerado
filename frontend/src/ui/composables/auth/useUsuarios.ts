import { ref } from 'vue';
import {
    getAllUsuariosUseCase,
    createUsuarioUseCase,
    updateUsuarioUseCase,
    getUsuarioByIdUseCase,
    deleteUsuarioUseCase
} from '../../../di';
import { Usuario } from '../../../domain/entities/Usuario';

export function useUsuarios() {
    const usuarios = ref<Usuario[]>([]);
    const currentUsuario = ref<Usuario | null>(null);
    const isLoading = ref(false);
    const error = ref<string | null>(null);

    const loadUsuarios = async () => {
        isLoading.value = true;
        error.value = null;
        try {
            usuarios.value = await getAllUsuariosUseCase.execute();
        } catch (e: any) {
            error.value = e.message || 'Error loading users';
        } finally {
            isLoading.value = false;
        }
    };

    const loadUsuarioById = async (id: number) => {
        isLoading.value = true;
        error.value = null;
        try {
            currentUsuario.value = await getUsuarioByIdUseCase.execute(id);
        } catch (e: any) {
            error.value = e.message || 'Error loading user';
        } finally {
            isLoading.value = false;
        }
    };

    const saveUsuario = async (usuario: Usuario) => {
        isLoading.value = true;
        error.value = null;
        try {
            if (usuario.id && usuario.id > 0) {
                await updateUsuarioUseCase.execute(usuario);
            } else {
                await createUsuarioUseCase.execute(usuario);
            }
        } catch (e: any) {
            error.value = e.message || 'Error saving user';
            throw e;
        } finally {
            isLoading.value = false;
        }
    };

    const deleteUsuario = async (id: number) => {
        isLoading.value = true;
        error.value = null;
        try {
            await deleteUsuarioUseCase.execute(id);
            await loadUsuarios();
        } catch (e: any) {
            error.value = e.message || 'Error deleting user';
            throw e;
        } finally {
            isLoading.value = false;
        }
    };

    return {
        usuarios,
        currentUsuario,
        isLoading,
        error,
        loadUsuarios,
        loadUsuarioById,
        saveUsuario,
        deleteUsuario
    };
}
