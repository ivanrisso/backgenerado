<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useCondicionesTributarias } from '@modules/Maestros/composables/useCondicionesTributarias';
import CondicionTributariaForm from './CondicionTributariaForm.vue';
import PageHeader from '@shared/ui/PageHeader.vue';
import DataTable from '@shared/ui/DataTable.vue';
import type { CondicionTributaria } from '@domain/entities/CondicionTributaria';

const { 
    condicionesTributarias, 
    loading, 
    error, 
    loadCondicionesTributarias, 
    createCondicionTributaria, 
    updateCondicionTributaria, 
    deleteCondicionTributaria 
} = useCondicionesTributarias();

const showForm = ref(false);
const isDeleteMode = ref(false);
const editingEntity = ref<CondicionTributaria | null>(null);

onMounted(() => {
    loadCondicionesTributarias();
});

const handleNew = () => {
    editingEntity.value = null;
    isDeleteMode.value = false;
    // We don't manually reset 'error' here because it's a ref from the composable shared state
    // Ideally, the composable should expose a clearError method or we just rely on the next action clearing it.
    showForm.value = true;
};

const handleEdit = (entity: CondicionTributaria) => {
    editingEntity.value = entity;
    isDeleteMode.value = false;
    showForm.value = true;
};

const handlePreDelete = (entity: CondicionTributaria) => {
    editingEntity.value = entity;
    isDeleteMode.value = true;
    showForm.value = true;
};

const handleConfirmDelete = async (id: number) => {
    try {
        await deleteCondicionTributaria(id);
        showForm.value = false;
    } catch (e) {
        // Error is set in 'error' ref by composable
    }
};

const handleCancel = () => {
    showForm.value = false;
    isDeleteMode.value = false;
};

const handleSubmit = async (entity: CondicionTributaria) => {
    try {
        if (entity.id === 0) {
           await createCondicionTributaria(entity);
        } else {
           await updateCondicionTributaria(entity);
        }
        showForm.value = false;
    } catch (e) {
        // Error handled in composable
    }
};
</script>

<template>
  <div class="space-y-6">
    <PageHeader title="Condiciones Tributarias" subtitle="Catálogo de condiciones ante AFIP (Inscripto, Exento, etc)">
      <template #actions>
        <button class="btn btn-primary" @click="handleNew">
          + Nueva
        </button>
      </template>
    </PageHeader>
    
    <!-- Global Error Display (if not in form) -->
    <div v-if="error && !showForm" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
      <strong class="font-bold">Error: </strong>
      <span class="block sm:inline">{{ error }}</span>
    </div>

    <div v-if="showForm" class="mb-8">
      <CondicionTributariaForm 
        :model-value="editingEntity" 
        :is-delete-mode="isDeleteMode"
        :server-error="error"
        @submit="handleSubmit" 
        @delete="handleConfirmDelete"
        @cancel="handleCancel" 
      />
    </div>

    <div v-if="!showForm">
      <div v-if="loading" class="text-blue-500 p-4">
        Cargando...
      </div>

      <DataTable 
        v-if="!loading && (!error || showForm)"
        :columns="[
          { key: 'nombre', label: 'Nombre', class: 'font-medium' },
          { key: 'tipo_impuesto', label: 'Impuesto', class: 'w-32' },
          { key: 'ambito', label: 'Ámbito', class: 'w-24 capitalize' },
          { key: 'descripcion', label: 'Descripción' }
        ]" 
        :items="condicionesTributarias" 
        actions
      >
        <template #cell-tipo_impuesto="{ item }">
          <span v-if="item.tipo_impuesto" class="text-xs font-semibold text-blue-700 bg-blue-50 px-2 py-0.5 rounded border border-blue-100">
            {{ item.tipo_impuesto.nombre }}
          </span>
          <span v-else class="text-xs text-gray-400 italic">General</span>
        </template>
        <template #actions="{ item }">
          <button class="btn-icon" title="Editar" @click="handleEdit(item)">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
          </button>
          <button class="btn-icon text-red-400 hover:text-red-600 hover:bg-red-50" title="Borrar" @click="handlePreDelete(item)">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
          </button>
        </template>
      </DataTable>
    </div>
  </div>
</template>
