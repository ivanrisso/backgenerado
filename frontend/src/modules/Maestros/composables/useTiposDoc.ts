
import { ref } from 'vue';
import type { TipoDoc } from '@domain/entities/TipoDoc';
import {
    getTiposDocUseCase,
    createTipoDocUseCase,
    updateTipoDocUseCase,
    deleteTipoDocUseCase
} from '@/di';

export function useTiposDoc() {
    const tiposDoc = ref<TipoDoc[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const loadTiposDoc = async () => {
        loading.value = true;
        error.value = null;
        try {
            tiposDoc.value = await getTiposDocUseCase.execute();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al cargar tipos de documento';
            error.value = msg;
            console.error(e);
        } finally {
            loading.value = false;
        }
    };

    const createTipoDoc = async (entity: Omit<TipoDoc, 'id'>) => {
        loading.value = true;
        error.value = null;
        try {
            await createTipoDocUseCase.execute(entity);
            await loadTiposDoc();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al crear tipo de documento';
            error.value = msg;
            console.error(e);
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const updateTipoDoc = async (entity: TipoDoc) => {
        loading.value = true;
        error.value = null;
        try {
            await updateTipoDocUseCase.execute(entity.id, entity);
            await loadTiposDoc();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al actualizar tipo de documento';
            error.value = msg;
            console.error(e);
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const deleteTipoDoc = async (id: number) => {
        loading.value = true;
        error.value = null;
        try {
            await deleteTipoDocUseCase.execute(id);
            await loadTiposDoc();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al eliminar tipo de documento';
            error.value = msg;
            console.error(e);
            throw e;
        } finally {
            loading.value = false;
        }
    };

    return {
        tiposDoc,
        loading,
        error,
        loadTiposDoc,
        createTipoDoc,
        updateTipoDoc,
        deleteTipoDoc
    };
}
