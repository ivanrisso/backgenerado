import { ref } from 'vue';
import {
    getMenuTreeUseCase,
    createMenuItemUseCase,
    updateMenuItemUseCase,
    deleteMenuItemUseCase,
    assignRolesToMenuItemUseCase
} from '../../../di';
import { MenuItem } from '../../../domain/entities/MenuItem';

export function useMenuItems() {
    const menuTree = ref<MenuItem[]>([]);
    const isLoading = ref(false);
    const error = ref<string | null>(null);

    const loadMenuTree = async () => {
        isLoading.value = true;
        error.value = null;
        try {
            menuTree.value = await getMenuTreeUseCase.execute();
        } catch (e: any) {
            error.value = e.message || 'Error loading menu tree';
        } finally {
            isLoading.value = false;
        }
    };

    const saveMenuItem = async (item: MenuItem) => {
        isLoading.value = true;
        try {
            if (item.id && item.id > 0) {
                await updateMenuItemUseCase.execute(item);
            } else {
                await createMenuItemUseCase.execute(item);
            }
            await loadMenuTree();
        } catch (e: any) {
            error.value = e.message;
            throw e;
        } finally {
            isLoading.value = false;
        }
    };

    const deleteMenuItem = async (id: number) => {
        isLoading.value = true;
        try {
            await deleteMenuItemUseCase.execute(id);
            await loadMenuTree();
        } catch (e: any) {
            error.value = e.message;
        } finally {
            isLoading.value = false;
        }
    };

    const assignRoles = async (id: number, roleIds: number[]) => {
        isLoading.value = true;
        try {
            await assignRolesToMenuItemUseCase.execute(id, roleIds);
            await loadMenuTree();
        } catch (e: any) {
            error.value = e.message;
            throw e;
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
        deleteMenuItem,
        assignRoles
    };
}
