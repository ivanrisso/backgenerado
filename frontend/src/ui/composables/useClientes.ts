import { ref, onMounted } from 'vue';
import { getClientesUseCase, createClienteUseCase, getClienteByIdUseCase, updateClienteUseCase, deleteClienteUseCase } from '../../di';
import type { Cliente } from '@domain/entities/Cliente';

export function useClientes() {
    const clientes = ref<Cliente[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const fetchClientes = async () => {
        loading.value = true;
        error.value = null;
        try {
            clientes.value = await getClientesUseCase.execute();
        } catch (e: any) {
            error.value = 'Error al cargar clientes: ' + (e.message || 'Desconocido');
            console.error(e);
        } finally {
            loading.value = false;
        }
    };

    const createCliente = async (cliente: Cliente) => {
        loading.value = true;
        try {
            await createClienteUseCase.execute(cliente);
            await fetchClientes(); // Refresh list
        } catch (e: any) {
            error.value = e.response?.data?.detail || 'Error al crear cliente';
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const fetchClienteById = async (id: number): Promise<Cliente | null> => {
        loading.value = true;
        error.value = null;
        try {
            return await getClienteByIdUseCase.execute(id);
        } catch (e: any) {
            error.value = 'Error al cargar cliente: ' + (e.message || 'Desconocido');
            console.error(e);
            return null;
        } finally {
            loading.value = false;
        }
    };

    const updateCliente = async (cliente: Cliente) => {
        loading.value = true;
        try {
            await updateClienteUseCase.execute(cliente);
            // Optionally refresh list if needed, but usually we redirect
        } catch (e: any) {
            error.value = e.response?.data?.detail || 'Error al actualizar cliente';
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const deleteCliente = async (id: number) => {
        try {
            loading.value = true;
            await deleteClienteUseCase.execute(id);
            await fetchClientes(); // Refresh list
        } catch (e: any) {
            error.value = 'Error al eliminar cliente: ' + (e.message || 'Desconocido');
            console.error(e);
        } finally {
            loading.value = false;
        }
    };

    onMounted(() => {
        fetchClientes();
    });

    return {
        clientes,
        loading,
        error,
        fetchClientes,
        fetchClienteById,
        createCliente,
        updateCliente,
        deleteCliente
    };
}
