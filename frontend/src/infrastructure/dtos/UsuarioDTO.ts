export interface UsuarioDTO {
    id: number;
    usuario_email: string;
    usuario_password?: string;
    nombre: string;
    apellido: string;
    roles?: RolDTO[];
    role_ids?: number[];
}

export interface RolDTO {
    id: number;
    rol_nombre: string;
    es_admin: boolean;
}
