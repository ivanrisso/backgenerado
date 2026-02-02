
<script setup lang="ts">
import { ref, watch } from 'vue';
import { TipoReparticionBaseImpuestoEnum } from '@domain/entities/TipoImpuestoDistribucion';

const props = defineProps<{
    modelValue: any[];
}>();

const emit = defineEmits(['update:modelValue']);

const items = ref<any[]>([]);

watch(() => props.modelValue, (newVal) => {
    items.value = newVal || [];
}, { immediate: true, deep: true });

const addItem = () => {
    const newItem = {
        factor_porcentaje: 100,
        basado_en: TipoReparticionBaseImpuestoEnum.BASE,
        cuenta_contable: '',
        etiqueta_nombre: ''
    };
    const newHistory = [...items.value, newItem];
    emit('update:modelValue', newHistory);
};

const removeItem = (index: number) => {
     const newHistory = [...items.value];
     newHistory.splice(index, 1);
     emit('update:modelValue', newHistory);
};

const updateItem = () => {
    emit('update:modelValue', items.value);
};
</script>

<template>
<div class="border rounded-lg overflow-hidden">
    <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
            <tr>
                <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase">Basado En</th>
                <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase">% Factor</th>
                <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase">Cuenta</th>
                <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase">Etiqueta</th>
                <th class="px-3 py-2 w-10"></th>
            </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="(item, idx) in items" :key="idx">
                <td class="px-3 py-2">
                    <select v-model="item.basado_en" @change="updateItem" class="block w-full text-sm border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500">
                        <option :value="TipoReparticionBaseImpuestoEnum.BASE">Base</option>
                        <option :value="TipoReparticionBaseImpuestoEnum.IMPUESTO">Impuesto</option>
                    </select>
                </td>
                <td class="px-3 py-2">
                    <input type="number" v-model.number="item.factor_porcentaje" @input="updateItem" class="block w-full text-sm border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500" />
                </td>
                 <td class="px-3 py-2">
                    <input type="text" v-model="item.cuenta_contable" @input="updateItem" placeholder="Ej: 1.0.0.1" class="block w-full text-sm border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500" />
                </td>
                 <td class="px-3 py-2">
                    <input type="text" v-model="item.etiqueta_nombre" @input="updateItem" placeholder="Etiqueta" class="block w-full text-sm border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500" />
                </td>
                <td class="px-3 py-2 text-right">
                    <button type="button" @click="removeItem(idx)" class="text-red-600 hover:text-red-900">
                        <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                    </button>
                </td>
            </tr>
            <tr v-if="items.length === 0">
                <td colspan="5" class="px-3 py-4 text-center text-sm text-gray-500">Sin reglas de distribución</td>
            </tr>
        </tbody>
    </table>
    <div class="bg-gray-50 px-3 py-2 border-t border-gray-200">
        <button type="button" @click="addItem" class="text-xs font-semibold text-blue-600 hover:text-blue-800 flex items-center">
            <svg class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" /></svg>
            Agregar Línea
        </button>
    </div>
</div>
</template>
