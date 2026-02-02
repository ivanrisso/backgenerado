
<script setup lang="ts">
import { ref, watch } from 'vue';
import type { Domicilio } from '@domain/entities/Domicilio';

const props = defineProps<{
    modelValue: Domicilio | null;
}>();

const emit = defineEmits<{
    (e: 'submit', entity: Domicilio): void;
    (e: 'cancel'): void;
}>();

const form = ref({
    id: 0,
    calle: '',
    numero: 0,
    cliente_id: 0,
    tipo_dom_id: 0,
    localidad_id: 0
});

watch(() => props.modelValue, (newVal) => {
    if (newVal) {
        form.value = { ...newVal };
    } else {
        form.value = { id: 0, calle: '', numero: 0, cliente_id: 0, tipo_dom_id: 0, localidad_id: 0 };
    }
}, { immediate: true });

const handleSubmit = () => {
    const entity: Domicilio = {
        id: form.value.id,
        calle: form.value.calle,
        numero: Number(form.value.numero),
        cliente_id: Number(form.value.cliente_id),
        tipo_dom_id: Number(form.value.tipo_dom_id),
        localidad_id: Number(form.value.localidad_id)
    };
    emit('submit', entity);
};
</script>

<template>
  <div class="bg-gray-50 p-4 rounded-lg border border-gray-200 mb-4">
    <h3 class="text-lg font-medium text-gray-900 mb-4">
      {{ modelValue ? 'Editar' : 'Nuevo' }} Domicilio
    </h3>
    <form class="space-y-4" @submit.prevent="handleSubmit">
      <div>
        <label class="block text-sm font-medium text-gray-700">Calle</label>
        <input v-model="form.calle" type="text" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm">
      </div>
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700">Número</label>
          <input v-model="form.numero" type="number" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm">
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Cliente ID</label>
          <input v-model="form.cliente_id" type="number" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm">
        </div>
      </div>
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700">Tipo Domicilio ID</label>
          <input v-model="form.tipo_dom_id" type="number" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm">
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Localidad ID</label>
          <input v-model="form.localidad_id" type="number" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm">
        </div>
      </div>
      <div class="flex justify-end gap-2">
        <button type="button" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50" @click="$emit('cancel')">
          Cancelar
        </button>
        <button type="submit" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700">
          Guardar
        </button>
      </div>
    </form>
  </div>
</template>
