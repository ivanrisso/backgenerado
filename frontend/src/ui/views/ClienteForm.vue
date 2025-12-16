<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useClientes } from '../composables/useClientes';
import { CUIT } from '@domain/value-objects/CUIT';
import { Email } from '@domain/value-objects/Email';

import { useRoute } from 'vue-router';
import { onMounted, computed } from 'vue';
import { useTipoDocs } from '../composables/useTipoDocs';
import { useIvas } from '../composables/useIvas';

const router = useRouter();
const route = useRoute();
const { createCliente, updateCliente, fetchClienteById, loading, error } = useClientes();
const { tipoDocs, loadTipoDocs } = useTipoDocs();
const { ivas, loadIvas } = useIvas();

const isEditing = computed(() => route.name === 'clientes-edit');
const clienteId = computed(() => Number(route.params.id));


const form = ref({
  nombre: '',
  apellido: '',
  cuit: '',
  email: '',
  razon_social: '',
  tipo_doc_id: 80, // CUIT por defecto
  iva_id: 5 // Consumidor Final default (or 1 depending on logic)
});

// ... inside onMounted
onMounted(async () => {
    await Promise.all([loadTipoDocs(), loadIvas()]);
    
    if (isEditing.value) {
        const cliente = await fetchClienteById(clienteId.value);
        if (cliente) {
            form.value = {
                nombre: cliente.nombre,
                apellido: cliente.apellido,
                cuit: cliente.cuit ? cliente.cuit.value : '',
                email: cliente.email ? cliente.email.getValue() : '',
                razon_social: cliente.razon_social || '',
                tipo_doc_id: cliente.tipo_doc_id,
                iva_id: cliente.iva_id
            };
        }
    } else {
        // Defaults
        const cuitDoc = tipoDocs.value.find(d => d.id === 80);
        if (cuitDoc) form.value.tipo_doc_id = 80;
        
        const consFinal = ivas.value.find(i => i.id === 5); // Consumidor Final
        if (consFinal) form.value.iva_id = 5;
    }
});
</script>

<template>
  <div class="max-w-2xl mx-auto">
    <div class="mb-8">
      <RouterLink to="/clientes" class="text-sm text-gray-500 hover:text-gray-900 mb-2 inline-block">← Volver a lista</RouterLink>
      <h1 class="text-2xl font-bold text-gray-900 tracking-tight">{{ isEditing ? 'Editar Cliente' : 'Nuevo Cliente' }}</h1>
      <p class="text-gray-500">{{ isEditing ? 'Modifica los datos del cliente.' : 'Ingresa los datos del nuevo cliente.' }}</p>
    </div>

    <div v-if="error" class="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
      {{ error }}
    </div>

    <div class="card p-8">
      <form @submit.prevent="submit" class="space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Nombre</label>
            <input v-model="form.nombre" required class="input-field" placeholder="Ej: Juan" />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Apellido</label>
            <input v-model="form.apellido" required class="input-field" placeholder="Ej: Pérez" />
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Razón Social <span class="text-gray-400 font-normal">(Opcional)</span></label>
          <input v-model="form.razon_social" class="input-field" placeholder="Ej: Empresa S.A." />
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
                 <label class="block text-sm font-medium text-gray-700 mb-1">Tipo de Documento</label>
                 <select v-model="form.tipo_doc_id" class="input-field">
                     <option v-for="td in tipoDocs" :key="td.id" :value="td.id">{{ td.nombre }}</option>
                 </select>
            </div>
            <div>
                 <label class="block text-sm font-medium text-gray-700 mb-1">Condición de IVA</label>
                 <select v-model="form.iva_id" class="input-field">
                     <option v-for="i in ivas" :key="i.id" :value="i.id">{{ i.descripcion }}</option>
                 </select>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">CUIT</label>
            <input v-model="form.cuit" required class="input-field" placeholder="20-12345678-9" />
            <p class="mt-1 text-xs text-gray-500">Sin guiones.</p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input v-model="form.email" type="email" class="input-field" placeholder="contacto@cliente.com" />
          </div>
        </div>

        <div class="pt-4 flex items-center justify-end gap-3">
          <RouterLink to="/clientes" class="btn btn-secondary">Cancelar</RouterLink>
          <button type="submit" :disabled="loading" class="btn btn-primary min-w-[120px] flex justify-center">
            <span v-if="loading" class="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></span>
            <span v-else>{{ isEditing ? 'Actualizar Cliente' : 'Guardar Cliente' }}</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
/* Tailwind classes used */
</style>
