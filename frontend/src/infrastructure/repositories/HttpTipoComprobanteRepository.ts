
import type { ITipoComprobanteRepository } from '../../domain/repositories/ITipoComprobanteRepository';
import type { TipoComprobante } from '../../domain/entities/TipoComprobante';
import { axiosClient } from '../api/axiosClient';

export class HttpTipoComprobanteRepository implements ITipoComprobanteRepository {
    private readonly baseUrl = '/tipocomprobantes/';

    async getAll(): Promise<TipoComprobante[]> {
        const response = await axiosClient.get<TipoComprobante[]>(this.baseUrl);
        return response.data;
    }

    async getById(id: number): Promise<TipoComprobante | null> {
        try {
            const response = await axiosClient.get<TipoComprobante>(`${this.baseUrl}${id}`);
            return response.data;
        } catch (error: any) {
            if (error.response?.status === 404) return null;
            throw error;
        }
    }

    async create(entity: Omit<TipoComprobante, 'id'>): Promise<TipoComprobante> {
        const response = await axiosClient.post<TipoComprobante>(this.baseUrl, entity);
        return response.data;
    }

    async update(id: number, entity: Partial<TipoComprobante>): Promise<TipoComprobante> {
        const response = await axiosClient.patch<TipoComprobante>(`${this.baseUrl}${id}`, entity);
        return response.data;
    }

    async delete(id: number): Promise<void> {
        await axiosClient.delete(`${this.baseUrl}${id}`);
    }
}
