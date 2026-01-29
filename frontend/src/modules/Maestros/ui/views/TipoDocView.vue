<script setup lang="ts">
import { ref } from 'vue';
import { useTiposDoc } from '../../composables/useTiposDoc';
import TipoDocForm from './TipoDocForm.vue';
import PageHeader from '../../components/common/PageHeader.vue';
import DataTable from '../../components/common/DataTable.vue';
import type { TipoDoc } from '../../../domain/entities/TipoDoc';

// We need to pass edit/delete handlers to the list, but extracting the list component might be tricky if it doesn't support events.
// Let's just inline the list here or modify the existing component. Ideally, modify the existing component to emit events.

const { tiposDoc, loading, error, createTipoDoc, updateTipoDoc, deleteTipoDoc } = useTiposDoc();

const showForm = ref(false);
const isDeleteMode = ref(false);
const editingEntity = ref<TipoDoc | null>(null);

const handleNew = () => {
    editingEntity.value = null;
    isDeleteMode.value = false;
    error.value = null;
    showForm.value = true;
};

const handleEdit = (entity: TipoDoc) => {
    editingEntity.value = entity;
    isDeleteMode.value = false;
    error.value = null;
    showForm.value = true;
};

const handlePreDelete = (entity: TipoDoc) => {
    editingEntity.value = entity;
    isDeleteMode.value = true;
    error.value = null;
    showForm.value = true;
};

const handleConfirmDelete = async (id: number) => {
    try {
        await deleteTipoDoc(id);
        showForm.value = false;
        error.value = null;
    } catch (e) {
        // Error set in composable
    }
};

const handleSubmit = async (entity: TipoDoc) => {
    try {
        if (entity.id === 0) {
           await createTipoDoc(entity);
        } else {
           await updateTipoDoc(entity);
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
    <PageHeader title="Tipos de Documento" subtitle="Catálogo maestro de documentos de identidad.">
      <template #actions>
        <button class="btn btn-primary" @click="handleNew">
          + Nuevo
        </button>
      </template>
    </PageHeader>

    <div v-if="showForm" class="mb-8">
      <TipoDocForm 
        :model-value="(editingEntity as any)" 
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
          { key: 'nombre', label: 'Nombre' },
          { key: 'codigoArca', label: 'Cod. Arca', class: 'w-32' },
          { key: 'habilitado', label: 'Estado', class: 'w-32 text-center' },
        ]" 
        :items="tiposDoc" 
        actions
      >
        <template #cell-codigoArca="{ item }">
          <span v-if="item.codigoArca && item.codigoArca.value" class="px-2 py-1 text-xs font-mono bg-blue-100 text-blue-800 rounded-md">{{ item.codigoArca.value }}</span>
        </template>
        <template #cell-habilitado="{ item }">
          <span v-if="item.habilitado" class="text-xs font-bold text-green-700 bg-green-50 border border-green-200 px-2 py-0.5 rounded">HABILITADO</span>
          <span v-else class="text-xs font-bold text-gray-700 bg-gray-50 border border-gray-200 px-2 py-0.5 rounded">DESHABILITADO</span>
        </template>
            
        <template #actions="{ item }">
          <button class="btn-icon" title="Editar" @click="handleEdit(item as any)">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
          </button>
          <button class="btn-icon text-red-400 hover:text-red-600 hover:bg-red-50" title="Borrar" @click="handlePreDelete(item as any)">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
          </button>
        </template>
      </DataTable>
    </div>
  </div>
</template>
