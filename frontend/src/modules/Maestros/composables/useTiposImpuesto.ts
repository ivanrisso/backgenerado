
import { ref } from 'vue';
import type { TipoImpuesto } from '@domain/entities/TipoImpuesto';
import {
    getTiposImpuestoUseCase,
    createTipoImpuestoUseCase,
    updateTipoImpuestoUseCase,
    deleteTipoImpuestoUseCase
} from '@/di';

export function useTiposImpuesto() {
    const tiposImpuesto = ref<TipoImpuesto[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const loadTiposImpuesto = async () => {
        loading.value = true;
        error.value = null;
        try {
            tiposImpuesto.value = await getTiposImpuestoUseCase.execute();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al cargar tipos de impuesto';
            error.value = msg;
            console.error(e);
        } finally {
            loading.value = false;
        }
    };

    const createTipoImpuesto = async (entity: Omit<TipoImpuesto, 'id'>) => {
        loading.value = true;
        error.value = null;
        try {
            await createTipoImpuestoUseCase.execute(entity);
            await loadTiposImpuesto();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al crear tipo de impuesto';
            error.value = msg;
            console.error(e);
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const updateTipoImpuesto = async (entity: TipoImpuesto) => {
        loading.value = true;
        error.value = null;
        try {
            await updateTipoImpuestoUseCase.execute(entity.id, entity);
            await loadTiposImpuesto();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al actualizar tipo de impuesto';
            error.value = msg;
            console.error(e);
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const deleteTipoImpuesto = async (id: number) => {
        loading.value = true;
        error.value = null;
        try {
            await deleteTipoImpuestoUseCase.execute(id);
            await loadTiposImpuesto();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al eliminar tipo de impuesto';
            error.value = msg;
            console.error(e);
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
