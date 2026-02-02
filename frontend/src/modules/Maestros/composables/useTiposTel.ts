
import { ref } from 'vue';
import type { TipoTel } from '@domain/entities/TipoTel';
import {
    getTiposTelUseCase,
    createTipoTelUseCase,
    updateTipoTelUseCase,
    deleteTipoTelUseCase
} from '@/di';

export function useTiposTel() {
    const tiposTel = ref<TipoTel[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const loadTiposTel = async () => {
        loading.value = true;
        error.value = null;
        try {
            tiposTel.value = await getTiposTelUseCase.execute();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al cargar tipos de teléfono';
            error.value = msg;
            console.error(e);
        } finally {
            loading.value = false;
        }
    };

    const createTipoTel = async (entity: Omit<TipoTel, 'id'>) => {
        loading.value = true;
        error.value = null;
        try {
            await createTipoTelUseCase.execute(entity);
            await loadTiposTel();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al crear tipo de teléfono';
            error.value = msg;
            console.error(e);
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const updateTipoTel = async (entity: TipoTel) => {
        loading.value = true;
        error.value = null;
        try {
            await updateTipoTelUseCase.execute(entity.id, entity);
            await loadTiposTel();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al actualizar tipo de teléfono';
            error.value = msg;
            console.error(e);
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const deleteTipoTel = async (id: number) => {
        loading.value = true;
        error.value = null;
        try {
            await deleteTipoTelUseCase.execute(id);
            await loadTiposTel();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al eliminar tipo de teléfono';
            error.value = msg;
            console.error(e);
            throw e;
        } finally {
            loading.value = false;
        }
    };

    return {
        tiposTel,
        loading,
        error,
        loadTiposTel,
        createTipoTel,
        updateTipoTel,
        deleteTipoTel
    };
}
