
import { ref } from 'vue';
import { getTiposTelUseCase, createTipoTelUseCase, updateTipoTelUseCase, deleteTipoTelUseCase } from '../../di';
import type { TipoTel } from '../../domain/entities/TipoTel';

export function useTiposTel() {
    const tiposTel = ref<TipoTel[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const loadTiposTel = async () => {
        loading.value = true;
        try {
            tiposTel.value = await getTiposTelUseCase.execute();
        } catch (e: any) {
            error.value = e.message;
        } finally {
            loading.value = false;
        }
    };

    const createTipoTel = async (entity: TipoTel) => {
        loading.value = true;
        try {
            await createTipoTelUseCase.execute(entity);
            await loadTiposTel();
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const updateTipoTel = async (entity: TipoTel) => {
        loading.value = true;
        try {
            await updateTipoTelUseCase.execute(entity);
            await loadTiposTel();
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const deleteTipoTel = async (id: number) => {
        loading.value = true;
        try {
            await deleteTipoTelUseCase.execute(id);
            await loadTiposTel();
        } catch (e: any) {
            error.value = e.message;
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
