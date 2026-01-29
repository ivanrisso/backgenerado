<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useCondicionesTributarias } from '../../composables/useCondicionesTributarias';
import CondicionTributariaForm from './CondicionTributariaForm.vue';
import DataTable from '../../components/common/DataTable.vue';
import type { CondicionTributaria } from '../../../domain/entities/CondicionTributaria';

const props = defineProps<{
    tipoImpuestoId: number;
}>();

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

// Filtrar las condiciones por el ID del impuesto actual
const filteredCondiciones = computed(() => {
    return condicionesTributarias.value.filter(c => c.tipo_impuesto_id === props.tipoImpuestoId);
});

onMounted(() => {
    loadCondicionesTributarias();
});

const handleNew = () => {
    editingEntity.value = { 
        id: 0, 
        nombre: '', 
        tipo_impuesto_id: props.tipoImpuestoId 
    } as CondicionTributaria;
    isDeleteMode.value = false;
    showForm.value = true;
};

const handleEdit = (entity: CondicionTributaria) => {
    editingEntity.value = { ...entity };
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
        // Error manejado en composable
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
        // Error manejado en composable
    }
};
</script>

<template>
  <div class="space-y-4">
    <div class="flex justify-between items-center bg-white p-4 rounded-lg border border-gray-100 shadow-sm">
      <div>
        <h4 class="text-sm font-semibold text-gray-900">
          Condiciones ante este Impuesto
        </h4>
        <p class="text-xs text-gray-500">
          Defina las categorías de contribuyentes para este tributo.
        </p>
      </div>
      <button v-if="!showForm" class="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500" @click="handleNew">
        + Nueva Condición
      </button>
    </div>

    <div v-if="showForm">
      <CondicionTributariaForm 
        :model-value="editingEntity" 
        :is-delete-mode="isDeleteMode"
        :server-error="error"
        :fixed-tipo-impuesto-id="tipoImpuestoId"
        @submit="handleSubmit" 
        @delete="handleConfirmDelete"
        @cancel="handleCancel" 
      />
    </div>

    <div v-else>
      <div v-if="loading && filteredCondiciones.length === 0" class="flex justify-center p-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
      </div>

      <div v-if="!loading && filteredCondiciones.length === 0" class="text-center py-12 bg-gray-50 rounded-xl border-2 border-dashed border-gray-200">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">
          No hay condiciones
        </h3>
        <p class="mt-1 text-sm text-gray-500">
          Comience agregando una nueva condición para este impuesto.
        </p>
      </div>

      <DataTable 
        v-if="filteredCondiciones.length > 0"
        :columns="[
          { key: 'nombre', label: 'Nombre', class: 'font-medium' },
          { key: 'ambito', label: 'Ámbito', class: 'w-24 capitalize' },
          { key: 'descripcion', label: 'Descripción' }
        ]" 
        :items="filteredCondiciones" 
        actions
      >
        <template #actions="{ item }">
          <button class="p-1 text-blue-600 hover:bg-blue-50 rounded transition-colors" title="Editar" @click="handleEdit(item)">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
          </button>
          <button class="p-1 text-red-600 hover:bg-red-50 rounded transition-colors" title="Borrar" @click="handlePreDelete(item)">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
          </button>
        </template>
      </DataTable>
    </div>
  </div>
</template>
