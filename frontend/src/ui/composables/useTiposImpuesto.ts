
import { ref } from 'vue';
import { getTiposImpuestoUseCase, createTipoImpuestoUseCase, updateTipoImpuestoUseCase, deleteTipoImpuestoUseCase } from '../../di';
import type { TipoImpuesto } from '../../domain/entities/TipoImpuesto';

export function useTiposImpuesto() {
    const tiposImpuesto = ref<TipoImpuesto[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const loadTiposImpuesto = async () => {
        loading.value = true;
        try {
            tiposImpuesto.value = await getTiposImpuestoUseCase.execute();
        } catch (e: any) {
            error.value = e.message;
        } finally {
            loading.value = false;
        }
    };

    const createTipoImpuesto = async (entity: TipoImpuesto) => {
        loading.value = true;
        try {
            await createTipoImpuestoUseCase.execute(entity);
            await loadTiposImpuesto();
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const updateTipoImpuesto = async (entity: TipoImpuesto) => {
        loading.value = true;
        try {
            await updateTipoImpuestoUseCase.execute(entity.id, entity);
            await loadTiposImpuesto();
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const deleteTipoImpuesto = async (id: number) => {
        loading.value = true;
        try {
            await deleteTipoImpuestoUseCase.execute(id);
            await loadTiposImpuesto();
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            loading.value = false;
        }
    };

    return {
        tiposImpuesto,
        loading,
        error,
        loadTiposImpuesto,
        createTipoImpuesto,
        updateTipoImpuesto,
        deleteTipoImpuesto
    };
}
