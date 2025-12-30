
<script setup lang="ts">
import { ref, watch, onMounted } from 'vue';
import type { Articulo } from '../../../domain/entities/Articulo';
import { TipoArticuloEnum } from '../../../domain/enums/TipoArticuloEnum';
import { useTiposImpuesto } from '../../composables/useTiposImpuesto';
import { TipoUsoImpuestoEnum } from '../../../domain/enums/TipoUsoImpuestoEnum';

const props = defineProps<{
    modelValue: Articulo | null;
    isDeleteMode?: boolean;
    serverError?: string | null;
}>();

const emit = defineEmits<{
    (e: 'submit', entity: Articulo): void;
    (e: 'delete', id: number): void;
    (e: 'cancel'): void;
}>();

const { tiposImpuesto, loadTiposImpuesto } = useTiposImpuesto();

const activeTab = ref('general');

const form = ref<any>({
    id: 0,
    codigo: '',
    nombre: '',
    descripcion: '',
    precio_venta: 0,
    precio_costo: 0,
    tipo: TipoArticuloEnum.SERVICIO,
    activo: true,
    impuesto_venta_id: undefined,
    impuesto_compra_id: undefined
});

onMounted(async () => {
    await loadTiposImpuesto();
});

watch(() => props.modelValue, (newVal) => {
    if (newVal) {
        form.value = { ...newVal };
    } else {
        form.value = {
            id: 0,
            codigo: '',
            nombre: '',
            descripcion: '',
            precio_venta: 0,
            precio_costo: 0,
            tipo: TipoArticuloEnum.SERVICIO,
            activo: true,
            impuesto_venta_id: undefined,
            impuesto_compra_id: undefined
        };
    }
}, { immediate: true });

const filteredVentaTaxes = ref<any[]>([]);
const filteredCompraTaxes = ref<any[]>([]);

watch(tiposImpuesto, (newTaxes) => {
    filteredVentaTaxes.value = newTaxes.filter(t => t.tipo_uso === TipoUsoImpuestoEnum.VENTAS);
    filteredCompraTaxes.value = newTaxes.filter(t => t.tipo_uso === TipoUsoImpuestoEnum.COMPRAS);
}, { immediate: true, deep: true });

const handleSubmit = () => {
    if (props.isDeleteMode) {
        emit('delete', form.value.id);
        return;
    }
    
    const entity: Articulo = {
        ...form.value,
        precio_venta: Number(form.value.precio_venta),
        precio_costo: Number(form.value.precio_costo),
        impuesto_venta_id: form.value.impuesto_venta_id ? Number(form.value.impuesto_venta_id) : undefined,
        impuesto_compra_id: form.value.impuesto_compra_id ? Number(form.value.impuesto_compra_id) : undefined
    };
    emit('submit', entity);
};
</script>

<template>
  <div class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden mb-8 transform transition-all duration-300">
    <!-- Header -->
    <div class="px-8 py-6 border-b border-gray-100 bg-gradient-to-r from-gray-50 to-white flex justify-between items-center">
        <div>
            <h3 class="text-2xl font-bold text-gray-800 tracking-tight">
                {{ isDeleteMode ? 'Eliminar' : (modelValue ? 'Editar' : 'Nuevo') }} Artículo
            </h3>
            <p class="text-sm text-gray-500 mt-1">Gestione sus productos y servicios de forma profesional.</p>
        </div>
        <div v-if="form.activo" class="flex items-center space-x-2">
            <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold bg-green-100 text-green-700 border border-green-200 uppercase tracking-tighter">
                <span class="w-1.5 h-1.5 rounded-full bg-green-500 mr-2 animate-pulse"></span>
                Activo
            </span>
        </div>
    </div>
    
    <!-- Error Notification -->
    <div v-if="serverError" class="mx-8 mt-6 p-4 bg-red-50 text-red-700 border border-red-200 rounded-xl flex items-center space-x-3 shadow-sm animate-shake">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-red-500" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
        </svg>
        <span class="font-medium">{{ serverError }}</span>
    </div>

    <!-- Delete Confirmation Message -->
    <div v-if="isDeleteMode" class="mx-8 mt-6 p-6 bg-amber-50 text-amber-900 border border-amber-200 rounded-xl shadow-inner">
        <div class="flex items-start">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-amber-600 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <div>
                <p class="font-bold text-lg">¿Está seguro de realizar esta acción?</p>
                <p class="text-sm mt-1 opacity-90">Eliminar este artículo desactivará su vinculación histórica en los cupones y reservas.</p>
            </div>
        </div>
    </div>

    <form @submit.prevent="handleSubmit">
        <fieldset :disabled="isDeleteMode" class="disabled:opacity-75">
            <!-- Main Info Section -->
            <div class="p-8 grid grid-cols-1 lg:grid-cols-12 gap-10">
                <!-- Left: Name and Basic Info -->
                <div class="lg:col-span-8 space-y-6">
                    <div>
                        <label class="block text-xs font-bold text-gray-500 uppercase tracking-widest mb-2">Nombre del Artículo / Servicio</label>
                        <input v-model="form.nombre" type="text" placeholder="Ej: Servicio de Consultoría" required 
                               class="w-full text-lg font-medium rounded-xl border-gray-200 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 transition-all duration-300 py-3 px-4" />
                    </div>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label class="block text-xs font-bold text-gray-500 uppercase tracking-widest mb-2">Código Interno</label>
                            <input v-model="form.codigo" type="text" placeholder="REF-001" required 
                                   class="w-full rounded-xl border-gray-200 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 transition-all duration-300 py-2.5 px-4" />
                        </div>
                        <div>
                            <label class="block text-xs font-bold text-gray-500 uppercase tracking-widest mb-2">Tipo de Artículo</label>
                            <select v-model="form.tipo" 
                                    class="w-full rounded-xl border-gray-200 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 transition-all duration-300 py-2.5 px-4 bg-gray-50 font-medium">
                                <option :value="TipoArticuloEnum.SERVICIO">Servicio</option>
                                <option :value="TipoArticuloEnum.PRODUCTO">Producto</option>
                                <option :value="TipoArticuloEnum.CONSUMIBLE">Consumible</option>
                            </select>
                        </div>
                    </div>
                </div>

                <!-- Right: Visual State or Preview -->
                <div class="lg:col-span-4 flex flex-col justify-start space-y-6 bg-gray-50/50 p-6 rounded-2xl border border-gray-100">
                    <div class="flex items-center justify-between">
                        <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">Estado de publicación</span>
                        <label class="relative inline-flex items-center cursor-pointer">
                            <input v-model="form.activo" type="checkbox" class="sr-only peer">
                            <div class="w-14 h-7 bg-gray-300 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-200 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[4px] after:left-[4px] after:bg-white after:border-gray-200 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600 shadow-sm"></div>
                        </label>
                    </div>
                    
                    <div class="pt-2">
                        <label class="block text-xs font-bold text-gray-500 uppercase tracking-widest mb-2">Precio de Venta</label>
                        <div class="relative rounded-xl shadow-sm">
                            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                <span class="text-gray-400 font-bold">$</span>
                            </div>
                            <input v-model="form.precio_venta" type="number" step="0.01" 
                                   class="block w-full pl-8 pr-4 py-3 rounded-xl border-gray-200 font-bold text-xl text-blue-700 bg-white focus:ring-blue-200 focus:border-blue-500 transition-all" />
                        </div>
                    </div>
                </div>
            </div>

            <!-- Tabs Section (Odoo Style) -->
            <div class="mt-4">
                <div class="px-8 border-b border-gray-100 overflow-x-auto scroller-hide">
                    <nav class="-mb-px flex space-x-10" aria-label="Tabs">
                        <button v-for="tab in [{id:'general', name:'General'}, {id:'ventas', name:'Ventas'}, {id:'compras', name:'Compras'}]" 
                                :key="tab.id"
                                type="button" 
                                @click="activeTab = tab.id"
                                :class="[activeTab === tab.id ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-400 hover:text-gray-600 hover:border-gray-300', 'whitespace-nowrap py-5 px-1 border-b-2 font-bold text-xs uppercase tracking-widest transition-all duration-300']">
                            {{ tab.name }}
                        </button>
                    </nav>
                </div>

                <div class="p-8 min-h-[300px] bg-white">
                    <!-- General Tab -->
                    <div v-show="activeTab === 'general'" class="max-w-3xl animate-fadeIn">
                        <div class="space-y-6">
                            <div>
                                <label class="block text-xs font-bold text-gray-500 uppercase tracking-widest mb-2">Notas internas / Descripción detallada</label>
                                <textarea v-model="form.description" rows="5" placeholder="Agregue información relevante sobre este artículo..."
                                          class="w-full rounded-xl border-gray-200 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-100 transition-all py-3 px-4 resize-none"></textarea>
                            </div>
                            
                            <div class="p-6 bg-blue-50 rounded-2xl border border-blue-100">
                                <h4 class="text-xs font-black text-blue-800 uppercase tracking-widest mb-3 flex items-center">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0116 0z" />
                                    </svg>
                                    Tip para el usuario
                                </h4>
                                <p class="text-sm text-blue-700 leading-relaxed font-medium">
                                    Recuerde que este código se utilizará para vincular las reservas externas automáticas. Mantenga los códigos sincronizados con su sistema de cupones.
                                </p>
                            </div>
                        </div>
                    </div>

                    <!-- Ventas Tab -->
                    <div v-show="activeTab === 'ventas'" class="grid grid-cols-1 md:grid-cols-2 gap-12 animate-fadeIn">
                        <div class="space-y-6">
                            <h4 class="text-xs font-black text-gray-800 uppercase tracking-widest border-b border-gray-100 pb-3">Impuestos de Venta</h4>
                            <div>
                                <label class="block text-xs font-bold text-gray-500 uppercase tracking-widest mb-2">IVA Venta predeterminado</label>
                                <select v-model="form.impuesto_venta_id" 
                                        class="w-full rounded-xl border-gray-200 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-100 py-3 px-4 transition-all">
                                    <option :value="undefined">Sin impuestos de venta</option>
                                    <option v-for="tax in filteredVentaTaxes" :key="tax.id" :value="tax.id">
                                        {{ tax.nombre }} ({{ tax.importe }}%)
                                    </option>
                                </select>
                            </div>
                        </div>
                        <div class="p-6 bg-gray-50 rounded-2xl border border-gray-100 flex flex-col justify-center">
                             <div class="text-center">
                                <div class="inline-flex items-center justify-center p-3 bg-white rounded-full shadow-sm mb-4">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0116 0z" />
                                    </svg>
                                </div>
                                <h5 class="font-bold text-gray-800">Cálculo Automático</h5>
                                <p class="text-xs text-gray-500 mt-2">Al seleccionar este impuesto, se aplicará automáticamente a cada línea de factura cuando se use este artículo.</p>
                             </div>
                        </div>
                    </div>

                    <!-- Compras Tab -->
                    <div v-show="activeTab === 'compras'" class="grid grid-cols-1 md:grid-cols-2 gap-12 animate-fadeIn">
                        <div class="space-y-6">
                            <h4 class="text-xs font-black text-gray-800 uppercase tracking-widest border-b border-gray-100 pb-3">Costos e Impuestos de Compra</h4>
                            <div>
                                <label class="block text-xs font-bold text-gray-500 uppercase tracking-widest mb-2">Precio de Costo</label>
                                <div class="relative rounded-xl shadow-sm max-w-[200px]">
                                    <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                        <span class="text-gray-400 font-bold">$</span>
                                    </div>
                                    <input v-model="form.precio_costo" type="number" step="0.01" 
                                           class="block w-full pl-8 pr-4 py-2.5 rounded-xl border-gray-200 font-medium bg-white focus:ring-blue-200 focus:border-blue-500 transition-all font-mono" />
                                </div>
                            </div>
                            <div>
                                <label class="block text-xs font-bold text-gray-500 uppercase tracking-widest mb-2">Impuestos de Compra</label>
                                <select v-model="form.impuesto_compra_id" 
                                        class="w-full rounded-xl border-gray-200 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-100 py-3 px-4 transition-all">
                                    <option :value="undefined">Sin impuestos de compra</option>
                                    <option v-for="tax in filteredCompraTaxes" :key="tax.id" :value="tax.id">
                                        {{ tax.nombre }} ({{ tax.importe }}%)
                                    </option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </fieldset>

        <!-- Action Bar -->
        <div class="px-8 py-6 bg-gray-50 border-t border-gray-100 flex justify-between items-center sm:px-10">
            <button type="button" @click="$emit('cancel')" 
                    class="px-6 py-2.5 text-sm font-bold text-gray-500 hover:text-gray-700 bg-white border border-gray-300 rounded-xl hover:bg-gray-100 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-200 shadow-sm">
                Descartar
            </button>
            
            <div class="flex space-x-4">
                <button v-if="isDeleteMode" type="submit" 
                        class="px-8 py-2.5 text-sm font-black text-white bg-red-600 border border-transparent rounded-xl hover:bg-red-700 focus:ring-4 focus:ring-red-200 transition-all duration-300 shadow-lg shadow-red-200 uppercase tracking-widest">
                    Confirmar Eliminación
                </button>
                <button v-else type="submit" 
                        class="px-10 py-2.5 text-sm font-black text-white bg-blue-600 border border-transparent rounded-xl hover:bg-blue-700 focus:ring-4 focus:ring-blue-200 transition-all duration-300 shadow-lg shadow-blue-200 uppercase tracking-widest">
                    {{ modelValue ? 'Actualizar Artículo' : 'Crear Artículo' }}
                </button>
            </div>
        </div>
    </form>
  </div>
</template>

<style scoped>
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}

.animate-fadeIn {
  animation: fadeIn 0.4s ease-out forwards;
}

.animate-shake {
  animation: shake 0.3s ease-in-out;
}

.scroller-hide::-webkit-scrollbar {
  display: none;
}
.scroller-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

input:focus, select:focus, textarea:focus {
    transform: scale(1.005);
}
</style>
