<script setup lang="ts">
import { ref, watch } from 'vue';
import type { TipoImpuesto } from '../../../domain/entities/TipoImpuesto';
import { TipoAplicacionEnum } from '../../../domain/enums/TipoAplicacionEnum';
import { BaseTributarioEnum } from '../../../domain/enums/BaseTributarioEnum';
import { AmbitoImpuestoEnum } from '../../../domain/enums/AmbitoImpuestoEnum';
import { CategoriaImpuestoEnum } from '../../../domain/enums/CategoriaImpuestoEnum';
import { TipoUsoImpuestoEnum } from '../../../domain/enums/TipoUsoImpuestoEnum';
import { MetodoCalculoImpuestoEnum } from '../../../domain/enums/MetodoCalculoImpuestoEnum';
import { AmbitoUsoImpuestoEnum } from '../../../domain/enums/AmbitoUsoImpuestoEnum';
import { CategoriaFiscalImpuestoEnum } from '../../../domain/enums/CategoriaFiscalImpuestoEnum';
import { TipoDistribucionImpuestoEnum, TipoReparticionBaseImpuestoEnum } from '../../../domain/entities/TipoImpuestoDistribucion';
import TaxDistributionTable from '../../components/maestros/TaxDistributionTable.vue';

const props = defineProps<{
    modelValue: TipoImpuesto | null;
    isDeleteMode?: boolean;
    serverError?: string | null;
}>();

const emit = defineEmits<{
    (e: 'submit', entity: TipoImpuesto): void;
    (e: 'delete', id: number): void;
    (e: 'cancel'): void;
}>();

const activeTab = ref('definicion');

const form = ref<any>({
    id: 0,
    codigo_afip: '',
    nombre: '',
    descripcion: '',
    tipo_aplicacion: TipoAplicacionEnum.SUMA,
    base_calculo: BaseTributarioEnum.NETO_GRAVADO,
    ambito: AmbitoImpuestoEnum.NACIONAL,
    categoria: CategoriaImpuestoEnum.IMPUESTO,
    porcentaje: 0,
    editable: true,
    obligatorio: false,
    activo: true,
    
    // Odoo fields
    tipo_uso: TipoUsoImpuestoEnum.VENTAS,
    metodo_calculo: MetodoCalculoImpuestoEnum.PORCENTAJE,
    ambito_uso: AmbitoUsoImpuestoEnum.AMBOS,
    importe: 0,
    etiqueta_factura: '',
    incluido_precio: false,
    afecta_base_subsecuente: false,
    categoria_fiscal: undefined,
    notas_legales: '',
    cuenta_impuesto_vta: '',
    cuenta_impuesto_com: '',
    
    // Repartition lines
    reparticion_facturas: [] as any[],
    reparticion_reembolsos: [] as any[]
});

watch(() => props.modelValue, (newVal) => {
     if (newVal) {
        form.value = { 
            ...newVal, 
            porcentaje: newVal.porcentaje || 0,
            importe: newVal.importe || 0,
            ambito: newVal.ambito || AmbitoImpuestoEnum.NACIONAL,
            categoria: newVal.categoria || CategoriaImpuestoEnum.IMPUESTO,
            tipo_uso: newVal.tipo_uso || TipoUsoImpuestoEnum.VENTAS,
            metodo_calculo: newVal.metodo_calculo || MetodoCalculoImpuestoEnum.PORCENTAJE,
            ambito_uso: newVal.ambito_uso || AmbitoUsoImpuestoEnum.AMBOS,
            etiqueta_factura: newVal.etiqueta_factura || newVal.nombre || '',
            incluido_precio: !!newVal.incluido_precio,
            afecta_base_subsecuente: !!newVal.afecta_base_subsecuente,
            reparticion_facturas: (newVal.reparticiones || []).filter((r: any) => r.tipo_reparticion === TipoDistribucionImpuestoEnum.FACTURA),
            reparticion_reembolsos: (newVal.reparticiones || []).filter((r: any) => r.tipo_reparticion === TipoDistribucionImpuestoEnum.REEMBOLSO)
        };
    } else {
        form.value = {
            id: 0, codigo_afip: '', nombre: '', descripcion: '',
            tipo_aplicacion: TipoAplicacionEnum.SUMA,
            base_calculo: BaseTributarioEnum.NETO_GRAVADO,
            ambito: AmbitoImpuestoEnum.NACIONAL,
            categoria: CategoriaImpuestoEnum.IMPUESTO,
            porcentaje: 0, editable: true, obligatorio: false, activo: true,
            tipo_uso: TipoUsoImpuestoEnum.VENTAS,
            metodo_calculo: MetodoCalculoImpuestoEnum.PORCENTAJE,
            ambito_uso: AmbitoUsoImpuestoEnum.AMBOS,
            importe: 0, etiqueta_factura: '', incluido_precio: false,
            afecta_base_subsecuente: false, categoria_fiscal: undefined,
            notas_legales: '', cuenta_impuesto_vta: '', cuenta_impuesto_com: '',
            reparticion_facturas: [
                { factor_porcentaje: 100, basado_en: TipoReparticionBaseImpuestoEnum.BASE, tipo_reparticion: TipoDistribucionImpuestoEnum.FACTURA },
                { factor_porcentaje: 100, basado_en: TipoReparticionBaseImpuestoEnum.IMPUESTO, tipo_reparticion: TipoDistribucionImpuestoEnum.FACTURA }
            ],
            reparticion_reembolsos: [
                { factor_porcentaje: 100, basado_en: TipoReparticionBaseImpuestoEnum.BASE, tipo_reparticion: TipoDistribucionImpuestoEnum.REEMBOLSO },
                { factor_porcentaje: 100, basado_en: TipoReparticionBaseImpuestoEnum.IMPUESTO, tipo_reparticion: TipoDistribucionImpuestoEnum.REEMBOLSO }
            ]
        };
    }
}, { immediate: true });

const handleSubmit = () => {
    if (props.isDeleteMode) {
        emit('delete', form.value.id);
        return;
    }
    
    // Merge repartition lines
    const reparticiones = [
        ...form.value.reparticion_facturas.map((r: any) => ({ ...r, tipo_reparticion: TipoDistribucionImpuestoEnum.FACTURA, etiqueta: r.etiqueta_nombre ? { nombre: r.etiqueta_nombre } : undefined })),
        ...form.value.reparticion_reembolsos.map((r: any) => ({ ...r, tipo_reparticion: TipoDistribucionImpuestoEnum.REEMBOLSO, etiqueta: r.etiqueta_nombre ? { nombre: r.etiqueta_nombre } : undefined }))
    ];

    // Ensure numeric types
    const entity: TipoImpuesto = {
        ...form.value,
        porcentaje: Number(form.value.porcentaje),
        importe: Number(form.value.importe),
        reparticiones
    };
    emit('submit', entity);
};
</script>

<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden mb-6">
    <div class="px-6 py-4 border-b border-gray-100 bg-gray-50 flex justify-between items-center">
      <h3 class="text-xl font-semibold text-gray-800">
        {{ isDeleteMode ? 'Eliminar' : (modelValue ? 'Editar' : 'Nuevo') }} Impuesto
      </h3>
      <div v-if="form.activo" class="flex items-center space-x-2">
        <span class="text-xs font-medium text-green-600 bg-green-50 px-2 py-1 rounded-full border border-green-100 uppercase tracking-wider">Activo</span>
      </div>
    </div>
    
    <div v-if="serverError" class="m-6 p-4 bg-red-50 text-red-700 border border-red-200 rounded-xl flex items-center space-x-3">
      <span class="font-bold">Error:</span>
      <span>{{ serverError }}</span>
    </div>

    <div v-if="isDeleteMode" class="m-6 p-4 bg-amber-50 text-amber-800 border border-amber-200 rounded-xl">
      <p class="font-medium">
        ¿Está seguro que desea eliminar este registro?
      </p>
      <p class="text-sm mt-1 opacity-80">
        Esta acción no se puede deshacer y podría afectar el histórico de facturación.
      </p>
    </div>

    <form @submit.prevent="handleSubmit">
      <fieldset :disabled="isDeleteMode" class="disabled:opacity-75">
        <!-- Main Info Grid (Odoo Style) -->
        <div class="p-6 grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-6">
          <!-- Left Column -->
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Nombre del impuesto</label>
              <input
                v-model="form.nombre" type="text" placeholder="Ej: IVA 21%" required 
                class="w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm transition-all duration-200"
              >
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Cálculo de impuestos</label>
              <select
                v-model="form.metodo_calculo" 
                class="w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm transition-all duration-200"
              >
                <option :value="MetodoCalculoImpuestoEnum.PORCENTAJE">
                  Porcentaje
                </option>
                <option :value="MetodoCalculoImpuestoEnum.FIJO">
                  Importe Fijo
                </option>
                <option :value="MetodoCalculoImpuestoEnum.PORCENTAJE_SOBRE_PRECIO">
                  Porcentaje sobre el precio
                </option>
                <option :value="MetodoCalculoImpuestoEnum.GRUPO">
                  Grupo de impuestos
                </option>
              </select>
            </div>
            <div class="flex items-center pt-2">
              <label class="relative inline-flex items-center cursor-pointer">
                <input v-model="form.activo" type="checkbox" class="sr-only peer">
                <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600" />
                <span class="ml-3 text-sm font-medium text-gray-700 uppercase tracking-wide">Activo</span>
              </label>
            </div>
          </div>

          <!-- Right Column -->
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Tipo de impuesto</label>
              <select
                v-model="form.tipo_uso" 
                class="w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm transition-all duration-200"
              >
                <option :value="TipoUsoImpuestoEnum.VENTAS">
                  Ventas
                </option>
                <option :value="TipoUsoImpuestoEnum.COMPRAS">
                  Compras
                </option>
                <option :value="TipoUsoImpuestoEnum.RETENCION_PAGO_PROVEEDOR">
                  Retención Pago Proveedor
                </option>
                <option :value="TipoUsoImpuestoEnum.RETENCION_PAGO_CLIENTE">
                  Retención Pago Cliente
                </option>
                <option :value="TipoUsoImpuestoEnum.OTRO">
                  Otros
                </option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Ámbito del impuesto</label>
              <select
                v-model="form.ambito_uso" 
                class="w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm transition-all duration-200"
              >
                <option :value="AmbitoUsoImpuestoEnum.BIENES">
                  Bienes
                </option>
                <option :value="AmbitoUsoImpuestoEnum.SERVICIOS">
                  Servicios
                </option>
                <option :value="AmbitoUsoImpuestoEnum.AMBOS">
                  Ambos
                </option>
              </select>
            </div>
            <div class="grid grid-cols-5 gap-3">
              <div class="col-span-3">
                <label class="block text-sm font-semibold text-gray-700 mb-1">Importe</label>
                <div class="relative rounded-lg shadow-sm">
                  <input
                    v-model="form.importe" type="number" step="0.0001" 
                    class="block w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500 sm:text-sm pr-8 transition-all duration-200"
                  >
                  <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                    <span class="text-gray-500 sm:text-sm">%</span>
                  </div>
                </div>
              </div>
              <div class="col-span-2">
                <label class="block text-sm font-semibold text-gray-700 mb-1">Cód. AFIP</label>
                <input
                  v-model="form.codigo_afip" type="text" placeholder="Ej: 5" required 
                  class="w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm transition-all duration-200"
                >
              </div>
            </div>
          </div>
        </div>

        <!-- Tabs Navigation -->
        <div class="px-6 border-b border-gray-200">
          <nav class="-mb-px flex space-x-8" aria-label="Tabs">
            <button
              type="button" 
              class="whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-all duration-200" :class="[activeTab === 'definicion' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300']"
              @click="activeTab = 'definicion'"
            >
              Definición
            </button>
            <button
              type="button" 
              class="whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-all duration-200" :class="[activeTab === 'avanzadas' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300']"
              @click="activeTab = 'avanzadas'"
            >
              Opciones avanzadas
            </button>
          </nav>
        </div>

        <!-- Tabs Content -->
        <div class="p-6 bg-gray-50/30">
          <!-- Definicion Tab -->
          <div v-show="activeTab === 'definicion'" class="space-y-8 pb-4">
            <section>
              <h4 class="text-sm font-black text-gray-900 border-b border-gray-100 pb-2 mb-4 uppercase tracking-widest flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Distribución de Facturas
              </h4>
              <p class="text-xs text-gray-500 mb-2 italic">
                Define cómo se distribuye el importe base e impuesto en facturaciones.
              </p>
              <TaxDistributionTable v-model="form.reparticion_facturas" />
            </section>

            <section>
              <h4 class="text-sm font-black text-gray-900 border-b border-gray-100 pb-2 mb-4 uppercase tracking-widest flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2 text-purple-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 15v-1a4 4 0 00-4-4H8m0 0l3 3m-3-3l3-3m9 14V5a2 2 0 00-2-2H6a2 2 0 00-2 2v16l4-2 4 2 4-2 4 2z" />
                </svg>
                Distribución de Reembolsos
              </h4>
              <p class="text-xs text-gray-500 mb-2 italic">
                Define cómo se distribuye el importe base e impuesto en notas de crédito.
              </p>
              <TaxDistributionTable v-model="form.reparticion_reembolsos" />
            </section>Section id: 6448
          </div>

          <!-- Opciones Avanzadas Tab -->
          <div v-show="activeTab === 'avanzadas'" class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <!-- Column 1 -->
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1">Etiqueta en facturas</label>
                <input
                  v-model="form.etiqueta_factura" type="text"
                  class="w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm transition-all duration-200"
                >
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1">Descripción</label>
                <textarea
                  v-model="form.descripcion" rows="2"
                  class="w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm transition-all duration-200"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1">Jurisdicción (Ámbito)</label>
                <select v-model="form.ambito" class="w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm transition-all duration-200">
                  <option :value="AmbitoImpuestoEnum.NACIONAL">
                    Nacional (Argentina)
                  </option>
                  <option :value="AmbitoImpuestoEnum.PROVINCIAL">
                    Provincial
                  </option>
                  <option :value="AmbitoImpuestoEnum.MUNICIPAL">
                    Municipal
                  </option>
                </select>
              </div>
            </div>

            <!-- Column 2 -->
            <div class="space-y-5">
              <div class="flex items-start space-x-3 p-1">
                <div class="flex items-center h-5">
                  <input v-model="form.incluido_precio" type="checkbox" class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded">
                </div>
                <div class="text-sm">
                  <label class="font-semibold text-gray-700">Incluido en el precio</label>
                  <p class="text-gray-500 text-xs">
                    El impuesto ya forma parte del precio de venta/costo.
                  </p>
                </div>
              </div>
              <div class="flex items-start space-x-3 p-1">
                <div class="flex items-center h-5">
                  <input v-model="form.afecta_base_subsecuente" type="checkbox" class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded">
                </div>
                <div class="text-sm">
                  <label class="font-semibold text-gray-700">Afecta la base de los impuestos subsecuentes</label>
                  <p class="text-gray-500 text-xs">
                    Cálculo en cascada (impuesto sobre impuesto).
                  </p>
                </div>
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1">Código de categoría del impuesto</label>
                <select v-model="form.categoria_fiscal" class="w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm transition-all duration-200">
                  <option :value="undefined">
                    --- Seleccionar Categoría ---
                  </option>
                  <option v-for="(label, key) in CategoriaFiscalImpuestoEnum" :key="key" :value="label">
                    {{ label }}
                  </option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </fieldset>

      <!-- Actions -->
      <div class="px-6 py-5 bg-gray-50 border-t border-gray-100 flex justify-end gap-3">
        <button
          type="button" class="px-5 py-2 text-sm font-semibold text-gray-600 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 hover:text-gray-800 transition-all duration-200 focus:ring-2 focus:ring-offset-2 focus:ring-gray-200" 
          @click="$emit('cancel')"
        >
          Descartar
        </button>
            
        <button
          v-if="isDeleteMode" type="submit" 
          class="px-6 py-2 text-sm font-bold text-white bg-red-600 border border-transparent rounded-lg hover:bg-red-700 focus:ring-4 focus:ring-red-200 transition-all duration-200 shadow-md shadow-red-100"
        >
          Confirmar Eliminación
        </button>
        <button
          v-else type="submit" 
          class="px-6 py-2 text-sm font-bold text-white bg-blue-600 border border-transparent rounded-lg hover:bg-blue-700 focus:ring-4 focus:ring-blue-200 transition-all duration-200 shadow-md shadow-blue-100"
        >
          Guardar Cambios
        </button>
      </div>
    </form>
  </div>
</template>

<style scoped>
/* Transiciones suaves para los inputs al deshabilitar */
fieldset:disabled {
  cursor: not-allowed;
}
</style>
