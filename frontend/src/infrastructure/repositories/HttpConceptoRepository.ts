
import type { IConceptoRepository } from '../../domain/repositories/IConceptoRepository';
import type { Concepto } from '../../domain/entities/Concepto';
import { axiosClient } from '../api/axiosClient';

export class HttpConceptoRepository implements IConceptoRepository {
    private readonly baseUrl = '/conceptos/';

    async getAll(): Promise<Concepto[]> {
        const response = await axiosClient.get<Concepto[]>(this.baseUrl);
        return response.data;
    }

    async getById(id: number): Promise<Concepto | null> {
        try {
            const response = await axiosClient.get<Concepto>(`${this.baseUrl}${id}`);
            return response.data;
        } catch (error: any) {
            if (error.response?.status === 404) return null;
            throw error;
        }
    }

    async create(entity: Omit<Concepto, 'id'>): Promise<Concepto> {
        const response = await axiosClient.post<Concepto>(this.baseUrl, entity);
        return response.data;
    }

    async update(id: number, entity: Partial<Concepto>): Promise<Concepto> {
        const response = await axiosClient.patch<Concepto>(`${this.baseUrl}${id}`, entity);
        return response.data;
    }

    async delete(id: number): Promise<void> {
        await axiosClient.delete(`${this.baseUrl}${id}`);
    }
}
