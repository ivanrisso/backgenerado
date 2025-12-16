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
        await deleteTipoDomUseCase.execute(id);
        await fetchData();
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
        await deleteTipoTelUseCase.execute(id);
        await fetchData();
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
