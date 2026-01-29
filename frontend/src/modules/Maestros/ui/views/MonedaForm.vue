
<script setup lang="ts">
import { ref, watch } from 'vue';
import type { Moneda } from '../../../domain/entities/Moneda';

const props = defineProps<{
    modelValue: Moneda | null;
    isDeleteMode?: boolean;
    serverError?: string | null;
}>();

const emit = defineEmits<{
    (e: 'submit', entity: Moneda): void;
    (e: 'delete', id: number): void;
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
    if (props.isDeleteMode) {
        emit('delete', form.value.id);
        return;
    }
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
  <div class="max-w-2xl mx-auto card p-0 overflow-hidden">
    <div class="px-6 py-4 border-b border-gray-100 bg-gray-50 flex justify-between items-center">
      <h3 class="text-lg font-bold text-gray-900">
        {{ isDeleteMode ? 'Eliminar' : (modelValue ? 'Editar' : 'Nueva') }} Moneda
      </h3>
      <button class="text-gray-400 hover:text-gray-600" @click="$emit('cancel')">
        <span class="sr-only">Cerrar</span>
        <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
      </button>
    </div>
    
    <div v-if="serverError" class="mx-6 mt-4 p-3 bg-red-100 text-red-700 border border-red-200 rounded-md">
      {{ serverError }}
    </div>

    <div v-if="isDeleteMode" class="mx-6 mt-4 p-3 bg-yellow-50 text-yellow-800 border border-yellow-200 rounded-md">
      ¿Está seguro que desea eliminar este registro? Esta acción no se puede deshacer.
    </div>

    <form class="p-6 space-y-4" @submit.prevent="handleSubmit">
      <fieldset :disabled="isDeleteMode" class="disabled:opacity-75 space-y-4">
        <div>
          <label class="input-label">Descripción</label>
          <input v-model="form.descripcion" type="text" required class="input-field disabled:bg-gray-100" placeholder="Ej. Peso Argentino">
          <p class="input-helper">
            Nombre completo de la moneda.
          </p>
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="input-label">Código ISO</label>
            <input v-model="form.codigo" type="text" required class="input-field font-mono disabled:bg-gray-100" placeholder="ARS">
            <p class="input-helper">
              Código único (3 letras).
            </p>
          </div>
          <div>
            <label class="input-label">Código ARCA</label>
            <input v-model="form.codigo_arca" type="text" class="input-field font-mono disabled:bg-gray-100" placeholder="PES">
            <p class="input-helper">
              Código para facturación electrónica.
            </p>
          </div>
        </div>
      </fieldset>

      <div class="pt-4 flex justify-end gap-3 border-t border-gray-50 mt-6">
        <button type="button" class="btn btn-secondary" @click="$emit('cancel')">
          Cancelar
        </button>
        <button v-if="isDeleteMode" type="submit" class="btn bg-red-600 text-white hover:bg-red-700">
          Eliminar
        </button>
        <button v-else type="submit" class="btn btn-primary">
          Guardar Moneda
        </button>
      </div>
    </form>
  </div>
</template>
