<script setup lang="ts">
import Sidebar from '../components/Sidebar.vue';
</script>

<template>
  <div class="min-h-screen bg-gray-100 flex">
    <!-- Sidebar -->
    <Sidebar />

    <!-- Mobile Header (Visible on small screens) -->
    <div class="flex flex-col flex-1 min-w-0">
      <header class="md:hidden bg-white shadow-sm p-4 flex justify-between items-center">
        <h1 class="text-lg font-bold text-gray-800">
          Facturación
        </h1>
        <!-- Mobile toggle placeholder -->
      </header>

      <!-- Main Content (Shared) -->
      <main class="flex-1 p-6 overflow-y-auto">
        <router-view />
      </main>
    </div>
  </div>
</template>
