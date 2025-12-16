<script setup lang="ts">
import MainLayout from '../layouts/MainLayout.vue';
import TipoDocList from '../components/config/TipoDocList.vue';
import UbicacionSelector from '../components/config/UbicacionSelector.vue';
// We could add TipoTel/TipoDom list here too if requested, but let's start with these major ones.
</script>

<template>
  <MainLayout>
    <div class="space-y-6">
      <h1 class="text-3xl font-bold text-gray-900">Configuración del Sistema</h1>
      <p class="text-gray-600">Gestión de catálogos y parámetros maestros.</p>

      <div class="grid grid-cols-1 gap-6">
        <TipoDocList />
        <UbicacionSelector />
      </div>
    </div>
  </MainLayout>
</template>
