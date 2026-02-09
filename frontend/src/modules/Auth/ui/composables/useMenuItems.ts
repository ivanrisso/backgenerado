import { ref } from 'vue';
import { AxiosMenuItemRepository } from '@infra/repositories/AxiosMenuItemRepository';
import type { MenuItem } from '@domain/entities/MenuItem';

export function useMenuItems() {
    const repository = new AxiosMenuItemRepository();
    const menuTree = ref<MenuItem[]>([]);
    const isLoading = ref(false);
    const error = ref<string | null>(null);

    const loadMenuTree = async () => {
        isLoading.value = true;
        error.value = null;
        try {
            menuTree.value = await repository.getTree();
        } catch (e) {
            error.value = 'Error loading menu tree';
            console.error(e);
        } finally {
            isLoading.value = false;
        }
    };

    const saveMenuItem = async (item: MenuItem) => {
        isLoading.value = true;
        try {
            if (item.id) {
                await repository.update(item);
            } else {
                await repository.create(item);
            }
            await loadMenuTree(); // Refresh
        } catch (e) {
            error.value = 'Error saving menu item';
            throw e;
        } finally {
            isLoading.value = false;
        }
    };

    const deleteMenuItem = async (id: number) => {
        if (!confirm('¿Seguro que desea eliminar este ítem?')) return;

        isLoading.value = true;
        try {
            await repository.delete(id);
            await loadMenuTree();
        } catch (e) {
            error.value = 'Error deleting menu item';
            console.error(e);
        } finally {
            isLoading.value = false;
        }
    };

    return {
        menuTree,
        isLoading,
        error,
        loadMenuTree,
        saveMenuItem,
        deleteMenuItem
    };
}
