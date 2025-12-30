
<template>
    <div class="mt-4 overflow-hidden border border-gray-100 rounded-xl">
        <table class="min-w-full divide-y divide-gray-100">
            <thead class="bg-gray-50/50">
                <tr>
                    <th scope="col" class="px-4 py-3 text-left text-[10px] font-black transform uppercase tracking-widest text-gray-400">%</th>
                    <th scope="col" class="px-4 py-3 text-left text-[10px] font-black transform uppercase tracking-widest text-gray-400">Con base en</th>
                    <th scope="col" class="px-4 py-3 text-left text-[10px] font-black transform uppercase tracking-widest text-gray-400">Cuenta</th>
                    <th scope="col" class="px-4 py-3 text-left text-[10px] font-black transform uppercase tracking-widest text-gray-400">Etiquetas de impuestos</th>
                    <th scope="col" class="relative px-4 py-3">
                        <span class="sr-only">Acciones</span>
                    </th>
                </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-50">
                <tr v-for="(line, index) in lines" :key="index" class="group hover:bg-gray-50/50 transition-colors">
                    <td class="px-4 py-2 whitespace-nowrap">
                        <input type="number" step="0.01" v-model.number="line.factor_porcentaje" 
                               class="w-20 px-2 py-1 text-sm font-bold bg-transparent border-b border-transparent focus:border-blue-500 focus:ring-0 outline-none transition-all" />
                    </td>
                    <td class="px-4 py-2 whitespace-nowrap text-sm text-gray-500">
                        <select v-model="line.basado_en"
                                class="bg-transparent border-b border-transparent focus:border-blue-500 focus:ring-0 text-sm font-medium outline-none cursor-pointer">
                            <option value="base">Base</option>
                            <option value="impuesto">de impuesto</option>
                        </select>
                    </td>
                    <td class="px-4 py-2 whitespace-nowrap">
                        <input type="text" v-model="line.cuenta_contable" placeholder="Cuenta contable..."
                               class="w-full px-2 py-1 text-sm bg-transparent border-b border-transparent focus:border-blue-500 focus:ring-0 outline-none placeholder:text-gray-300 transition-all font-medium" />
                    </td>
                    <td class="px-4 py-2">
                        <div class="flex flex-wrap gap-1">
                             <input type="text" v-model="line.etiqueta_nombre" placeholder="Etiqueta Libro IVA..."
                                    class="w-full px-2 py-1 text-sm bg-transparent border-b border-transparent focus:border-blue-500 focus:ring-0 outline-none placeholder:text-gray-300 transition-all font-bold text-blue-600" />
                        </div>
                    </td>
                    <td class="px-4 py-2 whitespace-nowrap text-right text-sm font-medium">
                        <button @click="removeLine(index)" class="text-gray-300 hover:text-red-500 transition-colors opacity-0 group-hover:opacity-100">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                            </svg>
                        </button>
                    </td>
                </tr>
                <tr v-if="lines.length === 0">
                    <td colspan="5" class="px-4 py-8 text-center">
                        <span class="text-xs font-bold text-gray-300 uppercase tracking-widest italic">No hay reglas de distribución definidas</span>
                    </td>
                </tr>
            </tbody>
        </table>
        
        <div class="p-3 bg-gray-50/30 border-t border-gray-50">
            <button @click="addLine" 
                    class="inline-flex items-center text-[11px] font-black text-blue-600 hover:text-blue-700 uppercase tracking-widest transition-all group">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-1 transform group-hover:scale-125 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="4" d="M12 4v16m8-8H4" />
                </svg>
                Agregar una línea
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';

const props = defineProps<{
    modelValue: any[]
}>();

const emit = defineEmits(['update:modelValue']);

// Local working copy to facilitate editing
// We map etiqueta_id/etiqueta to a temporary etiqueta_nombre for simplicity in this version
const lines = ref(props.modelValue.map(l => ({
    ...l,
    etiqueta_nombre: l.etiqueta?.nombre || ''
})));

watch(lines, (newLines) => {
    emit('update:modelValue', newLines);
}, { deep: true });

const addLine = () => {
    lines.value.push({
        factor_porcentaje: 100.0,
        basado_en: 'impuesto',
        cuenta_contable: '',
        etiqueta_nombre: ''
    });
};

const removeLine = (index: number) => {
    lines.value.splice(index, 1);
};
</script>
