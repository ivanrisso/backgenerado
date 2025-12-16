<script setup lang="ts">
import { useUbicacion } from '../../composables/useUbicacion';

const { 
  paises, provincias, localidades, 
  selectedPaisId, selectedProvinciaId,
  loading, error,
  handlePaisChange, handleProvinciaChange 
} = useUbicacion();
</script>

<template>
  <div class="bg-white p-6 rounded-lg shadow-md">
    <h2 class="text-xl font-semibold mb-4 text-gray-800">Ubicación (Cascada)</h2>

    <div v-if="loading" class="mb-4 text-blue-500 text-sm">Cargando datos...</div>
    <div v-if="error" class="mb-4 text-red-500 text-sm">{{ error }}</div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      
      <!-- Pais -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">País</label>
        <select 
          :value="selectedPaisId"
          @change="e => handlePaisChange(Number((e.target as HTMLSelectElement).value))"
          class="w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
        >
          <option value="">Seleccione un país</option>
          <option v-for="p in paises" :key="p.id" :value="p.id">
            {{ p.nombre }} ({{ p.codigo.value }})
          </option>
        </select>
      </div>

      <!-- Provincia -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Provincia</label>
        <select 
          :value="selectedProvinciaId"
          @change="e => handleProvinciaChange(Number((e.target as HTMLSelectElement).value))"
          :disabled="!selectedPaisId"
          class="w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 disabled:bg-gray-100 disabled:text-gray-400"
        >
          <option value="">Seleccione una provincia</option>
          <option v-for="pr in provincias" :key="pr.id" :value="pr.id">
            {{ pr.nombre }}
          </option>
        </select>
      </div>

      <!-- Localidad -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Localidad</label>
        <select 
          :disabled="!selectedProvinciaId"
          class="w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 disabled:bg-gray-100 disabled:text-gray-400"
        >
          <option value="">Seleccione una localidad</option>
          <option v-for="l in localidades" :key="l.id" :value="l.id">
            {{ l.nombre }} (CP: {{ l.codPostal }})
          </option>
        </select>
      </div>

    </div>
  </div>
</template>
