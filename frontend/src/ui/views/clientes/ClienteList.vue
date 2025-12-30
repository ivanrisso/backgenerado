<template>
  <div class="space-y-6">
    <!-- Header -->
    <PageHeader title="Clientes" subtitle="Gestión de clientes y sus datos relacionados.">
        <template #actions>
            <button v-if="!showForm" @click="handleNew" class="btn btn-primary flex items-center gap-2">
                <span class="text-xl leading-none font-light">+</span> Nuevo Cliente
            </button>
        </template>
    </PageHeader>

    <!-- Form Area -->
    <div v-if="showForm" class="mb-8">
        <div v-if="isRestoringState && !editingEntity" class="p-10 flex flex-col justify-center items-center card">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mb-2"></div>
            <span class="text-gray-500 text-sm">Restaurando sesión...</span>
        </div>
        <div v-else>
            <ClienteForm 
                :modelValue="(editingEntity as any)" 
                :isDeleteMode="isDeleteMode"
                :serverError="serverError"
                @submit="handleSubmit" 
                @delete="handleConfirmDelete"
                @cancel="handleCancel" 
            />
        </div>
    </div>

    <!-- List Area -->
    <div v-if="!showForm">
        <div v-if="isLoading" class="p-12 text-center text-blue-500">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-2"></div>
            Cargando clientes...
        </div>
        <div v-else-if="error" class="p-6 bg-red-50 text-red-600 rounded-lg border border-red-100">
            {{ error }}
        </div>

        <DataTable 
            v-else
            :columns="columns" 
            :items="clientes" 
            actions
        >
            <template #cell-id="{ item }">
                <span class="font-mono text-xs text-gray-500">#{{ item.id }}</span>
            </template>
            <template #cell-nombre="{ item }">
                 <span class="font-medium text-gray-900">{{ item.razon_social || `${item.nombre} ${item.apellido}` }}</span>
            </template>
            <template #cell-cuit="{ item }">
                 <span class="text-gray-500">{{ (item.cuit as any).value || item.cuit || '-' }}</span>
            </template>
            <template #cell-email="{ item }">
                 <span class="text-gray-500">{{ (item.email as any).value || (item.email as any).getValue?.() || item.email || '-' }}</span>
            </template>
            
            <template #actions="{ item }">
                <button @click="handleEdit(item)" class="btn-icon" title="Editar">
                    <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                </button>
                <button @click="handleDelete(item)" class="btn-icon text-red-400 hover:text-red-600 hover:bg-red-50" title="Borrar">
                    <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                </button>
            </template>
        </DataTable>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useClientes } from '../../composables/useClientes';
import ClienteForm from './ClienteForm.vue';
import PageHeader from '../../components/common/PageHeader.vue';
import DataTable from '../../components/common/DataTable.vue';
import type { Cliente } from '../../../domain/entities/Cliente';

const route = useRoute();
const router = useRouter();
const { clientes, isLoading, error, loadClientes, saveCliente, deleteCliente, loadClienteById, currentCliente } = useClientes();

const showForm = ref(false);
const editingEntity = ref<Cliente | null>(null);
const isRestoringState = ref(false);
const isDeleteMode = ref(false);
const serverError = ref<string | null>(null);

const columns = [
    { key: 'id', label: 'ID', class: 'w-16' },
    { key: 'nombre', label: 'Nombre / Razón Social' },
    { key: 'cuit', label: 'CUIT' },
    { key: 'email', label: 'Email' }
];

onMounted(async () => {
    // Immediate check to prevent UI flicker
    const editId = Number(route.query.edit);
    if (editId && !isNaN(editId)) {
        showForm.value = true;
        isRestoringState.value = true;
    }

    try {
        // Load clients
        const loadPromise = loadClientes();
        
        // If restoring, try to resolve entity in parallel or after
        if (editId) {
             // We wait for list to verify if it's there
             await loadPromise;
             await checkUrlParams();
        } else {
            await loadPromise;
        }
    } finally {
        isRestoringState.value = false;
    }
});

// Watch for route changes to handle navigation from other tabs/modals back to here
watch(() => route.query, () => {
    checkUrlParams();
}, { deep: true });

const checkUrlParams = async () => {
    const editId = Number(route.query.edit);
    if (editId && !isNaN(editId)) {
        // If we have the client in the list, use it
        const clientFromList = clientes.value.find(c => c.id === editId);
        if (clientFromList) {
            editingEntity.value = clientFromList;
            showForm.value = true;
            isDeleteMode.value = false;
        } else {
             // Fallback: fetch separately if not in list
             await loadClienteById(editId);
             if (currentCliente.value) {
                 editingEntity.value = currentCliente.value;
                 showForm.value = true;
                 isDeleteMode.value = false;
             }
        }
    } else {
        if (showForm.value && route.query.edit === undefined && !isDeleteMode.value) {
             showForm.value = false;
             editingEntity.value = null;
        }
    }
}

const handleNew = () => {
    editingEntity.value = null;
    showForm.value = true;
    router.replace({ query: {} }); 
};

const handleEdit = (entity: Cliente) => {
    editingEntity.value = entity;
    showForm.value = true;
    router.replace({ query: { ...route.query, edit: entity.id } });
};

const handleDelete = (item: Cliente) => {
    editingEntity.value = item;
    isDeleteMode.value = true;
    serverError.value = null;
    showForm.value = true;
    router.replace({ query: { ...route.query, delete: item.id } });
};

const handleConfirmDelete = async (id: number) => {
    try {
        await deleteCliente(id);
        handleCancel();
    } catch (e: any) {
        serverError.value = error.value;
    }
};

const handleSubmit = async (entity: Cliente) => {
    try {
        await saveCliente(entity);
        showForm.value = false;
        router.replace({ query: {} }); 
        await loadClientes();
    } catch (e: any) {
        alert(e.message || 'Error guardando cliente');
    }
};

const handleCancel = () => {
    showForm.value = false;
    isDeleteMode.value = false;
    editingEntity.value = null;
    serverError.value = null;
    router.replace({ query: {} }); 
};
</script>
