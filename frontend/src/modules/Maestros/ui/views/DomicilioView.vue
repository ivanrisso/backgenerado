
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useDomicilios } from '../../composables/useDomicilios';
import DomicilioForm from './DomicilioForm.vue';
import PageHeader from '../../components/common/PageHeader.vue';
import DataTable from '../../components/common/DataTable.vue';
import type { Domicilio } from '../../../domain/entities/Domicilio';

const { domicilios, loading, error, loadDomicilios, createDomicilio, updateDomicilio, deleteDomicilio } = useDomicilios();

const showForm = ref(false);
const editingEntity = ref<Domicilio | null>(null);

onMounted(() => {
    loadDomicilios();
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
           await updateDomicilio(entity);
        }
        showForm.value = false;
    } catch (e) {
        // Error handled in composable
    }
};
</script>

<template>
  <div class="space-y-6">
    <PageHeader title="Domicilios" subtitle="Catálogo global de domicilios.">
      <template #actions>
        <button class="btn btn-primary" @click="handleNew">
          + Nuevo
        </button>
      </template>
    </PageHeader>

    <div v-if="showForm" class="mb-8">
      <DomicilioForm :model-value="editingEntity" @submit="handleSubmit" @cancel="showForm = false" />
    </div>

    <div v-if="!showForm">
      <div v-if="loading" class="text-blue-500 p-4">
        Cargando...
      </div>
      <div v-if="error" class="text-red-500 p-4">
        {{ error }}
      </div>

      <DataTable 
        v-if="!loading && !error"
        :columns="[
          { key: 'descripcion', label: 'Domicilio' },
          { key: 'cliente_id', label: 'Cliente', class: 'w-32' },
        ]" 
        :items="domicilios" 
        actions
      >
        <template #cell-descripcion="{ item }">
          <span class="font-medium text-gray-900">{{ item.calle }} {{ item.numero }}</span>
          <span v-if="item.piso" class="text-gray-500 ml-1">Piso {{ item.piso }}</span>
          <span v-if="item.depto" class="text-gray-500 ml-1">Dpto {{ item.depto }}</span>
        </template>
        <template #cell-cliente_id="{ item }">
          <span class="px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded-full">ID: {{ item.cliente_id }}</span>
        </template>
            
        <template #actions="{ item }">
          <button class="btn-icon" title="Editar" @click="handleEdit(item)">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
          </button>
          <button class="btn-icon text-red-400 hover:text-red-600 hover:bg-red-50" title="Borrar" @click="handleDelete(item.id)">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
          </button>
        </template>
      </DataTable>
    </div>
  </div>
</template>
