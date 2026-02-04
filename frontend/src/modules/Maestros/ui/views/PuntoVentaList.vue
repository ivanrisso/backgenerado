<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { usePuntosVenta } from '../../composables/usePuntosVenta';
import type { PuntoVenta, PuntoVentaCreate, PuntoVentaUpdate } from '../../api/puntoVentaApi';
import PuntoVentaForm from '../components/PuntoVentaForm.vue';
import PageHeader from '@/shared/ui/PageHeader.vue';
import DataTable from '@/shared/ui/DataTable.vue';

const { puntosVenta, isLoading, error, loadPuntosVenta, createPuntoVenta, updatePuntoVenta, deletePuntoVenta } = usePuntosVenta();

const showModal = ref(false);
const editingItem = ref<PuntoVenta | null>(null);
const isDeleteMode = ref(false);
const serverError = ref<string | null>(null);

const columns = [
    { key: 'numero', label: 'Número', class: 'w-24 font-mono font-bold' },
    { key: 'tipo', label: 'Tipo' },
    { key: 'bloqueado', label: 'Estado' }
];

onMounted(async () => {
    await loadPuntosVenta();
});

const handleNew = () => {
    editingItem.value = null;
    isDeleteMode.value = false;
    serverError.value = null;
    showModal.value = true;
};

const handleEdit = (item: PuntoVenta) => {
    editingItem.value = item;
    isDeleteMode.value = false;
    serverError.value = null;
    showModal.value = true;
};

const handleDelete = (item: PuntoVenta) => {
    editingItem.value = item;
    isDeleteMode.value = true;
    serverError.value = null;
    showModal.value = true;
};

const handleModalSubmit = async (data: PuntoVentaCreate) => {
    try {
        if (isDeleteMode.value && editingItem.value) {
            await deletePuntoVenta(editingItem.value.id);
        } else if (editingItem.value) {
            await updatePuntoVenta(editingItem.value.id, data);
        } else {
            await createPuntoVenta(data);
        }
        showModal.value = false;
    } catch (e: any) {
        serverError.value = error.value; // Error from composable is updated
    }
};
</script>

<template>
  <div class="space-y-6">
    <PageHeader title="Puntos de Venta" subtitle="Gestión de puntos de emisión de comprobantes (AFIP).">
        <template #actions>
            <button class="btn btn-primary" @click="handleNew">
                + Nuevo
            </button>
        </template>
    </PageHeader>

    <div v-if="isLoading" class="text-center py-10 text-gray-500">
        Cargando...
    </div>
    
    <div v-else-if="error" class="bg-red-50 p-4 rounded-md text-red-700">
        {{ error }}
    </div>

    <DataTable 
        v-else 
        :columns="columns" 
        :items="puntosVenta"
        actions
    >
        <template #cell-tipo="{ item }">
            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                {{ item.tipo }}
            </span>
        </template>
        
        <template #cell-bloqueado="{ item }">
            <span v-if="item.bloqueado" class="text-red-600 font-medium text-sm flex items-center gap-1">
                <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>
                Bloqueado
            </span>
            <span v-else class="text-green-600 font-medium text-sm flex items-center gap-1">
                <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                Activo
            </span>
        </template>

        <template #actions="{ item }">
             <button class="text-gray-400 hover:text-blue-600 mr-3" title="Editar" @click="handleEdit(item)">
                <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg>
             </button>
             <button class="text-gray-400 hover:text-red-600" title="Eliminar" @click="handleDelete(item)">
                <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
             </button>
        </template>
    </DataTable>

    <!-- Modal Overlay -->
    <div v-if="showModal" class="fixed inset-0 z-10 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="showModal = false"></div>
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        <div class="inline-block align-bottom bg-transparent rounded-lg text-left overflow-hidden transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
            <PuntoVentaForm 
                :model-value="editingItem" 
                :is-delete-mode="isDeleteMode"
                :server-error="serverError"
                @submit="handleModalSubmit"
                @cancel="showModal = false"
            />
        </div>
      </div>
    </div>

  </div>
</template>
