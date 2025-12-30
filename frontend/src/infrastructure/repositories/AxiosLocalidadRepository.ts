import type { ILocalidadRepository } from '../../domain/repositories/ILocalidadRepository';
import type { Localidad } from '../../domain/entities/Localidad';
import { LocalidadMapper } from '../mappers/LocalidadMapper';
import { httpClient } from '../api/httpClient';

export class AxiosLocalidadRepository implements ILocalidadRepository {
    private readonly resource = '/localidades/';

    async getAll(): Promise<Localidad[]> {
        const response = await httpClient.get(this.resource);
        return response.data.map((dto: any) => LocalidadMapper.toDomain(dto));
    }

    async getById(id: number): Promise<Localidad | null> {
        try {
            const response = await httpClient.get(`${this.resource}${id}`);
            return LocalidadMapper.toDomain(response.data);
        } catch (error) {
            return null;
        }
    }

    async getAllByProvincia(provinciaId: number): Promise<Localidad[]> {
        const response = await httpClient.get(`${this.resource}?provincia_id=${provinciaId}`);
        return response.data.map((dto: any) => LocalidadMapper.toDomain(dto));
    }

    async create(entity: Localidad): Promise<void> {
        const dto = { localidad_nombre: entity.nombre, cod_postal: entity.codPostal, provincia_id: entity.provinciaId };
        await httpClient.post(this.resource, dto);
    }

    async update(entity: Localidad): Promise<void> {
        const dto = { localidad_nombre: entity.nombre, cod_postal: entity.codPostal, provincia_id: entity.provinciaId };
        await httpClient.patch(`${this.resource}${entity.id}`, dto);
    }

    async delete(id: number): Promise<void> {
        await httpClient.delete(`${this.resource}${id}`);
    }
}
