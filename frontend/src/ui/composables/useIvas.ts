import { ref } from 'vue';
import { AxiosIvaRepository } from '../../infrastructure/repositories/AxiosIvaRepository';
import type { Iva } from '../../domain/entities/Iva';

const repository = new AxiosIvaRepository();

export function useIvas() {
    const ivas = ref<Iva[]>([]);
    const isLoading = ref(false);
    const error = ref<string | null>(null);

    const loadIvas = async () => {
        isLoading.value = true;
        error.value = null;
        try {
            ivas.value = await repository.getAll();
        } catch (e: any) {
            error.value = e.message || 'Error cargando condiciones de IVA';
        } finally {
            isLoading.value = false;
        }
    };

    return {
        ivas,
        isLoading,
        error,
        loadIvas
    };
}
