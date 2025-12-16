import type { IRolRepository } from '../../../domain/repositories/IRolRepository';
import { Rol } from '../../../domain/entities/Rol';

export class GetAllRolesUseCase {
    constructor(private readonly repository: IRolRepository) { }

    async execute(): Promise<Rol[]> {
        return this.repository.getAll();
    }
}

export class GetRolByIdUseCase {
    constructor(private readonly repository: IRolRepository) { }

    async execute(id: number): Promise<Rol | null> {
        return this.repository.getById(id);
    }
}

export class CreateRolUseCase {
    constructor(private readonly repository: IRolRepository) { }

    async execute(rol: Rol): Promise<void> {
        await this.repository.create(rol);
    }
}

export class UpdateRolUseCase {
    constructor(private readonly repository: IRolRepository) { }

    async execute(rol: Rol): Promise<void> {
        await this.repository.update(rol);
    }
}

export class DeleteRolUseCase {
    constructor(private readonly repository: IRolRepository) { }

    async execute(id: number): Promise<void> {
        await this.repository.delete(id);
    }
}
