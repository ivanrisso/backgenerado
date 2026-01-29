<script setup lang="ts">
import { ref, watch, onMounted } from 'vue';
import { useUbicacion } from '../../composables/useUbicacion';
import LocalidadForm from './LocalidadForm.vue';
import PageHeader from '../../components/common/PageHeader.vue';
import DataTable from '../../components/common/DataTable.vue';
import type { Localidad } from '../../../domain/entities/Localidad';

const { 
    paises, provincias, localidades, 
    selectedPaisId, selectedProvinciaId, 
    loading, error, 
    handlePaisChange, handleProvinciaChange,
    createLocalidad, updateLocalidad, deleteLocalidad, loadPaises
} = useUbicacion();

onMounted(() => {
    loadPaises();
});

const showForm = ref(false);
const isDeleteMode = ref(false);
const editingEntity = ref<Localidad | null>(null);

// Auto-select logic
watch(paises, (newPaises) => {
    if (newPaises.length > 0 && selectedPaisId.value === null && newPaises[0]) {
        handlePaisChange(newPaises[0].id);
    }
});

watch(provincias, (newProvincias) => {
    if (newProvincias.length > 0 && selectedProvinciaId.value === null && newProvincias[0]) {
        handleProvinciaChange(newProvincias[0].id);
    }
});

const handleNew = () => {
    editingEntity.value = null;
    isDeleteMode.value = false;
    error.value = null;
    showForm.value = true;
};

const handleEdit = (entity: Localidad) => {
    editingEntity.value = entity;
    isDeleteMode.value = false;
    error.value = null;
    showForm.value = true;
};

const handlePreDelete = (entity: Localidad) => {
    editingEntity.value = entity;
    isDeleteMode.value = true;
    error.value = null;
    showForm.value = true;
};

const handleConfirmDelete = async (id: number) => {
    try {
        await deleteLocalidad(id);
        showForm.value = false;
        error.value = null;
    } catch (e) {
        // Error set in composable
    }
};

const handleSubmit = async (entity: Localidad) => {
    try {
        if (entity.id === 0) {
           await createLocalidad(entity);
        } else {
           await updateLocalidad(entity);
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
    <PageHeader title="Localidades" subtitle="Catálogo de localidades por provincia.">
      <template #actions>
        <button class="btn btn-primary" @click="handleNew">
          + Nueva
        </button>
      </template>
    </PageHeader>

    <!-- Filtros -->
    <div v-if="!showForm" class="bg-white p-4 rounded-lg shadow-sm border border-gray-200 grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">País</label>
        <select :value="selectedPaisId" class="input-field" @change="handlePaisChange(Number(($event.target as HTMLSelectElement).value))">
          <option v-for="p in paises" :key="p.id" :value="p.id">
            {{ p.nombre }}
          </option>
        </select>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Provincia</label>
        <select :value="selectedProvinciaId" class="input-field" @change="handleProvinciaChange(Number(($event.target as HTMLSelectElement).value))">
          <option :value="null">
            Seleccione...
          </option>
          <option v-for="p in provincias" :key="p.id" :value="p.id">
            {{ p.nombre }}
          </option>
        </select>
      </div>
    </div>

    <!-- Form Area -->
    <div v-if="showForm" class="mb-8">
      <LocalidadForm 
        :model-value="editingEntity" 
        :initial-provincia-id="selectedProvinciaId" 
        :initial-pais-id="selectedPaisId"
        :provincias="provincias"
        :paises="paises"
        :is-delete-mode="isDeleteMode"
        :server-error="error"
        @submit="handleSubmit" 
        @delete="handleConfirmDelete"
        @cancel="handleCancel" 
        @change-pais="handlePaisChange"
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
          { key: 'codPostal', label: 'C. Postal', class: 'w-32' },
        ]" 
        :items="localidades" 
        actions
      >
        <template #empty>
          <span v-if="!selectedProvinciaId">Seleccione un país y una provincia para ver las localidades.</span>
          <span v-else>No hay registros para esta provincia.</span>
        </template>
            
        <template #cell-codPostal="{ item }">
          <span class="font-mono text-gray-600">{{ item.codPostal }}</span>
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
