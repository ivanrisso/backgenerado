<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useRecibos } from '../../composables/useRecibos';
import { useClientes } from '@modules/Clientes/composables/useClientes';

const router = useRouter();
const { recibos, loading, error, loadRecibos } = useRecibos();
const { clientes, loadClientes } = useClientes();

// Initialize Dates
const today = new Date();
const firstDayOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);

const formatDateForInput = (date: Date) => {
    return date.toISOString().split('T')[0];
};

// Filters State
const filters = ref({
    fechaDesde: formatDateForInput(firstDayOfMonth),
    fechaHasta: formatDateForInput(today),
    cliente_id: '',
    // nroComprobante: '' // Backend filter implementation might vary, let's stick to dates/clients for MVP
});

const clearFilters = () => {
    filters.value = {
        fechaDesde: formatDateForInput(firstDayOfMonth),
        fechaHasta: formatDateForInput(today),
        cliente_id: ''
    };
    applyFilters();
};

const applyFilters = () => {
    loadRecibos({
        fecha_desde: filters.value.fechaDesde,
        fecha_hasta: filters.value.fechaHasta,
        cliente_id: filters.value.cliente_id || undefined
    });
};

const navigateToCreate = () => {
    router.push({ name: 'recibo-nuevo' });
};

// Utils
const formatDate = (dateVal: string | undefined) => {
    if (!dateVal) return '';
    const [year, month, day] = dateVal.split('-');
    return `${day}/${month}/${year}`;
};

const formatMoney = (amount: number) => {
    return amount.toLocaleString('es-AR', { style: 'currency', currency: 'ARS' });
};

onMounted(async () => {
    await Promise.all([
        loadRecibos({
             fecha_desde: filters.value.fechaDesde,
             fecha_hasta: filters.value.fechaHasta
        }),
        loadClientes()
    ]);
});
</script>

<template>
  <div class="min-h-screen bg-gray-50 pb-12">
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
        <h1 class="text-3xl font-bold text-gray-900">
          Recibos de Cobranza
        </h1>
        <button 
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none transition-colors duration-150"
          @click="navigateToCreate"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Nuevo Recibo
        </button>
      </div>
    </header>

    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="bg-white shadow px-4 py-5 sm:rounded-lg sm:p-6">
        <!-- Filters Section -->
        <div class="mb-8 bg-gray-50 p-6 rounded-lg border border-gray-200">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-lg font-medium text-gray-700 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
              </svg>
              Filtros de Búsqueda
            </h2>
            <button 
              class="text-sm text-blue-600 hover:text-blue-800 hover:underline" 
              @click="clearFilters"
            >
              Limpiar filtros
            </button>
          </div>

          <div class="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-12 items-end">
            <!-- Date Range -->
            <div class="sm:col-span-2">
              <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Desde</label>
              <input v-model="filters.fechaDesde" type="date" class="block w-full shadow-sm sm:text-sm border-gray-300 rounded-md py-2 px-3 focus:ring-blue-500 focus:border-blue-500" @change="applyFilters">
            </div>
            <div class="sm:col-span-2">
              <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Hasta</label>
              <input v-model="filters.fechaHasta" type="date" class="block w-full shadow-sm sm:text-sm border-gray-300 rounded-md py-2 px-3 focus:ring-blue-500 focus:border-blue-500" @change="applyFilters">
            </div>

            <!-- Client Select -->
            <div class="sm:col-span-4 relative">
              <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Cliente</label>
              <select 
                  v-model="filters.cliente_id" 
                  class="block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  @change="applyFilters"
              >
                  <option value="">Todos</option>
                  <option v-for="c in clientes" :key="c.id" :value="c.id">
                      {{ c.razon_social || `${c.nombre} ${c.apellido}` }}
                  </option>
              </select>
            </div>

            <div class="sm:col-span-2">
                <button @click="applyFilters" class="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 font-bold py-2 px-4 rounded">
                    Filtrar
                </button>
            </div>
          </div>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="flex justify-center py-12">
          <svg class="animate-spin h-8 w-8 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
        </div>

        <!-- Error -->
        <div v-else-if="error" class="bg-red-50 border-l-4 border-red-400 p-4 mb-4">
          <div class="flex">
            <div class="flex-shrink-0">
               <!-- Error Icon -->
            </div>
            <div class="ml-3">
              <p class="text-sm text-red-700">
                {{ error }}
              </p>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else-if="recibos.length === 0" class="text-center py-12">
            <p class="text-gray-500">No se encontraron recibos con los filtros seleccionados.</p>
        </div>

        <!-- Table -->
        <div v-else class="flex flex-col">
          <div class="-my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
            <div class="py-2 align-middle inline-block min-w-full sm:px-6 lg:px-8">
              <div class="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg">
                <table class="min-w-full divide-y divide-gray-200">
                  <thead class="bg-gray-50">
                    <tr>
                      <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Fecha
                      </th>
                      <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Número
                      </th>
                      <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Cliente
                      </th>
                      <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Total
                      </th>
                      <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Saldo
                      </th>
                      <th scope="col" class="relative px-6 py-3">
                        <span class="sr-only">Acciones</span>
                      </th>
                    </tr>
                  </thead>
                  <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="r in recibos" :key="r.id" class="hover:bg-gray-50 transition-colors">
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {{ formatDate(r.fecha_emision) }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                         Recibo #{{ r.numero.toString().padStart(8, '0') }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {{ r.nombre_cliente || `Cliente #${r.cliente_id}` }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-bold">
                        {{ formatMoney(r.total) }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                         {{ formatMoney(r.saldo) }}
                      </td>

                      <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
                        <router-link :to="{ name: 'recibo-detalle', params: { id: r.id } }" class="text-blue-600 hover:text-blue-900" title="Ver Detalle">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                            </svg>
                        </router-link>
                        <router-link :to="{ name: 'recibo-imprimir', params: { id: r.id } }" class="text-gray-600 hover:text-gray-900" title="Imprimir">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
                            </svg>
                        </router-link>
                         <router-link :to="{ name: 'recibo-modificar', params: { id: r.id } }" class="text-indigo-600 hover:text-indigo-900" title="Modificar">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                            </svg>
                        </router-link>
                        <router-link :to="{ name: 'recibo-eliminar', params: { id: r.id } }" class="text-red-600 hover:text-red-900" title="Eliminar">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                            </svg>
                        </router-link>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>
