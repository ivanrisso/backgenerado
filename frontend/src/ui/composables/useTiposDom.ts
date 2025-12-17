
import { ref } from 'vue';
import { getTiposDomUseCase, createTipoDomUseCase, updateTipoDomUseCase, deleteTipoDomUseCase } from '../../di';
import type { TipoDom } from '../../domain/entities/TipoDom';

export function useTiposDom() {
    const tiposDom = ref<TipoDom[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const loadTiposDom = async () => {
        loading.value = true;
        try {
            tiposDom.value = await getTiposDomUseCase.execute();
        } catch (e: any) {
            error.value = e.message;
        } finally {
            loading.value = false;
        }
    };

    const createTipoDom = async (entity: TipoDom) => {
        loading.value = true;
        try {
            await createTipoDomUseCase.execute(entity);
            await loadTiposDom();
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const updateTipoDom = async (entity: TipoDom) => {
        loading.value = true;
        try {
            await updateTipoDomUseCase.execute(entity);
            await loadTiposDom();
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const deleteTipoDom = async (id: number) => {
        loading.value = true;
        try {
            await deleteTipoDomUseCase.execute(id);
            await loadTiposDom();
        } catch (e: any) {
            error.value = e.message;
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
