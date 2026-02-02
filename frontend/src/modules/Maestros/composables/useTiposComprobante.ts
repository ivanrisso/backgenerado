
import { ref } from 'vue';
import type { TipoComprobante } from '@domain/entities/TipoComprobante';
import {
    getTiposComprobanteUseCase,
    createTipoComprobanteUseCase,
    updateTipoComprobanteUseCase,
    deleteTipoComprobanteUseCase
} from '@/di';

export function useTiposComprobante() {
    const tiposComprobante = ref<TipoComprobante[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const loadTiposComprobante = async () => {
        loading.value = true;
        error.value = null;
        try {
            tiposComprobante.value = await getTiposComprobanteUseCase.execute();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al cargar tipos de comprobante';
            error.value = msg;
            console.error(e);
        } finally {
            loading.value = false;
        }
    };

    const createTipoComprobante = async (entity: Omit<TipoComprobante, 'id'>) => {
        loading.value = true;
        error.value = null;
        try {
            await createTipoComprobanteUseCase.execute(entity);
            await loadTiposComprobante();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al crear tipo de comprobante';
            error.value = msg;
            console.error(e);
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const updateTipoComprobante = async (entity: TipoComprobante) => {
        loading.value = true;
        error.value = null;
        try {
            await updateTipoComprobanteUseCase.execute(entity.id, entity);
            await loadTiposComprobante();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al actualizar tipo de comprobante';
            error.value = msg;
            console.error(e);
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const deleteTipoComprobante = async (id: number) => {
        loading.value = true;
        error.value = null;
        try {
            await deleteTipoComprobanteUseCase.execute(id);
            await loadTiposComprobante();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al eliminar tipo de comprobante';
            error.value = msg;
            console.error(e);
            throw e;
        } finally {
            loading.value = false;
        }
    };

    return {
        tiposComprobante, // Keep consistent naming
        loading,
        error,
        loadTiposComprobante,
        createTipoComprobante,
        updateTipoComprobante,
        deleteTipoComprobante
    };
}
