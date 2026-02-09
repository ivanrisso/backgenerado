<template>
    <div class="p-8 max-w-2xl mx-auto mt-10 bg-white shadow rounded-lg">
        <h1 class="text-2xl font-bold mb-6 text-indigo-600">Modificar Recibo</h1>
        
        <div v-if="loading" class="text-gray-600">Cargando datos...</div>
        
        <div v-else-if="recibo" class="space-y-6">
            <!-- Info no editable -->
            <div class="grid grid-cols-2 gap-4 bg-gray-50 p-4 rounded text-sm">
                <div>
                    <label class="font-bold text-gray-500">Número:</label>
                    <p>{{ recibo.numero }}</p>
                </div>
                <div>
                    <label class="font-bold text-gray-500">Cliente:</label>
                    <p>{{ recibo.nombre_cliente || recibo.cliente_id }}</p>
                </div>
                <div>
                    <label class="font-bold text-gray-500">Total:</label>
                    <p>${{ recibo.total }}</p>
                </div>
            </div>

            <!-- Form -->
            <form @submit.prevent="save">
                <div class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Fecha Emisión</label>
                        <input v-model="form.fecha_emision" type="date" required 
                               class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                    </div>
                    
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Observaciones</label>
                        <textarea v-model="form.observaciones" rows="3" 
                                  class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"></textarea>
                    </div>
                </div>

                <div class="flex justify-end space-x-4 mt-8">
                    <button type="button" @click="$router.back()" class="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600">
                        Cancelar
                    </button>
                    <button type="submit" class="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700" :disabled="saving">
                        {{ saving ? 'Guardando...' : 'Guardar Cambios' }}
                    </button>
                </div>
            </form>
            
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
import { onMounted, ref, reactive } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ReciboService } from '../../infrastructure/api/ReciboService';
import type { ReciboResponse } from '../../domain/models/Recibo';

const route = useRoute();
const router = useRouter();
const recibo = ref<ReciboResponse | null>(null);
const loading = ref(true);
const saving = ref(false);
const error = ref<string | null>(null);

const id = Number(route.params.id);

const form = reactive({
    fecha_emision: '',
    observaciones: ''
});

onMounted(async () => {
    try {
        const data = await ReciboService.getById(id);
        recibo.value = data;
        // Init form
        form.fecha_emision = data.fecha_emision;
        form.observaciones = data.observaciones || '';
    } catch (e) {
        error.value = "Error al cargar el recibo.";
        console.error(e);
    } finally {
        loading.value = false;
    }
});

const save = async () => {
    saving.value = true;
    error.value = null;
    try {
        await ReciboService.update(id, { 
            fecha_emision: form.fecha_emision,
            observaciones: form.observaciones
        });
        router.push({ name: 'recibos' });
    } catch (e) {
        error.value = "Error al actualizar el recibo.";
        console.error(e);
        saving.value = false;
    }
};
</script>
