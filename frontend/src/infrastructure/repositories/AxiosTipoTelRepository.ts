import type { ITipoTelRepository } from '../../domain/repositories/ITipoTelRepository';
import type { TipoTel } from '../../domain/entities/TipoTel';
import { TipoTelMapper } from '../mappers/TipoTelMapper';
import { httpClient } from '../api/httpClient';

export class AxiosTipoTelRepository implements ITipoTelRepository {
    private readonly resource = '/tipotels/';

    async getAll(): Promise<TipoTel[]> {
        const response = await httpClient.get(this.resource);
        return response.data.map((dto: any) => TipoTelMapper.toDomain(dto));
    }

    async getById(id: number): Promise<TipoTel | null> {
        try {
            const response = await httpClient.get(`${this.resource}${id}`);
            return TipoTelMapper.toDomain(response.data);
        } catch (error) {
            return null;
        }
    }

    async create(entity: TipoTel): Promise<void> {
        const dto = { nombre: entity.nombre };
        await httpClient.post(this.resource, dto);
    }

    async update(entity: TipoTel): Promise<void> {
        const dto = { nombre: entity.nombre };
        await httpClient.patch(`${this.resource}${entity.id}`, dto);
    }

    async delete(id: number): Promise<void> {
        await httpClient.delete(`${this.resource}${id}`);
    }
}
