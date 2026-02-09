import { ref } from 'vue';
import type { ReciboResponse } from '../domain/models/Recibo';
import { ReciboService } from '../infrastructure/api/ReciboService';

export function useRecibos() {
    const recibos = ref<ReciboResponse[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const loadRecibos = async (filters?: any) => {
        loading.value = true;
        error.value = null;
        try {
            recibos.value = await ReciboService.getAll(filters);
        } catch (e: any) {
            error.value = e.message || 'Error al cargar recibos';
            console.error('Failed to load recibos:', e);
        } finally {
            loading.value = false;
        }
    };

    return {
        recibos,
        loading,
        error,
        loadRecibos
    };
}
