import type { IMenuItemRepository } from '../../domain/repositories/IMenuItemRepository';
import type { MenuItem } from '../../domain/entities/MenuItem';
import { httpClient } from '../api/httpClient';
import { MenuItemMapper } from '../mappers/MenuItemMapper';
import type { MenuItemDTO } from '../dtos/MenuItemDTO';

export class AxiosMenuItemRepository implements IMenuItemRepository {
    private readonly resource = '/menuitems/';

    async getTree(): Promise<MenuItem[]> {
        // Backend doesn't support /tree, fetching all and building tree locally
        const { data } = await httpClient.get<MenuItemDTO[]>(this.resource);
        const items = data.map(MenuItemMapper.toDomain);
        return this.buildTree(items);
    }

    private buildTree(items: MenuItem[]): MenuItem[] {
        const map = new Map<number, MenuItem>();
        const roots: MenuItem[] = [];

        items.forEach(item => {
            // Re-create items to ensure children arrays are fresh if needed, 
            // though toDomain initializes them empty.
            map.set(item.id, item);
        });

        items.forEach(item => {
            if (item.parentId && map.has(item.parentId)) {
                const parent = map.get(item.parentId);
                parent?.addChild(item);
            } else {
                roots.push(item);
            }
        });

        return roots;
    }

    async create(item: MenuItem): Promise<void> {
        await httpClient.post(this.resource, MenuItemMapper.toDTO(item));
    }

    async update(item: MenuItem): Promise<void> {
        await httpClient.patch(`${this.resource}${item.id}`, MenuItemMapper.toDTO(item));
    }

    async delete(id: number): Promise<void> {
        await httpClient.delete(`${this.resource}${id}`);
    }

    async assignRoles(menuItemId: number, roleIds: number[]): Promise<void> {
        await httpClient.post(`${this.resource}${menuItemId}/roles`, { role_ids: roleIds });
    }
}
