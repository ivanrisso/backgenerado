<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ReciboService } from '../../infrastructure/api/ReciboService';
import type { ReciboResponse } from '../../domain/models/Recibo';

const route = useRoute();
const router = useRouter();
const loading = ref(true);
const error = ref<string | null>(null);
const recibo = ref<ReciboResponse | null>(null);

const loadRecibo = async () => {
    const id = Number(route.params.id);
    if (!id) return;
    
    try {
        recibo.value = await ReciboService.getById(id);
    } catch (e: any) {
        error.value = 'Error al cargar el recibo. Posiblemente no exista o no sea válido.';
        console.error(e);
    } finally {
        loading.value = false;
    }
};

const goBack = () => {
    router.push({ name: 'recibos' });
};

const formatDate = (dateVal: string | undefined) => {
    if (!dateVal) return '';
    const [year, month, day] = dateVal.split('-');
    return `${day}/${month}/${year}`;
};

const formatMoney = (amount: number | undefined) => {
    if (amount === undefined) return '';
    return amount.toLocaleString('es-AR', { style: 'currency', currency: 'ARS' });
};

onMounted(() => {
    loadRecibo();
});
</script>

<template>
    <div class="min-h-screen bg-gray-50 pb-12">
        <header class="bg-white shadow">
            <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 flex items-center mb-4">
                <button @click="goBack" class="mr-4 text-gray-500 hover:text-gray-700">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                    </svg>
                </button>
                <h1 class="text-3xl font-bold text-gray-900">
                    Detalle de Recibo
                </h1>
            </div>
        </header>

        <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
            <div v-if="loading" class="flex justify-center py-12">
                <svg class="animate-spin h-8 w-8 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
            </div>

            <div v-else-if="error" class="bg-red-50 border-l-4 border-red-400 p-4">
                <p class="text-red-700">{{ error }}</p>
                <button @click="goBack" class="mt-2 text-red-600 font-bold hover:underline">Volver</button>
            </div>

            <div v-else-if="recibo" class="bg-white shadow overflow-hidden sm:rounded-lg">
                <div class="px-4 py-5 sm:px-6 flex justify-between">
                    <div>
                        <h3 class="text-lg leading-6 font-medium text-gray-900">
                            Recibo #{{ recibo.numero.toString().padStart(8, '0') }}
                        </h3>
                        <p class="mt-1 max-w-2xl text-sm text-gray-500">
                            Detalles del movimiento de tesorería.
                        </p>
                    </div>
                    <div class="text-right">
                         <span class="block text-sm text-gray-500">Fecha</span>
                         <span class="block text-lg font-bold text-gray-900">{{ formatDate(recibo.fecha_emision) }}</span>
                    </div>
                </div>
                <div class="border-t border-gray-200">
                    <dl>
                        <div class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                            <dt class="text-sm font-medium text-gray-500">Cliente</dt>
                            <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                {{ recibo.nombre_cliente || `ID: ${recibo.cliente_id}` }}
                            </dd>
                        </div>
                        <div class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                            <dt class="text-sm font-medium text-gray-500">Total</dt>
                            <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2 font-bold text-green-600">
                                {{ formatMoney(recibo.total) }}
                            </dd>
                        </div>
                        <div class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                            <dt class="text-sm font-medium text-gray-500">Saldo Disponible</dt>
                            <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                {{ formatMoney(recibo.saldo) }}
                            </dd>
                        </div>
                        <div class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                            <dt class="text-sm font-medium text-gray-500">Observaciones</dt>
                            <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                {{ recibo.observaciones || '-' }}
                            </dd>
                        </div>
                    </dl>
                </div>
            </div>
        </main>
    </div>
</template>
