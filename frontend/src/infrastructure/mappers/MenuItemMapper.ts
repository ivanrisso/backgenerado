import { MenuItem } from '../../domain/entities/MenuItem';
import { Rol } from '../../domain/entities/Rol';
import type { MenuItemDTO } from '../dtos/MenuItemDTO';
import type { RolDTO } from '../dtos/UsuarioDTO';

export class MenuItemMapper {
    static toDomain(dto: MenuItemDTO): MenuItem {
        const roles = dto.roles ? dto.roles.map((r: RolDTO) => new Rol(r.id, r.rol_nombre, r.es_admin)) : [];
        const children = dto.children ? dto.children.map(c => MenuItemMapper.toDomain(c)) : [];

        return new MenuItem(
            dto.id,
            dto.nombre,
            dto.path,
            dto.parent_id,
            dto.orden || 0,
            children,
            roles
        );
    }

    // Usually we don't send the Full Tree back in create/update, just fields.
    // But for completeness:
    static toDTO(entity: MenuItem): MenuItemDTO {
        return {
            id: entity.id,
            nombre: entity.nombre,
            path: entity.path,
            parent_id: entity.parentId,
            orden: entity.orden,
            role_ids: entity.roles.map(r => r.id)
        };
    }
}
