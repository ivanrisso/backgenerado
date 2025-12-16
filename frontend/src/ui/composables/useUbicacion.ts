import { ref, onMounted } from 'vue';
import {
    getPaisesUseCase, createPaisUseCase, updatePaisUseCase, deletePaisUseCase,
    getProvinciasByPaisUseCase, createProvinciaUseCase, updateProvinciaUseCase, deleteProvinciaUseCase,
    getLocalidadesByProvinciaUseCase, createLocalidadUseCase, updateLocalidadUseCase, deleteLocalidadUseCase
} from '../../di';
import type { Pais } from '../../domain/entities/Pais';
import type { Provincia } from '../../domain/entities/Provincia';
import type { Localidad } from '../../domain/entities/Localidad';

export function useUbicacion() {
    const paises = ref<Pais[]>([]);
    const provincias = ref<Provincia[]>([]);
    const localidades = ref<Localidad[]>([]);

    // Selection state
    const selectedPaisId = ref<number | null>(null);
    const selectedProvinciaId = ref<number | null>(null);

    const loading = ref(false);
    const error = ref<string | null>(null);

    const fetchPaises = async () => {
        loading.value = true;
        try {
            paises.value = await getPaisesUseCase.execute();
        } catch (e) {
            error.value = 'Error al cargar países';
        } finally {
            loading.value = false;
        }
    };

    const fetchProvincias = async (paisId: number) => {
        if (!paisId) {
            provincias.value = [];
            return;
        }
        loading.value = true;
        try {
            provincias.value = await getProvinciasByPaisUseCase.execute(paisId);
        } catch (e) {
            error.value = 'Error al cargar provincias';
        } finally {
            loading.value = false;
        }
    };

    const fetchLocalidades = async (provinciaId: number) => {
        if (!provinciaId) {
            localidades.value = [];
            return;
        }
        loading.value = true;
        try {
            localidades.value = await getLocalidadesByProvinciaUseCase.execute(provinciaId);
        } catch (e) {
            error.value = 'Error al cargar localidades';
        } finally {
            loading.value = false;
        }
    };

    const handlePaisChange = (paisId: number) => {
        selectedPaisId.value = paisId;
        selectedProvinciaId.value = null; // Reset child
        localidades.value = []; // Reset grand-child
        fetchProvincias(paisId);
    };

    const handleProvinciaChange = (provinciaId: number) => {
        selectedProvinciaId.value = provinciaId;
        fetchLocalidades(provinciaId);
    };

    onMounted(() => {
        fetchPaises();
    });

    // Pais CRUD
    const createPais = async (entity: Pais) => {
        await createPaisUseCase.execute(entity);
        await fetchPaises();
    };
    const updatePais = async (entity: Pais) => {
        await updatePaisUseCase.execute(entity);
        await fetchPaises();
    };
    const deletePais = async (id: number) => {
        await deletePaisUseCase.execute(id);
        await fetchPaises();
    };

    // Provincia CRUD
    const createProvincia = async (entity: Provincia) => {
        await createProvinciaUseCase.execute(entity);
        if (selectedPaisId.value) await fetchProvincias(selectedPaisId.value);
    };
    const updateProvincia = async (entity: Provincia) => {
        await updateProvinciaUseCase.execute(entity);
        if (selectedPaisId.value) await fetchProvincias(selectedPaisId.value);
    };
    const deleteProvincia = async (id: number) => {
        await deleteProvinciaUseCase.execute(id);
        if (selectedPaisId.value) await fetchProvincias(selectedPaisId.value);
    };

    // Localidad CRUD
    const createLocalidad = async (entity: Localidad) => {
        await createLocalidadUseCase.execute(entity);
        if (selectedProvinciaId.value) await fetchLocalidades(selectedProvinciaId.value);
    };
    const updateLocalidad = async (entity: Localidad) => {
        await updateLocalidadUseCase.execute(entity);
        if (selectedProvinciaId.value) await fetchLocalidades(selectedProvinciaId.value);
    };
    const deleteLocalidad = async (id: number) => {
        await deleteLocalidadUseCase.execute(id);
        if (selectedProvinciaId.value) await fetchLocalidades(selectedProvinciaId.value);
    };

    return {
        paises,
        provincias,
        localidades,
        selectedPaisId,
        selectedProvinciaId,
        loading,
        error,
        handlePaisChange,
        handleProvinciaChange,
        fetchPaises, fetchProvincias, fetchLocalidades,
        createPais, updatePais, deletePais,
        createProvincia, updateProvincia, deleteProvincia,
        createLocalidad, updateLocalidad, deleteLocalidad
    };
}
