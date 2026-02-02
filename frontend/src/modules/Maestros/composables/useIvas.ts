
import { ref } from 'vue';
import type { Iva } from '@domain/entities/Iva';
import {
    getIvasUseCase,
    createIvaUseCase,
    updateIvaUseCase,
    deleteIvaUseCase
} from '@/di';

export function useIvas() {
    const ivas = ref<Iva[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const loadIvas = async () => {
        loading.value = true;
        error.value = null;
        try {
            ivas.value = await getIvasUseCase.execute();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al cargar tasas IVA';
            error.value = msg;
            console.error(e);
        } finally {
            loading.value = false;
        }
    };

    const createIva = async (entity: Omit<Iva, 'id'>) => {
        loading.value = true;
        error.value = null;
        try {
            await createIvaUseCase.execute(entity);
            await loadIvas();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al crear tasa IVA';
            error.value = msg;
            console.error(e);
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const updateIva = async (entity: Iva) => {
        loading.value = true;
        error.value = null;
        try {
            await updateIvaUseCase.execute(entity.id, entity);
            await loadIvas();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al actualizar tasa IVA';
            error.value = msg;
            console.error(e);
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const deleteIva = async (id: number) => {
        loading.value = true;
        error.value = null;
        try {
            await deleteIvaUseCase.execute(id);
            await loadIvas();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al eliminar tasa IVA';
            error.value = msg;
            console.error(e);
            throw e;
        } finally {
            loading.value = false;
        }
    };

    return { ivas, loading, error, loadIvas, createIva, updateIva, deleteIva };
}
