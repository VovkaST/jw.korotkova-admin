<script setup lang="ts">
const props = defineProps<{
  to: string;
}>();
</script>

<template>
  <a :href="`/#${to}`">
    <slot />
  </a>
</template>

<style scoped></style>
