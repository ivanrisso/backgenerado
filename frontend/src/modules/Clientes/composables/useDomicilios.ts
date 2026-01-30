import { ref } from 'vue';
import { HttpDomicilioRepository } from '@infra/repositories/HttpDomicilioRepository';
import type { Domicilio } from '@domain/entities/Domicilio';

const repository = new HttpDomicilioRepository();

export function useDomicilios() {
    const domicilios = ref<Domicilio[]>([]);
    const loading = ref(false);

    const loadDomicilios = async () => {
        loading.value = true;
        try {
            domicilios.value = await repository.getAll();
        } finally {
            loading.value = false;
        }
    };

    const createDomicilio = async (dom: Omit<Domicilio, 'id'>) => {
        await repository.create(dom);
        // await loadDomicilios(); // Optimistic update or reload
    };

    const updateDomicilio = async (dom: Domicilio) => {
        await repository.update(dom.id, dom);
    };

    const deleteDomicilio = async (id: number) => {
        await repository.delete(id);
    };

    return {
        domicilios, loadDomicilios,
        createDomicilio, updateDomicilio, deleteDomicilio,
        loading
    };
}
