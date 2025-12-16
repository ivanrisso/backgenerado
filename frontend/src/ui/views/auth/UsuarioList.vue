<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Usuarios</h1>
        <p class="text-gray-600">Gestión de usuarios y accesos.</p>
      </div>
      <button v-if="!showForm" @click="handleNew" class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 flex items-center gap-2">
        <span class="text-xl font-light">+</span> Nuevo Usuario
      </button>
    </div>

    <!-- Form Area -->
    <div v-if="showForm">
        <UsuarioForm :modelValue="(editingEntity as any)" @submit="handleSubmit" @cancel="showForm = false" />
    </div>

    <div v-if="loading" class="text-blue-500 py-4">Cargando usuarios...</div>
    <div v-if="error" class="text-red-500 py-4">{{ error }}</div>

    <!-- List Area -->
    <div v-if="!loading && !error" class="bg-white shadow overflow-hidden sm:rounded-md border border-gray-200">
      <ul class="divide-y divide-gray-200">
        <li v-for="item in usuarios" :key="item.id" class="px-6 py-4 flex items-center justify-between hover:bg-gray-50 transition-colors">
          <div class="flex flex-col gap-1">
            <div class="flex items-center gap-2">
                <span class="text-sm font-bold text-gray-900">{{ item.nombre }} {{ item.apellido }}</span>
                <span class="text-xs text-gray-500">({{ item.email instanceof Object ? item.email.getValue() : item.email }})</span>
            </div>
            <div class="flex gap-1 flex-wrap">
                <span v-for="role in item.roles" :key="role.id" class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800">
                    {{ role.rolNombre }}
                </span>
                <span v-if="!item.roles || item.roles.length === 0" class="text-xs text-gray-400 italic">Sin roles</span>
            </div>
          </div>
          <div class="flex space-x-3">
             <button @click="handleEdit(item)" class="text-indigo-600 hover:text-indigo-900 text-sm font-medium">Editar</button>
             <button @click="handleDelete(item)" class="text-red-600 hover:text-red-900 text-sm font-medium">Borrar</button>
          </div>
        </li>
        <li v-if="usuarios.length === 0" class="px-6 py-8 text-center text-gray-500 italic">
            No hay usuarios registrados.
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useUsuarios } from '@ui/composables/auth/useUsuarios';
import UsuarioForm from './UsuarioForm.vue';
import { Usuario } from '../../../domain/entities/Usuario';

const { usuarios, isLoading: loading, error, loadUsuarios, saveUsuario, deleteUsuario, assignRoles } = useUsuarios();

const showForm = ref(false);
const editingEntity = ref<Usuario | null>(null);

onMounted(async () => {
    await loadUsuarios();
});

const handleNew = () => {
    editingEntity.value = null;
    showForm.value = true;
};

const handleEdit = (entity: Usuario) => {
    editingEntity.value = entity;
    showForm.value = true;
};

const handleDelete = async (item: Usuario) => {
    if(confirm(`¿Está seguro de eliminar al usuario ${item.nombre}?`)) {
        await deleteUsuario(item.id);
    }
};

const handleSubmit = async (entity: Usuario) => {
    try {
        await saveUsuario(entity);
        
        showForm.value = false;
        await loadUsuarios(); // Refresh list to see changes
    } catch (e: any) {
        alert(e.message || 'Error guardando usuario');
    }
};
</script>
