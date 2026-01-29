<script setup lang="ts">
defineProps<{
  type: "success" | "warning" | "error" | "overdue" | "info";
}>();
</script>

<template>
  <span
    :class="[
      'inline-flex items-center px-2 py-1 rounded-md text-xs font-medium',
      `bg-semantic-${type}-bg text-semantic-${type}-fg`
    ]"
  >
    <slot />
  </span>
</template>
