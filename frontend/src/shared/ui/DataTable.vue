<script setup lang="ts">
import BaseTable from './BaseTable.vue';

defineProps<{
  columns: { key: string; label: string }[];
  items: any[];
  actions?: boolean;
}>();

defineEmits<{
  (e: 'edit', item: any): void;
  (e: 'delete', item: any): void;
}>();
</script>

<template>
  <BaseTable>
    <template #header>
      <th v-for="col in columns" :key="col.key" class="text-left py-3 px-4 font-semibold text-gray-600">
        {{ col.label }}
      </th>
      <th v-if="actions" class="text-right py-3 px-4 font-semibold text-gray-600">
        Acciones
      </th>
    </template>

    <tr v-for="(item, index) in items" :key="item.id || index" class="border-b last:border-0 hover:bg-gray-50 transition-colors">
      <td v-for="col in columns" :key="col.key" class="py-3 px-4">
        <!-- Slot dinámico por columna -->
        <slot :name="`cell-${col.key}`" :item="item">
          {{ item[col.key] }}
        </slot>
      </td>
      <td v-if="actions" class="py-3 px-4 text-right">
        <div class="flex justify-end gap-2">
          <slot name="actions" :item="item" />
        </div>
      </td>
    </tr>
  </BaseTable>
</template>
