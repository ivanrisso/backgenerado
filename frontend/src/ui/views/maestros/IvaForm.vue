
<script setup lang="ts">
import { ref, watch } from 'vue';
import type { Iva } from '../../../domain/entities/Iva';

const props = defineProps<{
    modelValue: Iva | null;
    isDeleteMode?: boolean;
    serverError?: string | null;
}>();

const emit = defineEmits<{
    (e: 'submit', entity: Iva): void;
    (e: 'delete', id: number): void;
    (e: 'cancel'): void;
}>();

const form = ref({
    id: 0,
    codigo: 0,
    descripcion: '',
    porcentaje: 0,
    discriminado: true,
    porcentaje_sobre: 0
});

watch(() => props.modelValue, (newVal) => {
    if (newVal) {
        form.value = { ...newVal };
    } else {
        form.value = { id: 0, codigo: 0, descripcion: '', porcentaje: 21, discriminado: true, porcentaje_sobre: 0 };
    }
}, { immediate: true });

const handleSubmit = () => {
    if (props.isDeleteMode) {
        emit('delete', form.value.id);
        return;
    }

    const entity: Iva = {
        id: form.value.id,
        codigo: Number(form.value.codigo),
        descripcion: form.value.descripcion,
        porcentaje: Number(form.value.porcentaje),
        discriminado: form.value.discriminado,
        porcentaje_sobre: Number(form.value.porcentaje_sobre)
    };
    emit('submit', entity);
};
</script>

<template>
  <div class="bg-gray-50 p-4 rounded-lg border border-gray-200 mb-4">
    <h3 class="text-lg font-medium text-gray-900 mb-4">
        {{ isDeleteMode ? 'Eliminar' : (modelValue ? 'Editar' : 'Nuevo') }} IVA
    </h3>

    <div v-if="serverError" class="mb-4 p-3 bg-red-100 text-red-700 border border-red-200 rounded-md">
        {{ serverError }}
    </div>

    <div v-if="isDeleteMode" class="mb-4 p-3 bg-yellow-50 text-yellow-800 border border-yellow-200 rounded-md">
        ¿Está seguro que desea eliminar este registro? Esta acción no se puede deshacer.
    </div>

    <form @submit.prevent="handleSubmit" class="space-y-4">
        <fieldset :disabled="isDeleteMode" class="disabled:opacity-75 space-y-4">
            <div class="grid grid-cols-2 gap-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700">Código</label>
                    <input v-model="form.codigo" type="number" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm disabled:bg-gray-100" />
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700">Porcentaje (%)</label>
                    <input v-model="form.porcentaje" type="number" step="0.01" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm disabled:bg-gray-100" />
                </div>
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700">Descripción</label>
                <input v-model="form.descripcion" type="text" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm disabled:bg-gray-100" />
            </div>
            
            <div class="flex items-center">
                <input v-model="form.discriminado" type="checkbox" class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded disabled:bg-gray-100" />
                <label class="ml-2 block text-sm text-gray-900">Discriminado</label>
            </div>
        </fieldset>

        <div class="flex justify-end gap-2">
            <button type="button" @click="$emit('cancel')" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50">Cancelar</button>
            
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
