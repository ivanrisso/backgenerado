<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useClientes } from '../../composables/useClientes';
import { useTiposComprobante } from '../../composables/useTiposComprobante';
import { useMonedas } from '../../composables/useMonedas';
import { useConceptos } from '../../composables/useConceptos';
import { useIvas } from '../../composables/useIvas';
import { useCondicionIva } from '../../composables/useCondicionIva';
import { useDomicilios } from '../../composables/useDomicilios';

import { createComprobanteFullUseCase, getLocalidadByIdUseCase, getProvinciaByIdUseCase } from '../../../di';
import { Money } from '../../../domain/value-objects/Money';
import { useComprobantes } from '../../composables/useComprobantes';



const router = useRouter();

// Composables
const { clientes, loadClientes } = useClientes();
const { tiposComprobante, loadTiposComprobante } = useTiposComprobante();
const { monedas, loadMonedas } = useMonedas();
const { conceptos, loadConceptos } = useConceptos();
const { ivas, loadIvas } = useIvas();
const { condicionesIva, loadCondicionesIva } = useCondicionIva();
const { domicilios, loadDomicilios } = useDomicilios();

const { comprobantes, loadComprobantes } = useComprobantes();

// State
const loading = ref(false);
const error = ref<string | null>(null);

// Form State
const cabecera = ref({
    cliente_id: null as number | null,
    tipo_comprobante_id: null as number | null,
    concepto_id: null as number | null,
    tipo_doc_id: null as number | null,
    moneda_id: null as number | null,
    punto_venta: 1, 
    numero: 0, 
    fecha_emision: new Date().toISOString().split('T')[0],
    
    // Client Snapshot
    doc_nro: '',
    nombre_cliente: '',
    cuit_cliente: '',
    domicilio_cliente: '',
    localidad_cliente: '',
    cod_postal_cliente: '',
    provincia_cliente: '',
    
    cotizacion_moneda: 1, 
    observaciones: ''
});

const detalles = ref<Array<{
    descripcion: string;
    cantidad: number;
    precio_unitario: number;
    iva_id: number | null;
}>>([
    { descripcion: '', cantidad: 1, precio_unitario: 0, iva_id: null }
]);


// Autocomplete State
const clientSearchQuery = ref('');
const clientShowSuggestions = ref(false);

const clientFilteredList = computed(() => {
    const query = clientSearchQuery.value.toLowerCase();
    
    // If query is empty and we have customers, maybe show some default? 
    if (!query) return clientes.value.slice(0, 50); 

    return clientes.value.filter(c => 
        c.nombre.toLowerCase().includes(query) || 
        c.apellido.toLowerCase().includes(query) ||
        (c.razon_social && c.razon_social.toLowerCase().includes(query)) ||
        (c.cuit?.value && c.cuit.value.includes(query))
    ).slice(0, 50);
});

const selectClient = (cliente: any) => {
    cabecera.value.cliente_id = cliente.id;
    // Query update is handled by watch now, or we can set it here for instant feedback
    clientSearchQuery.value = cliente.razon_social || `${cliente.nombre} ${cliente.apellido}`;
    clientShowSuggestions.value = false;
};

const handleClientInput = () => {
    // Reset ID on input to force re-selection and ensure validity
    if (cabecera.value.cliente_id) {
        cabecera.value.cliente_id = null;
    }
    clientShowSuggestions.value = true;
};

const handleClientBlur = () => {
    // Delay hiding to allow click
    setTimeout(() => {
        clientShowSuggestions.value = false;
    }, 200);
};

// Computed Totals
const calculatedDetalles = computed(() => {
    return detalles.value.map(d => {
        const neto = d.cantidad * d.precio_unitario;
        let ivaAmount = 0;
        let alicuota = 0;
        
        if (d.iva_id) {
            const ivaObj = ivas.value.find(i => i.id === d.iva_id);
            if (ivaObj) {
               alicuota = Number(ivaObj.porcentaje);
               ivaAmount = neto * (alicuota / 100);
            }
        }
        
        return {
            ...d,
            importe: neto,
            alicuota_iva: alicuota,
            importe_iva: ivaAmount,
            subtotal_con_iva: neto + ivaAmount
        };
    });
});

const totalNeto = computed(() => calculatedDetalles.value.reduce((sum, d) => sum + d.importe, 0));
const totalIva = computed(() => calculatedDetalles.value.reduce((sum, d) => sum + d.importe_iva, 0));
const totalImpuestos = computed(() => 0); 
const totalGeneral = computed(() => totalNeto.value + totalIva.value + totalImpuestos.value);

// Filtered Lists
const ivasTasas = computed(() => ivas.value.filter(i => i.discriminado));

// Watchers
const associatedVoucher = ref({
    tipo_id: null as number | null,
    punto_venta: 1,
    numero: null as number | null
});

const isCreditNote = computed(() => {
    if (!cabecera.value.tipo_comprobante_id) return false;
    const t = tiposComprobante.value.find(x => x.id === cabecera.value.tipo_comprobante_id);
    return t ? t.descripcion.toLowerCase().includes('nota') : false;
});

const clientInvoices = computed(() => {
    if (!cabecera.value.cliente_id) return [];
    // Filter invoices for this client, excluding Credit/Debit Notes
    return comprobantes.value.filter(c => {
        if (c.cliente_id !== cabecera.value.cliente_id) return false;
        const t = tiposComprobante.value.find(type => type.id === c.tipo_comprobante_id);
        
        // Exclude notes (Credit/Debit Notes) -> Only Invoices can be annulled/credited
        const isInvoice = t && !t.descripcion.toLowerCase().includes('nota');
        
        // Filter by Balance > 0
        const hasBalance = c.saldo && c.saldo.amount > 0;
        
        return isInvoice && hasBalance;
    }).sort((a, b) => b.id - a.id);
}); // Newest first

const selectAssociatedInvoice = (invoiceId: number) => {
    const inv = clientInvoices.value.find(c => c.id === invoiceId);
    if (inv) {
        associatedVoucher.value.tipo_id = inv.tipo_comprobante_id;
        associatedVoucher.value.punto_venta = inv.punto_venta;
        associatedVoucher.value.numero = inv.numero;
    }
};

const formatInvoiceLabel = (inv: any) => {
    try {
        const dateStr = new Date(inv.fecha_emision).toLocaleDateString();
        // Handle Money object vs number
        let amount = '0.00';
        let currency = '';
        
        if (typeof inv.total === 'object' && inv.total !== null) {
            amount = Number(inv.total.amount).toFixed(2);
            currency = inv.total.currency || '';
        } else {
            amount = Number(inv.total).toFixed(2);
        }
        
        const saldoAmount = inv.saldo ? Number(inv.saldo.amount).toFixed(2) : amount;
        
        return `${dateStr} - PV ${inv.punto_venta} Nro ${inv.numero} (Total: $${amount} ${currency} / Saldo: $${saldoAmount} ${currency})`;
    } catch (e) {
        return `Inv #${inv.id} (Error display)`;
    }
};

watch(() => cabecera.value.cliente_id, async (newId) => {
    if (!newId) return;
    const cliente = clientes.value.find(c => c.id === newId);
    if (cliente) {
        // Sync Search Query if not matching (important for initial load or programmatic changes)
        const name = cliente.razon_social || `${cliente.nombre} ${cliente.apellido}`;
        if (clientSearchQuery.value !== name) {
            clientSearchQuery.value = name;
        }

        cabecera.value.nombre_cliente = `${cliente.nombre} ${cliente.apellido}`;
        cabecera.value.cuit_cliente = cliente.cuit?.value || '';
        cabecera.value.tipo_doc_id = cliente.tipo_doc_id;
        cabecera.value.doc_nro = cliente.cuit?.value || ''; 
        
        // Address logic
        const clienteDomicilios = domicilios.value.filter(d => d.cliente_id === newId);
        const dom = clienteDomicilios.length > 0 ? clienteDomicilios[0] : null;

        if (dom) {
             cabecera.value.domicilio_cliente = `${dom.calle} ${dom.numero}`;
             
             try {
                const loc = await getLocalidadByIdUseCase.execute(dom.localidad_id);
                if (loc) {
                    cabecera.value.localidad_cliente = loc.nombre;
                    cabecera.value.cod_postal_cliente = loc.codPostal;
                    
                    const prov = await getProvinciaByIdUseCase.execute(loc.provinciaId);
                    if (prov) {
                        cabecera.value.provincia_cliente = prov.nombre;
                    }
                }
             } catch (e) {
                console.error("Error fetching location details", e);
             }
        }
        
        // Auto-select Tipo Comprobante based on Condicion IVA
        if (cliente.iva_id) {
            const ivaCond = condicionesIva.value.find(i => i.id === cliente.iva_id);
            if (ivaCond) {

                // Responsable Inscripto (Code 1) -> Factura A (Code "01")
                // Others -> Factura B (Code "06")
                
                let targetCodeArca = "06"; // Default B
                if (ivaCond.codigo === 1) { // 1 = Responsable Inscripto
                    targetCodeArca = "01"; // A
                }
                
                const tipoCbte = tiposComprobante.value.find(t => t.codigo_arca === targetCodeArca && t.descripcion.includes("Factura")); // Ensure it's a Invoice not Note
                if (tipoCbte) {
                     cabecera.value.tipo_comprobante_id = tipoCbte.id;
                }
            }
        }
    }
});



// Methods
const addItem = () => {
    detalles.value.push({ descripcion: '', cantidad: 1, precio_unitario: 0, iva_id: null });
};

const removeItem = (index: number) => {
    detalles.value.splice(index, 1);
};

const submit = async () => {
    if (!cabecera.value.cliente_id || !cabecera.value.tipo_comprobante_id || !cabecera.value.concepto_id) {
        error.value = "Por favor complete los campos obligatorios.";
        return;
    }

    if (detalles.value.length === 0) {
        error.value = "Debe agregar al menos un item.";
        return;
    }

    if (detalles.value.some(d => !d.iva_id || !d.descripcion || d.cantidad <= 0 || d.precio_unitario < 0)) {
        error.value = "Revise los items: todos deben tener descripción, cantidad, precio e IVA válido.";
        return;
    }

    loading.value = true;
    error.value = null;

    try {
        const payload = {
            ...cabecera.value,
            id: 0,
            fecha_emision: new Date(cabecera.value.fecha_emision as string),
            total_neto: new Money(totalNeto.value),
            total_iva: new Money(totalIva.value),
            total_impuestos: new Money(totalImpuestos.value),
            total: new Money(totalGeneral.value),
            
             cuit_cliente: { value: cabecera.value.cuit_cliente }, 
             
             detalles: calculatedDetalles.value.map(d => ({
                 id: 0,
                 comprobante_id: 0,
                 iva_id: d.iva_id as number,
                 descripcion: d.descripcion,
                 cantidad: d.cantidad,
                 precio_unitario: new Money(d.precio_unitario),
                 importe: new Money(d.importe),
                 alicuota_iva: d.alicuota_iva,
                 importe_iva: new Money(d.importe_iva)
             })),
             impuestos: [] 
        };

        if (isCreditNote.value) {
            if (!associatedVoucher.value.tipo_id || !associatedVoucher.value.numero) {
                error.value = "Para Nota de Crédito debe indicar el comprobante asociado.";
                loading.value = false;
                return;
            }
            const assocType = tiposComprobante.value.find(t => t.id === associatedVoucher.value.tipo_id);
            if (assocType) {
                // Add to payload
                 (payload as any).cbtes_asociados = [{
                    Tipo: Number(assocType.codigo_arca),
                    PtoVta: associatedVoucher.value.punto_venta,
                    Nro: associatedVoucher.value.numero
                }];
            }
        }

        await createComprobanteFullUseCase.execute(payload as any);
        
        router.push({ name: 'comprobantes' }); 
    } catch (e: any) {
        error.value = e.message || "Error al generar comprobante";
    } finally {
        loading.value = false;
    }
};

onMounted(async () => {
    await Promise.all([
        loadClientes(),
        loadTiposComprobante(),
        loadMonedas(),
        loadConceptos(),
        loadIvas(),
        loadCondicionesIva(),
        loadDomicilios(),
        loadComprobantes()

    ]);
});
</script>

<template>
  <div class="min-h-screen bg-gray-50 pb-12">
    <!-- Header -->
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
        <h1 class="text-3xl font-bold text-gray-900">
          Nueva Factura
        </h1>
      </div>
    </header>

    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="bg-white shadow px-4 py-5 sm:rounded-lg sm:p-6">
        <!-- Error Message -->
        <div v-if="error" class="mb-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative">
          {{ error }}
        </div>

        <form class="space-y-8 divide-y divide-gray-200" @submit.prevent="submit">
          <!-- Cabecera -->
          <div class="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6 pt-4">
            <!-- Cliente Autocomplete -->
            <div class="sm:col-span-4 relative">
              <label class="block text-sm font-medium text-gray-700">Cliente</label>
              <div class="relative mt-1">
                <input 
                  v-model="clientSearchQuery" 
                  type="text" 
                  class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm pl-3 pr-10 py-2"
                  placeholder="Buscar cliente..."
                  autocomplete="off"
                  @focus="clientShowSuggestions = true" 
                  @blur="handleClientBlur"
                  @input="handleClientInput"
                >
                <!-- Arrow/Icon -->
                <div class="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
                  <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fill-rule="evenodd" d="M10 3a1 1 0 01.707.293l3 3a1 1 0 01-1.414 1.414L10 5.414 7.707 7.707a1 1 0 01-1.414-1.414l3-3A1 1 0 0110 3zm-3.707 9.293a1 1 0 011.414 0L10 14.586l2.293-2.293a1 1 0 011.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd" />
                  </svg>
                </div>
              </div>

              <!-- Suggestions -->
              <div v-if="clientShowSuggestions && clientFilteredList.length > 0" class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                <ul tabindex="-1" role="listbox">
                  <li 
                    v-for="c in clientFilteredList" 
                    :key="c.id" 
                    class="relative cursor-default select-none py-2 pl-3 pr-9 hover:bg-blue-100 text-gray-900"
                    role="option"
                    @click="selectClient(c)"
                  >
                    <div class="flex flex-col">
                      <span class="block truncate font-normal">
                        {{ c.nombre }} {{ c.apellido }}
                      </span>
                      <span class="block truncate text-xs text-gray-500">
                        {{ c.razon_social ? `${c.razon_social } - ` : '' }} CUIT: {{ c.cuit?.value || 'S/C' }}
                      </span>
                    </div>
                  </li>
                </ul>
              </div>
            </div>

            <div class="sm:col-span-2">
              <label class="block text-sm font-medium text-gray-700">Fecha Emisión</label>
              <input v-model="cabecera.fecha_emision" type="date" class="mt-1 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md py-2 px-3 focus:ring-blue-500 focus:border-blue-500">
            </div>

            <!-- Associated Voucher (Only for Credit Notes) -->
            <div v-if="isCreditNote" class="sm:col-span-6 bg-yellow-50 p-4 rounded-md border border-yellow-200 mt-2 grid grid-cols-1 sm:grid-cols-3 gap-4">
              <h4 class="sm:col-span-3 text-sm font-medium text-yellow-800 mb-2">
                Comprobante Asociado (Requerido para Nota de Crédito)
              </h4>
                            
              <!-- Search Helper -->
              <div class="sm:col-span-3">
                <label class="block text-xs font-medium text-gray-700 mb-1">Buscar Comprobante del Cliente</label>
                <select class="block w-full py-1 px-2 border border-gray-300 bg-white rounded-md shadow-sm sm:text-xs" @change="selectAssociatedInvoice(Number(($event.target as HTMLSelectElement).value))">
                  <option value="">
                    -- Seleccionar Comprobante a Anular --
                  </option>
                  <option v-for="inv in clientInvoices" :key="inv.id" :value="inv.id">
                    {{ formatInvoiceLabel(inv) }}
                  </option>
                </select>
              </div>

              <div>
                <label class="block text-xs font-medium text-gray-700">Tipo Cbte. Orig.</label>
                <select v-model="associatedVoucher.tipo_id" class="mt-1 block w-full py-1 px-2 border border-gray-300 bg-white rounded-md shadow-sm sm:text-xs">
                  <option v-for="t in tiposComprobante" :key="t.id" :value="t.id">
                    {{ t.descripcion }}
                  </option>
                </select>
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-700">Pto. Vta.</label>
                <input v-model.number="associatedVoucher.punto_venta" type="number" class="mt-1 block w-full py-1 px-2 border border-gray-300 rounded-md shadow-sm sm:text-xs">
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-700">Número</label>
                <input v-model.number="associatedVoucher.numero" type="number" class="mt-1 block w-full py-1 px-2 border border-gray-300 rounded-md shadow-sm sm:text-xs">
              </div>
            </div>

            <!-- Config -->
            <div class="sm:col-span-2">
              <label class="block text-sm font-medium text-gray-700">Tipo Comprobante</label>
              <select v-model="cabecera.tipo_comprobante_id" class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
                <option v-for="t in tiposComprobante" :key="t.id" :value="t.id">
                  {{ t.descripcion }}
                </option>
              </select>
            </div>

            <div class="sm:col-span-2">
              <label class="block text-sm font-medium text-gray-700">Concepto</label>
              <select v-model="cabecera.concepto_id" class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
                <option v-for="c in conceptos" :key="c.id" :value="c.id">
                  {{ c.descripcion }}
                </option>
              </select>
            </div>
                        
            <div class="sm:col-span-2">
              <label class="block text-sm font-medium text-gray-700">Moneda</label>
              <select v-model="cabecera.moneda_id" class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
                <option v-for="m in monedas" :key="m.id" :value="m.id">
                  {{ m.descripcion }}
                </option>
              </select>
            </div>
          </div>

          <!-- Detalles -->
          <div class="pt-8">
            <h3 class="text-lg leading-6 font-medium text-gray-900">
              Items
            </h3>
            <div class="mt-4 flex flex-col">
              <div class="-my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
                <div class="py-2 align-middle inline-block min-w-full sm:px-6 lg:px-8">
                  <div class="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg">
                    <table class="min-w-full divide-y divide-gray-200">
                      <thead class="bg-gray-50">
                        <tr>
                          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Descripción
                          </th>
                          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-24">
                            Cant.
                          </th>
                          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-32">
                            Precio Unit.
                          </th>
                          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-32">
                            IVA
                          </th>
                          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-32">
                            Subtotal
                          </th>
                          <th scope="col" class="relative px-6 py-3">
                            <span class="sr-only">Acciones</span>
                          </th>
                        </tr>
                      </thead>
                      <tbody class="bg-white divide-y divide-gray-200">
                        <tr v-for="(detalle, index) in detalles" :key="index">
                          <td class="px-6 py-4 whitespace-nowrap">
                            <input v-model="detalle.descripcion" type="text" class="focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md">
                          </td>
                          <td class="px-6 py-4 whitespace-nowrap">
                            <input v-model.number="detalle.cantidad" type="number" step="0.01" class="focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md">
                          </td>
                          <td class="px-6 py-4 whitespace-nowrap">
                            <input v-model.number="detalle.precio_unitario" type="number" step="0.01" class="focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md">
                          </td>
                          <td class="px-6 py-4 whitespace-nowrap">
                            <select v-model="detalle.iva_id" class="block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none sm:text-sm">
                              <option v-for="iva in ivasTasas" :key="iva.id" :value="iva.id">
                                {{ iva.descripcion }}
                              </option>
                            </select>
                          </td>
                          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            $ {{ calculatedDetalles[index] ? calculatedDetalles[index].importe.toFixed(2) : '0.00' }}
                          </td>
                          <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                            <button type="button" class="text-red-600 hover:text-red-900" @click="removeItem(index)">
                              Eliminar
                            </button>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
            <div class="mt-4">
              <button type="button" class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-blue-700 bg-blue-100 hover:bg-blue-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500" @click="addItem">
                + Agregar Item
              </button>
            </div>
          </div>

          <!-- Totales -->
          <div class="pt-8">
            <dl class="space-y-2 text-right">
              <div class="flex justify-end gap-4">
                <dt class="text-sm font-medium text-gray-500">
                  Subtotal Neto:
                </dt>
                <dd class="text-sm font-medium text-gray-900">
                  $ {{ totalNeto.toFixed(2) }}
                </dd>
              </div>
              <div class="flex justify-end gap-4">
                <dt class="text-sm font-medium text-gray-500">
                  IVA Total:
                </dt>
                <dd class="text-sm font-medium text-gray-900">
                  $ {{ totalIva.toFixed(2) }}
                </dd>
              </div>
              <div class="flex justify-end gap-4 border-t border-gray-200 pt-2">
                <dt class="text-base font-bold text-gray-900">
                  Total:
                </dt>
                <dd class="text-base font-bold text-blue-600">
                  $ {{ totalGeneral.toFixed(2) }}
                </dd>
              </div>
            </dl>
          </div>

          <!-- Actions -->
          <div class="pt-5">
            <div class="flex justify-end">
              <button type="button" class="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none" @click="router.back()">
                Cancelar
              </button>
              <button type="submit" :disabled="loading" class="ml-3 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none disabled:opacity-50">
                {{ loading ? 'Generando...' : 'Generar Comprobante' }}
              </button>
            </div>
          </div>
        </form>
      </div>
    </main>
  </div>
</template>
