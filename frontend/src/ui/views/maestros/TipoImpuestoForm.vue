
<script setup lang="ts">
import { ref, watch } from 'vue';
import type { TipoImpuesto } from '../../../domain/entities/TipoImpuesto';
import { TipoAplicacionEnum } from '../../../domain/enums/TipoAplicacionEnum';
import { BaseTributarioEnum } from '../../../domain/enums/BaseTributarioEnum';

const props = defineProps<{
    modelValue: TipoImpuesto | null;
}>();

const emit = defineEmits<{
    (e: 'submit', entity: TipoImpuesto): void;
    (e: 'cancel'): void;
}>();

const form = ref({
    id: 0,
    codigo_afip: '',
    nombre: '',
    descripcion: '',
    tipo_aplicacion: TipoAplicacionEnum.SUMA, // Default
    base_calculo: BaseTributarioEnum.NETO_GRAVADO, // Default
    porcentaje: 0,
    editable: true,
    obligatorio: false,
    activo: true
});

watch(() => props.modelValue, (newVal) => {
    if (newVal) {
        form.value = { ...newVal, porcentaje: newVal.porcentaje || 0 };
    } else {
        form.value = {
            id: 0, codigo_afip: '', nombre: '', descripcion: '',
            tipo_aplicacion: TipoAplicacionEnum.SUMA,
            base_calculo: BaseTributarioEnum.NETO_GRAVADO,
            porcentaje: 0, editable: true, obligatorio: false, activo: true
        };
    }
}, { immediate: true });

const handleSubmit = () => {
    const entity: TipoImpuesto = {
        id: form.value.id,
        codigo_afip: form.value.codigo_afip,
        nombre: form.value.nombre,
        descripcion: form.value.descripcion,
        tipo_aplicacion: form.value.tipo_aplicacion,
        base_calculo: form.value.base_calculo,
        porcentaje: Number(form.value.porcentaje),
        editable: form.value.editable,
        obligatorio: form.value.obligatorio,
        activo: form.value.activo
    };
    emit('submit', entity);
};
</script>

<template>
  <div class="bg-gray-50 p-4 rounded-lg border border-gray-200 mb-4">
    <h3 class="text-lg font-medium text-gray-900 mb-4">{{ modelValue ? 'Editar' : 'Nuevo' }} Tipo de Impuesto</h3>
    <form @submit.prevent="handleSubmit" class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
            <div>
                <label class="block text-sm font-medium text-gray-700">Código AFIP</label>
                <input v-model="form.codigo_afip" type="text" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" />
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700">Nombre</label>
                <input v-model="form.nombre" type="text" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" />
            </div>
        </div>
        <div>
            <label class="block text-sm font-medium text-gray-700">Descripción</label>
            <input v-model="form.descripcion" type="text" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" />
        </div>
        <div class="grid grid-cols-2 gap-4">
             <div>
                <label class="block text-sm font-medium text-gray-700">Aplicación</label>
                <select v-model="form.tipo_aplicacion" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm">
                    <option value="suma">Se Suma</option>
                    <option value="descuento">Se Resta</option>
                    <option value="neutro">Neutro</option>
                </select>
            </div>
            <div>
                 <label class="block text-sm font-medium text-gray-700">Base Cálculo</label>
                 <select v-model="form.base_calculo" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm">
                    <option value="neto_gravado">Neto Gravado</option>
                    <option value="total">Total Factura</option>
                    <option value="subtotal">Subtotal</option>
                    <option value="otros">Otros</option>
                 </select>
            </div>
        </div>
        <div>
             <label class="block text-sm font-medium text-gray-700">Porcentaje (%)</label>
             <input v-model="form.porcentaje" type="number" step="0.01" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" />
        </div>
        
        <div class="flex space-x-6">
            <div class="flex items-center">
                <input v-model="form.activo" type="checkbox" class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded" />
                <label class="ml-2 block text-sm text-gray-900">Activo</label>
            </div>
             <div class="flex items-center">
                <input v-model="form.obligatorio" type="checkbox" class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded" />
                <label class="ml-2 block text-sm text-gray-900">Obligatorio</label>
            </div>
             <div class="flex items-center">
                <input v-model="form.editable" type="checkbox" class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded" />
                <label class="ml-2 block text-sm text-gray-900">Editable</label>
            </div>
        </div>

        <div class="flex justify-end gap-2">
            <button type="button" @click="$emit('cancel')" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50">Cancelar</button>
            <button type="submit" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700">Guardar</button>
        </div>
    </form>
  </div>
</template>
