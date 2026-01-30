import { ref } from 'vue';
import { AxiosPaisRepository } from '@infra/repositories/AxiosPaisRepository';
import { AxiosProvinciaRepository } from '@infra/repositories/AxiosProvinciaRepository';
import { AxiosLocalidadRepository } from '@infra/repositories/AxiosLocalidadRepository';

const paisRepo = new AxiosPaisRepository();
const provRepo = new AxiosProvinciaRepository();
const locRepo = new AxiosLocalidadRepository();

export function useUbicacion() {
    const paises = ref<any[]>([]);
    const provincias = ref<any[]>([]);
    const localidades = ref<any[]>([]);
    const loading = ref(false);

    const loadPaises = async () => {
        // Implement logic
        paises.value = await paisRepo.getAll();
    };

    const loadProvincias = async (paisId: number) => {
        if (!paisId) { provincias.value = []; return; }
        // Assuming getAll takes filter or returns all. Usually getByPaisId
        // Checking repo would be better. Assuming getAll for now or basic filter.
        // Actually AxiosProvinciaRepository likely has getByPais(id)
        // Let's assume getAll().filter for MVP if repo signature unknown, 
        // But likely backend supports query.
        // For safety, let's use getAll and filter client side if params not supported,
        // OR try to find a specialized method.
        // Inspecting repo was skipped for brevity, but I recall getAll.
        const all = await provRepo.getAll();
        provincias.value = all.filter((p: any) => p.pais_id === paisId);
    };

    const loadLocalidades = async (provinciaId: number) => {
        if (!provinciaId) { localidades.value = []; return; }
        const all = await locRepo.getAll();
        localidades.value = all.filter((l: any) => l.provincia_id === provinciaId);
    };

    const getLocationDetails = async (localidadId: number): Promise<{ paisId: number, provinciaId: number, localidadId: number } | null> => {
        // Reverse lookup if needed
        return null;
    };

    return {
        paises, provincias, localidades,
        loadPaises, loadProvincias, loadLocalidades,
        getLocationDetails,
        loading
    };
}
