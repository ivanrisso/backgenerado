<template>
  <div class="min-h-screen bg-gray-100 flex">
    <!-- Sidebar -->
    <aside class="w-64 bg-white shadow-md flex-shrink-0 hidden md:flex md:flex-col">
      <div class="p-6 border-b border-gray-200">
        <h1 class="text-xl font-bold text-gray-800">Facturación</h1>
      </div>
      <nav class="flex-1 px-4 py-4 space-y-1 overflow-y-auto">
        <template v-for="item in menuTree" :key="item.id">
            <!-- Parent Item with Children -->
            <div v-if="item.children && item.children.length > 0" class="space-y-1">
                <button @click="toggleGroup(item.id)" class="w-full flex items-center justify-between px-2 py-2 text-sm font-medium text-gray-700 rounded-md hover:bg-gray-50 group focus:outline-none">
                    <span class="flex items-center gap-2">
                        <!-- Icon placeholder could go here -->
                        {{ item.nombre }}
                    </span>
                    <svg :class="{'rotate-90': openGroups.includes(item.id)}" class="w-4 h-4 text-gray-400 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                    </svg>
                </button>
                <div v-show="openGroups.includes(item.id)" class="pl-4 space-y-1">
                    <router-link 
                        v-for="child in item.children" 
                        :key="child.id"
                        :to="child.path || '#'" 
                        class="flex items-center px-2 py-2 text-sm font-medium text-gray-600 rounded-md hover:bg-gray-50 group"
                        active-class="bg-blue-50 text-blue-700"
                    >
                        {{ child.nombre }}
                    </router-link>
                </div>
            </div>
            
            <!-- Single Item -->
            <router-link 
                v-else
                :to="item.path || '#'" 
                class="flex items-center px-2 py-2 text-sm font-medium text-gray-700 rounded-md hover:bg-gray-50 group"
                active-class="bg-gray-100 text-gray-900"
            >
                {{ item.nombre }}
            </router-link>
        </template>
        
        <!-- Fallback/loading state -->
        <div v-if="loading" class="px-4 py-2 text-sm text-gray-400">
            Cargando menú...
        </div>
      </nav>
      <div class="p-4 border-t border-gray-200">
        <button @click="handleLogout" class="w-full flex items-center px-2 py-2 text-sm font-medium text-red-600 rounded-md hover:bg-red-50 group">
            <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            Cerrar Sesión
        </button>
      </div>
    </aside>

    <!-- Mobile Header (Visible on small screens) -->
    <div class="flex flex-col flex-1 min-w-0">
        <header class="md:hidden bg-white shadow-sm p-4 flex justify-between items-center">
             <h1 class="text-lg font-bold text-gray-800">Facturación</h1>
             <!-- Mobile menu toggle could go here -->
        </header>

        <!-- Main Content (Shared) -->
        <main class="flex-1 p-6 overflow-y-auto">
          <router-view></router-view>
        </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useMenuItems } from '../composables/auth/useMenuItems';
import { logoutUseCase } from '../../di';

const router = useRouter();
const { menuTree, isLoading: loading, loadMenuTree } = useMenuItems();
const openGroups = ref<number[]>([]);

const toggleGroup = (id: number) => {
    if (openGroups.value.includes(id)) {
        openGroups.value = openGroups.value.filter(g => g !== id);
    } else {
        openGroups.value.push(id);
    }
};

const handleLogout = async () => {
    if (confirm('¿Cerrar sesión?')) {
        try {
            await logoutUseCase.execute();
            router.push('/login');
        } catch (error) {
            console.error('Error logging out:', error);
            // Force redirect even on error
            router.push('/login');
        }
    }
};

onMounted(async () => {
    await loadMenuTree();
});
</script>
