<template>
    <div class="table-container">
        <table class="min-w-full">
            <thead>
                <tr>
                    <th v-for="col in columns" :key="col.key" :class="['table-header', col.class]">
                        {{ col.label }}
                    </th>
                    <th v-if="actions" class="table-header text-right">Acciones</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-50">
                <tr v-for="(item, index) in items" :key="index" class="table-row group">
                    <td v-for="col in columns" :key="col.key" :class="['table-cell', col.cellClass]">
                        <slot :name="`cell-${col.key}`" :item="item" :value="getValue(item, col.key)">
                            {{ getValue(item, col.key) }}
                        </slot>
                    </td>
                    <td v-if="actions" class="table-cell text-right">
                        <div class="flex justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                            <slot name="actions" :item="item"></slot>
                        </div>
                    </td>
                </tr>
                <tr v-if="items.length === 0">
                    <td :colspan="columns.length + (actions ? 1 : 0)" class="px-6 py-12 text-center text-gray-400">
                        <slot name="empty">No hay registros.</slot>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';

const props = defineProps<{
    columns: Array<{ key: string, label: string, class?: string, cellClass?: string }>;
    items: Array<any>;
    actions?: boolean;
}>();

const getValue = (item: any, key: string) => {
    // Support nested keys like 'info.value' or simple keys
    if (!key) return '';
    return key.split('.').reduce((o, i) => (o ? o[i] : null), item);
};
</script>
