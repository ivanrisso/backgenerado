import type { IRolRepository } from '../../domain/repositories/IRolRepository';
import { Rol } from '../../domain/entities/Rol';
import { httpClient } from '../api/httpClient';
import { RolMapper } from '../mappers/RolMapper';
import type { RolDTO } from '../dtos/UsuarioDTO';

export class AxiosRolRepository implements IRolRepository {
    private readonly resource = '/rols';

    async getAll(): Promise<Rol[]> {
        const { data } = await httpClient.get<RolDTO[]>(this.resource);
        return data.map(RolMapper.toDomain);
    }

    async getById(id: number): Promise<Rol | null> {
        try {
            const { data } = await httpClient.get<RolDTO>(`${this.resource}/${id}`);
            return RolMapper.toDomain(data);
        } catch (e: any) {
            if (e.response && e.response.status === 404) return null;
            throw e;
        }
    }

    async create(rol: Rol): Promise<void> {
        await httpClient.post(this.resource, RolMapper.toDTO(rol));
    }

    async update(rol: Rol): Promise<void> {
        await httpClient.patch(`${this.resource}/${rol.id}`, RolMapper.toDTO(rol));
    }

    async delete(id: number): Promise<void> {
        await httpClient.delete(`${this.resource}/${id}`);
    }
}
