
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useConceptos } from '../../composables/useConceptos';
import ConceptoForm from './ConceptoForm.vue';
import type { Concepto } from '../../../domain/entities/Concepto';

const { conceptos, loading, error, loadConceptos, createConcepto, updateConcepto, deleteConcepto } = useConceptos();

const showForm = ref(false);
const editingEntity = ref<Concepto | null>(null);

onMounted(() => {
    loadConceptos();
});

const handleNew = () => {
    editingEntity.value = null;
    showForm.value = true;
};

const handleEdit = (entity: Concepto) => {
    editingEntity.value = entity;
    showForm.value = true;
};

const handleDelete = async (id: number) => {
    if(confirm('¿Está seguro de eliminar este registro?')) {
        await deleteConcepto(id);
    }
};

const handleSubmit = async (entity: Concepto) => {
    try {
        if (entity.id === 0) {
           await createConcepto(entity);
        } else {
           await updateConcepto(entity);
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
        <h1 class="text-2xl font-bold text-gray-900">Conceptos</h1>
        <p class="text-gray-600">Catálogo de conceptos de facturación.</p>
      </div>
      <button @click="handleNew" class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
        + Nuevo
      </button>
    </div>

    <div v-if="showForm">
        <ConceptoForm :modelValue="editingEntity" @submit="handleSubmit" @cancel="showForm = false" />
    </div>

    <div v-if="loading" class="text-blue-500">Cargando...</div>
    <div v-if="error" class="text-red-500">{{ error }}</div>

    <div v-if="!loading && !error" class="bg-white shadow overflow-hidden sm:rounded-md">
      <ul class="divide-y divide-gray-200">
        <li v-for="item in conceptos" :key="item.id" class="px-6 py-4 flex items-center justify-between hover:bg-gray-50">
          <div>
            <span class="font-medium text-gray-900">{{ item.descripcion }}</span>
            <span class="ml-2 px-2 py-0.5 text-xs bg-gray-100 text-gray-600 rounded-full select-all">{{ item.codigo }}</span>
          </div>
          <div class="flex space-x-2">
             <button @click="handleEdit(item)" class="text-indigo-600 hover:text-indigo-900 text-sm font-medium">Editar</button>
             <button @click="handleDelete(item.id)" class="text-red-600 hover:text-red-900 text-sm font-medium">Borrar</button>
          </div>
        </li>
        <li v-if="conceptos.length === 0" class="px-6 py-4 text-gray-500 italic">No hay registros</li>
      </ul>
    </div>
  </div>
</template>
