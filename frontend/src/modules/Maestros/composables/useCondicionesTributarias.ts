
import { ref } from 'vue';
import type { CondicionTributaria } from '@domain/entities/CondicionTributaria';
import {
    getCondicionesTributariasUseCase,
    createCondicionTributariaUseCase,
    updateCondicionTributariaUseCase,
    deleteCondicionTributariaUseCase
} from '@/di';

export function useCondicionesTributarias() {
    const condicionesTributarias = ref<CondicionTributaria[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const loadCondicionesTributarias = async () => {
        loading.value = true;
        error.value = null;
        try {
            condicionesTributarias.value = await getCondicionesTributariasUseCase.execute();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al cargar condiciones tributarias';
            error.value = msg;
            console.error(e);
        } finally {
            loading.value = false;
        }
    };

    const createCondicionTributaria = async (entity: Omit<CondicionTributaria, 'id'>) => {
        loading.value = true;
        error.value = null;
        try {
            await createCondicionTributariaUseCase.execute(entity);
            await loadCondicionesTributarias();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al crear condición tributaria';
            error.value = msg;
            console.error(e);
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const updateCondicionTributaria = async (entity: CondicionTributaria) => {
        loading.value = true;
        error.value = null;
        try {
            await updateCondicionTributariaUseCase.execute(entity.id, entity);
            await loadCondicionesTributarias();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al actualizar condición tributaria';
            error.value = msg;
            console.error(e);
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const deleteCondicionTributaria = async (id: number) => {
        loading.value = true;
        error.value = null;
        try {
            await deleteCondicionTributariaUseCase.execute(id);
            await loadCondicionesTributarias();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al eliminar condición tributaria';
            error.value = msg;
            console.error(e);
            throw e;
        } finally {
            loading.value = false;
        }
    };

    return {
        condicionesTributarias,
        loading,
        error,
        loadCondicionesTributarias,
        createCondicionTributaria,
        updateCondicionTributaria,
        deleteCondicionTributaria
    };
}
