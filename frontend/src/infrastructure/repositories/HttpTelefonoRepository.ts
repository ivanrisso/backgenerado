
import type { ITelefonoRepository } from '../../domain/repositories/ITelefonoRepository';
import type { Telefono } from '../../domain/entities/Telefono';
import { axiosClient } from '../api/axiosClient';

export class HttpTelefonoRepository implements ITelefonoRepository {
    private readonly baseUrl = '/telefonos';

    async getAll(): Promise<Telefono[]> {
        const response = await axiosClient.get<Telefono[]>(this.baseUrl);
        return response.data;
    }

    async getById(id: number): Promise<Telefono | null> {
        try {
            const response = await axiosClient.get<Telefono>(`${this.baseUrl}/${id}`);
            return response.data;
        } catch (error: any) {
            if (error.response?.status === 404) return null;
            throw error;
        }
    }

    async create(telefono: Omit<Telefono, 'id'>): Promise<Telefono> {
        const response = await axiosClient.post<Telefono>(this.baseUrl, telefono);
        return response.data;
    }

    async update(id: number, telefono: Partial<Telefono>): Promise<Telefono> {
        const response = await axiosClient.patch<Telefono>(`${this.baseUrl}/${id}`, telefono);
        return response.data;
    }

    async delete(id: number): Promise<void> {
        await axiosClient.delete(`${this.baseUrl}/${id}`);
    }
}
