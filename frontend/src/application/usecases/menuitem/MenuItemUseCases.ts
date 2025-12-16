import type { IMenuItemRepository } from '../../../domain/repositories/IMenuItemRepository';
import { MenuItem } from '../../../domain/entities/MenuItem';

export class GetMenuTreeUseCase {
    constructor(private readonly repository: IMenuItemRepository) { }

    async execute(): Promise<MenuItem[]> {
        return this.repository.getTree();
    }
}

export class CreateMenuItemUseCase {
    constructor(private readonly repository: IMenuItemRepository) { }

    async execute(item: MenuItem): Promise<void> {
        await this.repository.create(item);
    }
}

export class UpdateMenuItemUseCase {
    constructor(private readonly repository: IMenuItemRepository) { }

    async execute(item: MenuItem): Promise<void> {
        await this.repository.update(item);
    }
}

export class DeleteMenuItemUseCase {
    constructor(private readonly repository: IMenuItemRepository) { }

    async execute(id: number): Promise<void> {
        await this.repository.delete(id);
    }
}

export class AssignRolesToMenuItemUseCase {
    constructor(private readonly repository: IMenuItemRepository) { }

    async execute(menuItemId: number, roleIds: number[]): Promise<void> {
        await this.repository.assignRoles(menuItemId, roleIds);
    }
}
