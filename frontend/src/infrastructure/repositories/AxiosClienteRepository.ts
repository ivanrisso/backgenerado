import type { IClienteRepository } from '@domain/repositories/IClienteRepository';
import type { Cliente } from '@domain/entities/Cliente';
import { httpClient } from '../api/httpClient';
import { ClienteMapper } from '../mappers/ClienteMapper';

export class AxiosClienteRepository implements IClienteRepository {
    private readonly resource = '/clientes/';

    async getAll(): Promise<Cliente[]> {
        const response = await httpClient.get(this.resource);
        return response.data.map(ClienteMapper.toDomain);
    }

    async getById(id: number): Promise<Cliente | null> {
        try {
            console.log(`[AxiosClienteRepository] getById called with id: ${id} (type: ${typeof id})`);
            const response = await httpClient.get(`${this.resource}${id}`);
            return ClienteMapper.toDomain(response.data);
        } catch (error: any) {
            if (error.response?.status === 404) {
                return null;
            }
            throw error;
        }
    }

    async save(cliente: Cliente): Promise<Cliente> {
        const payload = ClienteMapper.toApi(cliente);
        const response = await httpClient.post(this.resource, payload);
        return ClienteMapper.toDomain(response.data);
    }

    async update(cliente: Cliente): Promise<Cliente> {
        const payload = ClienteMapper.toApi(cliente);
        const response = await httpClient.patch(`${this.resource}${cliente.id}`, payload);
        return ClienteMapper.toDomain(response.data);
    }

    async delete(id: number): Promise<void> {
        await httpClient.delete(`${this.resource}${id}`);
    }

    async getAfipTaxComparison(id: number): Promise<any> {
        const response = await httpClient.get(`${this.resource}${id}/sync-afip-taxes`);
        return response.data;
    }

    async syncAfipTaxes(id: number, afipIds: string[]): Promise<any> {
        const response = await httpClient.post(`${this.resource}${id}/sync-afip-taxes`, afipIds);
        return response.data;
    }

    async getDeudores(): Promise<Cliente[]> {
        const response = await httpClient.get(`${this.resource}deudores`);
        return response.data.map(ClienteMapper.toDomain);
    }
}

