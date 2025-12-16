import { ref, onMounted } from 'vue';
import { getTiposDocUseCase, createTipoDocUseCase, updateTipoDocUseCase, deleteTipoDocUseCase } from '../../di';
import type { TipoDoc } from '../../domain/entities/TipoDoc';

export function useTiposDoc() {
    const tiposDoc = ref<TipoDoc[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const fetchTiposDoc = async () => {
        loading.value = true;
        error.value = null;
        try {
            tiposDoc.value = await getTiposDocUseCase.execute();
        } catch (e) {
            error.value = 'Error al cargar tipos de documento';
            console.error(e);
        } finally {
            loading.value = false;
        }
    };

    onMounted(() => {
        fetchTiposDoc();
    });

    const createTipoDoc = async (entity: TipoDoc) => {
        try {
            await createTipoDocUseCase.execute(entity);
            await fetchTiposDoc();
        } catch (e) {
            error.value = 'Error al crear tipo de documento';
            throw e;
        }
    };

    const updateTipoDoc = async (entity: TipoDoc) => {
        try {
            await updateTipoDocUseCase.execute(entity);
            await fetchTiposDoc();
        } catch (e) {
            error.value = 'Error al actualizar tipo de documento';
            throw e;
        }
    };

    const deleteTipoDoc = async (id: number) => {
        try {
            await deleteTipoDocUseCase.execute(id);
            await fetchTiposDoc();
        } catch (e) {
            error.value = 'Error al eliminar tipo de documento';
            throw e;
        }
    };

    return {
        tiposDoc,
        loading,
        error,
        fetchTiposDoc,
        createTipoDoc,
        updateTipoDoc,
        deleteTipoDoc
    };
}
