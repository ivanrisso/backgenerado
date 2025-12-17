
import { ref } from 'vue';
import { getTiposComprobanteUseCase, createTipoComprobanteUseCase, updateTipoComprobanteUseCase, deleteTipoComprobanteUseCase } from '../../di';
import type { TipoComprobante } from '../../domain/entities/TipoComprobante';

export function useTiposComprobante() {
    const tiposComprobante = ref<TipoComprobante[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const loadTiposComprobante = async () => {
        loading.value = true;
        try {
            tiposComprobante.value = await getTiposComprobanteUseCase.execute();
        } catch (e: any) {
            error.value = e.message;
        } finally {
            loading.value = false;
        }
    };

    const createTipoComprobante = async (entity: TipoComprobante) => {
        loading.value = true;
        try {
            await createTipoComprobanteUseCase.execute(entity);
            await loadTiposComprobante();
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const updateTipoComprobante = async (entity: TipoComprobante) => {
        loading.value = true;
        try {
            await updateTipoComprobanteUseCase.execute(entity.id, entity);
            await loadTiposComprobante();
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const deleteTipoComprobante = async (id: number) => {
        loading.value = true;
        try {
            await deleteTipoComprobanteUseCase.execute(id);
            await loadTiposComprobante();
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            loading.value = false;
        }
    };

    return {
        tiposComprobante,
        loading,
        error,
        loadTiposComprobante,
        createTipoComprobante,
        updateTipoComprobante,
        deleteTipoComprobante
    };
}
