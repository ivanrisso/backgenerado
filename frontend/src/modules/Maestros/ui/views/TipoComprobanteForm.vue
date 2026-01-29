
<script setup lang="ts">
import { ref, watch } from 'vue';
import type { TipoComprobante } from '../../../domain/entities/TipoComprobante';

const props = defineProps<{
    modelValue: TipoComprobante | null;
    isDeleteMode?: boolean;
    serverError?: string | null;
}>();

const emit = defineEmits<{
    (e: 'submit', entity: TipoComprobante): void;
    (e: 'delete', id: number): void;
    (e: 'cancel'): void;
}>();

const form = ref({
    id: 0,
    codigo: '',
    descripcion: '',
    es_fiscal: false,
    codigo_arca: ''
});

watch(() => props.modelValue, (newVal) => {
    if (newVal) {
        form.value = {
            id: newVal.id,
            codigo: newVal.codigo,
            descripcion: newVal.descripcion,
            es_fiscal: newVal.es_fiscal,
            codigo_arca: newVal.codigo_arca
        };
    } else {
        form.value = { id: 0, codigo: '', descripcion: '', es_fiscal: false, codigo_arca: '' };
    }
}, { immediate: true });

const handleSubmit = () => {
    if (props.isDeleteMode) {
        emit('delete', form.value.id);
        return;
    }
    const entity: TipoComprobante = {
        id: form.value.id,
        codigo: form.value.codigo,
        descripcion: form.value.descripcion,
        es_fiscal: form.value.es_fiscal,
        codigo_arca: form.value.codigo_arca
    };
    emit('submit', entity);
};
</script>

<template>
  <div class="bg-gray-50 p-4 rounded-lg border border-gray-200 mb-4">
    <h3 class="text-lg font-medium text-gray-900 mb-4">
      {{ isDeleteMode ? 'Eliminar' : (modelValue ? 'Editar' : 'Nuevo') }} Tipo de Comprobante
    </h3>

    <div v-if="serverError" class="mb-4 p-3 bg-red-100 text-red-700 border border-red-200 rounded-md">
      {{ serverError }}
    </div>

    <div v-if="isDeleteMode" class="mb-4 p-3 bg-yellow-50 text-yellow-800 border border-yellow-200 rounded-md">
      ¿Está seguro que desea eliminar este registro? Esta acción no se puede deshacer.
    </div>

    <form class="space-y-4" @submit.prevent="handleSubmit">
      <fieldset :disabled="isDeleteMode" class="disabled:opacity-75 space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700">Código</label>
          <input v-model="form.codigo" type="text" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm disabled:bg-gray-100">
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Descripción</label>
          <input v-model="form.descripcion" type="text" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm disabled:bg-gray-100">
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Código ARCA</label>
          <input v-model="form.codigo_arca" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm disabled:bg-gray-100">
        </div>
        <div class="flex items-center">
          <input v-model="form.es_fiscal" type="checkbox" class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded disabled:text-gray-400">
          <label class="ml-2 block text-sm text-gray-900">Fiscal</label>
        </div>
      </fieldset>

      <div class="flex justify-end gap-2">
        <button type="button" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50" @click="$emit('cancel')">
          Cancelar
        </button>
        <button v-if="isDeleteMode" type="submit" class="px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-md hover:bg-red-700 focus:ring-red-500">
          Eliminar
        </button>
        <button v-else type="submit" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700">
          Guardar
        </button>
      </div>
    </form>
  </div>
</template>
