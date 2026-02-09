<template>
    <div class="p-8 text-center max-w-2xl mx-auto mt-10 bg-white shadow rounded-lg">
        <h1 class="text-2xl font-bold mb-4 text-red-600">Eliminar Recibo</h1>
        
        <div v-if="loading" class="text-gray-600">Cargando datos...</div>
        
        <div v-else-if="recibo" class="space-y-4">
            <p class="text-gray-800 text-lg">¿Está seguro que desea eliminar el siguiente recibo?</p>
            
            <div class="bg-gray-100 p-4 rounded text-left">
                <p><strong>Nro:</strong> {{ recibo.numero }}</p>
                <p><strong>Fecha:</strong> {{ recibo.fecha_emision }}</p>
                <p><strong>Cliente ID:</strong> {{ recibo.cliente_id }}</p>
                <p v-if="recibo.nombre_cliente"><strong>Cliente:</strong> {{ recibo.nombre_cliente }}</p>
                <p><strong>Total:</strong> ${{ recibo.total }}</p>
            </div>

            <div class="flex justify-center space-x-4 mt-8">
                <button @click="$router.back()" class="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600">
                    Cancelar
                </button>
                <button @click="confirmDelete" class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700" :disabled="deleting">
                    {{ deleting ? 'Eliminando...' : 'Confirmar Eliminación' }}
                </button>
            </div>
            
             <div v-if="error" class="text-red-500 mt-2">
                {{ error }}
            </div>
        </div>
        
        <div v-else class="text-red-500">
            No se encontró el recibo.
            <br>
            <button @click="$router.back()" class="mt-4 px-4 py-2 bg-blue-600 text-white rounded">Volver</button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ReciboService } from '../../infrastructure/api/ReciboService';
import type { ReciboResponse } from '../../domain/models/Recibo';

const route = useRoute();
const router = useRouter();
const recibo = ref<ReciboResponse | null>(null);
const loading = ref(true);
const deleting = ref(false);
const error = ref<string | null>(null);

const id = Number(route.params.id);

onMounted(async () => {
    try {
        recibo.value = await ReciboService.getById(id);
    } catch (e) {
        error.value = "Error al cargar el recibo.";
        console.error(e);
    } finally {
        loading.value = false;
    }
});

const confirmDelete = async () => {
    if (!confirm("Esta acción no se puede deshacer. ¿Continuar?")) return;
    
    deleting.value = true;
    error.value = null;
    try {
        await ReciboService.delete(id);
        router.push({ name: 'recibos' });
    } catch (e) {
        error.value = "Error al eliminar el recibo.";
        console.error(e);
        deleting.value = false;
    }
};
</script>
