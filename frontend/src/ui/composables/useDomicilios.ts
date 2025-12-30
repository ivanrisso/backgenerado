
import { ref } from 'vue';
import {
    getDomiciliosUseCase,
    createDomicilioUseCase,
    updateDomicilioUseCase,
    deleteDomicilioUseCase,
    getDomicilioByIdUseCase
} from '../../di';
import type { Domicilio } from '../../domain/entities/Domicilio';

export function useDomicilios() {
    const domicilios = ref<Domicilio[]>([]);
    const loading = ref(false); // Renamed from isLoading
    const error = ref<string | null>(null);

    const loadDomicilios = async () => {
        loading.value = true;
        error.value = null;
        try {
            domicilios.value = await getDomiciliosUseCase.execute();
        } catch (e: any) {
            error.value = e.message || 'Error loading domicilios';
        } finally {
            loading.value = false;
        }
    };

    const createDomicilio = async (domicilio: Domicilio) => {
        loading.value = true;
        error.value = null;
        try {
            // Removing ID if needed, though UseCase often handles it or ignores it
            const { id, ...rest } = domicilio;
            await createDomicilioUseCase.execute(rest as any);
            await loadDomicilios();
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const updateDomicilio = async (domicilio: Domicilio) => {
        loading.value = true;
        error.value = null;
        try {
            const { id, ...rest } = domicilio;
            await updateDomicilioUseCase.execute(id, rest);
            await loadDomicilios();
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const deleteDomicilio = async (id: number) => {
        loading.value = true;
        error.value = null;
        try {
            await deleteDomicilioUseCase.execute(id);
            await loadDomicilios();
        } catch (e: any) {
            error.value = e.message || 'Error deleting domicilio';
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const currentDomicilio = ref<Domicilio | null>(null);

    const loadDomicilioById = async (id: number) => {
        loading.value = true;
        error.value = null;
        try {
            currentDomicilio.value = await getDomicilioByIdUseCase.execute(id);
        } catch (e: any) {
            error.value = e.message || 'Error loading domicilio';
        } finally {
            loading.value = false;
        }
    };

    return {
        domicilios,
        currentDomicilio, // Exported
        loading,
        error,
        loadDomicilios,
        loadDomicilioById, // Exported
        createDomicilio,
        updateDomicilio,
        deleteDomicilio
    };
}
