import type { IUsuarioRepository } from '../../../domain/repositories/IUsuarioRepository';
import { Usuario } from '../../../domain/entities/Usuario';

export class GetAllUsuariosUseCase {
    constructor(private readonly repository: IUsuarioRepository) { }

    async execute(): Promise<Usuario[]> {
        return this.repository.getAll();
    }
}

export class GetUsuarioByIdUseCase {
    constructor(private readonly repository: IUsuarioRepository) { }

    async execute(id: number): Promise<Usuario | null> {
        return this.repository.getById(id);
    }
}

export class CreateUsuarioUseCase {
    constructor(private readonly repository: IUsuarioRepository) { }

    async execute(usuario: Usuario): Promise<void> {
        // Business Rule: Check if email is unique? Usually handled by Repo/Backend, 
        // but we could have logic here if we had a check method.
        await this.repository.create(usuario);
    }
}

export class UpdateUsuarioUseCase {
    constructor(private readonly repository: IUsuarioRepository) { }

    async execute(usuario: Usuario): Promise<void> {
        await this.repository.update(usuario);
    }
}

export class AssignRolesToUsuarioUseCase {
    constructor(private readonly repository: IUsuarioRepository) { }

    async execute(usuarioId: number, roleIds: number[]): Promise<void> {
        await this.repository.assignRoles(usuarioId, roleIds);
    }
}

export class DeleteUsuarioUseCase {
    constructor(private readonly repository: IUsuarioRepository) { }

    async execute(id: number): Promise<void> {
        await this.repository.delete(id);
    }
}
