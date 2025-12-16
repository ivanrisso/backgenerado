<script setup lang="ts">
import { ref, watch } from 'vue';
import type { TipoDom } from '../../../domain/entities/TipoDom';

const props = defineProps<{
    modelValue: TipoDom | null;
}>();

const emit = defineEmits<{
    (e: 'submit', entity: TipoDom): void;
    (e: 'cancel'): void;
}>();

const form = ref({
    id: 0,
    nombre: ''
});

watch(() => props.modelValue, (newVal) => {
    if (newVal) {
        form.value = { id: newVal.id, nombre: newVal.nombre };
    } else {
        form.value = { id: 0, nombre: '' };
    }
}, { immediate: true });

const handleSubmit = () => {
    const entity = {
        id: form.value.id,
        nombre: form.value.nombre
    } as unknown as TipoDom;
    emit('submit', entity);
};
</script>

<template>
  <div class="bg-gray-50 p-4 rounded-lg border border-gray-200 mb-4">
    <h3 class="text-lg font-medium text-gray-900 mb-4">{{ modelValue ? 'Editar' : 'Nuevo' }} Tipo de Domicilio</h3>
    <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
            <label class="block text-sm font-medium text-gray-700">Nombre</label>
            <input v-model="form.nombre" type="text" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" />
        </div>
        <div class="flex justify-end gap-2">
            <button type="button" @click="$emit('cancel')" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50">Cancelar</button>
            <button type="submit" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700">Guardar</button>
        </div>
    </form>
  </div>
</template>
