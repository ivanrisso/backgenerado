
import { ref } from 'vue';
import { getIvasUseCase, createIvaUseCase, updateIvaUseCase, deleteIvaUseCase } from '../../di';
import type { Iva } from '../../domain/entities/Iva';

export function useIvas() {
    const ivas = ref<Iva[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const loadIvas = async () => {
        loading.value = true;
        try {
            ivas.value = await getIvasUseCase.execute();
        } catch (e: any) {
            error.value = e.message;
        } finally {
            loading.value = false;
        }
    };

    const createIva = async (entity: Iva) => {
        loading.value = true;
        try {
            await createIvaUseCase.execute(entity);
            await loadIvas();
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const updateIva = async (entity: Iva) => {
        loading.value = true;
        try {
            await updateIvaUseCase.execute(entity.id, entity);
            await loadIvas();
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const deleteIva = async (id: number) => {
        loading.value = true;
        try {
            await deleteIvaUseCase.execute(id);
            await loadIvas();
        } catch (e: any) {
            if (e.response && e.response.status === 409) {
                error.value = "No se puede eliminar el IVA porque está referenciado en otros registros (Clientes, Comprobantes o Productos).";
            } else {
                error.value = e.response?.data?.detail || e.message || "Error desconocido al eliminar";
            }
            throw e;
        } finally {
            loading.value = false;
        }
    };

    return {
        ivas,
        loading,
        error,
        loadIvas,
        createIva,
        updateIva,
        deleteIva
    };
}
