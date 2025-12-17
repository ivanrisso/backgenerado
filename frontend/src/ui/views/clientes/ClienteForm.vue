<script setup lang="ts">
import { ref, watch, onMounted } from 'vue';
import type { Cliente } from '../../../domain/entities/Cliente';
// We need these models for the lists
import type { Domicilio } from '../../../domain/entities/Domicilio';
import DomicilioForm from './DomicilioForm.vue';
import TelefonoManager from './TelefonoManager.vue';
import { useTiposDoc } from '../../composables/useTiposDoc';
import { useIvas } from '../../composables/useIvas';
import { useDomicilios } from '../../composables/useDomicilios';
import { useTelefonos } from '../../composables/useTelefonos';
import { useTiposTel } from '../../composables/useTiposTel';

const props = defineProps<{
    modelValue: Cliente | null;
}>();

const emit = defineEmits<{
    (e: 'submit', entity: Cliente): void;
    (e: 'cancel'): void;
}>();

const { tiposDoc, loadTiposDoc } = useTiposDoc();
const { ivas, loadIvas } = useIvas();
const { domicilios, createDomicilio, updateDomicilio, deleteDomicilio, loadDomicilios } = useDomicilios(); // Ideally scoped to client or generic
const { telefonos, loadTelefonos } = useTelefonos();
const { tiposTel, loadTiposTel } = useTiposTel();

const activeTab = ref('general');
const tabs = [
    { id: 'general', name: 'Datos Generales' },
    { id: 'domicilios', name: 'Domicilios' }
];

const showDomicilioModal = ref(false);
const editingDomicilio = ref<Domicilio | null>(null);
const currentDomicilios = ref<Domicilio[]>([]); 

const managingTelefonosFor = ref<number | null>(null);

onMounted(async () => {
    await Promise.all([loadTiposDoc(), loadIvas(), loadDomicilios(), loadTelefonos(), loadTiposTel()]);
});

const form = ref({
    id: 0,
    nombre: '',
    apellido: '',
    razon_social: '',
    cuit: '',
    email: '',
    tipo_doc_id: 0, 
    iva_id: 0,     
});

// We'll manage domicilios via local fetch or store for this client
// Since relationships are not fully loaded in Client entity (based on previous files),
// we might need to fetch them separately if backend doesn't hydrate 'domicilios' prop.
// 'Cliente' entity definition has 'domicilios: Domicilio[]' ? 
// Checked definition: NO, it didn't in 'Cliente.ts' viewed earlier?
// Wait, Cliente.ts:
// export interface Cliente { ... tipo_doc_id: number; iva_id: number; }
// It DOES NOT have 'domicilios' array in the interface I viewed in Step 485.
// So we MUST fetch domicilios separately using API, or the Client List view is irrelevant for that.
// But the backend ORM has it. The Frontend Entity might be incomplete. 
// For now, I'll rely on fetching via useDomicilios and filtering by client, 
// OR I should assume the API call updates the list.
// Let's filter global list for this ID? Or just use what we have.

watch(() => props.modelValue, async (newVal) => {
    if (newVal) {
        form.value = {
            id: newVal.id,
            nombre: newVal.nombre,
            apellido: newVal.apellido,
            razon_social: newVal.razon_social || '',
            cuit: (newVal.cuit as any)?.value || newVal.cuit || '',
            email: (newVal.email as any)?.value || (newVal.email as any)?.getValue?.() || newVal.email || '',
            tipo_doc_id: newVal.tipo_doc_id,
            iva_id: newVal.iva_id,
        };
        // TODO: Load domicilios
        await loadDomicilios(); // Loads all?
        currentDomicilios.value = domicilios.value.filter(d => d.cliente_id === newVal.id);
    } else {
        form.value = { 
            id: 0, nombre: '', apellido: '', razon_social: '', cuit: '', email: '', 
            tipo_doc_id: 0, iva_id: 0
        };
        currentDomicilios.value = [];
    }
}, { immediate: true });

const handleDomicilioSubmit = async (dom: any) => {
    // Add client_id if missing
    if (form.value.id) {
        dom.cliente_id = form.value.id;
        try {
            if (dom.id) {
                await updateDomicilio(dom);
            } else {
                await createDomicilio(dom);
            }
            
            showDomicilioModal.value = false;
            // Refresh
            await loadDomicilios();
            await loadTelefonos(); // Refresh phones too
            currentDomicilios.value = domicilios.value.filter(d => d.cliente_id === form.value.id);
        } catch(e) {
            console.error(e);
            alert('Error guardando domicilio');
        }
    } else {
        alert('Debe guardar el cliente antes de asignar domicilios.');
    }
};

const handleAddDomicilio = () => {
    if(form.value.id === 0) {
        alert('Guarde el cliente primero.');
        return;
    }
    editingDomicilio.value = { cliente_id: form.value.id } as Domicilio;
    showDomicilioModal.value = true;
};

const handleEditDomicilio = (dom: Domicilio) => {
    editingDomicilio.value = { ...dom };
    showDomicilioModal.value = true;
};

const handleDeleteDomicilio = async (id: number) => {
    if(confirm('¿Eliminar domicilio?')) {
        await deleteDomicilio(id);
        // Refresh
        await loadDomicilios();
        currentDomicilios.value = domicilios.value.filter(d => d.cliente_id === form.value.id);
    }
};

const handleSubmit = () => {
    const entity = {
        ...props.modelValue, 
        id: form.value.id,
        nombre: form.value.nombre,
        apellido: form.value.apellido,
        razon_social: form.value.razon_social,
        cuit: form.value.cuit ? { value: form.value.cuit } : undefined,
        email: form.value.email ? { value: form.value.email } : undefined,
        tipo_doc_id: form.value.tipo_doc_id,
        iva_id: form.value.iva_id
    } as unknown as Cliente;
    
    emit('submit', entity);
};
</script>

<template>
  <div>
    <!-- Tabs Header -->
    <div class="border-b border-gray-200 mb-6">
      <nav class="-mb-px flex space-x-8" aria-label="Tabs">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="[
            activeTab === tab.id
              ? 'border-blue-500 text-blue-600'
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
            'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm'
          ]"
        >
          {{ tab.name }}
        </button>
      </nav>
    </div>

    <!-- GENERAL TAB (Main Form) -->
    <div v-show="activeTab === 'general'" class="space-y-4">
        <form id="cliente-form" @submit.prevent="handleSubmit">
             <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700">Nombre</label>
                    <input v-model="form.nombre" type="text" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border" />
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700">Apellido</label>
                    <input v-model="form.apellido" type="text" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border" />
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700">Razón Social</label>
                    <input v-model="form.razon_social" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border" />
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700">CUIT</label>
                    <input v-model="form.cuit" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border" />
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700">Email</label>
                    <input v-model="form.email" type="email" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border" />
                </div>
                <!-- Selectors -->
                <div>
                     <label class="block text-sm font-medium text-gray-700">Tipo Documento</label>
                     <select v-model="form.tipo_doc_id" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border">
                        <option value="0" disabled>Seleccione...</option>
                        <option v-for="td in tiposDoc" :key="td.id" :value="td.id">{{ td.nombre }}</option>
                     </select>
                </div>
                <div>
                     <label class="block text-sm font-medium text-gray-700">Condición IVA</label>
                     <select v-model="form.iva_id" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border">
                        <option value="0" disabled>Seleccione...</option>
                        <option v-for="i in ivas" :key="i.id" :value="i.id">{{ i.descripcion }}</option>
                     </select>
                </div>
             </div>
        </form>
    </div>

    <!-- DOMICILIOS TAB (Independent) -->
    <div v-show="activeTab === 'domicilios'" class="space-y-4">
        
        <!-- List View -->
        <div v-if="!showDomicilioModal" class="space-y-4">
            <div class="flex justify-between">
                <h4 class="text-md font-bold text-gray-800">Domicilios Asociados</h4>
                <button type="button" @click="handleAddDomicilio" class="text-sm text-blue-600 hover:text-blue-800 font-medium">+ Agregar Domicilio</button>
            </div>
            
            <table class="min-w-full divide-y divide-gray-200 border">
                <thead class="bg-gray-50">
                    <tr>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Calle</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Número</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Teléfonos</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="dom in currentDomicilios" :key="dom.id">
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ dom.calle }}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ dom.numero }}</td>
                        <td class="px-6 py-4 text-sm text-gray-500">
                            <ul v-if="telefonos.some(t => t.domicilio_id === dom.id)">
                                <li v-for="tel in telefonos.filter(t => t.domicilio_id === dom.id)" :key="tel.id">
                                    <span class="font-medium text-xs text-gray-700">{{ tiposTel.find(tt => tt.id === tel.tipo_tel_id)?.nombre }}:</span> {{ tel.prefijo }} {{ tel.numero }}
                                </li>
                            </ul>
                            <span v-else class="text-xs text-gray-400 italic">Sin teléfonos</span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium flex gap-2">
                            <button type="button" @click="handleEditDomicilio(dom)" class="text-indigo-600 hover:text-indigo-900">Editar</button>
                            <button type="button" @click="managingTelefonosFor = dom.id" class="text-green-600 hover:text-green-900 border border-green-200 px-2 rounded-sm bg-green-50">Teléfonos</button>
                            <button type="button" @click="handleDeleteDomicilio(dom.id)" class="text-red-600 hover:text-red-900">Quitar</button>
                        </td>
                    </tr>
                    <tr v-if="currentDomicilios.length === 0">
                        <td colspan="4" class="px-6 py-4 text-center text-sm text-gray-500">Sin domicilios asignados.</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Phone Manager Modal -->
        <div v-if="managingTelefonosFor" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50 flex items-center justify-center">
            <div class="relative bg-white rounded-lg shadow-xl p-6 w-full max-w-2xl border">
                <div class="flex justify-between items-center mb-4">
                    <h3 class="text-lg font-medium text-gray-900">Administrar Teléfonos</h3>
                    <button type="button" @click="managingTelefonosFor = null" class="text-gray-400 hover:text-gray-500">
                         <span class="sr-only">Cerrar</span>
                         <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                           <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>
                <TelefonoManager :domicilioId="managingTelefonosFor" />
                <div class="mt-4 flex justify-end">
                    <button type="button" @click="managingTelefonosFor = null" class="px-4 py-2 bg-gray-200 rounded text-gray-700 text-sm hover:bg-gray-300">Cerrar</button>
                </div>
            </div>
        </div>

        <!-- Inline Form View (Component contains its own form) -->
        <div v-else class="bg-gray-50 p-4 rounded-lg border border-gray-200">
            <div class="flex justify-between items-center mb-4">
                 <h3 class="text-lg font-medium text-gray-900">
                    {{ editingDomicilio && editingDomicilio.id ? 'Editar' : 'Nuevo' }} Domicilio
                </h3>
                <button type="button" @click="showDomicilioModal = false" class="text-gray-400 hover:text-gray-500">
                    <span class="sr-only">Cerrar</span>
                     <!-- simple x icon -->
                    <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                       <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>
            <DomicilioForm :modelValue="editingDomicilio || {} as any" @submit="handleDomicilioSubmit" @cancel="showDomicilioModal = false" />
        </div>
    </div>

    <!-- Form Actions (Shared) -->
    <div class="flex justify-end gap-3 pt-6 border-t border-gray-200 mt-6" v-show="activeTab === 'general'">
        <button type="button" @click="$emit('cancel')" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
            Cancelar
        </button>
        <button type="submit" form="cliente-form" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
            Guardar Cliente
        </button>
    </div>
  </div>
</template>
