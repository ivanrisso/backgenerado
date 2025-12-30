import { ref } from 'vue';
import type { CondicionTributaria } from '../../domain/entities/CondicionTributaria';
import {
    getCondicionesTributariasUseCase,
    createCondicionTributariaUseCase,
    updateCondicionTributariaUseCase,
    deleteCondicionTributariaUseCase
} from '../../di';

export function useCondicionesTributarias() {
    const condicionesTributarias = ref<CondicionTributaria[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    async function loadCondicionesTributarias() {
        loading.value = true;
        error.value = null;
        try {
            condicionesTributarias.value = await getCondicionesTributariasUseCase.execute();
        } catch (e: any) {
            error.value = e.message || 'Error al cargar condiciones tributarias';
            console.error('Error loading condiciones tributarias:', e);
        } finally {
            loading.value = false;
        }
    }

    async function createCondicionTributaria(data: Omit<CondicionTributaria, 'id'>) {
        loading.value = true;
        error.value = null;
        try {
            await createCondicionTributariaUseCase.execute(data);
            await loadCondicionesTributarias(); // Refresh list
        } catch (e: any) {
            error.value = e.message || 'Error al crear condición tributaria';
            console.error('Error creating condicion tributaria:', e);
            throw e;
        } finally {
            loading.value = false;
        }
    }

    async function updateCondicionTributaria(entity: CondicionTributaria) {
        loading.value = true;
        error.value = null;
        try {
            await updateCondicionTributariaUseCase.execute(entity);
            await loadCondicionesTributarias(); // Refresh list
        } catch (e: any) {
            error.value = e.message || 'Error al actualizar condición tributaria';
            console.error('Error updating condicion tributaria:', e);
            throw e;
        } finally {
            loading.value = false;
        }
    }

    async function deleteCondicionTributaria(id: number) {
        loading.value = true;
        error.value = null;
        try {
            await deleteCondicionTributariaUseCase.execute(id);
            await loadCondicionesTributarias(); // Refresh list
        } catch (e: any) {
            // Check for constraint violation (e.g. foreign key)
            if (e.response && e.response.status === 409) {
                error.value = 'No se puede eliminar la condición porque está asignada a uno o más clientes.';
            } else {
                error.value = e.message || 'Error al eliminar condición tributaria';
            }
            console.error('Error deleting condicion tributaria:', e);
            throw e;
        } finally {
            loading.value = false;
        }
    }

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

