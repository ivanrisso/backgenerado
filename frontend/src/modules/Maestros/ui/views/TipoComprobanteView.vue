<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useTiposComprobante } from '@modules/Maestros/composables/useTiposComprobante';
import TipoComprobanteForm from './TipoComprobanteForm.vue';
import PageHeader from '@shared/ui/PageHeader.vue';
import DataTable from '@shared/ui/DataTable.vue';
import type { TipoComprobante } from '@domain/entities/TipoComprobante';

const { tiposComprobante, loading, error, loadTiposComprobante, createTipoComprobante, updateTipoComprobante, deleteTipoComprobante } = useTiposComprobante();

const showForm = ref(false);
const isDeleteMode = ref(false);
const editingEntity = ref<TipoComprobante | null>(null);

onMounted(() => {
    loadTiposComprobante();
});

const handleNew = () => {
    editingEntity.value = null;
    isDeleteMode.value = false;
    error.value = null;
    showForm.value = true;
};

const handleEdit = (entity: TipoComprobante) => {
    editingEntity.value = entity;
    isDeleteMode.value = false;
    error.value = null;
    showForm.value = true;
};

const handlePreDelete = (entity: TipoComprobante) => {
    editingEntity.value = entity;
    isDeleteMode.value = true;
    error.value = null;
    showForm.value = true;
};

const handleConfirmDelete = async (id: number) => {
    try {
        await deleteTipoComprobante(id);
        showForm.value = false;
        error.value = null;
    } catch (e) {
        // Error set in composable
    }
};

const handleSubmit = async (entity: TipoComprobante) => {
    try {
        if (entity.id === 0) {
           await createTipoComprobante(entity);
        } else {
           await updateTipoComprobante(entity);
        }
        showForm.value = false;
        error.value = null;
    } catch (e) {
        // Error handled in composable
    }
};

const handleCancel = () => {
    showForm.value = false;
    error.value = null;
    isDeleteMode.value = false;
};
</script>

<template>
  <div class="space-y-6">
    <PageHeader title="Tipos de Comprobante" subtitle="Catálogo de tipos de comprobantes.">
      <template #actions>
        <button class="btn btn-primary" @click="handleNew">
          + Nuevo
        </button>
      </template>
    </PageHeader>

    <div v-if="showForm" class="mb-8">
      <TipoComprobanteForm 
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
      <div v-if="error && !showForm" class="text-red-500 p-4">
        {{ error }}
      </div>

      <DataTable 
        v-if="!loading && (!error || showForm)"
        :columns="[
          { key: 'descripcion', label: 'Descripción' },
          { key: 'codigo', label: 'Código', class: 'w-24' },
          { key: 'es_fiscal', label: 'Fiscal', class: 'w-24 text-center' },
        ]" 
        :items="tiposComprobante" 
        actions
      >
        <template #cell-codigo="{ item }">
          <span class="px-2 py-1 text-xs font-mono bg-gray-100 text-gray-600 rounded-md">{{ item.codigo }}</span>
        </template>
        <template #cell-es_fiscal="{ item }">
          <span v-if="item.es_fiscal" class="text-xs font-bold text-green-700 bg-green-50 border border-green-200 px-2 py-0.5 rounded">SI</span>
          <span v-else class="text-xs text-gray-400">NO</span>
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
