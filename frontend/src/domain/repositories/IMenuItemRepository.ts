import type { MenuItem } from '../entities/MenuItem';

export interface IMenuItemRepository {
    getTree: () => Promise<MenuItem[]>; // Returns hierarchical structure
    create: (item: MenuItem) => Promise<void>;
    update: (item: MenuItem) => Promise<void>;
    delete: (id: number) => Promise<void>;
    assignRoles: (menuItemId: number, roleIds: number[]) => Promise<void>;
}
