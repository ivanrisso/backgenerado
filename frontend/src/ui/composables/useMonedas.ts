
import { ref } from 'vue';
import { getMonedasUseCase, createMonedaUseCase, updateMonedaUseCase, deleteMonedaUseCase } from '../../di';
import type { Moneda } from '../../domain/entities/Moneda';

export function useMonedas() {
    const monedas = ref<Moneda[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const loadMonedas = async () => {
        loading.value = true;
        try {
            monedas.value = await getMonedasUseCase.execute();
        } catch (e: any) {
            error.value = e.message;
        } finally {
            loading.value = false;
        }
    };

    const createMoneda = async (entity: Moneda) => {
        loading.value = true;
        try {
            await createMonedaUseCase.execute(entity);
            await loadMonedas();
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const updateMoneda = async (entity: Moneda) => {
        loading.value = true;
        try {
            await updateMonedaUseCase.execute(entity.id, entity);
            await loadMonedas();
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const deleteMoneda = async (id: number) => {
        loading.value = true;
        try {
            await deleteMonedaUseCase.execute(id);
            await loadMonedas();
        } catch (e: any) {
            error.value = e.message;
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
