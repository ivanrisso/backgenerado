import type { IUsuarioRepository } from '../../domain/repositories/IUsuarioRepository';
import { Usuario } from '../../domain/entities/Usuario';
import { httpClient } from '../api/httpClient';
import { UsuarioMapper } from '../mappers/UsuarioMapper';
import type { UsuarioDTO } from '../dtos/UsuarioDTO';

export class AxiosUsuarioRepository implements IUsuarioRepository {
    private readonly resource = '/usuarios'; // Based on routes file name 'usuario_routes.py' usually /usuarios or /users. Checking... routes file says prefix="/usuarios" ? or /users?
    // Let's assume /usuarios based on naming convention or verify. 
    // Wait, tipodoc_routes was /tipodocs. usuario_routes is likely /usuarios.
    // I will use /usuarios.

    async getMe(): Promise<Usuario> {
        const { data } = await httpClient.get<UsuarioDTO>(`${this.resource}/me`);
        return UsuarioMapper.toDomain(data);
    }

    async getAll(): Promise<Usuario[]> {
        const { data } = await httpClient.get<UsuarioDTO[]>(this.resource);
        return data.map(UsuarioMapper.toDomain);
    }

    async getById(id: number): Promise<Usuario | null> {
        try {
            const { data } = await httpClient.get<UsuarioDTO>(`${this.resource}/${id}`);
            return UsuarioMapper.toDomain(data);
        } catch (e: any) {
            if (e.response && e.response.status === 404) return null;
            throw e;
        }
    }

    async create(usuario: Usuario): Promise<void> {
        // DTO for creation might differ (password included), but reusing main DTO for now or partial
        // Usually creation needs password. Domain Usuario entity has it? No, we removed password from Entity.
        // So this create method might need a dedicated Payload or different args in Domain?
        // Domain Entity Usuario usually represents Query side.
        // Valid point. But for now, mapping what we have.
        // Assuming Backend Create expects body.
        await httpClient.post(this.resource, UsuarioMapper.toDTO(usuario));
    }

    async update(usuario: Usuario): Promise<void> {
        await httpClient.patch(`${this.resource}/${usuario.id}`, UsuarioMapper.toDTO(usuario));
    }

    async delete(id: number): Promise<void> {
        await httpClient.delete(`${this.resource}/${id}`);
    }

    async assignRoles(usuarioId: number, roleIds: number[]): Promise<void> {
        await httpClient.post(`${this.resource}/${usuarioId}/roles`, { role_ids: roleIds });
    }
}
