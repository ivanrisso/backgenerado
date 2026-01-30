import { ref } from 'vue';
import { HttpCondicionTributariaRepository } from '@infra/repositories/HttpCondicionTributariaRepository';

const repository = new HttpCondicionTributariaRepository();

export function useCondicionesTributarias() {
    const condicionesTributarias = ref<any[]>([]);
    const loading = ref(false);

    const loadCondicionesTributarias = async () => {
        loading.value = true;
        try {
            condicionesTributarias.value = await repository.getAll();
        } finally {
            loading.value = false;
        }
    };

    return { condicionesTributarias, loadCondicionesTributarias, loading };
}
