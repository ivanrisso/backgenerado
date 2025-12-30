<script setup lang="ts">
import { ref } from 'vue';
import { useTiposContacto } from '../../composables/useTiposContacto';
import TipoDomForm from './TipoDomForm.vue';
import PageHeader from '../../components/common/PageHeader.vue';
import DataTable from '../../components/common/DataTable.vue';
import type { TipoDom } from '../../../domain/entities/TipoDom';

const { tiposDom, loading, error, createTipoDom, updateTipoDom, deleteTipoDom } = useTiposContacto();

// Trigger load on mount since useTiposContacto fetches both on mount but we want to be sure or just reuse it
// The composable has onMounted inside it? Let's check. 
// Yes, line 32: onMounted(() => { fetchData(); });
// So it auto-loads. We might not need to call it again, but if we do, it's fine.
// Wait, if I import it here, it might run onMounted again or share state? 
// Composable creates state inside function scope. So calling useTiposContacto() creates NEW state and runs onMounted.
// This is typical for "per-component" state. So it works.

const showForm = ref(false);
const isDeleteMode = ref(false);
const editingEntity = ref<TipoDom | null>(null);

const handleNew = () => {
    editingEntity.value = null;
    isDeleteMode.value = false;
    error.value = null;
    showForm.value = true;
};

const handleEdit = (entity: TipoDom) => {
    editingEntity.value = entity;
    isDeleteMode.value = false;
    error.value = null;
    showForm.value = true;
};

const handlePreDelete = (entity: TipoDom) => {
    editingEntity.value = entity;
    isDeleteMode.value = true;
    error.value = null;
    showForm.value = true;
};

const handleConfirmDelete = async (id: number) => {
    try {
        await deleteTipoDom(id);
        showForm.value = false;
        error.value = null;
    } catch (e) {
        // Error set in composable
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
        error.value = null;
    } catch (e) {
        // Error handled in composable
    }
};

const handleCancel = () => {
    showForm.value = false;
    error.value = null;
    isDeleteMode.value = false;
};
</script>

<template>
  <div class="space-y-6">
    <PageHeader title="Tipos de Domicilio" subtitle="Catálogo de tipos de domicilio.">
        <template #actions>
            <button @click="handleNew" class="btn btn-primary">
                + Nuevo
            </button>
        </template>
    </PageHeader>

    <div v-if="showForm" class="mb-8">
        <TipoDomForm 
            :modelValue="editingEntity" 
            :isDeleteMode="isDeleteMode"
            :serverError="error"
            @submit="handleSubmit" 
            @delete="handleConfirmDelete"
            @cancel="handleCancel" 
        />
    </div>

    <div v-if="!showForm">
        <div v-if="loading" class="text-blue-500 p-4">Cargando...</div>
        <div v-if="error && !showForm" class="text-red-500 p-4">{{ error }}</div>

        <DataTable 
            v-if="!loading && (!error || showForm)"
            :columns="[
                { key: 'nombre', label: 'Nombre' },
            ]" 
            :items="tiposDom" 
            actions
        >
            <template #actions="{ item }">
                 <button @click="handleEdit(item)" class="btn-icon" title="Editar">
                    <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                </button>
                <button @click="handlePreDelete(item)" class="btn-icon text-red-400 hover:text-red-600 hover:bg-red-50" title="Borrar">
                    <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                </button>
            </template>
        </DataTable>
    </div>
  </div>
</template>
