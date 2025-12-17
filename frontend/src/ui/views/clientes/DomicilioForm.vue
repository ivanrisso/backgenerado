<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import type { Domicilio } from '../../../domain/entities/Domicilio';
import { useUbicacion } from '../../composables/useUbicacion';
import { useTiposDom } from '../../composables/useTiposDom';

const props = defineProps<{
    modelValue: Omit<Domicilio, 'id'> & { id?: number }; // Partial/New domicilio
}>();

const emit = defineEmits<{
    (e: 'submit', entity: any): void;
    (e: 'cancel'): void;
}>();

const { paises, provincias, localidades, loadPaises, loadProvincias, loadLocalidades } = useUbicacion();
const { tiposDom, loadTiposDom } = useTiposDom();

// Local state for selectors (not part of Domicilio entity usually, but needed for UX)
const selectedPais = ref<number>(0);
const selectedProvincia = ref<number>(0);

const form = ref({
    id: 0,
    calle: '',
    numero: 0,
    piso: '',
    depto: '',
    tipo_dom_id: 0,
    localidad_id: 0,
    cliente_id: 0
});

onMounted(async () => {
    await Promise.all([loadPaises(), loadTiposDom()]);
    initForm();
});

watch(() => props.modelValue, () => {
    initForm();
}, { deep: true });

const initForm = async () => {
    if (props.modelValue) {
        form.value = {
            id: props.modelValue.id || 0,
            calle: props.modelValue.calle || '',
            numero: props.modelValue.numero || 0,
            piso: (props.modelValue as any).piso || '',
            depto: (props.modelValue as any).depto || '',
            tipo_dom_id: props.modelValue.tipo_dom_id || 0,
            localidad_id: props.modelValue.localidad_id || 0,
            cliente_id: props.modelValue.cliente_id || 0
        };
    }
};

watch(selectedPais, async (newVal) => {
    await loadProvincias(newVal);
    selectedProvincia.value = 0;
    if (form.value.localidad_id) form.value.localidad_id = 0;
});

watch(selectedProvincia, async (newVal) => {
    await loadLocalidades(newVal);
    if (form.value.localidad_id && !localidades.value.find(l => l.id === form.value.localidad_id)) {
        form.value.localidad_id = 0;
    }
});

const handleSubmit = () => {
    emit('submit', { ...form.value });
};
</script>

<template>
    <div class="space-y-6">
        <!-- Main Domicilio Form -->
        <form @submit.prevent="handleSubmit" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700">Tipo Domicilio</label>
                    <select v-model="form.tipo_dom_id" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border">
                        <option value="0" disabled>Seleccione...</option>
                        <option v-for="t in tiposDom" :key="t.id" :value="t.id">{{ t.nombre }}</option>
                    </select>
                </div>
                 <!-- Ubicacion Selectors -->
                <div>
                    <label class="block text-sm font-medium text-gray-700">País</label>
                    <select v-model="selectedPais" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border">
                        <option value="0" disabled>Seleccione...</option>
                        <option v-for="p in paises" :key="p.id" :value="p.id">{{ p.nombre }}</option>
                    </select>
                </div>
                 <div>
                    <label class="block text-sm font-medium text-gray-700">Provincia</label>
                    <select v-model="selectedProvincia" :disabled="!selectedPais" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border">
                        <option value="0" disabled>Seleccione...</option>
                        <option v-for="p in provincias" :key="p.id" :value="p.id">{{ p.nombre }}</option>
                    </select>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700">Localidad</label>
                    <select v-model="form.localidad_id" :disabled="!selectedProvincia" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border">
                        <option value="0" disabled>Seleccione...</option>
                        <option v-for="l in localidades" :key="l.id" :value="l.id">{{ l.nombre }}</option>
                    </select>
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700">Calle</label>
                    <input v-model="form.calle" type="text" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border" />
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700">Número</label>
                    <input v-model.number="form.numero" type="number" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border" />
                </div>
                 <div>
                    <label class="block text-sm font-medium text-gray-700">Piso</label>
                    <input v-model="form.piso" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border" />
                </div>
                 <div>
                    <label class="block text-sm font-medium text-gray-700">Depto</label>
                    <input v-model="form.depto" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border" />
                </div>
            </div>

            <div class="flex justify-end gap-3 pt-6 border-t border-gray-200 mt-6">
                <button type="button" @click="$emit('cancel')" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none">
                    Cancelar
                </button>
                <button type="submit" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none">
                    Guardar Domicilio
                </button>
            </div>
        </form>
    </div>
</template>
