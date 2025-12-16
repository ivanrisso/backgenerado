<script setup lang="ts">
import { ref, watch } from 'vue';
import { Pais } from '../../../domain/entities/Pais';
import { CodigoPais } from '../../../domain/value-objects/CodigoPais';

const props = defineProps<{
    modelValue: Pais | null;
}>();

const emit = defineEmits<{
    (e: 'submit', entity: Pais): void;
    (e: 'cancel'): void;
}>();

const form = ref({
    id: 0,
    nombre: '',
    codigo: ''
});

watch(() => props.modelValue, (newVal) => {
    if (newVal) {
        form.value = { id: newVal.id, nombre: newVal.nombre, codigo: newVal.codigo.value };
    } else {
        form.value = { id: 0, nombre: '', codigo: '' };
    }
}, { immediate: true });

const handleSubmit = () => {
    try {
        const codigoPaisVo = new CodigoPais(form.value.codigo);
        const entity = new Pais(
            form.value.id,
            form.value.nombre,
            codigoPaisVo
        );
        emit('submit', entity);
    } catch (e: any) {
        alert(e.message);
    }
};
</script>

<template>
  <div class="bg-gray-50 p-4 rounded-lg border border-gray-200 mb-4">
    <h3 class="text-lg font-medium text-gray-900 mb-4">{{ modelValue ? 'Editar' : 'Nuevo' }} País</h3>
    <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
            <label class="block text-sm font-medium text-gray-700">Nombre</label>
            <input v-model="form.nombre" type="text" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" />
        </div>
        <div>
            <label class="block text-sm font-medium text-gray-700">Código</label>
            <input v-model="form.codigo" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" placeholder="AR" />
            <p class="text-xs text-gray-500 mt-1">2 o 3 letras.</p>
        </div>
        <div class="flex justify-end gap-2">
            <button type="button" @click="$emit('cancel')" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50">Cancelar</button>
            <button type="submit" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700">Guardar</button>
        </div>
    </form>
  </div>
</template>
