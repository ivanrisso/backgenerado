<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import type { Domicilio } from '../../../domain/entities/Domicilio';
import { useUbicacion } from '../../composables/useUbicacion';
import { useTiposDom } from '../../composables/useTiposDom';

const props = defineProps<{
    modelValue: Omit<Domicilio, 'id'> & { id?: number }; // Partial/New domicilio
    isDeleteMode?: boolean;
    serverError?: string | null;
}>();

const emit = defineEmits<{
    (e: 'submit', entity: any): void;
    (e: 'delete', id: number): void;
    (e: 'cancel'): void;
}>();

const { paises, provincias, localidades, loadPaises, loadProvincias, loadLocalidades, getLocationDetails } = useUbicacion();
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

const isInitializing = ref(false);

const initForm = async () => {
    isInitializing.value = true;
    try {
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

            // If we have a localidad, reverse lookup the hierarchy
            if (form.value.localidad_id) {
                 const details = await getLocationDetails(form.value.localidad_id);
                 if (details) {
                     // Set values without triggering resets via watchers (due to flag)
                     selectedPais.value = details.paisId;
                     await loadProvincias(details.paisId);
                     
                     selectedProvincia.value = details.provinciaId;
                     await loadLocalidades(details.provinciaId);
                     
                     form.value.localidad_id = details.localidadId;
                 }
            }
        }
    } finally {
        // Use setTimeout to ensure watchers have fired and been ignored before disabling flag
        // or just nextTick. Usually synchronous update of refs triggers watchers asynchronously? 
        // Vue watchers `flush: 'pre'` by default. 
        // Setting flag to false immediately might be too soon if watchers run in next tick.
        // But since we await async calls above, we yielded. 
        // The safest approach: check flag inside watchers.
        isInitializing.value = false;
    }
};

watch(selectedPais, async (newVal) => {
    if (isInitializing.value) return; // Skip reset if initializing
    await loadProvincias(newVal);
    selectedProvincia.value = 0;
    if (form.value.localidad_id) form.value.localidad_id = 0;
});

watch(selectedProvincia, async (newVal) => {
    if (isInitializing.value) return; // Skip reset if initializing
    await loadLocalidades(newVal);
    // If the currently selected locality doesn't belong to the new province, reset it
    // But this check relies on 'localidades' being updated.
    // 'loadLocalidades' awaits update.
    if (!isInitializing.value) { // Redundant check but clear intent
        if (form.value.localidad_id && !localidades.value.find(l => l.id === form.value.localidad_id)) {
            form.value.localidad_id = 0;
        }
    }
});

const handleSubmit = () => {
    if (props.isDeleteMode && form.value.id) {
        emit('delete', form.value.id);
        return;
    }
    emit('submit', { ...form.value });
};
</script>

<template>
  <div class="space-y-6">
    <!-- Error Alert -->
    <div v-if="serverError" class="p-4 bg-red-50 border border-red-100 rounded-lg flex items-start gap-3 text-red-700">
      <svg class="w-5 h-5 mt-0.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
      <span class="text-sm font-medium">{{ serverError }}</span>
    </div>

    <!-- Delete Warning -->
    <div v-if="isDeleteMode" class="p-4 bg-amber-50 border border-amber-100 rounded-lg flex items-start gap-3">
      <svg class="w-5 h-5 text-amber-500 mt-0.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
      <div>
        <h3 class="text-sm font-bold text-amber-800">
          ¿Eliminar este domicilio?
        </h3>
        <p class="text-xs text-amber-700 mt-1">
          Se borrarán también los teléfonos asociados.
        </p>
      </div>
    </div>

    <!-- Main Domicilio Form -->
    <form class="space-y-6" @submit.prevent="handleSubmit">
      <fieldset :disabled="isDeleteMode" class="space-y-6">
        <div class="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
          <!-- Tipo Domicilio -->
          <div class="sm:col-span-3">
            <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5">Tipo Domicilio</label>
            <div class="relative">
              <select v-model="form.tipo_dom_id" required class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-[15px] py-2.5 appearance-none transition-shadow">
                <option value="0" disabled>
                  Seleccione...
                </option>
                <option v-for="t in tiposDom" :key="t.id" :value="t.id">
                  {{ t.nombre }}
                </option>
              </select>
              <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-gray-500">
                <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" /></svg>
              </div>
            </div>
          </div>

          <!-- Ubicacion Selectors -->
          <div class="sm:col-span-2">
            <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5">País</label>
            <div class="relative">
              <select v-model="selectedPais" class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-[15px] py-2.5 appearance-none transition-shadow">
                <option value="0" disabled>
                  Seleccione...
                </option>
                <option v-for="p in paises" :key="p.id" :value="p.id">
                  {{ p.nombre }}
                </option>
              </select>
              <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-gray-500">
                <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" /></svg>
              </div>
            </div>
          </div>
          <div class="sm:col-span-2">
            <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5">Provincia</label>
            <div class="relative">
              <select v-model="selectedProvincia" :disabled="!selectedPais" class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-[15px] py-2.5 appearance-none transition-shadow disabled:bg-gray-50">
                <option value="0" disabled>
                  Seleccione...
                </option>
                <option v-for="p in provincias" :key="p.id" :value="p.id">
                  {{ p.nombre }}
                </option>
              </select>
              <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-gray-500">
                <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" /></svg>
              </div>
            </div>
          </div>
          <div class="sm:col-span-2">
            <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5">Localidad</label>
            <div class="relative">
              <select v-model="form.localidad_id" :disabled="!selectedProvincia" required class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-[15px] py-2.5 appearance-none transition-shadow disabled:bg-gray-50">
                <option value="0" disabled>
                  Seleccione...
                </option>
                <option v-for="l in localidades" :key="l.id" :value="l.id">
                  {{ l.nombre }}
                </option>
              </select>
              <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-gray-500">
                <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" /></svg>
              </div>
            </div>
          </div>

          <div class="sm:col-span-4">
            <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5">Calle</label>
            <input v-model="form.calle" type="text" required class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-[15px] py-2.5 transition-shadow">
          </div>
          <div class="sm:col-span-2">
            <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5">Número</label>
            <input v-model.number="form.numero" type="number" required class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-[15px] py-2.5 transition-shadow">
          </div>
          <div class="sm:col-span-3">
            <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5">Piso</label>
            <input v-model="form.piso" type="text" class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-[15px] py-2.5 transition-shadow">
          </div>
          <div class="sm:col-span-3">
            <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5">Depto</label>
            <input v-model="form.depto" type="text" class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-[15px] py-2.5 transition-shadow">
          </div>
        </div>
      </fieldset>

      <div class="flex justify-end gap-3 pt-6 border-t border-gray-100 mt-6">
        <button type="button" class="px-5 py-2.5 text-[15px] font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 shadow-sm transition-all focus:outline-none" @click="$emit('cancel')">
          Cancelar
        </button>
        <button 
          type="submit" 
          class="px-5 py-2.5 text-[15px] font-medium text-white rounded-lg shadow-sm transition-all focus:outline-none"
          :class="isDeleteMode ? 'bg-red-600 hover:bg-red-700' : 'bg-blue-600 hover:bg-blue-700'"
        >
          {{ isDeleteMode ? 'Eliminar Definitivamente' : 'Guardar Domicilio' }}
        </button>
      </div>
    </form>
  </div>
</template>
