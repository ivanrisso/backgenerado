import { ref, onMounted } from 'vue';
import {
    getTiposDomUseCase, createTipoDomUseCase, updateTipoDomUseCase, deleteTipoDomUseCase,
    getTiposTelUseCase, createTipoTelUseCase, updateTipoTelUseCase, deleteTipoTelUseCase
} from '../../di';
import type { TipoDom } from '../../domain/entities/TipoDom';
import type { TipoTel } from '../../domain/entities/TipoTel';

export function useTiposContacto() {
    const tiposDom = ref<TipoDom[]>([]);
    const tiposTel = ref<TipoTel[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const fetchData = async () => {
        loading.value = true;
        error.value = null;
        try {
            const [doms, tels] = await Promise.all([
                getTiposDomUseCase.execute(),
                getTiposTelUseCase.execute()
            ]);
            tiposDom.value = doms;
            tiposTel.value = tels;
        } catch (e) {
            error.value = 'Error al cargar tipos de contacto';
        } finally {
            loading.value = false;
        }
    };

    onMounted(() => {
        fetchData();
    });

    // Tipo Dom CRUD
    const createTipoDom = async (entity: TipoDom) => {
        await createTipoDomUseCase.execute(entity);
        await fetchData();
    };
    const updateTipoDom = async (entity: TipoDom) => {
        await updateTipoDomUseCase.execute(entity);
        await fetchData();
    };
    const deleteTipoDom = async (id: number) => {
        try {
            await deleteTipoDomUseCase.execute(id);
            await fetchData();
        } catch (e: any) {
            if (e.response && e.response.status === 409) {
                error.value = "No se puede eliminar el Tipo de Domicilio porque está referenciado en Domicilios de Clientes o Proveedores.";
            } else {
                error.value = e.response?.data?.detail || e.message || "Error desconocido al eliminar";
            }
            throw e;
        }
    };

    // Tipo Tel CRUD
    const createTipoTel = async (entity: TipoTel) => {
        await createTipoTelUseCase.execute(entity);
        await fetchData();
    };
    const updateTipoTel = async (entity: TipoTel) => {
        await updateTipoTelUseCase.execute(entity);
        await fetchData();
    };
    const deleteTipoTel = async (id: number) => {
        try {
            await deleteTipoTelUseCase.execute(id);
            await fetchData();
        } catch (e: any) {
            if (e.response && e.response.status === 409) {
                error.value = "No se puede eliminar el Tipo de Teléfono porque está referenciado en Teléfonos de Clientes o Proveedores.";
            } else {
                error.value = e.response?.data?.detail || e.message || "Error desconocido al eliminar";
            }
            throw e;
        }
    };

    return {
        tiposDom,
        tiposTel,
        loading,
        error,
        createTipoDom, updateTipoDom, deleteTipoDom,
        createTipoTel, updateTipoTel, deleteTipoTel
    };
}
