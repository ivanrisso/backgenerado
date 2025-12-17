
<script setup lang="ts">
import { ref, watch } from 'vue';
import type { Moneda } from '../../../domain/entities/Moneda';

const props = defineProps<{
    modelValue: Moneda | null;
}>();

const emit = defineEmits<{
    (e: 'submit', entity: Moneda): void;
    (e: 'cancel'): void;
}>();

const form = ref({
    id: 0,
    codigo: '',
    descripcion: '',
    codigo_arca: ''
});

watch(() => props.modelValue, (newVal) => {
    if (newVal) {
        form.value = {
            id: newVal.id,
            codigo: newVal.codigo,
            descripcion: newVal.descripcion,
            codigo_arca: newVal.codigo_arca
        };
    } else {
        form.value = { id: 0, codigo: '', descripcion: '', codigo_arca: '' };
    }
}, { immediate: true });

const handleSubmit = () => {
    const entity: Moneda = {
        id: form.value.id,
        codigo: form.value.codigo,
        descripcion: form.value.descripcion,
        codigo_arca: form.value.codigo_arca
    };
    emit('submit', entity);
};
</script>

<template>
  <div class="bg-gray-50 p-4 rounded-lg border border-gray-200 mb-4">
    <h3 class="text-lg font-medium text-gray-900 mb-4">{{ modelValue ? 'Editar' : 'Nueva' }} Moneda</h3>
    <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
            <label class="block text-sm font-medium text-gray-700">Código</label>
            <input v-model="form.codigo" type="text" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" />
        </div>
        <div>
            <label class="block text-sm font-medium text-gray-700">Descripción</label>
            <input v-model="form.descripcion" type="text" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" />
        </div>
        <div>
            <label class="block text-sm font-medium text-gray-700">Código ARCA</label>
            <input v-model="form.codigo_arca" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" />
        </div>
        <div class="flex justify-end gap-2">
            <button type="button" @click="$emit('cancel')" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50">Cancelar</button>
            <button type="submit" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700">Guardar</button>
        </div>
    </form>
  </div>
</template>
