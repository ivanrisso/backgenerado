<script setup lang="ts">
import { ref, watch } from 'vue';
import type { PuntoVenta, PuntoVentaCreate } from '../../api/puntoVentaApi';

const props = defineProps<{
    modelValue: PuntoVenta | null;
    isDeleteMode?: boolean;
    serverError?: string | null;
}>();

const emit = defineEmits<{
    (e: 'submit', entity: PuntoVentaCreate): void;
    (e: 'cancel'): void;
}>();

const form = ref({
    numero: 0,
    tipo: 'ELECTRONICA' as 'ELECTRONICA' | 'FISCAL' | 'MANUAL',
    bloqueado: false
});

watch(() => props.modelValue, (newVal) => {
    if (newVal) {
        form.value = {
            numero: newVal.numero,
            tipo: newVal.tipo,
            bloqueado: newVal.bloqueado
        };
    } else {
        form.value = {
            numero: 0,
            tipo: 'ELECTRONICA',
            bloqueado: false
        };
    }
}, { immediate: true });

const handleSubmit = () => {
    emit('submit', { ...form.value });
};
</script>

<template>
  <div class="bg-white rounded-lg shadow-xl transform transition-all sm:max-w-lg sm:w-full">
    <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4 rounded-t-lg">
      <div class="sm:flex sm:items-start">
        <div 
          class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full sm:mx-0 sm:h-10 sm:w-10"
          :class="isDeleteMode ? 'bg-red-100' : 'bg-blue-100'"
        >
          <svg v-if="isDeleteMode" class="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <svg v-else class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
        </div>
        <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
          <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
            {{ isDeleteMode ? 'Eliminar Punto de Venta' : (props.modelValue ? 'Editar Punto de Venta' : 'Nuevo Punto de Venta') }}
          </h3>
          <div class="mt-2 text-sm text-gray-500">
             <p v-if="isDeleteMode">¿Estás seguro de que deseas eliminar este punto de venta? Esta acción no se puede deshacer.</p>
             <p v-else>Configure los detalles del punto de venta para facturación.</p>
          </div>

          <!-- Error Alert -->
          <div v-if="serverError" class="mt-2 p-3 bg-red-50 text-red-700 rounded-md text-sm border border-red-100">
             {{ serverError }}
          </div>
          
          <!-- Form Fields -->
          <div class="mt-4 space-y-4 text-left">
            <fieldset :disabled="isDeleteMode" class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700">Número</label>
                <div class="mt-1">
                  <input v-model.number="form.numero" type="number" required class="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md">
                </div>
                <p class="mt-1 text-xs text-gray-500">Número oficial (AFIP), ej: 1, 2, 5.</p>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700">Tipo</label>
                <div class="mt-1">
                    <select v-model="form.tipo" class="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md">
                        <option value="ELECTRONICA">Electrónica (RECE)</option>
                        <option value="FISCAL">Controlador Fiscal</option>
                        <option value="MANUAL">Manual / Talonario</option>
                    </select>
                </div>
              </div>

              <div class="flex items-start">
                  <div class="flex items-center h-5">
                    <input v-model="form.bloqueado" id="bloqueado" type="checkbox" class="focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300 rounded">
                  </div>
                  <div class="ml-3 text-sm">
                    <label for="bloqueado" class="font-medium text-gray-700">Bloqueado</label>
                    <p class="text-gray-500">Si está marcado, no se podrá utilizar para emitir nuevos comprobantes.</p>
                  </div>
              </div>
            </fieldset>
          </div>
        </div>
      </div>
    </div>
    <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse rounded-b-lg">
      <button 
        type="button" 
        class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 text-base font-medium text-white sm:ml-3 sm:w-auto sm:text-sm"
        :class="isDeleteMode ? 'bg-red-600 hover:bg-red-700' : 'bg-blue-600 hover:bg-blue-700'"
        @click="handleSubmit"
      >
        {{ isDeleteMode ? 'Eliminar' : 'Guardar' }}
      </button>
      <button 
        type="button" 
        class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
        @click="$emit('cancel')"
      >
        Cancelar
      </button>
    </div>
  </div>
</template>
