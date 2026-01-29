<script setup lang="ts">
import { ref, watch } from 'vue';
import { Rol } from '../../../domain/entities/Rol';

const props = defineProps<{
    modelValue: Rol | null;
}>();

const emit = defineEmits<{
    (e: 'submit', entity: Rol): void;
    (e: 'cancel'): void;
}>();

const form = ref({
    id: 0,
    rolNombre: '',
    esAdmin: false
});

watch(() => props.modelValue, (newVal) => {
    if (newVal) {
        form.value = {
            id: newVal.id,
            rolNombre: newVal.rolNombre,
            esAdmin: newVal.esAdmin
        };
    } else {
        form.value = { id: 0, rolNombre: '', esAdmin: false };
    }
}, { immediate: true });

const handleSubmit = () => {
    try {
        const entity = new Rol(
            form.value.id,
            form.value.rolNombre,
            form.value.esAdmin
        );
        emit('submit', entity);
    } catch (e: any) {
        alert(e.message);
    }
};
</script>

<template>
  <div class="bg-gray-50 p-6 rounded-lg border border-gray-200 mb-6 shadow-sm">
    <h3 class="text-lg font-medium text-gray-900 mb-4">
      {{ modelValue ? 'Editar' : 'Nuevo' }} Rol
    </h3>
    <form class="space-y-4" @submit.prevent="handleSubmit">
      <div>
        <label class="block text-sm font-medium text-gray-700">Nombre del Rol</label>
        <input v-model="form.rolNombre" type="text" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border">
      </div>
        
      <div class="flex items-center">
        <input id="esAdmin" v-model="form.esAdmin" type="checkbox" class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded">
        <label for="esAdmin" class="ml-2 block text-sm text-gray-900">
          Es Administrador (Acceso Total)
        </label>
      </div>

      <div class="flex justify-end gap-3 pt-2">
        <button type="button" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500" @click="$emit('cancel')">
          Cancelar
        </button>
        <button type="submit" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
          Guardar
        </button>
      </div>
    </form>
  </div>
</template>
