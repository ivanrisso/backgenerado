<script setup lang="ts">
import { ref } from 'vue';
import { useTiposDoc } from '../../composables/useTiposDoc';
import TipoDocForm from './TipoDocForm.vue';
import type { TipoDoc } from '../../../domain/entities/TipoDoc';

// We need to pass edit/delete handlers to the list, but extracting the list component might be tricky if it doesn't support events.
// Let's just inline the list here or modify the existing component. Ideally, modify the existing component to emit events.

const { tiposDoc, loading, error, createTipoDoc, updateTipoDoc, deleteTipoDoc } = useTiposDoc();

const showForm = ref(false);
const editingEntity = ref<TipoDoc | null>(null);

const handleNew = () => {
    editingEntity.value = null;
    showForm.value = true;
};

const handleEdit = (entity: TipoDoc) => {
    editingEntity.value = entity;
    showForm.value = true;
};

const handleDelete = async (id: number) => {
    if(confirm('¿Está seguro de eliminar este registro?')) {
        await deleteTipoDoc(id);
    }
};

const handleSubmit = async (entity: TipoDoc) => {
    try {
        if (entity.id === 0) {
           await createTipoDoc(entity);
        } else {
           await updateTipoDoc(entity);
        }
        showForm.value = false;
    } catch (e) {
        // Error handled in composable
    }
};

const handleCancel = () => {
    showForm.value = false;
};
</script>

<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Tipos de Documento</h1>
        <p class="text-gray-600">Catálogo maestro de documentos de identidad.</p>
      </div>
      <button @click="handleNew" class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
        + Nuevo
      </button>
    </div>

    <!-- Form Area -->
    <div v-if="showForm">
        <TipoDocForm :modelValue="(editingEntity as any)" @submit="handleSubmit" @cancel="handleCancel" />
    </div>

    <div v-if="loading" class="text-blue-500">Cargando...</div>
    <div v-if="error" class="text-red-500">{{ error }}</div>

    <!-- Custom List with Actions -->
    <div v-if="!loading && !error" class="bg-white shadow overflow-hidden sm:rounded-md">
      <ul class="divide-y divide-gray-200">
        <li v-for="td in tiposDoc" :key="td.id" class="px-6 py-4 flex items-center justify-between hover:bg-gray-50">
          <div>
            <span class="font-medium text-gray-900">{{ td.nombre }}</span>
            <span v-if="td.codigoArca.value" class="ml-2 px-2 py-0.5 text-xs bg-blue-100 text-blue-800 rounded-full">Arca: {{ td.codigoArca.value }}</span>
             <span :class="td.habilitado ? 'text-green-600' : 'text-gray-400'" class="ml-2 text-xs">
                {{ td.habilitado ? 'Habilitado' : 'Deshabilitado' }}
            </span>
          </div>
          <div class="flex space-x-2">
             <button @click="handleEdit(td as any)" class="text-indigo-600 hover:text-indigo-900 text-sm font-medium">Editar</button>
             <button @click="handleDelete(td.id)" class="text-red-600 hover:text-red-900 text-sm font-medium">Borrar</button>
          </div>
        </li>
        <li v-if="tiposDoc.length === 0" class="px-6 py-4 text-gray-500 italic">No hay registros</li>
      </ul>
    </div>
  </div>
</template>
