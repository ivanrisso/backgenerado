
import type { IDomicilioRepository } from '../../domain/repositories/IDomicilioRepository';
import type { Domicilio } from '../../domain/entities/Domicilio';
import { axiosClient } from '../api/axiosClient';

export class HttpDomicilioRepository implements IDomicilioRepository {
    private readonly baseUrl = '/domicilios';

    async getAll(): Promise<Domicilio[]> {
        const response = await axiosClient.get<Domicilio[]>(this.baseUrl);
        return response.data;
    }

    async getById(id: number): Promise<Domicilio | null> {
        try {
            const response = await axiosClient.get<Domicilio>(`${this.baseUrl}/${id}`);
            return response.data;
        } catch (error: any) {
            if (error.response?.status === 404) return null;
            throw error;
        }
    }

    async create(domicilio: Omit<Domicilio, 'id'>): Promise<Domicilio> {
        const response = await axiosClient.post<Domicilio>(this.baseUrl, domicilio);
        return response.data;
    }

    async update(id: number, domicilio: Partial<Domicilio>): Promise<Domicilio> {
        const response = await axiosClient.patch<Domicilio>(`${this.baseUrl}/${id}`, domicilio);
        return response.data;
    }

    async delete(id: number): Promise<void> {
        await axiosClient.delete(`${this.baseUrl}/${id}`);
    }
}
