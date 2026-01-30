import { ref } from 'vue';
import { HttpTelefonoRepository } from '@infra/repositories/HttpTelefonoRepository';

const repository = new HttpTelefonoRepository();

export function useTelefonos() {
    const telefonos = ref<any[]>([]);
    const loading = ref(false);

    const loadTelefonos = async () => {
        loading.value = true;
        try {
            const data = await repository.getAll();
            // Assuming getAll returns array.
            // Check repo implementation if wrapped in {data: ...} but HttpTelefonoRepository likely follows Base pattern
            // HttpDomicilioRepository returned response.data directly.
            telefonos.value = data;
        } finally {
            loading.value = false;
        }
    };

    return { telefonos, loadTelefonos, loading };
}
