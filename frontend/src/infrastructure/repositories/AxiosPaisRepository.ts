import type { IPaisRepository } from '../../domain/repositories/IPaisRepository';
import type { Pais } from '../../domain/entities/Pais';
import { PaisMapper } from '../mappers/PaisMapper';
import { httpClient } from '../api/httpClient';

export class AxiosPaisRepository implements IPaisRepository {
    private readonly resource = '/paiss';

    async getAll(): Promise<Pais[]> {
        const response = await httpClient.get(this.resource);
        return response.data.map((dto: any) => PaisMapper.toDomain(dto));
    }

    async getById(id: number): Promise<Pais | null> {
        try {
            const response = await httpClient.get(`${this.resource}/${id}`);
            return PaisMapper.toDomain(response.data);
        } catch (error) {
            return null;
        }
    }

    async create(entity: Pais): Promise<void> {
        const dto = { nombre: entity.nombre, codigo: entity.codigo.value };
        await httpClient.post(this.resource, dto);
    }

    async update(entity: Pais): Promise<void> {
        const dto = { nombre: entity.nombre, codigo: entity.codigo.value };
        await httpClient.patch(`${this.resource}/${entity.id}`, dto);
    }

    async delete(id: number): Promise<void> {
        await httpClient.delete(`${this.resource}/${id}`);
    }
}
