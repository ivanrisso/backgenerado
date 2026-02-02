<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useTiposImpuesto } from '@modules/Maestros/composables/useTiposImpuesto';
import TipoImpuestoForm from './TipoImpuestoForm.vue';
import TipoImpuestoCondicionesTab from './TipoImpuestoCondicionesTab.vue';
import PageHeader from '@shared/ui/PageHeader.vue';
import DataTable from '@shared/ui/DataTable.vue';
import type { TipoImpuesto } from '@domain/entities/TipoImpuesto';
import { TipoUsoImpuestoEnum } from '@domain/enums/TipoUsoImpuestoEnum';

const { tiposImpuesto, loading, error, loadTiposImpuesto, createTipoImpuesto, updateTipoImpuesto, deleteTipoImpuesto } = useTiposImpuesto();

const showForm = ref(false);
const isDeleteMode = ref(false);
const editingEntity = ref<TipoImpuesto | null>(null);
const activeTab = ref<'generales' | 'condiciones'>('generales');

// Filter state
const usageFilter = ref<string>('all');
const searchQuery = ref<string>('');

onMounted(() => {
    loadTiposImpuesto();
});

const filteredTipos = computed(() => {
    return tiposImpuesto.value.filter(t => {
        const matchesUsage = usageFilter.value === 'all' || t.tipo_uso === usageFilter.value;
        const matchesSearch = !searchQuery.value || 
            t.nombre.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
            t.etiqueta_factura?.toLowerCase().includes(searchQuery.value.toLowerCase());
        return matchesUsage && matchesSearch;
    });
});

const handleNew = () => {
    editingEntity.value = null;
    isDeleteMode.value = false;
    error.value = null;
    showForm.value = true;
    activeTab.value = 'generales';
};

const handleEdit = (entity: TipoImpuesto) => {
    editingEntity.value = entity;
    isDeleteMode.value = false;
    error.value = null;
    showForm.value = true;
    activeTab.value = 'generales';
};

// Triggered from Table Delete Icon
const handlePreDelete = (entity: TipoImpuesto) => {
    editingEntity.value = entity;
    isDeleteMode.value = true;
    error.value = null; // Reset errors
    showForm.value = true;
};

// Confirmation Action from Form
const handleConfirmDelete = async (id: number) => {
    try {
        await deleteTipoImpuesto(id);
        showForm.value = false;
        error.value = null; // Clear error on success
    } catch (e) {
        // Error is set in 'error' ref by composable and passed to form via prop
    }
};

const handleCancel = () => {
    showForm.value = false;
    error.value = null; // Clear error on cancel
    isDeleteMode.value = false;
    activeTab.value = 'generales';
};

const handleSubmit = async (entity: TipoImpuesto) => {
    try {
        if (entity.id === 0) {
           await createTipoImpuesto(entity);
        } else {
           await updateTipoImpuesto(entity);
        }
        showForm.value = false;
        error.value = null; // Clear error on success
    } catch (e) {
        // Error handled in composable
    }
};
</script>

<template>
  <div class="space-y-6">
    <PageHeader title="Impuestos" subtitle="Configuración fiscal alineada con Odoo.">
      <template #actions>
        <button class="btn btn-primary shadow-blue-100" @click="handleNew">
          <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" /></svg>
          Nuevo Impuesto
        </button>
      </template>
    </PageHeader>

    <div v-if="showForm" class="space-y-4">
      <!-- Tabs Selector -->
      <div v-if="editingEntity?.id && !isDeleteMode" class="border-b border-gray-200">
        <nav class="-mb-px flex space-x-8" aria-label="Tabs">
          <button 
            class="whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-colors" :class="[
              activeTab === 'generales' 
                ? 'border-blue-500 text-blue-600' 
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            ]"
            @click="activeTab = 'generales'"
          >
            Definición del Impuesto
          </button>
          <button 
            class="whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-colors" :class="[
              activeTab === 'condiciones' 
                ? 'border-blue-500 text-blue-600' 
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            ]"
            @click="activeTab = 'condiciones'"
          >
            Condiciones Asociadas
          </button>
        </nav>
      </div>

      <!-- Generales Tab -->
      <div v-if="activeTab === 'generales'">
        <TipoImpuestoForm 
          :model-value="editingEntity" 
          :is-delete-mode="isDeleteMode"
          :server-error="error"
          @submit="handleSubmit" 
          @delete="handleConfirmDelete"
          @cancel="handleCancel" 
        />
      </div>

      <!-- Condiciones Tab -->
      <div v-if="activeTab === 'condiciones' && editingEntity?.id">
        <TipoImpuestoCondicionesTab 
          :tipo-impuesto-id="editingEntity.id" 
          :fixed-tipo-impuesto-id="editingEntity.id"
        />
        <div class="mt-4 flex justify-end">
          <button class="btn btn-secondary" @click="handleCancel">
            Cerrar y Volver
          </button>
        </div>
      </div>
    </div>

    <div v-if="!showForm" class="space-y-4">
      <!-- Odoo-Style Filter Bar -->
      <div class="flex flex-col md:flex-row gap-4 bg-white p-4 rounded-xl shadow-sm border border-gray-200">
        <div class="flex-1 relative">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
          </div>
          <input
            v-model="searchQuery" type="text" placeholder="Buscar impuesto o etiqueta..." 
            class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-all"
          >
        </div>
        <div class="flex items-center space-x-2">
          <span class="text-sm font-medium text-gray-500">Filtrar por:</span>
          <select v-model="usageFilter" class="rounded-lg border-gray-300 text-sm focus:ring-blue-500 focus:border-blue-500 transition-all">
            <option value="all">
              Venta o Compras
            </option>
            <option :value="TipoUsoImpuestoEnum.VENTAS">
              Solo Ventas
            </option>
            <option :value="TipoUsoImpuestoEnum.COMPRAS">
              Solo Compras
            </option>
            <option :value="TipoUsoImpuestoEnum.RETENCION_PAGO_PROVEEDOR">
              Retenciones
            </option>
          </select>
        </div>
      </div>

      <div v-if="loading" class="flex justify-center p-12">
        <div class="animate-spin h-8 w-8 border-4 border-blue-500 border-t-transparent rounded-full shadow-lg shadow-blue-100" />
      </div>
      <!-- Only show global error if form is closed -->
      <div v-if="error && !showForm" class="p-4 bg-red-50 text-red-700 rounded-xl border border-red-200">
        {{ error }}
      </div>

      <DataTable 
        v-if="!loading && (!error || showForm)"
        :columns="[
          { key: 'nombre', label: 'Nombre del impuesto' },
          { key: 'descripcion', label: 'Descripción' },
          { key: 'tipo_uso', label: 'Tipo de impuesto', class: 'w-40' },
          { key: 'ambito_uso', label: 'Ámbito de impuesto', class: 'w-40' },
          { key: 'etiqueta_factura', label: 'Etiqueta en facturas', class: 'w-40' },
          { key: 'activo', label: 'Activo', class: 'w-24 text-center' },
        ]" 
        :items="filteredTipos" 
        actions
      >
        <template #cell-tipo_uso="{ item }">
          <span
            class="px-2 py-0.5 text-xs font-semibold rounded-full border shadow-sm capitalize" :class="[
              item.tipo_uso === 'ventas' ? 'bg-blue-50 text-blue-700 border-blue-100' : 
              item.tipo_uso === 'compras' ? 'bg-green-50 text-green-700 border-green-100' : 'bg-gray-50 text-gray-700 border-gray-100'
            ]"
          >
            {{ item.tipo_uso }}
          </span>
        </template>
        <template #cell-ambito_uso="{ item }">
          <span class="text-xs text-gray-600 capitalize">{{ item.ambito_uso }}</span>
        </template>
        <template #cell-etiqueta_factura="{ item }">
          <span class="text-sm font-medium text-gray-900 italic">{{ item.etiqueta_factura || '-' }}</span>
        </template>
        <template #cell-activo="{ item }">
          <div class="flex justify-center">
            <div class="w-10 h-5 rounded-full relative transition-colors duration-200" :class="[item.activo ? 'bg-green-400' : 'bg-gray-300']">
              <div class="absolute top-1 w-3 h-3 bg-white rounded-full transition-all duration-200" :class="[item.activo ? 'right-1' : 'left-1']" />
            </div>
          </div>
        </template>
            
        <template #actions="{ item }">
          <div class="flex justify-center space-x-1">
            <button class="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors" title="Editar" @click="handleEdit(item)">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
            </button>
            <button class="p-2 text-red-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors" title="Borrar" @click="handlePreDelete(item)">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
            </button>
          </div>
        </template>
      </DataTable>
    </div>
  </div>
</template>
