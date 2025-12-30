
import { ref } from 'vue';
import { getComprobantesUseCase } from '../../di';
import type { Comprobante } from '../../domain/entities/Comprobante';

export function useComprobantes() {
    const comprobantes = ref<Comprobante[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const loadComprobantes = async () => {
        loading.value = true;
        error.value = null;
        try {
            comprobantes.value = await getComprobantesUseCase.execute();
        } catch (e: any) {
            error.value = e.message || 'Error al cargar comprobantes';
        } finally {
            loading.value = false;
        }
    };

    return {
        comprobantes,
        loading,
        error,
        loadComprobantes
    };
}
