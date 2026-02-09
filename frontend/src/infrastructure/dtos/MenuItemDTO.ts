import type { RolDTO } from './UsuarioDTO';

export interface MenuItemDTO {
    id: number;
    nombre: string;
    path: string | null;
    parent_id: number | null;
    orden?: number;
    children?: MenuItemDTO[];
    roles?: RolDTO[];
    role_ids?: number[];
}
