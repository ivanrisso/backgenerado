import { httpClient } from '../api/httpClient';
import type { CondicionTributaria } from '@domain/entities/CondicionTributaria';
import type { ICondicionTributariaRepository } from '@domain/repositories/ICondicionTributariaRepository';

export class HttpCondicionTributariaRepository implements ICondicionTributariaRepository {
    private readonly resource = '/condiciones-tributarias/';

    async getAll(): Promise<CondicionTributaria[]> {
        const response = await httpClient.get<CondicionTributaria[]>(this.resource);
        return response.data;
    }

    async getById(id: number): Promise<CondicionTributaria | null> {
        const response = await httpClient.get<CondicionTributaria>(`${this.resource}${id}`);
        return response.data;
    }

    async create(data: Omit<CondicionTributaria, 'id'>): Promise<CondicionTributaria> {
        const response = await httpClient.post<CondicionTributaria>(this.resource, data);
        return response.data;
    }

    async update(id: number, data: Partial<CondicionTributaria>): Promise<CondicionTributaria> {
        const response = await httpClient.patch<CondicionTributaria>(`${this.resource}${id}`, data);
        return response.data;
    }

    async delete(id: number): Promise<void> {
        await httpClient.delete(`${this.resource}${id}`);
    }
}
