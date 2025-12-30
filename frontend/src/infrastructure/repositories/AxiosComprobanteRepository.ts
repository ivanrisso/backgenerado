import type { IComprobanteRepository } from '@domain/repositories/IComprobanteRepository';
import type { Comprobante } from '@domain/entities/Comprobante';
import { httpClient } from '../api/httpClient';
import { ComprobanteMapper } from '../mappers/ComprobanteMapper';

export class AxiosComprobanteRepository implements IComprobanteRepository {
    private readonly resource = '/comprobantes/';

    async getAll(): Promise<Comprobante[]> {
        const response = await httpClient.get(this.resource);
        return response.data.map(ComprobanteMapper.toDomain);
    }

    async getById(id: number): Promise<Comprobante | null> {
        try {
            const response = await httpClient.get(`${this.resource}${id}`);
            return ComprobanteMapper.toDomain(response.data);
        } catch (error: any) {
            if (error.response?.status === 404) {
                return null;
            }
            throw error;
        }
    }

    async save(comprobante: Comprobante): Promise<Comprobante> {
        const payload = ComprobanteMapper.toApi(comprobante);
        const response = await httpClient.post(this.resource, payload);
        return ComprobanteMapper.toDomain(response.data);
    }

    async update(comprobante: Comprobante): Promise<Comprobante> {
        const payload = ComprobanteMapper.toApi(comprobante);
        const response = await httpClient.put(`${this.resource}${comprobante.id}`, payload);
        return ComprobanteMapper.toDomain(response.data);
    }
}
