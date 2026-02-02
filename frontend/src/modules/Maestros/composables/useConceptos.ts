
import { ref } from 'vue';
import type { Concepto } from '@domain/entities/Concepto';
import {
    getConceptosUseCase,
    createConceptoUseCase,
    updateConceptoUseCase,
    deleteConceptoUseCase
} from '@/di';

export function useConceptos() {
    const conceptos = ref<Concepto[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const loadConceptos = async () => {
        loading.value = true;
        error.value = null;
        try {
            conceptos.value = await getConceptosUseCase.execute();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al cargar conceptos';
            error.value = msg;
            console.error(e);
        } finally {
            loading.value = false;
        }
    };

    const createConcepto = async (entity: Omit<Concepto, 'id'>) => {
        loading.value = true;
        error.value = null;
        try {
            await createConceptoUseCase.execute(entity);
            await loadConceptos();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al crear concepto';
            error.value = msg;
            console.error(e);
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const updateConcepto = async (entity: Concepto) => {
        loading.value = true;
        error.value = null;
        try {
            await updateConceptoUseCase.execute(entity.id, entity);
            await loadConceptos();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al actualizar concepto';
            error.value = msg;
            console.error(e);
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const deleteConcepto = async (id: number) => {
        loading.value = true;
        error.value = null;
        try {
            await deleteConceptoUseCase.execute(id);
            await loadConceptos();
        } catch (e: any) {
            const msg = e.response?.data?.detail || e.message || 'Error al eliminar concepto';
            error.value = msg;
            console.error(e);
            throw e;
        } finally {
            loading.value = false;
        }
    };

    return { conceptos, loading, error, loadConceptos, createConcepto, updateConcepto, deleteConcepto };
}
