<template>
  <div class="bg-surface rounded-lg shadow-sm overflow-hidden">
    <table class="w-full text-sm">
      <thead class="bg-gray-50 text-text-muted">
        <tr>
          <slot name="header" />
        </tr>
      </thead>
      <tbody>
        <slot />
      </tbody>
    </table>
  </div>
</template>
