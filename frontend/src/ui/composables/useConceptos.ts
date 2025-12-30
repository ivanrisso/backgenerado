
import { ref } from 'vue';
import { getConceptosUseCase, createConceptoUseCase, updateConceptoUseCase, deleteConceptoUseCase } from '../../di';
import type { Concepto } from '../../domain/entities/Concepto';

export function useConceptos() {
    const conceptos = ref<Concepto[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const loadConceptos = async () => {
        loading.value = true;
        try {
            conceptos.value = await getConceptosUseCase.execute();
        } catch (e: any) {
            error.value = e.message;
        } finally {
            loading.value = false;
        }
    };

    const createConcepto = async (entity: Concepto) => {
        loading.value = true;
        try {
            await createConceptoUseCase.execute(entity);
            await loadConceptos();
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const updateConcepto = async (entity: Concepto) => {
        loading.value = true;
        try {
            await updateConceptoUseCase.execute(entity.id, entity);
            await loadConceptos();
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const deleteConcepto = async (id: number) => {
        loading.value = true;
        try {
            await deleteConceptoUseCase.execute(id);
            await loadConceptos();
        } catch (e: any) {
            if (e.response && e.response.status === 409) {
                error.value = "No se puede eliminar el Concepto porque está referenciado en Comprobantes.";
            } else {
                error.value = e.response?.data?.detail || e.message || "Error desconocido al eliminar";
            }
            throw e;
        } finally {
            loading.value = false;
        }
    };

    return {
        conceptos,
        loading,
        error,
        loadConceptos,
        createConcepto,
        updateConcepto,
        deleteConcepto
    };
}
