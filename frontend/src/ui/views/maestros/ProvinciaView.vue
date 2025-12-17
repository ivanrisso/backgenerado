<script setup lang="ts">
import { ref, watch, onMounted } from 'vue';
import { useUbicacion } from '../../composables/useUbicacion';
import ProvinciaForm from './ProvinciaForm.vue';
import type { Provincia } from '../../../domain/entities/Provincia';

const { 
    paises, provincias, selectedPaisId, loading, error, 
    handlePaisChange, createProvincia, updateProvincia, deleteProvincia, loadPaises 
} = useUbicacion();

onMounted(() => {
    loadPaises();
});

const showForm = ref(false);
const editingEntity = ref<Provincia | null>(null);

// Auto-select first country logic
watch(paises, (newPaises) => {
    if (newPaises.length > 0 && selectedPaisId.value === null && newPaises[0]) {
        handlePaisChange(newPaises[0].id);
    }
});

const handleNew = () => {
    editingEntity.value = null;
    showForm.value = true;
};

const handleEdit = (entity: Provincia) => {
    editingEntity.value = entity;
    showForm.value = true;
};

const handleDelete = async (id: number) => {
    if(confirm('¿Está seguro de eliminar este registro?')) {
        await deleteProvincia(id);
    }
};

const handleSubmit = async (entity: Provincia) => {
    try {
        if (entity.id === 0) {
           await createProvincia(entity);
        } else {
           await updateProvincia(entity);
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
        <h1 class="text-2xl font-bold text-gray-900">Provincias</h1>
        <p class="text-gray-600">Catálogo de provincias por país.</p>
      </div>
      <button @click="handleNew" class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
        + Nueva
      </button>
    </div>

    <!-- Filtro Pais -->
    <div class="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
        <label class="block text-sm font-medium text-gray-700 mb-1">Filtrar por País</label>
        <select :value="selectedPaisId" @change="handlePaisChange(Number(($event.target as HTMLSelectElement).value))" class="block w-full md:w-1/3 border-gray-300 rounded-md shadow-sm">
            <option v-for="p in paises" :key="p.id" :value="p.id">{{ p.nombre }}</option>
        </select>
    </div>

    <!-- Form Area -->
    <div v-if="showForm">
        <ProvinciaForm 
            :modelValue="editingEntity" 
            :initialPaisId="selectedPaisId" 
            :paises="paises"
            @submit="handleSubmit" 
            @cancel="showForm = false" 
        />
    </div>

    <div v-if="loading" class="text-blue-500">Cargando...</div>
    <div v-if="error" class="text-red-500">{{ error }}</div>

    <div v-if="!loading && !error" class="bg-white shadow overflow-hidden sm:rounded-md">
      <ul class="divide-y divide-gray-200">
        <li v-for="item in provincias" :key="item.id" class="px-6 py-4 flex items-center justify-between hover:bg-gray-50">
          <span class="text-sm font-medium text-gray-900">{{ item.nombre }}</span>
          <div class="flex space-x-2">
             <button @click="handleEdit(item)" class="text-indigo-600 hover:text-indigo-900 text-sm font-medium">Editar</button>
             <button @click="handleDelete(item.id)" class="text-red-600 hover:text-red-900 text-sm font-medium">Borrar</button>
          </div>
        </li>
        <li v-if="provincias.length === 0" class="px-6 py-4 text-gray-500 italic">No hay registros para este país</li>
      </ul>
    </div>
  </div>
</template>
