<script setup lang="ts">
defineProps<{
  variant?: "primary" | "secondary" | "ghost";
}>();
</script>

<template>
  <button
    :class="[
      'h-10 px-4 rounded-xl text-sm font-medium transition focus:outline-none focus:ring-2',
      variant === 'primary' && 'bg-primary text-white hover:bg-opacity-90 focus:ring-primary/30',
      variant === 'secondary' && 'bg-white border border-border text-text-primary hover:bg-gray-50',
      variant === 'ghost' && 'bg-transparent text-text-muted hover:bg-gray-100'
    ]"
  >
    <slot />
  </button>
</template>
