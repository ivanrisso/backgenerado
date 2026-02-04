import { ref } from 'vue';
import { puntoVentaApi, type PuntoVenta, type PuntoVentaCreate, type PuntoVentaUpdate } from '../api/puntoVentaApi';

export function usePuntosVenta() {
    const puntosVenta = ref<PuntoVenta[]>([]);
    const currentPuntoVenta = ref<PuntoVenta | null>(null);
    const isLoading = ref(false);
    const error = ref<string | null>(null);

    const loadPuntosVenta = async () => {
        isLoading.value = true;
        error.value = null;
        try {
            puntosVenta.value = await puntoVentaApi.getAll();
        } catch (e: any) {
            error.value = e.response?.data?.detail || e.message || 'Error cargando puntos de venta';
        } finally {
            isLoading.value = false;
        }
    };

    const loadPuntoVentaById = async (id: number) => {
        isLoading.value = true;
        error.value = null;
        try {
            currentPuntoVenta.value = await puntoVentaApi.getById(id);
        } catch (e: any) {
            error.value = e.response?.data?.detail || e.message || 'Error cargando punto de venta';
        } finally {
            isLoading.value = false;
        }
    };

    const createPuntoVenta = async (data: PuntoVentaCreate) => {
        isLoading.value = true;
        error.value = null;
        try {
            await puntoVentaApi.create(data);
            await loadPuntosVenta();
        } catch (e: any) {
            error.value = e.response?.data?.detail || e.message || 'Error creando punto de venta';
            throw e;
        } finally {
            isLoading.value = false;
        }
    };

    const updatePuntoVenta = async (id: number, data: PuntoVentaUpdate) => {
        isLoading.value = true;
        error.value = null;
        try {
            await puntoVentaApi.update(id, data);
            await loadPuntosVenta();
        } catch (e: any) {
            error.value = e.response?.data?.detail || e.message || 'Error actualizando punto de venta';
            throw e;
        } finally {
            isLoading.value = false;
        }
    };

    const deletePuntoVenta = async (id: number) => {
        isLoading.value = true;
        error.value = null;
        try {
            await puntoVentaApi.delete(id);
            await loadPuntosVenta();
        } catch (e: any) {
            error.value = e.response?.data?.detail || e.message || 'Error eliminando punto de venta';
            throw e;
        } finally {
            isLoading.value = false;
        }
    };

    return {
        puntosVenta,
        currentPuntoVenta,
        isLoading,
        error,
        loadPuntosVenta,
        loadPuntoVentaById,
        createPuntoVenta,
        updatePuntoVenta,
        deletePuntoVenta
    };
}
