import { ref } from 'vue';
import { getArticulosUseCase, createArticuloUseCase, updateArticuloUseCase, deleteArticuloUseCase } from '../../di';
import type { Articulo } from '../../domain/entities/Articulo';

export function useArticulos() {
    const articulos = ref<Articulo[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const loadArticulos = async () => {
        loading.value = true;
        try {
            articulos.value = await getArticulosUseCase.execute();
        } catch (e: any) {
            error.value = e.message;
        } finally {
            loading.value = false;
        }
    };

    const createArticulo = async (entity: Articulo) => {
        loading.value = true;
        try {
            await createArticuloUseCase.execute(entity);
            await loadArticulos();
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const updateArticulo = async (entity: Articulo) => {
        loading.value = true;
        try {
            await updateArticuloUseCase.execute(articuloId(entity), entity);
            await loadArticulos();
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const deleteArticulo = async (id: number) => {
        loading.value = true;
        try {
            await deleteArticuloUseCase.execute(id);
            await loadArticulos();
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            loading.value = false;
        }
    };

    // Helper to get ID reliably
    const articuloId = (entity: any): number => {
        return entity.id;
    }

    return {
        articulos,
        loading,
        error,
        loadArticulos,
        createArticulo,
        updateArticulo,
        deleteArticulo
    };
}
