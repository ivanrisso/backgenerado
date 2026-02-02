import { ref } from 'vue';
import type { Comprobante } from '@domain/entities/Comprobante';
import { AxiosComprobanteRepository } from '@infra/repositories/AxiosComprobanteRepository';
import { GetComprobantesUseCase } from '../application/GetComprobantesUseCase';

export function useComprobantes() {
    const comprobantes = ref<Comprobante[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    // Dependency Injection could be improved here, but for now direct instantiation
    const repository = new AxiosComprobanteRepository();
    const getComprobantesUseCase = new GetComprobantesUseCase(repository);

    const loadComprobantes = async () => {
        loading.value = true;
        error.value = null;
        try {
            comprobantes.value = await getComprobantesUseCase.execute();
        } catch (e: any) {
            error.value = e.message || 'Error al cargar comprobantes';
            console.error('Failed to load comprobantes:', e);
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
