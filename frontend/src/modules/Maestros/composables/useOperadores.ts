
import { ref } from 'vue';
import type { Operador } from '@domain/entities/Operador';
import {
    getOperadoresUseCase,
    createOperadorUseCase,
    updateOperadorUseCase,
    deleteOperadorUseCase
} from '@/di';

export function useOperadores() {
    const operadores = ref<Operador[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const loadOperadores = async () => {
        loading.value = true;
        error.value = null;
        try {
            operadores.value = await getOperadoresUseCase.execute();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al cargar operadores';
            error.value = msg;
            console.error(e);
        } finally {
            loading.value = false;
        }
    };

    const createOperador = async (entity: Omit<Operador, 'id'>) => {
        loading.value = true;
        error.value = null;
        try {
            await createOperadorUseCase.execute(entity);
            await loadOperadores();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al crear operador';
            error.value = msg;
            console.error(e);
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const updateOperador = async (entity: Operador) => {
        loading.value = true;
        error.value = null;
        try {
            await updateOperadorUseCase.execute(entity.id, entity);
            await loadOperadores();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al actualizar operador';
            error.value = msg;
            console.error(e);
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const deleteOperador = async (id: number) => {
        loading.value = true;
        error.value = null;
        try {
            await deleteOperadorUseCase.execute(id);
            await loadOperadores();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al eliminar operador';
            error.value = msg;
            console.error(e);
            throw e;
        } finally {
            loading.value = false;
        }
    };

    return {
        operadores,
        loading,
        error,
        loadOperadores,
        createOperador,
        updateOperador,
        deleteOperador
    };
}
