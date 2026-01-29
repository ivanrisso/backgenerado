<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useClientes } from '../../composables/useClientes';
import { useDomicilios } from '../../composables/useDomicilios';
import TelefonoManager from './TelefonoManager.vue';

const route = useRoute();
const router = useRouter();
const clienteId = Number(route.params.clienteId);
const domicilioId = Number(route.params.domicilioId);

const { currentCliente, loadClienteById, isLoading: loadingCliente } = useClientes();
const { currentDomicilio, loadDomicilioById, loading: loadingDomicilio } = useDomicilios();

const initializing = ref(true);

onMounted(async () => {
    const promises = [];
    if (clienteId) promises.push(loadClienteById(clienteId));
    if (domicilioId) promises.push(loadDomicilioById(domicilioId));
    
    if (promises.length > 0) {
        await Promise.all(promises);
    }
    initializing.value = false;
});

// ... inside template ...
// <div v-if="initializing || loadingCliente || loadingDomicilio" ...>

const goBack = () => {
    // Navigate back to the client list, restoring the edit mode state
    router.push({ 
        name: 'clientes', 
        query: { 
            edit: clienteId.toString(), 
            tab: 'domicilios' 
        } 
    });
};
</script>

<template>
  <div class="min-h-screen bg-gray-50 font-sans text-gray-900 pb-10">
    <!-- Top Navigation Bar / Header -->
    <div class="bg-white/80 backdrop-blur-md border-b border-gray-200 sticky top-0 z-10">
      <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <h1 class="text-xl font-semibold tracking-tight text-gray-900 truncate">
          Gestionar Teléfonos
        </h1>
        <button class="text-blue-600 hover:text-blue-500 font-medium text-[17px] flex items-center transition-colors" @click="goBack">
          <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7" />
          </svg>
          Atrás
        </button>
      </div>
    </div>

    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 mt-8 space-y-8">
      <!-- Context Header Cards -->
      <div v-if="currentCliente || currentDomicilio" class="space-y-2">
        <h2 class="text-xs font-semibold uppercase tracking-wider text-gray-500 ml-4 mb-2">
          Información del Contexto
        </h2>
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden divide-y divide-gray-100">
          <div v-if="currentCliente" class="p-4 flex flex-col">
            <span class="text-xs text-gray-400 font-medium uppercase tracking-wide">Cliente</span>
            <div class="font-medium text-[17px] text-gray-900 mt-0.5">
              {{ currentCliente.nombre }} {{ currentCliente.apellido }}
              <span v-if="currentCliente.razon_social" class="text-gray-500 text-sm font-normal">({{ currentCliente.razon_social }})</span>
            </div>
            <div class="text-[15px] text-gray-500">
              {{ currentCliente.cuit?.value || currentCliente.cuit }}
            </div>
          </div>
          <div v-if="currentDomicilio" class="p-4 flex flex-col">
            <span class="text-xs text-gray-400 font-medium uppercase tracking-wide">Domicilio</span>
            <div class="font-medium text-[17px] text-gray-900 mt-0.5">
              {{ currentDomicilio.calle }} {{ currentDomicilio.numero }}
            </div>
          </div>
        </div>
      </div>

      <!-- Content Area -->
      <div v-if="initializing || loadingCliente || loadingDomicilio" class="flex justify-center items-center py-20">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-400" />
      </div>

      <TelefonoManager v-else :domicilio-id="domicilioId" />
    </div>
  </div>
</template>
