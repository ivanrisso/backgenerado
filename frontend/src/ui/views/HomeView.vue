<script setup lang="ts">
import MinimalLineChart from '../components/MinimalLineChart.vue'
</script>

<template>
  <div class="space-y-8">
    <!-- Header -->
    <div>
      <h1 class="text-3xl font-bold text-gray-900 tracking-tight">Bienvenido de nuevo</h1>
      <p class="text-gray-500 mt-2">Resumen de la actividad reciente de facturación.</p>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="card p-6">
        <h3 class="text-sm font-medium text-gray-500 mb-4">Total Facturado (Mes)</h3>
        <div class="text-3xl font-bold text-gray-900 mb-2">$ 8.450.200</div>
        <div class="text-sm text-green-600 flex items-center font-medium">
          <span class="mr-1">↑</span> 12.5% vs mes anterior
        </div>
      </div>
      
      <div class="card p-6">
        <h3 class="text-sm font-medium text-gray-500 mb-4">Comprobantes Emitidos</h3>
        <div class="text-3xl font-bold text-gray-900 mb-2">142</div>
        <div class="text-sm text-gray-500 flex items-center">
          Sin cambios significativos
        </div>
      </div>

      <div class="card p-6">
        <h3 class="text-sm font-medium text-gray-500 mb-4">Clientes Nuevos</h3>
        <div class="text-3xl font-bold text-gray-900 mb-2">15</div>
        <div class="text-sm text-green-600 flex items-center font-medium">
          <span class="mr-1">↑</span> 4 nuevos esta semana
        </div>
      </div>
    </div>

    <!-- Charts Section -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Chart 1: Evolution -->
      <div class="card p-6">
        <div class="flex items-center justify-between mb-6">
          <h3 class="font-semibold text-gray-900">Evolución de Ventas</h3>
          <select class="text-sm border-none bg-gray-50 rounded-md px-2 py-1 text-gray-600 outline-none cursor-pointer hover:bg-gray-100">
            <option>Últimos 7 días</option>
            <option>Último mes</option>
          </select>
        </div>
        <MinimalLineChart :data="[120, 190, 150, 220, 180, 250, 310]" />
      </div>

      <!-- Chart 2: Activity -->
      <div class="card p-6">
         <div class="flex items-center justify-between mb-6">
          <h3 class="font-semibold text-gray-900">Nuevos Clientes</h3>
        </div>
        <MinimalLineChart :data="[5, 8, 12, 5, 15, 10, 18]" color="#34d399" label="Clientes" />
      </div>
    </div>
  </div>
</template>
