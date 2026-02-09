import { ref } from 'vue';
import { httpClient } from '@/shared/http/client';
// MenuItem import removed as unused

// Simple interface for response structure if Entity is too complex or not perfectly matching
interface MenuItemDTO {
    id: number;
    nombre: string;
    path: string | null;
    parent_id: number | null;
    orden: number;
    roles: any[];
}

export function useUserMenu() {
    const menuTree = ref<any[]>([]); // Using any[] to allow flexible UI structure
    const isLoading = ref(false);
    const error = ref<string | null>(null);

    const buildTree = (items: MenuItemDTO[]): any[] => {
        const map = new Map<string, any>();
        const roots: any[] = [];

        console.log('Raw Menu Items:', items);

        // 1. Create nodes and map by String ID for safety
        items.forEach(item => {
            const strId = String(item.id);
            map.set(strId, {
                id: item.id,
                label: item.nombre,
                route: item.path,
                icon: 'home', // Default
                orden: item.orden,
                roles: item.roles,
                children: []
            });
        });

        // 2. Assemble tree
        items.forEach(item => {
            const strId = String(item.id);
            const node = map.get(strId);

            // Check parent
            if (item.parent_id !== null && item.parent_id !== undefined) {
                const strParentId = String(item.parent_id);
                if (map.has(strParentId)) {
                    const parent = map.get(strParentId);
                    parent.children.push(node);
                } else {
                    console.warn(`Orphan item found: ${item.nombre} (ID: ${item.id}) points to missing Parent ID: ${item.parent_id}`);
                    // Decision: Add to roots or hide? Let's add to roots so it's visible at least
                    // roots.push(node); 
                    // Better for now: don't push to roots if it's supposed to be a child, just log. 
                    // Or push to roots to debug. Let's push to roots so user can see it's broken but accessible.
                    roots.push(node);
                }
            } else {
                roots.push(node);
            }
        });

        return roots;
    };

    const loadUserMenu = async () => {
        isLoading.value = true;
        error.value = null;
        try {
            // Fetch from the correct user-specific endpoint
            const response = await httpClient.get<MenuItemDTO[]>('/usuarios/me/menu');
            menuTree.value = buildTree(response.data);
        } catch (e: any) {
            console.error('Failed to load user menu', e);
            error.value = 'No se pudo cargar el menú.';
        } finally {
            isLoading.value = false;
        }
    };

    return {
        menuTree,
        isLoading,
        error,
        loadUserMenu
    };
}
