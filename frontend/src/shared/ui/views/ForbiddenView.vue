<script setup lang="ts">
// Simple static view
</script>

<template>
  <div class="flex min-h-screen flex-col items-center justify-center bg-gray-100">
    <h1 class="text-6xl font-bold text-gray-800">
      403
    </h1>
    <p class="mt-4 text-xl text-gray-600">
      Acceso Denegado
    </p>
    <p class="mt-2 text-gray-500">
      No tienes permisos para ver esta página.
    </p>
    <router-link to="/" class="mt-6 rounded bg-blue-600 px-6 py-2 text-white hover:bg-blue-700">
      Volver al Inicio
    </router-link>
  </div>
</template>
