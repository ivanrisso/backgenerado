
<script setup lang="ts">
import { ref, watch } from 'vue';
import type { Operador } from '../../../domain/entities/Operador';

const props = defineProps<{
    modelValue: Operador | null;
}>();

const emit = defineEmits<{
    (e: 'submit', entity: Operador): void;
    (e: 'cancel'): void;
}>();

const form = ref({
    id: 0,
    cliente_id: 0
});

watch(() => props.modelValue, (newVal) => {
    if (newVal) {
        form.value = { ...newVal };
    } else {
        form.value = { id: 0, cliente_id: 0 };
    }
}, { immediate: true });

const handleSubmit = () => {
    const entity: Operador = {
        id: form.value.id,
        cliente_id: form.value.cliente_id
    };
    emit('submit', entity);
};
</script>

<template>
  <div class="bg-gray-50 p-4 rounded-lg border border-gray-200 mb-4">
    <h3 class="text-lg font-medium text-gray-900 mb-4">{{ modelValue ? 'Editar' : 'Nuevo' }} Operador</h3>
    <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
            <label class="block text-sm font-medium text-gray-700">ID Cliente</label>
            <input v-model="form.cliente_id" type="number" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" />
            <p class="text-xs text-gray-500 mt-1">ID del Cliente asociado.</p>
        </div>
        <div class="flex justify-end gap-2">
            <button type="button" @click="$emit('cancel')" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50">Cancelar</button>
            <button type="submit" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700">Guardar</button>
        </div>
    </form>
  </div>
</template>
