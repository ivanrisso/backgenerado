<script setup lang="ts">
import UbicacionSelector from '@modules/Maestros/components/config/UbicacionSelector.vue';
</script>

<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">
          Ubicación Geográfica
        </h1>
        <p class="text-gray-600">
          Gestión de Países, Provincias y Localidades.
        </p>
      </div>
    </div>
    <UbicacionSelector />
  </div>
</template>
