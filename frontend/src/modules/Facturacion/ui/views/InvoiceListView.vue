<script setup lang="ts">
import { onMounted, ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useComprobantes } from '@modules/Facturacion/composables/useComprobantes';
import { useTiposComprobante } from '@modules/Maestros/composables/useTiposComprobante';
import { useClientes } from '@modules/Clientes/composables/useClientes';

const router = useRouter();
const { comprobantes, loading, error, loadComprobantes } = useComprobantes();
const { tiposComprobante, loadTiposComprobante } = useTiposComprobante();
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
    cliente: '',
    tipoComprobanteId: '',
    nroComprobante: '',
    letra: ''
});

// Autocomplete State
const showSuggestions = ref(false);
const clientSuggestions = computed(() => {
    const query = filters.value.cliente.toLowerCase();
    if (query.length < 3) return [];
    return clientes.value.filter(c => 
        c.nombre.toLowerCase().includes(query) || 
        c.apellido.toLowerCase().includes(query) ||
        (c.razon_social && c.razon_social.toLowerCase().includes(query))
    ).slice(0, 10); // Limit to 10
});

const selectSuggestion = (name: string) => {
    filters.value.cliente = name;
    showSuggestions.value = false;
};

// Handle Blur with Delay to allow click
const handleBlur = () => {
    setTimeout(() => {
        showSuggestions.value = false;
    }, 200);
};

// Navigation
const navigateToCreate = () => {
    router.push({ name: 'comprobante-nuevo' });
};

// Utils
const formatDate = (dateVal: string | Date | undefined) => {
    if (!dateVal) return '';
    return new Date(dateVal).toLocaleDateString('es-AR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
};

const formatMoney = (amount: any) => {
    if (amount && typeof amount === 'object' && 'amount' in amount) {
        return Number(amount.amount).toLocaleString('es-AR', { style: 'currency', currency: 'ARS' });
    }
    return Number(amount).toLocaleString('es-AR', { style: 'currency', currency: 'ARS' });
};

const getTipoComprobanteName = (id: number) => {
    const t = tiposComprobante.value.find(t => t.id === id);
    return t ? t.descripcion : id;
};

// Filter Logic
const filteredComprobantes = computed(() => {
    return comprobantes.value.filter(c => {
        // Filter by Date
        if (filters.value.fechaDesde) {
             const d = new Date(c.fecha_emision);
             const filterDate = new Date(filters.value.fechaDesde);
             if (d < filterDate) return false;
        }
        if (filters.value.fechaHasta) {
             const d = new Date(c.fecha_emision);
             const filterDate = new Date(filters.value.fechaHasta);
             // Ensure we include the selected day? Comparing dates directly.
             // If d is YYYY-MM-DD and filter is YYYY-MM-DD, > check is strict.
             // If c.fecha_emision has time, we might have issues.
             // Usually it's better to compare pure date strings or set filter time to 23:59:59.
             // For now assume date comparison works enough or loose "strictly greater".
             if (d > filterDate) return false; 
        }

        // Filter by Client Name (Case insensitive)
        if (filters.value.cliente) {
            if (!c.nombre_cliente.toLowerCase().includes(filters.value.cliente.toLowerCase())) return false;
        }

        // Filter by Type
        if (filters.value.tipoComprobanteId && filters.value.tipoComprobanteId !== '') {
            if (c.tipo_comprobante_id !== Number(filters.value.tipoComprobanteId)) return false;
        }
        
        // Filter by Number
        if (filters.value.nroComprobante) {
            if (!c.numero.toString().includes(filters.value.nroComprobante)) return false;
        }

        // Filter by Letter
        if (filters.value.letra) {
            const t = tiposComprobante.value.find(t => t.id === c.tipo_comprobante_id);
            if (t) {
                if (!t.descripcion.toLowerCase().includes(filters.value.letra.toLowerCase())) return false; 
            }
        }
        
        return true;
    });
});

onMounted(async () => {
    await Promise.all([
        loadComprobantes(),
        loadTiposComprobante(),
        loadClientes()
    ]);
});
</script>

<template>
  <div class="min-h-screen bg-gray-50 pb-12">
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
        <h1 class="text-3xl font-bold text-gray-900">
          Facturas
        </h1>
        <button 
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none transition-colors duration-150"
          @click="navigateToCreate"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Nueva Factura
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
              @click="filters = { fechaDesde: formatDateForInput(firstDayOfMonth), fechaHasta: formatDateForInput(today), cliente: '', tipoComprobanteId: '', nroComprobante: '', letra: '' }"
            >
              Limpiar filtros
            </button>
          </div>

          <div class="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-12 items-end">
            <!-- Date Range -->
            <div class="sm:col-span-2">
              <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Desde</label>
              <input v-model="filters.fechaDesde" type="date" class="block w-full shadow-sm sm:text-sm border-gray-300 rounded-md py-2 px-3 focus:ring-blue-500 focus:border-blue-500">
            </div>
            <div class="sm:col-span-2">
              <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Hasta</label>
              <input v-model="filters.fechaHasta" type="date" class="block w-full shadow-sm sm:text-sm border-gray-300 rounded-md py-2 px-3 focus:ring-blue-500 focus:border-blue-500">
            </div>

            <!-- Client with Autocomplete -->
            <div class="sm:col-span-3 relative">
              <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Cliente</label>
              <div class="relative rounded-md shadow-sm">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
                  </svg>
                </div>
                <input 
                  v-model="filters.cliente" 
                  type="text" 
                  class="focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 sm:text-sm border-gray-300 rounded-md py-2"
                  placeholder="Nombre"
                  autocomplete="off"
                  @focus="showSuggestions = true" 
                  @blur="handleBlur"
                  @input="showSuggestions = true"
                >
              </div>
              <!-- Suggestions Dropdown -->
              <div v-if="showSuggestions && clientSuggestions.length > 0" class="absolute z-10 w-full bg-white shadow-lg max-h-60 rounded-md py-1 text-base ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm mt-1">
                <ul tabindex="-1" role="listbox">
                  <li 
                    v-for="c in clientSuggestions" 
                    :key="c.id" 
                    class="cursor-pointer select-none relative py-2 pl-3 pr-9 hover:bg-blue-100 text-gray-900"
                    role="option"
                    @click="selectSuggestion(c.razon_social || `${c.nombre} ${c.apellido}`)"
                  >
                    <span class="block truncate font-normal">
                      {{ c.razon_social || `${c.nombre} ${c.apellido}` }}
                    </span>
                  </li>
                </ul>
              </div>
            </div>

            <!-- Type -->
            <div class="sm:col-span-2">
              <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Tipo</label>
              <select v-model="filters.tipoComprobanteId" class="block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
                <option value="">
                  Todos
                </option>
                <option v-for="t in tiposComprobante" :key="t.id" :value="t.id">
                  {{ t.descripcion }}
                </option>
              </select>
            </div>
                        
            <!-- Letter -->
            <div class="sm:col-span-1">
              <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Letra</label>
              <input v-model="filters.letra" type="text" class="block w-full shadow-sm sm:text-sm border-gray-300 rounded-md py-2 px-3 focus:ring-blue-500 focus:border-blue-500 text-center uppercase" placeholder="A" maxlength="1">
            </div>
                        
            <!-- Number -->
            <div class="sm:col-span-2">
              <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Nro</label>
              <input v-model="filters.nroComprobante" type="text" class="block w-full shadow-sm sm:text-sm border-gray-300 rounded-md py-2 px-3 focus:ring-blue-500 focus:border-blue-500">
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
              <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <p class="text-sm text-red-700">
                {{ error }}
              </p>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else-if="filteredComprobantes.length === 0" class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 011.414.586l4 4a1 1 0 01.586 1.414V19a2 2 0 01-2 2z" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">
            No se encontraron comprobantes
          </h3>
          <p class="mt-1 text-sm text-gray-500">
            Intente ajustar los filtros de búsqueda.
          </p>
          <div class="mt-6">
            <button 
              class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-blue-700 bg-blue-100 hover:bg-blue-200 focus:outline-none" 
              @click="filters = { fechaDesde: formatDateForInput(firstDayOfMonth), fechaHasta: formatDateForInput(today), cliente: '', tipoComprobanteId: '', nroComprobante: '', letra: '' }"
            >
              Ver todos
            </button>
          </div>
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
                        Comprobante
                      </th>
                      <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Cliente
                      </th>
                      <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Neto
                      </th>
                      <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        IVA
                      </th>
                      <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Total
                      </th>
                      <th scope="col" class="relative px-6 py-3">
                        <span class="sr-only">Ver</span>
                      </th>
                    </tr>
                  </thead>
                  <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="c in filteredComprobantes" :key="c.id" class="hover:bg-gray-50 transition-colors">
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {{ formatDate(c.fecha_emision) }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {{ getTipoComprobanteName(c.tipo_comprobante_id) }}
                        <span class="ml-2 px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">
                          {{ c.punto_venta.toString().padStart(4, '0') }}-{{ c.numero.toString().padStart(8, '0') }}
                        </span>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        <div class="font-medium">
                          {{ c.nombre_cliente }}
                        </div>
                        <div class="text-xs text-gray-500">
                          {{ c.cuit_cliente ? (typeof c.cuit_cliente === 'object' ? c.cuit_cliente.value : c.cuit_cliente) : 'S/C' }}
                        </div>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {{ formatMoney(c.total_neto) }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {{ formatMoney(c.total_iva) }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-bold">
                        {{ formatMoney(c.total) }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <a href="#" class="text-blue-600 hover:text-blue-900 flex justify-end items-center">
                          Ver
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                          </svg>
                        </a>
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
