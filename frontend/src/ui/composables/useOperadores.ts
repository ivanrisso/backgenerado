
import { ref } from 'vue';
import { getOperadoresUseCase, createOperadorUseCase, updateOperadorUseCase, deleteOperadorUseCase } from '../../di';
import type { Operador } from '../../domain/entities/Operador';

export function useOperadores() {
    const operadores = ref<Operador[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const loadOperadores = async () => {
        loading.value = true;
        try {
            operadores.value = await getOperadoresUseCase.execute();
        } catch (e: any) {
            error.value = e.message;
        } finally {
            loading.value = false;
        }
    };

    const createOperador = async (entity: Operador) => {
        loading.value = true;
        try {
            await createOperadorUseCase.execute(entity);
            await loadOperadores();
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const updateOperador = async (entity: Operador) => {
        loading.value = true;
        try {
            await updateOperadorUseCase.execute(entity.id, entity);
            await loadOperadores();
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            loading.value = false;
        }
    }

    const deleteOperador = async (id: number) => {
        loading.value = true;
        try {
            await deleteOperadorUseCase.execute(id);
            await loadOperadores();
        } catch (e: any) {
            error.value = e.message;
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
