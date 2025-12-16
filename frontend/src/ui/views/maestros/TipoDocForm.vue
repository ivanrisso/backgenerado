<script setup lang="ts">
import { ref, watch } from 'vue';
import { TipoDoc } from '../../../domain/entities/TipoDoc';
import { CodigoArca } from '../../../domain/value-objects/CodigoArca';

const props = defineProps<{
    modelValue: TipoDoc | null; // If null, assume creation
}>();

const emit = defineEmits<{
    (e: 'submit', entity: TipoDoc): void;
    (e: 'cancel'): void;
}>();

const form = ref({
    id: 0,
    nombre: '',
    habilitado: true,
    codigoArca: ''
});

// Watch for changes in prop to populate form
watch(() => props.modelValue, (newVal) => {
    if (newVal) {
        form.value = {
            id: newVal.id,
            nombre: newVal.nombre,
            habilitado: newVal.habilitado,
            codigoArca: newVal.codigoArca.value
        };
    } else {
        // Reset for new creation
        form.value = { id: 0, nombre: '', habilitado: true, codigoArca: '' };
    }
}, { immediate: true });

const handleSubmit = () => {
    // Construct domain entity
    // Note: ID 0 for creation, handled by backend usually, but for update we need it.
    // We recreate the entity using the class constructor or factory logic
    // But since the entity has immutable props, we might need a DTO approach or just mock it here.
    // A simpler way for UI is to emit the data and let the Parent/Composable construct the Entity.
    // However, the Use Cases expect an Entity. So we must construct it here.
    
    // Warning: Validation logic inside ValueObjects might throw errors.
    try {
        // We create a "plain" object that mimics the Entity structure or use a factory method if available.
        // Since we don't have a factory, we can instantiate it if we have access to constructor.
        // Or we pass a plain object to a mapper.
        
        // Let's import the Class and instantiate it.
        // We need to import TipoDoc class.
        // We assume ID 0 is for new.
        
        // This requires strict coupling to Domain in UI, which is fine for Forms.
        
        // Create the Value Object instance
        const codigoArcaVo = new CodigoArca(form.value.codigoArca);
        
        // Use the Domain Entity constructor
        const entity = new TipoDoc(
            form.value.id,
            form.value.nombre,
            form.value.habilitado,
            codigoArcaVo
        );

        emit('submit', entity);
    } catch (e: any) {
        alert(e.message);
    }
};
</script>

<template>
  <div class="bg-gray-50 p-4 rounded-lg border border-gray-200 mb-4">
    <h3 class="text-lg font-medium text-gray-900 mb-4">{{ modelValue ? 'Editar' : 'Nuevo' }} Tipo de Documento</h3>
    <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
            <label class="block text-sm font-medium text-gray-700">Nombre</label>
            <input v-model="form.nombre" type="text" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" />
        </div>
        <div>
            <label class="block text-sm font-medium text-gray-700">Código ARCA</label>
            <input v-model="form.codigoArca" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm" />
            <p class="text-xs text-gray-500 mt-1">Opcional. Máx 3 caracteres.</p>
        </div>
        <div class="flex items-center">
            <input v-model="form.habilitado" type="checkbox" class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded" />
            <label class="ml-2 block text-sm text-gray-900">Habilitado</label>
        </div>
        <div class="flex justify-end gap-2">
            <button type="button" @click="$emit('cancel')" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50">Cancelar</button>
            <button type="submit" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700">Guardar</button>
        </div>
    </form>
  </div>
</template>
