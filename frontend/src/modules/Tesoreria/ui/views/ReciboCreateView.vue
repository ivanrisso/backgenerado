<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { httpClient } from '../../../../shared/http/client';
import { ReciboService } from '../../infrastructure/api/ReciboService';
import type { ImputacionCreate } from '../../domain/models/Recibo';

const router = useRouter();

// State
const clientes = ref<any[]>([]);
const comprobantesPendientes = ref<any[]>([]);
const selectedClientId = ref<number | null>(null);
const clientSearchQuery = ref('');
const clientShowSuggestions = ref(false);

const form = ref({
    fecha_emision: new Date().toISOString().split('T')[0],
    punto_venta: 1, // Default or fetch
    total: 0,
    observaciones: '',
    imputaciones: [] as ImputacionCreate[]
});

const isSubmitting = ref(false);
const errorMsg = ref('');

// Computed
const clientFilteredList = computed(() => {
    const query = clientSearchQuery.value.toLowerCase();
    if (!query) return clientes.value.slice(0, 50);
    return clientes.value.filter((c: any) => 
        c.nombre.toLowerCase().includes(query) || 
        c.apellido.toLowerCase().includes(query) ||
        (c.razon_social && c.razon_social.toLowerCase().includes(query)) ||
        (c.cuit && c.cuit.includes(query))
    ).slice(0, 50);
});

// Methods
const handleClientBlur = () => {
    setTimeout(() => {
        clientShowSuggestions.value = false;
    }, 200);
};

const loadClientes = async () => {
    try {
        const res = await httpClient.get('/clientes');
        clientes.value = res.data;
    } catch (e) {
        console.error("Error loading clientes", e);
    }
};

const loadDeudas = async () => {
    if (!selectedClientId.value) return;
    try {
        const res = await httpClient.get(`/comprobantes/by_cliente/${selectedClientId.value}`);
        // Filter those with saldo > 0 AND type NOT Receipt (if receipts were returned)
        // Ideally backend filters, but we do client side
        comprobantesPendientes.value = res.data.filter((c: any) => c.saldo > 0);
    } catch (e) {
        console.error("Error loading deudas", e);
    }
};

const selectCliente = (cliente: any) => {
    selectedClientId.value = cliente.id;
    clientSearchQuery.value = cliente.razon_social || `${cliente.nombre} ${cliente.apellido}`;
    clientShowSuggestions.value = false;
    loadDeudas();
};

const autoImputar = () => {
    let remaining = form.value.total;
    const newImputaciones: ImputacionCreate[] = [];
    
    // Sort debts by date? Oldest first
    const debts = [...comprobantesPendientes.value].sort((a, b) => new Date(a.fecha_emision).getTime() - new Date(b.fecha_emision).getTime());

    for (const debt of debts) {
        if (remaining <= 0) break;
        const amountToApply = Math.min(debt.saldo, remaining);
        newImputaciones.push({
            comprobante_deuda_id: debt.id,
            importe: amountToApply
        });
        remaining -= amountToApply;
    }
    form.value.imputaciones = newImputaciones;
};

const submit = async () => {
    if (!selectedClientId.value) {
        errorMsg.value = "Seleccione un cliente";
        return;
    }
    if (form.value.total <= 0) {
        errorMsg.value = "El total debe ser mayor a 0";
        return;
    }

    isSubmitting.value = true;
    errorMsg.value = '';

    try {
        await ReciboService.create({
            cliente_id: selectedClientId.value,
            fecha_emision: form.value.fecha_emision,
            punto_venta: form.value.punto_venta,
            total: form.value.total,
            observaciones: form.value.observaciones,
            imputaciones: form.value.imputaciones
        });
        alert("Recibo creado exitosamente");
        router.push('/cuentacorriente'); // Go to CC view
    } catch (e: any) {
        errorMsg.value = (e as any).response?.data?.detail || "Error al crear recibo";
    } finally {
        isSubmitting.value = false;
    }
};

onMounted(() => {
    loadClientes();
});
</script>

<template>
    <div class="p-6">
        <h1 class="text-2xl font-bold mb-6 text-gray-800">Nuevo Recibo de Cobranza</h1>

        <div class="bg-white p-6 rounded-lg shadow space-y-6">
            
            <!-- Cliente -->
            <div>
                <label class="block text-sm font-medium text-gray-700">Cliente</label>
                <div class="relative mt-1">
                    <input 
                        v-model="clientSearchQuery" 
                        type="text" 
                        class="block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                        placeholder="Buscar cliente..."
                        @focus="clientShowSuggestions = true"
                        @blur="handleClientBlur"
                    />
                    <ul v-if="clientShowSuggestions && clientFilteredList.length" class="absolute z-10 w-full bg-white border border-gray-300 rounded-md mt-1 max-h-60 overflow-auto shadow-lg">
                        <li v-for="c in clientFilteredList" :key="c.id" 
                            class="px-4 py-2 hover:bg-blue-100 cursor-pointer text-sm"
                            @mousedown.prevent="selectCliente(c)"
                        >
                            {{ c.razon_social || c.nombre + ' ' + c.apellido }} ({{ c.cuit }})
                        </li>
                    </ul>
                </div>
            </div>

            <!-- Datos Recibo -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700">Fecha Emisión</label>
                    <input v-model="form.fecha_emision" type="date" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 sm:text-sm" />
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700">Punto de Venta</label>
                    <input v-model.number="form.punto_venta" type="number" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 sm:text-sm" />
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700">Importe Total</label>
                    <div class="relative mt-1 rounded-md shadow-sm">
                        <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                          <span class="text-gray-500 sm:text-sm">$</span>
                        </div>
                        <input v-model.number="form.total" type="number" step="0.01" class="block w-full rounded-md border-gray-300 pl-7 pr-12 focus:border-blue-500 focus:ring-blue-500 sm:text-sm" placeholder="0.00" />
                    </div>
                </div>
            </div>

            <div>
                <label class="block text-sm font-medium text-gray-700">Observaciones</label>
                <textarea v-model="form.observaciones" rows="2" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 sm:text-sm"></textarea>
            </div>

            <!-- Imputaciones -->
            <div v-if="selectedClientId" class="border-t pt-4">
                <div class="flex justify-between items-center mb-4">
                    <h3 class="text-lg font-medium text-gray-900">Imputación a Facturas</h3>
                    <button type="button" @click="autoImputar" class="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-full shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none">
                        Auto-Imputar (Antigüedad)
                    </button>
                </div>

                <div v-if="comprobantesPendientes.length === 0" class="text-sm text-gray-500 italic">
                    El cliente no tiene facturas con saldo pendiente. Se generará un saldo a favor.
                </div>

                <div v-else class="space-y-2">
                    <div v-for="debt in comprobantesPendientes" :key="debt.id" class="flex items-center justify-between bg-gray-50 p-3 rounded border">
                        <div class="text-sm">
                            <span class="font-bold">{{ debt.tipo_comprobante_id }}</span> <!-- TODO: Map Name -->
                            Nro: {{ debt.numero }} - Fecha: {{ new Date(debt.fecha_emision).toLocaleDateString() }}
                            <div class="text-gray-500">Saldo: ${{ debt.saldo }}</div>
                        </div>
                        <div class="w-32">
                             <!-- Check if this debt is in imputaciones list -->
                            <input 
                                :value="form.imputaciones.find(i => i.comprobante_deuda_id === debt.id)?.importe || 0"
                                @input="(e: any) => {
                                    const val = Number(e.target.value);
                                    const idx = form.imputaciones.findIndex(i => i.comprobante_deuda_id === debt.id);
                                    if (val > 0) {
                                        if (idx >= 0) form.imputaciones[idx].importe = val;
                                        else form.imputaciones.push({ comprobante_deuda_id: debt.id, importe: val });
                                    } else {
                                        if (idx >= 0) form.imputaciones.splice(idx, 1);
                                    }
                                }"
                                type="number" 
                                class="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md text-right" 
                            />
                        </div>
                    </div>
                    <div class="text-right text-sm font-bold text-gray-700 mt-2">
                        Total Imputado: ${{ form.imputaciones.reduce((sum, i) => sum + i.importe, 0).toFixed(2) }}
                    </div>
                </div>
            </div>

            <!-- Botones -->
            <div class="flex justify-end pt-4 space-x-3">
                <button type="button" @click="router.back()" class="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                    Cancelar
                </button>
                <button type="button" @click="submit" :disabled="isSubmitting" class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50">
                    {{ isSubmitting ? 'Guardando...' : 'Crear Recibo' }}
                </button>
            </div>
            
            <div v-if="errorMsg" class="text-red-600 text-sm font-bold text-center">
                {{ errorMsg }}
            </div>
        </div>
    </div>
</template>
