<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { useTelefonos } from '../../composables/useTelefonos';
import { useTiposTel } from '../../composables/useTiposTel';
import type { Telefono } from '../../../domain/entities/Telefono';

const props = defineProps<{
    domicilioId: number;
}>();

const { telefonos, loadTelefonosByDomicilio, createTelefono, updateTelefono, deleteTelefono } = useTelefonos();
const { tiposTel, loadTiposTel } = useTiposTel();

const telefonoForm = ref({
    id: 0,
    tipo_tel_id: 0,
    prefijo: '',
    numero: ''
});
const showTelefonoForm = ref(false);
const isDeleteMode = ref(false);
const serverError = ref<string | null>(null);


// No longer needed as 'telefonos' will contain only the filtered list
// const currentTelefonos = computed(() => { ... });

onMounted(async () => {
    if (props.domicilioId) {
        await Promise.all([loadTiposTel(), loadTelefonosByDomicilio(props.domicilioId)]);
    } else {
        await loadTiposTel();
    }
});

// Watch for prop change to ensuring reloading/filtering if modal is reused
watch(() => props.domicilioId, async (newId) => {
    if(newId) {
        await loadTelefonosByDomicilio(newId);
    }
});

const resetTelefonoForm = () => {
    telefonoForm.value = { id: 0, tipo_tel_id: 0, prefijo: '', numero: '' };
    showTelefonoForm.value = false;
    isDeleteMode.value = false;
    serverError.value = null;
};

const handleEditTelefono = (tel: Telefono) => {
    telefonoForm.value = { 
        id: tel.id, 
        tipo_tel_id: tel.tipo_tel_id, 
        prefijo: tel.prefijo, 
        numero: tel.numero 
    };
    isDeleteMode.value = false;
    serverError.value = null;
    showTelefonoForm.value = true;
};

const handlePreDeleteTelefono = (tel: Telefono) => {
    telefonoForm.value = { 
        id: tel.id, 
        tipo_tel_id: tel.tipo_tel_id, 
        prefijo: tel.prefijo, 
        numero: tel.numero 
    };
    isDeleteMode.value = true;
    serverError.value = null;
    showTelefonoForm.value = true;
};

const handleSaveTelefono = async () => {
    if (!props.domicilioId) return;

    if (isDeleteMode.value) {
        try {
            await deleteTelefono(telefonoForm.value.id);
            await loadTelefonosByDomicilio(props.domicilioId);
            resetTelefonoForm();
        } catch (e: any) {
            serverError.value = e.message || "Error al eliminar teléfono";
        }
        return;
    }

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
        
        // Manually reload filtered list
        if (props.domicilioId) {
            await loadTelefonosByDomicilio(props.domicilioId);
        }
        resetTelefonoForm();
    } catch (e: any) {
        serverError.value = e.message || "Error guardando teléfono";
    }
};

// Logic moved to handleSaveTelefono to standardise UX
const handleDeleteTelefono = (id: number) => {
    const tel = telefonos.value.find(t => t.id === id);
    if (tel) handlePreDeleteTelefono(tel);
};
</script>

<template>
    <div class="space-y-6">
        <!-- List Header with Action -->
        <div class="flex flex-col sm:flex-row justify-between items-end sm:items-center px-4 sm:px-0">
             <h2 class="text-xs font-semibold uppercase tracking-wider text-gray-500 sm:ml-4">Lista de Contacto</h2>
             <button v-if="!showTelefonoForm" type="button" @click="showTelefonoForm = true" class="mt-2 sm:mt-0 text-[15px] font-medium text-blue-600 hover:text-blue-500 transition-colors">
                + Agregar Teléfono
            </button>
        </div>

        <!-- Phone Form Card -->
        <div v-if="showTelefonoForm" class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden mx-0 sm:mx-0">
            <div class="px-5 py-4 border-b border-gray-100 backdrop-blur-sm" :class="isDeleteMode ? 'bg-red-50' : 'bg-gray-50/50'">
                <h5 class="text-[17px] font-semibold text-gray-900">
                    {{ isDeleteMode ? 'Eliminar' : (telefonoForm.id ? 'Editar' : 'Nuevo') }} Teléfono
                </h5>
            </div>
            
            <div class="p-5 space-y-4">
                <!-- Error Alert -->
                <div v-if="serverError" class="p-4 bg-red-50 border border-red-100 rounded-lg flex items-start gap-3 text-red-700 mb-2">
                    <svg class="w-5 h-5 mt-0.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                    <span class="text-sm font-medium">{{ serverError }}</span>
                </div>

                <fieldset :disabled="isDeleteMode" class="space-y-4">
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div class="col-span-1">
                        <label class="block text-xs font-medium text-gray-500 uppercase tracking-wide mb-1.5">Tipo</label>
                        <div class="relative">
                            <select v-model="telefonoForm.tipo_tel_id" class="block w-full rounded-lg border-gray-300 bg-gray-50 py-2.5 px-3 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-[15px] appearance-none transition-shadow">
                                <option value="0" disabled>Seleccionar...</option>
                                <option v-for="t in tiposTel" :key="t.id" :value="t.id">{{ t.nombre }}</option>
                            </select>
                            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-500">
                                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                            </div>
                        </div>
                    </div>
                    <div class="col-span-1">
                        <label class="block text-xs font-medium text-gray-500 uppercase tracking-wide mb-1.5">Prefijo</label>
                         <input v-model="telefonoForm.prefijo" type="text" class="block w-full rounded-lg border-gray-300 bg-gray-50 py-2.5 px-3 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-[15px] transition-shadow placeholder-gray-400" placeholder="Ej. 54 9 11" />
                    </div>
                    <div class="col-span-1">
                         <label class="block text-xs font-medium text-gray-500 uppercase tracking-wide mb-1.5">Número</label>
                         <input v-model="telefonoForm.numero" type="text" class="block w-full rounded-lg border-gray-300 bg-gray-50 py-2.5 px-3 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-[15px] transition-shadow" placeholder="Número" />
                    </div>
                </div>
                </fieldset>
            </div>
            
            <div class="px-5 py-3 bg-gray-50 border-t border-gray-100 flex justify-end gap-3">
                <button @click="resetTelefonoForm" type="button" class="px-4 py-2 text-[15px] font-medium text-gray-600 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 shadow-sm transition-all">Cancelar</button>
                <button 
                    @click="handleSaveTelefono" 
                    type="button" 
                    class="px-4 py-2 text-[15px] font-medium text-white rounded-lg shadow-sm transition-all focus:ring-2 focus:ring-offset-1"
                    :class="isDeleteMode ? 'bg-red-600 hover:bg-red-700 focus:ring-red-500' : 'bg-blue-600 hover:bg-blue-500 focus:ring-blue-500'"
                >
                    {{ isDeleteMode ? 'Eliminar Definitivamente' : 'Guardar' }}
                </button>
            </div>
        </div>

        <!-- Phones List (Apple Style) -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden divide-y divide-gray-100">
            <template v-if="telefonos.length > 0">
                <div v-for="tel in telefonos" :key="tel.id" class="group flex items-center justify-between p-4 hover:bg-gray-50 transition-colors">
                    <div class="flex-1 min-w-0">
                         <div class="flex flex-col sm:flex-row sm:items-baseline">
                            <span class="text-[17px] font-medium text-gray-900 truncate mr-3">
                                {{ tel.prefijo }} {{ tel.numero }}
                            </span>
                            <span class="text-[15px] text-gray-500">
                                {{ tiposTel.find(t => t.id === tel.tipo_tel_id)?.nombre || 'Teléfono' }}
                            </span>
                        </div>
                    </div>
                    <div class="flex items-center gap-4 ml-4">
                        <button @click="handleEditTelefono(tel)" type="button" class="text-[15px] font-medium text-blue-600 hover:text-blue-500 transition-colors">Editar</button>
                        <div class="h-4 w-px bg-gray-200"></div>
                        <button @click="handleDeleteTelefono(tel.id)" type="button" class="text-[15px] font-medium text-red-600 hover:text-red-500 transition-colors">Eliminar</button>
                    </div>
                </div>
            </template>
            <div v-else class="p-8 text-center">
                <p class="text-[17px] text-gray-400">No hay teléfonos asociados.</p>
                <button @click="showTelefonoForm = true" class="mt-2 text-sm text-blue-600 hover:underline">
                    Agregar el primero
                </button>
            </div>
        </div>
    </div>
</template>
