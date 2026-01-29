<script setup lang="ts">
import { ref, watch, onMounted } from 'vue';
import type { CondicionTributaria } from '../../../domain/entities/CondicionTributaria';
import { AmbitoImpuestoEnum } from '../../../domain/enums/AmbitoImpuestoEnum';
import { useTiposImpuesto } from '../../composables/useTiposImpuesto';

const props = defineProps<{
    modelValue: CondicionTributaria | null;
    isDeleteMode?: boolean;
    serverError?: string | null;
    fixedTipoImpuestoId?: number; // Nueva prop para bloquear el impuesto
}>();

const emit = defineEmits<{
    (e: 'submit', entity: CondicionTributaria): void;
    (e: 'delete', id: number): void;
    (e: 'cancel'): void;
}>();

const { tiposImpuesto, loadTiposImpuesto } = useTiposImpuesto();

onMounted(() => {
    loadTiposImpuesto();
});

const form = ref<Partial<CondicionTributaria & { id: number }>>({
    id: 0,
    nombre: '',
    descripcion: '',
    ambito: AmbitoImpuestoEnum.NACIONAL,
    tipo_impuesto_id: 0
});

watch(() => props.modelValue, (newVal) => {
    if (newVal) {
        form.value = {
            id: newVal.id,
            nombre: newVal.nombre,
            descripcion: newVal.descripcion || '',
            ambito: newVal.ambito || AmbitoImpuestoEnum.NACIONAL,
            tipo_impuesto_id: newVal.tipo_impuesto_id || props.fixedTipoImpuestoId || 0
        };
    } else {
        form.value = {
            id: 0,
            nombre: '',
            descripcion: '',
            ambito: AmbitoImpuestoEnum.NACIONAL,
            tipo_impuesto_id: props.fixedTipoImpuestoId || 0
        };
    }
}, { immediate: true });

const handleSubmit = () => {
    if (props.isDeleteMode && form.value.id) {
        emit('delete', form.value.id);
        return;
    }
    emit('submit', form.value as CondicionTributaria);
};
</script>

<template>
  <div class="bg-gray-50 p-4 rounded-lg border border-gray-200 mb-4">
    <h3 class="text-lg font-medium text-gray-900 mb-4">
      {{ isDeleteMode ? 'Eliminar' : (modelValue ? 'Editar' : 'Nueva') }} Condición Tributaria
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
          <label class="block text-sm font-medium text-gray-700">Nombre</label>
          <input v-model="form.nombre" type="text" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm disabled:bg-gray-100" placeholder="Ej: Responsable Inscripto">
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Tipo de Impuesto</label>
            <select v-model="form.tipo_impuesto_id" :disabled="!!fixedTipoImpuestoId" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm disabled:bg-gray-100">
              <option :value="0">
                Ninguno / General
              </option>
              <option v-for="t in tiposImpuesto" :key="t.id" :value="t.id">
                {{ t.nombre }}
              </option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Ámbito</label>
            <select v-model="form.ambito" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm disabled:bg-gray-100">
              <option :value="AmbitoImpuestoEnum.NACIONAL">
                Nacional
              </option>
              <option :value="AmbitoImpuestoEnum.PROVINCIAL">
                Provincial
              </option>
              <option :value="AmbitoImpuestoEnum.MUNICIPAL">
                Municipal
              </option>
            </select>
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">Descripción</label>
          <input v-model="form.descripcion" type="text" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm disabled:bg-gray-100">
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
