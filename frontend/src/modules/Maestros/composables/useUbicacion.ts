import { ref } from 'vue';
import { AxiosPaisRepository } from '@infra/repositories/AxiosPaisRepository';
import { AxiosProvinciaRepository } from '@infra/repositories/AxiosProvinciaRepository';
import { AxiosLocalidadRepository } from '@infra/repositories/AxiosLocalidadRepository';

const paisRepo = new AxiosPaisRepository();
const provRepo = new AxiosProvinciaRepository();
const locRepo = new AxiosLocalidadRepository();

export function useUbicacion() {
    // State
    const paises = ref<any[]>([]);
    const provincias = ref<any[]>([]);
    const localidades = ref<any[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);
    const selectedPaisId = ref<number | null>(null);
    const selectedProvinciaId = ref<number | null>(null);

    // Loaders
    const loadPaises = async () => {
        try {
            loading.value = true;
            error.value = null;
            paises.value = await paisRepo.getAll();
        } catch (e: any) {
            console.error('Error loading paises:', e);
            error.value = "Error al cargar países.";
            paises.value = [];
        } finally {
            loading.value = false;
        }
    };

    const loadProvincias = async (paisId: number) => {
        try {
            loading.value = true;
            error.value = null;
            if (!paisId) { provincias.value = []; return; }
            const all = await provRepo.getAll();
            // Client-side filtering as per original pattern
            provincias.value = all.filter((p: any) => p.paisId === paisId);
        } catch (e: any) {
            console.error('Error loading provincias:', e);
            error.value = "Error al cargar provincias.";
            provincias.value = [];
        } finally {
            loading.value = false;
        }
    };

    const loadLocalidades = async (provinciaId: number) => {
        try {
            loading.value = true;
            error.value = null;
            if (!provinciaId) { localidades.value = []; return; }
            const all = await locRepo.getAll();
            localidades.value = all.filter((l: any) => l.provinciaId === provinciaId);
        } catch (e: any) {
            console.error('Error loading localidades:', e);
            error.value = "Error al cargar localidades.";
            localidades.value = [];
        } finally {
            loading.value = false;
        }
    };

    // Event Handlers
    const handlePaisChange = async (id: number) => {
        selectedPaisId.value = id;
        selectedProvinciaId.value = null;
        localidades.value = [];
        await loadProvincias(id);
    };

    const handleProvinciaChange = async (id: number) => {
        selectedProvinciaId.value = id;
        await loadLocalidades(id);
    };

    // CRUD Wrappers
    const createProvincia = async (prov: any) => {
        loading.value = true;
        try {
            await provRepo.create(prov);
            if (selectedPaisId.value) await loadProvincias(selectedPaisId.value);
        } catch (e: any) { error.value = "Error al crear provincia"; throw e; } finally { loading.value = false; }
    };

    const updateProvincia = async (prov: any) => {
        loading.value = true;
        try {
            await provRepo.update(prov);
            if (selectedPaisId.value) await loadProvincias(selectedPaisId.value);
        } catch (e: any) { error.value = "Error al actualizar provincia"; throw e; } finally { loading.value = false; }
    };

    const deleteProvincia = async (id: number) => {
        loading.value = true;
        try {
            await provRepo.delete(id);
            if (selectedPaisId.value) await loadProvincias(selectedPaisId.value);
        } catch (e: any) { error.value = "Error al borrar provincia"; throw e; } finally { loading.value = false; }
    };

    const createLocalidad = async (loc: any) => {
        loading.value = true;
        try {
            await locRepo.create(loc);
            if (selectedProvinciaId.value) await loadLocalidades(selectedProvinciaId.value);
        } catch (e: any) { error.value = "Error al crear localidad"; throw e; } finally { loading.value = false; }
    };

    const updateLocalidad = async (loc: any) => {
        loading.value = true;
        try {
            await locRepo.update(loc);
            if (selectedProvinciaId.value) await loadLocalidades(selectedProvinciaId.value);
        } catch (e: any) { error.value = "Error al actualizar localidad"; throw e; } finally { loading.value = false; }
    };

    const deleteLocalidad = async (id: number) => {
        loading.value = true;
        try {
            await locRepo.delete(id);
            if (selectedProvinciaId.value) await loadLocalidades(selectedProvinciaId.value);
        } catch (e: any) {
            const detail = e.response?.data?.detail || "";
            // Check for 409 Conflict, specific keywords, or 500 which often hides DB Integrity Errors
            if (e.response?.status === 409 || e.response?.status === 500 || detail.includes("foreign key") || detail.includes("constraint")) {
                error.value = "No se puede eliminar la localidad porque registra movimientos o está asociada a otras entidades (Clientes/Proveedores).";
            } else {
                error.value = detail || "Error al borrar localidad";
            }
            throw e;
        } finally { loading.value = false; }
    };

    const getLocationDetails = async (_localidadId: number): Promise<{ paisId: number, provinciaId: number, localidadId: number } | null> => {
        return null; // Implementation deferred
    };

    return {
        // State
        paises, provincias, localidades,
        selectedPaisId, selectedProvinciaId,
        loading, error,

        // Loaders
        loadPaises, loadProvincias, loadLocalidades,

        // Handlers
        handlePaisChange, handleProvinciaChange,

        // CRUD
        createProvincia, updateProvincia, deleteProvincia,
        createLocalidad, updateLocalidad, deleteLocalidad,

        getLocationDetails
    };
}
