import { ref } from 'vue';
import {
    getPaisesUseCase,
    getProvinciasByPaisUseCase,
    getLocalidadesByProvinciaUseCase,
    createPaisUseCase,
    updatePaisUseCase,
    deletePaisUseCase,
    createProvinciaUseCase,
    updateProvinciaUseCase,
    deleteProvinciaUseCase,
    createLocalidadUseCase,
    updateLocalidadUseCase,
    deleteLocalidadUseCase,
    getLocalidadByIdUseCase,
    getProvinciaByIdUseCase
} from '../../di';
import type { Pais } from '../../domain/entities/Pais';
import type { Provincia } from '../../domain/entities/Provincia';
import type { Localidad } from '../../domain/entities/Localidad';

export function useUbicacion() {
    const paises = ref<Pais[]>([]);
    const provincias = ref<Provincia[]>([]);
    const localidades = ref<Localidad[]>([]);
    const isLoading = ref(false);
    const error = ref<string | null>(null);

    // State for selections
    const selectedPaisId = ref<number | null>(null);
    const selectedProvinciaId = ref<number | null>(null);

    const loadPaises = async () => {
        isLoading.value = true;
        try {
            paises.value = await getPaisesUseCase.execute();
            // If we have a selected pais, reload its provinces too
            if (selectedPaisId.value) {
                await loadProvincias(selectedPaisId.value);
            }
        } catch (e: any) {
            error.value = e.message || 'Error loading countries';
            console.error(e);
        } finally {
            isLoading.value = false;
        }
    };

    const loadProvincias = async (paisId: number) => {
        if (!paisId) {
            provincias.value = [];
            return;
        }
        isLoading.value = true;
        try {
            provincias.value = await getProvinciasByPaisUseCase.execute(paisId);
        } catch (e: any) {
            error.value = e.message || 'Error loading provinces';
            console.error(e);
        } finally {
            isLoading.value = false;
        }
    };

    const loadLocalidades = async (provinciaId: number) => {
        if (!provinciaId) {
            localidades.value = [];
            return;
        }
        isLoading.value = true;
        try {
            localidades.value = await getLocalidadesByProvinciaUseCase.execute(provinciaId);
        } catch (e: any) {
            error.value = e.message || 'Error loading localities';
            console.error(e);
        } finally {
            isLoading.value = false;
        }
    };

    const handlePaisChange = async (id: number) => {
        selectedPaisId.value = id;
        selectedProvinciaId.value = null; // Reset provincia
        localidades.value = []; // Clear localidades
        await loadProvincias(id);
    };

    const handleProvinciaChange = async (id: number) => {
        selectedProvinciaId.value = id;
        await loadLocalidades(id);
    };

    const createPais = async (entity: Pais) => {
        isLoading.value = true;
        try {
            await createPaisUseCase.execute(entity);
            await loadPaises();
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            isLoading.value = false;
        }
    };

    const updatePais = async (entity: Pais) => {
        isLoading.value = true;
        try {
            await updatePaisUseCase.execute(entity);
            await loadPaises();
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            isLoading.value = false;
        }
    };

    const deletePais = async (id: number) => {
        isLoading.value = true;
        try {
            await deletePaisUseCase.execute(id);
            await loadPaises();
        } catch (e: any) {
            if (e.response && e.response.status === 409) {
                error.value = "No se puede eliminar el País porque tiene Provincias o está referenciado en Domicilios.";
            } else {
                error.value = e.response?.data?.detail || e.message || "Error desconocido al eliminar";
            }
            throw e;
        } finally {
            isLoading.value = false;
        }
    };

    const createProvincia = async (entity: Provincia) => {
        isLoading.value = true;
        try {
            await createProvinciaUseCase.execute(entity);
            if (selectedPaisId.value) await loadProvincias(selectedPaisId.value);
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            isLoading.value = false;
        }
    };

    const updateProvincia = async (entity: Provincia) => {
        isLoading.value = true;
        try {
            await updateProvinciaUseCase.execute(entity);
            if (selectedPaisId.value) await loadProvincias(selectedPaisId.value);
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            isLoading.value = false;
        }
    };

    const deleteProvincia = async (id: number) => {
        isLoading.value = true;
        try {
            await deleteProvinciaUseCase.execute(id);
            if (selectedPaisId.value) await loadProvincias(selectedPaisId.value);
        } catch (e: any) {
            if (e.response && e.response.status === 409) {
                error.value = "No se puede eliminar la Provincia porque tiene Localidades o está referenciada en Domicilios.";
            } else {
                error.value = e.response?.data?.detail || e.message || "Error desconocido al eliminar";
            }
            throw e;
        } finally {
            isLoading.value = false;
        }
    };

    const createLocalidad = async (entity: Localidad) => {
        isLoading.value = true;
        try {
            await createLocalidadUseCase.execute(entity);
            if (selectedProvinciaId.value) await loadLocalidades(selectedProvinciaId.value);
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            isLoading.value = false;
        }
    };

    const updateLocalidad = async (entity: Localidad) => {
        isLoading.value = true;
        try {
            await updateLocalidadUseCase.execute(entity);
            if (selectedProvinciaId.value) await loadLocalidades(selectedProvinciaId.value);
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            isLoading.value = false;
        }
    };

    const deleteLocalidad = async (id: number) => {
        isLoading.value = true;
        try {
            await deleteLocalidadUseCase.execute(id);
            if (selectedProvinciaId.value) await loadLocalidades(selectedProvinciaId.value);
        } catch (e: any) {
            if (e.response && e.response.status === 409) {
                error.value = "No se puede eliminar la Localidad porque está referenciada en Domicilios.";
            } else {
                error.value = e.response?.data?.detail || e.message || "Error desconocido al eliminar";
            }
            throw e;
        } finally {
            isLoading.value = false;
        }
    };

    const getLocationDetails = async (localidadId: number) => {
        if (!localidadId) return null;
        isLoading.value = true;
        try {
            const localidad = await getLocalidadByIdUseCase.execute(localidadId);
            if (!localidad) return null;

            const provincia = await getProvinciaByIdUseCase.execute(localidad.provinciaId);
            if (!provincia) return null;

            return {
                paisId: provincia.paisId,
                provinciaId: provincia.id,
                localidadId: localidad.id
            };
        } catch (e: any) {
            console.error(e);
            return null;
        } finally {
            isLoading.value = false;
        }
    };

    return {
        paises,
        provincias,
        localidades,
        selectedPaisId,
        selectedProvinciaId,
        loading: isLoading,
        error,
        handlePaisChange,
        handleProvinciaChange,
        loadPaises,
        loadProvincias,
        loadLocalidades,
        getLocationDetails,
        createPais,
        updatePais,
        deletePais,
        createProvincia,
        updateProvincia,
        deleteProvincia,
        createLocalidad,
        updateLocalidad,
        deleteLocalidad
    };
}
