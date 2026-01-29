
<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useArticulos } from '../../composables/useArticulos';
import type { Articulo } from '../../../domain/entities/Articulo';
import { TipoArticuloEnum } from '../../../domain/enums/TipoArticuloEnum';
import ArticuloForm from './ArticuloForm.vue';
import DataTable from '../../components/common/DataTable.vue';

const { articulos, loading, loadArticulos, createArticulo, updateArticulo, deleteArticulo } = useArticulos();

const showForm = ref(false);
const selectedArticulo = ref<Articulo | null>(null);
const isDeleteMode = ref(false);
const serverError = ref<string | null>(null);

// Filters
const searchQuery = ref('');
const typeFilter = ref<string>('all');

onMounted(async () => {
    await loadArticulos();
});

const filteredArticulos = computed(() => {
    return articulos.value.filter(item => {
        const matchesSearch = !searchQuery.value || 
            item.nombre.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
            item.codigo.toLowerCase().includes(searchQuery.value.toLowerCase());
        
        const matchesType = typeFilter.value === 'all' || item.tipo === typeFilter.value;
        
        return matchesSearch && matchesType;
    });
});

const handleCreate = () => {
    selectedArticulo.value = null;
    isDeleteMode.value = false;
    showForm.value = true;
    serverError.value = null;
};

const handleEdit = (item: Articulo) => {
    selectedArticulo.value = { ...item };
    isDeleteMode.value = false;
    showForm.value = true;
    serverError.value = null;
};

const handleDelete = (item: Articulo) => {
    selectedArticulo.value = { ...item };
    isDeleteMode.value = true;
    showForm.value = true;
    serverError.value = null;
};

const handleSubmit = async (entity: Articulo) => {
    try {
        serverError.value = null;
        if (entity.id) {
            await updateArticulo(entity);
        } else {
            await createArticulo(entity);
        }
        showForm.value = false;
    } catch (e: any) {
        serverError.value = e.response?.data?.detail || e.message || "Error al guardar el artículo";
    }
};

const confirmDelete = async (id: number) => {
    try {
        serverError.value = null;
        await deleteArticulo(id);
        showForm.value = false;
    } catch (e: any) {
        serverError.value = e.response?.data?.detail || e.message || "Error al eliminar el artículo";
    }
};

const columns = [
    { key: 'codigo', label: 'CÓDIGO', sortable: true },
    { key: 'nombre', label: 'NOMBRE', sortable: true },
    { key: 'tipo', label: 'TIPO', sortable: true },
    { key: 'precio_venta', label: 'P. VENTA', sortable: true },
    { key: 'impuesto_venta.nombre', label: 'IVA VTA', sortable: false },
    { key: 'activo', label: 'ESTADO', sortable: true },
    { key: 'actions', label: 'ACCIONES', sortable: false }
];

const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('es-AR', { style: 'currency', currency: 'ARS' }).format(value);
};

const getTipoLabel = (tipo: string) => {
    switch (tipo) {
        case TipoArticuloEnum.SERVICIO: return 'Servicio';
        case TipoArticuloEnum.PRODUCTO: return 'Producto';
        case TipoArticuloEnum.CONSUMIBLE: return 'Consumible';
        default: return tipo;
    }
};

const getTipoClass = (tipo: string) => {
    switch (tipo) {
        case TipoArticuloEnum.SERVICIO: return 'bg-indigo-50 text-indigo-700 border-indigo-100';
        case TipoArticuloEnum.PRODUCTO: return 'bg-sky-50 text-sky-700 border-sky-100';
        default: return 'bg-gray-50 text-gray-700 border-gray-100';
    }
};
</script>

<template>
  <div class="p-8 space-y-8 bg-gray-50/50 min-h-screen">
    <!-- Header Section -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
      <div>
        <h1 class="text-3xl font-black text-gray-900 tracking-tight">
          Artículos y Servicios
        </h1>
        <div class="flex items-center mt-2 text-sm text-gray-500 font-medium">
          <span class="flex h-2 w-2 rounded-full bg-blue-500 mr-2" />
          Gestión del catálogo maestro para facturación automática
        </div>
      </div>
            
      <button
        class="group relative inline-flex items-center px-8 py-3 bg-blue-600 text-white text-sm font-black rounded-xl hover:bg-blue-700 transition-all duration-300 shadow-lg shadow-blue-200 uppercase tracking-widest overflow-hidden" 
        @click="handleCreate"
      >
        <span class="relative z-10 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 transform group-hover:rotate-90 transition-transform duration-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M12 4v16m8-8H4" />
          </svg>
          Nuevo Artículo
        </span>
        <div class="absolute inset-0 bg-white opacity-0 group-hover:opacity-10 transition-opacity duration-300" />
      </button>
    </div>

    <!-- Filter & Search Bar (Odoo Style) -->
    <div class="bg-white p-4 rounded-2xl shadow-sm border border-gray-200 flex flex-wrap items-center justify-between gap-4">
      <div class="flex items-center space-x-2">
        <button
          v-for="filter in [{id:'all', label:'Todos'}, {id:TipoArticuloEnum.SERVICIO, label:'Servicios'}, {id:TipoArticuloEnum.PRODUCTO, label:'Productos'}]"
          :key="filter.id"
          class="px-4 py-2 rounded-xl text-xs font-black uppercase tracking-widest border transition-all duration-300" :class="[typeFilter === filter.id ? 'bg-blue-50 text-blue-700 border-blue-200' : 'bg-transparent text-gray-500 border-transparent hover:bg-gray-50']"
          @click="typeFilter = filter.id"
        >
          {{ filter.label }}
        </button>
      </div>

      <div class="relative flex-grow max-w-md">
        <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
          <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
          </svg>
        </div>
        <input
          v-model="searchQuery" type="text" placeholder="Buscar por código o nombre..."
          class="block w-full pl-11 pr-4 py-2.5 bg-gray-50 border-gray-100 rounded-xl text-sm focus:ring-blue-500 focus:border-blue-500 focus:bg-white transition-all shadow-inner"
        >
      </div>
    </div>

    <!-- Form Modal-like Overlay -->
    <div v-if="showForm" class="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 lg:p-10 pointer-events-none">
      <div class="absolute inset-0 bg-gray-900/60 backdrop-blur-sm pointer-events-auto" @click="showForm = false" />
      <div class="relative w-full max-w-5xl max-h-full overflow-y-auto pointer-events-auto shadow-2xl animate-modalUp">
        <ArticuloForm
          :model-value="selectedArticulo" 
          :is-delete-mode="isDeleteMode" 
          :server-error="serverError"
          @submit="handleSubmit"
          @delete="confirmDelete"
          @cancel="showForm = false"
        />
      </div>
    </div>

    <!-- Main List -->
    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
      <DataTable :items="filteredArticulos" :columns="columns" :loading="loading" :actions="true">
        <template #cell-codigo="{ item }">
          <span class="font-mono text-xs font-bold text-gray-400 bg-gray-50 px-2 py-1 rounded border border-gray-100">{{ item.codigo }}</span>
        </template>
                
        <template #cell-nombre="{ item }">
          <div class="flex flex-col">
            <span class="text-sm font-bold text-gray-800">{{ item.nombre }}</span>
            <span class="text-xs text-gray-400 truncate max-w-[300px]">{{ item.descripcion || 'Sin descripción' }}</span>
          </div>
        </template>

        <template #cell-tipo="{ item }">
          <span class="px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest border" :class="[getTipoClass(item.tipo)]">
            {{ getTipoLabel(item.tipo) }}
          </span>
        </template>

        <template #cell-precio_venta="{ item }">
          <span class="font-bold text-gray-900">{{ formatCurrency(item.precio_venta) }}</span>
        </template>

        <template #cell-impuesto_venta.nombre="{ item }">
          <span v-if="item.impuesto_venta" class="inline-flex items-center text-xs font-bold text-blue-600 bg-blue-50 px-2 py-1 rounded border border-blue-100">
            {{ item.impuesto_venta.nombre }}
          </span>
          <span v-else class="text-xs text-gray-300 italic">No asignado</span>
        </template>

        <template #cell-activo="{ item }">
          <div class="flex items-center">
            <div class="h-2.5 w-2.5 rounded-full mr-2" :class="[item.activo ? 'bg-green-500' : 'bg-gray-300']" />
            <span class="text-xs font-medium uppercase tracking-tighter" :class="item.activo ? 'text-green-700' : 'text-gray-400'">
              {{ item.activo ? 'Activo' : 'Inactivo' }}
            </span>
          </div>
        </template>

        <template #actions="{ item }">
          <div class="flex space-x-2">
            <button
              class="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors group" 
              title="Editar" @click="handleEdit(item)"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
              </svg>
            </button>
            <button
              class="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors group" 
              title="Eliminar" @click="handleDelete(item)"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </template>
      </DataTable>
    </div>
  </div>
</template>

<style scoped>
@keyframes modalUp {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.animate-modalUp {
  animation: modalUp 0.3s ease-out forwards;
}
</style>
