<script setup lang="ts">
import { ref, watch } from 'vue';
import { Provincia } from '../../../domain/entities/Provincia';


const props = defineProps<{
    modelValue: Provincia | null;
    initialPaisId: number | null; // Pre-select pais
    paises: any[];
    isDeleteMode?: boolean;
    serverError?: string | null;
}>();

const emit = defineEmits<{
    (e: 'submit', entity: Provincia): void;
    (e: 'delete', id: number): void;
    (e: 'cancel'): void;
}>();

const form = ref({
    id: 0,
    nombre: '',
    paisId: 0
});

// Update form when modelValue (editing) changes
watch(() => props.modelValue, (newVal) => {
    if (newVal) {
        form.value = { id: newVal.id, nombre: newVal.nombre, paisId: newVal.paisId };
    } else {
        // Only set default if not editing
        if (!form.value.id) {
             form.value.paisId = props.initialPaisId || 0;
             form.value.nombre = '';
             form.value.id = 0;
        }
    }
}, { immediate: true });

// Update form default when initialPaisId changes (only if in creation mode)
watch(() => props.initialPaisId, (newId) => {
    if (!props.modelValue && newId) {
        form.value.paisId = newId;
    }
});

const handleSubmit = () => {
    if (props.isDeleteMode) {
        emit('delete', form.value.id);
        return;
    }
    if(!form.value.paisId) {
        alert("Debe seleccionar un país");
        return;
    }
    const entity = new Provincia(
        form.value.id,
        form.value.nombre,
        form.value.paisId
    );
    emit('submit', entity);
};
</script>

<template>
  <div class="bg-gray-50 p-4 rounded-lg border border-gray-200 mb-4">
    <h3 class="text-lg font-medium text-gray-900 mb-4">
      {{ isDeleteMode ? 'Eliminar' : (modelValue ? 'Editar' : 'Nueva') }} Provincia
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
          <label class="block text-sm font-medium text-gray-700">País</label>
          <select v-model="form.paisId" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm disabled:bg-gray-100">
            <option :value="0" disabled>
              Seleccione un país
            </option>
            <option v-for="p in paises" :key="p.id" :value="p.id">
              {{ p.nombre }}
            </option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Nombre</label>
          <input v-model="form.nombre" type="text" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm disabled:bg-gray-100">
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
