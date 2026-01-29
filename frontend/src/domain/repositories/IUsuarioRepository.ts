import type { Usuario } from '../entities/Usuario';

export interface IUsuarioRepository {
    getMe: () => Promise<Usuario>; // For current user
    getAll: () => Promise<Usuario[]>;
    getById: (id: number) => Promise<Usuario | null>;
    create: (usuario: Usuario) => Promise<void>;
    update: (usuario: Usuario) => Promise<void>;
    delete: (id: number) => Promise<void>;
    assignRoles: (usuarioId: number, roleIds: number[]) => Promise<void>;
}
