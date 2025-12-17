
import type { ITipoImpuestoRepository } from '../../domain/repositories/ITipoImpuestoRepository';
import type { TipoImpuesto } from '../../domain/entities/TipoImpuesto';
import { axiosClient } from '../api/axiosClient';

export class HttpTipoImpuestoRepository implements ITipoImpuestoRepository {
    private readonly baseUrl = '/tipoimpuestos';

    async getAll(): Promise<TipoImpuesto[]> {
        const response = await axiosClient.get<TipoImpuesto[]>(this.baseUrl);
        return response.data;
    }

    async getById(id: number): Promise<TipoImpuesto | null> {
        try {
            const response = await axiosClient.get<TipoImpuesto>(`${this.baseUrl}/${id}`);
            return response.data;
        } catch (error: any) {
            if (error.response?.status === 404) return null;
            throw error;
        }
    }

    async create(tipoImpuesto: Omit<TipoImpuesto, 'id'>): Promise<TipoImpuesto> {
        const response = await axiosClient.post<TipoImpuesto>(this.baseUrl, tipoImpuesto);
        return response.data;
    }

    async update(id: number, tipoImpuesto: Partial<TipoImpuesto>): Promise<TipoImpuesto> {
        const response = await axiosClient.patch<TipoImpuesto>(`${this.baseUrl}/${id}`, tipoImpuesto);
        return response.data;
    }

    async delete(id: number): Promise<void> {
        await axiosClient.delete(`${this.baseUrl}/${id}`);
    }
}
