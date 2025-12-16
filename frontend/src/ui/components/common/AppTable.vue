<template>
  <div class="overflow-x-auto">
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          <th v-for="col in columns" :key="col.key" scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            {{ col.label }}
          </th>
          <th scope="col" class="relative px-6 py-3">
            <span class="sr-only">Actions</span>
          </th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        <tr v-if="loading">
            <td :colspan="columns.length + 1" class="px-6 py-4 text-center">Loading...</td>
        </tr>
        <tr v-else-if="!data || data.length === 0">
             <td :colspan="columns.length + 1" class="px-6 py-4 text-center">No data found</td>
        </tr>
        <tr v-else v-for="item in data" :key="item.id">
          <td v-for="col in columns" :key="col.key" class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
            <slot :name="col.key" :value="item[col.key]" :item="item">
              {{ item[col.key] }}
            </slot>
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
            <button @click="$emit('edit', item)" class="text-indigo-600 hover:text-indigo-900 mr-4">Edit</button>
            <button @click="$emit('delete', item)" class="text-red-600 hover:text-red-900">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  columns: { key: string; label: string }[];
  data: any[];
  loading?: boolean;
}>();

defineEmits(['edit', 'delete']);
</script>
