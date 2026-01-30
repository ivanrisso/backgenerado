import { ref } from 'vue';
import { AxiosClienteRepository } from '@infra/repositories/AxiosClienteRepository';
import type { Cliente } from '@domain/entities/Cliente';

const repository = new AxiosClienteRepository();

export function useClientes() {
    const clientes = ref<Cliente[]>([]);
    const clientesDeudores = ref<any[]>([]); // Should be ClienteDeudor but reusing structure for now or defining type
    const loading = ref(false);

    const currentCliente = ref<Cliente | null>(null);
    const error = ref<string | null>(null);

    const loadClientes = async () => {
        loading.value = true;
        error.value = null;
        try {
            clientes.value = await repository.getAll();
        } catch (e: any) {
            error.value = e.message || 'Error loading clientes';
            throw e;
        } finally {
            loading.value = false;
        }
    };

    const loadClientesDeudores = async () => {
        loading.value = true;
        error.value = null;
        try {
            // calling equivalent of repository.getDeudores()
            clientesDeudores.value = await (repository as any).getDeudores();
        } catch (e: any) {
            error.value = e.message || 'Error loading deudores';
            throw e;
        } finally {
            loading.value = false;
        }
    }

    const loadClienteById = async (id: number) => {
        loading.value = true;
        error.value = null;
        try {
            currentCliente.value = await repository.getById(id);
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            loading.value = false;
        }
    }

    const saveCliente = async (cliente: Cliente) => {
        loading.value = true;
        error.value = null;
        try {
            if (cliente.id) {
                await repository.update(cliente);
            } else {
                await repository.save(cliente);
            }
        } catch (e: any) {
            error.value = e.message || 'Error saving cliente';
            throw e;
        } finally {
            loading.value = false;
        }
    }

    const deleteCliente = async (id: number) => {
        loading.value = true;
        error.value = null;
        try {
            await repository.delete(id);
            await loadClientes();
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            loading.value = false;
        }
    }

    const getAfipTaxComparison = async (id: number) => {
        return await repository.getAfipTaxComparison(id);
    };

    const syncAfipTaxes = async (id: number, afipIds: string[]) => {
        return await repository.syncAfipTaxes(id, afipIds);
    };

    return {
        clientes, clientesDeudores, currentCliente, loadClientes, loadClientesDeudores, loadClienteById,
        saveCliente, deleteCliente,
        loading, isLoading: loading, error,
        getAfipTaxComparison, syncAfipTaxes
    };
}
