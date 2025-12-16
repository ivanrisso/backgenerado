import type { ITipoDomRepository } from '../../domain/repositories/ITipoDomRepository';
import type { TipoDom } from '../../domain/entities/TipoDom';
import { TipoDomMapper } from '../mappers/TipoDomMapper';
import { httpClient } from '../api/httpClient';

export class AxiosTipoDomRepository implements ITipoDomRepository {
    private readonly resource = '/tipodoms';

    async getAll(): Promise<TipoDom[]> {
        const response = await httpClient.get(this.resource);
        return response.data.map((dto: any) => TipoDomMapper.toDomain(dto));
    }

    async getById(id: number): Promise<TipoDom | null> {
        try {
            const response = await httpClient.get(`${this.resource}/${id}`);
            return TipoDomMapper.toDomain(response.data);
        } catch (error) {
            return null;
        }
    }

    async create(entity: TipoDom): Promise<void> {
        const dto = { nombre: entity.nombre };
        await httpClient.post(this.resource, dto);
    }

    async update(entity: TipoDom): Promise<void> {
        const dto = { nombre: entity.nombre };
        await httpClient.patch(`${this.resource}/${entity.id}`, dto);
    }

    async delete(id: number): Promise<void> {
        await httpClient.delete(`${this.resource}/${id}`);
    }
}
