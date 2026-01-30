import { ref } from 'vue';
import { AxiosTipoDomRepository } from '@infra/repositories/AxiosTipoDomRepository';
// import type { TipoDom } from '@domain/entities/TipoDom'; // Assuming type exists

const repository = new AxiosTipoDomRepository();

export function useTiposDom() {
    const tiposDom = ref<any[]>([]); // Using any if Entity type uncertain, but preferably strict
    const loading = ref(false);

    const loadTiposDom = async () => {
        loading.value = true;
        try {
            const data = await repository.getAll();
            tiposDom.value = data;
        } finally {
            loading.value = false;
        }
    };

    return { tiposDom, loadTiposDom, loading };
}
