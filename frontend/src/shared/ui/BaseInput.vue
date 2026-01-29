<script setup lang="ts">
defineProps<{ modelValue: string }>();
const emit = defineEmits(["update:modelValue"]);

const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement;
  emit("update:modelValue", target.value);
};
</script>

<template>
  <input
    class="h-10 w-full rounded-md border border-border px-3 text-sm
           focus:outline-none focus:ring-2 focus:ring-primary/30"
    :value="modelValue"
    @input="handleInput"
  />
</template>
