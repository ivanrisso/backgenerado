import { ref } from 'vue';
import { HttpTipoImpuestoRepository } from '@infra/repositories/HttpTipoImpuestoRepository';

const repository = new HttpTipoImpuestoRepository();

export function useTiposImpuesto() {
    const tiposImpuesto = ref<any[]>([]);
    const loading = ref(false);

    const loadTiposImpuesto = async () => {
        loading.value = true;
        try {
            tiposImpuesto.value = await repository.getAll();
        } finally {
            loading.value = false;
        }
    };

    return { tiposImpuesto, loadTiposImpuesto, loading };
}
