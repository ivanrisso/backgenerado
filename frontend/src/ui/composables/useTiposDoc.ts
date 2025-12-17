
import { ref } from 'vue';
import { getTiposDocUseCase, createTipoDocUseCase, updateTipoDocUseCase, deleteTipoDocUseCase } from '../../di';
import type { TipoDoc } from '../../domain/entities/TipoDoc';

export function useTiposDoc() {
    const tiposDoc = ref<TipoDoc[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const loadTiposDoc = async () => {
        loading.value = true;
        try {
            tiposDoc.value = await getTiposDocUseCase.execute();
        } catch (e: any) {
            error.value = e.message;
        } finally {
            loading.value = false;
        }
    };

    const createTipoDoc = async (entity: TipoDoc) => {
        loading.value = true;
        try {
            await createTipoDocUseCase.execute(entity);
            await loadTiposDoc();
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const updateTipoDoc = async (entity: TipoDoc) => {
        loading.value = true;
        try {
            await updateTipoDocUseCase.execute(entity);
            await loadTiposDoc();
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const deleteTipoDoc = async (id: number) => {
        loading.value = true;
        try {
            await deleteTipoDocUseCase.execute(id);
            await loadTiposDoc();
        } catch (e: any) {
            error.value = e.message;
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
