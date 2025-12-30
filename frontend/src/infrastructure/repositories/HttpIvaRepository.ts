
import type { IIvaRepository } from '../../domain/repositories/IIvaRepository';
import type { Iva } from '../../domain/entities/Iva';
import { axiosClient } from '../api/axiosClient';

export class HttpIvaRepository implements IIvaRepository {
    private readonly baseUrl = '/ivas/';

    async getAll(): Promise<Iva[]> {
        const response = await axiosClient.get<Iva[]>(this.baseUrl);
        return response.data;
    }

    async getById(id: number): Promise<Iva | null> {
        try {
            const response = await axiosClient.get<Iva>(`${this.baseUrl}${id}`);
            return response.data;
        } catch (error: any) {
            if (error.response?.status === 404) return null;
            throw error;
        }
    }

    async create(entity: Omit<Iva, 'id'>): Promise<Iva> {
        const response = await axiosClient.post<Iva>(this.baseUrl, entity);
        return response.data;
    }

    async update(id: number, entity: Partial<Iva>): Promise<Iva> {
        const response = await axiosClient.patch<Iva>(`${this.baseUrl}${id}`, entity);
        return response.data;
    }

    async delete(id: number): Promise<void> {
        await axiosClient.delete(`${this.baseUrl}${id}`);
    }
}
