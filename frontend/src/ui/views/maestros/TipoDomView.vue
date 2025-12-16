<script setup lang="ts">
import { ref } from 'vue';
import { useTiposContacto } from '../../composables/useTiposContacto';
import TipoDomForm from './TipoDomForm.vue';
import type { TipoDom } from '../../../domain/entities/TipoDom';

const { tiposDom, loading, error, createTipoDom, updateTipoDom, deleteTipoDom } = useTiposContacto();

const showForm = ref(false);
const editingEntity = ref<TipoDom | null>(null);

const handleNew = () => {
    editingEntity.value = null;
    showForm.value = true;
};

const handleEdit = (entity: TipoDom) => {
    editingEntity.value = entity;
    showForm.value = true;
};

const handleDelete = async (id: number) => {
    if(confirm('¿Está seguro de eliminar este registro?')) {
        await deleteTipoDom(id);
    }
};

const handleSubmit = async (entity: TipoDom) => {
    try {
        if (entity.id === 0) {
           await createTipoDom(entity);
        } else {
           await updateTipoDom(entity);
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
        <h1 class="text-2xl font-bold text-gray-900">Tipos de Domicilio</h1>
        <p class="text-gray-600">Catálogo de tipos de domicilio.</p>
      </div>
      <button @click="handleNew" class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
        + Nuevo
      </button>
    </div>

    <!-- Form Area -->
    <div v-if="showForm">
        <TipoDomForm :modelValue="editingEntity" @submit="handleSubmit" @cancel="showForm = false" />
    </div>

    <div v-if="loading" class="text-blue-500">Cargando...</div>
    <div v-if="error" class="text-red-500">{{ error }}</div>

    <div v-if="!loading && !error" class="bg-white shadow overflow-hidden sm:rounded-md">
      <ul class="divide-y divide-gray-200">
        <li v-for="item in tiposDom" :key="item.id" class="px-6 py-4 flex items-center justify-between hover:bg-gray-50">
          <span class="text-sm font-medium text-gray-900">{{ item.nombre }}</span>
          <div class="flex space-x-2">
             <button @click="handleEdit(item)" class="text-indigo-600 hover:text-indigo-900 text-sm font-medium">Editar</button>
             <button @click="handleDelete(item.id)" class="text-red-600 hover:text-red-900 text-sm font-medium">Borrar</button>
          </div>
        </li>
        <li v-if="tiposDom.length === 0" class="px-6 py-4 text-gray-500 italic">No hay registros</li>
      </ul>
    </div>
  </div>
</template>
