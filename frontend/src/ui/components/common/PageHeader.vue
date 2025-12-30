<template>
    <div class="flex justify-between items-start mb-8">
        <div>
            <h1 class="text-3xl font-bold text-[#092e6a] mb-1">{{ title }}</h1>
            <p v-if="subtitle" class="text-gray-500 text-sm">{{ subtitle }}</p>
        </div>
        <div v-if="$slots.actions">
             <slot name="actions"></slot>
        </div>
    </div>
</template>

<script setup lang="ts">
defineProps<{
    title: string;
    subtitle?: string;
}>();
</script>
