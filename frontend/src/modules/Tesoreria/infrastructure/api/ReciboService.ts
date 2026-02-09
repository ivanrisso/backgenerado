import { httpClient } from '../../../../shared/http/client';
import type { ReciboCreate, ReciboResponse } from '../../domain/models/Recibo';

export class ReciboService {
    private static readonly BASE_PATH = '/recibos';

    static async create(data: ReciboCreate): Promise<ReciboResponse> {
        const response = await httpClient.post<ReciboResponse>(this.BASE_PATH, data);
        return response.data;
    }

    static async getAll(params?: any): Promise<ReciboResponse[]> {
        const response = await httpClient.get<ReciboResponse[]>(this.BASE_PATH, { params });
        return response.data;
    }

    static async getById(id: number): Promise<ReciboResponse> {
        const response = await httpClient.get<ReciboResponse>(`${this.BASE_PATH}/${id}`);
        return response.data;
    }

    static async delete(id: number): Promise<void> {
        await httpClient.delete(`${this.BASE_PATH}/${id}`);
    }

    static async update(id: number, data: Partial<ReciboResponse>): Promise<ReciboResponse> {
        const response = await httpClient.put<ReciboResponse>(`${this.BASE_PATH}/${id}`, data);
        return response.data;
    }
}
