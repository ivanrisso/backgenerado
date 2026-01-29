<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoles } from '@ui/composables/auth/useRoles';
import RolForm from './RolForm.vue';
import PageHeader from '../../components/common/PageHeader.vue';
import DataTable from '../../components/common/DataTable.vue';
import type { Rol } from '../../../domain/entities/Rol';

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

<template>
  <div class="space-y-6">
    <PageHeader title="Roles" subtitle="Gestión de roles y permisos.">
      <template #actions>
        <button v-if="!showForm" class="btn btn-primary flex items-center gap-2" @click="handleNew">
          <span class="text-xl leading-none font-light">+</span> Nuevo Rol
        </button>
      </template>
    </PageHeader>

    <div v-if="showForm" class="mb-8">
      <RolForm :model-value="(editingEntity as any)" @submit="handleSubmit" @cancel="showForm = false" />
    </div>

    <div v-if="!showForm">
      <div v-if="isLoading" class="text-blue-500 py-4">
        Cargando roles...
      </div>
      <div v-if="error" class="text-red-500 py-4">
        {{ error }}
      </div>

      <DataTable 
        v-if="!isLoading && !error"
        :columns="[
          { key: 'rolNombre', label: 'Nombre' },
          { key: 'esAdmin', label: 'Tipo' }
        ]" 
        :items="roles" 
        actions
      >
        <template #cell-rolNombre="{ item }">
          <span class="font-medium text-gray-900">{{ item.rolNombre }}</span>
        </template>
        <template #cell-esAdmin="{ item }">
          <span v-if="item.esAdmin" class="text-xs font-semibold text-green-700 bg-green-50 border border-green-200 rounded px-2 py-0.5">Administrador</span>
          <span v-else class="text-xs text-gray-500">Regular</span>
        </template>
            
        <template #actions="{ item }">
          <button class="btn-icon" title="Editar" @click="handleEdit(item)">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
          </button>
          <button class="btn-icon text-red-400 hover:text-red-600 hover:bg-red-50" title="Borrar" @click="handleDelete(item)">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
          </button>
        </template>
      </DataTable>
    </div>
  </div>
</template>
