
import { ref } from 'vue';
import type { Moneda } from '@domain/entities/Moneda';
import {
    getMonedasUseCase,
    createMonedaUseCase,
    updateMonedaUseCase,
    deleteMonedaUseCase
} from '@/di';

export function useMonedas() {
    const monedas = ref<Moneda[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const loadMonedas = async () => {
        loading.value = true;
        error.value = null;
        try {
            monedas.value = await getMonedasUseCase.execute();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al cargar monedas';
            error.value = msg;
            console.error(e);
        } finally {
            loading.value = false;
        }
    };

    const createMoneda = async (entity: Omit<Moneda, 'id'>) => {
        loading.value = true;
        error.value = null;
        try {
            await createMonedaUseCase.execute(entity);
            await loadMonedas(); // Refresh list
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al crear moneda';
            error.value = msg;
            console.error(e);
            throw e; // Propagate to view for handling
        } finally {
            loading.value = false;
        }
    };

    const updateMoneda = async (entity: Moneda) => {
        loading.value = true;
        error.value = null;
        try {
            await updateMonedaUseCase.execute(entity.id, entity);
            await loadMonedas(); // Refresh list
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al actualizar moneda';
            error.value = msg;
            console.error(e);
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const deleteMoneda = async (id: number) => {
        loading.value = true;
        error.value = null;
        try {
            await deleteMonedaUseCase.execute(id);
            await loadMonedas(); // Refresh list
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al eliminar moneda';
            error.value = msg;
            console.error(e);
            throw e;
        } finally {
            loading.value = false;
        }
    };

    return {
        monedas,
        loading,
        error,
        loadMonedas,
        createMoneda,
        updateMoneda,
        deleteMoneda
    };
}
