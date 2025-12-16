<script setup lang="ts">
import { useTiposDoc } from '../../composables/useTiposDoc';

const { tiposDoc, loading, error } = useTiposDoc();
</script>

<template>
  <div class="bg-white p-6 rounded-lg shadow-md">
    <h2 class="text-xl font-semibold mb-4 text-gray-800">Tipos de Documento</h2>

    <div v-if="loading" class="text-blue-500">Cargando...</div>
    <div v-if="error" class="text-red-500">{{ error }}</div>

    <ul v-if="!loading && !error" class="space-y-2">
      <li v-for="td in tiposDoc" :key="td.id" class="p-3 bg-gray-50 rounded border border-gray-200 flex justify-between items-center">
        <div>
          <span class="font-medium text-gray-900">{{ td.nombre }}</span>
          <span class="ml-2 px-2 py-0.5 text-xs bg-blue-100 text-blue-800 rounded-full">Arca: {{ td.codigoArca.value }}</span>
        </div>
        <span :class="td.habilitado ? 'text-green-600' : 'text-gray-400'" class="text-sm">
          {{ td.habilitado ? 'Habilitado' : 'Deshabilitado' }}
        </span>
      </li>
    </ul>
    <div v-if="!loading && tiposDoc.length === 0" class="text-gray-500 italic">No hay tipos de documento.</div>
  </div>
</template>
