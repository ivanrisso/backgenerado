<template>
    <div class="print-container bg-white">
        <!-- Toolbar (No Impullso) -->
        <div class="no-print p-4 bg-gray-100 flex justify-between items-center mb-8 shadow">
            <h1 class="text-xl font-bold text-gray-700">Vista Preliminar de Impresión</h1>
            <div class="space-x-4">
                <button @click="$router.back()" class="px-4 py-2 bg-gray-500 text-white rounded">Volver</button>
                <button @click="print" class="px-4 py-2 bg-blue-600 text-white rounded font-bold">Imprimir</button>
            </div>
        </div>

        <div v-if="loading" class="p-8 text-center text-gray-500">Cargando Recibo...</div>
        
        <div v-else-if="recibo" class="max-w-4xl mx-auto p-8 border border-gray-200 shadow-sm print:border-0 print:shadow-none">
            <!-- Header -->
            <div class="flex justify-between items-start mb-8 border-b pb-4">
                <div>
                    <h2 class="text-3xl font-bold text-gray-900">RECIBO</h2>
                    <p class="text-gray-500 mt-1">X (Documento No Válido como Factura)</p>
                </div>
                <div class="text-right">
                    <p class="text-xl font-bold">N° {{ String(recibo.punto_venta || 0).padStart(4, '0') }}-{{ String(recibo.numero).padStart(8, '0') }}</p>
                    <p class="text-gray-600">Fecha: {{ formatDate(recibo.fecha_emision) }}</p>
                </div>
            </div>

            <!-- Cliente -->
            <div class="mb-8 p-4 bg-gray-50 print:bg-white rounded border">
                <h3 class="text-xs font-bold text-gray-500 uppercase mb-2">Recibimos de:</h3>
                <p class="text-lg font-bold">{{ recibo.nombre_cliente || `Cliente #${recibo.cliente_id}` }}</p>
                <p class="text-gray-600 text-sm mt-1" v-if="recibo.observaciones">
                    <span class="font-bold">Observaciones:</span> {{ recibo.observaciones }}
                </p>
            </div>

            <!-- Totales -->
            <div class="mb-8">
                <div class="flex justify-between items-center border-t border-b py-4">
                    <span class="text-xl font-bold">TOTAL RECIBIDO</span>
                    <span class="text-2xl font-bold">{{ formatMoney(recibo.total) }}</span>
                </div>
                <div class="text-right mt-2 text-sm text-gray-500">
                    Son: {{ formatMoney(recibo.total) }} pesos
                </div>
            </div>

            <!-- Firma Dummy -->
            <div class="mt-20 pt-8 border-t border-gray-400 w-1/3 text-center mx-auto print:block hidden">
                <p class="text-sm text-gray-600">Firma y Aclaración</p>
            </div>

            <div class="mt-20 text-center text-xs text-gray-400">
                <p>Comprobante generado electrónicamente</p>
            </div>
        </div>
        
         <div v-else class="p-8 text-center text-red-500">
            Error al cargar recibo.
        </div>
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { ReciboService } from '../../infrastructure/api/ReciboService';
import type { ReciboResponse } from '../../domain/models/Recibo';

const route = useRoute();
const recibo = ref<ReciboResponse | null>(null);
const loading = ref(true);

const id = Number(route.params.id);

onMounted(async () => {
    try {
        recibo.value = await ReciboService.getById(id);
    } catch (e) {
        console.error(e);
    } finally {
        loading.value = false;
    }
});

const print = () => {
    window.print();
};

const formatMoney = (value: number) => {
    return new Intl.NumberFormat('es-AR', { style: 'currency', currency: 'ARS' }).format(value);
};

const formatDate = (dateStr: string) => {
    if (!dateStr) return '-';
    const [year, month, day] = dateStr.split('-');
    return `${day}/${month}/${year}`;
};
</script>

<style scoped>
@media print {
    .no-print {
        display: none !important;
    }
    .print-container {
        padding: 0;
        background: white;
    }
}
</style>
