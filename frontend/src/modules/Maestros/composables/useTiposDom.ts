
import { ref } from 'vue';
import type { TipoDom } from '@domain/entities/TipoDom';
import {
    getTiposDomUseCase,
    createTipoDomUseCase,
    updateTipoDomUseCase,
    deleteTipoDomUseCase
} from '@/di';

export function useTiposDom() {
    const tiposDom = ref<TipoDom[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const loadTiposDom = async () => {
        loading.value = true;
        error.value = null;
        try {
            tiposDom.value = await getTiposDomUseCase.execute();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al cargar tipos de domicilio';
            error.value = msg;
            console.error(e);
        } finally {
            loading.value = false;
        }
    };

    const createTipoDom = async (entity: Omit<TipoDom, 'id'>) => {
        loading.value = true;
        error.value = null;
        try {
            await createTipoDomUseCase.execute(entity);
            await loadTiposDom();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al crear tipo de domicilio';
            error.value = msg;
            console.error(e);
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const updateTipoDom = async (entity: TipoDom) => {
        loading.value = true;
        error.value = null;
        try {
            await updateTipoDomUseCase.execute(entity.id, entity);
            await loadTiposDom();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al actualizar tipo de domicilio';
            error.value = msg;
            console.error(e);
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const deleteTipoDom = async (id: number) => {
        loading.value = true;
        error.value = null;
        try {
            await deleteTipoDomUseCase.execute(id);
            await loadTiposDom();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al eliminar tipo de domicilio';
            error.value = msg;
            console.error(e);
            throw e;
        } finally {
            loading.value = false;
        }
    };

    return {
        tiposDom,
        loading,
        error,
        loadTiposDom,
        createTipoDom,
        updateTipoDom,
        deleteTipoDom
    };
}
