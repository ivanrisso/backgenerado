import { ref } from 'vue';
import { AxiosTipoDocRepository } from '../../infrastructure/repositories/AxiosTipoDocRepository';
import type { TipoDoc } from '../../domain/entities/TipoDoc';

const repository = new AxiosTipoDocRepository();

export function useTipoDocs() {
    const tipoDocs = ref<TipoDoc[]>([]);
    const isLoading = ref(false);
    const error = ref<string | null>(null);

    const loadTipoDocs = async () => {
        isLoading.value = true;
        error.value = null;
        try {
            tipoDocs.value = await repository.getAll();
        } catch (e: any) {
            error.value = e.message || 'Error cargando tipos de documentos';
        } finally {
            isLoading.value = false;
        }
    };

    return {
        tipoDocs,
        isLoading,
        error,
        loadTipoDocs
    };
}
