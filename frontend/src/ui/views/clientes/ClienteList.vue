<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Clientes</h1>
        <p class="text-gray-600">Gestión de clientes y sus datos relacionados.</p>
      </div>
      <button v-if="!showForm" @click="handleNew" class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 flex items-center gap-2">
        <span class="text-xl font-light">+</span> Nuevo Cliente
      </button>
    </div>

    <!-- Form Area -->
    <div v-if="showForm" class="bg-white rounded-lg shadow-xl overflow-hidden mb-6 border border-gray-200">
        <div class="p-6 border-b border-gray-200 flex justify-between items-center bg-gray-50">
            <h3 class="text-lg font-medium text-gray-900">{{ editingEntity ? 'Editar' : 'Nuevo' }} Cliente</h3>
            <button @click="showForm = false" class="text-gray-400 hover:text-gray-500">
                <span class="sr-only">Cerrar</span>
                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>
        </div>
        <div class="p-6">
           <ClienteForm :modelValue="(editingEntity as any)" @submit="handleSubmit" @cancel="showForm = false" />
        </div>
    </div>

    <div v-if="isLoading" class="text-blue-500 py-4">Cargando clientes...</div>
    <div v-if="error" class="text-red-500 py-4">{{ error }}</div>

    <!-- List Area -->
    <div v-if="!isLoading && !error" class="bg-white shadow overflow-hidden sm:rounded-md border border-gray-200">
      <ul class="divide-y divide-gray-200">
        <li v-for="item in clientes" :key="item.id" class="px-6 py-4 flex items-center justify-between hover:bg-gray-50 transition-colors">
          <div class="flex flex-col gap-1">
             <div class="flex items-center gap-2">
                 <span class="text-sm font-bold text-gray-900">{{ item.razon_social || `${item.nombre} ${item.apellido}` }}</span>
                 <span class="text-xs text-gray-500" v-if="item.cuit">CUIT: {{ (item.cuit as any).value || item.cuit }}</span>
             </div>
             <div class="text-xs text-gray-500 flex gap-4">
                 <span v-if="item.email">✉️ {{ (item.email as any).value || (item.email as any).getValue?.() || item.email }}</span>
             </div>
          </div>
          <div class="flex space-x-3">
             <button @click="handleEdit(item)" class="text-indigo-600 hover:text-indigo-900 text-sm font-medium">Editar</button>
             <button @click="handleDelete(item)" class="text-red-600 hover:text-red-900 text-sm font-medium">Borrar</button>
          </div>
        </li>
        <li v-if="clientes.length === 0" class="px-6 py-8 text-center text-gray-500 italic">
            No hay clientes registrados.
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useClientes } from '../../composables/useClientes';
import ClienteForm from './ClienteForm.vue';
import type { Cliente } from '../../../domain/entities/Cliente';

const { clientes, isLoading, error, loadClientes, saveCliente, deleteCliente } = useClientes();

const showForm = ref(false);
const editingEntity = ref<Cliente | null>(null);

onMounted(async () => {
    await loadClientes();
});

const handleNew = () => {
    editingEntity.value = null;
    showForm.value = true;
};

const handleEdit = (entity: Cliente) => {
    editingEntity.value = entity;
    showForm.value = true;
};

const handleDelete = async (item: Cliente) => {
    if(confirm(`¿Está seguro de eliminar al cliente ${item.nombre}?`)) {
        await deleteCliente(item.id);
    }
};

const handleSubmit = async (entity: Cliente) => {
    try {
        await saveCliente(entity);
        showForm.value = false;
        await loadClientes();
    } catch (e: any) {
        alert(e.message || 'Error guardando cliente');
    }
};
</script>
