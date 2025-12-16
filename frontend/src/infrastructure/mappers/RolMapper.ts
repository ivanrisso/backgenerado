import { Rol } from '../../domain/entities/Rol';
import type { RolDTO } from '../dtos/UsuarioDTO';

export class RolMapper {
    static toDomain(dto: RolDTO): Rol {
        return new Rol(dto.id, dto.rol_nombre, dto.es_admin);
    }

    static toDTO(entity: Rol): RolDTO {
        return {
            id: entity.id,
            rol_nombre: entity.rolNombre,
            es_admin: entity.esAdmin
        };
    }
}
