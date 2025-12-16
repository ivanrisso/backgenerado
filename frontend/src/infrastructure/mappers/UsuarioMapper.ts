import { Usuario } from '../../domain/entities/Usuario';
import { Rol } from '../../domain/entities/Rol';
import { Email } from '../../domain/value-objects/Email';
import type { UsuarioDTO } from '../dtos/UsuarioDTO';

export class UsuarioMapper {
    static toDomain(dto: UsuarioDTO): Usuario {
        const roles = dto.roles ? dto.roles.map(r => new Rol(r.id, r.rol_nombre, r.es_admin)) : [];
        return new Usuario(
            dto.id,
            new Email(dto.usuario_email),
            dto.nombre,
            dto.apellido,
            roles
        );
    }

    static toDTO(entity: Usuario): UsuarioDTO {
        return {
            id: entity.id,
            usuario_email: entity.email.getValue(),
            usuario_password: entity.password,
            nombre: entity.nombre,
            apellido: entity.apellido,
            roles: entity.roles.map(r => ({
                id: r.id,
                rol_nombre: r.rolNombre,
                es_admin: r.esAdmin
            })),
            role_ids: entity.roles.map(r => r.id)
        };
    }
}
