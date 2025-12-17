import { ref } from 'vue';
import {
    getClientesUseCase,
    createClienteUseCase,
    updateClienteUseCase,
    getClienteByIdUseCase,
    deleteClienteUseCase
} from '../../di';
import type { Cliente } from '../../domain/entities/Cliente';

export function useClientes() {
    const clientes = ref<Cliente[]>([]);
    const currentCliente = ref<Cliente | null>(null);
    const isLoading = ref(false);
    const error = ref<string | null>(null);

    const loadClientes = async () => {
        isLoading.value = true;
        error.value = null;
        try {
            clientes.value = await getClientesUseCase.execute();
        } catch (e: any) {
            error.value = e.message || 'Error loading clientes';
        } finally {
            isLoading.value = false;
        }
    };

    const loadClienteById = async (id: number) => {
        isLoading.value = true;
        error.value = null;
        try {
            // Note: getClienteByIdUseCase might return Promise<Cliente | null>
            currentCliente.value = await getClienteByIdUseCase.execute(id);
        } catch (e: any) {
            error.value = e.message || 'Error loading cliente';
        } finally {
            isLoading.value = false;
        }
    };

    const saveCliente = async (cliente: Cliente) => {
        isLoading.value = true;
        error.value = null;
        try {
            if (cliente.id && cliente.id > 0) {
                await updateClienteUseCase.execute(cliente);
            } else {
                await createClienteUseCase.execute(cliente);
            }
        } catch (e: any) {
            error.value = e.message || 'Error saving cliente';
            throw e;
        } finally {
            isLoading.value = false;
        }
    };

    const deleteCliente = async (id: number) => {
        isLoading.value = true;
        error.value = null;
        try {
            await deleteClienteUseCase.execute(id);
            await loadClientes();
        } catch (e: any) {
            error.value = e.message || 'Error deleting cliente';
            throw e;
        } finally {
            isLoading.value = false;
        }
    };

    return {
        clientes,
        currentCliente,
        isLoading,
        error,
        loadClientes,
        loadClienteById,
        saveCliente,
        deleteCliente
    };
}
