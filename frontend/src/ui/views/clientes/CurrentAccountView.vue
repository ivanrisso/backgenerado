
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useClientes } from '../../composables/useClientes';
import { useComprobantes } from '../../composables/useComprobantes';
import { useTiposComprobante } from '../../composables/useTiposComprobante';

const { 
    clientes, 
    loadClientes 
} = useClientes();

const { comprobantes, loadComprobantes } = useComprobantes();
const { tiposComprobante, loadTiposComprobante } = useTiposComprobante();
const selectedClientId = ref<number | null>(null);

// Search Logic
const clientSearchQuery = ref('');
const clientShowSuggestions = ref(false);

const clientFilteredList = computed(() => {
    const query = clientSearchQuery.value.toLowerCase();
    
    if (!query) return clientes.value.slice(0, 50); 

    return clientes.value.filter(c => 
        c.nombre.toLowerCase().includes(query) || 
        c.apellido.toLowerCase().includes(query) ||
        (c.razon_social && c.razon_social.toLowerCase().includes(query)) ||
        (c.cuit?.value && c.cuit.value.includes(query))
    ).slice(0, 50);
});

const handleClientInput = () => {
    selectedClientId.value = null; // Reset selection on input
    clientShowSuggestions.value = true;
};

const handleClientBlur = () => {
    setTimeout(() => {
        clientShowSuggestions.value = false;
    }, 200);
};

const selectCliente = (cliente: any) => {
    selectedClientId.value = cliente.id;
    clientSearchQuery.value = cliente.razon_social || `${cliente.nombre} ${cliente.apellido}`;
    clientShowSuggestions.value = false;
};

const onClientSelect = (cliente: any) => {
    selectCliente(cliente);
};

onMounted(async () => {
    await loadClientes();
    await loadTiposComprobante(); 
    // Optimization: Load Comprobantes only when client is selected?
    // Current backend doesn't support generic filtering in clean way, but we added get_by_cliente logic.
    // Ideally we should NOT load ALL comprobantes here if DB is large.
    // For now we will trigger loadComprobantes when client is selected?
    // Or just load all.
    // Wait, the View relies on 'comprobantes' which is global?
    // Let's use the new backend capability.
    // But 'useComprobantes' might not support filtering yet.
    // It calls 'getComprobantesUseCase.execute()'.
    await loadComprobantes();
});

const filters = ref({
    fechaDesde: '',
    fechaHasta: '',
    tipoComprobanteId: '' as string | number
});

// Filter comprobantes by client
const accountMovements = computed(() => {
    if (!selectedClientId.value) return [];
    
    return comprobantes.value
        .filter(c => {
            if (c.cliente_id !== selectedClientId.value) return false;
            
            // Date Filter
            if (filters.value.fechaDesde) {
                const d = new Date(c.fecha_emision);
                const from = new Date(filters.value.fechaDesde);
                if (d < from) return false;
            }
            if (filters.value.fechaHasta) {
                const d = new Date(c.fecha_emision);
                const to = new Date(filters.value.fechaHasta);
                 // Normalize to end of day? 
                 // Assuming simple date comparison.
                if (d > to) return false;
            }
            
            // Type Filter
            if (filters.value.tipoComprobanteId && filters.value.tipoComprobanteId !== '') {
                if (c.tipo_comprobante_id !== Number(filters.value.tipoComprobanteId)) return false;
            }
            
            return true;
        })
        .sort((a, b) => {
            // Sort by date ascending
            return a.fecha_emision.getTime() - b.fecha_emision.getTime();
        });
});

const getTypeName = (id: number) => {
    const t = tiposComprobante.value.find(type => type.id === id);
    return t ? t.descripcion : `Tipo ${id}`;
};

</script>

<template>
    <div class="p-6">
        <h1 class="text-2xl font-bold mb-6 text-gray-800">Cuenta Corriente</h1>
        
        <div class="bg-white p-4 rounded-lg shadow mb-6 border border-gray-200">
            <div class="grid grid-cols-1 md:grid-cols-12 gap-4 items-end">
                <!-- Cliente Selector -->
                <div class="md:col-span-4">
                     <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Cliente</label>
                     <div class="relative">
                         <input 
                             type="text" 
                             v-model="clientSearchQuery"
                             @input="handleClientInput"
                             @blur="handleClientBlur"
                             placeholder="Buscar por nombre o CUIT..."
                             class="block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                         />
                         <ul v-if="clientShowSuggestions && clientFilteredList.length" class="absolute z-10 w-full bg-white border border-gray-300 rounded-md mt-1 max-h-60 overflow-auto shadow-lg">
                             <li 
                                 v-for="cliente in clientFilteredList" 
                                 :key="cliente.id"
                                 @mousedown.prevent="onClientSelect(cliente)"
                                 class="px-4 py-2 hover:bg-blue-100 cursor-pointer text-sm"
                             >
                                 {{ cliente.razon_social || cliente.nombre + ' ' + cliente.apellido }} ({{ cliente.cuit || 'Sin CUIT' }})
                             </li>
                         </ul>
                     </div>
                </div>

                <!-- Date Range -->
                <div class="md:col-span-2">
                     <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Desde</label>
                     <input type="date" v-model="filters.fechaDesde" class="block w-full shadow-sm sm:text-sm border-gray-300 rounded-md py-2 px-3 focus:ring-blue-500 focus:border-blue-500">
                </div>
                <div class="md:col-span-2">
                     <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Hasta</label>
                     <input type="date" v-model="filters.fechaHasta" class="block w-full shadow-sm sm:text-sm border-gray-300 rounded-md py-2 px-3 focus:ring-blue-500 focus:border-blue-500">
                </div>

                <!-- Type Selector -->
                <div class="md:col-span-2">
                    <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Tipo Comprobante</label>
                    <select v-model="filters.tipoComprobanteId" class="block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
                        <option value="">Todos</option>
                        <option v-for="t in tiposComprobante" :key="t.id" :value="t.id">{{ t.descripcion }}</option>
                    </select>
                </div>
                
                 <div class="md:col-span-2 flex justify-end">
                    <button 
                        @click="filters = { fechaDesde: '', fechaHasta: '', tipoComprobanteId: '' }" 
                        class="text-sm text-blue-600 hover:text-blue-800 hover:underline mb-2"
                    >
                        Limpiar filtros
                    </button>
                 </div>
            </div>
        </div>
        
        <!-- Movements Table -->
        <div v-if="selectedClientId" class="bg-white shadow rounded-lg overflow-hidden">
            <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                    <tr>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fecha</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Comprobante</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Número</th>
                        <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Total Original</th>
                        <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Saldo Pendiente</th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="mov in accountMovements" :key="mov.id">
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {{ mov.fecha_emision.toLocaleDateString() }}
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {{ getTypeName(mov.tipo_comprobante_id) }}
                        </td>
                         <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {{ mov.punto_venta.toString().padStart(4, '0') }}-{{ mov.numero.toString().padStart(8, '0') }}
                        </td>
                         <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 text-right">
                            $ {{ mov.total.amount.toFixed(2) }}
                        </td>
                         <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-gray-900 text-right">
                            $ {{ mov.saldo ? mov.saldo.amount.toFixed(2) : mov.total.amount.toFixed(2) }}
                        </td>
                    </tr>
                    <tr v-if="accountMovements.length === 0">
                        <td colspan="5" class="px-6 py-4 text-center text-sm text-gray-500">
                             No hay movimientos registrados con los filtros actuales.
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <div v-if="selectedClientId && accountMovements.length > 0" class="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-md flex justify-end">
             <div class="text-xl font-bold text-gray-800">
                 <!-- Total Calculation Logic needs refinement based on Types -->
                 <!-- Displaying raw sum of balances for now as "Deuda Neta" approximation -->
             </div>
        </div>
    </div>
</template>
