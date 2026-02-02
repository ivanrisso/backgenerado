<script setup lang="ts">
import { onMounted } from 'vue';
import { useClientes } from '@modules/Clientes/composables/useClientes';
import PageHeader from '@shared/ui/PageHeader.vue';
import DataTable from '@shared/ui/DataTable.vue';

const { clientesDeudores, isLoading, error, loadClientesDeudores } = useClientes();

const columns = [
    { key: 'id', label: 'ID', class: 'w-16' },
    { key: 'nombre', label: 'Nombre / Razón Social' },
    { key: 'cuit', label: 'CUIT' },
    { key: 'saldo', label: 'Saldo Deudor', class: 'text-right font-bold text-red-600' }
];

onMounted(async () => {
    await loadClientesDeudores();
});

const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('es-AR', { style: 'currency', currency: 'ARS' }).format(value);
};
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <PageHeader title="Clientes Deudores" subtitle="Listado de clientes con saldo pendiente de pago.">
      <template #actions>
        <button class="btn btn-secondary flex items-center gap-2" @click="loadClientesDeudores">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>
          Actualizar
        </button>
      </template>
    </PageHeader>

    <!-- List Area -->
    <div>
      <div v-if="isLoading" class="p-12 text-center text-blue-500">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-2" />
        Calculando saldos...
      </div>
      <div v-else-if="error" class="p-6 bg-red-50 text-red-600 rounded-lg border border-red-100">
        {{ error }}
      </div>

      <DataTable 
        v-else
        :columns="columns" 
        :items="clientesDeudores" 
      >
        <template #cell-id="{ item }">
          <span class="font-mono text-xs text-gray-500">#{{ item.id }}</span>
        </template>
        <template #cell-nombre="{ item }">
          <span class="font-medium text-gray-900">{{ item.razon_social || `${item.nombre} ${item.apellido}` }}</span>
          <div v-if="item.email" class="text-xs text-gray-400">
            {{ item.email }}
          </div>
        </template>
        <template #cell-cuit="{ item }">
          <span class="text-gray-500 font-mono">{{ item.cuit || '-' }}</span>
        </template>
        <template #cell-saldo="{ item }">
          <span class="text-red-600 font-bold block text-right">{{ formatCurrency(item.saldo) }}</span>
        </template>
      </DataTable>
      
      <div v-if="!isLoading && clientesDeudores.length === 0" class="p-8 text-center text-gray-500 italic">
        No se encontraron clientes con deuda.
      </div>
    </div>
  </div>
</template>
