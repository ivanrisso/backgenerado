import { ref } from 'vue';
import { AxiosTipoDocRepository } from '@infra/repositories/AxiosTipoDocRepository';
import type { TipoDoc } from '@domain/entities/TipoDoc';

// Singleton instance usually preferred, or DI
const repository = new AxiosTipoDocRepository();

export function useTiposDoc() {
    const tiposDoc = ref<TipoDoc[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const loadTiposDoc = async () => {
        loading.value = true;
        error.value = null;
        try {
            tiposDoc.value = await repository.getAll();
        } catch (e: any) {
            error.value = e.message || 'Error loading TipoDocs';
            console.error(e);
        } finally {
            loading.value = false;
        }
    };

    return { tiposDoc, loadTiposDoc, loading, error };
}
