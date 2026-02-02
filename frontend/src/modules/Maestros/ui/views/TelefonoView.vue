<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useTelefonos } from '@modules/Maestros/composables/useTelefonos';
import TelefonoForm from './TelefonoForm.vue';
import PageHeader from '@shared/ui/PageHeader.vue';
import DataTable from '@shared/ui/DataTable.vue';
import type { Telefono } from '@domain/entities/Telefono';

const { telefonos, loading, error, loadTelefonos, createTelefono, updateTelefono, deleteTelefono } = useTelefonos();

const showForm = ref(false);
const editingEntity = ref<Telefono | null>(null);

onMounted(() => {
    loadTelefonos();
});

const handleNew = () => {
    editingEntity.value = null;
    showForm.value = true;
};

const handleEdit = (entity: Telefono) => {
    editingEntity.value = entity;
    showForm.value = true;
};

const handleDelete = async (id: number) => {
    if(confirm('¿Está seguro de eliminar este registro?')) {
        await deleteTelefono(id);
    }
};

const handleSubmit = async (entity: Telefono) => {
    try {
        if (entity.id === 0) {
           await createTelefono(entity);
        } else {
           await updateTelefono(entity);
        }
        showForm.value = false;
    } catch (e) {
        // Error handled in composable
    }
};
</script>

<template>
  <div class="space-y-6">
    <PageHeader title="Teléfonos" subtitle="Catálogo global de teléfonos.">
      <template #actions>
        <button class="btn btn-primary" @click="handleNew">
          + Nuevo
        </button>
      </template>
    </PageHeader>

    <div v-if="showForm" class="mb-8">
      <TelefonoForm :model-value="editingEntity" @submit="handleSubmit" @cancel="showForm = false" />
    </div>

    <div v-if="!showForm">
      <div v-if="loading" class="text-blue-500 p-4">
        Cargando...
      </div>
      <div v-if="error" class="text-red-500 p-4">
        {{ error }}
      </div>

      <DataTable 
        v-if="!loading && !error"
        :columns="[
          { key: 'numero', label: 'Número' },
          { key: 'domicilio_id', label: 'Domicilio', class: 'w-32' },
        ]" 
        :items="telefonos" 
        actions
      >
        <template #cell-numero="{ item }">
          <span class="font-mono text-gray-900">{{ item.prefijo }} - {{ item.numero }}</span>
        </template>
        <template #cell-domicilio_id="{ item }">
          <span class="px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded-full">ID: {{ item.domicilio_id }}</span>
        </template>
            
        <template #actions="{ item }">
          <button class="btn-icon" title="Editar" @click="handleEdit(item)">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
          </button>
          <button class="btn-icon text-red-400 hover:text-red-600 hover:bg-red-50" title="Borrar" @click="handleDelete(item.id)">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
          </button>
        </template>
      </DataTable>
    </div>
  </div>
</template>
