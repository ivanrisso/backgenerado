<script setup lang="ts">
import { useTiposContacto } from '../../composables/useTiposContacto';

const { tiposDom, tiposTel, loading, error } = useTiposContacto();
</script>

<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-2xl font-bold text-gray-900">Tipos de Contacto</h1>
      <p class="text-gray-600">Catálogos de teléfonos y domicilios.</p>
    </div>

    <div v-if="loading" class="text-blue-500">Cargando...</div>
    <div v-if="error" class="text-red-500">{{ error }}</div>

    <div v-if="!loading && !error" class="grid grid-cols-1 md:grid-cols-2 gap-6">
      
      <!-- Tipos de Teléfono -->
      <div class="bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-lg font-semibold mb-4 text-gray-800 border-b pb-2">Tipos de Teléfono</h2>
        <ul class="space-y-2">
          <li v-for="tel in tiposTel" :key="tel.id" class="flex items-center text-gray-700">
            <span class="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
            {{ tel.nombre }}
          </li>
          <li v-if="tiposTel.length === 0" class="text-gray-400 italic">No hay registros</li>
        </ul>
      </div>

      <!-- Tipos de Domicilio -->
      <div class="bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-lg font-semibold mb-4 text-gray-800 border-b pb-2">Tipos de Domicilio</h2>
        <ul class="space-y-2">
          <li v-for="dom in tiposDom" :key="dom.id" class="flex items-center text-gray-700">
            <span class="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
            {{ dom.nombre }}
          </li>
          <li v-if="tiposDom.length === 0" class="text-gray-400 italic">No hay registros</li>
        </ul>
      </div>

    </div>
  </div>
</template>
