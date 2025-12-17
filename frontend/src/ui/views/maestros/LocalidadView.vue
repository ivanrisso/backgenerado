<script setup lang="ts">
import { ref, watch, onMounted } from 'vue';
import { useUbicacion } from '../../composables/useUbicacion';
import LocalidadForm from './LocalidadForm.vue';
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
    showForm.value = true;
};

const handleEdit = (entity: Localidad) => {
    editingEntity.value = entity;
    showForm.value = true;
};

const handleDelete = async (id: number) => {
    if(confirm('¿Está seguro de eliminar este registro?')) {
        await deleteLocalidad(id);
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
    } catch (e) {
        // Error handled in composable
    }
};
</script>

<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Localidades</h1>
        <p class="text-gray-600">Catálogo de localidades por provincia.</p>
      </div>
      <button @click="handleNew" class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
        + Nueva
      </button>
    </div>

    <!-- Filtros -->
    <div class="bg-white p-4 rounded-lg shadow-sm border border-gray-200 grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">País</label>
            <select :value="selectedPaisId" @change="handlePaisChange(Number(($event.target as HTMLSelectElement).value))" class="block w-full border-gray-300 rounded-md shadow-sm">
                <option v-for="p in paises" :key="p.id" :value="p.id">{{ p.nombre }}</option>
            </select>
        </div>
        <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Provincia</label>
            <select :value="selectedProvinciaId" @change="handleProvinciaChange(Number(($event.target as HTMLSelectElement).value))" class="block w-full border-gray-300 rounded-md shadow-sm">
                <option :value="null">Seleccione...</option>
                <option v-for="p in provincias" :key="p.id" :value="p.id">{{ p.nombre }}</option>
            </select>
        </div>
    </div>

    <!-- Form Area -->
    <div v-if="showForm">
        <LocalidadForm 
            :modelValue="editingEntity" 
            :initialProvinciaId="selectedProvinciaId" 
            :initialPaisId="selectedPaisId"
            :provincias="provincias"
            :paises="paises"
            @submit="handleSubmit" 
            @cancel="showForm = false" 
            @change-pais="handlePaisChange"
        />
    </div>

    <div v-if="loading" class="text-blue-500">Cargando...</div>
    <div v-if="error" class="text-red-500">{{ error }}</div>

    <div v-if="!loading && !error" class="bg-white shadow overflow-hidden sm:rounded-md">
      <ul class="divide-y divide-gray-200">
        <li v-for="item in localidades" :key="item.id" class="px-6 py-4 flex items-center justify-between hover:bg-gray-50">
          <div>
            <span class="text-sm font-medium text-gray-900">{{ item.nombre }}</span>
            <span class="ml-2 text-xs text-gray-500">CP: {{ item.codPostal }}</span>
          </div>
          <div class="flex space-x-2">
             <button @click="handleEdit(item)" class="text-indigo-600 hover:text-indigo-900 text-sm font-medium">Editar</button>
             <button @click="handleDelete(item.id)" class="text-red-600 hover:text-red-900 text-sm font-medium">Borrar</button>
          </div>
        </li>
        <li v-if="localidades.length === 0" class="px-6 py-4 text-gray-500 italic">No hay registros para esta provincia</li>
      </ul>
    </div>
    <div v-if="!selectedProvinciaId" class="text-center py-8 text-gray-500">
        Seleccione un país y una provincia para ver las localidades.
    </div>
  </div>
</template>
