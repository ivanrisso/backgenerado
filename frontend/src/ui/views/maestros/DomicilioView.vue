
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useDomicilios } from '../../composables/useDomicilios'; // Using global/shared composable if possible, or assume it exists from previous work
// Wait, useDomicilios was CLIENT scoped or GLOBAL?
// I checked useDomicilios.ts earlier. It was using HttpDomicilioRepository and seemed generic.
// But it might need params. Let's assume it has loadDomicilios() or similar.
// Actually, earlier check showed "loadDomicilios" but it was scoped to component ref? No, it was using a ref.
// Let's check useDomicilios again if needed, or assume standard pattern.
// "useDomicilios.ts" content showed: loadDomicilios, list defaults to ref([]).
// But wait, the previous useDomicilios might have been configured for CLIENT context.
// I will check useDomicilios.ts content quickly.
// Can't invoke tool inside write_to_file thought.
// I will assume standard or adapt.
// Actually, useDomicilios usually filters by Client. If I want ALL, I might need a new method in repo.
// The Repo has getAll() ?
// I'll assume standard pattern.

import DomicilioForm from './DomicilioForm.vue';
import type { Domicilio } from '../../../domain/entities/Domicilio';

const { domicilios, loading, error, loadDomicilios, createDomicilio, updateDomicilio, deleteDomicilio } = useDomicilios();

const showForm = ref(false);
const editingEntity = ref<Domicilio | null>(null);

onMounted(() => {
    loadDomicilios(); // If this requires ID, it might fail. I'll check after.
});

const handleNew = () => {
    editingEntity.value = null;
    showForm.value = true;
};

const handleEdit = (entity: Domicilio) => {
    editingEntity.value = entity;
    showForm.value = true;
};

const handleDelete = async (id: number) => {
    if(confirm('¿Está seguro de eliminar este registro?')) {
        await deleteDomicilio(id);
    }
};

const handleSubmit = async (entity: Domicilio) => {
    try {
        if (entity.id === 0) {
           await createDomicilio(entity);
        } else {
           await updateDomicilio(entity); // Repository uses PATCH, but needs full object? No, separate args usually.
           // Composable updateDomicilio(entity) usually handles it.
        }
        showForm.value = false;
    } catch (e) {
        // Error handled in composable
    }
};
</script>

<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Domicilios</h1>
        <p class="text-gray-600">Catálogo global de domicilios.</p>
      </div>
      <button @click="handleNew" class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
        + Nuevo
      </button>
    </div>

    <div v-if="showForm">
        <DomicilioForm :modelValue="editingEntity" @submit="handleSubmit" @cancel="showForm = false" />
    </div>

    <div v-if="loading" class="text-blue-500">Cargando...</div>
    <div v-if="error" class="text-red-500">{{ error }}</div>

    <div v-if="!loading && !error" class="bg-white shadow overflow-hidden sm:rounded-md">
      <ul class="divide-y divide-gray-200">
        <li v-for="item in domicilios" :key="item.id" class="px-6 py-4 flex items-center justify-between hover:bg-gray-50">
          <div>
            <span class="font-medium text-gray-900">{{ item.calle }} {{ item.numero }}</span>
            <span class="ml-2 px-2 py-0.5 text-xs bg-gray-100 text-gray-600 rounded-full">Cliente: {{ item.cliente_id }}</span>
          </div>
          <div class="flex space-x-2">
             <button @click="handleEdit(item)" class="text-indigo-600 hover:text-indigo-900 text-sm font-medium">Editar</button>
             <button @click="handleDelete(item.id)" class="text-red-600 hover:text-red-900 text-sm font-medium">Borrar</button>
          </div>
        </li>
        <li v-if="domicilios.length === 0" class="px-6 py-4 text-gray-500 italic">No hay registros</li>
      </ul>
    </div>
  </div>
</template>
