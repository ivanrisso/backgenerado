
import type { IOperadorRepository } from '../../domain/repositories/IOperadorRepository';
import type { Operador } from '../../domain/entities/Operador';
import { axiosClient } from '../api/axiosClient';

export class HttpOperadorRepository implements IOperadorRepository {
    private readonly baseUrl = '/operadors/';

    async getAll(): Promise<Operador[]> {
        const response = await axiosClient.get<Operador[]>(this.baseUrl);
        return response.data;
    }

    async getById(id: number): Promise<Operador | null> {
        try {
            const response = await axiosClient.get<Operador>(`${this.baseUrl}${id}`);
            return response.data;
        } catch (error: any) {
            if (error.response?.status === 404) return null;
            throw error;
        }
    }

    async create(operador: Omit<Operador, 'id'>): Promise<Operador> {
        const response = await axiosClient.post<Operador>(this.baseUrl, operador);
        return response.data;
    }

    async update(id: number, operador: Partial<Operador>): Promise<Operador> {
        const response = await axiosClient.patch<Operador>(`${this.baseUrl}${id}`, operador);
        return response.data;
    }

    async delete(id: number): Promise<void> {
        await axiosClient.delete(`${this.baseUrl}${id}`);
    }
}
