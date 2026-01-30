import { ref } from 'vue';
import { AxiosTipoTelRepository } from '@infra/repositories/AxiosTipoTelRepository';

const repository = new AxiosTipoTelRepository();

export function useTiposTel() {
    const tiposTel = ref<any[]>([]);
    const loading = ref(false);

    const loadTiposTel = async () => {
        loading.value = true;
        try {
            tiposTel.value = await repository.getAll();
        } finally {
            loading.value = false;
        }
    };

    return { tiposTel, loadTiposTel, loading };
}
