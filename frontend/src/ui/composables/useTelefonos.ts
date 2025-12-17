
import { ref } from 'vue';
import { getTelefonosUseCase, createTelefonoUseCase, updateTelefonoUseCase, deleteTelefonoUseCase } from '../../di';
import type { Telefono } from '../../domain/entities/Telefono';

export function useTelefonos() {
    const telefonos = ref<Telefono[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const loadTelefonos = async () => {
        loading.value = true;
        try {
            telefonos.value = await getTelefonosUseCase.execute();
        } catch (e: any) {
            error.value = e.message;
        } finally {
            loading.value = false;
        }
    };

    const createTelefono = async (entity: Telefono) => {
        loading.value = true;
        try {
            await createTelefonoUseCase.execute(entity);
            await loadTelefonos();
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const updateTelefono = async (entity: Telefono) => {
        loading.value = true;
        try {
            const { id, ...rest } = entity;
            await updateTelefonoUseCase.execute(id, rest); // ID as first arg, partial entity as second
            await loadTelefonos();
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const deleteTelefono = async (id: number) => {
        loading.value = true;
        try {
            await deleteTelefonoUseCase.execute(id);
            await loadTelefonos();
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            loading.value = false;
        }
    };

    return {
        telefonos,
        loading,
        error,
        loadTelefonos,
        createTelefono,
        updateTelefono,
        deleteTelefono
    };
}
