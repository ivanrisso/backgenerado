
import type { IMonedaRepository } from '../../domain/repositories/IMonedaRepository';
import type { Moneda } from '../../domain/entities/Moneda';
import { axiosClient } from '../api/axiosClient';

export class HttpMonedaRepository implements IMonedaRepository {
    private readonly baseUrl = '/monedas/';

    async getAll(): Promise<Moneda[]> {
        const response = await axiosClient.get<Moneda[]>(this.baseUrl);
        return response.data;
    }

    async getById(id: number): Promise<Moneda | null> {
        try {
            const response = await axiosClient.get<Moneda>(`${this.baseUrl}${id}`);
            return response.data;
        } catch (error: any) {
            if (error.response?.status === 404) return null;
            throw error;
        }
    }

    async create(entity: Omit<Moneda, 'id'>): Promise<Moneda> {
        const response = await axiosClient.post<Moneda>(this.baseUrl, entity);
        return response.data;
    }

    async update(id: number, entity: Partial<Moneda>): Promise<Moneda> {
        const response = await axiosClient.patch<Moneda>(`${this.baseUrl}${id}`, entity);
        return response.data;
    }

    async delete(id: number): Promise<void> {
        await axiosClient.delete(`${this.baseUrl}${id}`);
    }
}
