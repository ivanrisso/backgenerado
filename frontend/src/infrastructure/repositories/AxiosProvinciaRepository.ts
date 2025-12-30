import type { IProvinciaRepository } from '../../domain/repositories/IProvinciaRepository';
import type { Provincia } from '../../domain/entities/Provincia';
import { ProvinciaMapper } from '../mappers/ProvinciaMapper';
import { httpClient } from '../api/httpClient';

export class AxiosProvinciaRepository implements IProvinciaRepository {
    private readonly resource = '/provincias/';

    async getAll(): Promise<Provincia[]> {
        const response = await httpClient.get(this.resource);
        return response.data.map((dto: any) => ProvinciaMapper.toDomain(dto));
    }

    async getById(id: number): Promise<Provincia | null> {
        try {
            const response = await httpClient.get(`${this.resource}${id}`);
            return ProvinciaMapper.toDomain(response.data);
        } catch (error) {
            return null;
        }
    }

    async getAllByPais(paisId: number): Promise<Provincia[]> {
        const response = await httpClient.get(`${this.resource}?pais_id=${paisId}`);
        return response.data.map((dto: any) => ProvinciaMapper.toDomain(dto));
    }

    async create(entity: Provincia): Promise<void> {
        const dto = { provincia_nombre: entity.nombre, pais_id: entity.paisId };
        await httpClient.post(this.resource, dto);
    }

    async update(entity: Provincia): Promise<void> {
        const dto = { provincia_nombre: entity.nombre, pais_id: entity.paisId };
        await httpClient.patch(`${this.resource}${entity.id}`, dto);
    }

    async delete(id: number): Promise<void> {
        await httpClient.delete(`${this.resource}${id}`);
    }
}
