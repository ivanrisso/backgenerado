<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Roles</h1>
        <p class="text-gray-600">Gestión de roles y permisos.</p>
      </div>
      <button v-if="!showForm" @click="handleNew" class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 flex items-center gap-2">
        <span class="text-xl font-light">+</span> Nuevo Rol
      </button>
    </div>

    <!-- Form Area -->
    <div v-if="showForm">
        <RolForm :modelValue="(editingEntity as any)" @submit="handleSubmit" @cancel="showForm = false" />
    </div>

    <div v-if="isLoading" class="text-blue-500 py-4">Cargando roles...</div>
    <div v-if="error" class="text-red-500 py-4">{{ error }}</div>

    <!-- List Area -->
    <div v-if="!isLoading && !error" class="bg-white shadow overflow-hidden sm:rounded-md border border-gray-200">
      <ul class="divide-y divide-gray-200">
        <li v-for="item in roles" :key="item.id" class="px-6 py-4 flex items-center justify-between hover:bg-gray-50 transition-colors">
          <div class="flex items-center gap-3">
             <div class="flex flex-col">
                <span class="text-sm font-bold text-gray-900">{{ item.rolNombre }}</span>
                <span v-if="item.esAdmin" class="text-xs font-semibold text-green-700 bg-green-100 rounded px-2 py-0.5 inline-block w-fit mt-1">Administrador</span>
             </div>
          </div>
          <div class="flex space-x-3">
             <button @click="handleEdit(item)" class="text-indigo-600 hover:text-indigo-900 text-sm font-medium">Editar</button>
             <button @click="handleDelete(item)" class="text-red-600 hover:text-red-900 text-sm font-medium">Borrar</button>
          </div>
        </li>
        <li v-if="roles.length === 0" class="px-6 py-8 text-center text-gray-500 italic">
            No hay roles registrados.
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoles } from '@ui/composables/auth/useRoles';
import RolForm from './RolForm.vue';
import { Rol } from '../../../domain/entities/Rol';

const { roles, isLoading, error, loadRoles, saveRol, deleteRol } = useRoles();

const showForm = ref(false);
const editingEntity = ref<Rol | null>(null);

onMounted(async () => {
    await loadRoles();
});

const handleNew = () => {
    editingEntity.value = null;
    showForm.value = true;
};

const handleEdit = (entity: Rol) => {
    editingEntity.value = entity;
    showForm.value = true;
};

const handleDelete = async (item: Rol) => {
    if(confirm(`¿Está seguro de eliminar el rol ${item.rolNombre}?`)) {
        await deleteRol(item.id);
    }
};

const handleSubmit = async (entity: Rol) => {
    try {
        await saveRol(entity);
        showForm.value = false;
        await loadRoles();
    } catch (e: any) {
        alert(e.message || 'Error guardando rol');
    }
};
</script>
