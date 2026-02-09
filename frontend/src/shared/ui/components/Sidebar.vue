<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '../../stores/auth';
import { useUserMenu } from '@/shared/composables/useUserMenu';

const authStore = useAuthStore();
const { menuTree, loadUserMenu } = useUserMenu();
const openGroups = ref<string[]>(['facturacion', 'clientes']); // Default open

// Load menu on mount
onMounted(async () => {
    await loadUserMenu();
});

// Filter mainly to remove empty groups (backend already filters by permission)
const filterItems = (items: any[]): any[] => {
    return items
        .map(item => {
            // If it has children, recurse
            if (item.children && item.children.length > 0) {
                return {
                    ...item,
                    children: filterItems(item.children)
                };
            }
            return item;
        })
        .filter(item => {
            // Remove groups that ended up empty
            if (item.children && item.children.length === 0) {
                // Determine if it was a group (has children property originally or intention)
                // For now, if it implies having children but has none, hide it.
                // Or if it is a folder (no route) and has no children.
                if (!item.route || item.route === '#') {
                     return false;
                }
            }
            return true;
        });
};

const sortItems = (items: any[]): any[] => {
    return items.slice().sort((a, b) => (a.orden || 0) - (b.orden || 0)).map(item => {
        if (item.children && item.children.length > 0) {
            return { ...item, children: sortItems(item.children) };
        }
        return item;
    });
};

const filteredMenu = computed(() => sortItems(filterItems(menuTree.value)));

const toggleGroup = (id: string) => {
    if (openGroups.value.includes(id)) {
        openGroups.value = openGroups.value.filter(g => g !== id);
    } else {
        openGroups.value.push(id);
    }
};

const handleLogout = async () => {
    if (confirm('¿Cerrar sesión?')) {
        await authStore.logout();
    }
};
</script>

<template>
  <aside class="w-64 bg-white shadow-md flex-shrink-0 hidden md:flex md:flex-col">
    <div class="p-6 border-b border-gray-200">
      <h1 class="text-xl font-bold text-gray-800">
        Facturación
      </h1>
      <div v-if="authStore.user" class="mt-2 text-xs text-gray-500">
        Hola, {{ authStore.user.email }}
      </div>
    </div>
    <nav class="flex-1 px-4 py-4 space-y-1 overflow-y-auto">
      <template v-for="item in filteredMenu" :key="item.id">
        <!-- Parent Item with Children -->
        <div v-if="item.children && item.children.length > 0" class="space-y-1">
          <button class="w-full flex items-center justify-between px-2 py-2 text-sm font-medium text-gray-700 rounded-md hover:bg-gray-50 group focus:outline-none" @click="toggleGroup(item.id)">
            <span class="flex items-center gap-2">
              <!-- Simple Icon Logic based on name or item.icon -->
              <span v-if="item.icon === 'home'">🏠</span>
              <span v-else-if="item.icon === 'users'">👥</span>
              <span v-else-if="item.icon === 'document-text'">📄</span>
              <span v-else-if="item.icon === 'database'">🗄️</span>
              <span v-else-if="item.icon === 'cog'">⚙️</span>
              <span v-else>👉</span>
                        
              {{ item.label }}
            </span>
            <svg :class="{'rotate-90': openGroups.includes(item.id)}" class="w-4 h-4 text-gray-400 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
          <div v-show="openGroups.includes(item.id)" class="pl-4 space-y-1">
            <router-link 
              v-for="child in item.children" 
              :key="child.id"
              :to="child.route || '#'" 
              class="flex items-center px-2 py-2 text-sm font-medium text-gray-600 rounded-md hover:bg-gray-50 group"
              active-class="bg-blue-50 text-blue-700"
            >
              {{ child.label }}
            </router-link>
          </div>
        </div>
            
        <!-- Single Item -->
        <router-link 
          v-else
          :to="item.route || '#'" 
          class="flex items-center px-2 py-2 text-sm font-medium text-gray-700 rounded-md hover:bg-gray-50 group"
          active-class="bg-gray-100 text-gray-900"
        >
          <span class="flex items-center gap-2">
            <span v-if="item.icon === 'home'">🏠</span>
            <span v-else>👉</span>
            {{ item.label }}
          </span>
        </router-link>
      </template>
    </nav>
    <div class="p-4 border-t border-gray-200">
      <button class="w-full flex items-center px-2 py-2 text-sm font-medium text-red-600 rounded-md hover:bg-red-50 group" @click="handleLogout">
        <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
        </svg>
        Cerrar Sesión
      </button>
    </div>
  </aside>
</template>
