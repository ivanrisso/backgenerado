<script setup lang="ts">
import { useClientes } from '../composables/useClientes';
import { RouterLink } from 'vue-router';

const { clientes, loading, error, deleteCliente } = useClientes();

const confirmDelete = async (id: number) => {
    if (confirm('¿Estás seguro de que deseas eliminar este cliente?')) {
        await deleteCliente(id);
    }
};
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 tracking-tight">Clientes</h1>
        <p class="text-gray-500 mt-1">Gestiona tu cartera de clientes</p>
      </div>
      <RouterLink to="/clientes/new" class="btn btn-primary">
        Nuevo Cliente
      </RouterLink>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center p-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
    </div>

    <!-- Error State -->
    <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
      {{ error }}
    </div>

    <!-- Data Table -->
    <div v-if="!loading && !error && clientes.length > 0" class="card overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th scope="col" class="table-header">ID</th>
            <th scope="col" class="table-header">Nombre</th>
            <th scope="col" class="table-header">CUIT</th>
            <th scope="col" class="table-header">Email</th>
            <th scope="col" class="table-header text-right">Acciones</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="cliente in clientes" :key="cliente.id" class="hover:bg-gray-50 transition-colors">
            <td class="table-cell font-medium text-gray-900">#{{ cliente.id }}</td>
            <td class="table-cell">
              <div class="font-medium text-gray-900">{{ cliente.apellido }}, {{ cliente.nombre }}</div>
              <div v-if="cliente.razon_social" class="text-xs text-gray-500">{{ cliente.razon_social }}</div>
            </td>
            <td class="table-cell font-mono text-gray-600">{{ cliente.cuit?.format() || '-' }}</td>
            <td class="table-cell text-gray-600">{{ cliente.email?.toString() || '-' }}</td>
            <td class="table-cell text-right">
              <RouterLink :to="`/clientes/${cliente.id}/edit`" class="text-blue-600 hover:text-blue-900 font-medium text-sm mr-3">Editar</RouterLink>
              <button @click="confirmDelete(cliente.id)" class="text-red-600 hover:text-red-900 font-medium text-sm">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Empty State -->
    <div v-if="!loading && !error && clientes.length === 0" class="card p-12 text-center">
      <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
        <span class="text-3xl">👥</span>
      </div>
      <h3 class="text-lg font-medium text-gray-900">No hay clientes</h3>
      <p class="text-gray-500 mt-1 mb-6">Comienza creando tu primer cliente.</p>
      <RouterLink to="/clientes/new" class="btn btn-primary">
        Crear Cliente
      </RouterLink>
    </div>
  </div>
</template>

<style scoped>
/* Tailwind handles styling */
</style>
