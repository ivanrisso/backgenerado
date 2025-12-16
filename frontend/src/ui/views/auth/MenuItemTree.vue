<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Menú del Sistema</h1>
        <p class="text-gray-600">Configuración de estructura y permisos de menú.</p>
      </div>
      <button v-if="!showForm" @click="handleNew(null)" class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 flex items-center gap-2">
        <span class="text-xl font-light">+</span> Nuevo Item Raíz
      </button>
    </div>

    <!-- Form Area -->
    <div v-if="showForm">
        <MenuItemForm 
            :modelValue="(editingEntity as any)" 
            :parentId="newParentId" 
            :availableParents="flatMenuItems"
            @submit="handleSubmit" 
            @cancel="showForm = false" 
        />
    </div>

    <div v-if="isLoading" class="text-blue-500 py-4">Cargando menú...</div>
    <div v-if="error" class="text-red-500 py-4">{{ error }}</div>

    <!-- Tree List Area -->
    <div v-if="!isLoading && !error" class="bg-white shadow overflow-hidden sm:rounded-md border border-gray-200">
      <ul class="divide-y divide-gray-200">
        <li v-for="item in menuTree" :key="item.id" class="px-6 py-4">
            <div class="flex justify-between items-start">
                <div class="flex flex-col">
                    <span class="text-sm font-bold text-gray-900 flex items-center gap-2">
                        {{ item.nombre }}
                        <span v-if="item.roles.length > 0" class="text-xs font-normal text-gray-500 bg-gray-100 px-1.5 py-0.5 rounded">🔒 {{ item.roles.length }} roles</span>
                    </span>
                    <span class="text-xs text-gray-500">{{ item.path || '(Sin ruta)' }}</span>
                </div>
                        <div class="flex space-x-2">
                            <button @click="openCreateChild(item.id)" class="text-green-600 hover:text-green-900 text-xs font-medium border border-green-200 px-2 py-1 rounded bg-green-50">+ Hijo</button>
                            <button @click="handleEdit(item)" class="text-indigo-600 hover:text-indigo-900 text-xs font-medium border border-indigo-200 px-2 py-1 rounded bg-indigo-50">Editar</button>
                            <button @click="handleDelete(item.id)" class="text-red-600 hover:text-red-900 text-xs font-medium border border-red-200 px-2 py-1 rounded bg-red-50">Borrar</button>
                        </div>
                    </div>
                    
             <!-- Recursive Children (Flattened for simplicitly or nested) -->
             <!-- For deep nesting, a recursive component is better, but doing 1-level deep here as before -->
             <ul v-if="item.children && item.children.length > 0" class="mt-3 ml-4 border-l-2 border-gray-100 pl-4 space-y-3">
                 <li v-for="child in item.children" :key="child.id">
                    <div class="flex justify-between items-start">
                        <div class="flex flex-col">
                            <span class="text-sm font-medium text-gray-800 flex items-center gap-2">
                                {{ child.nombre }}
                                <span v-if="child.roles.length > 0" class="text-xs font-normal text-gray-500 bg-gray-100 px-1.5 py-0.5 rounded">🔒 {{ child.roles.length }} roles</span>
                            </span>
                            <span class="text-xs text-gray-500">{{ child.path || '(Sin ruta)' }}</span>
                        </div>
                        <div class="flex space-x-2">
                             <button @click="handleEdit(child)" class="text-indigo-600 hover:text-indigo-900 text-xs font-medium">Editar</button>
                             <button @click="handleDelete(child.id)" class="text-red-600 hover:text-red-900 text-xs font-medium pl-2">Borrar</button>
                        </div>
                    </div>
                 </li>
             </ul>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useMenuItems } from '@ui/composables/auth/useMenuItems';
import MenuItemForm from './MenuItemForm.vue';
import { MenuItem } from '../../../domain/entities/MenuItem';

const { menuTree, isLoading, error, loadMenuTree, saveMenuItem, deleteMenuItem } = useMenuItems();

const showForm = ref(false);
const editingEntity = ref<MenuItem | null>(null);
const newParentId = ref<number | null>(null);

// Flatten the tree for the select dropdown
const flattenItems = (items: MenuItem[], result: MenuItem[] = []) => {
    for (const item of items) {
        result.push(item);
        if (item.children && item.children.length > 0) {
            flattenItems(item.children, result);
        }
    }
    return result;
};

const flatMenuItems = computed(() => flattenItems(menuTree.value));

onMounted(async () => {
    await loadMenuTree();
});

const handleNew = (parentId: number | null) => {
    editingEntity.value = null;
    newParentId.value = parentId;
    showForm.value = true;
};

const openCreateChild = (parentId: number) => {
    handleNew(parentId);
};

const handleEdit = (item: MenuItem) => {
    editingEntity.value = item;
    newParentId.value = item.parentId; // Should be part of item? yes. parentId property.
    showForm.value = true;
};

const handleDelete = async (id: number) => {
    if (confirm('¿Está seguro de eliminar este item de menú?')) {
        await deleteMenuItem(id);
    }
};

const handleSubmit = async (entity: MenuItem) => {
    try {
        await saveMenuItem(entity);
        showForm.value = false;
    } catch (e: any) {
        alert(e.message || 'Error guardando item');
    }
};
</script>
