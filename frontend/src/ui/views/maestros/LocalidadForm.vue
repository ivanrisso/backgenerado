<script setup lang="ts">
import { ref, watch } from 'vue';
import type { Localidad } from '../../../domain/entities/Localidad';
import { Localidad as LocalidadEntity } from '../../../domain/entities/Localidad'; // Alias to avoid conflict with types if needed, or just use same name if class
import type { Provincia } from '../../../domain/entities/Provincia';

const props = defineProps<{
    modelValue: Localidad | null;
    initialProvinciaId: number | null;
    initialPaisId: number | null;
    provincias: Provincia[];
    paises: any[];
}>();

const emit = defineEmits<{
    (e: 'submit', entity: Localidad): void;
    (e: 'cancel'): void;
    (e: 'change-pais', id: number): void;
}>();

const form = ref({
    id: 0,
    nombre: '',
    codPostal: '',
    provinciaId: 0,
    paisId: 0
});

// Update form when modelValue (editing) changes
watch(() => props.modelValue, (newVal) => {
    if (newVal) {
        form.value = { 
            id: newVal.id, 
            nombre: newVal.nombre, 
            codPostal: newVal.codPostal, 
            provinciaId: newVal.provinciaId,
            paisId: props.initialPaisId || 0
        };
    } else {
        // Only set default if not editing
        if (!form.value.id) {
            form.value = { 
                id: 0, 
                nombre: '', 
                codPostal: '', 
                provinciaId: props.initialProvinciaId || 0,
                paisId: props.initialPaisId || 0
            };
        }
    }
}, { immediate: true });

// Update form default when initialProvinciaId changes
watch(() => props.initialProvinciaId, (newId) => {
    if (!props.modelValue && newId) {
        form.value.provinciaId = newId;
    }
});

watch(() => props.initialPaisId, (newId) => {
    // Sync external changes to internal state
    if (newId) form.value.paisId = newId;
});

const onPaisChange = () => {
    emit('change-pais', Number(form.value.paisId));
    form.value.provinciaId = 0; // Reset provincia when country changes
};

const handleSubmit = () => {
    if(!form.value.provinciaId) {
        alert("Debe seleccionar una provincia");
        return;
    }
    
    try {
        const entity = new LocalidadEntity(
            form.value.id,
            form.value.nombre,
            form.value.codPostal,
            form.value.provinciaId
        );
        emit('submit', entity);
    } catch (e: any) {
        alert(e.message);
    }
};
</script>

<template>
  <div class="bg-gray-50 p-4 rounded-lg border border-gray-200 mb-4">
    <h3 class="text-lg font-medium text-gray-900 mb-4">{{ modelValue ? 'Editar' : 'Nueva' }} Localidad</h3>
    <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
            <label class="block text-sm font-medium text-gray-700">País</label>
            <select v-model="form.paisId" @change="onPaisChange" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm">
                <option :value="0" disabled>Seleccione un país</option>
                <option v-for="p in paises" :key="p.id" :value="p.id">{{ p.nombre }}</option>
            </select>
        </div>
        <div>
            <label class="block text-sm font-medium text-gray-700">Provincia</label>
            <select v-model="form.provinciaId" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm">
                <option :value="0" disabled>Seleccione una provincia</option>
                <option v-for="p in provincias" :key="p.id" :value="p.id">{{ p.nombre }}</option>
            </select>
        </div>
        <div>
            <label class="block text-sm font-medium text-gray-700">Nombre</label>
            <input v-model="form.nombre" type="text" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" />
        </div>
        <div>
            <label class="block text-sm font-medium text-gray-700">Código Postal</label>
            <input v-model="form.codPostal" type="text" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" />
        </div>
        <div class="flex justify-end gap-2">
            <button type="button" @click="$emit('cancel')" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50">Cancelar</button>
            <button type="submit" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700">Guardar</button>
        </div>
    </form>
  </div>
</template>
