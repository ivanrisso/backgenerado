<script setup lang="ts">
import { ref, watch, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import type { Cliente } from '../../../domain/entities/Cliente';
// We need these models for the lists
import type { Domicilio } from '../../../domain/entities/Domicilio';
import DomicilioForm from './DomicilioForm.vue';
import { useTiposDoc } from '../../composables/useTiposDoc';

import { useDomicilios } from '../../composables/useDomicilios';
import { useTelefonos } from '../../composables/useTelefonos';
import { useTiposTel } from '../../composables/useTiposTel';
import { useCondicionesTributarias } from '../../composables/useCondicionesTributarias';
import { useTiposImpuesto } from '../../composables/useTiposImpuesto';
import { useClientes } from '../../composables/useClientes';
import { computed } from 'vue';


const props = defineProps<{
    modelValue: Cliente | null;
    isDeleteMode?: boolean;
    serverError?: string | null;
}>();

const emit = defineEmits<{
    (e: 'submit', entity: Cliente): void;
    (e: 'delete', id: number): void;
    (e: 'cancel'): void;
}>();

const router = useRouter();
const { tiposDoc, loadTiposDoc } = useTiposDoc();

const { domicilios, createDomicilio, updateDomicilio, deleteDomicilio, loadDomicilios } = useDomicilios();
const { telefonos, loadTelefonos } = useTelefonos();
const { tiposTel, loadTiposTel } = useTiposTel();
const { condicionesTributarias, loadCondicionesTributarias } = useCondicionesTributarias();
const { tiposImpuesto, loadTiposImpuesto } = useTiposImpuesto();
const { getAfipTaxComparison, syncAfipTaxes } = useClientes();


const activeTab = ref('general');
const tabs = [
    { id: 'general', name: 'Datos Generales' },
    { id: 'domicilios', name: 'Domicilios' }
];

const showDomicilioModal = ref(false);
const editingDomicilio = ref<Domicilio | null>(null);
const isDomicilioDeleteMode = ref(false);
const domicilioServerError = ref<string | null>(null);
const currentDomicilios = ref<Domicilio[]>([]); 

const isSyncingAfip = ref(false);
const afipComparison = ref<any>(null);
const showAfipSyncModal = ref(false);
const selectedAfipTaxes = ref<string[]>([]);


// impuestos ref from composable is reactively updated by loadClienteImpuestos

const route = useRoute();

onMounted(async () => {
    await Promise.all([
        loadTiposDoc(), 
        loadDomicilios(), 
        loadTelefonos(), 
        loadTiposTel(),
        loadTiposImpuesto(),
        loadCondicionesTributarias()
    ]);
    
    // Check for tab query param
    if (route.query.tab && typeof route.query.tab === 'string') {
        if(tabs.some(t => t.id === route.query.tab)) {
            activeTab.value = route.query.tab;
        }
    }
});

watch(activeTab, (newTab) => {
    router.replace({ query: { ...route.query, tab: newTab } });
});

const form = ref({
    id: 0,
    nombre: '',
    apellido: '',
    razon_social: '',
    cuit: '',
    email: '',
    tipo_doc_id: 0, 
    condicion_iva_id: 0,
    condicion_iibb_id: 0,
    nro_iibb: ''
});

const condicionesIva = computed(() => {
    const ivaTipo = tiposImpuesto.value.find(t => t.codigo_afip === '30');
    return condicionesTributarias.value.filter(c => c.tipo_impuesto_id === ivaTipo?.id);
});

const condicionesIibb = computed(() => {
    const iibbTipo = tiposImpuesto.value.find(t => t.codigo_afip === '900'); // Custom IIBB code
    return condicionesTributarias.value.filter(c => c.tipo_impuesto_id === iibbTipo?.id);
});

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
            condicion_iva_id: newVal.condicion_iva_id || 0,
            condicion_iibb_id: newVal.condicion_iibb_id || 0,
            nro_iibb: newVal.nro_iibb || ''
        };
        // Load relations
        await loadDomicilios();
        currentDomicilios.value = domicilios.value.filter(d => d.cliente_id === newVal.id);
    } else {
        form.value = { 
            id: 0, nombre: '', apellido: '', razon_social: '', cuit: '', email: '', 
            tipo_doc_id: 0, condicion_iva_id: 0, condicion_iibb_id: 0, nro_iibb: ''
        };
        currentDomicilios.value = [];
    }
}, { immediate: true });

// DOMICILIOS Logic
const handleDomicilioSubmit = async (dom: any) => {
    if (form.value.id) {
        dom.cliente_id = form.value.id;
        try {
            if (dom.id) {
                await updateDomicilio(dom);
            } else {
                await createDomicilio(dom);
            }
            showDomicilioModal.value = false;
            await loadDomicilios();
            await loadTelefonos(); 
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
    isDomicilioDeleteMode.value = false;
    domicilioServerError.value = null;
    showDomicilioModal.value = true;
};

const handleEditDomicilio = (dom: Domicilio) => {
    editingDomicilio.value = { ...dom };
    isDomicilioDeleteMode.value = false;
    domicilioServerError.value = null;
    showDomicilioModal.value = true;
};

const handlePreDeleteDomicilio = (dom: Domicilio) => {
    editingDomicilio.value = { ...dom };
    isDomicilioDeleteMode.value = true;
    domicilioServerError.value = null;
    showDomicilioModal.value = true;
};

const handleConfirmDeleteDomicilio = async (id: number) => {
    try {
        await deleteDomicilio(id);
        await loadDomicilios();
        currentDomicilios.value = domicilios.value.filter(d => d.cliente_id === form.value.id);
        showDomicilioModal.value = false;
    } catch (e: any) {
        domicilioServerError.value = e.message || "Error al eliminar domicilio";
    }
};

const navigateToTelefonos = (domicilioId: number) => {
    if (!form.value.id) {
        alert("Debe guardar el cliente primero.");
        return;
    }
    router.push({ 
        name: 'cliente-domicilio-telefonos', 
        params: { 
            clienteId: form.value.id.toString(), 
            domicilioId: domicilioId.toString() 
        } 
    });
};


// AFIP Sync Logic
const handleSyncWithAfip = async () => {
    if (!form.value.id) return;
    isSyncingAfip.value = true;
    try {
        const result = await getAfipTaxComparison(form.value.id);
        afipComparison.value = result;
        // Pre-select missing ones that have a match in local Master Table
        selectedAfipTaxes.value = result.missing_in_local
            .filter((t: any) => t.tipo_impuesto_id)
            .map((t: any) => t.afip_id);
        showAfipSyncModal.value = true;
    } catch (e: any) {
        alert("Error al obtener datos de AFIP: " + (e.message || "Error desconocido"));
    } finally {
        isSyncingAfip.value = false;
    }
};

const handleConfirmAfipSync = async () => {
    if (!form.value.id || selectedAfipTaxes.value.length === 0) {
        showAfipSyncModal.value = false;
        return;
    }
    
    isSyncingAfip.value = true;
    try {
        await syncAfipTaxes(form.value.id, selectedAfipTaxes.value);
        // await loadClienteImpuestos(form.value.id); // No longer needed
        showAfipSyncModal.value = false;
        alert("Sincronización completada con éxito. Los impuestos se han actualizado.");
    } catch (e: any) {
        alert("Error al sincronizar con AFIP: " + (e.message || "Error desconocido"));
    } finally {
        isSyncingAfip.value = false;
    }
};


// CLIENT Logic
const handleSubmit = () => {
    if (props.isDeleteMode) {
        emit('delete', form.value.id);
        return;
    }

    const entity = {
        ...props.modelValue, 
        id: form.value.id,
        nombre: form.value.nombre,
        apellido: form.value.apellido,
        razon_social: form.value.razon_social,
        cuit: form.value.cuit ? { value: form.value.cuit } : undefined,
        email: form.value.email ? { value: form.value.email } : undefined,
        tipo_doc_id: form.value.tipo_doc_id,
        condicion_iva_id: form.value.condicion_iva_id > 0 ? form.value.condicion_iva_id : undefined,
        condicion_iibb_id: form.value.condicion_iibb_id > 0 ? form.value.condicion_iibb_id : undefined,
        nro_iibb: form.value.nro_iibb || undefined
    } as unknown as Cliente;
    
    emit('submit', entity);
};
</script>

<template>
  <div class="max-w-3xl mx-auto">
    <!-- Main Content Card -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        
        <!-- Header -->
        <div class="px-8 py-6 border-b border-gray-100 bg-white flex items-center gap-4" :class="{ 'bg-red-50/50': isDeleteMode }">
             <button @click="$emit('cancel')" class="p-2 -ml-2 text-gray-400 hover:text-gray-600 hover:bg-gray-50 rounded-lg transition-colors">
                 <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" /></svg>
             </button>
             <div>
                <h1 class="text-2xl font-bold text-gray-900">
                    {{ isDeleteMode ? 'Eliminar Cliente' : (form.id ? 'Editar Cliente' : 'Nuevo Cliente') }}
                </h1>
                <p class="text-gray-500 text-sm">
                    {{ isDeleteMode ? 'Confirma que deseas eliminar este registro.' : 'Define los detalles personales y fiscales.' }}
                </p>
             </div>
        </div>

        <!-- Tabs -->
        <div class="px-8 pt-6 pb-2">
            <div class="flex space-x-6 border-b border-gray-100 overflow-x-auto">
                <button 
                    v-for="tab in tabs" 
                    :key="tab.id"
                    @click="activeTab = tab.id"
                    :class="[
                        activeTab === tab.id
                        ? 'border-blue-600 text-blue-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                        'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-colors'
                    ]"
                >
                {{ tab.name }}
                </button>
            </div>
        </div>

        <!-- GENERAL TAB -->
        <div v-show="activeTab === 'general'" class="p-8">
            <!-- Error Alert -->
            <div v-if="serverError" class="mb-6 p-4 bg-red-50 border border-red-100 rounded-lg flex items-start gap-3 text-red-700">
                <svg class="w-5 h-5 mt-0.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <span class="text-sm font-medium">{{ serverError }}</span>
            </div>

            <!-- Delete Warning -->
            <div v-if="isDeleteMode" class="mb-8 p-4 bg-amber-50 border border-amber-100 rounded-lg flex items-start gap-3">
                <svg class="w-5 h-5 text-amber-500 mt-0.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                <div>
                    <h3 class="text-sm font-bold text-amber-800">¿Estás seguro de eliminar este cliente?</h3>
                    <p class="text-xs text-amber-700 mt-1">Se eliminarán también todos los datos vinculados (domicilios, teléfonos, etc.). Esta acción no se puede deshacer.</p>
                </div>
            </div>

            <form id="cliente-form" @submit.prevent="handleSubmit" class="space-y-6">
                 <fieldset :disabled="isDeleteMode" class="space-y-6">
                 <div class="grid grid-cols-1 gap-y-6 gap-x-6 sm:grid-cols-2">
                    
                    <div class="col-span-2">
                        <label class="input-label">Nombre de Cuenta (Opcional)</label>
                        <input 
                            v-model="form.razon_social" 
                            type="text" 
                            placeholder="Ej. Empresa SA"
                            class="input-field" 
                        />
                        <p class="input-helper">Razón social o nombre de fantasía para identificar al cliente corporativo.</p>
                    </div>

                    <div>
                        <label class="input-label">Nombre</label>
                        <input v-model="form.nombre" type="text" required class="input-field" />
                        <p class="input-helper">Nombre de pila del cliente.</p>
                    </div>
                    <div>
                        <label class="input-label">Apellido</label>
                        <input v-model="form.apellido" type="text" required class="input-field" />
                        <p class="input-helper">Apellido del cliente.</p>
                    </div>

                    <div>
                        <label class="input-label">CUIT</label>
                        <input v-model="form.cuit" type="text" class="input-field" placeholder="20-12345678-9" />
                        <p class="input-helper">Clave Única de Identificación Tributaria.</p>
                    </div>
                    <div>
                        <label class="input-label">Email</label>
                        <input v-model="form.email" type="email" class="input-field" placeholder="ejemplo@correo.com" />
                        <p class="input-helper">Correo electrónico de contacto principal.</p>
                    </div>
    
                    <div>
                         <label class="input-label">Tipo Documento</label>
                         <div class="relative">
                            <select v-model="form.tipo_doc_id" required class="input-field appearance-none">
                                <option value="0" disabled>Seleccione...</option>
                                <option v-for="td in tiposDoc" :key="td.id" :value="td.id">{{ td.nombre }}</option>
                            </select>
                             <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-gray-500">
                                <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" /></svg>
                             </div>
                         </div>
                         <p class="input-helper">Tipo de documento de identidad.</p>
                    </div>

                    <!-- Tax Fields Selection -->
                    <div class="col-span-2 border-t border-gray-100 pt-6 mt-2">
                        <div class="flex items-center justify-between mb-4">
                            <h3 class="text-sm font-bold text-gray-800 uppercase tracking-wider">Información Fiscal</h3>
                            <!-- AFIP Sync Button moved here for easier access -->
                            <button 
                                v-if="!isDeleteMode && form.id" 
                                type="button" 
                                @click="handleSyncWithAfip" 
                                class="flex items-center gap-1.5 text-[13px] font-medium text-indigo-600 hover:text-indigo-700 transition-colors disabled:opacity-50"
                                :disabled="isSyncingAfip"
                            >
                                <svg v-if="isSyncingAfip" class="animate-spin h-3.5 w-3.5" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                                <svg v-else class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
                                {{ isSyncingAfip ? 'Sincronizando...' : 'Consultar AFIP' }}
                            </button>
                        </div>
                        
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
                            <div>
                                <label class="input-label">Condición IVA</label>
                                <div class="relative">
                                    <select v-model="form.condicion_iva_id" class="input-field appearance-none">
                                        <option :value="0">Seleccione condición...</option>
                                        <option v-for="c in condicionesIva" :key="c.id" :value="c.id">{{ c.nombre }}</option>
                                    </select>
                                    <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-gray-500">
                                        <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" /></svg>
                                    </div>
                                </div>
                            </div>

                            <div>
                                <label class="input-label">Condición IIBB</label>
                                <div class="relative">
                                    <select v-model="form.condicion_iibb_id" class="input-field appearance-none">
                                        <option :value="0">Seleccione condición...</option>
                                        <option v-for="c in condicionesIibb" :key="c.id" :value="c.id">{{ c.nombre }}</option>
                                    </select>
                                    <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-gray-500">
                                        <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" /></svg>
                                    </div>
                                </div>
                            </div>

                            <div class="sm:col-span-2">
                                <label class="input-label">Nro Inscripción IIBB</label>
                                <input v-model="form.nro_iibb" type="text" class="input-field" placeholder="Ej: 901-123456-7" />
                                <p class="input-helper">Número de inscripción en Ingresos Brutos (si corresponde).</p>
                            </div>
                        </div>
                    </div>
                  </div>
                 </fieldset>
                 
                 <div class="pt-8 flex justify-end gap-3 border-t border-gray-100 mt-8">
                    <button type="button" @click="$emit('cancel')" class="btn btn-secondary flex-1 sm:flex-none">
                        Cancelar
                    </button>
                    <button 
                        type="submit" 
                        class="btn w-full sm:w-auto min-w-[140px]"
                        :class="isDeleteMode ? 'btn-danger' : 'btn-primary'"
                    >
                        {{ isDeleteMode ? 'Eliminar Definitivamente' : 'Guardar Cliente' }}
                    </button>
                </div>
            </form>
        </div>

        <!-- DOMICILIOS TAB -->
        <div v-show="activeTab === 'domicilios'" class="p-6 bg-gray-50/50 min-h-[400px]">
            <!-- List View -->
            <div v-if="!showDomicilioModal" class="space-y-6">
                <div class="flex justify-between items-center px-1">
                    <h4 class="text-xs font-semibold uppercase tracking-wider text-gray-500">Domicilios Asociados</h4>
                    <button v-if="!isDeleteMode" type="button" @click="handleAddDomicilio" class="text-[15px] font-medium text-blue-600 hover:text-blue-700 transition-colors">+ Agregar Domicilio</button>
                </div>
                
                <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden divide-y divide-gray-100">
                    <div v-for="dom in currentDomicilios" :key="dom.id" class="p-4 sm:p-5 hover:bg-gray-50 transition-colors group">
                        <div class="flex flex-col sm:flex-row justify-between sm:items-center gap-4">
                            <div class="flex-1">
                                <div class="flex items-baseline gap-2 mb-1">
                                    <span class="text-[17px] font-medium text-gray-900">{{ dom.calle }} {{ dom.numero }}</span>
                                    <span class="text-sm text-gray-500" v-if="dom.localidad_id">(Loc: {{ dom.localidad_id }})</span>
                                </div>
                                <!-- Phones Preview -->
                                <div class="space-y-1">
                                     <div v-if="telefonos.some(t => t.domicilio_id === dom.id)" class="text-[14px] text-gray-600 space-y-0.5">
                                        <div v-for="tel in telefonos.filter(t => t.domicilio_id === dom.id)" :key="tel.id" class="flex items-center gap-2">
                                            <svg class="w-3.5 h-3.5 text-gray-400" fill="currentColor" viewBox="0 0 20 20"><path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"/></svg>
                                            <span>
                                                <span class="text-gray-400 text-xs uppercase tracking-wide mr-1">{{ tiposTel.find(tt => tt.id === tel.tipo_tel_id)?.nombre }}:</span> 
                                                <span class="font-medium text-gray-700">{{ tel.prefijo }} {{ tel.numero }}</span>
                                            </span>
                                        </div>
                                     </div>
                                     <span v-else class="text-[13px] text-gray-400 italic flex items-center gap-1.5">
                                        No hay teléfonos registrados
                                     </span>
                                </div>
                            </div>
                            
                            <div v-if="!isDeleteMode" class="flex items-center gap-3 sm:border-l sm:border-gray-100 sm:pl-4">
                                <button type="button" @click="handleEditDomicilio(dom)" class="text-sm font-medium text-indigo-600 hover:text-indigo-500">Editar</button>
                                <button type="button" @click="handlePreDeleteDomicilio(dom)" class="text-sm font-medium text-red-600 hover:text-red-500">Eliminar</button>
                                <button type="button" @click="navigateToTelefonos(dom.id)" class="flex items-center gap-1.5 text-sm font-medium text-green-700 bg-green-50 px-3 py-1.5 rounded-full hover:bg-green-100 border border-green-100 transition-colors">

                                    <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1.084.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
                                    Teléfonos
                                </button>
                            </div>
                        </div>
                    </div>
                    
                    <div v-if="currentDomicilios.length === 0" class="p-12 text-center">
                        <span class="inline-block p-3 rounded-full bg-gray-100 text-gray-400 mb-3">
                            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                        </span>
                        <p class="text-[15px] text-gray-500 font-medium">Sin domicilios asignados</p>
                        <p class="text-[13px] text-gray-400 mt-1">Agrega una dirección para comenzar.</p>
                    </div>
                </div>
            </div>

            <!-- Inline Form View (Domicilio) -->
            <div v-else class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                <div class="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-gray-50/50">
                     <h3 class="text-[17px] font-bold text-gray-900">
                        {{ isDomicilioDeleteMode ? 'Eliminar' : (editingDomicilio && editingDomicilio.id ? 'Editar' : 'Nuevo') }} Domicilio
                    </h3>
                    <button type="button" @click="showDomicilioModal = false" class="text-gray-400 hover:text-gray-600 transition-colors">
                        <span class="sr-only">Cerrar</span>
                         <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                           <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>
                <div class="p-6">
                    <DomicilioForm 
                        :modelValue="editingDomicilio || {} as any" 
                        :isDeleteMode="isDomicilioDeleteMode"
                        :serverError="domicilioServerError"
                        @submit="handleDomicilioSubmit" 
                        @delete="handleConfirmDeleteDomicilio"
                        @cancel="showDomicilioModal = false" 
                    />
                </div>
            </div>
        </div>


         <!-- AFIP Sync Modal -->
         <div v-if="showAfipSyncModal" class="fixed inset-0 z-[100] overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
             <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                 <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true" @click="showAfipSyncModal = false"></div>
                 <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
                 <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-xl sm:w-full">
                     <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                         <div class="sm:flex sm:items-start">
                             <div class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-blue-100 sm:mx-0 sm:h-10 sm:w-10">
                                 <svg class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                     <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                                 </svg>
                             </div>
                             <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
                                 <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                                     Sincronización con AFIP (Padrón A5)
                                 </h3>
                                 <div class="mt-4 space-y-4">
                                     <p class="text-sm text-gray-500">
                                         Se han recuperado los impuestos registrados en AFIP para este CUIT. Seleccione los que desea agregar localmente.
                                     </p>
                                     
                                     <!-- Missing in Local -->
                                     <div v-if="afipComparison?.missing_in_local.length" class="space-y-2">
                                         <h4 class="text-xs font-bold text-gray-400 uppercase tracking-wider">Impuestos en AFIP no registrados localmente</h4>
                                         <div class="border border-gray-200 rounded-lg divide-y divide-gray-100">
                                             <div v-for="item in afipComparison.missing_in_local" :key="item.afip_id" class="p-3 flex items-center gap-3">
                                                 <input 
                                                     type="checkbox" 
                                                     :id="`afip-tax-${item.afip_id}`" 
                                                     :value="item.afip_id" 
                                                     v-model="selectedAfipTaxes"
                                                     :disabled="!item.tipo_impuesto_id"
                                                     class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 disabled:opacity-50"
                                                 >
                                                 <div class="flex-1">
                                                     <label :for="`afip-tax-${item.afip_id}`" class="block text-sm font-medium text-gray-700" :class="{'opacity-50': !item.tipo_impuesto_id}">
                                                         {{ item.nombre }} (Cód. {{ item.afip_id }})
                                                     </label>
                                                     <p v-if="!item.tipo_impuesto_id" class="text-[11px] text-red-500 font-medium">No mapeado en el sistema local</p>
                                                     <p v-else class="text-[11px] text-green-600 font-medium italic">Listo para sincronizar</p>
                                                 </div>
                                             </div>
                                         </div>
                                     </div>

                                     <!-- Matches -->
                                     <div v-if="afipComparison?.matches.length" class="space-y-2">
                                         <h4 class="text-xs font-bold text-gray-400 uppercase tracking-wider">Impuestos ya sincronizados</h4>
                                         <div class="border border-gray-100 rounded-lg divide-y divide-gray-100 bg-gray-50/50">
                                             <div v-for="item in afipComparison.matches" :key="item.afip_id" class="p-3 flex items-center gap-3 opacity-60">
                                                  <svg class="h-4 w-4 text-green-500" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
                                                  <span class="text-sm font-medium text-gray-600">{{ item.nombre }} (Cód. {{ item.afip_id }})</span>
                                             </div>
                                         </div>
                                     </div>

                                     <div v-if="!afipComparison?.missing_in_local.length && !afipComparison?.matches.length" class="text-center py-6">
                                         <p class="text-sm text-gray-500 italic">No se encontraron impuestos registrados en AFIP.</p>
                                     </div>
                                 </div>
                             </div>
                         </div>
                     </div>
                     <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse gap-2">
                         <button 
                             type="button" 
                             class="btn btn-primary w-full sm:w-auto"
                             @click="handleConfirmAfipSync"
                             :disabled="selectedAfipTaxes.length === 0 || isSyncingAfip"
                         >
                             <svg v-if="isSyncingAfip" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                             Sincronizar {{ selectedAfipTaxes.length }} seleccionados
                         </button>
                         <button 
                             type="button" 
                             class="btn btn-secondary w-full sm:w-auto mt-2 sm:mt-0" 
                             @click="showAfipSyncModal = false"
                             :disabled="isSyncingAfip"
                         >
                             Cerrar
                         </button>
                     </div>
                 </div>
             </div>
         </div>

    </div>
  </div>

</template>
