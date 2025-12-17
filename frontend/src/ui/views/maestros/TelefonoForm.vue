
<script setup lang="ts">
import { ref, watch } from 'vue';
import type { Telefono } from '../../../domain/entities/Telefono';

const props = defineProps<{
    modelValue: Telefono | null;
}>();

const emit = defineEmits<{
    (e: 'submit', entity: Telefono): void;
    (e: 'cancel'): void;
}>();

const form = ref({
    id: 0,
    prefijo: '',
    numero: '',
    tipo_tel_id: 0,
    domicilio_id: 0
});

watch(() => props.modelValue, (newVal) => {
    if (newVal) {
        form.value = { ...newVal };
    } else {
        form.value = { id: 0, prefijo: '', numero: '', tipo_tel_id: 0, domicilio_id: 0 };
    }
}, { immediate: true });

const handleSubmit = () => {
    const entity: Telefono = {
        id: form.value.id,
        prefijo: form.value.prefijo,
        numero: form.value.numero,
        tipo_tel_id: Number(form.value.tipo_tel_id),
        domicilio_id: Number(form.value.domicilio_id)
    };
    emit('submit', entity);
};
</script>

<template>
  <div class="bg-gray-50 p-4 rounded-lg border border-gray-200 mb-4">
    <h3 class="text-lg font-medium text-gray-900 mb-4">{{ modelValue ? 'Editar' : 'Nuevo' }} Teléfono</h3>
    <form @submit.prevent="handleSubmit" class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
            <div>
                 <label class="block text-sm font-medium text-gray-700">Prefijo</label>
                 <input v-model="form.prefijo" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" />
            </div>
            <div>
                 <label class="block text-sm font-medium text-gray-700">Número</label>
                 <input v-model="form.numero" type="text" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" />
            </div>
        </div>
         <div class="grid grid-cols-2 gap-4">
             <div>
                <label class="block text-sm font-medium text-gray-700">Tipo Teléfono ID</label>
                <input v-model="form.tipo_tel_id" type="number" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" />
            </div>
            <div>
                 <label class="block text-sm font-medium text-gray-700">Domicilio ID</label>
                 <input v-model="form.domicilio_id" type="number" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" />
            </div>
        </div>
        <div class="flex justify-end gap-2">
            <button type="button" @click="$emit('cancel')" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50">Cancelar</button>
            <button type="submit" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700">Guardar</button>
        </div>
    </form>
  </div>
</template>
