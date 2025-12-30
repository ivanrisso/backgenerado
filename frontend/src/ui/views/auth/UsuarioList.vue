<template>
  <div class="space-y-6">
    <PageHeader title="Usuarios" subtitle="Gestión de usuarios y accesos del sistema.">
        <template #actions>
            <button v-if="!showForm" @click="handleNew" class="btn btn-primary flex items-center gap-2">
                <span class="text-xl leading-none font-light">+</span> Nuevo Usuario
            </button>
        </template>
    </PageHeader>

    <div v-if="showForm" class="mb-8">
        <UsuarioForm :modelValue="(editingEntity as any)" @submit="handleSubmit" @cancel="showForm = false" />
    </div>

    <div v-if="!showForm">
        <div v-if="loading" class="text-blue-500 py-4">Cargando usuarios...</div>
        <div v-if="error" class="text-red-500 py-4">{{ error }}</div>

        <DataTable 
            v-if="!loading && !error"
            :columns="[
                { key: 'nombre', label: 'Nombre' },
                { key: 'roles', label: 'Roles' },
                { key: 'email', label: 'Email' }
            ]" 
            :items="usuarios" 
            actions
        >
            <template #cell-nombre="{ item }">
                 <div class="flex flex-col">
                    <span class="font-medium text-gray-900">{{ item.nombre }} {{ item.apellido }}</span>
                 </div>
            </template>
            <template #cell-email="{ item }">
                 <span class="text-gray-500">{{ item.email instanceof Object ? item.email.getValue() : item.email }}</span>
            </template>
            <template #cell-roles="{ item }">
                <div class="flex gap-1 flex-wrap">
                    <span v-for="role in item.roles" :key="role.id" class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-50 text-blue-700 border border-blue-100">
                        {{ role.rolNombre }}
                    </span>
                    <span v-if="!item.roles || item.roles.length === 0" class="text-xs text-gray-400 italic">Sin roles</span>
                </div>
            </template>
            
            <template #actions="{ item }">
                 <button @click="handleEdit(item)" class="btn-icon" title="Editar">
                    <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                </button>
                <button @click="handleDelete(item)" class="btn-icon text-red-400 hover:text-red-600 hover:bg-red-50" title="Borrar">
                    <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                </button>
            </template>
        </DataTable>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useUsuarios } from '@ui/composables/auth/useUsuarios';
import UsuarioForm from './UsuarioForm.vue';
import PageHeader from '../../components/common/PageHeader.vue';
import DataTable from '../../components/common/DataTable.vue';
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
