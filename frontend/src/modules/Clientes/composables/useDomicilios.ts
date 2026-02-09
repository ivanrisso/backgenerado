import { ref } from 'vue';
import { HttpDomicilioRepository } from '@infra/repositories/HttpDomicilioRepository';
import type { Domicilio } from '@domain/entities/Domicilio';

const repository = new HttpDomicilioRepository();

export function useDomicilios() {
    const domicilios = ref<Domicilio[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const loadDomicilios = async () => {
        loading.value = true;
        error.value = null;
        try {
            domicilios.value = await repository.getAll();
        } catch (e: any) {
            error.value = e.message || 'Error al cargar domicilios';
        } finally {
            loading.value = false;
        }
    };

    const createDomicilio = async (dom: Omit<Domicilio, 'id'>) => {
        loading.value = true;
        error.value = null;
        try {
            await repository.create(dom);
            // await loadDomicilios(); // Optimistic update or reload
        } catch (e: any) {
            error.value = e.message || 'Error al crear domicilio';
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const updateDomicilio = async (dom: Domicilio) => {
        loading.value = true;
        error.value = null;
        try {
            await repository.update(dom.id, dom);
        } catch (e: any) {
            error.value = e.message || 'Error al actualizar domicilio';
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const deleteDomicilio = async (id: number) => {
        loading.value = true;
        error.value = null;
        try {
            await repository.delete(id);
        } catch (e: any) {
            error.value = e.message || 'Error al eliminar domicilio';
            throw e;
        } finally {
            loading.value = false;
        }
    };

    return {
        domicilios, loadDomicilios,
        createDomicilio, updateDomicilio, deleteDomicilio,
        loading, error
    };
}
