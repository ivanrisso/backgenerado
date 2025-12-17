<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import { useTelefonos } from '../../composables/useTelefonos';
import { useTiposTel } from '../../composables/useTiposTel';
import type { Telefono } from '../../../domain/entities/Telefono';

const props = defineProps<{
    domicilioId: number;
}>();

const { telefonos, loadTelefonos, createTelefono, updateTelefono, deleteTelefono } = useTelefonos();
const { tiposTel, loadTiposTel } = useTiposTel();

const telefonoForm = ref({
    id: 0,
    tipo_tel_id: 0,
    prefijo: '',
    numero: ''
});
const showTelefonoForm = ref(false);

const currentTelefonos = computed(() => {
    if (!props.domicilioId) return [];
    return telefonos.value.filter(t => t.domicilio_id === props.domicilioId);
});

onMounted(async () => {
    await Promise.all([loadTiposTel(), loadTelefonos()]);
});

// Watch for prop change to ensuring reloading/filtering if modal is reused
watch(() => props.domicilioId, async () => {
    // If we wanted to fetch *only* for this ID we would do it here. 
    // Since useTelefonos loads all, we just rely on computed filter. 
    // Ensuring data is fresh:
    await loadTelefonos(); 
});

const resetTelefonoForm = () => {
    telefonoForm.value = { id: 0, tipo_tel_id: 0, prefijo: '', numero: '' };
    showTelefonoForm.value = false;
};

const handleEditTelefono = (tel: Telefono) => {
    telefonoForm.value = { 
        id: tel.id, 
        tipo_tel_id: tel.tipo_tel_id, 
        prefijo: tel.prefijo, 
        numero: tel.numero 
    };
    showTelefonoForm.value = true;
};

const handleSaveTelefono = async () => {
    if (!props.domicilioId) return;

    if (!telefonoForm.value.tipo_tel_id) {
        alert("Debe seleccionar un Tipo de Teléfono.");
        return;
    }
    
    try {
        const payload: Telefono = {
            id: telefonoForm.value.id,
            tipo_tel_id: telefonoForm.value.tipo_tel_id,
            prefijo: telefonoForm.value.prefijo,
            numero: telefonoForm.value.numero,
            domicilio_id: props.domicilioId
        };

        if (telefonoForm.value.id) {
            await updateTelefono(payload);
        } else {
            await createTelefono(payload);
        }
        resetTelefonoForm();
    } catch (e: any) {
        alert("Error guardando teléfono: " + e.message);
    }
};

const handleDeleteTelefono = async (id: number) => {
    if(confirm('¿Eliminar teléfono?')) {
        await deleteTelefono(id);
    }
};
</script>

<template>
    <div class="space-y-4">
        <div class="flex justify-between items-center mb-4">
            <h4 class="text-md font-bold text-gray-800">Listado de Teléfonos</h4>
            <button v-if="!showTelefonoForm" type="button" @click="showTelefonoForm = true" class="text-sm text-blue-600 hover:text-blue-800 font-medium">+ Agregar Teléfono</button>
        </div>

        <!-- Phone Form -->
        <div v-if="showTelefonoForm" class="bg-gray-100 p-4 rounded-md mb-4 border border-gray-300">
            <h5 class="text-sm font-bold text-gray-700 mb-2">{{ telefonoForm.id ? 'Editar' : 'Nuevo' }} Teléfono</h5>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-2">
                    <div>
                    <label class="block text-xs font-medium text-gray-600">Tipo</label>
                    <select v-model="telefonoForm.tipo_tel_id" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm sm:text-sm p-1 border">
                        <option value="0" disabled>Seleccione...</option>
                        <option v-for="t in tiposTel" :key="t.id" :value="t.id">{{ t.nombre }}</option>
                    </select>
                </div>
                <div>
                    <label class="block text-xs font-medium text-gray-600">Prefijo</label>
                    <input v-model="telefonoForm.prefijo" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm sm:text-sm p-1 border" placeholder="e.g. 54 9 11" />
                </div>
                <div>
                        <label class="block text-xs font-medium text-gray-600">Número</label>
                    <input v-model="telefonoForm.numero" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm sm:text-sm p-1 border" />
                </div>
            </div>
                <div class="flex justify-end gap-2 mt-2">
                <button @click="resetTelefonoForm" type="button" class="text-xs text-gray-600 hover:text-gray-800">Cancelar</button>
                <button @click="handleSaveTelefono" type="button" class="text-xs bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700">Guardar</button>
            </div>
        </div>

        <!-- Phones List -->
        <ul class="divide-y divide-gray-200 bg-white border rounded-md">
            <li v-for="tel in currentTelefonos" :key="tel.id" class="px-4 py-3 flex items-center justify-between text-sm">
                <div>
                    <span class="font-medium text-gray-900 mr-2">
                        {{ tiposTel.find(t => t.id === tel.tipo_tel_id)?.nombre || 'Teléfono' }}:
                    </span>
                    <span class="text-gray-600">{{ tel.prefijo }} {{ tel.numero }}</span>
                </div>
                <div class="flex space-x-2">
                    <button @click="handleEditTelefono(tel)" type="button" class="text-indigo-600 hover:text-indigo-900">Editar</button>
                    <button @click="handleDeleteTelefono(tel.id)" type="button" class="text-red-600 hover:text-red-900">Quitar</button>
                </div>
            </li>
                <li v-if="currentTelefonos.length === 0" class="px-4 py-3 text-gray-500 italic text-center">
                No hay teléfonos asociados.
            </li>
        </ul>
    </div>
</template>
